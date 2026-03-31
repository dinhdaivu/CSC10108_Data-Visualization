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

Analyze daily revenue and daily units sold by product category from **February 20, 2026** to **March 20, 2026** in order to identify the **three categories with the highest total revenue** during the study period.

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

#### Theme 2. Pricing and Discount Strategy

This theme focuses on the relationship between pricing, discount level, and sales outcomes.

**Objective 2.1**

Quantify the relationship between discount rate and sales performance for Nike products from **February 20, 2026** to **March 20, 2026** in order to determine the **discount ranges associated with stronger revenue and higher daily units sold**.

- `Specific`: Discount effectiveness in relation to sales outcomes
- `Measurable`: Uses discount rate, `daily_units_sold`, and `daily_revenue`
- `Achievable`: `selling_price` and `original_price` support direct discount-rate calculation
- `Relevant`: Helps evaluate how discount policy relates to product performance
- `Time-bound`: Evaluated within the analytical window from `20-02-2026` to `20-03-2026`

**Objective 2.2**

Compare revenue contribution and stability across predefined price bands from **February 20, 2026** to **March 20, 2026** in order to identify the **price segment with the best balance between scale and consistency**.

- `Specific`: Price-segment comparison
- `Measurable`: Uses total `daily_revenue`, average `daily_units_sold`, and variation measures by band
- `Achievable`: Price bands can be created from the existing price variables
- `Relevant`: Supports interpretation of pricing structure and sales performance
- `Time-bound`: Limited to the same analytical period from `20-02-2026` to `20-03-2026`

#### Theme 3. Customer Ratings and Review Signals

This theme focuses on how customer feedback appears in relation to product performance.

**Objective 3.1**

Analyze the relationship among `rating_score`, `review_count`, and `cumulative_units_sold` in the **March 20, 2026** snapshot in order to determine whether products with stronger social proof tend to achieve better sales performance.

- `Specific`: Relationship between social proof and product performance
- `Measurable`: Uses `rating_score`, `review_count`, and `cumulative_units_sold`
- `Achievable`: All required fields are available in the final snapshot
- `Relevant`: Customer trust signals are important in e-commerce environments
- `Time-bound`: Limited to the final snapshot date

**Objective 3.2**

Analyze review rating distribution and review-time patterns in the collected review dataset in order to identify **dominant sentiment patterns** and **longer-term customer feedback trends**, while explicitly separating these review patterns from the main sales-analysis window that runs from **February 20, 2026** to **March 20, 2026**.

- `Specific`: Rating distribution and temporal review patterns
- `Measurable`: Uses review `rating`, review frequency over time, and review-period summaries
- `Achievable`: Review fields are already available in the collected dataset
- `Relevant`: Adds customer feedback context to the broader sales analysis
- `Time-bound`: Evaluated using the review records stored in the project dataset

#### Theme 4. Inventory and Product Portfolio Structure

This theme focuses on stock availability and the structure of the product portfolio.

**Objective 4.1**

Track in-stock ratio and product listing count by category from **February 20, 2026** to **March 20, 2026** in order to identify categories with the **highest stockout pressure** and estimate potential sales opportunity loss.

- `Specific`: Stock availability and listing dynamics by category
- `Measurable`: Uses in-stock counts, out-of-stock counts, in-stock ratio, and category-level sales
- `Achievable`: Variables are directly available in the daily snapshots
- `Relevant`: Stock availability may affect sales performance and product visibility
- `Time-bound`: Limited to the analytical period from `20-02-2026` to `20-03-2026`

**Objective 4.2**

Measure revenue concentration from top products in the **March 20, 2026** snapshot and over the full analytical period in order to determine whether sales are diversified or highly dependent on a relatively small number of products.

- `Specific`: Product concentration and portfolio risk
- `Measurable`: Uses top-product revenue share and concentration indicators
- `Achievable`: Product-level revenue and sales fields are available
- `Relevant`: Supports interpretation of product portfolio structure
- `Time-bound`: Includes the final snapshot and the full period summary

#### Theme 5. Machine Learning Support for Sales Performance Drivers

This theme uses Machine Learning as a supporting analytical method to strengthen the interpretation of the common analytical problem. Instead of presenting ML as a purely technical forecasting task, the theme focuses on how predictive models can help reveal which product characteristics are most consistently associated with stronger sales performance and which combinations of signals are associated with short-term sales weakness.

**Objective 5.1**

Develop and compare interpretable regression models for `daily_units_sold` at the product-day level using category, selling price, discount rate, stock status, rating score, review count, cumulative sales, and time-related features from **February 20, 2026** to **March 20, 2026**, in order to estimate short-term sales performance, assess whether the selected model performs better than a baseline benchmark, and rank the relative influence of the main sales drivers through model interpretation.

- `Specific`: Interpretable regression analysis of short-term sales drivers
- `Measurable`: Uses `MAE`, `RMSE`, and `R^2`, together with feature-ranking outputs such as coefficients or permutation importance
- `Achievable`: The required variables are available in the cleaned sales dataset and can be modeled with baseline, linear, and tree-based methods
- `Relevant`: Directly supports the common analytical problem by quantifying which observed product factors are most strongly associated with better sales performance
- `Time-bound`: Model trained on earlier dates and evaluated on later dates within the same analytical period from `20-02-2026` to `20-03-2026`, while `19-02-2026` is retained only as the baseline snapshot

**Objective 5.2**

Develop a product segmentation model using clustering techniques on variables such as selling price, discount rate, rating score, review count, cumulative units sold, average daily units sold, average daily revenue, stock availability, and sales volatility, in order to identify distinct product groups with different sales-performance profiles and to explain how these groups reflect the combined influence of category, pricing, stock status, and customer feedback.

- `Specific`: Clustering-based analysis of product performance segments
- `Measurable`: Uses cluster quality indicators such as silhouette score and interprets segment profiles through average feature values
- `Achievable`: Product-level aggregated features can be constructed directly from the existing sales dataset
- `Relevant`: Supports the common analytical problem by revealing meaningful groups of products with stronger or weaker performance characteristics
- `Time-bound`: Built from the analytical dataset spanning **February 20, 2026** to **March 20, 2026**, with **February 19, 2026** retained only as the baseline snapshot

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

#### Theme 2. Pricing and Discount Strategy

This theme examines how price structure and discount policy relate to sales performance. The main variables are `selling_price`, `original_price`, discount rate, `daily_units_sold`, and `daily_revenue`. Scatter plots are suitable for exploring the relationship between discount and units sold, while boxplots and grouped bar charts can be used to compare price bands and their revenue contribution.

For **Objective 2.1**, the analysis should examine whether products with larger discount rates tend to achieve stronger revenue or daily sales performance. For **Objective 2.2**, the analysis should compare predefined price bands in terms of both scale and stability.

Suggested figures:

- Figure X. Discount rate versus daily units sold
- Figure Y. Revenue by price band
- Figure Z. Revenue distribution across price segments

Suggested interpretation sentence:

> The price and discount analysis indicates that [insert finding about discount range or price segment]. This suggests that products in the [insert price band] segment contribute [more/less] consistently to revenue compared with other price groups in the dataset.

#### Theme 3. Customer Ratings and Review Signals

This theme examines whether customer evaluation signals are associated with stronger product performance. The main variables are `rating_score`, `review_count`, `cumulative_units_sold`, `rating`, and `review_time`. Scatter plots with trendlines can be used to study the relationship between ratings, review count, and sales, while histograms and time-series review charts can be used to describe the distribution and timing of customer feedback.

For **Objective 3.1**, the analysis should examine whether higher rating scores and higher review counts are associated with stronger cumulative sales in the final snapshot. For **Objective 3.2**, the analysis should describe broader sentiment patterns in the review dataset and clearly note that review timing extends beyond the main sales-analysis period from **February 20, 2026** to **March 20, 2026**.

The review data is heavily concentrated in positive feedback, with **7,003 five-star reviews** out of **7,605 total reviews**. The lower ratings are much less common, including **340 one-star reviews**, **36 two-star reviews**, **84 three-star reviews**, and **142 four-star reviews**.

Suggested figures:

- Figure X. Rating score versus cumulative units sold
- Figure Y. Distribution of review ratings
- Figure Z. Review frequency over time

Suggested interpretation sentence:

> The review analysis shows that customer feedback is dominated by five-star ratings, indicating an overall positive sentiment pattern in the collected review dataset. However, because review timestamps span a longer period than the sales snapshots, these review trends should be interpreted as broader customer feedback signals rather than direct short-term sales drivers.

#### Theme 4. Inventory and Product Portfolio Structure

This theme examines stock availability and the concentration of performance within the product portfolio. The main variables are `category`, `stock_status`, listing count, and revenue-related indicators. Bar charts, line charts, and treemaps are suitable for showing inventory structure and portfolio concentration.

For **Objective 4.1**, the analysis should compare in-stock and out-of-stock proportions across categories and track how listing counts change over time. For **Objective 4.2**, the analysis should evaluate whether the observed revenue is broadly distributed or concentrated in a relatively small number of top-performing products.

Suggested figures:

- Figure X. In-stock versus out-of-stock products by category
- Figure Y. Listing count trend over time
- Figure Z. Revenue share by category or top-product concentration

Suggested interpretation sentence:

> The inventory and portfolio analysis suggests that [insert category or product concentration finding]. This implies that sales performance in the dataset is [well distributed / concentrated] across the product portfolio.

#### Theme 5. Machine Learning Support for the Common Analytical Problem

The Machine Learning component should be presented as a supporting method for the optional bonus point. Its purpose is not simply to forecast future values, but to strengthen the interpretation of the common analytical problem by testing whether the factors discussed in the earlier themes can also explain or predict stronger and weaker sales outcomes.

For **Objective 5.1**, regression models may be used to predict `daily_units_sold` from category, price, discount, stock status, rating score, review count, cumulative sales, location, and time-related features. The purpose of this objective is not only to compare model accuracy, but also to identify which variables repeatedly appear as the strongest explanatory signals of short-term sales performance. Accordingly, the report should discuss both model metrics such as `MAE`, `RMSE`, and `R^2` and the feature-level interpretation of the selected model.

For **Objective 5.2**, a clustering model may be used to segment products into groups with distinct performance profiles. This objective should be interpreted as a way to identify meaningful product segments rather than as a purely technical modeling exercise. The report should therefore describe the cluster quality, summarize the profile of each segment, and explain how the segments differ in terms of pricing, discount level, stock availability, customer feedback, and observed sales performance.

Suggested figures and tables:

- Table X. Regression model comparison
- Table Y. Product segmentation metrics and selected number of clusters
- Figure Z. Cluster profile comparison or segment-center visualization

Suggested interpretation sentence:

> The Machine Learning component is used as an additional analytical tool to support the group’s common analytical problem. By combining regression-based explanation of sales level with clustering-based product segmentation, the group can examine not only which factors are associated with stronger sales performance, but also how different combinations of those factors form distinct product-performance profiles. Model results should still be interpreted cautiously due to the short observation window and the platform-specific nature of the dataset.

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
