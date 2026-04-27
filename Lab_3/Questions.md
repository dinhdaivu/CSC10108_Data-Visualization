# Phân tích Dữ liệu Thương mại Điện tử

---

## Chủ đề 1: Phân tích Doanh thu và Tăng trưởng (Revenue & Growth)

### Mục tiêu 1

Tổng doanh thu và số lượng đơn hàng thực tế được phân tích để đánh giá sự biến động theo thời gian, bao gồm các chu kỳ tháng, quý và năm nhằm xác định xu hướng tăng trưởng hoặc suy giảm trong từng giai đoạn.

**Bảng sử dụng:**

- `olist_orders_dataset`
  - `order_id`: Đếm số lượng đơn hàng
  - `order_purchase_timestamp`: Trích xuất Tháng / Quý / Năm (X-axis)
- `olist_order_payments_dataset`
  - `payment_value`: Tổng doanh thu

### Mục tiêu 2

Tỷ lệ tăng trưởng doanh thu theo tháng (Month-over-Month) được xem xét giữa các năm để xác định sự thay đổi theo thời gian, đồng thời đánh giá mức độ ảnh hưởng của yếu tố mùa vụ đến xu hướng tăng trưởng này.

**Bảng sử dụng:**

- `olist_orders_dataset`
  - `order_purchase_timestamp` (theo Tháng/Năm)
  - `payment_value` (Tổng doanh thu)

### Mục tiêu 3

Các ngày lễ hoặc sự kiện mua sắm lớn như Black Friday vào tháng 11 được phân tích để xác định mức độ đột biến về khối lượng đơn hàng so với các ngày thông thường, từ đó đánh giá tác động của các sự kiện này đến hành vi mua sắm.

**Bảng sử dụng:**

- `olist_orders_dataset`
  - `order_purchase_timestamp`: Trích xuất Ngày
- `olist_order_payments_dataset`
  - `payment_value`: Tổng doanh thu theo ngày
  - `order_id`: Tổng số đơn

---

## Chủ đề 2: Phân tích Hành vi và Trải nghiệm Thanh toán (Customer Behavior & Payments)

### Mục tiêu 1

Các hình thức thanh toán như Credit Card, Boleto, Voucher và Debit được phân tích nhằm xác định tỷ trọng của từng phương thức dựa trên tổng giá trị giao dịch, từ đó hiểu rõ hơn về xu hướng lựa chọn thanh toán của khách hàng.

**Bảng sử dụng:**

- `olist_order_payments_dataset`
  - `payment_type`: Loại thanh toán
  - `payment_value`: Tổng giá trị

### Mục tiêu 2

Hành vi trả góp (payment_installments) được phân tích để xác định số kỳ trả góp phổ biến và mối liên hệ giữa số kỳ này với các nhóm giá trị đơn hàng khác nhau, bao gồm mức thấp, trung bình và cao.

**Bảng sử dụng:**

- `olist_order_payments_dataset`
  - `payment_installments`: Số kỳ trả góp
  - `payment_value`: Giá trị đơn hàng

### Mục tiêu 3

Thời điểm khách hàng thực hiện chốt đơn và thanh toán được phân tích theo khung giờ trong ngày như sáng, trưa và tối, đồng thời xem xét theo từng ngày trong tuần nhằm xác định khoảng thời gian có lưu lượng giao dịch cao nhất.

**Bảng sử dụng:**

- `olist_orders_dataset`
  - `order_purchase_timestamp`: Tách Hour & Day of Week
  - `order_id`: Đếm đơn

---

## Chủ đề 3: Phân tích Hiệu suất Kho vận và Vận chuyển (Logistics & Delivery Performance)

### Mục tiêu 1

Tỷ lệ phần trăm các đơn hàng giao đúng hạn và giao trễ hạn được phân tích theo từng năm nhằm đánh giá hiệu suất vận chuyển và xu hướng cải thiện hoặc suy giảm theo thời gian.

**Bảng sử dụng:**

- `olist_orders_dataset`
  - `order_delivered_customer_date`
  - `order_estimated_delivery_date`

### Mục tiêu 2

Thời gian vận chuyển trung bình được so sánh giữa các bang và khu vực địa lý khác nhau tại Brazil nhằm xác định sự chênh lệch trong hiệu quả giao hàng và phát hiện các khu vực có thời gian giao hàng nhanh hoặc chậm hơn.

**Bảng sử dụng:**

- `olist_orders_dataset`
  - `order_purchase_timestamp` & `order_delivered_customer_date`: Tính khoảng thời gian giao hàng (số ngày).
- `olist_customers_dataset`
  - `customer_state` hoặc `customer_city`: Xem sự chênh lệch thời gian giao theo từng bang/thành phố của khách.

### Mục tiêu 3

Phí vận chuyển (freight_value) được phân tích để xác định tỷ trọng của nó trong tổng chi phí mà khách hàng phải trả, đồng thời xem xét sự thay đổi của chi phí này theo khoảng cách địa lý giữa nơi bán và nơi giao hàng.

**Bảng sử dụng:**

- `olist_order_items_dataset`:
  - `freight_value`: Phí vận chuyển.

  - `price`: Giá sản phẩm. (Tỷ trọng = freight_value / (price + freight_value))

- `olist_customers_dataset` & `olist_sellers_dataset`:
  - `customer_state` và `seller_state`: Để xem phí vận chuyển thay đổi thế nào khi giao nội bang (cùng state) vs. khác bang.

---

## Chủ đề 4: Phân tích Danh mục Sản phẩm (Product Performance)

### Mục tiêu 1

Các danh mục sản phẩm được phân tích nhằm xác định top 10 danh mục mang lại tổng doanh thu cao nhất và top 10 danh mục có số lượng bán ra nhiều nhất, từ đó đánh giá hiệu suất kinh doanh của từng nhóm sản phẩm.

**Bảng sử dụng**

- `olist_order_items_dataset`:
  - `price`: Tính tổng (Sum) để ra doanh thu.

  - `order_item_id`: Đếm số dòng để lấy số lượng bán ra.

- `olist_products_dataset`:
  - `product_category_name`: Tên danh mục sản phẩm.

- `product_category_name_translation` (Nên dùng để chuyển tên danh mục từ tiếng Bồ Đào Nha sang tiếng Anh).

### Mục tiêu 2

Tổng doanh thu toàn sàn được phân tích theo 3 phân khúc giá sản phẩm (Bình dân, Trung cấp, Cao cấp) nhằm xác định Olist là một nền tảng bán lẻ tập trung vào số lượng lớn hàng giá rẻ hay sống dựa vào biên lợi nhuận của các mặt hàng đắt tiền.

**Bảng sử dụng**

- `olist_order_items_dataset`:
  - Cột tự tạo: `Price Tier` (Phân loại giá: Low < 50, Medium 50-150, Premium > 150).

  - `price`: Tính tổng (Sum) để ra doanh thu.

### Mục tiêu 3

Các đơn hàng bị hủy hoặc không giao thành công được phân tích nhằm xác định đặc điểm chung của các nhóm sản phẩm này, bao gồm loại sản phẩm, giá trị đơn hàng và khu vực giao hàng.

**Bảng sử dụng**

- `olist_orders_dataset`:
  - `order_status`: Lọc riêng các trạng thái canceled hoặc unavailable.

- Các bảng liên quan: `product_category_name` (Sản phẩm nào hay bị hủy?), `customer_state` (Khu vực nào hay bị hủy?).

---

## Chủ đề 5: Đánh giá Mức độ Hài lòng của Khách hàng (Customer Satisfaction)

### Mục tiêu 1

Mối liên hệ giữa thời gian giao hàng thực tế và điểm đánh giá (review score) của khách hàng được phân tích, đặc biệt tập trung vào các trường hợp giao hàng trễ để đánh giá tác động đến sự hài lòng.

**Bảng sử dụng**

- `olist_orders_dataset`:
  - Cột trạng thái "Đúng hạn/Trễ hạn" (đã tạo ở Chủ đề 3).

- `olist_order_reviews_dataset`:
  - `review_score`: Xem điểm số trung bình (Average) giữa nhóm giao đúng hạn và giao trễ.

### Mục tiêu 2

Các danh mục sản phẩm có xu hướng nhận nhiều đánh giá 1 sao được xác định và phân tích nguyên nhân, bao gồm khả năng đến từ chất lượng sản phẩm hoặc trải nghiệm vận chuyển không tốt.

**Bảng sử dụng**:

- `olist_order_reviews_dataset`:
  - `review_score`: Lọc điểm bằng 1.

- `olist_products_dataset`: `product_category_name`.

- Kết hợp Bảng `olist_orders_dataset`: Kiểm tra các đơn 1 sao này có dính trạng thái "giao trễ hạn" hay không để tìm nguyên nhân.

### Mục tiêu 3

Sự khác biệt trong hành vi để lại bình luận văn bản được phân tích giữa nhóm khách hàng cực kỳ hài lòng (5 sao) và nhóm khách hàng không hài lòng (1–2 sao), nhằm đánh giá mức độ chi tiết và tần suất phản hồi của từng nhóm.

**Bảng sử dụng**

- `olist_order_reviews_dataset`:
  - `review_score` (Nhóm: 5 sao, 1-2 sao).

  - `review_comment_message`: Tạo cột tính toán kiểm tra xem cột này có "Trống" (ISBLANK) hay "Có chữ". Bạn cũng có thể đo độ dài chuỗi (LEN) để xem nhóm nào viết dài hơn.
