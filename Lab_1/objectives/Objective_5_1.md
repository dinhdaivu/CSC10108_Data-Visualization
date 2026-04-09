# Objective 5.1 - Clustering Quality and Segment Identification

Use the **silhouette score comparison bar chart** and the **cluster scatter chart** to evaluate the clustering solution and identify distinct Nike product groups from **February 20, 2026** to **March 20, 2026**, in order to show that the dataset can be meaningfully segmented into different sales-performance patterns.

- `Specific`: Compare clustering quality across candidate cluster settings using `silhouette_score`, then visualize product distribution by `segment_id` on the scatter chart.
- `Measurable`: Uses differences in `silhouette_score` across cluster options and visible separation of products by `segment_id` on the scatter plot.
- `Achievable`: All required fields are available in `segmentation_metrics.csv` and `product_segments.csv`.
- `Relevant`: Supports the analytical problem by showing that products can be grouped into meaningful clusters before interpreting sales behavior.
- `Time-bound`: Evaluated within the analysis window from `20-02-2026` to `20-03-2026`.

## Suggested chart evidence
- Bar chart: Axis = `n_clusters`, Values = `silhouette_score`.
- Scatter chart: X = `pca_component_1`, Y = `pca_component_2`, Legend = `segment_id`.
