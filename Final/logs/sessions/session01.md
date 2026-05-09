# Session 01 — 10/04/2026

## Human-first analysis (2-5 dòng)
- Nhóm tổng hợp 5 file CSV (thpt2020–thpt2024) và đếm thủ công: tổng xấp xỉ 4,6 triệu dòng.
- Liệt kê 11 cột: sbd, toan, ngu_van, ngoai_ngu, vat_ly, hoa_hoc, sinh_hoc, lich_su, dia_ly, gdcd, nam.
- 100% dữ liệu là thí sinh Việt Nam → tỷ lệ Việt Nam = 100% (vượt ngưỡng 50%).
- Nhóm tự đánh giá PASS cả 3 tiêu chí trước khi dùng AI xác nhận lại.

## Task A — Kiểm định dataset theo yêu cầu đồ án (gatekeeper)
- Helper đã dùng: `gatekeeper`
- Prompt file: `logs/prompts/session01_gatekeeper.txt`
- AI output file: `logs/generated/session01_gatekeeper_output.md`
- Human-edited file: (inline, không tách riêng)
- Evidence file: `logs/evidence/session01_combined_info.png`

## Task B — Xác nhận cấu trúc cột và kiểu dữ liệu
- Helper đã dùng: `gatekeeper`
- Prompt file: `logs/prompts/session01_dtype_check.txt`
- AI output file: `logs/generated/session01_dtype_fix.md`
- Human-edited file: (inline, không tách riêng)
- Evidence file: `logs/evidence/session01_dtype_check.png`

## Kết quả
- Dataset PASS toàn bộ: 4.612.847 dòng, 11 cột, 100% Việt Nam.
- Tất cả cột điểm ép về float64, không còn giá trị ngoài [0, 10].
- Ghi rõ nguồn Kaggle, ngày tải 08/04/2026.

## Next step
- Chạy `source-reliability` ở Session 02 để luận chứng tính tin cậy 3 nguồn dữ liệu.
