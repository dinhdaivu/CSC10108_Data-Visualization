# Power BI Dashboard and Relational Dataset Guide

## 1. Why this guide exists

For Lab 1, you need two things at the same time:

1. a dataset structure that clearly shows the relationships among `Shop`, `Product`, `Category`, and `Review`
2. a Power BI-ready dataset that is easy to import, model, and visualize

This guide combines both needs into one workflow.

## 2. Important clarification about the shop entity

Yes, your design is still valid even though you only have **one shop**.

That is still a proper relational structure because:
- one `Shop` can have many `Products`
- one `Category` can contain many `Products`
- one `Product` can have many daily `Snapshots`
- one `Product` can have many `Reviews`

In the current project:
- `Shop`: 1
- `Products`: 693
- `Categories`: 21
- `Reviews`: 7,605

So the relationship structure is still meaningful and still satisfies the lab requirement.

## 3. Main data-preparation script

Use this script:
- `prepare_powerbi_relational_data.py`

What it does:
- reads `model_outputs/daily_sales_cleaned.csv`
- reads `data/reviews/all_reviews.json`
- splits the data into relational Power BI tables
- copies the ML result tables into the same output folder

Run it with:

```powershell
C:\Users\Vu\AppData\Local\Python\pythoncore-3.14-64\python.exe c:\Users\Vu\schoolProject\CSC100800\CSC10080\Lab_1\prepare_powerbi_relational_data.py
```

Output folder:
- `powerbi_relational_data/`

## 4. Files generated for Power BI

Core relational tables:
- `powerbi_relational_data/dim_shop.csv`
- `powerbi_relational_data/dim_category.csv`
- `powerbi_relational_data/dim_product.csv`
- `powerbi_relational_data/dim_date.csv`
- `powerbi_relational_data/fact_product_snapshot.csv`
- `powerbi_relational_data/fact_review.csv`

Machine Learning support tables:
- `powerbi_relational_data/regression_metrics.csv`
- `powerbi_relational_data/regression_permutation_importance.csv`
- `powerbi_relational_data/segmentation_metrics.csv`
- `powerbi_relational_data/product_segments.csv`
- `powerbi_relational_data/segment_profiles.csv`
- `powerbi_relational_data/segment_centers.csv`
- `powerbi_relational_data/model_summary.json`

Schema reference:
- `powerbi_relational_data/schema_summary.json`

## 5. Recommended entity relationship design

Recommended relationships:
- `dim_shop.shop_id` -> `dim_product.shop_id`
- `dim_category.category_id` -> `dim_product.category_id`
- `dim_product.product_id` -> `fact_product_snapshot.product_id`
- `dim_product.product_id` -> `fact_review.product_id`
- `dim_date.date_key` -> `fact_product_snapshot.date_key`
- `dim_date.date_key` -> `fact_review.date_key`

Cardinality:
- one `Shop` to many `Products`
- one `Category` to many `Products`
- one `Product` to many `Product Snapshots`
- one `Product` to many `Reviews`
- one `Date` to many snapshot rows
- one `Date` to many review rows

Recommended Power BI setup:
- use `dim_*` tables as the `one` side
- use `fact_*` tables as the `many` side
- keep cross-filter direction as `Single`
- do not connect `fact_product_snapshot` directly to `fact_review`
- hide technical key columns after relationships are created

Quick setup checklist:
1. Import all files from `powerbi_relational_data/`.
2. Set the correct data types first.
3. Build the six relationships listed above.
4. Mark `dim_date` as the date table using the `date` column.
5. Create the core DAX measures.
6. Apply the main sales-analysis filter from `2026-02-20` to `2026-03-20`.
7. Build pages in the same order as the analytical themes in the report.

## 6. Dataset overview

Local dataset profile from the current workspace:
- Snapshot collection range: `2026-02-19` to `2026-03-20`
- Main analysis range: `2026-02-20` to `2026-03-20`
- Product snapshot rows: `18,487`
- Unique products: `693`
- Unique categories: `21`
- Review rows: `7,605`
- Segments in clustering output: `3`
- Best regression model: `linear_regression`

Important note:
- `2026-02-19` is a baseline date used to derive daily sales
- the main sales analysis should focus on `2026-02-20` to `2026-03-20`
- keep `2026-02-19` in the model, but do not use it in the main sales trend visuals

## 7. Important modeling notes

This dataset is strong enough for a useful dashboard, but it must be modeled carefully.

Why that matters:
- `daily_units_sold` and `daily_revenue` are derived fields, not raw crawl fields
- `cumulative_units_sold` and `review_count` are cumulative snapshot fields and should not be summed across dates
- the sales fact table is product-day level, so repeated `product_id` values across dates are expected
- the review fact table is review-level and should stay separate from daily sales
- `warehouse_location` exists, but it is not a strong headline dimension in this project

Use the dashboard for:
- category and time analysis
- pricing and discount analysis
- rating and review analysis
- inventory and portfolio concentration analysis
- optional ML storytelling

Do not overclaim:
- direct causation from discount to sales
- direct causation from rating to sales
- precise demand forecasting quality from the regression model
- strong geography conclusions from warehouse location

## 8. Suggested dashboard framing

Recommended title:

**Nike Product Sales Dashboard on Lazada**

Suggested subtitle:

**Category performance, pricing, customer feedback, stock status, and model-based insights from a self-collected product and review dataset**

## 9. Recommended Power BI model

Recommended approach:
- use `fact_product_snapshot` as the main sales fact table
- use `fact_review` as the review fact table
- use `dim_product`, `dim_category`, `dim_shop`, and `dim_date` as shared dimensions
- use ML output tables as page-level support tables

This is better than using one flattened file because:
- it matches the lab requirement more clearly
- it keeps review analysis cleaner
- it makes the entity relationships easier to explain in the report

## 10. Data type guide by table

### `dim_shop.csv`

- `shop_id`: Text
- `shop_name`: Text
- `platform`: Text
- `brand_name`: Text
- `shop_url`: Text

### `dim_category.csv`

- `category_id`: Text
- `category_name`: Text

### `dim_product.csv`

- `product_id`: Text
- `product_name`: Text
- `shop_id`: Text
- `category_id`: Text
- `brand_name`: Text
- `product_url`: Text
- `primary_warehouse_location`: Text

### `dim_date.csv`

- `date_key`: Whole Number
- `date`: Date
- `year`: Whole Number
- `month_number`: Whole Number
- `month_name`: Text
- `quarter`: Text
- `day_of_month`: Whole Number
- `day_of_week_number`: Whole Number
- `day_of_week_name`: Text
- `is_weekend`: Whole Number

### `fact_product_snapshot.csv`

- `snapshot_id`: Text
- `product_id`: Text
- `date_key`: Whole Number
- `snapshot_date`: Date
- `selling_price`: Decimal Number or Fixed Decimal Number
- `original_price`: Decimal Number or Fixed Decimal Number
- `discount_rate`: Decimal Number
- `daily_units_sold`: Whole Number
- `daily_revenue`: Decimal Number or Fixed Decimal Number
- `cumulative_units_sold`: Whole Number
- `rating_score`: Decimal Number
- `review_count`: Whole Number
- `stock_status`: Text
- `is_in_stock`: Whole Number
- `warehouse_location`: Text
- `day_of_week`: Whole Number
- `is_weekend`: Whole Number

### `fact_review.csv`

- `review_id`: Text
- `product_id`: Text
- `date_key`: Whole Number
- `review_date`: Date
- `rating`: Whole Number
- `review_comment`: Text
- `sku`: Text

### ML output tables

Use the same types as previously:
- `regression_metrics.csv`: text and numeric evaluation metrics
- `regression_permutation_importance.csv`: feature text and decimal values
- `segmentation_metrics.csv`: text, whole number, and decimal values
- `product_segments.csv`: product-level mixed text and numeric fields
- `segment_profiles.csv`: segment-level summary
- `segment_centers.csv`: segment-center numeric values

## 11. Core DAX measures

Use these measures first:

```DAX
Total Revenue =
SUM('fact_product_snapshot'[daily_revenue])

Total Daily Units Sold =
SUM('fact_product_snapshot'[daily_units_sold])

Distinct Products =
DISTINCTCOUNT('dim_product'[product_id])

Average Selling Price =
AVERAGE('fact_product_snapshot'[selling_price])

Average Discount Rate =
AVERAGE('fact_product_snapshot'[discount_rate])

Average Rating Score =
AVERAGE('fact_product_snapshot'[rating_score])

In-Stock Ratio =
AVERAGE('fact_product_snapshot'[is_in_stock])

Total Reviews =
COUNTROWS('fact_review')

Average Review Rating =
AVERAGE('fact_review'[rating])

Products In Stock =
CALCULATE(
    DISTINCTCOUNT('fact_product_snapshot'[product_id]),
    'fact_product_snapshot'[is_in_stock] = 1
)

Products Out of Stock =
CALCULATE(
    DISTINCTCOUNT('fact_product_snapshot'[product_id]),
    'fact_product_snapshot'[is_in_stock] = 0
)
```

Use these carefully:

```DAX
Latest Snapshot Date =
MAX('fact_product_snapshot'[snapshot_date])

Latest Snapshot Cumulative Units =
CALCULATE(
    SUM('fact_product_snapshot'[cumulative_units_sold]),
    'fact_product_snapshot'[snapshot_date] = [Latest Snapshot Date]
)

Latest Snapshot Review Count =
CALCULATE(
    SUM('fact_product_snapshot'[review_count]),
    'fact_product_snapshot'[snapshot_date] = [Latest Snapshot Date]
)
```

Important warning:
- do not create `SUM(review_count)` across all dates as a headline KPI
- do not create `SUM(cumulative_units_sold)` across all dates as a trend KPI
- those fields should usually be filtered to a single snapshot date

Recommended calculated columns:

```DAX
Price Band =
SWITCH(
    TRUE(),
    'fact_product_snapshot'[selling_price] < 1000000, "Below 1M VND",
    'fact_product_snapshot'[selling_price] < 2000000, "1M-2M VND",
    'fact_product_snapshot'[selling_price] < 3000000, "2M-3M VND",
    "Above 3M VND"
)

Analysis Window Flag =
IF(
    'fact_product_snapshot'[snapshot_date] >= DATE(2026, 2, 20) &&
    'fact_product_snapshot'[snapshot_date] <= DATE(2026, 3, 20),
    1,
    0
)
```

Use `Analysis Window Flag = 1` for pages based on `daily_units_sold` and `daily_revenue`.

## 12. Best dashboard pages by objective

### Page 1. Executive Overview

Use:
- KPI cards: `Total Revenue`, `Total Daily Units Sold`, `Distinct Products`, `Average Rating Score`
- line chart: revenue over time
- bar chart: top categories by revenue
- slicers: date, category, stock status

### Page 2. Theme 1 - Sales Performance by Category and Time

Use:
- line chart: revenue trend by category
- matrix or heatmap: category vs date
- bar chart: top 3 categories by revenue
- variability chart by category

Targets:
- Objective 1.1
- Objective 1.2

### Page 3. Theme 2 - Pricing and Discount Strategy

Use:
- scatter plot: discount vs daily units sold
- scatter plot: selling price vs daily revenue
- clustered bar chart by `Price Band`

Targets:
- Objective 2.1
- Objective 2.2

### Page 4. Theme 3 - Ratings and Reviews

Use:
- scatter plot: `rating_score` vs `cumulative_units_sold` from `fact_product_snapshot`
- scatter plot: `review_count` vs `cumulative_units_sold` from `fact_product_snapshot`
- histogram or column chart of `rating` from `fact_review`
- line chart of review volume by month from `fact_review`

Targets:
- Objective 3.1
- Objective 3.2

### Page 5. Theme 4 - Inventory and Portfolio Structure

Use:
- stacked bar: in-stock vs out-of-stock by category
- line chart: product count over time
- Pareto-style bar: top products by total revenue
- treemap of revenue concentration

Useful measures:

```DAX
Products Out of Stock =
CALCULATE(
    DISTINCTCOUNT('fact_product_snapshot'[product_id]),
    'fact_product_snapshot'[is_in_stock] = 0
)

Products In Stock =
CALCULATE(
    DISTINCTCOUNT('fact_product_snapshot'[product_id]),
    'fact_product_snapshot'[is_in_stock] = 1
)
```

Targets:
- Objective 4.1
- Objective 4.2

### Page 6. Theme 5 - Machine Learning Insights

Use:
- model comparison from `regression_metrics`
- feature importance from `regression_permutation_importance`
- segmentation quality from `segmentation_metrics`
- segment summary from `segment_profiles`
- product scatter by segment from `product_segments`

Targets:
- Objective 5.1
- Objective 5.2

## 13. Recommended visual tone

Keep the dashboard analytical and evidence-based.

Use words like:
- compare
- trend
- correlate
- share
- segment

Avoid words like:
- prove
- guarantee
- cause

unless the visual clearly supports that claim.

## 14. Suggested report explanation for the dataset requirement

You can explain the dataset design like this:

> Although the data was collected from only one Lazada shop, the dataset was still organized into a relational structure to clearly represent the relationships among the main entities required by the lab. A separate `Shop` entity was used to represent the Nike Flagship Store, a `Category` entity was used to classify products, a `Product` entity was used as the central object of analysis, a `Product Snapshot` fact table was used to store daily product-level observations, and a `Review` fact table was used to store customer feedback records. This structure makes the relationships among shop, product, category, daily observations, and reviews explicit and suitable for both database design explanation and Power BI modeling.

## 15. Final recommendation

The best setup for Lab 1 is now:

- use `powerbi_relational_data/*.csv` as the main Power BI import set
- use the same relational structure to explain the dataset requirement in the report
- use the ML outputs as a final insight page, not the backbone of the whole model
- keep the dashboard focused on the analytical window `2026-02-20` to `2026-03-20`
- treat `2026-02-19` only as the baseline snapshot for deriving daily sales

This gives you both:
- a cleaner Power BI model
- a stronger argument that your dataset structure satisfies the requirement about entity relationships
