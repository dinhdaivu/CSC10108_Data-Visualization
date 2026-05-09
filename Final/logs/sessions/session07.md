# Session 07 — 05/05/2026

## Human-first analysis (2-5 dòng)
- Nhóm tự phác thảo logic Choropleth: GeoJSON → merge điểm TB theo tỉnh → vẽ map với color scale.
- Nhóm biết API `px.choropleth_mapbox` nhưng chưa cấu hình được `featureidkey` đúng cho GeoJSON Việt Nam.
- Tự thử 30 phút, bản đồ bị trống → nhờ AI chẩn đoán và sinh code đầy đủ.

## Task A — Sinh code Choropleth Map tích hợp GeoJSON 63 tỉnh (Vũ Hoàng Minh)
- Helper đã dùng: `cleaning-script` (tái dụng để sinh mã dashboard)
- Prompt file: `logs/prompts/session07_choropleth.txt`
- AI output file: `logs/generated/session07_choropleth_v1.py`
- Human-edited file: `logs/edited/session07_choropleth_v2.py`
- Evidence file: `logs/evidence/session07_choropleth_63tinh.png`

## Task B — Sinh code Correlation Heatmap ma trận Pearson 9×9 (Đinh Đại Vũ)
- Helper đã dùng: `cleaning-script` (tái dụng để sinh mã dashboard)
- Prompt file: `logs/prompts/session07_heatmap.txt`
- AI output file: `logs/generated/session07_heatmap_v1.py`
- Human-edited file: `logs/edited/session07_heatmap_v2.py`
- Evidence file: `logs/evidence/session07_heatmap_9x9.png`

## Kết quả
- 63/63 tỉnh có màu trên choropleth, hover hiển thị tên + điểm TB + rank ✓
- Heatmap 9×9 với label tiếng Việt, ẩn tam giác trên, annotation số liệu ✓
- GeoJSON cache với `@st.cache_data` để tối ưu hiệu năng.

## Next step
- Chạy Session 08 để debug 4 lỗi phát hiện khi test dashboard thực tế.
