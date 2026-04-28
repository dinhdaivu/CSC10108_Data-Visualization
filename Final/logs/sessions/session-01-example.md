# Session 01 Example (dd/mm/yyyy)

## Human-first analysis (2-5 dòng)
- Nhóm cần kiểm tra dataset có đạt >=2000 dòng, >=7 biến độc lập, và >50% liên quan Việt Nam.
- Mục tiêu hôm nay: hoàn tất kiểm tra điều kiện và tạo script làm sạch bản nháp.

## Task A - Gatekeeper check
- Helper đã dùng: `/gatekeeper`
- Prompt file: `logs/prompts/2026-04-06-gatekeeper-prompt-example.md`
- AI output file: `logs/generated/2026-04-06-gatekeeper-output-example.md`
- Human-edited file: `logs/edited/2026-04-06-cleaning-script-v1-example.py`
- Evidence file: `logs/evidence/2026-04-06-verification-evidence-example.md`

## Kết quả tạm thời
- PASS: điều kiện dòng dữ liệu.
- Cần xác minh thêm: tỷ lệ liên quan Việt Nam bằng truy vấn rõ ràng.

## Next step
- Chạy `/source-reliability` và lưu tiếp theo cùng format.
