# Football Dataset Phù Hợp Với Yêu Cầu Lab 03 Như Thế Nào

## 1. Kết luận ngắn gọn

Football dataset đã được điều chỉnh để phù hợp hơn với yêu cầu của Lab 03 cho phần:

- `Tìm hiểu công cụ Power BI`
- `Minh họa các chức năng và tính năng cơ bản`

Football dataset không dùng cho phần phân tích chính của đồ án. Dataset chính vẫn là:

- Olist Brazilian E-Commerce Dataset

## 2. Vì sao cần điều chỉnh

Trong đề bài, phần giới thiệu Power BI yêu cầu:

- Minh họa các chức năng của Power BI
- Dùng `dataset mẫu` hoặc `dataset đơn giản`
- Dataset này `không liên quan đến dataset chính`

Nếu dùng nguyên full football database:

- Vẫn đúng về mặt dữ liệu
- Nhưng hơi nặng cho phần giới thiệu công cụ
- Khó chụp hình và trình bày gọn trong báo cáo

Vì vậy, football dataset đã được chuyển thành một sample relational dataset gọn hơn, để dùng đúng mục đích của phần này.

## 3. Phiên bản football nên dùng cho báo cáo

Nên dùng bộ dữ liệu sau:

- `lab3/football/demo_processed`

Không nên dùng full processed cho phần giới thiệu, trừ khi nhóm cần bổ sung ví dụ.

## 4. Football demo dataset đã được đơn giản hóa như thế nào

Bộ demo chỉ giữ:

- 2 giải đấu:
  - `England Premier League`
  - `Spain LIGA BBVA`
- 2 mùa giải:
  - `2014/2015`
  - `2015/2016`

Kết quả sau khi rút gọn:

- `dim_country_demo`: 2 dòng
- `dim_league_demo`: 2 dòng
- `dim_team_demo`: 46 dòng
- `dim_date_demo`: 297 dòng
- `team_attributes_demo`: 46 dòng
- `fact_match_demo`: 1,520 dòng
- `fact_team_match_demo`: 3,040 dòng

Đây là kích thước rất hợp lý cho:

- Import nhanh
- Dễ thao tác Power Query
- Dễ quan sát relationship
- Dễ tạo visual mẫu
- Dễ chụp hình minh họa trong báo cáo

## 5. Football demo dataset đáp ứng yêu cầu nào trong đề

### 5.1 Đáp ứng yêu cầu "dataset mẫu hoặc dataset đơn giản"

Bộ `demo_processed` đã được rút gọn có chủ ý, nên:

- Đơn giản hơn bản full
- Vẫn đủ lớn để tạo visual
- Không quá nặng khi demo Power BI

Vì vậy nó phù hợp hơn với tinh thần:

- `dataset mẫu`
- `dataset đơn giản`

### 5.2 Đáp ứng yêu cầu "không liên quan đến dataset chính"

Dataset chính của nhóm là:

- Olist Brazilian E-Commerce

Football là chủ đề hoàn toàn khác:

- Thể thao
- Bóng đá châu Âu

Như vậy football dataset không liên quan đến dataset chính, đúng yêu cầu đề bài.

### 5.3 Đáp ứng yêu cầu minh họa các chức năng của Power BI

Football demo dataset có thể minh họa đầy đủ:

- `Import data`
- `Data transformation (Power Query)`
- `Data modeling`
- `Visualization`
- `Filter`
- `Slicer`

### 5.4 Đáp ứng yêu cầu dữ liệu quan hệ

Bộ football demo vẫn là relational dataset vì có nhiều bảng liên kết với nhau:

- `dim_country_demo`
- `dim_league_demo`
- `dim_team_demo`
- `dim_date_demo`
- `team_attributes_demo`
- `fact_match_demo`
- `fact_team_match_demo`

## 6. Relationship để chứng minh tính quan hệ

Để chứng minh football demo là bộ dữ liệu quan hệ, nhóm có thể trình bày model như sau:

1. `dim_country_demo[country_key]` -> `dim_league_demo[country_key]`
2. `dim_league_demo[league_key]` -> `fact_match_demo[league_key]`
3. `dim_league_demo[league_key]` -> `fact_team_match_demo[league_key]`
4. `dim_team_demo[team_key]` -> `team_attributes_demo[team_key]`
5. `dim_team_demo[team_key]` -> `fact_team_match_demo[team_key]`
6. `dim_date_demo[date_key]` -> `fact_match_demo[match_date_key]`
7. `dim_date_demo[date_key]` -> `fact_team_match_demo[match_date_key]`

Điều này cho thấy:

- One-to-many
- Nhiều bảng có liên kết rõ ràng
- Đủ để demo phần `data modeling`

## 7. Cách football demo phục vụ từng mục trong phần Power BI

### Import dữ liệu

Import các bảng:

- `dim_country_demo.csv`
- `dim_league_demo.csv`
- `dim_team_demo.csv`
- `dim_date_demo.csv`
- `fact_match_demo.csv`
- `fact_team_match_demo.csv`

Nếu cần thêm ví dụ về thuộc tính đội bóng:

- `team_attributes_demo.csv`

### Data transformation

Có thể demo:

- đổi kiểu dữ liệu
- đổi tên cột
- tạo cột `Goal Band`
- tách cột `season`
- lọc theo league hoặc season

### Data modeling

Có thể vào `Model view` và tạo các relationship ở mục 6.

### Visualization

Có thể tạo nhanh:

- Bar chart
- Line chart
- Pie chart
- Table
- Matrix
- Scatter plot

### Filter và slicer

Có thể tạo slicer theo:

- `country_name`
- `league_name`
- `season`
- `team_name`

## 8. Vì sao bộ demo này tốt hơn cho phần giới thiệu công cụ

So với bộ full football:

- Nhẹ hơn
- Dễ import hơn
- Dễ trình bày hơn
- Ít bảng hơn
- Dễ chụp hình minh họa hơn
- Ít gây rối cho người đọc báo cáo hơn

Nó giúp nhóm nhấn mạnh đúng điều cần nói:

- cách sử dụng Power BI

Thay vì:

- đi quá sâu vào phân tích thể thao

## 9. Cách viết vào báo cáo

Nhóm có thể viết ngắn gọn như sau:

`Để minh họa các chức năng cơ bản của Power BI, nhóm sử dụng một sample relational dataset được trích xuất từ European Soccer Database. Để phù hợp với mục đích giới thiệu công cụ, nhóm rút gọn dữ liệu thành 2 giải đấu và 2 mùa giải tiêu biểu, đồng thời giữ cấu trúc nhiều bảng liên kết gồm country, league, team, date và match. Bộ dữ liệu này được dùng để minh họa quá trình import dữ liệu, biến đổi dữ liệu bằng Power Query, xây dựng data model, tạo visual và sử dụng slicer/filter.`

## 10. Files nên dùng từ football

### Nên dùng trong báo cáo

- `FOOTBALL_POWERBI_FEATURES_GUIDE.md`
- `lab3/football/demo_processed`

### Dùng để tham chiếu kỹ thuật

- `lab3/football/processed`
- `lab3/football/raw/database.sqlite`

## 11. Khuyến nghị cuối cùng

Để đúng nhất với đề bài:

- dùng `football/demo_processed` cho phần `Tìm hiểu công cụ Power BI`
- dùng `Olist` cho phần phân tích chính, dashboard và insight

Đó là cách tách vai trò dataset rõ ràng, dễ giải thích, và an toàn nhất khi nộp báo cáo.
