# Olist Dataset Guide For Lab 03

## 1. Mục tiêu của bộ dữ liệu này

Bạn đã chọn dataset:

- **Brazilian E-Commerce Public Dataset by Olist**
- Nguồn gốc: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

Mục tiêu của phần chuẩn bị dữ liệu là:

- Tải đầy đủ 9 file gốc từ Kaggle
- Tạo thư mục dữ liệu rõ ràng cho bài lab
- Tiền xử lý dữ liệu thành bộ bảng phù hợp hơn cho Power BI
- Giữ được **mô hình dữ liệu quan hệ** để đáp ứng yêu cầu đề bài

## 2. Cấu trúc thư mục đã tạo

Trong [lab3](/c:/Users/Vu/schoolProject/CSC100800/lab3) hiện có:

- [data/raw](/c:/Users/Vu/schoolProject/CSC100800/lab3/data/raw): chứa dữ liệu gốc tải từ Kaggle
- [data/processed](/c:/Users/Vu/schoolProject/CSC100800/lab3/data/processed): chứa dữ liệu đã làm sạch và chuẩn bị cho Power BI
- [scripts/preprocess_olist_for_powerbi.py](/c:/Users/Vu/schoolProject/CSC100800/lab3/scripts/preprocess_olist_for_powerbi.py): script tiền xử lý chính
- [scripts/run_olist_pipeline.ps1](/c:/Users/Vu/schoolProject/CSC100800/lab3/scripts/run_olist_pipeline.ps1): script chạy lại toàn bộ pipeline

## 3. Dữ liệu gốc đã tải

Thư mục [data/raw](/c:/Users/Vu/schoolProject/CSC100800/lab3/data/raw) chứa 9 file gốc:

- `olist_customers_dataset.csv`
- `olist_geolocation_dataset.csv`
- `olist_order_items_dataset.csv`
- `olist_order_payments_dataset.csv`
- `olist_order_reviews_dataset.csv`
- `olist_orders_dataset.csv`
- `olist_products_dataset.csv`
- `olist_sellers_dataset.csv`
- `product_category_name_translation.csv`

Đây là các file gốc từ Kaggle dùng làm bằng chứng nguồn dữ liệu cho báo cáo.

## 4. Bộ dữ liệu processed đã tạo

Thư mục [data/processed](/c:/Users/Vu/schoolProject/CSC100800/lab3/data/processed) chứa bộ dữ liệu Power BI-ready:

### Bảng dimension

- [dim_customer.csv](/c:/Users/Vu/schoolProject/CSC100800/lab3/data/processed/dim_customer.csv)
- [dim_seller.csv](/c:/Users/Vu/schoolProject/CSC100800/lab3/data/processed/dim_seller.csv)
- [dim_category.csv](/c:/Users/Vu/schoolProject/CSC100800/lab3/data/processed/dim_category.csv)
- [dim_product.csv](/c:/Users/Vu/schoolProject/CSC100800/lab3/data/processed/dim_product.csv)
- [dim_date.csv](/c:/Users/Vu/schoolProject/CSC100800/lab3/data/processed/dim_date.csv)
- [dim_order.csv](/c:/Users/Vu/schoolProject/CSC100800/lab3/data/processed/dim_order.csv)

### Bảng fact

- [fact_order_item.csv](/c:/Users/Vu/schoolProject/CSC100800/lab3/data/processed/fact_order_item.csv)
- [fact_payment.csv](/c:/Users/Vu/schoolProject/CSC100800/lab3/data/processed/fact_payment.csv)
- [fact_review.csv](/c:/Users/Vu/schoolProject/CSC100800/lab3/data/processed/fact_review.csv)

### Bảng metadata hỗ trợ

- [schema_entities.csv](/c:/Users/Vu/schoolProject/CSC100800/lab3/data/processed/schema_entities.csv)
- [schema_relationships.csv](/c:/Users/Vu/schoolProject/CSC100800/lab3/data/processed/schema_relationships.csv)
- [schema_summary.json](/c:/Users/Vu/schoolProject/CSC100800/lab3/data/processed/schema_summary.json)
- [model_summary.csv](/c:/Users/Vu/schoolProject/CSC100800/lab3/data/processed/model_summary.csv)
- [geo_zip_lookup.csv](/c:/Users/Vu/schoolProject/CSC100800/lab3/data/processed/geo_zip_lookup.csv)

## 5. Ý nghĩa của từng bảng

### `dim_customer`

- Một dòng cho mỗi `customer_id`
- Chứa thông tin khách hàng và vị trí địa lý
- Đã nối thêm `lat/lng` theo `zip_code_prefix`

Các cột quan trọng:

- `customer_key`
- `customer_id`
- `customer_unique_id`
- `customer_city`
- `customer_state`
- `customer_geolocation_lat`
- `customer_geolocation_lng`

### `dim_seller`

- Một dòng cho mỗi `seller_id`
- Chứa thông tin người bán và vị trí địa lý

Các cột quan trọng:

- `seller_key`
- `seller_id`
- `seller_city`
- `seller_state`
- `seller_geolocation_lat`
- `seller_geolocation_lng`

### `dim_category`

- Một dòng cho mỗi nhóm sản phẩm
- Có cả tên danh mục tiếng Bồ Đào Nha và tiếng Anh

Các cột quan trọng:

- `category_key`
- `category_name_portuguese`
- `category_name_english`
- `category_name_display`

### `dim_product`

- Một dòng cho mỗi `product_id`
- Chứa thông tin mô tả sản phẩm, kích thước và category

Các cột quan trọng:

- `product_key`
- `product_id`
- `category_key`
- `product_weight_g`
- `product_length_cm`
- `product_height_cm`
- `product_width_cm`
- `product_volume_cm3`

### `dim_date`

- Một dòng cho mỗi ngày trong toàn bộ khoảng dữ liệu
- Dùng làm bảng ngày chính trong Power BI

Các cột quan trọng:

- `date`
- `date_key`
- `year`
- `quarter`
- `month_number`
- `month_name`
- `year_month`
- `day_of_week_name`
- `is_weekend`

### `dim_order`

- Một dòng cho mỗi `order_id`
- Đây là bảng trung tâm rất quan trọng để nối khách hàng với order item, payment và review
- Đã bổ sung các cột tính toán để phân tích nhanh hơn

Các cột quan trọng:

- `order_key`
- `order_id`
- `customer_key`
- `order_status`
- `purchase_date_key`
- `approved_date_key`
- `delivered_customer_date_key`
- `estimated_delivery_date_key`
- `approval_delay_hours`
- `delivery_to_customer_days`
- `is_late_delivery`
- `item_count`
- `items_price_total`
- `freight_total`
- `payment_total_value`
- `average_review_score`

### `fact_order_item`

- Một dòng cho mỗi sản phẩm trong đơn hàng
- Đây là fact table chính cho doanh thu và số lượng dòng hàng

Các cột quan trọng:

- `order_item_key`
- `order_key`
- `product_key`
- `seller_key`
- `shipping_limit_date_key`
- `price`
- `freight_value`
- `item_quantity`
- `item_total_value`

### `fact_payment`

- Một dòng cho mỗi lần thanh toán hoặc mỗi payment sequence của đơn hàng

Các cột quan trọng:

- `payment_key`
- `order_key`
- `payment_type`
- `payment_installments`
- `payment_value`

### `fact_review`

- Một dòng cho mỗi review
- Dùng để phân tích chất lượng dịch vụ và mức độ hài lòng

Các cột quan trọng:

- `review_id`
- `order_key`
- `review_score`
- `review_comment_message`
- `review_comment_length`
- `has_review_comment`
- `review_creation_date_key`

## 6. Tổng quan dữ liệu sau xử lý

Theo [schema_summary.json](/c:/Users/Vu/schoolProject/CSC100800/lab3/data/processed/schema_summary.json):

- `dim_customer`: 99,441 dòng
- `dim_seller`: 3,095 dòng
- `dim_category`: 74 dòng
- `dim_product`: 32,951 dòng
- `dim_date`: 1,314 dòng
- `dim_order`: 99,441 dòng
- `fact_order_item`: 112,650 dòng
- `fact_payment`: 103,886 dòng
- `fact_review`: 99,224 dòng

Khoảng thời gian mua hàng:

- Từ `2016-09-04`
- Đến `2018-10-17`

## 7. Quan hệ dữ liệu khuyến nghị trong Power BI

Tạo các relationship sau:

1. `dim_customer[customer_key]` -> `dim_order[customer_key]`
2. `dim_category[category_key]` -> `dim_product[category_key]`
3. `dim_product[product_key]` -> `fact_order_item[product_key]`
4. `dim_seller[seller_key]` -> `fact_order_item[seller_key]`
5. `dim_order[order_key]` -> `fact_order_item[order_key]`
6. `dim_order[order_key]` -> `fact_payment[order_key]`
7. `dim_order[order_key]` -> `fact_review[order_key]`
8. `dim_date[date_key]` -> `dim_order[purchase_date_key]` as active relationship

Các relationship phụ có thể tạo ở trạng thái inactive:

- `dim_date[date_key]` -> `dim_order[approved_date_key]`
- `dim_date[date_key]` -> `dim_order[delivered_customer_date_key]`
- `dim_date[date_key]` -> `fact_order_item[shipping_limit_date_key]`
- `dim_date[date_key]` -> `fact_review[review_creation_date_key]`

Thiết lập khuyến nghị:

- Cardinality: `One to many`
- Cross filter direction: `Single`
- Dùng `dim_*` làm phía `one`
- Dùng `fact_*` làm phía `many`

## 8. Hướng import vào Power BI

### Cách import

1. Mở Power BI Desktop
2. Chọn `Get Data` -> `Text/CSV`
3. Import toàn bộ các file trong [data/processed](/c:/Users/Vu/schoolProject/CSC100800/lab3/data/processed)
4. Nhấn `Transform Data` để kiểm tra kiểu dữ liệu trước khi load

### Kiểu dữ liệu nên chỉnh

- Các cột `*_key`:
  - Nếu là mã ID dạng chuỗi như `order_key`, `customer_key`, `product_key`, giữ kiểu `Text`
  - Nếu là `date_key`, có thể để `Whole Number`
- Các cột ngày như `purchase_date`, `review_creation_date_only`: `Date`
- Các cột timestamp như `order_purchase_timestamp`: `Date/Time`
- Các cột số tiền như `price`, `freight_value`, `payment_value`: `Decimal Number`
- Các cột cờ như `is_delivered`, `is_late_delivery`, `has_review_comment`: `Whole Number`

### Date table

Sau khi import:

1. Chọn bảng `dim_date`
2. Vào `Table tools`
3. Chọn `Mark as date table`
4. Chọn cột `date`

## 9. Một số measure nên tạo ngay

Bạn có thể tạo các measure DAX cơ bản sau:

```DAX
Total Orders = DISTINCTCOUNT(dim_order[order_id])

Total Customers = DISTINCTCOUNT(dim_customer[customer_id])

Total Sellers = DISTINCTCOUNT(dim_seller[seller_id])

Total Products = DISTINCTCOUNT(dim_product[product_id])

Total Revenue = SUM(fact_order_item[price])

Total Freight = SUM(fact_order_item[freight_value])

Total Order Item Value = SUM(fact_order_item[item_total_value])

Total Payment Value = SUM(fact_payment[payment_value])

Average Review Score = AVERAGE(fact_review[review_score])

Late Delivery Orders =
CALCULATE(
    COUNTROWS(dim_order),
    dim_order[is_late_delivery] = 1
)

Delivered Orders =
CALCULATE(
    COUNTROWS(dim_order),
    dim_order[is_delivered] = 1
)
```

## 10. Một số câu hỏi phân tích phù hợp với bộ dữ liệu này

Bạn có thể phát triển câu hỏi theo các nhóm sau:

### Doanh thu và đơn hàng

- Doanh thu biến động như thế nào theo thời gian?
- Tháng nào có số lượng đơn hàng cao nhất?
- Danh mục nào tạo ra doanh thu cao nhất?

### Khách hàng

- Khách hàng tập trung nhiều ở bang nào?
- Bang nào có giá trị đơn hàng trung bình cao hơn?
- Có sự khác biệt nào giữa số lượng khách hàng và doanh thu theo khu vực?

### Người bán

- Seller nào có doanh thu cao nhất?
- Seller nào có nhiều đơn hàng nhất?
- Seller ở bang nào có hiệu suất tốt hơn?

### Giao hàng

- Tỷ lệ giao trễ là bao nhiêu?
- Bang nào có thời gian giao hàng lâu nhất?
- Giao trễ có liên quan đến điểm review thấp hay không?

### Review và chất lượng dịch vụ

- Điểm review trung bình theo danh mục sản phẩm là bao nhiêu?
- Những danh mục nào có nhiều bình luận tiêu cực hơn?
- Đơn hàng giao trễ có review thấp hơn hay không?

### Thanh toán

- Phương thức thanh toán nào phổ biến nhất?
- Khách hàng thường trả góp bao nhiêu kỳ?
- Payment type nào gắn với đơn hàng giá trị cao hơn?

## 11. Một storyboard dashboard gợi ý

Bạn có thể thiết kế 3 trang dashboard như sau:

### Page 1: Executive Overview

- KPI Cards:
  - Total Orders
  - Total Revenue
  - Total Customers
  - Average Review Score
- Line chart: doanh thu theo tháng
- Bar chart: top category theo doanh thu
- Map: phân bố khách hàng theo bang
- Slicer:
  - năm
  - bang
  - category

### Page 2: Logistics and Service Quality

- Bar chart: tỷ lệ giao trễ theo bang
- Line chart: thời gian giao hàng trung bình theo tháng
- Scatter plot: delivery days vs review score
- Matrix: category x average review score

### Page 3: Sellers and Payments

- Bar chart: top sellers theo doanh thu
- Donut/Pie chart: payment type distribution
- Column chart: doanh thu theo số kỳ trả góp
- Table: seller, orders, revenue, average review

## 12. Cách chạy lại toàn bộ pipeline

Nếu muốn chạy lại toàn bộ quá trình:

```powershell
powershell -ExecutionPolicy Bypass -File "c:\Users\Vu\schoolProject\CSC100800\lab3\scripts\run_olist_pipeline.ps1"
```

Script này sẽ:

1. Tải lại dataset từ Kaggle vào `data/raw`
2. Chạy preprocessing
3. Sinh lại toàn bộ file trong `data/processed`

## 13. Lưu ý khi viết báo cáo

Trong báo cáo, bạn nên mô tả rõ:

- Dataset gốc gồm nhiều bảng dữ liệu quan hệ
- Các khóa chính và khóa ngoại dùng trong Power BI
- Vì sao nhóm tách dữ liệu thành dimension và fact table
- Các bước tiền xử lý đã thực hiện:
  - Chuẩn hóa kiểu ngày
  - Tạo `date_key`
  - Tạo khóa thay thế như `order_key`, `product_key`, `seller_key`
  - Tạo cột dẫn xuất như `delivery_to_customer_days`, `is_late_delivery`, `item_total_value`
  - Bổ sung thông tin địa lý theo `zip_code_prefix`

## 14. Tóm tắt nhanh

Bạn đã có sẵn:

- Dữ liệu gốc từ Kaggle
- Bộ dữ liệu processed để import ngay vào Power BI
- Script tiền xử lý
- Script chạy lại toàn bộ pipeline
- Metadata mô tả quan hệ và số dòng

Nếu muốn, bước tiếp theo mình có thể làm luôn cho bạn:

- tạo `AnalysisQuestions.md` với bộ câu hỏi phân tích đủ cho nhóm 3-5 người
- tạo `ReportTemplate.md` đúng cấu trúc báo cáo môn học
- tạo `DAXMeasures.md` với bộ measure hoàn chỉnh cho dashboard
