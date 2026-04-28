---
name: "dashboard-critic"
description: "Use when: standalone dashboard critique for clarity, analysis depth, and viva readiness"
argument-hint: "Paste goal + chart list + filters + screenshot summary"
agent: "agent"
---

Use the following full project constraints exactly.

## Full Requirements (from Requirements.md)

### Đồ Án Cuối Kỳ - Trực Quan Hóa Dữ Liệu

#### Nội dung
- Trình bày một dự án ứng dụng trực quan sử dụng dashboard để phân tích dữ liệu.
- Ngữ cảnh của dữ liệu là Việt Nam.
- Các nhóm sẽ trình bày trong buổi vấn đáp.

#### Yêu cầu về dữ liệu
- Là dữ liệu thật, có liên quan đến đất nước Việt Nam.
- Có tối thiểu 7 biến độc lập.
- Có tối thiểu 2000 dòng dữ liệu.
- Tổng số dữ liệu liên quan đến Việt Nam phải chiếm trên 50% toàn bộ tập dữ liệu.

#### Các tiêu chí đánh giá
1. Kết hợp nguồn dữ liệu đáng tin cậy:
	- Nguồn dữ liệu phải đáng tin cậy và minh bạch.
	- Kiểm tra thiếu sót trong quy trình xử lý dữ liệu.
2. Phù hợp với mục đích:
	- Trực quan hóa phải phản ánh đúng mục đích cụ thể.
	- Chọn loại biểu đồ phù hợp với bài toán.
3. Rõ ràng và dễ hiểu:
	- Truyền đạt thông điệp rõ ràng.
4. Sự tích hợp và liên kết:
	- Nếu có nhiều biểu đồ, phải có liên kết logic.
5. Tương tác và điều hướng:
	- Tương tác hợp lý, điều hướng dễ dùng.
6. Thiết kế hấp dẫn:
	- Màu sắc có ý nghĩa, tránh quá tải.
7. Phân tích dữ liệu:
	- Thể hiện xu hướng/thay đổi theo thời gian (nếu có).
	- Làm rõ quan hệ giữa các biến.
	- Rút ra kết luận và câu chuyện từ dữ liệu.
8. Tích hợp AI:
	- Có tích hợp AI trong thiết kế và vận hành.

## Full Notes (from Notes.md)

#### Ngữ cảnh
- Đồ án dùng dashboard để phân tích dữ liệu.
- Dữ liệu phải gắn với Việt Nam.
- Trình bày trong buổi vấn đáp với giảng viên/trợ giảng.

#### Yêu cầu về dữ liệu
- Dữ liệu dạng bảng.
- Ít nhất 7 biến độc lập.
- Tối thiểu 2000 dòng.
- Có thể tự thu thập, dùng Kaggle hoặc nguồn chính thống.

#### Thu thập dữ liệu
- Được dùng công cụ hỗ trợ (AI, Selenium, ...).
- Ưu tiên dữ liệu có yếu tố thú vị (ngoại lệ, bất thường, bất ngờ).

#### Thiết kế dashboard
- Cần tích hợp AI trong quá trình thiết kế.
- AI có thể hỗ trợ lên ý tưởng/brainstorm/đánh giá khuyết điểm.
- Công cụ dashboard không giới hạn (Power BI, Tableau, Streamlit, ...).

#### Định hướng phân tích
- Dashboard phải phục vụ phân tích, không chỉ trình bày.
- Insight cần thú vị và có chiều sâu.
- Lưu lại các insight đáng chú ý cho báo cáo.

#### Lưu ý quan trọng
- Cần báo cáo quá trình tương tác với Agent và AI.
- Mỗi thành viên chuẩn bị ít nhất 2 câu hỏi.
- Trình bày và báo cáo bằng tiếng Việt.
- Lưu toàn bộ quá trình dùng AI bằng một file Markdown.

#### Quy trình lưu vết AI
- Cần ghi theo chuỗi:
  - Prompt
  - Script được AI sinh ra
  - Script sau khi đã chỉnh sửa
- Bắt buộc tự phân tích trước, sau đó mới dùng AI hỗ trợ.

Input:
{{input}}

Behavior:
- If screenshot/layout details are missing, ask for them briefly before final review.

Review criteria:
- clarity/readability
- chart appropriateness
- linkage among visuals
- interaction/navigation
- color usage
- analysis depth (not only presentation)

Output strictly:
Use these exact headings in order:

## 1) Input snapshot
- Summarize provided goal/charts/filters/layout details in 3-6 bullets.

## 2) Core analysis
- 3 strongest points.
- 5 urgent fixes (priority order).
- Concrete improvements.

## 3) Priority actions
- Immediate next 5 dashboard edits in execution order.

## 4) Manual verification checklist
- Checklist items team must verify manually.

## 5) Block dán vào `ai-trace.md`
- Include the 60-90 second Vietnamese viva explanation draft and key review notes.
