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
- `powerbi_relational_data/regression_feature_importance.csv`
- `powerbi_relational_data/regression_permutation_importance.csv`
- `powerbi_relational_data/segmentation_metrics.csv`
- `powerbi_relational_data/product_segments.csv`
- `powerbi_relational_data/segment_profiles.csv`
- `powerbi_relational_data/segment_centers.csv`
- `powerbi_relational_data/model_summary.csv`

Schema reference:
- `powerbi_relational_data/schema_entities.csv`
- `powerbi_relational_data/schema_relationships.csv`

Optional JSON reference files:
- `powerbi_relational_data/model_summary.json`
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

### 8.1 Rewritten analytical questions (based on the current chart)

For the current page layout (KPI cards + **Top Trending** line chart + **Price Distribution** pie chart + category/date slicers), keep questions in this format:

- **Question**
- **Visual evidence**
- **Primary measures**

Main question:

**Within the selected date range and category filters, how do category-level trend behavior and price-band structure explain the KPI level of revenue, units sold, and average selling price on this page?**

Supporting questions:

1. **Question:** Which categories are the main drivers of total revenue in the selected window?
  - **Visual evidence:** `Top Trending` line chart (category legend) + KPI cards
  - **Primary measures:** `Total Revenue`, `Total Daily Units Sold`

2. **Question:** Are revenue spikes concentrated in a few dates/categories or distributed more evenly over time?
  - **Visual evidence:** `Top Trending` line chart
  - **Primary measures:** date-level `Total Revenue` by `category_name`

3. **Question:** Which price band contributes the largest revenue share, and is that share stable under slicer changes?
  - **Visual evidence:** `Price Distribution` pie chart + date/category slicers
  - **Primary measures:** `Total Revenue` by `Price Band`

4. **Question:** Is there a mismatch between value contribution and volume contribution across price bands?
  - **Visual evidence:** `Price Distribution` pie chart + KPI cards
  - **Primary measures:** `Total Revenue` by `Price Band` vs `Total Daily Units Sold` by `Price Band`

5. **Question:** When filters change, which KPI is most sensitive (`Revenue`, `Units Sold`, or `Average Selling Price`), and what does that imply for strategy?
  - **Visual evidence:** KPI cards under interactive slicing
  - **Primary measures:** `Total Revenue`, `Total Daily Units Sold`, `Average Selling Price`

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

### `regression_metrics.csv`

- `model`: Text
- `mae`: Decimal Number
- `rmse`: Decimal Number
- `r2`: Decimal Number
- `train_start_date`: Date
- `train_end_date`: Date
- `test_start_date`: Date
- `test_end_date`: Date

### `regression_feature_importance.csv`

- `feature`: Text
- `coefficient`: Decimal Number
- `importance`: Decimal Number

Note:
- if the exported model does not have coefficients, this table may instead contain only `feature` and `importance`

### `regression_permutation_importance.csv`

- `feature`: Text
- `importance_mean`: Decimal Number
- `importance_std`: Decimal Number

### `segmentation_metrics.csv`

- `model`: Text
- `n_clusters`: Whole Number
- `silhouette_score`: Decimal Number
- `inertia`: Decimal Number
- `calinski_harabasz_score`: Decimal Number
- `davies_bouldin_score`: Decimal Number

### `product_segments.csv`

- `product_id`: Text
- `product_name`: Text
- `category`: Text
- `warehouse_location`: Text
- `stock_status`: Text
- `selling_price`: Decimal Number or Fixed Decimal Number
- `original_price`: Decimal Number or Fixed Decimal Number
- `discount_rate`: Decimal Number
- `rating_score`: Decimal Number
- `review_count`: Whole Number
- `cumulative_units_sold`: Whole Number
- `latest_snapshot_date`: Date
- `avg_daily_units_sold`: Decimal Number
- `avg_daily_revenue`: Decimal Number or Fixed Decimal Number
- `total_period_revenue`: Decimal Number or Fixed Decimal Number
- `avg_discount_rate`: Decimal Number
- `avg_rating_score`: Decimal Number
- `avg_review_count`: Decimal Number
- `stock_availability_rate`: Decimal Number
- `observation_days`: Whole Number
- `sales_volatility`: Decimal Number
- `segment_id`: Whole Number
- `pca_component_1`: Decimal Number
- `pca_component_2`: Decimal Number
- `distance_to_center`: Decimal Number
- `representative_rank`: Whole Number
- `is_representative_product`: True/False

### `segment_profiles.csv`

- `segment_id`: Whole Number
- `product_count`: Whole Number
- `dominant_category`: Text
- `avg_selling_price`: Decimal Number or Fixed Decimal Number
- `avg_discount_rate`: Decimal Number
- `avg_rating_score`: Decimal Number
- `avg_review_count`: Decimal Number
- `avg_cumulative_units_sold`: Decimal Number
- `avg_daily_units_sold`: Decimal Number
- `avg_daily_revenue`: Decimal Number or Fixed Decimal Number
- `avg_total_period_revenue`: Decimal Number or Fixed Decimal Number
- `avg_stock_availability_rate`: Decimal Number
- `avg_sales_volatility`: Decimal Number
- `product_share`: Decimal Number

### `segment_centers.csv`

- `segment_id`: Whole Number
- `selling_price`: Decimal Number or Fixed Decimal Number
- `discount_rate`: Decimal Number
- `rating_score`: Decimal Number
- `review_count`: Decimal Number
- `cumulative_units_sold`: Decimal Number
- `avg_daily_units_sold`: Decimal Number
- `avg_daily_revenue`: Decimal Number or Fixed Decimal Number
- `total_period_revenue`: Decimal Number or Fixed Decimal Number
- `stock_availability_rate`: Decimal Number
- `sales_volatility`: Decimal Number

### `model_summary.csv`

Recommended types:
- `date_range_baseline_start`: Date
- `date_range_analysis_start`: Date
- `date_range_end`: Date
- `evaluation_split_type`: Text
- `evaluation_split_train_fraction_by_unique_dates`: Decimal Number
- `evaluation_split_test_fraction_by_unique_dates`: Decimal Number
- `dataset_rows`: Whole Number
- `dataset_unique_products`: Whole Number
- `dataset_unique_categories`: Whole Number
- `best_models_regression`: Text
- `best_models_segmentation`: Text
- `regression_explanation_permutation_features_exported`: Whole Number
- `regression_explanation_model_feature_importance_exported`: True/False
- `segmentation_best_n_clusters`: Whole Number
- `segmentation_products_segmented`: Whole Number
- `segmentation_segments_exported`: Whole Number

### `schema_entities.csv`

- `entity_name`: Text
- `row_count`: Whole Number

### `schema_relationships.csv`

- `relationship_id`: Whole Number
- `from`: Text
- `to`: Text
- `type`: Text
- `from_table`: Text
- `from_column`: Text
- `to_table`: Text
- `to_column`: Text

## 11. ML table relationship recommendations

Recommended approach:
- keep most ML/support tables disconnected
- only connect `product_segments.csv` if you want segment labels to filter product-level visuals
- do not connect ML tables directly to fact tables

### `product_segments.csv`

Recommended relationship:
- `dim_product[product_id]` -> `product_segments[product_id]`

Recommended settings:
- cardinality: One-to-one if Power BI accepts it
- cross filter direction: Single
- status: Active

Why:
- `product_segments` has one row per product
- this lets you use `segment_id` as a slicer or legend together with product attributes
- this is the only ML relationship that is usually worth creating

### `segment_profiles.csv`

Recommended relationship:
- none by default

Why:
- it is already a segment-level summary table
- use it for standalone charts, cards, or tables on the segmentation page
- connecting it is optional, not required

### `segment_centers.csv`

Recommended relationship:
- none by default

Why:
- it is also a segment-level summary table
- use it as a standalone support table for explaining cluster characteristics

### `regression_metrics.csv`

Recommended relationship:
- none

Why:
- it is a model-evaluation table, not a transactional table
- use it for KPI cards, score tables, or model-comparison visuals

### `regression_feature_importance.csv`

Recommended relationship:
- none

Why:
- it is an explanatory model-output table
- use it for bar charts of feature importance

### `regression_permutation_importance.csv`

Recommended relationship:
- none

Why:
- it is an explanatory model-output table
- use it for feature-importance ranking visuals

### `segmentation_metrics.csv`

Recommended relationship:
- none

Why:
- it is only used to compare clustering quality
- use it for a simple comparison table or chart

### `model_summary.csv`

Recommended relationship:
- none

Why:
- it is a one-row metadata table
- use it for cards and text-based model summary visuals

### `schema_entities.csv`

Recommended relationship:
- none

Why:
- it is documentation/metadata
- use it only for dataset overview tables if needed

### `schema_relationships.csv`

Recommended relationship:
- none

Why:
- it is documentation/metadata
- use it only to explain the model design in the report

Important note:
- if you want a more advanced segmentation model later, create a dedicated `dim_segment` table and connect it to `product_segments`, `segment_profiles`, and `segment_centers`
- for the current lab, that extra layer is optional and not necessary

## 12. Core DAX measures

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
VAR LatestDate = [Latest Snapshot Date]
RETURN
CALCULATE(
    SUM('fact_product_snapshot'[cumulative_units_sold]),
    FILTER(
        'fact_product_snapshot',
        'fact_product_snapshot'[snapshot_date] = LatestDate
    )
)

Latest Snapshot Review Count =
VAR LatestDate = [Latest Snapshot Date]
RETURN
CALCULATE(
    SUM('fact_product_snapshot'[review_count]),
    FILTER(
        'fact_product_snapshot',
        'fact_product_snapshot'[snapshot_date] = LatestDate
    )
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
    'fact_product_snapshot 1'[selling_price] < 1000000, "Below 1M VND",
    'fact_product_snapshot 1'[selling_price] < 2000000, "1M-2M VND",
    'fact_product_snapshot 1'[selling_price] < 3000000, "2M-3M VND",
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

Scatter-chart note for Power BI website:
- the web visual uses these field wells: `Values`, `X Axis`, `Y Axis`, `Legend`, `Size`, `Play Axis`, and `Tooltips`
- it does not expose a separate `Details` field in the same way some other Power BI experiences do
- for this guide, leave `Values` empty for scatter charts unless a specific aggregation is needed
- use `Legend` for grouping and `Tooltips` for product-level context
- if one point appears instead of many, the chart is being aggregated too heavily

### Page 1. Theme 2 - Finance Structure

Purpose:
- show how revenue is distributed across price bands and how KPI performance changes under the selected filter context

Main tables used:
- `fact_product_snapshot`
- `dim_category`
- `dim_date`

Recommended visuals:
- KPI cards
  Values: `Total Daily Revenue`, `Average Daily Units Sold`, `Average Price per Product`
- line chart
  Title: `Top Trending`
  Axis: `dim_date[date]`
  Legend: `dim_category[category_name]`
  Values: `Total Revenue`
- pie or donut chart
  Title: `Price Distribution`
  Legend: `fact_product_snapshot[Price Band]`
  Values: `Total Revenue`

Page filters:
- `fact_product_snapshot[Analysis Window Flag] = 1`

Recommended slicers:
- date range
- category or page filter slicer

Notes:
- this page corresponds to Objective 2.1 and Objective 2.2
- keep the interpretation focused on revenue concentration by price band and KPI sensitivity under filter changes

### Page 2. Theme 1 - Sales Performance by Category and Time

Purpose:
- answer which categories perform best over time and how stable their sales are

Main tables used:
- `fact_product_snapshot`
- `dim_category`
- `dim_date`

Recommended visuals:
- line chart
  Axis: `dim_date[date]`
  Legend: `dim_category[category_name]`
  Values: `Total Revenue`
- matrix
  Rows: `dim_category[category_name]`
  Columns: `dim_date[date]` or month-level date grouping
  Values: `Total Revenue`
- bar chart
  Axis: `dim_category[category_name]`
  Values: `Total Daily Units Sold`
  Visual filter: Top N = 3 by `Total Daily Units Sold`
- column chart
  Axis: `dim_category[category_name]`
  Values: `Average Selling Price` or `Average Discount Rate`

Page filters:
- `fact_product_snapshot[Analysis Window Flag] = 1`

Recommended slicers:
- `dim_date[date]`
- `dim_category[category_name]`
- `dim_product[brand_name]`

Notes:
- this page should stay focused on `fact_product_snapshot`
- use `dim_date[date]` for the timeline, not `snapshot_date` directly when possible

Targets:
- Objective 1.1
- Objective 1.2

### Page 3. Theme 3 - Product Influence Analysis

Purpose:
- identify the products with the strongest unit performance and check whether their strength is stable or spike-driven over time

Main tables used:
- `fact_product_snapshot`
- `dim_product`
- `dim_date`

Recommended visuals:
- horizontal bar chart
  Title: `Top Products by Average Unit Sold`
  Axis: `dim_product[product_name]`
  Values: unit-performance measure used on the page
- line chart
  Title: `Top Unit`
  Axis: `dim_date[date]`
  Legend: `dim_product[product_name]`
  Values: unit-performance trend for the leading products
- KPI cards
  Values: `Average Price`, `Average Daily Units Sold`, `Distinct Products`

Page filters:
- `fact_product_snapshot[Analysis Window Flag] = 1`

Recommended slicers:
- date range
- category or page filter slicer if enabled

Notes:
- this page corresponds to Objective 3.1 and Objective 3.2
- keep the interpretation focused on product ranking, spike timing, and concentration risk

Targets:
- Objective 3.1
- Objective 3.2

### Page 4. Theme 4 - Customer Ratings and Review Signals

Purpose:
- show monthly customer review activity and rating patterns within the selected year

Main tables used:
- `fact_review`
- `dim_product`
- `dim_date`

Recommended visuals:
- line chart
  Title: `Monthly Rating and Review Trends`
  Axis: review month
  Values: monthly `review_count`, monthly `average_rating`
- line chart
  Title: `Monthly Comment Trends for Top Products`
  Axis: review month
  Values: `review_count`
  Legend: `product_name`
  Visual filter: Top N products by `review_count` within the selected year
- KPI cards
  Values: `Total Reviews`, `Average Rating`, `Average Reviews per Product`

Page filters:
- no fixed sales-window filter
- use the `year` slicer to focus the page on one selected year from `2024`, `2025`, or `2026`

Recommended slicers:
- review year
- review month if needed
- `dim_product[product_name]`
- optional product/category filter if your review model supports it

Notes:
- this page is review-focused and should not mix in revenue with the review visuals
- review history spans beyond the main sales-analysis window from `2026-02-20` to `2026-03-20`

Targets:
- Objective 4.1
- Objective 4.2

### Page 5. Theme 5 - Machine Learning Insights (Clustering)

Purpose:
- present clustering outputs as supporting insights rather than as the main fact model

Main tables used:
- `segmentation_metrics`
- `segment_profiles`
- `product_segments`

Recommended visuals:
- scatter chart
  Title: `Product Segments by Units Sold vs Revenue`
  Source: `product_segments`
  X-axis: `avg_daily_units_sold`
  Y-axis: `avg_daily_revenue`
  Legend: `segment_id`
- bar chart
  Title: `Silhouette Score by Number of Clusters`
  Source: `segmentation_metrics`
  Axis: `n_clusters`
  Values: `silhouette_score`
- pie or donut chart
  Title: `Cluster Revenue Contribution (%)`
  Source: segment summary
  Legend: `segment_id`
  Values: cluster revenue share

Page filters:
- usually none
- model outputs are already derived from the prepared dataset

Recommended slicers:
- `product_segments[segment_id]` if needed
- optional category filter if your connected model supports it

Notes:
- keep this as a final insight page
- the clustering page should support Objective 5.1 and Objective 5.2 directly

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
