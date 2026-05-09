# Session 03 — 23/04/2026

## Human-first analysis (2-5 dòng)
- Nhóm quan sát thủ công 100 dòng ngẫu nhiên: thấy nhiều dòng có toàn bộ cột điểm là NaN (thí sinh đăng ký nhưng không thi).
- Không thấy duplicate rõ ràng khi nhìn bằng mắt (số báo danh có vẻ unique).
- Không phát hiện điểm > 10 hoặc < 0 trong sample nhỏ.
- Nhóm quyết định cần script tự động để kiểm tra trên toàn tập 4,6M dòng.

## Task A — Rà soát missing values và duplicate
- Helper đã dùng: `data-quality`
- Prompt file: `logs/prompts/session03_dq_check.txt`
- AI output file: `logs/generated/session03_dq_script.py`
- Human-edited file: (script inline)
- Evidence file: `logs/evidence/session03_dq_report.txt`

## Task B — Phát hiện outlier điểm số
- Helper đã dùng: `data-quality`
- Prompt file: `logs/prompts/session03_outlier.txt`
- AI output file: `logs/generated/session03_outlier_script.py`
- Human-edited file: (script inline)
- Evidence file: `logs/evidence/session03_outlier_table.md`

## Kết quả
- 147.234 dòng NaN toàn phần (3,19%) — thí sinh đăng ký không dự thi, quyết định loại bỏ.
- 0 dòng duplicate theo (sbd, nam).
- Không có lỗi dữ liệu điểm ngoài [0, 10].
- IQR outlier ở Ngoại ngữ (24%) là hiện tượng thực (bimodal), không phải lỗi.

## Next step
- Chạy `cleaning-script` ở Session 04 để sinh pipeline tiền xử lý hoàn chỉnh.
