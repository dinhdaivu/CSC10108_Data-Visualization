# Power BI Dashboard Blueprint

Use this as your Power BI setup guide for every table in `powerbi_data`.

## Dashboard framing

Recommended report title:
- **Global AI & Data Science Job Market Dashboard (2020-2026)**

Recommended subtitle:
- **Role demand, salary patterns, skills, geography, and hiring structure from a synthetic multi-country job market dataset**

Important caution:
- This dataset is clean and highly usable for Power BI, but it appears strongly synthetic.
- Present insights as market-pattern analysis, not proof of real-world labor market behavior.
- Keep wording analytical: compare, correlate, trend, share.

## Global setup

For all tables:
- Text columns: set to `Text`
- Year columns: set to `Whole number`
- Count columns: set to `Whole number`
- Salary fields: set to `Decimal number` or `Fixed decimal number`, then format as `Currency` in USD
- Percentage fields: set to `Decimal number`, then format as `%` only if values are `0-1`; if values are already `32.1`, `35.5`, keep them as decimal and show `%` in label or custom formatting
- Avoid converting `posted_year` into `Date`, because your dataset only has year

Recommended theme direction:
- Background: white or very light gray
- Primary color: deep navy `#16324F`
- Secondary color: teal `#2A9D8F`
- Accent color: warm gold `#E9C46A`
- Alert/highlight color: coral `#E76F51`
- Neutral text: charcoal `#2B2D42`

Recommended color usage:
- Volume and counts: navy
- Salary metrics: teal
- Growth and opportunity: gold
- Risk, low scores, or caution: coral
- Keep the same meaning for colors across all pages

Recommended canvas layout:
- Top row: page title, subtitle, and slicers
- Second row: 3 KPI cards
- Lower area: 2 main visuals side by side
- Bottom area: 1 supporting table or matrix

Recommended global slicers:
- `country`
- `posted_year`
- `job_title`
- `experience_level`
- `industry`

## Data type guide by table

### Q1 - `Q1_entry_level_jobs_by_role.csv`
- `job_title`: Text
- `country`: Text
- `posted_year`: Whole number
- `job_count`: Whole number
- `avg_salary_usd`: Decimal / Currency
- `min_salary_usd`: Decimal / Currency
- `max_salary_usd`: Decimal / Currency

### Q6 - `Q6_senior_salary_ceiling_by_industry.csv`
- `industry`: Text
- `country`: Text
- `avg_max_salary_usd`: Decimal / Currency
- `avg_salary_usd`: Decimal / Currency
- `avg_min_salary_usd`: Decimal / Currency
- `job_count`: Whole number

### Q11 - `Q11_salary_city_vs_remote.csv`
- `location_group`: Text
- `job_title`: Text
- `experience_level`: Text
- `avg_salary_usd`: Decimal / Currency
- `min_salary_usd`: Decimal / Currency
- `max_salary_usd`: Decimal / Currency
- `job_count`: Whole number

### Q13 - `Q13_analytics_vs_engineering_entry.csv`
- `role_category`: Text
- `job_title`: Text
- `country`: Text
- `avg_salary_usd`: Decimal / Currency
- `min_salary_usd`: Decimal / Currency
- `max_salary_usd`: Decimal / Currency
- `job_count`: Whole number

### Q14 - `Q14_cloud_skill_salary_premium.csv`
- `has_advanced_cloud`: Text
- `experience_level`: Text
- `job_title`: Text
- `avg_salary_usd`: Decimal / Currency
- `max_salary_usd`: Decimal / Currency
- `job_count`: Whole number

### Q16 - `Q16_hiring_trend_by_year.csv`
- `posted_year`: Whole number
- `country`: Text
- `experience_level`: Text
- `total_jobs`: Whole number
- `avg_salary_usd`: Decimal / Currency
- `year_total`: Whole number
- `yoy_growth_pct`: Decimal number

### Q18 - `Q18_undersupplied_skills.csv`
- `skill`: Text
- `skill_category`: Text
- `advanced_demand_count`: Whole number
- `total_demand_count`: Whole number
- `advanced_demand_pct`: Decimal number

### Q19 - `Q19_mid_vs_2_juniors.csv`
- `job_title`: Text
- `country`: Text
- `entry_avg_salary_usd`: Decimal / Currency
- `mid_avg_salary_usd`: Decimal / Currency
- `cost_2_juniors_usd`: Decimal / Currency
- `mid_to_entry_ratio`: Decimal number
- `cost_verdict`: Text

### Q21 - `Q21_opportunity_by_country.csv`
- `country`: Text
- `posted_year`: Whole number
- `total_jobs`: Whole number
- `avg_salary_usd`: Decimal / Currency
- `avg_max_salary`: Decimal / Currency
- `remote_pct`: Decimal number
- `opportunity_score`: Decimal number

### Q25 - `Q25_growth_by_company_size.csv`
- `company_size`: Text
- `posted_year`: Whole number
- `country`: Text
- `total_jobs`: Whole number
- `avg_salary_usd`: Decimal / Currency
- `yoy_growth_pct`: Decimal number

### ZZ - `ZZ_reference_values.csv`
- `value`: Text
- `category`: Text

Use `ZZ_reference_values.csv` as a helper table only, not as a main fact table.

## Full report blueprint

### Trang 1 - Tổng quan điều hành

Tiêu đề trang:
- **Tổng quan thị trường AI & Khoa học dữ liệu**

Mục đích:
- Tóm tắt nhanh nhu cầu tuyển dụng, mức lương, tỷ lệ remote, và mức độ cơ hội theo quốc gia.

Thông điệp chính của trang:
- Thị trường nhìn chung ổn định giữa các quốc gia, nhưng vẫn có những khác biệt nhỏ nhưng dễ nhận thấy về lương, nhu cầu, và tỷ lệ remote.

Bảng dữ liệu chính:
- `Q21_opportunity_by_country.csv`
- `Q16_hiring_trend_by_year.csv`

Bố trí biểu đồ:
- KPI trên cùng bên trái: giá trị trung bình `opportunity_score`
- KPI trên cùng ở giữa: giá trị trung bình `avg_salary_usd`
- KPI trên cùng bên phải: giá trị trung bình `remote_pct`
- Giữa bên trái: biểu đồ phân tán `total_jobs` vs `avg_salary_usd`
- Giữa bên phải: biểu đồ đường `year_total` theo `posted_year`
- Bên dưới: matrix `country` x `posted_year` dùng `opportunity_score`

Thẻ KPI:
- `Điểm cơ hội trung bình`
- `Lương trung bình (USD)`
- `Tỷ lệ Remote trung bình`

Bộ lọc:
- `country`
- `posted_year`

Sử dụng màu:
- Điểm cơ hội: gradient vàng
- Lương: xanh teal
- Số lượng việc làm: xanh navy

### Trang 2 - Q1 vai trò entry-level

Tiêu đề trang:
- **Vai trò entry-level nào có sự cân bằng tốt nhất giữa nhu cầu và mức lương?**

Mục đích:
- Hỗ trợ so sánh các vai trò entry-level theo mức lương và số lượng việc làm.

Thông điệp chính của trang:
- Các vai trò entry-level khác nhau về nhu cầu và mức lương, và lựa chọn tốt nhất phụ thuộc vào việc ưu tiên số lượng cơ hội hay mức lương.

Bảng dữ liệu chính:
- `Q1_entry_level_jobs_by_role.csv`

Bố trí biểu đồ:
- KPI trên cùng bên trái: tổng `job_count`
- KPI trên cùng ở giữa: giá trị trung bình `avg_salary_usd`
- KPI trên cùng bên phải: vai trò đứng đầu theo `job_count`
- Giữa bên trái: biểu đồ cột cụm `job_count` theo `job_title`
- Giữa bên phải: biểu đồ đường `avg_salary_usd` theo `posted_year`
- Bên dưới: biểu đồ phân tán `job_count` vs `avg_salary_usd`

Thẻ KPI:
- `Tổng việc làm Entry-Level`
- `Lương Entry-Level trung bình`
- `Vai trò có nhu cầu cao nhất`

Bộ lọc:
- `country`
- `posted_year`
- `job_title`

Sử dụng màu:
- Biểu đồ nhu cầu: xanh navy
- Biểu đồ lương: xanh teal
- Nhấn mạnh vai trò top: vàng

### Trang 3 - Q6 trần lương senior theo ngành

Tiêu đề trang:
- **Ngành nào có mức trần lương Senior cao nhất?**

Mục đích:
- So sánh các cơ hội Senior có mức thu nhập cao nhất theo ngành và quốc gia.

Thông điệp chính của trang:
- Trần lương Senior có sự khác biệt giữa các ngành, nhưng chênh lệch khá hẹp và nên được xem là xu hướng tham khảo thay vì kết luận tuyệt đối.

Bảng dữ liệu chính:
- `Q6_senior_salary_ceiling_by_industry.csv`

Bố trí biểu đồ:
- KPI trên cùng bên trái: giá trị lớn nhất `avg_max_salary_usd`
- KPI trên cùng ở giữa: giá trị trung bình `avg_salary_usd`
- KPI trên cùng bên phải: tổng `job_count`
- Giữa bên trái: biểu đồ thanh ngang `avg_max_salary_usd` theo `industry`
- Giữa bên phải: matrix `industry` x `country`
- Bên dưới: bảng gồm `industry`, `country`, và các trường lương

Thẻ KPI:
- `Trần lương Senior cao nhất`
- `Lương Senior trung bình`
- `Số việc làm Senior`

Bộ lọc:
- `country`
- `industry`

Sử dụng màu:
- Trần lương tối đa: vàng
- Lương trung bình: xanh teal
- Số lượng việc làm: xanh navy

### Trang 4 - Q11 hình thức làm việc

Tiêu đề trang:
- **Mức lương thay đổi như thế nào theo hình thức làm việc?**

Mục đích:
- So sánh xu hướng mức lương giữa remote, hybrid, và onsite.

Thông điệp chính của trang:
- Hình thức làm việc có ảnh hưởng đến mức lương, nhưng cần hiểu đây là so sánh theo hình thức làm việc, không phải theo thành phố.

Bảng dữ liệu chính:
- `Q11_salary_city_vs_remote.csv`

Bố trí biểu đồ:
- KPI trên cùng bên trái: giá trị cao nhất `avg_salary_usd`
- KPI trên cùng ở giữa: tổng `job_count`
- KPI trên cùng bên phải: `location_group` đứng đầu
- Giữa bên trái: biểu đồ cột cụm `avg_salary_usd` theo `location_group`
- Giữa bên phải: matrix `job_title` x `location_group`
- Bên dưới: small multiples theo `experience_level`

Thẻ KPI:
- `Mức lương cao nhất theo hình thức`
- `Số việc làm được bao phủ`
- `Hình thức nổi bật nhất`

Bộ lọc:
- `experience_level`
- `job_title`
- `location_group`

Sử dụng màu:
- Remote: xanh teal
- Hybrid: vàng
- Onsite: xanh navy

### Trang 5 - Q13 analytics vs engineering

Tiêu đề trang:
- **Lương entry-level giữa nhóm Analytics và Engineering khác nhau ra sao?**

Mục đích:
- So sánh mức lương entry-level giữa các nhóm vai trò.

Thông điệp chính của trang:
- Có thể so sánh vai trò Engineering và Analytics ở cấp độ entry-level, nhưng đây là so sánh nhóm vai trò, không phải kết luận về lộ trình học vấn.

Bảng dữ liệu chính:
- `Q13_analytics_vs_engineering_entry.csv`

Bố trí biểu đồ:
- KPI trên cùng bên trái: giá trị trung bình `avg_salary_usd`
- KPI trên cùng ở giữa: tổng `job_count`
- KPI trên cùng bên phải: `role_category` có mức lương cao nhất
- Giữa bên trái: biểu đồ thanh cụm theo `job_title`
- Giữa bên phải: decomposition tree dùng `role_category`, `job_title`, `country`
- Bên dưới: matrix có conditional formatting theo `avg_salary_usd`

Thẻ KPI:
- `Lương Entry-Level trung bình`
- `Số việc làm trong so sánh`
- `Nhóm vai trò trả lương cao nhất`

Bộ lọc:
- `country`
- `role_category`
- `job_title`

Sử dụng màu:
- Analytics: xanh navy
- Engineering: xanh teal

### Trang 6 - Q14 premium kỹ năng cloud

Tiêu đề trang:
- **Kỹ năng cloud nâng cao có liên hệ với mức lương cao hơn không?**

Mục đích:
- Thể hiện liệu yêu cầu cloud nâng cao có đi kèm mức lương cao hơn hay không.

Thông điệp chính của trang:
- Các việc làm gắn với kỹ năng cloud nâng cao thường có dấu hiệu premium về lương, nhưng đây là mối tương quan, không phải quan hệ nhân quả.

Bảng dữ liệu chính:
- `Q14_cloud_skill_salary_premium.csv`

Bố trí biểu đồ:
- KPI trên cùng bên trái: giá trị trung bình `avg_salary_usd` có cloud
- KPI trên cùng ở giữa: giá trị trung bình `avg_salary_usd` không có cloud
- KPI trên cùng bên phải: mức chênh premium
- Giữa bên trái: biểu đồ cột cụm theo `has_advanced_cloud`
- Giữa bên phải: matrix theo `job_title` và `has_advanced_cloud`
- Bên dưới: bảng hỗ trợ theo `experience_level`

Thẻ KPI:
- `Lương TB có kỹ năng Cloud`
- `Lương TB không có Cloud`
- `Chênh lệch Cloud Premium (USD)`

Bộ lọc:
- `experience_level`
- `job_title`

Sử dụng màu:
- Có cloud: xanh teal
- Không cloud: xanh navy
- Thẻ premium: vàng

Suggested measure:
```DAX
Cloud Premium USD =
VAR CloudPay =
    CALCULATE(
        AVERAGE('Q14_cloud_skill_salary_premium'[avg_salary_usd]),
        'Q14_cloud_skill_salary_premium'[has_advanced_cloud] = "Has Advanced Cloud Skill"
    )
VAR NonCloudPay =
    CALCULATE(
        AVERAGE('Q14_cloud_skill_salary_premium'[avg_salary_usd]),
        'Q14_cloud_skill_salary_premium'[has_advanced_cloud] = "No Advanced Cloud Skill"
    )
RETURN
    CloudPay - NonCloudPay
```

### Trang 7 - Q16 xu hướng tuyển dụng

Tiêu đề trang:
- **Quy mô tuyển dụng đã thay đổi như thế nào theo thời gian?**

Mục đích:
- Thể hiện biến động tuyển dụng theo năm giữa các quốc gia và cấp độ kinh nghiệm.

Thông điệp chính của trang:
- Tuyển dụng thay đổi theo năm và theo thị trường, nhưng bộ dữ liệu chỉ hỗ trợ đọc xu hướng hàng năm, không hỗ trợ kết luận theo mùa vụ.

Bảng dữ liệu chính:
- `Q16_hiring_trend_by_year.csv`

Bố trí biểu đồ:
- KPI trên cùng bên trái: `year_total` mới nhất
- KPI trên cùng ở giữa: `yoy_growth_pct` mới nhất
- KPI trên cùng bên phải: giá trị trung bình `avg_salary_usd`
- Giữa bên trái: biểu đồ đường `year_total` theo `posted_year`
- Giữa bên phải: combo chart gồm `year_total` và `yoy_growth_pct`
- Bên dưới: matrix theo `country` và `posted_year`

Thẻ KPI:
- `Quy mô tuyển dụng mới nhất`
- `Tăng trưởng YoY mới nhất`
- `Lương trung bình`

Bộ lọc:
- `country`
- `experience_level`

Sử dụng màu:
- Đường xu hướng: xanh navy
- Đường tăng trưởng: vàng
- Thẻ lương: xanh teal

### Trang 8 - Q18 nhu cầu kỹ năng

Tiêu đề trang:
- **Kỹ năng nào có nhu cầu nâng cao mạnh nhất?**

Mục đích:
- Xếp hạng kỹ năng theo số lượng và tỷ lệ nhu cầu nâng cao.

Thông điệp chính của trang:
- Một số kỹ năng xuất hiện nhiều hơn trong các yêu cầu nâng cao, nhưng đây là cường độ nhu cầu, không phải thước đo trực tiếp của sự thiếu hụt nhân lực.

Bảng dữ liệu chính:
- `Q18_undersupplied_skills.csv`

Bố trí biểu đồ:
- KPI trên cùng bên trái: `skill` đứng đầu
- KPI trên cùng ở giữa: giá trị lớn nhất `advanced_demand_count`
- KPI trên cùng bên phải: giá trị lớn nhất `advanced_demand_pct`
- Giữa bên trái: biểu đồ thanh ngang `advanced_demand_count` theo `skill`
- Giữa bên phải: biểu đồ cột hoặc lollipop cho `advanced_demand_pct`
- Bên dưới: bảng chi tiết

Thẻ KPI:
- `Kỹ năng đứng đầu`
- `Số lượng nhu cầu nâng cao cao nhất`
- `Tỷ lệ nhu cầu nâng cao cao nhất`

Bộ lọc:
- `skill_category`

Sử dụng màu:
- Kỹ năng Cloud: xanh teal
- Kỹ năng ML: xanh navy
- Kỹ năng lập trình: vàng

### Trang 9 - Q19 so sánh chi phí tuyển dụng

Tiêu đề trang:
- **Một nhân sự Mid-Level có rẻ hơn hai nhân sự Entry-Level không?**

Mục đích:
- So sánh bài toán chi phí lương giữa một nhân sự mid-level và hai nhân sự junior.

Thông điệp chính của trang:
- Xét riêng chi phí lương, nhân sự mid-level có thể hiệu quả hơn trong nhiều trường hợp, nhưng trang này không nên hàm ý rằng năng suất lao động là tương đương.

Bảng dữ liệu chính:
- `Q19_mid_vs_2_juniors.csv`

Bố trí biểu đồ:
- KPI trên cùng bên trái: số trường hợp `Mid is cheaper`
- KPI trên cùng ở giữa: giá trị trung bình `mid_to_entry_ratio`
- KPI trên cùng bên phải: mức tiết kiệm trung bình
- Giữa bên trái: biểu đồ thanh cụm so sánh `mid_avg_salary_usd` và `cost_2_juniors_usd`
- Giữa bên phải: matrix `job_title` x `country`
- Bên dưới: bảng hỗ trợ với `cost_verdict`

Thẻ KPI:
- `Số trường hợp Mid rẻ hơn`
- `Tỉ lệ Mid/Entry trung bình`
- `Chênh lệch chi phí trung bình`

Bộ lọc:
- `country`
- `job_title`
- `cost_verdict`

Sử dụng màu:
- Lương Mid: xanh teal
- Chi phí 2 Junior: xanh navy
- Nhấn mạnh kết luận rẻ hơn: vàng

Suggested measure:
```DAX
Avg Cost Difference USD =
AVERAGEX(
    'Q19_mid_vs_2_juniors',
    'Q19_mid_vs_2_juniors'[cost_2_juniors_usd] - 'Q19_mid_vs_2_juniors'[mid_avg_salary_usd]
)
```

### Trang 10 - Q21 cơ hội theo quốc gia

Tiêu đề trang:
- **Tổ hợp quốc gia và năm nào có điểm cơ hội cao nhất về việc làm và mức lương?**

Mục đích:
- So sánh cơ hội theo địa lý dựa trên nhu cầu, mức lương, và tỷ lệ remote.

Thông điệp chính của trang:
- Cơ hội theo quốc gia là câu chuyện tổng hợp của quy mô việc làm và mức lương, vì vậy điểm số hữu ích cho so sánh nhưng cần được trình bày như một chỉ số tự xây dựng.

Bảng dữ liệu chính:
- `Q21_opportunity_by_country.csv`

Bố trí biểu đồ:
- KPI trên cùng bên trái: `opportunity_score` cao nhất
- KPI trên cùng ở giữa: `avg_salary_usd` cao nhất
- KPI trên cùng bên phải: `remote_pct` cao nhất
- Giữa bên trái: biểu đồ phân tán `total_jobs` vs `avg_salary_usd`
- Giữa bên phải: matrix `country` x `posted_year` dùng `opportunity_score`
- Bên dưới: bảng xếp hạng theo `opportunity_score`

Thẻ KPI:
- `Điểm cơ hội cao nhất`
- `Lương trung bình cao nhất`
- `Tỷ lệ Remote cao nhất`

Bộ lọc:
- `country`
- `posted_year`

Sử dụng màu:
- Điểm cơ hội: gradient vàng
- Lương: xanh teal
- Số lượng việc làm: xanh navy

### Trang 11 - Q25 tăng trưởng theo quy mô công ty

Tiêu đề trang:
- **Tăng trưởng tuyển dụng khác nhau như thế nào theo quy mô công ty?**

Mục đích:
- Thể hiện sự khác biệt về tăng trưởng việc làm giữa công ty nhỏ, vừa, và lớn.

Thông điệp chính của trang:
- Quy mô công ty ảnh hưởng đến mô hình tuyển dụng, nhưng các khác biệt year-over-year nên được xem là xu hướng tham khảo vì bộ dữ liệu là synthetic và cân bằng.

Bảng dữ liệu chính:
- `Q25_growth_by_company_size.csv`

Bố trí biểu đồ:
- KPI trên cùng bên trái: `total_jobs` mới nhất
- KPI trên cùng ở giữa: `yoy_growth_pct` mới nhất
- KPI trên cùng bên phải: giá trị trung bình `avg_salary_usd`
- Giữa bên trái: biểu đồ đường `total_jobs` theo `posted_year`
- Giữa bên phải: matrix `company_size` x `posted_year`
- Bên dưới: biểu đồ cột chồng theo `posted_year`

Thẻ KPI:
- `Quy mô việc làm mới nhất`
- `Tăng trưởng YoY mới nhất`
- `Lương trung bình theo quy mô công ty`

Bộ lọc:
- `country`
- `company_size`

Sử dụng màu:
- Công ty nhỏ: xanh teal
- Công ty vừa: vàng
- Công ty lớn: xanh navy

## Thứ tự trang đề xuất

Thứ tự trang đề xuất:
1. Tổng quan điều hành
2. Q1 vai trò entry-level
3. Q6 trần lương senior theo ngành
4. Q11 hình thức làm việc
5. Q13 analytics vs engineering
6. Q14 premium kỹ năng cloud
7. Q16 xu hướng tuyển dụng
8. Q18 nhu cầu kỹ năng
9. Q19 so sánh chi phí tuyển dụng
10. Q21 cơ hội theo quốc gia
11. Q25 tăng trưởng theo quy mô công ty

## Lưu ý hoàn thiện báo cáo

Để báo cáo trông mạnh mẽ và chuyên nghiệp hơn:
- Mỗi trang chỉ nên tập trung vào một câu hỏi chính
- Mỗi trang nên có 2 biểu đồ chính và 3 thẻ KPI
- Lặp lại vị trí slicer và ý nghĩa màu sắc giữa các trang
- Đặt thêm dòng subtitle insight ngắn bên dưới tiêu đề trang
- Tránh khẳng định quan hệ nhân quả khi dữ liệu chỉ thể hiện tương quan hoặc so sánh
- Nêu rõ ở phần mở đầu rằng bộ dữ liệu là synthetic hoặc simulated
