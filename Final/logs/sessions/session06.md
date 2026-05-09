# Session 06 — 02/05/2026

## Human-first analysis (2-5 dòng)
- Nhóm đã tự phác thảo layout 5 tab trên giấy, thống nhất màu chủ đạo navy blue và cam/vàng trước khi hỏi AI.
- Nhóm tự đánh giá: Tab 1 có Pie Chart nhìn "không chuyên nghiệp", cần thay bằng biểu đồ phù hợp hơn.
- Nhờ AI để có đánh giá khách quan và độc lập trước khi quyết định.

## Task A — Phê bình thiết kế Tab 1 và đề xuất cải tiến
- Helper đã dùng: `dashboard-critic`
- Prompt file: `logs/prompts/session06_dashboard_critic.txt`
- AI output file: `logs/generated/session06_critic_tab1.md`
- Human-edited file: (cải tiến áp dụng trực tiếp vào code Tab 1)
- Evidence file: `logs/evidence/session06_tab1_dual_chart.png`

## Kết quả
- 4/5 đề xuất AI được áp dụng: Pie → Donut + 100% Stacked Bar; thêm trendline; tăng font KPI; thêm annotation COVID 2021.
- Đề xuất 3 (Heatmap table) bị nhóm bác bỏ — giữ Line Chart để thể hiện xu hướng theo năm.
- Dual-chart design (Donut + 100% Stacked Bar) hiển thị KHTN/KHXH/Không đầy đủ tổ hợp rõ ràng.

## Next step
- Chạy Session 07 để sinh code Choropleth Map (Tab 4) và Correlation Heatmap (Tab 5).
