# AI Helpers Starter (Final Project)

README này là hướng dẫn chạy nhanh bộ AI helpers cho đồ án dashboard dữ liệu Việt Nam.

## Mục tiêu

- Dùng AI đúng quy trình môn học.
- Lưu được toàn bộ bằng chứng cho vấn đáp.
- Có thể chạy gần như toàn bộ flow chỉ bằng slash commands (`/`).

## File quan trọng

- `Requirements.md`: yêu cầu chính thức của đồ án.
- `Notes.md`: lưu ý triển khai, yêu cầu báo cáo AI, vấn đáp.
- `ai-trace.md`: nhật ký bắt buộc theo chuỗi Prompt -> AI output -> Human-edited -> Verified.
- `viva-checklist.md`: checklist trước vấn đáp + câu hỏi theo từng thành viên.
- `.github/prompts/*.prompt.md`: slash commands cho từng helper.

## Tổ chức thư mục log (khuyến nghị)

Sử dụng cấu trúc sau để quản lý log/evidence rõ ràng trước khi nộp:

- `logs/sessions/`: markdown log theo từng session (bản cắt nhỏ từ `ai-trace.md` nếu cần).
- `logs/prompts/`: prompt đã dùng thực tế.
- `logs/generated/`: output/script do AI sinh.
- `logs/edited/`: script đã chỉnh sửa bởi nhóm.
- `logs/evidence/`: ảnh chụp, bảng số liệu, output kiểm chứng.
- `logs/archive/`: bản đóng gói hoặc snapshot cuối kỳ.

## Bắt đầu trong 3 phút

1. Mở `ai-trace.md` và điền thông tin nhóm + chủ đề.
2. Viết **Human-first analysis** (2-5 dòng).
3. Mở chat, gõ `/gatekeeper` và dán input dataset.
4. Chạy lần lượt các lệnh còn lại theo thứ tự khuyến nghị.
5. Sau mỗi lệnh, cập nhật lại `ai-trace.md`.

## Chạy bằng Slash Commands (`/`)

Các prompt đã được cấu hình trong `.github/prompts/`.

### Lệnh tổng

- Không dùng lệnh tổng.
- Chạy theo từng lệnh để kiểm soát chất lượng và bằng chứng tốt hơn.

### Lệnh theo từng bước

- `/gatekeeper` - kiểm tra điều kiện môn học (rows, variables, Vietnam ratio, source)
- `/source-reliability` - đánh giá độ tin cậy nguồn
- `/data-quality` - rà soát chất lượng dữ liệu
- `/cleaning-script` - tạo script làm sạch starter
- `/insight-hypothesis` - tạo giả thuyết insight + chart
- `/dashboard-critic` - phản biện dashboard
- `/viva-report` - tạo bộ câu hỏi vấn đáp + tóm tắt AI usage

### Thứ tự chạy khuyến nghị

1. `/gatekeeper`
2. `/source-reliability`
3. `/data-quality`
4. `/cleaning-script`
5. `/insight-hypothesis`
6. `/dashboard-critic`
7. `/viva-report`

> Nếu chưa thấy lệnh mới: đóng/mở lại chat hoặc reload VS Code window, sau đó gõ lại `/`.

## Input mẫu cho các lệnh

Dán block này và điền thông tin:

```text
Chủ đề dashboard: [điền]
Dataset: [tên]
Nguồn: [link + đơn vị phát hành]
Số dòng hiện có: [điền]
Danh sách cột: [điền]
Ước tính tỷ lệ liên quan Việt Nam: [điền]
Thành viên nhóm: [danh sách]
Mục tiêu phiên làm việc hôm nay: [điền]
```

## Tiêu chí pass nhanh (trước khi build dashboard)

- Dữ liệu dạng bảng.
- Số dòng >= 2000.
- Số biến độc lập >= 7.
- Tỷ lệ dữ liệu liên quan Việt Nam > 50%.
- Nguồn dữ liệu rõ ràng, đáng tin cậy.

## Tiêu chí pass cuối (trước khi vấn đáp)

- Dashboard có phân tích, không chỉ mô tả.
- Insight có bằng chứng cụ thể.
- Có tích hợp AI trong thiết kế/vận hành.
- Báo cáo bằng tiếng Việt.
- Mỗi thành viên có ít nhất 2 câu hỏi vấn đáp đã luyện.

## Checklist cuối mỗi session

- [ ] Đã ghi Human-first analysis.
- [ ] Đã lưu prompt đã dùng.
- [ ] Đã lưu output AI.
- [ ] Đã lưu script/chỉnh sửa của nhóm.
- [ ] Đã lưu bằng chứng kiểm chứng.
- [ ] Đã cập nhật kết luận tạm thời + rủi ro trong `ai-trace.md`.
