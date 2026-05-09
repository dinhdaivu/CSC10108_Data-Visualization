# Session 04 — 26/04/2026

## Human-first analysis (2-5 dòng)
- Nhóm tự xác định 7 bước cần thiết cho pipeline: chuẩn hóa cột → ghép file → trích mã vùng → merge tỉnh → xóa NaN toàn phần → ép kiểu → đồng bộ tên GeoJSON.
- Nhóm nhận ra bước 3 (trích mã vùng) phải đến trước bước 4 (merge tỉnh) — thứ tự logic rõ ràng.
- Nhóm tự viết pseudocode trước khi nhờ AI sinh code Python thực tế.

## Task A — Sinh pipeline tiền xử lý tự động
- Helper đã dùng: `cleaning-script`
- Prompt file: `logs/prompts/session04_cleaning.txt`
- AI output file: `logs/generated/session04_cleaning_v1.py`
- Human-edited file: `logs/edited/session04_cleaning_v2.py`
- Evidence file: `logs/evidence/session04_pipeline_output.txt`

## Kết quả
- Pipeline hoàn chỉnh 7 bước, tái lập được (reproducible).
- Tổng dòng: 4.612.847 → 4.320.441 (sau loại NaN + mã đặc biệt + dtype coerce).
- 63/63 tỉnh khớp GeoJSON: `unmatched = set()` ✓
- Output: `cleaned_thpt.parquet` — (4.320.441, 13) columns.

## Next step
- Chạy `insight-hypothesis` ở Session 05 để xây dựng giả thuyết phân tích cho cả 5 tab.
