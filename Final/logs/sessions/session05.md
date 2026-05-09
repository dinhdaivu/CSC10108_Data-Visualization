# Session 05 — 29/04/2026

## Human-first analysis (2-5 dòng)
- Nhóm thảo luận nội bộ 45 phút, mỗi người tự liệt kê 3–4 câu hỏi phân tích cho tab mình phụ trách.
- Tổng hợp được 18 câu hỏi ban đầu, lọc còn 12 câu do một số câu thiếu biến để kiểm chứng.
- Nhóm mang 12 câu đã lọc vào prompt AI để bổ sung và làm sâu hơn thành 16 giả thuyết.

## Task A — Xây dựng giả thuyết phân tích Tab 1 và Tab 2
- Helper đã dùng: `insight-hypothesis`
- Prompt file: `logs/prompts/session05_hypotheses_tab12.txt`
- AI output file: `logs/generated/session05_hypotheses_tab12.md`
- Human-edited file: (scripts kiểm chứng inline)
- Evidence file: `logs/evidence/session05_h1.png`, `session05_h2_rejected.png`, `session05_h5_bimodal.png`

## Task B — Xây dựng giả thuyết phân tích Tab 3, Tab 4, Tab 5
- Helper đã dùng: `insight-hypothesis`
- Prompt file: `logs/prompts/session05_hypotheses_tab345.txt`
- AI output file: `logs/generated/session05_hypotheses_tab345.md`
- Human-edited file: (scripts kiểm chứng inline)
- Evidence file: `logs/evidence/session05_corr_matrix.png`, `session05_h10.png`, `session05_h14.png`

## Kết quả
- 16 giả thuyết tổng cộng (8 Tab 1+2, 8 Tab 3+4+5).
- 13/16 xác nhận, 3/16 bác bỏ: H2 (quy mô thí sinh giảm 2021), H7, H16 (Toán–Lý cao nhất).
- Insight nổi bật: Lý–Hóa (r=0,724) cao hơn Toán–Lý (r=0,681); Ngoại ngữ bimodal 2021.

## Next step
- Chạy `dashboard-critic` ở Session 06 để phê bình thiết kế Tab 1 và đề xuất cải tiến.
