# Report Content for Sections 3.1 and 3.3

==

---

## 3.1. Defining Analytical Objectives

### 3.1.1. Dataset Context

The project is based on a self-collected dataset of Nike products on Lazada. The sales dataset covers the period from **February 19, 2026** to **March 20, 2026**, corresponding to **30 consecutive daily snapshots**. The snapshot on **February 19, 2026** is used as the **baseline** for calculating day-to-day sales, so analyses that rely on `daily_units_sold` and `daily_revenue` are conducted from **February 20, 2026** to **March 20, 2026**. Across the full observation window, the dataset contains **19,150 product-day records**, representing **686 unique products** and **20 unique categories**. On average, each daily snapshot contains **638.33 records**, with the smallest daily snapshot containing **590 records** and the largest containing **668 records**.

The final snapshot on **March 20, 2026** contains **590 products** across **15 categories**. In this snapshot, **580 products** are marked as in stock and **10 products** are marked as out of stock. The selling price ranges from **309,000 VND** to **5,279,000 VND**, while the total cumulative units sold recorded in that snapshot is **26,068 units**.

The review dataset is stored separately and contains **7,605 reviews** for **585 products**. Review timestamps range from **September 13, 2024** to **March 14, 2026**. As a result, review-based analysis can provide useful information about customer feedback patterns, but it should not be interpreted as perfectly aligned with the **February 20, 2026 to March 20, 2026** sales-analysis window.

### 3.1.2. Overall Group Analysis Problem

Based on the collected dataset, the group defines the common analytical problem as follows:

**The group's common analytical problem is to examine how product category, pricing, discount policy, stock status, ratings, and customer review behavior influence the sales performance of Nike products on Lazada, based on data collected from February 20, 2026 to March 20, 2026.**

This analytical problem is appropriate for the project for three reasons. First, it is directly derived from the variables available in the self-collected dataset. Second, it allows the group to combine descriptive analysis, comparison across categories, and relationship analysis through visualization. Third, it provides a clear framework for integrating the optional Machine Learning component as a supporting method rather than treating it as a separate topic.

### 3.1.3. Analytical Themes and SMART Objectives

To address the common analytical problem, the group divides the work into five themes. Each member is assigned one theme and proposes two SMART objectives, resulting in a total of ten analytical objectives.

#### Theme 1. Sales Performance by Category and Time

This theme focuses on category-level sales dynamics throughout the observation period.

**Objective 1.1**

Analyze daily revenue and daily units sold by product category from **February 20, 2026** to **March 20, 2026** in order to identify the **three categories with the highest total revenue** during th  e study period.

- `Specific`: Category-level sales performance over time
- `Measurable`: Uses `daily_revenue`, `daily_units_sold`, and top-three ranking
- `Achievable`: Required fields are available in the daily snapshots
- `Relevant`: Identifies the main revenue-generating categories in the dataset
- `Time-bound`: Limited to `20-02-2026` to `20-03-2026`, with `19-02-2026` used as the baseline snapshot

**Objective 1.2**

Measure day-to-day revenue variability by category from **February 20, 2026** to **March 20, 2026** in order to identify the **three most volatile categories** and the **three most stable categories** during the observation period.

- `Specific`: Category-level revenue stability
- `Measurable`: Uses standard deviation or coefficient of variation of `daily_revenue`
- `Achievable`: Can be computed from daily category-level aggregates
- `Relevant`: Helps identify categories with stable or unstable sales patterns
- `Time-bound`: Limited to the same analytical period from `20-02-2026` to `20-03-2026`

#### Theme 2. Finance Structure

This theme focuses on the financial structure of the portfolio through price-band contribution, KPI behavior, and trend changes under the selected filters.

**Objective 2.1**

Measure revenue-share differences across predefined `Price Band` groups from **February 20, 2026** to **March 20, 2026** in order to identify the **dominant price band** in the current dashboard design.

- `Specific`: Price-band contribution analysis aligned with the `Price Distribution` visual
- `Measurable`: Uses share of `daily_revenue` and average `selling_price` by `Price Band`
- `Achievable`: `selling_price` and sales variables are available in the prepared snapshot dataset
- `Relevant`: Directly supports interpretation of the KPI cards and pie-chart structure on the dashboard
- `Time-bound`: Evaluated within the analytical window from `20-02-2026` to `20-03-2026`

**Objective 2.2**

Use the `Top Trending` line chart together with KPI cards and dashboard slicers from **February 20, 2026** to **March 20, 2026** in order to determine whether sales performance is **broad-based or concentrated** in a small number of dates or product groups.

- `Specific`: Dashboard-based sensitivity analysis using the `Top Trending` line chart, KPI cards, and slicers
- `Measurable`: Uses changes in `Total Daily Revenue`, `Average Daily Units Sold`, and `Average Price per Product` under selected date and filter states
- `Achievable`: The required KPIs, segment dimensions, and filters are available in the current dashboard and source tables
- `Relevant`: Matches the interactive dashboard workflow and provides visual evidence for report/viva interpretation
- `Time-bound`: Limited to the same analytical period from `20-02-2026` to `20-03-2026`

#### Theme 3. Product Influence Analysis

This theme focuses on how leading products influence unit performance on the dashboard page.

**Objective 3.1**

Identify the top Nike products driving unit performance from **February 20, 2026** to **March 20, 2026** using the `Top Products by Average Unit Sold` visual and dashboard filters.

- `Specific`: Product-level comparison focused on the leading products by unit performance
- `Measurable`: Uses ranking of products by the `Avg Daily Units Sold` measure shown in the current visual
- `Achievable`: Product name, unit measures, and supporting product attributes are available in the current dashboard model
- `Relevant`: Directly supports the page purpose of understanding product influence on sales outcomes
- `Time-bound`: Evaluated within the analysis window from `20-02-2026` to `20-03-2026`

**Objective 3.2**

Analyze time-based spikes and concentration risk among top products from **February 20, 2026** to **March 20, 2026** by combining the `Top Unit` trend visual with the dashboard slicers.

- `Specific`: Temporal sensitivity analysis of top-product unit performance under interactive filters
- `Measurable`: Uses peak values of the `Avg Daily Units Sold` trend by date, spike frequency of top products, and comparison of product-level peaks within the selected period
- `Achievable`: Date, product, and unit metrics are available in the current dashboard visuals
- `Relevant`: Explains whether page-level performance is broad-based or overly dependent on a small number of products
- `Time-bound`: Limited to the same analytical period from `20-02-2026` to `20-03-2026`

#### Theme 4. Customer Ratings and Review Signals

This theme focuses on monthly customer review activity and rating patterns within a selected year in the review dataset.

**Objective 4.1**

Analyze monthly changes in review count and average rating within a selected year in order to determine when customer engagement and customer evaluation are strongest for the selected Nike categories.

- `Specific`: Monthly review and rating trend analysis within a selected year
- `Measurable`: Uses `review_count` and `average_rating` by month in the `Monthly Rating and Review Trends` visual
- `Achievable`: Variables are directly available in the review dataset
- `Relevant`: Customer review behavior helps describe longer-term customer feedback patterns
- `Time-bound`: Evaluated within a selected year from the observed review period `2024` to `2026`

**Objective 4.2**

Identify the Nike products with the highest number of comments within a selected year in order to determine whether customer attention is concentrated in a small group of products.

- `Specific`: Product-level concentration of review attention by month within the selected year
- `Measurable`: Uses `review_count` by `product_name` across months in the `Monthly Comment Trends for Top Products` visual
- `Achievable`: Product identifiers and review counts are available in the review dataset
- `Relevant`: Shows which products attract the strongest customer discussion
- `Time-bound`: Evaluated within a selected year from the observed review period `2024` to `2026`

#### Theme 5. Machine Learning Insights (Clustering)

This theme uses clustering as a supporting analytical method to strengthen the interpretation of the common analytical problem. Instead of presenting ML as a purely technical forecasting task, the theme focuses on whether the collected products can be grouped into distinct sales-performance profiles and how those profiles contribute to overall revenue.

**Objective 5.1**

Use the silhouette score comparison bar chart and the `Product Segments by Units Sold vs Revenue` scatter chart to evaluate the clustering solution and identify distinct Nike product groups from **February 20, 2026** to **March 20, 2026**, in order to show that the dataset can be meaningfully segmented into different sales-performance patterns.

- `Specific`: Compare clustering quality across candidate cluster settings using `silhouette_score`, then visualize product distribution by `segment_id` on the `Product Segments by Units Sold vs Revenue` scatter chart
- `Measurable`: Uses differences in `silhouette_score` across cluster options and visible separation of products by `segment_id`, `avg_daily_units_sold`, and `avg_daily_revenue` on the scatter plot
- `Achievable`: All required fields are available in `segmentation_metrics.csv` and `product_segments.csv`
- `Relevant`: Supports the analytical problem by showing that products can be grouped into meaningful clusters before interpreting sales behavior
- `Time-bound`: Evaluated within the analysis window from `20-02-2026` to `20-03-2026`

**Objective 5.2**

Use the `Product Segments by Units Sold vs Revenue` scatter chart together with the pie chart of revenue contribution by cluster to interpret how each product segment contributes to overall Nike sales performance from **February 20, 2026** to **March 20, 2026**, in order to explain which clusters dominate total revenue and which clusters represent smaller but distinct performance groups.

- `Specific`: Compare revenue contribution across `segment_id` and relate each cluster's share of revenue to its position in the `Product Segments by Units Sold vs Revenue` scatter chart
- `Measurable`: Uses `% revenue contribution` by cluster, cluster membership on the scatter chart, and differences in `avg_daily_units_sold` and `avg_daily_revenue`
- `Achievable`: The required fields are available from `product_segments.csv` and `segment_profiles.csv`
- `Relevant`: Directly supports the common analytical problem by linking clustered product characteristics to overall sales performance contribution
- `Time-bound`: Limited to the same analytical period from `20-02-2026` to `20-03-2026`

### 3.1.4. Why These Objectives Match the Project Requirements

These objectives are consistent with the project requirements because they are built directly from the team's self-collected data, follow the SMART principle, and can be supported through charts, descriptive statistics, and evidence-based conclusions. In addition, the Machine Learning theme remains aligned with the common analytical problem and serves as a meaningful optional extension rather than replacing the required visualization-based analysis.

### 3.1.5. Note for Final Report Integration

In the final report, the placeholders `Member 1` to `Member 5` should be replaced with the actual names of the group members. The report should clearly distinguish between the **full collected snapshot range** (**February 19, 2026** to **March 20, 2026**) and the **analytical window** (**February 20, 2026** to **March 20, 2026**), because **February 19, 2026** serves only as the baseline snapshot for deriving daily sales values.

---

## 3.3. Data Analysis

### 3.3.1. Overview of the Collected Dataset

The data analysis section is based on the same self-collected Lazada dataset described above. The sales data captures product-level information across **30 daily snapshots**, with the **February 19, 2026** snapshot used as a baseline and the main analysis conducted on the period from **February 20, 2026** to **March 20, 2026**. The review data provides additional customer feedback context. Together, these sources support several levels of analysis, including overall dataset description, comparison across categories, relationship analysis among variables, and optional predictive modeling.

At the descriptive level, the dataset is sufficiently structured for analysis. Numeric variables such as price, cumulative units sold, daily units sold, daily revenue, rating score, and review count can be used for distributional and relational analysis. Categorical variables such as category, stock status, and warehouse location can be used to compare product groups and identify structural differences across the product portfolio.

### 3.3.2. General Analytical Approach

The group analyzes the dataset through a combination of descriptive statistics, comparative visualization, and evidence-based interpretation. The analysis follows four main steps:

1. describing the size and structure of the dataset,
2. selecting the variables most relevant to each analytical objective,
3. using chart types appropriate to the nature of the data,
4. drawing conclusions directly from observable patterns in the data.

This approach is consistent with the requirements of the lab, which emphasize correct chart selection, direct interpretation from the data, and the avoidance of unsupported assumptions.

### 3.3.3. Analysis by Theme

#### Theme 1. Sales Performance by Category and Time

This theme examines how sales performance changes across categories and across time. The main variables are `snapshot_date`, `category`, `daily_units_sold`, and `daily_revenue`. Line charts are suitable for showing temporal trends, stacked bar charts are useful for comparing category-level revenue contribution, and heatmaps can help visualize category behavior across dates.

For **Objective 1.1**, the analysis should identify the categories with the strongest revenue contribution over the full analytical period. For **Objective 1.2**, the analysis should compare day-to-day revenue variation across categories in order to distinguish stable categories from volatile ones.

Suggested figures:

- Figure X. Daily revenue trend by category
- Figure Y. Total revenue by category
- Figure Z. Revenue variability by category

Suggested interpretation sentence:

> Based on the category-level revenue trend and revenue variability charts, the analysis shows that [insert top categories] generated the highest total revenue, while [insert volatile categories] displayed the largest day-to-day fluctuations during the analytical period from February 20, 2026 to March 20, 2026.

#### Theme 2. Finance Structure

This theme is presented on the `Finance Structure` dashboard page. The main variables are `selling_price`, `daily_revenue`, `daily_units_sold`, and `Price Band`. The page combines KPI cards, the `Top Trending` line chart, and the `Price Distribution` pie chart to show how the financial structure of the portfolio changes under the selected filter context.

For **Objective 2.1**, the analysis should identify which price band contributes the largest share of revenue. For **Objective 2.2**, the analysis should use the KPI cards and supporting trend chart to assess whether performance changes are broad-based or concentrated.

Suggested figures:

- Figure X. Top Trending
- Figure Y. Price Distribution
- Figure Z. KPI cards on the Finance Structure page

Suggested interpretation sentence:

> The finance-structure analysis indicates that revenue is concentrated in [insert price band], while the KPI cards and trend line show whether the observed performance is broadly distributed or driven by a narrower part of the portfolio.

#### Theme 3. Product Influence Analysis

This theme is presented on the `Product Influence Analysis` page. The main variables are product name, date, and unit-performance measures. The page combines a ranking chart of leading products with a time-trend chart that shows when product-level spikes occur.

For **Objective 3.1**, the analysis should identify the products with the strongest unit performance in the selected period. For **Objective 3.2**, the analysis should examine whether the strongest products maintain stable performance or depend on short-lived spikes.

Suggested figures:

- Figure X. Top Products by Average Unit Sold
- Figure Y. Top Unit
- Figure Z. KPI cards on the Product Influence Analysis page

Suggested interpretation sentence:

> The product-influence analysis shows that a small group of products contributes disproportionately to visible unit performance, while the trend chart reveals whether those products are consistently strong or driven by a few spikes during the analytical window.

#### Theme 4. Customer Ratings and Review Signals

This theme examines customer feedback patterns using the review dataset under the selected year and category filters in the dashboard. The main variables are review month, `review_count`, `average_rating`, and `product_name`. Line charts are suitable for showing monthly review trends and identifying the most-commented products within the selected year.

For **Objective 4.1**, the analysis should use the `Monthly Rating and Review Trends` visual to compare monthly review volume and average rating within the selected year. For **Objective 4.2**, the analysis should use the `Monthly Comment Trends for Top Products` chart to identify which products receive the most comments across months in the selected year and assess whether customer attention is concentrated.

Suggested figures:

- Figure X. Monthly Rating and Review Trends
- Figure Y. Monthly Comment Trends for Top Products
- Figure Z. Review count summary or average rating KPI cards

Suggested interpretation sentence:

> The review-signal analysis suggests that customer feedback activity varies across months within the selected year, while attention is concentrated on [insert product or product group], indicating that customer discussion is not evenly distributed across all Nike products.

#### Theme 5. Machine Learning Insights (Clustering)

The Machine Learning component should be presented as a supporting method for the optional bonus point. In the current dashboard, this support is represented through clustering rather than regression.

For **Objective 5.1**, the analysis should use the silhouette score chart and cluster scatter plot to justify the selected clustering solution. For **Objective 5.2**, the analysis should use the revenue-contribution pie chart together with the scatter plot to explain how the identified segments differ in business significance.

Suggested figures and tables:

- Figure X. Product Segments by Units Sold vs Revenue
- Figure Y. Silhouette Score by Number of Clusters
- Figure Z. Cluster Revenue Contribution (%)

Suggested interpretation sentence:

> The clustering-based Machine Learning component is used as an additional analytical tool to support the group’s common analytical problem. By grouping products into distinct segments and comparing their revenue contribution, the group can show that the Nike catalog contains clearly different product-performance profiles rather than one homogeneous sales pattern.

### 3.3.4. Overall Analytical Summary

The final analytical summary should synthesize the findings from all themes in order to answer the group’s common analytical problem. In particular, the final report should clearly state:

- which categories or products perform best,
- how pricing and discount patterns relate to sales performance,
- how customer feedback appears in relation to product performance,
- whether stock availability and portfolio structure affect the observed outcomes,
- how the optional Machine Learning component further supports the interpretation of sales performance drivers.

Suggested closing paragraph:

> In summary, the analysis of Nike products on Lazada during the analytical period from **February 20, 2026** to **March 20, 2026**, using **February 19, 2026** as the baseline snapshot, provides a structured view of category performance, pricing behavior, customer feedback, and product availability. By combining descriptive visualization with objective-based interpretation, the group is able to identify the main observable patterns in the collected dataset and use them to address the overall analytical problem in a data-driven manner.

### 3.3.5. Final Editing Note

Before submitting the final report, replace all placeholders such as `Figure X`, `Table X`, and `[insert ...]` with the actual figure numbers, chart titles, and results from the completed analysis.
