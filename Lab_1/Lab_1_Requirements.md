# Lab 01: Thu thập dữ liệu và trực quan hóa dữ liệu

## 1. Quy định chung

- Bài làm được thực hiện theo nhóm từ `3` đến `5` thành viên.
- Thành viên không tham gia sẽ không có điểm bài tập này.
- Bài làm phải tuân thủ đúng yêu cầu của đồ án.
- Mọi tài liệu tham khảo cần được ghi đầy đủ trong báo cáo ở mục **Tài liệu tham khảo**.
- Các công cụ hỗ trợ như `ChatGPT`, `GitHub Copilot`, ... chỉ được dùng để tham khảo; nội dung phải được kiểm tra và chỉnh sửa cho phù hợp với bài toán.
- Nếu phát hiện lạm dụng công cụ AI để sinh nội dung, hoặc nội dung tạo ra sai lệch/không phù hợp, nhóm có thể bị trừ tối đa `50%` số điểm tùy mức độ.
- Bài làm giống nhau sẽ bị `0 điểm`.

## 2. Giới thiệu đồ án

### 2.1. Bối cảnh

Trong những năm gần đây, các sàn thương mại điện tử như `Shopee`, `Lazada`, `Tiki`, `Sendo`, ... đã trở thành kênh mua sắm phổ biến tại Việt Nam. Các nền tảng này tạo ra lượng dữ liệu lớn liên quan đến:

- Sản phẩm
- Giá bán
- Số lượng đã bán
- Đánh giá người dùng
- Gian hàng
- Chương trình khuyến mãi

Tuy nhiên, phần lớn dữ liệu này chỉ xuất hiện rời rạc trên từng trang sản phẩm và chưa được khai thác một cách có hệ thống để phục vụ:

- Phân tích xu hướng thị trường
- Phân tích hành vi tiêu dùng
- Đánh giá hiệu quả kinh doanh

Đồ án tập trung vào việc thu thập, phân tích và trực quan hóa dữ liệu bán hàng từ các sàn thương mại điện tử để rút ra những kết luận có ý nghĩa thực tiễn.

### 2.2. Mục tiêu chung của bài lab

- Xây dựng bộ dữ liệu liên quan đến thương mại điện tử có cấu trúc hợp lý, đủ lớn và có ý nghĩa phân tích.
- Rèn luyện kỹ năng thu thập dữ liệu thực tế, phân tích dữ liệu và trình bày kết quả.
- Sử dụng trực quan hóa dữ liệu để khám phá mối quan hệ giữa các yếu tố.

## 3. Nhiệm vụ đồ án

### 3.1. Xác định mục tiêu phân tích

- Nhóm cần xác định một bài toán phân tích chung xuyên suốt toàn bộ bài lab, liên quan đến hoạt động bán hàng trên sàn thương mại điện tử.
- Từ bài toán chung, mỗi thành viên đề xuất các hướng phân tích riêng để làm rõ hoặc giải quyết bài toán đó.
- Mỗi thành viên cần xác định ít nhất `2` mục tiêu phân tích.
- Các mục tiêu phân tích cần tuân theo nguyên tắc `SMART`:
  - `Specific`
  - `Measurable`
  - `Achievable`
  - `Relevant`
  - `Time-bound`

Ví dụ:

> Phân tích hành vi mua hàng của khách online trong 6 tháng gần nhất để xác định 3 yếu tố chính làm tăng tỷ lệ mua lại thêm 5% trước cuối quý 2.

### 3.2. Thu thập, xây dựng và tiền xử lý dữ liệu

- Nhóm chọn một hoặc nhiều sàn thương mại điện tử để thu thập dữ liệu bán hàng.
- Có thể sử dụng các phương pháp như:
  - `Web crawling`
  - `API` (nếu có)
- Dữ liệu thu thập cần phản ánh đầy đủ các thông tin liên quan đến bài toán phân tích.
- Cần thiết kế và xây dựng `database/dataset` có cấu trúc hợp lý, thể hiện rõ quan hệ giữa các thực thể như:
  - Sản phẩm
  - Gian hàng
  - Danh mục
  - Đánh giá
- Thực hiện tiền xử lý dữ liệu, kiểm tra tính nhất quán và hợp lệ của dữ liệu.
- Quy trình thu thập và xử lý dữ liệu phải được mô tả trong:
  - Báo cáo
  - `Jupyter Notebook` (nếu có)

### 3.3. Phân tích dữ liệu

Nhóm cần thực hiện phân tích dữ liệu thông qua trực quan hóa, bao gồm:

- Phân tích tổng quan dữ liệu:
  - Kích thước mẫu
  - Cấu trúc dữ liệu
  - Phân bố các biến
- Lựa chọn các trường dữ liệu phù hợp cho từng mục tiêu phân tích.
- Chọn loại biểu đồ phù hợp với bản chất dữ liệu và mục tiêu phân tích.
- Mỗi biểu đồ cần có:
  - Tiêu đề
  - Nhãn trục
  - Chú thích rõ ràng
- Cần sử dụng đa dạng các loại biểu đồ đã được học.
- Mọi nhận xét và kết luận phải được rút ra trực tiếp từ dữ liệu hoặc biểu đồ.

Nhóm có thể áp dụng thêm một hoặc nhiều mô hình `Machine Learning` nếu phù hợp:

- Không yêu cầu tối ưu mô hình phức tạp.
- Tập trung vào ý nghĩa phân tích và cách trình bày kết quả.
- Kết quả mô hình phải được giải thích rõ ràng.
- Kết quả nên được thể hiện hoặc hỗ trợ bằng trực quan hóa.

### 3.4. Lưu ý quan trọng khi phân tích

- Phải sử dụng đúng và hợp lý các loại biểu đồ tương ứng với bản chất dữ liệu và mục tiêu phân tích.
- Mọi nhận xét, kết luận phải phản ánh đúng xu hướng, phân bố, sự khác biệt hoặc mối quan hệ thể hiện trên dữ liệu.
- Không chấp nhận:
  - Giả định không có căn cứ
  - Suy đoán không được chứng minh bằng dữ liệu
  - Nhận xét cảm tính
  - Kết luận dựa trên kiến thức ngoài dữ liệu nhưng không được biểu đồ hoặc dữ liệu hỗ trợ

## 4. Yêu cầu đồ án

- Có thể sử dụng các công cụ như `Python`, `Tableau`, `Power BI`, ... để thực hiện bài lab.
- Tất cả thư viện và công cụ sử dụng cần được ghi rõ trong báo cáo.
- Không được sử dụng dữ liệu có sẵn từ `Kaggle` hoặc các nguồn tương tự.
- Dữ liệu phải do nhóm tự thu thập bằng các phương pháp như `web crawling`, `API`, ...
- Code thu thập dữ liệu bắt buộc phải có trong file `Python` hoặc `Jupyter Notebook`.
- Trong quá trình phân tích có thể sử dụng dữ liệu của nhóm khác, nhưng phải ghi rõ lý do trong:
  - Báo cáo
  - Phần code
- Nếu lý do sử dụng dữ liệu của nhóm khác phù hợp, nhóm có thể được cộng điểm; ngược lại có thể bị trừ điểm tùy mức độ.

## 5. Yêu cầu báo cáo

Báo cáo cần trình bày ngắn gọn, rõ ràng toàn bộ quá trình thực hiện. Độ dài tối đa là `24` trang, không tính:

- Trang bìa
- Mục lục
- Tài liệu tham khảo

Nội dung báo cáo cần bao gồm:

1. Thông tin nhóm `xx`: `STT`, `MSSV`, họ tên, tỷ lệ đóng góp.
2. Giới thiệu bài toán phân tích chung và mục tiêu phân tích của từng thành viên.
3. Mô tả quy trình thu thập, xây dựng và tiền xử lý dữ liệu.
4. Phân tích dữ liệu:
   - Công cụ sử dụng
   - Quy trình thực hiện
   - Tiền xử lý dữ liệu
   - Kết quả phân tích
   - Bảng biểu và hình minh họa
   - Nhận xét và kết luận
   - Tổng kết kết quả của bài toán lớn
5. Tài liệu tham khảo

## 6. Quy định nộp bài

- Nhóm cử `1` người đại diện nộp bài.
- Trước khi nộp, cần chạy lại các cell.
- Không cần chạy lại code thu thập dữ liệu.
- Không được xóa output của các cell, để đảm bảo biểu đồ đúng như trong báo cáo.

Bài nộp là một file nén tên theo mẫu `[Nhom_xx].zip`, bao gồm:

1. Thư mục chứa dữ liệu hoặc link đến dữ liệu.
2. File code hoặc file chứa dashboard.
3. File báo cáo: `[Nhom_xx].pdf`.

Nếu dữ liệu quá nặng:

- Có thể tải dữ liệu lên server ngoài như `Google Drive`, `Kaggle`, ...
- Nộp link dữ liệu thay cho file dữ liệu.
- Link phải được giữ ở trạng thái public ít nhất `2 năm`.
- File code và báo cáo vẫn phải nộp trên `Moodle`.

## 7. Tiêu chí đánh giá

| Tiêu chí | Điểm |
| --- | ---: |
| Xác định bài toán phân tích chung và mục tiêu phân tích của từng thành viên | 2.0 |
| Thu thập, xây dựng và tiền xử lý dữ liệu | 2.0 |
| Trực quan hóa và phân tích dữ liệu | 5.0 |
| Trình bày bài báo cáo | 1.0 |
| **Tổng điểm cơ bản** | **10.0** |
| Điểm cộng: Ứng dụng Machine Learning trong phân tích (không bắt buộc) | +1 |

## 8. Liên hệ

Mọi thắc mắc trong quá trình thực hiện, vui lòng gửi email về:

- `vntan.work@gmail.com`
