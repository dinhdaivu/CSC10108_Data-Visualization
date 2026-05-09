# Session 08 — 08/05/2026

## Human-first analysis (2-5 dòng)
- Nhóm phát hiện 4 lỗi khi test dashboard thực tế: (1) chart Top 5% trả cùng giá trị mọi năm, (2) heatmap xuất hiện NaN ở một số ô, (3) choropleth thiếu màu 4 tỉnh, (4) chatbot lỗi gửi ảnh lên Gemini.
- Nhóm tự chẩn đoán lỗi 1 (thiếu groupby năm) và lỗi 2 (ít thí sinh thi cả KHTN lẫn KHXH) đúng nguyên nhân trước khi nhờ AI xác nhận.

## Task A — Debug lỗi Top 5% và NaN trong heatmap (Nguyễn Đỗ Bảo)
- Helper đã dùng: (không dùng helper chuẩn, mô tả lỗi trực tiếp)
- Prompt file: `logs/prompts/session08_debug_top5_corr.txt`
- AI output file: `logs/generated/session08_debug_analysis.md`
- Human-edited file: `logs/edited/session08_debug_top5_corr_v2.py`
- Evidence file: `logs/evidence/session08_top5_fixed.png`, `session08_corr_no_nan.png`

## Task B — Debug Choropleth thiếu tỉnh và Chatbot encode lỗi (Nguyễn Đỗ Bảo)
- Helper đã dùng: (không dùng helper chuẩn)
- Prompt file: `logs/prompts/session08_debug_geo_chatbot.txt`
- AI output file: `logs/generated/session08_debug_geo_chatbot.md`
- Human-edited file: `logs/edited/session08_debug_geo_chatbot_v2.py`
- Evidence file: `logs/evidence/session08_choropleth_63_fixed.png`, `session08_chatbot_gemini_ok.png`

## Kết quả
- Lỗi 1: Thêm `nam` vào `groupby(['khoi', 'nam'])` — Top 5% hiển thị đúng theo năm ✓
- Lỗi 2: `min_periods=100` trong `corr()` — không còn NaN trong heatmap ✓
- Lỗi 3: `TINH_MAP` mapping thủ công — 63/63 tỉnh có màu ✓
- Lỗi 4: `plotly.io.to_image()` thay `st.pyplot()` — chatbot Gemini nhận ảnh thành công ✓

## Next step
- Dashboard hoàn chỉnh. Kiểm tra toàn bộ ai-trace.md và logs/ trước khi nộp.
