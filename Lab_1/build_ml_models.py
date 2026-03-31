from __future__ import annotations

from pathlib import Path
from datetime import datetime, date
import json
from typing import Dict, List, Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    silhouette_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


START_DATE = date(2026, 2, 19)
END_DATE = date(2026, 3, 20)
RANDOM_STATE = 42

COLUMN_MAP = {
    "id": "product_id",
    "ten_san_pham": "product_name",
    "danh_muc": "category",
    "gia_ban": "selling_price",
    "gia_goc": "original_price",
    "so_luong_da_ban": "cumulative_units_sold",
    "diem_danh_gia": "rating_score",
    "so_luot_nhan_xet": "review_count",
    "dia_diem_kho": "warehouse_location",
    "ton_kho": "stock_status",
    "thuong_hieu": "brand_name",
    "link_san_pham": "product_url",
    "so_luong_ban_trong_ngay": "daily_units_sold",
    "doanh_thu_ngay": "daily_revenue",
}


def parse_folder_date(folder_name: str) -> date | None:
    try:
        return datetime.strptime(folder_name, "%m-%d-%Y").date()
    except ValueError:
        return None


def load_sales_data(sales_root: Path, start_date: date, end_date: date) -> pd.DataFrame:
    records: List[pd.DataFrame] = []

    for folder in sorted(sales_root.iterdir()):
        if not folder.is_dir():
            continue

        folder_date = parse_folder_date(folder.name)
        if folder_date is None or folder_date < start_date or folder_date > end_date:
            continue

        csv_path = folder / "products.csv"
        if not csv_path.exists():
            continue

        df = pd.read_csv(csv_path)
        df["snapshot_date"] = pd.to_datetime(folder_date)
        records.append(df)

    if not records:
        raise FileNotFoundError(
            f"No sales CSV files found in {sales_root} for the date range {start_date} to {end_date}."
        )

    combined = pd.concat(records, ignore_index=True)
    return combined


def clean_sales_data(raw_df: pd.DataFrame) -> pd.DataFrame:
    df = raw_df.rename(columns=COLUMN_MAP).copy()

    expected_columns = list(COLUMN_MAP.values()) + ["snapshot_date"]
    for col in expected_columns:
        if col not in df.columns:
            df[col] = np.nan

    numeric_cols = [
        "selling_price",
        "original_price",
        "cumulative_units_sold",
        "rating_score",
        "review_count",
        "daily_units_sold",
        "daily_revenue",
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    for col in ["product_id", "product_name", "category", "warehouse_location", "stock_status", "brand_name"]:
        df[col] = df[col].astype(str).str.strip()

    df["snapshot_date"] = pd.to_datetime(df["snapshot_date"], errors="coerce")
    df = df.dropna(subset=["snapshot_date"])

    # Feature engineering
    df["discount_rate"] = np.where(
        (df["original_price"] > 0) & df["original_price"].notna(),
        (df["original_price"] - df["selling_price"]) / df["original_price"],
        0.0,
    )
    df["discount_rate"] = df["discount_rate"].clip(lower=0.0, upper=1.0)

    df["is_in_stock"] = df["stock_status"].str.contains("Còn", case=False, na=False).astype(int)
    df["day_of_week"] = df["snapshot_date"].dt.dayofweek
    df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)

    # Fill common numeric gaps with 0 for transaction fields
    for col in ["daily_units_sold", "daily_revenue", "review_count", "cumulative_units_sold"]:
        df[col] = df[col].fillna(0)

    return df


def build_preprocessor(numeric_features: List[str], categorical_features: List[str]) -> ColumnTransformer:
    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )


def get_time_split_dates(df: pd.DataFrame, date_col: str = "snapshot_date", test_fraction: float = 0.2) -> Tuple[List[pd.Timestamp], List[pd.Timestamp]]:
    unique_dates = sorted(pd.to_datetime(df[date_col].dropna()).dt.normalize().unique())
    if len(unique_dates) < 2:
        raise ValueError("At least two distinct dates are required for a time-based train/test split.")

    split_idx = max(1, int(len(unique_dates) * (1 - test_fraction)))
    if split_idx >= len(unique_dates):
        split_idx = len(unique_dates) - 1

    train_dates = list(unique_dates[:split_idx])
    test_dates = list(unique_dates[split_idx:])
    return train_dates, test_dates


def time_based_train_test_split(
    df: pd.DataFrame,
    feature_cols: List[str],
    target_col: str,
    date_col: str = "snapshot_date",
    test_fraction: float = 0.2,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, List[pd.Timestamp], List[pd.Timestamp]]:
    train_dates, test_dates = get_time_split_dates(df, date_col=date_col, test_fraction=test_fraction)

    train_mask = df[date_col].dt.normalize().isin(train_dates)
    test_mask = df[date_col].dt.normalize().isin(test_dates)

    X_train = df.loc[train_mask, feature_cols]
    X_test = df.loc[test_mask, feature_cols]
    y_train = df.loc[train_mask, target_col]
    y_test = df.loc[test_mask, target_col]

    if X_train.empty or X_test.empty:
        raise ValueError("Time-based split produced an empty training or test set.")

    return X_train, X_test, y_train, y_test, train_dates, test_dates


def evaluate_regression_models(df: pd.DataFrame, output_dir: Path) -> Tuple[pd.DataFrame, Pipeline, str, pd.DataFrame]:
    target_col = "daily_units_sold"

    numeric_features = [
        "selling_price",
        "original_price",
        "discount_rate",
        "rating_score",
        "review_count",
        "cumulative_units_sold",
        "day_of_week",
        "is_weekend",
        "is_in_stock",
    ]
    categorical_features = ["category", "warehouse_location", "stock_status"]

    model_df = df.dropna(subset=[target_col]).copy()
    model_df = model_df.sort_values("snapshot_date")
    feature_cols = numeric_features + categorical_features

    X_train, X_test, y_train, y_test, train_dates, test_dates = time_based_train_test_split(
        model_df,
        feature_cols=feature_cols,
        target_col=target_col,
    )

    preprocessor = build_preprocessor(numeric_features, categorical_features)

    models: Dict[str, object] = {
        "baseline_dummy": DummyRegressor(strategy="mean"),
        "linear_regression": LinearRegression(),
        "random_forest": RandomForestRegressor(
            n_estimators=300,
            random_state=RANDOM_STATE,
            n_jobs=-1,
        ),
        "gradient_boosting": GradientBoostingRegressor(random_state=RANDOM_STATE),
    }

    metrics = []
    fitted_pipelines: Dict[str, Pipeline] = {}

    for name, model in models.items():
        pipeline = Pipeline(
            steps=[
                ("preprocess", preprocessor),
                ("model", model),
            ]
        )
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)

        rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))
        mae = float(mean_absolute_error(y_test, y_pred))
        r2 = float(r2_score(y_test, y_pred))

        metrics.append({
            "model": name,
            "mae": mae,
            "rmse": rmse,
            "r2": r2,
            "train_start_date": pd.Timestamp(train_dates[0]).date().isoformat(),
            "train_end_date": pd.Timestamp(train_dates[-1]).date().isoformat(),
            "test_start_date": pd.Timestamp(test_dates[0]).date().isoformat(),
            "test_end_date": pd.Timestamp(test_dates[-1]).date().isoformat(),
        })
        fitted_pipelines[name] = pipeline

    metrics_df = pd.DataFrame(metrics).sort_values(by="mae", ascending=True).reset_index(drop=True)
    best_model_name = metrics_df.loc[0, "model"]
    best_pipeline = fitted_pipelines[best_model_name]

    metrics_df.to_csv(output_dir / "regression_metrics.csv", index=False)
    joblib.dump(best_pipeline, output_dir / "best_regression_model.joblib")

    # Model-agnostic importance on the held-out time-based test set.
    perm = permutation_importance(
        best_pipeline,
        X_test,
        y_test,
        n_repeats=10,
        random_state=RANDOM_STATE,
        scoring="neg_mean_absolute_error",
        n_jobs=1,
    )
    permutation_df = pd.DataFrame(
        {
            "feature": feature_cols,
            "importance_mean": perm.importances_mean,
            "importance_std": perm.importances_std,
        }
    ).sort_values("importance_mean", ascending=False)
    permutation_df.to_csv(output_dir / "regression_permutation_importance.csv", index=False)

    return metrics_df, best_pipeline, best_model_name, permutation_df


def build_product_segmentation_frame(df: pd.DataFrame) -> pd.DataFrame:
    latest_snapshot = (
        df.sort_values(["product_id", "snapshot_date"])
        .groupby("product_id", as_index=False)
        .tail(1)[
            [
                "product_id",
                "product_name",
                "category",
                "warehouse_location",
                "stock_status",
                "selling_price",
                "original_price",
                "discount_rate",
                "rating_score",
                "review_count",
                "cumulative_units_sold",
                "snapshot_date",
            ]
        ]
        .rename(columns={"snapshot_date": "latest_snapshot_date"})
    )

    aggregated = (
        df.groupby("product_id", as_index=False)
        .agg(
            avg_daily_units_sold=("daily_units_sold", "mean"),
            avg_daily_revenue=("daily_revenue", "mean"),
            total_period_revenue=("daily_revenue", "sum"),
            avg_discount_rate=("discount_rate", "mean"),
            avg_rating_score=("rating_score", "mean"),
            avg_review_count=("review_count", "mean"),
            stock_availability_rate=("is_in_stock", "mean"),
            observation_days=("snapshot_date", "nunique"),
            sales_volatility=("daily_units_sold", "std"),
        )
    )
    aggregated["sales_volatility"] = aggregated["sales_volatility"].fillna(0.0)

    segmentation_df = latest_snapshot.merge(aggregated, on="product_id", how="left")
    return segmentation_df


def evaluate_segmentation_models(df: pd.DataFrame, output_dir: Path) -> Tuple[pd.DataFrame, Dict[str, object], int, pd.DataFrame, pd.DataFrame]:
    seg_df = build_product_segmentation_frame(df)

    feature_cols = [
        "selling_price",
        "discount_rate",
        "rating_score",
        "review_count",
        "cumulative_units_sold",
        "avg_daily_units_sold",
        "avg_daily_revenue",
        "total_period_revenue",
        "stock_availability_rate",
        "sales_volatility",
    ]

    model_df = seg_df.copy()
    for col in feature_cols:
        model_df[col] = pd.to_numeric(model_df[col], errors="coerce")
    model_df[feature_cols] = model_df[feature_cols].fillna(model_df[feature_cols].median())

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(model_df[feature_cols])

    metrics = []
    best_k = None
    best_score = -np.inf
    best_model = None

    max_k = min(6, len(model_df) - 1)
    for k in range(3, max_k + 1):
        model = KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=20)
        labels = model.fit_predict(X_scaled)
        score = float(silhouette_score(X_scaled, labels))
        metrics.append(
            {
                "model": "kmeans",
                "n_clusters": k,
                "silhouette_score": score,
                "inertia": float(model.inertia_),
            }
        )

        if score > best_score:
            best_score = score
            best_k = k
            best_model = model

    if best_model is None or best_k is None:
        raise ValueError("Unable to build a valid clustering model for product segmentation.")

    model_df["segment_id"] = best_model.predict(X_scaled)

    centers = pd.DataFrame(
        scaler.inverse_transform(best_model.cluster_centers_),
        columns=feature_cols,
    )
    centers.insert(0, "segment_id", range(best_k))

    def most_common(series: pd.Series) -> str:
        mode = series.mode()
        return mode.iloc[0] if not mode.empty else "N/A"

    segment_profiles = (
        model_df.groupby("segment_id", as_index=False)
        .agg(
            product_count=("product_id", "count"),
            dominant_category=("category", most_common),
            avg_selling_price=("selling_price", "mean"),
            avg_discount_rate=("discount_rate", "mean"),
            avg_rating_score=("rating_score", "mean"),
            avg_review_count=("review_count", "mean"),
            avg_cumulative_units_sold=("cumulative_units_sold", "mean"),
            avg_daily_units_sold=("avg_daily_units_sold", "mean"),
            avg_daily_revenue=("avg_daily_revenue", "mean"),
            avg_total_period_revenue=("total_period_revenue", "mean"),
            avg_stock_availability_rate=("stock_availability_rate", "mean"),
            avg_sales_volatility=("sales_volatility", "mean"),
        )
        .sort_values("avg_total_period_revenue", ascending=False)
    )

    metrics_df = pd.DataFrame(metrics).sort_values(by="silhouette_score", ascending=False).reset_index(drop=True)
    metrics_df.to_csv(output_dir / "segmentation_metrics.csv", index=False)
    centers.to_csv(output_dir / "segment_centers.csv", index=False)
    model_df.to_csv(output_dir / "product_segments.csv", index=False)
    segment_profiles.to_csv(output_dir / "segment_profiles.csv", index=False)
    joblib.dump({"model": best_model, "scaler": scaler, "feature_cols": feature_cols}, output_dir / "best_segmentation_model.joblib")

    return metrics_df, {"model": best_model, "scaler": scaler, "feature_cols": feature_cols}, best_k, model_df, segment_profiles


def export_feature_importance(
    pipeline: Pipeline,
    output_file: Path,
) -> None:
    model = pipeline.named_steps["model"]
    preprocessor: ColumnTransformer = pipeline.named_steps["preprocess"]

    if not hasattr(model, "feature_importances_"):
        return

    feature_names = preprocessor.get_feature_names_out()
    importance_df = pd.DataFrame(
        {
            "feature": feature_names,
            "importance": model.feature_importances_,
        }
    ).sort_values("importance", ascending=False)

    importance_df.to_csv(output_file, index=False)


def main() -> None:
    root = Path(__file__).resolve().parent
    sales_root = root / "data" / "sales"
    output_dir = root / "model_outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Loading and preparing sales data...")
    raw_df = load_sales_data(sales_root, START_DATE, END_DATE)
    sales_df = clean_sales_data(raw_df)

    # Save cleaned base table for Power BI
    sales_df.to_csv(output_dir / "daily_sales_cleaned.csv", index=False)

    print("Training regression models...")
    reg_metrics, best_reg_pipeline, best_reg_name, reg_perm_importance = evaluate_regression_models(sales_df, output_dir)

    print("Building product segmentation model...")
    seg_metrics, best_seg_model, best_k, segmented_products, segment_profiles = evaluate_segmentation_models(sales_df, output_dir)

    export_feature_importance(best_reg_pipeline, output_dir / "regression_feature_importance.csv")

    summary = {
        "date_range": {
            "start": START_DATE.isoformat(),
            "end": END_DATE.isoformat(),
        },
        "evaluation_split": {
            "type": "time_based",
            "train_fraction_by_unique_dates": 0.8,
            "test_fraction_by_unique_dates": 0.2,
        },
        "dataset": {
            "rows": int(len(sales_df)),
            "unique_products": int(sales_df["product_id"].nunique()),
            "unique_categories": int(sales_df["category"].nunique()),
        },
        "best_models": {
            "regression": best_reg_name,
            "segmentation": f"kmeans_{best_k}_clusters",
        },
        "regression_explanation": {
            "permutation_features_exported": int(len(reg_perm_importance)),
        },
        "segmentation": {
            "best_n_clusters": int(best_k),
            "products_segmented": int(len(segmented_products)),
            "segments_exported": int(len(segment_profiles)),
        },
    }

    with open(output_dir / "model_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print("\nDone.")
    print(f"Best regression model: {best_reg_name}")
    print(f"Best segmentation model: KMeans with {best_k} clusters")
    print(f"Output folder: {output_dir}")


if __name__ == "__main__":
    main()
