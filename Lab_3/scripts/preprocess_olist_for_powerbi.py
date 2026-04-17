from __future__ import annotations

from pathlib import Path
import json

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT_DIR / "data" / "raw"
PROCESSED_DIR = ROOT_DIR / "data" / "processed"


ID_COLUMNS = {
    "order_id",
    "customer_id",
    "customer_unique_id",
    "product_id",
    "seller_id",
    "review_id",
    "product_category_name",
    "product_category_name_english",
}


DATE_COLUMNS = {
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
    "shipping_limit_date",
    "review_creation_date",
    "review_answer_timestamp",
}


NUMERIC_COLUMNS = {
    "order_item_id",
    "price",
    "freight_value",
    "payment_sequential",
    "payment_installments",
    "payment_value",
    "review_score",
    "product_name_lenght",
    "product_description_lenght",
    "product_photos_qty",
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm",
    "customer_zip_code_prefix",
    "seller_zip_code_prefix",
    "geolocation_zip_code_prefix",
    "geolocation_lat",
    "geolocation_lng",
}


RAW_FILES = {
    "customers": "olist_customers_dataset.csv",
    "geolocation": "olist_geolocation_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "category_translation": "product_category_name_translation.csv",
}


def read_csv(name: str) -> pd.DataFrame:
    path = RAW_DIR / RAW_FILES[name]
    df = pd.read_csv(path)

    for column in df.columns:
        if column in ID_COLUMNS:
            df[column] = df[column].astype("string")
        if column in DATE_COLUMNS:
            df[column] = pd.to_datetime(df[column], errors="coerce")
        if column in NUMERIC_COLUMNS:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    return df


def build_geolocation_lookup(geolocation: pd.DataFrame) -> pd.DataFrame:
    geo = geolocation.copy()
    geo["geolocation_zip_code_prefix"] = geo["geolocation_zip_code_prefix"].astype("Int64")

    agg = (
        geo.groupby("geolocation_zip_code_prefix", dropna=False)
        .agg(
            geolocation_lat=("geolocation_lat", "mean"),
            geolocation_lng=("geolocation_lng", "mean"),
            geolocation_city=("geolocation_city", lambda s: s.dropna().mode().iat[0] if not s.dropna().empty else pd.NA),
            geolocation_state=("geolocation_state", lambda s: s.dropna().mode().iat[0] if not s.dropna().empty else pd.NA),
        )
        .reset_index()
        .rename(columns={"geolocation_zip_code_prefix": "zip_code_prefix"})
    )

    return agg


def build_dim_customer(customers: pd.DataFrame, geo_lookup: pd.DataFrame) -> pd.DataFrame:
    dim_customer = customers.copy()
    dim_customer["customer_zip_code_prefix"] = dim_customer["customer_zip_code_prefix"].astype("Int64")
    dim_customer = dim_customer.merge(
        geo_lookup.add_prefix("customer_"),
        left_on="customer_zip_code_prefix",
        right_on="customer_zip_code_prefix",
        how="left",
    )

    dim_customer["customer_key"] = dim_customer["customer_id"]

    return dim_customer[
        [
            "customer_key",
            "customer_id",
            "customer_unique_id",
            "customer_zip_code_prefix",
            "customer_city",
            "customer_state",
            "customer_geolocation_lat",
            "customer_geolocation_lng",
            "customer_geolocation_city",
            "customer_geolocation_state",
        ]
    ].drop_duplicates()


def build_dim_seller(sellers: pd.DataFrame, geo_lookup: pd.DataFrame) -> pd.DataFrame:
    dim_seller = sellers.copy()
    dim_seller["seller_zip_code_prefix"] = dim_seller["seller_zip_code_prefix"].astype("Int64")
    dim_seller = dim_seller.merge(
        geo_lookup.add_prefix("seller_"),
        left_on="seller_zip_code_prefix",
        right_on="seller_zip_code_prefix",
        how="left",
    )

    dim_seller["seller_key"] = dim_seller["seller_id"]

    return dim_seller[
        [
            "seller_key",
            "seller_id",
            "seller_zip_code_prefix",
            "seller_city",
            "seller_state",
            "seller_geolocation_lat",
            "seller_geolocation_lng",
            "seller_geolocation_city",
            "seller_geolocation_state",
        ]
    ].drop_duplicates()


def build_dim_category(category_translation: pd.DataFrame, products: pd.DataFrame) -> pd.DataFrame:
    used_categories = (
        products[["product_category_name"]]
        .drop_duplicates()
        .rename(columns={"product_category_name": "category_name_portuguese"})
    )

    dim_category = used_categories.merge(
        category_translation.rename(
            columns={
                "product_category_name": "category_name_portuguese",
                "product_category_name_english": "category_name_english",
            }
        ),
        on="category_name_portuguese",
        how="left",
    )

    dim_category = dim_category.sort_values("category_name_portuguese", na_position="last").reset_index(drop=True)
    dim_category["category_key"] = [f"CAT_{i:03d}" for i in range(1, len(dim_category) + 1)]
    dim_category["category_name_display"] = dim_category["category_name_english"].fillna(dim_category["category_name_portuguese"])

    return dim_category[
        [
            "category_key",
            "category_name_portuguese",
            "category_name_english",
            "category_name_display",
        ]
    ]


def build_dim_product(products: pd.DataFrame, dim_category: pd.DataFrame) -> pd.DataFrame:
    dim_product = products.copy()
    dim_product = dim_product.rename(columns={"product_category_name": "category_name_portuguese"})
    dim_product = dim_product.merge(
        dim_category[["category_key", "category_name_portuguese"]],
        on="category_name_portuguese",
        how="left",
    )

    dim_product["product_key"] = dim_product["product_id"]
    dim_product["product_volume_cm3"] = (
        dim_product["product_length_cm"]
        * dim_product["product_height_cm"]
        * dim_product["product_width_cm"]
    )

    return dim_product[
        [
            "product_key",
            "product_id",
            "category_key",
            "category_name_portuguese",
            "product_name_lenght",
            "product_description_lenght",
            "product_photos_qty",
            "product_weight_g",
            "product_length_cm",
            "product_height_cm",
            "product_width_cm",
            "product_volume_cm3",
        ]
    ].drop_duplicates()


def build_dim_date(orders: pd.DataFrame, order_items: pd.DataFrame, reviews: pd.DataFrame) -> pd.DataFrame:
    date_series = pd.concat(
        [
            orders["order_purchase_timestamp"],
            orders["order_approved_at"],
            orders["order_delivered_carrier_date"],
            orders["order_delivered_customer_date"],
            orders["order_estimated_delivery_date"],
            order_items["shipping_limit_date"],
            reviews["review_creation_date"],
            reviews["review_answer_timestamp"],
        ],
        ignore_index=True,
    ).dropna()

    full_range = pd.date_range(date_series.min().normalize(), date_series.max().normalize(), freq="D")
    dim_date = pd.DataFrame({"date": full_range})
    dim_date["date_key"] = dim_date["date"].dt.strftime("%Y%m%d").astype(int)
    dim_date["year"] = dim_date["date"].dt.year
    dim_date["quarter"] = "Q" + dim_date["date"].dt.quarter.astype(str)
    dim_date["month_number"] = dim_date["date"].dt.month
    dim_date["month_name"] = dim_date["date"].dt.strftime("%B")
    dim_date["year_month"] = dim_date["date"].dt.strftime("%Y-%m")
    dim_date["day_of_month"] = dim_date["date"].dt.day
    dim_date["day_of_week_number"] = dim_date["date"].dt.dayofweek
    dim_date["day_of_week_name"] = dim_date["date"].dt.strftime("%A")
    dim_date["is_weekend"] = dim_date["day_of_week_number"].isin([5, 6]).astype(int)
    return dim_date


def to_date_key(series: pd.Series) -> pd.Series:
    normalized = pd.to_datetime(series, errors="coerce").dt.normalize()
    return normalized.dt.strftime("%Y%m%d").where(normalized.notna())


def build_dim_order(orders: pd.DataFrame, order_items: pd.DataFrame, payments: pd.DataFrame, reviews: pd.DataFrame) -> pd.DataFrame:
    item_agg = (
        order_items.groupby("order_id", dropna=False)
        .agg(
            item_count=("order_item_id", "count"),
            product_count=("product_id", "nunique"),
            seller_count=("seller_id", "nunique"),
            items_price_total=("price", "sum"),
            freight_total=("freight_value", "sum"),
        )
        .reset_index()
    )
    item_agg["order_item_total_value"] = item_agg["items_price_total"] + item_agg["freight_total"]

    payment_agg = (
        payments.groupby("order_id", dropna=False)
        .agg(
            payment_count=("payment_sequential", "count"),
            payment_total_value=("payment_value", "sum"),
            payment_installments_max=("payment_installments", "max"),
        )
        .reset_index()
    )

    review_agg = (
        reviews.groupby("order_id", dropna=False)
        .agg(
            review_count=("review_id", "count"),
            average_review_score=("review_score", "mean"),
        )
        .reset_index()
    )

    dim_order = orders.copy()
    dim_order["order_key"] = dim_order["order_id"]
    dim_order["customer_key"] = dim_order["customer_id"]

    dim_order["purchase_date"] = dim_order["order_purchase_timestamp"].dt.normalize()
    dim_order["approved_date"] = dim_order["order_approved_at"].dt.normalize()
    dim_order["delivered_carrier_date"] = dim_order["order_delivered_carrier_date"].dt.normalize()
    dim_order["delivered_customer_date"] = dim_order["order_delivered_customer_date"].dt.normalize()
    dim_order["estimated_delivery_date"] = dim_order["order_estimated_delivery_date"].dt.normalize()

    dim_order["purchase_date_key"] = to_date_key(dim_order["order_purchase_timestamp"])
    dim_order["approved_date_key"] = to_date_key(dim_order["order_approved_at"])
    dim_order["delivered_carrier_date_key"] = to_date_key(dim_order["order_delivered_carrier_date"])
    dim_order["delivered_customer_date_key"] = to_date_key(dim_order["order_delivered_customer_date"])
    dim_order["estimated_delivery_date_key"] = to_date_key(dim_order["order_estimated_delivery_date"])

    dim_order["approval_delay_hours"] = (
        (dim_order["order_approved_at"] - dim_order["order_purchase_timestamp"]).dt.total_seconds() / 3600
    )
    dim_order["delivery_to_customer_days"] = (
        (dim_order["order_delivered_customer_date"] - dim_order["order_purchase_timestamp"]).dt.total_seconds() / 86400
    )
    dim_order["carrier_to_customer_days"] = (
        (dim_order["order_delivered_customer_date"] - dim_order["order_delivered_carrier_date"]).dt.total_seconds() / 86400
    )
    dim_order["estimated_vs_actual_delivery_days"] = (
        (dim_order["order_estimated_delivery_date"] - dim_order["order_delivered_customer_date"]).dt.total_seconds() / 86400
    )

    dim_order["is_delivered"] = (dim_order["order_status"] == "delivered").astype(int)
    dim_order["is_canceled"] = (dim_order["order_status"] == "canceled").astype(int)
    dim_order["is_late_delivery"] = (
        (dim_order["order_delivered_customer_date"] > dim_order["order_estimated_delivery_date"])
        & dim_order["order_delivered_customer_date"].notna()
        & dim_order["order_estimated_delivery_date"].notna()
    ).astype(int)

    dim_order = dim_order.merge(item_agg, on="order_id", how="left")
    dim_order = dim_order.merge(payment_agg, on="order_id", how="left")
    dim_order = dim_order.merge(review_agg, on="order_id", how="left")

    numeric_fill_zero = [
        "item_count",
        "product_count",
        "seller_count",
        "items_price_total",
        "freight_total",
        "order_item_total_value",
        "payment_count",
        "payment_total_value",
        "payment_installments_max",
        "review_count",
    ]
    for column in numeric_fill_zero:
        dim_order[column] = dim_order[column].fillna(0)

    return dim_order[
        [
            "order_key",
            "order_id",
            "customer_key",
            "customer_id",
            "order_status",
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
            "purchase_date",
            "approved_date",
            "delivered_carrier_date",
            "delivered_customer_date",
            "estimated_delivery_date",
            "purchase_date_key",
            "approved_date_key",
            "delivered_carrier_date_key",
            "delivered_customer_date_key",
            "estimated_delivery_date_key",
            "approval_delay_hours",
            "delivery_to_customer_days",
            "carrier_to_customer_days",
            "estimated_vs_actual_delivery_days",
            "is_delivered",
            "is_canceled",
            "is_late_delivery",
            "item_count",
            "product_count",
            "seller_count",
            "items_price_total",
            "freight_total",
            "order_item_total_value",
            "payment_count",
            "payment_total_value",
            "payment_installments_max",
            "review_count",
            "average_review_score",
        ]
    ].drop_duplicates()


def build_fact_order_item(order_items: pd.DataFrame) -> pd.DataFrame:
    fact_order_item = order_items.copy()
    fact_order_item["order_item_key"] = (
        fact_order_item["order_id"].astype("string") + "_" + fact_order_item["order_item_id"].astype("Int64").astype("string")
    )
    fact_order_item["order_key"] = fact_order_item["order_id"]
    fact_order_item["product_key"] = fact_order_item["product_id"]
    fact_order_item["seller_key"] = fact_order_item["seller_id"]
    fact_order_item["shipping_limit_date_key"] = to_date_key(fact_order_item["shipping_limit_date"])
    fact_order_item["shipping_limit_date"] = fact_order_item["shipping_limit_date"].dt.normalize()
    fact_order_item["item_quantity"] = 1
    fact_order_item["item_total_value"] = fact_order_item["price"] + fact_order_item["freight_value"]

    return fact_order_item[
        [
            "order_item_key",
            "order_key",
            "order_id",
            "order_item_id",
            "product_key",
            "product_id",
            "seller_key",
            "seller_id",
            "shipping_limit_date",
            "shipping_limit_date_key",
            "price",
            "freight_value",
            "item_quantity",
            "item_total_value",
        ]
    ]


def build_fact_payment(payments: pd.DataFrame) -> pd.DataFrame:
    fact_payment = payments.copy()
    fact_payment["payment_key"] = (
        fact_payment["order_id"].astype("string")
        + "_"
        + fact_payment["payment_sequential"].astype("Int64").astype("string")
    )
    fact_payment["order_key"] = fact_payment["order_id"]
    return fact_payment[
        [
            "payment_key",
            "order_key",
            "order_id",
            "payment_sequential",
            "payment_type",
            "payment_installments",
            "payment_value",
        ]
    ]


def build_fact_review(reviews: pd.DataFrame) -> pd.DataFrame:
    fact_review = reviews.copy()
    fact_review["order_key"] = fact_review["order_id"]
    fact_review["review_creation_date_only"] = fact_review["review_creation_date"].dt.normalize()
    fact_review["review_answer_date_only"] = fact_review["review_answer_timestamp"].dt.normalize()
    fact_review["review_creation_date_key"] = to_date_key(fact_review["review_creation_date"])
    fact_review["review_answer_date_key"] = to_date_key(fact_review["review_answer_timestamp"])
    fact_review["review_comment_title"] = fact_review["review_comment_title"].fillna("")
    fact_review["review_comment_message"] = fact_review["review_comment_message"].fillna("")
    fact_review["review_comment_length"] = fact_review["review_comment_message"].str.len()
    fact_review["has_review_comment"] = (fact_review["review_comment_message"].str.strip() != "").astype(int)

    return fact_review[
        [
            "review_id",
            "order_key",
            "order_id",
            "review_score",
            "review_comment_title",
            "review_comment_message",
            "review_comment_length",
            "has_review_comment",
            "review_creation_date",
            "review_answer_timestamp",
            "review_creation_date_only",
            "review_answer_date_only",
            "review_creation_date_key",
            "review_answer_date_key",
        ]
    ]


def build_summary_tables(
    dim_customer: pd.DataFrame,
    dim_seller: pd.DataFrame,
    dim_category: pd.DataFrame,
    dim_product: pd.DataFrame,
    dim_date: pd.DataFrame,
    dim_order: pd.DataFrame,
    fact_order_item: pd.DataFrame,
    fact_payment: pd.DataFrame,
    fact_review: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    schema_entities = pd.DataFrame(
        [
            {"table_name": "dim_customer", "row_count": len(dim_customer), "grain": "one row per customer_id"},
            {"table_name": "dim_seller", "row_count": len(dim_seller), "grain": "one row per seller_id"},
            {"table_name": "dim_category", "row_count": len(dim_category), "grain": "one row per product category"},
            {"table_name": "dim_product", "row_count": len(dim_product), "grain": "one row per product_id"},
            {"table_name": "dim_date", "row_count": len(dim_date), "grain": "one row per calendar date"},
            {"table_name": "dim_order", "row_count": len(dim_order), "grain": "one row per order_id"},
            {"table_name": "fact_order_item", "row_count": len(fact_order_item), "grain": "one row per order_id + order_item_id"},
            {"table_name": "fact_payment", "row_count": len(fact_payment), "grain": "one row per order_id + payment_sequential"},
            {"table_name": "fact_review", "row_count": len(fact_review), "grain": "one row per review_id"},
        ]
    )

    schema_relationships = pd.DataFrame(
        [
            {"from_table": "dim_customer", "from_column": "customer_key", "to_table": "dim_order", "to_column": "customer_key", "cardinality": "one-to-many"},
            {"from_table": "dim_category", "from_column": "category_key", "to_table": "dim_product", "to_column": "category_key", "cardinality": "one-to-many"},
            {"from_table": "dim_product", "from_column": "product_key", "to_table": "fact_order_item", "to_column": "product_key", "cardinality": "one-to-many"},
            {"from_table": "dim_seller", "from_column": "seller_key", "to_table": "fact_order_item", "to_column": "seller_key", "cardinality": "one-to-many"},
            {"from_table": "dim_order", "from_column": "order_key", "to_table": "fact_order_item", "to_column": "order_key", "cardinality": "one-to-many"},
            {"from_table": "dim_order", "from_column": "order_key", "to_table": "fact_payment", "to_column": "order_key", "cardinality": "one-to-many"},
            {"from_table": "dim_order", "from_column": "order_key", "to_table": "fact_review", "to_column": "order_key", "cardinality": "one-to-many"},
            {"from_table": "dim_date", "from_column": "date_key", "to_table": "dim_order", "to_column": "purchase_date_key", "cardinality": "one-to-many (active)"},
            {"from_table": "dim_date", "from_column": "date_key", "to_table": "dim_order", "to_column": "approved_date_key", "cardinality": "one-to-many (inactive)"},
            {"from_table": "dim_date", "from_column": "date_key", "to_table": "dim_order", "to_column": "delivered_customer_date_key", "cardinality": "one-to-many (inactive)"},
            {"from_table": "dim_date", "from_column": "date_key", "to_table": "fact_order_item", "to_column": "shipping_limit_date_key", "cardinality": "one-to-many (inactive or separate role)"},
            {"from_table": "dim_date", "from_column": "date_key", "to_table": "fact_review", "to_column": "review_creation_date_key", "cardinality": "one-to-many (inactive or separate role)"},
        ]
    )

    summary = {
        "source": {
            "dataset_name": "Brazilian E-Commerce Public Dataset by Olist",
            "source_url": "https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce",
        },
        "generated_tables": {
            "dim_customer": len(dim_customer),
            "dim_seller": len(dim_seller),
            "dim_category": len(dim_category),
            "dim_product": len(dim_product),
            "dim_date": len(dim_date),
            "dim_order": len(dim_order),
            "fact_order_item": len(fact_order_item),
            "fact_payment": len(fact_payment),
            "fact_review": len(fact_review),
        },
        "date_range": {
            "purchase_date_min": str(dim_order["purchase_date"].min()) if dim_order["purchase_date"].notna().any() else None,
            "purchase_date_max": str(dim_order["purchase_date"].max()) if dim_order["purchase_date"].notna().any() else None,
        },
        "metrics": {
            "unique_customers": int(dim_customer["customer_id"].nunique()),
            "unique_customer_entities": int(dim_customer["customer_unique_id"].nunique()),
            "unique_sellers": int(dim_seller["seller_id"].nunique()),
            "unique_products": int(dim_product["product_id"].nunique()),
            "unique_categories": int(dim_category["category_key"].nunique()),
            "unique_orders": int(dim_order["order_id"].nunique()),
            "total_item_revenue": float(fact_order_item["price"].sum()),
            "total_freight": float(fact_order_item["freight_value"].sum()),
            "total_payment_value": float(fact_payment["payment_value"].sum()),
            "average_review_score": float(fact_review["review_score"].mean()),
        },
    }

    return schema_entities, schema_relationships, summary


def write_csv(df: pd.DataFrame, filename: str) -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_DIR / filename, index=False, encoding="utf-8-sig")


def main() -> None:
    customers = read_csv("customers")
    geolocation = read_csv("geolocation")
    order_items = read_csv("order_items")
    payments = read_csv("payments")
    reviews = read_csv("reviews")
    orders = read_csv("orders")
    products = read_csv("products")
    sellers = read_csv("sellers")
    category_translation = read_csv("category_translation")

    geo_lookup = build_geolocation_lookup(geolocation)
    dim_customer = build_dim_customer(customers, geo_lookup)
    dim_seller = build_dim_seller(sellers, geo_lookup)
    dim_category = build_dim_category(category_translation, products)
    dim_product = build_dim_product(products, dim_category)
    dim_date = build_dim_date(orders, order_items, reviews)
    dim_order = build_dim_order(orders, order_items, payments, reviews)
    fact_order_item = build_fact_order_item(order_items)
    fact_payment = build_fact_payment(payments)
    fact_review = build_fact_review(reviews)

    schema_entities, schema_relationships, summary = build_summary_tables(
        dim_customer=dim_customer,
        dim_seller=dim_seller,
        dim_category=dim_category,
        dim_product=dim_product,
        dim_date=dim_date,
        dim_order=dim_order,
        fact_order_item=fact_order_item,
        fact_payment=fact_payment,
        fact_review=fact_review,
    )

    write_csv(dim_customer, "dim_customer.csv")
    write_csv(dim_seller, "dim_seller.csv")
    write_csv(dim_category, "dim_category.csv")
    write_csv(dim_product, "dim_product.csv")
    write_csv(dim_date, "dim_date.csv")
    write_csv(dim_order, "dim_order.csv")
    write_csv(fact_order_item, "fact_order_item.csv")
    write_csv(fact_payment, "fact_payment.csv")
    write_csv(fact_review, "fact_review.csv")
    write_csv(schema_entities, "schema_entities.csv")
    write_csv(schema_relationships, "schema_relationships.csv")
    write_csv(geo_lookup, "geo_zip_lookup.csv")

    with (PROCESSED_DIR / "schema_summary.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    pd.DataFrame([summary["metrics"]]).to_csv(
        PROCESSED_DIR / "model_summary.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print("Generated processed Olist files in:", PROCESSED_DIR)


if __name__ == "__main__":
    main()
