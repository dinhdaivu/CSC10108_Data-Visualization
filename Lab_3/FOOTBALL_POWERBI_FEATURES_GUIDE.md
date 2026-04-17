# Hướng Dẫn Sử Dụng Football Dataset Để Minh Họa Power BI

## 1. Mục đích của football dataset trong Lab 03

Football dataset này không phải là dataset chính cho phần dashboard và phân tích cuối cùng. Nhóm sẽ dùng nó để:

- Giới thiệu tổng quan về Power BI
- Minh họa các chức năng cơ bản của Power BI
- Trình bày nhanh quy trình:
  - Import dữ liệu
  - Data transformation với Power Query
  - Data modeling
  - Tạo biểu đồ
  - Filter và slicer

Dataset chính cho phần phân tích và dashboard vẫn là:

- Olist Brazilian E-Commerce Dataset

Để phù hợp hơn với yêu cầu đề bài, football dataset nên được dùng dưới dạng sample dataset đã rút gọn, thay vì dùng toàn bộ dữ liệu gốc.

## 2. Nguồn dataset

- Tên dataset: European Soccer Database
- Nguồn: Kaggle
- Link nguồn: `https://www.kaggle.com/datasets/hugomathien/soccer`

Trong workspace, dataset đã được tải về và lưu tại:

- Raw database: `lab3/football/raw/database.sqlite`
- Processed tables: `lab3/football/processed`
- Recommended sample dataset: `lab3/football/demo_processed`

## 3. Các file đã được chuẩn bị

### Raw

- `database.sqlite`

Đây là database gốc của dataset.

### Processed

Bộ bảng đã được trích xuất và tiền xử lý để dễ import vào Power BI:

- `dim_country.csv`
- `dim_league.csv`
- `dim_team.csv`
- `dim_player.csv`
- `dim_date.csv`
- `team_attributes_latest.csv`
- `player_attributes_latest.csv`
- `fact_match_summary.csv`
- `fact_team_match.csv`

### Recommended demo subset

Để dùng đúng vai trò dataset mẫu cho phần giới thiệu Power BI, nên ưu tiên bộ:

- `dim_country_demo.csv`
- `dim_league_demo.csv`
- `dim_team_demo.csv`
- `dim_date_demo.csv`
- `team_attributes_demo.csv`
- `fact_match_demo.csv`
- `fact_team_match_demo.csv`

Metadata:

- `schema_entities_demo.csv`
- `schema_relationships_demo.csv`
- `demo_summary.json`

Metadata hỗ trợ cho bộ đầy đủ:

- `schema_entities.csv`
- `schema_relationships.csv`
- `dataset_summary.json`
- `model_summary.csv`

## 4. Tổng quan dữ liệu sau xử lý

Theo `dataset_summary.json`:

- `dim_country`: 11 dòng
- `dim_league`: 11 dòng
- `dim_team`: 299 dòng
- `dim_player`: 11,060 dòng
- `dim_date`: 3,424 dòng
- `team_attributes_latest`: 288 dòng
- `player_attributes_latest`: 11,060 dòng
- `fact_match_summary`: 25,979 dòng
- `fact_team_match`: 51,958 dòng

Khoảng thời gian trận đấu:

- Từ `2008-07-18`
- Đến `2016-05-25`

### Tổng quan bộ demo subset

Bộ demo subset được khuyến nghị cho báo cáo:

- 2 leagues: `England Premier League`, `Spain LIGA BBVA`
- 2 seasons: `2014/2015`, `2015/2016`
- `fact_match_demo`: 1,520 dòng
- `fact_team_match_demo`: 3,040 dòng
- `dim_team_demo`: 46 dòng

Bộ này nhẹ hơn và phù hợp hơn cho phần `Tìm hiểu công cụ Power BI`.

## 5. Ý nghĩa của từng bảng

### `dim_country`

- Một dòng cho mỗi quốc gia
- Dùng để phân loại giải đấu theo quốc gia

Cột quan trọng:

- `country_key`
- `country_name`

### `dim_league`

- Một dòng cho mỗi giải đấu
- Có liên kết đến quốc gia

Cột quan trọng:

- `league_key`
- `country_key`
- `league_name`
- `country_name`

### `dim_team`

- Một dòng cho mỗi đội bóng

Cột quan trọng:

- `team_key`
- `team_long_name`
- `team_short_name`

### `dim_player`

- Một dòng cho mỗi cầu thủ
- Phù hợp để minh họa import và query đơn giản

Cột quan trọng:

- `player_key`
- `player_name`
- `height`
- `weight`

### `dim_date`

- Một dòng cho mỗi ngày trong khoảng dữ liệu
- Dùng để demo Date Table, time intelligence cơ bản và slicer theo thời gian

Cột quan trọng:

- `date`
- `date_key`
- `year`
- `quarter`
- `month_number`
- `month_name`
- `year_month`

### `team_attributes_latest`

- Chỉ giữ dòng mới nhất của mỗi đội bóng
- Phù hợp để demo transformation và visual về sức mạnh đội bóng

Cột quan trọng:

- `team_key`
- `attribute_date`
- `buildUpPlaySpeed`
- `chanceCreationPassing`
- `defencePressure`

### `player_attributes_latest`

- Chỉ giữ dòng mới nhất của mỗi cầu thủ
- Phù hợp để demo histogram, scatter plot, rank, filter

Cột quan trọng:

- `player_key`
- `attribute_date`
- `overall_rating`
- `potential`
- `finishing`
- `short_passing`
- `ball_control`
- `sprint_speed`

### `fact_match_summary`

- Một dòng cho mỗi trận đấu
- Đây là bảng phù hợp nhất để demo visual về match, league, season

Cột quan trọng:

- `match_key`
- `country_key`
- `league_key`
- `season`
- `stage`
- `match_date`
- `home_team_name`
- `away_team_name`
- `home_team_goal`
- `away_team_goal`
- `total_goals`
- `goal_difference`
- `match_result`

### `fact_team_match`

- Một dòng cho mỗi đội bóng trong mỗi trận đấu
- Đã chuyển bảng `Match` sang dạng long table để dễ phân tích theo đội bóng
- Rất tốt để demo data modeling và visual theo team

Cột quan trọng:

- `team_match_key`
- `match_key`
- `match_date`
- `season`
- `league_name`
- `team_name`
- `opponent_team_name`
- `is_home`
- `goals_for`
- `goals_against`
- `goal_difference`
- `match_points`
- `match_result`

## 6. Vì sao bộ bảng này hợp để giới thiệu Power BI

Football dataset rất hợp cho phần giới thiệu Power BI vì:

- Có nhiều bảng liên kết để demo `data modeling`
- Có dữ liệu thời gian để demo `date table`, `line chart`, `slicer`
- Có dữ liệu phân cấp để demo `country -> league -> team`
- Có số liệu số học để demo `bar chart`, `scatter plot`, `table`, `matrix`
- Có thể làm visual để nhìn thấy kết quả ngay, không cần dashboard phức tạp

## 7. Cách dùng dataset này để giới thiệu từng tính năng Power BI

### 7.1 Import dữ liệu

Để demo import, bạn không cần nạp tất cả bảng.

Nên import trước 4 bảng:

- `dim_country_demo.csv`
- `dim_league_demo.csv`
- `dim_team_demo.csv`
- `fact_match_demo.csv`

Nếu muốn demo thêm transformation và visual theo đội bóng, import thêm:

- `fact_team_match_demo.csv`
- `team_attributes_demo.csv`

Nếu muốn demo player-level analysis, dùng bộ đầy đủ:

- `dim_player.csv`
- `player_attributes_latest.csv`

### 7.2 Power Query / Data Transformation

Football dataset rất hợp để minh họa một vài thao tác Power Query ngắn gọn:

1. Đổi kiểu dữ liệu
- `match_date` thành `Date`
- `season` thành `Text`
- `home_team_goal`, `away_team_goal`, `total_goals` thành `Whole Number`

2. Tạo cột mới
- `Total Goals = home_team_goal + away_team_goal`
- `Goal Difference = home_team_goal - away_team_goal`
- `Match Type = if total_goals >= 4 then "High Scoring" else "Normal"`

3. Tách cột `season`
- Tách năm bắt đầu và năm kết thúc từ `2008/2009`

4. Lọc dữ liệu
- Chỉ giữ các giải đấu trong bộ demo

5. Đổi tên cột cho dễ đọc
- Đổi `match_result` thành `Match Result`
- Đổi `goals_for` thành `Goals For`

6. Loại bỏ các cột không cần
- Nếu minh họa nhanh, có thể bỏ các cột kỹ thuật không dùng đến

### 7.3 Data Modeling

Để demo phần data model, bạn nên dùng model sau:

1. `dim_country_demo[country_key]` -> `dim_league_demo[country_key]`
2. `dim_league_demo[league_key]` -> `fact_match_demo[league_key]`
3. `dim_league_demo[league_key]` -> `fact_team_match_demo[league_key]`
4. `dim_team_demo[team_key]` -> `fact_team_match_demo[team_key]`
5. `dim_team_demo[team_key]` -> `team_attributes_demo[team_key]`
6. `dim_date_demo[date_key]` -> `fact_match_demo[match_date_key]`
7. `dim_date_demo[date_key]` -> `fact_team_match_demo[match_date_key]`

Thiết lập khuyến nghị:

- Cardinality: `One to many`
- Cross filter direction: `Single`
- Mark `dim_date_demo` as date table

## 8. Cách import vào Power BI

### Bước 1

Mở Power BI Desktop.

### Bước 2

Chọn `Get Data` -> `Text/CSV`.

### Bước 3

Import các file trong thư mục `lab3/football/demo_processed`.

### Bước 4

Chọn `Transform Data` trước khi load.

### Bước 5

Kiểm tra lại kiểu dữ liệu:

- `country_key`, `league_key`, `team_key`: `Whole Number`
- `match_key`: `Whole Number`
- `date_key`: `Whole Number`
- `match_date`, `attribute_date`: `Date`
- `home_team_goal`, `away_team_goal`, `goals_for`, `goals_against`, `match_points`: `Whole Number`

### Bước 6

Sau khi load, vào `Model view` và tạo relationship theo mục 7.

### Bước 7

Chọn `dim_date_demo` -> `Table tools` -> `Mark as date table` -> chọn cột `date`.

## 9. Các measure DAX gợi ý để demo nhanh

```DAX
Total Matches = DISTINCTCOUNT(fact_match_demo[match_key])

Total Teams = DISTINCTCOUNT(dim_team_demo[team_key])

Total Leagues = DISTINCTCOUNT(dim_league_demo[league_key])

Total Goals = SUM(fact_match_demo[total_goals])

Average Goals Per Match = AVERAGE(fact_match_demo[total_goals])

Home Win Matches =
CALCULATE(
    COUNTROWS(fact_match_demo),
    fact_match_demo[home_win] = 1
)

Draw Matches =
CALCULATE(
    COUNTROWS(fact_match_demo),
    fact_match_demo[is_draw] = 1
)

Total Team Points = SUM(fact_team_match_demo[match_points])

Average Goal Difference = AVERAGE(fact_team_match_demo[goal_difference])
```

## 10. Các visual để minh họa trong phần giới thiệu Power BI

Vì đây chỉ là phần giới thiệu công cụ, bạn nên làm ít visual nhưng dễ nhìn:

### Visual 1: Bar chart

- Mục tiêu: So sánh số trận đấu theo giải
- Axis: `league_name`
- Value: `Total Matches`

### Visual 2: Line chart

- Mục tiêu: Tổng số bàn thắng theo thời gian
- Axis: `dim_date_demo[year_month]`
- Value: `Total Goals`

### Visual 3: Pie chart hoặc donut chart

- Mục tiêu: Tỷ lệ kết quả trận đấu
- Legend: `match_result`
- Value: `Total Matches`

### Visual 4: Table hoặc matrix

- Mục tiêu: So sánh đội bóng theo tổng điểm
- Rows: `team_name`
- Values:
  - `Total Team Points`
  - `Average Goal Difference`

### Visual 5: Scatter plot

- Mục tiêu: Tương quan giữa chỉ số đội bóng và kết quả
- X-axis: một chỉ số trong `team_attributes_demo`
- Y-axis: `Total Team Points`
- Details: `team_name`

## 11. Cách minh họa filter và slicer

Football dataset rất dễ demo `Filter` và `Slicer`.

Nên tạo các slicer sau:

- `country_name`
- `league_name`
- `season`
- `team_name`

Sau đó chụp màn hình trước và sau khi chọn slicer để minh họa tính tương tác của Power BI.

## 12. Một luồng demo ngắn gọn để đưa vào báo cáo

Bạn có thể trình bày phần tìm hiểu Power BI theo luồng sau:

1. Import 4 bảng cơ bản: country, league, team, fact_match
2. Vào Power Query và đổi kiểu dữ liệu
3. Tạo thêm 1-2 cột mới như `Total Goals`, `Goal Difference`
4. Sang Model view và tạo relationship
5. Tạo 3-5 visual cơ bản
6. Thêm 2 slicer: `league_name`, `season`
7. Minh họa khi thay đổi slicer, biểu đồ thay đổi theo

Luồng này gọn, dễ chụp hình, và rất hợp cho mục `Tìm hiểu công cụ Power BI`.

## 13. Cách viết vào báo cáo

Trong báo cáo, bạn có thể viết theo ý sau:

- Football dataset được dùng để minh họa các chức năng cơ bản của Power BI
- Dataset gồm nhiều bảng liên kết như Country, League, Team, Match
- Nhóm đã trích xuất và chuẩn hóa thành các bảng dễ nhập vào Power BI
- Nhóm đã thực hiện:
  - Import dữ liệu
  - Xử lý dữ liệu trong Power Query
  - Tạo model dữ liệu
  - Tạo visual cơ bản
  - Sử dụng slicer và filter

Không nên đi quá sâu vào insight ở phần này vì đây chỉ là phần giới thiệu công cụ.

## 14. Cách chạy lại pipeline football

Nếu cần tải lại và tiền xử lý lại dataset:

```powershell
powershell -ExecutionPolicy Bypass -File "c:\Users\Vu\schoolProject\CSC100800\lab3\scripts\run_football_pipeline.ps1"
```

Nếu cần tạo lại bộ demo subset:

```powershell
C:\Users\Vu\AppData\Local\Python\bin\python.exe "c:\Users\Vu\schoolProject\CSC100800\lab3\scripts\build_football_demo_subset.py"
```

## 15. Tóm tắt để dùng nhanh

Nếu muốn làm nhanh phần giới thiệu Power BI, chỉ cần dùng:

- `dim_country_demo.csv`
- `dim_league_demo.csv`
- `dim_team_demo.csv`
- `dim_date_demo.csv`
- `fact_match_demo.csv`
- `fact_team_match_demo.csv`
- `team_attributes_demo.csv`

## 16. Bước tiếp theo hợp lý

Football dataset đã sẵn sàng cho phần giới thiệu Power BI.

Bước tiếp theo hợp lý nhất là:

- dùng football cho phần `Tìm hiểu công cụ Power BI`
- dùng Olist cho phần phân tích chính, dashboard và insight

Nếu muốn, mình có thể làm tiếp ngay:

- `Football_Demo_Slides_Content.md` để bạn đưa thẳng vào báo cáo
- `PowerBI_Features_Writeup.md` viết sẵn nội dung mô tả chức năng Power BI
- `Olist_AnalysisQuestions.md` để chuẩn bị phần phân tích chính
