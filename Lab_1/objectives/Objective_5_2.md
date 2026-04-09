# Objective 5.2 - Cluster Revenue Contribution Interpretation

Use the **cluster scatter chart** together with the **pie chart of revenue contribution by cluster** to interpret how each product segment contributes to overall Nike sales performance from **February 20, 2026** to **March 20, 2026**, in order to explain which clusters dominate total revenue and which clusters represent smaller but distinct performance groups.

- `Specific`: Compare revenue contribution across `segment_id` and relate each cluster's share of revenue to its position in the cluster scatter chart.
- `Measurable`: Uses `% revenue contribution` by cluster, cluster membership on the scatter chart, and differences in `avg_daily_revenue` or `avg_total_period_revenue`.
- `Achievable`: The required fields are available from `product_segments.csv` and `segment_profiles.csv`.
- `Relevant`: Directly supports the analytical problem by linking clustered product characteristics to overall sales performance contribution.
- `Time-bound`: Limited to the same analytical period from `20-02-2026` to `20-03-2026`.

## Suggested chart evidence
- Scatter chart: X = `pca_component_1`, Y = `pca_component_2`, Legend = `segment_id`.
- Pie or donut chart: Legend = `segment_id`, Values = cluster revenue share based on `avg_total_period_revenue` or aggregated cluster revenue.
- Optional supporting table: `segment_id`, `product_count`, `product_share`, `avg_daily_revenue`, `avg_total_period_revenue`.
