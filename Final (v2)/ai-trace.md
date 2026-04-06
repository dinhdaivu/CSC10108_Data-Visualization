# AI Trace (Markdown duy nhất để nộp quy trình AI)

> Mục tiêu: đáp ứng yêu cầu lưu vết theo chuỗi: **Prompt -> Script AI sinh ra -> Script sau chỉnh sửa -> Kết quả đã kiểm chứng**.

---

## 0. Thông tin nhóm

- Chủ đề dashboard:
- Thành viên:
- Công cụ dashboard (Power BI/Tableau/Streamlit/...):
- Dataset chính:
- Ngày bắt đầu:
- Thư mục log chính: `logs/`
- Session hiện tại: `logs/sessions/`
- Prompt lưu tại: `logs/prompts/`
- AI output lưu tại: `logs/generated/`
- Human-edited lưu tại: `logs/edited/`
- Evidence lưu tại: `logs/evidence/`

---

## 1. Session log

### Session 01 - [dd/mm/yyyy]

#### Human-first analysis (bắt buộc, 2-5 dòng)

-

#### Task A - [Tên task]

- Mục tiêu:
- Helper đã dùng: (Gatekeeper / Source / Quality / Cleaning / Insight / Dashboard / Viva)
- Prompt đã dùng:

```text
[dán prompt]
```

- AI output (tóm tắt + link/file):
- Script AI sinh ra (file hoặc snippet):
- Script sau chỉnh sửa bởi nhóm (file hoặc snippet):
- Cách kiểm chứng:
  - [ ] Kiểm tra số dòng
  - [ ] Kiểm tra số biến độc lập
  - [ ] Kiểm tra tỷ lệ liên quan Việt Nam > 50%
  - [ ] Kiểm tra missing/duplicate/outlier
  - [ ] Kiểm tra chart phản ánh đúng insight
- Bằng chứng (ảnh/table/output):
- Kết quả đã xác nhận:
- Rủi ro/giới hạn còn lại:

#### Task B - [Tên task]

- Mục tiêu:
- Helper đã dùng:
- Prompt đã dùng:

```text
[dán prompt]
```

- AI output:
- Script AI sinh ra:
- Script sau chỉnh sửa bởi nhóm:
- Cách kiểm chứng:
- Bằng chứng:
- Kết quả đã xác nhận:
- Rủi ro/giới hạn còn lại:

---

## 2. Dataset compliance checklist (bắt buộc)

- [ ] Dữ liệu thật
- [ ] Ngữ cảnh Việt Nam
- [ ] Dữ liệu dạng bảng
- [ ] >= 2000 dòng
- [ ] >= 7 biến độc lập
- [ ] > 50% dữ liệu liên quan Việt Nam
- [ ] Nguồn minh bạch và đáng tin cậy

Ghi chú kiểm chứng:

-

---

## 3. Insight đã kiểm chứng (đưa vào dashboard)

| # | Insight | Biến sử dụng | Chart | Bằng chứng | AI gợi ý hay nhóm tự tìm | Trạng thái |
|---|---|---|---|---|---|---|
| 1 |  |  |  |  |  | Draft/Verified |
| 2 |  |  |  |  |  | Draft/Verified |
| 3 |  |  |  |  |  | Draft/Verified |

---

## 4. Tổng kết AI usage (cho báo cáo cuối)

- AI hỗ trợ phần nào:
- Nhóm đã chỉnh sửa gì:
- Nhóm đã kiểm chứng bằng cách nào:
- Hạn chế/rủi ro khi dùng AI:
- Bài học rút ra:
