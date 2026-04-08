# Objective 5.2 — Segment Performance Driver Interpretation

Interpret which variables are most associated with high- and low-performing clusters by combining the segment visuals with feature-importance evidence, in order to explain why some segments outperform others during **February 20, 2026** to **March 20, 2026**.

- `Specific`: Driver-focused interpretation across segments using feature relevance and segment-level outcomes.
- `Measurable`: Uses `importance_mean` ranking, segment differences in `avg_daily_revenue` and `avg_total_period_revenue`, and concentration of `product_count`.
- `Achievable`: Feature-importance chart and segment summary metrics are already available on the dashboard page.
- `Relevant`: Strengthens ML storytelling by linking cluster outcomes to interpretable performance drivers.
- `Time-bound`: Limited to the same analytical period from `20-02-2026` to `20-03-2026`.

## Suggested chart evidence
- Feature-importance bar chart: ranked `importance_mean` by feature.
- Segment scatter chart and segment table for outcome comparison.
- Optional slicers: `segment_id`, `category`, date range.
