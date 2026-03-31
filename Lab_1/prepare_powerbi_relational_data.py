from __future__ import annotations

"""Recommended Lab 1 data-preparation entrypoint.

Use this script for the current workflow. It creates the Power BI-ready
relational model, keeps the required entity relationships explicit, and copies
the ML result tables into the same output folder.

"""

from pathlib import Path
from datetime import datetime
import json
import shutil

import pandas as pd


SHOP_ID = "SHOP_001"
SHOP_NAME = "Nike Flagship Store"
PLATFORM = "Lazada"
SHOP_URL = "https://www.lazada.vn/nike-flagship-store/"


def load_sales_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, dtype={"product_id": str})
    df["snapshot_date"] = pd.to_datetime(df["snapshot_date"], errors="coerce").dt.normalize()
    return df


def load_reviews(path: Path) -> pd.DataFrame:
    with path.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    reviews = pd.DataFrame(raw)
    reviews = reviews.rename(
        columns={
            "id_sp": "product_id",
            "time": "review_date",
            "comment": "review_comment",
        }
    )
    reviews["product_id"] = reviews["product_id"].astype(str)
    reviews["review_date"] = pd.to_datetime(reviews["review_date"], errors="coerce").dt.normalize()
    reviews["review_comment"] = reviews["review_comment"].fillna("")
    reviews["sku"] = reviews["sku"].fillna("")
    reviews["review_id"] = [f"REV_{i:05d}" for i in range(1, len(reviews) + 1)]
    return reviews[["review_id", "product_id", "rating", "review_comment", "review_date", "sku"]]


def build_dim_shop() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "shop_id": SHOP_ID,
                "shop_name": SHOP_NAME,
                "platform": PLATFORM,
                "brand_name": "Nike",
                "shop_url": SHOP_URL,
            }
        ]
    )


def build_dim_category(sales_df: pd.DataFrame) -> pd.DataFrame:
    categories = sales_df[["category"]].drop_duplicates().sort_values("category").reset_index(drop=True)
    categories["category_id"] = [f"CAT_{i:03d}" for i in range(1, len(categories) + 1)]
    return categories[["category_id", "category"]].rename(columns={"category": "category_name"})


def build_dim_product(sales_df: pd.DataFrame, category_df: pd.DataFrame) -> pd.DataFrame:
    products = (
        sales_df.sort_values(["product_id", "snapshot_date"])
        .groupby("product_id", as_index=False)
        .tail(1)[
            [
                "product_id",
                "product_name",
                "category",
                "brand_name",
                "product_url",
                "warehouse_location",
            ]
        ]
        .copy()
    )
    products["shop_id"] = SHOP_ID
    products = products.merge(
        category_df.rename(columns={"category_name": "category"}),
        on="category",
        how="left",
    )
    products["primary_warehouse_location"] = products["warehouse_location"]
    return products[
        [
            "product_id",
            "product_name",
            "shop_id",
            "category_id",
            "brand_name",
            "product_url",
            "primary_warehouse_location",
        ]
    ]


def build_dim_date(sales_df: pd.DataFrame, review_df: pd.DataFrame) -> pd.DataFrame:
    date_series = pd.concat(
        [
            sales_df["snapshot_date"].dropna().rename("date"),
            review_df["review_date"].dropna().rename("date"),
        ],
        ignore_index=True,
    ).drop_duplicates().sort_values()

    dim_date = pd.DataFrame({"date": date_series})
    dim_date["date_key"] = dim_date["date"].dt.strftime("%Y%m%d").astype(int)
    dim_date["year"] = dim_date["date"].dt.year
    dim_date["month_number"] = dim_date["date"].dt.month
    dim_date["month_name"] = dim_date["date"].dt.strftime("%B")
    dim_date["quarter"] = "Q" + dim_date["date"].dt.quarter.astype(str)
    dim_date["day_of_month"] = dim_date["date"].dt.day
    dim_date["day_of_week_number"] = dim_date["date"].dt.dayofweek
    dim_date["day_of_week_name"] = dim_date["date"].dt.strftime("%A")
    dim_date["is_weekend"] = dim_date["day_of_week_number"].isin([5, 6]).astype(int)
    return dim_date


def build_fact_product_snapshot(sales_df: pd.DataFrame) -> pd.DataFrame:
    fact = sales_df.copy()
    fact["snapshot_id"] = fact["product_id"].astype(str) + "_" + fact["snapshot_date"].dt.strftime("%Y-%m-%d")
    fact["date_key"] = fact["snapshot_date"].dt.strftime("%Y%m%d").astype(int)
    return fact[
        [
            "snapshot_id",
            "product_id",
            "date_key",
            "snapshot_date",
            "selling_price",
            "original_price",
            "discount_rate",
            "daily_units_sold",
            "daily_revenue",
            "cumulative_units_sold",
            "rating_score",
            "review_count",
            "stock_status",
            "is_in_stock",
            "warehouse_location",
            "day_of_week",
            "is_weekend",
        ]
    ]


def build_fact_review(review_df: pd.DataFrame, valid_product_ids: set[str]) -> pd.DataFrame:
    fact = review_df[review_df["product_id"].isin(valid_product_ids)].copy()
    fact["date_key"] = fact["review_date"].dt.strftime("%Y%m%d")
    fact = fact[fact["date_key"].notna()].copy()
    fact["date_key"] = fact["date_key"].astype(int)
    return fact[
        [
            "review_id",
            "product_id",
            "date_key",
            "review_date",
            "rating",
            "review_comment",
            "sku",
        ]
    ]


def copy_ml_outputs(source_dir: Path, target_dir: Path) -> None:
    files_to_copy = [
        "regression_metrics.csv",
        "regression_permutation_importance.csv",
        "segmentation_metrics.csv",
        "product_segments.csv",
        "segment_profiles.csv",
        "segment_centers.csv",
        "model_summary.json",
    ]
    for filename in files_to_copy:
        shutil.copy2(source_dir / filename, target_dir / filename)


def build_schema_summary(
    dim_shop: pd.DataFrame,
    dim_category: pd.DataFrame,
    dim_product: pd.DataFrame,
    dim_date: pd.DataFrame,
    fact_snapshot: pd.DataFrame,
    fact_review: pd.DataFrame,
) -> dict:
    return {
        "entities": {
            "dim_shop": len(dim_shop),
            "dim_category": len(dim_category),
            "dim_product": len(dim_product),
            "dim_date": len(dim_date),
            "fact_product_snapshot": len(fact_snapshot),
            "fact_review": len(fact_review),
        },
        "relationships": [
            {"from": "dim_shop.shop_id", "to": "dim_product.shop_id", "type": "one-to-many"},
            {"from": "dim_category.category_id", "to": "dim_product.category_id", "type": "one-to-many"},
            {"from": "dim_product.product_id", "to": "fact_product_snapshot.product_id", "type": "one-to-many"},
            {"from": "dim_product.product_id", "to": "fact_review.product_id", "type": "one-to-many"},
            {"from": "dim_date.date_key", "to": "fact_product_snapshot.date_key", "type": "one-to-many"},
            {"from": "dim_date.date_key", "to": "fact_review.date_key", "type": "one-to-many"},
        ],
    }


def main() -> None:
    root = Path(__file__).resolve().parent
    model_output_dir = root / "model_outputs"
    sales_path = model_output_dir / "daily_sales_cleaned.csv"
    reviews_path = root / "data" / "reviews" / "all_reviews.json"
    output_dir = root / "powerbi_relational_data"
    output_dir.mkdir(parents=True, exist_ok=True)

    sales_df = load_sales_data(sales_path)
    review_df = load_reviews(reviews_path)

    dim_shop = build_dim_shop()
    dim_category = build_dim_category(sales_df)
    dim_product = build_dim_product(sales_df, dim_category)
    dim_date = build_dim_date(sales_df, review_df)
    fact_snapshot = build_fact_product_snapshot(sales_df)
    valid_product_ids = set(dim_product["product_id"].astype(str))
    fact_review = build_fact_review(review_df, valid_product_ids)

    dim_shop.to_csv(output_dir / "dim_shop.csv", index=False, encoding="utf-8-sig")
    dim_category.to_csv(output_dir / "dim_category.csv", index=False, encoding="utf-8-sig")
    dim_product.to_csv(output_dir / "dim_product.csv", index=False, encoding="utf-8-sig")
    dim_date.to_csv(output_dir / "dim_date.csv", index=False, encoding="utf-8-sig")
    fact_snapshot.to_csv(output_dir / "fact_product_snapshot.csv", index=False, encoding="utf-8-sig")
    fact_review.to_csv(output_dir / "fact_review.csv", index=False, encoding="utf-8-sig")

    copy_ml_outputs(model_output_dir, output_dir)

    summary = build_schema_summary(
        dim_shop=dim_shop,
        dim_category=dim_category,
        dim_product=dim_product,
        dim_date=dim_date,
        fact_snapshot=fact_snapshot,
        fact_review=fact_review,
    )
    with (output_dir / "schema_summary.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print("Recommended export completed: Power BI relational dataset created successfully.")
    print(f"Output folder: {output_dir}")


if __name__ == "__main__":
    main()
