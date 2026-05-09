# Session 02 — 17/04/2026

## Human-first analysis (2-5 dòng)
- Nhóm tự tra cứu: dataset Kaggle được tổng hợp từ công bố chính thức của Bộ GD&ĐT, có ghi rõ nguồn gốc.
- Nhóm tự đánh giá SimpleMaps là nhà cung cấp GIS uy tín (trang web chuyên nghiệp, được dùng trong nhiều dự án mã nguồn mở).
- Nhóm chủ động ghi rõ nguồn vào báo cáo trước khi hỏi AI để kiểm tra có thiếu sót gì không.

## Task A — Đánh giá độ tin cậy nguồn dữ liệu
- Helper đã dùng: `source-reliability`
- Prompt file: `logs/prompts/session02_source_reliability.txt`
- AI output file: `logs/generated/session02_source_reliability.md`
- Human-edited file: (hash script inline)
- Evidence file: `logs/evidence/session02_source_hashes.txt`

## Kết quả
- Kaggle dataset: RELIABLE với điều kiện ghi rõ link + ngày tải + hash file.
- SimpleMaps GeoJSON: RELIABLE.
- mavung.csv (tự tổng hợp): CONDITIONAL — đã đối chiếu danh mục Bộ Nội vụ.
- Tất cả 7 file nguồn đã được đóng băng phiên bản bằng MD5 hash.

## Next step
- Chạy `data-quality` ở Session 03 để định lượng missing values và outlier.
