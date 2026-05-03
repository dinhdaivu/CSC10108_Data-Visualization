# Báo cáo insight Tab 1 và Tab 5: Phân tích điểm thi THPT Quốc gia

## Phạm vi dữ liệu

Báo cáo sử dụng dữ liệu trong `THPT_Dashboard/data/processed`, là cùng nguồn dữ liệu đang được dashboard Streamlit sử dụng. Phạm vi phân tích chính gồm các năm 2020-2024 với 4.859.667 bản ghi thí sinh và 9 môn thi: Toán, Ngữ văn, Ngoại ngữ, Vật lý, Hóa học, Sinh học, Lịch sử, Địa lý và GDCD.

Tỉnh/thành được suy ra từ hai chữ số đầu của số báo danh và bảng `mavung.csv`. Giai đoạn 2021-2024 ánh xạ đầy đủ tỉnh/thành; riêng năm 2020 có 56.738 bản ghi mang mã `00` nên không xác định được tỉnh/thành. Các file dữ liệu 2025 không được đưa vào xu hướng chính vì chưa phải bộ dữ liệu hoàn chỉnh theo cùng cấu trúc năm.

## Tab 1: Tổng quan kỳ thi THPT Quốc gia

### 1. Quy mô thí sinh thay đổi như thế nào qua các năm?

| Năm | Số thí sinh | Thay đổi so với năm trước | Tỷ lệ thay đổi |
| --- | --- | --- | --- |
| 2020 | 870.486 |  |  |
| 2021 | 914.558 | 44.072 | 5,06% |
| 2022 | 995.435 | 80.877 | 8,84% |
| 2023 | 1.017.584 | 22.149 | 2,23% |
| 2024 | 1.061.604 | 44.020 | 4,33% |

Quy mô kỳ thi tăng ổn định trong toàn bộ giai đoạn. Tổng số thí sinh tăng từ 870.486 năm 2020 lên 1.061.604 năm 2024, tương đương tăng 21,96%. Nếu chỉ xét giai đoạn 2021-2024, mức tăng là 16,08%. Tốc độ tăng trung bình hằng năm trong giai đoạn 2020-2024 đạt 5,11%.

Năm 2022 là năm có mức tăng mạnh nhất về số lượng tuyệt đối và tỷ lệ phần trăm, với thêm 80.877 thí sinh so với năm 2021. Điều này cho thấy nhu cầu dự thi và quy mô hệ thống đang mở rộng, nhưng tốc độ tăng không tuyến tính; năm 2023 tăng chậm hơn, sau đó năm 2024 phục hồi mức tăng cao hơn.

### 2. Mức độ phân hóa điểm giữa các môn học như thế nào?

| Môn | Điểm trung bình | Độ lệch chuẩn | Trung vị | Số bài thi hợp lệ |
| --- | --- | --- | --- | --- |
| GDCD | 8,19 | 1,10 | 8,25 | 2.674.578 |
| Ngữ văn | 6,75 | 1,36 | 6,75 | 4.798.302 |
| Địa lý | 6,75 | 1,26 | 6,75 | 3.176.187 |
| Hóa học | 6,69 | 1,58 | 7,00 | 1.623.925 |
| Vật lý | 6,65 | 1,50 | 7,00 | 1.616.452 |
| Toán | 6,48 | 1,68 | 6,80 | 4.803.559 |
| Lịch sử | 5,87 | 1,71 | 6,00 | 3.200.121 |
| Sinh học | 5,77 | 1,44 | 5,75 | 1.600.865 |
| Ngoại ngữ | 5,33 | 2,01 | 5,00 | 4.240.694 |

GDCD có điểm trung bình cao nhất, đạt 8,19, đồng thời có độ lệch chuẩn thấp nhất, chỉ 1,10. Điều này cho thấy mặt bằng điểm GDCD cao nhưng khả năng phân loại giữa các nhóm thí sinh không mạnh.

Ngoại ngữ có điểm trung bình thấp nhất, đạt 5,33, nhưng lại có độ lệch chuẩn cao nhất, đạt 2,01. Đây là môn có mức chênh lệch năng lực rõ nhất giữa các thí sinh, phù hợp để nhận diện khoảng cách trình độ. Lịch sử và Toán cũng có độ lệch chuẩn cao, lần lượt là 1,71 và 1,68, nên có khả năng phân hóa tốt hơn nhiều môn còn lại.

Khoảng cách giữa môn có điểm trung bình cao nhất và thấp nhất là 2,87 điểm. Đây là mức chênh đáng kể, cho thấy cấu trúc điểm giữa các môn không đồng đều: một số môn có xu hướng điểm cao và tập trung, trong khi một số môn thể hiện phổ điểm rộng hơn.

### 3. Thí sinh phân bố theo địa phương như thế nào?

Top 10 tỉnh/thành có số thí sinh lớn nhất năm 2024:

| Xếp hạng | Tỉnh/thành | Số thí sinh |
| --- | --- | --- |
| 1 | Hà Nội | 107.867 |
| 2 | TP. Hồ Chí Minh | 87.322 |
| 3 | Thanh Hóa | 38.532 |
| 4 | Nghệ An | 36.729 |
| 5 | Đồng Nai | 33.800 |
| 6 | Hải Phòng | 25.529 |
| 7 | Hải Dương | 23.366 |
| 8 | Thái Bình | 22.580 |
| 9 | Nam Định | 21.760 |
| 10 | Bắc Giang | 21.755 |

Hà Nội và TP. Hồ Chí Minh là hai trung tâm thí sinh lớn nhất, vượt xa các địa phương còn lại. Nhóm tỉnh có quy mô lớn tiếp theo gồm Thanh Hóa, Nghệ An và Đồng Nai. Đây là các địa phương có dân số lớn hoặc quy mô học sinh phổ thông cao, nên đóng góp đáng kể vào tổng số thí sinh toàn quốc.

Các tỉnh có số thí sinh thấp nhất năm 2024:

| Tỉnh/thành | Số thí sinh |
| --- | --- |
| Ninh Thuận | 6.288 |
| Cao Bằng | 5.506 |
| Kon Tum | 5.038 |
| Lai Châu | 4.188 |
| Bắc Kạn | 3.174 |

Sự khác biệt này cho thấy dashboard cần hỗ trợ cả hai góc nhìn: so sánh tuyệt đối để thấy quy mô, và so sánh theo tỷ lệ hoặc điểm trung bình để tránh các địa phương nhỏ bị lu mờ.

### 4. Xu hướng lựa chọn tổ hợp thi của học sinh ra sao?

| Năm | KHTN | KHXH | Thi không đầy đủ tổ hợp |
| --- | --- | --- | --- |
| 2020 | 286.170 (32,87%) | 482.601 (55,44%) | 101.715 (11,68%) |
| 2021 | 318.205 (34,79%) | 487.980 (53,36%) | 108.373 (11,85%) |
| 2022 | 318.685 (32,01%) | 554.090 (55,66%) | 122.660 (12,32%) |
| 2023 | 322.540 (31,70%) | 565.243 (55,55%) | 129.801 (12,76%) |
| 2024 | 339.787 (32,01%) | 583.106 (54,93%) | 138.711 (13,07%) |

KHXH là nhóm tổ hợp chiếm ưu thế trong toàn bộ giai đoạn, dao động quanh 53-56% tổng số thí sinh. Năm 2024, KHXH chiếm 54,93%, cao hơn đáng kể so với KHTN ở mức 32,01%.

KHTN tăng về số lượng tuyệt đối từ 286.170 năm 2020 lên 339.787 năm 2024, nhưng tỷ trọng không tăng tương ứng vì tổng quy mô kỳ thi cũng mở rộng. Nhóm “thi không đầy đủ tổ hợp” tăng từ 11,68% năm 2020 lên 13,07% năm 2024, cho thấy số thí sinh không rơi vào cấu trúc KHTN/KHXH đầy đủ ngày càng đáng chú ý.

## Tab 5: Tương quan và phân hóa đề thi

### 1. Mối quan hệ giữa các môn học trong kỳ thi như thế nào?

Các cặp môn có tương quan Pearson trên 0,50 gồm:

| Cặp môn | Hệ số tương quan |
| --- | --- |
| Toán - Vật lý | 0,566 |
| Toán - Ngoại ngữ | 0,559 |
| Lịch sử - Địa lý | 0,559 |
| Địa lý - GDCD | 0,549 |

Trong nhóm KHTN, tương quan nội bộ trung bình là 0,30. Vật lý - Hóa học và Hóa học - Sinh học có tương quan khoảng 0,38, trong khi Vật lý - Sinh học chỉ đạt 0,122. Điều này cho thấy các môn KHTN không hoàn toàn đi cùng nhau; mỗi môn vẫn đòi hỏi kiểu năng lực và chiến lược học khác nhau.

Trong nhóm KHXH, tương quan nội bộ trung bình là 0,53, cao hơn rõ rệt so với KHTN. Lịch sử - Địa lý đạt 0,559 và Địa lý - GDCD đạt 0,549. Như vậy, thí sinh có kết quả tốt ở một môn KHXH thường có xu hướng đạt kết quả tương đối tốt ở các môn KHXH khác.

Toán có mối liên hệ mạnh với Vật lý và Ngoại ngữ. Với Vật lý, điều này phản ánh vai trò của năng lực định lượng. Với Ngoại ngữ, tương quan có thể phản ánh nhóm thí sinh có nền tảng học thuật tổng quát tốt hơn, đặc biệt ở các thành phố lớn và nhóm định hướng xét tuyển cạnh tranh.

### 2. Hà Nội và TP. Hồ Chí Minh khác nhau như thế nào theo từng môn?

So sánh điểm trung bình năm 2024:

| Môn | Hà Nội | TP. Hồ Chí Minh | Chênh lệch Hà Nội - TP. Hồ Chí Minh |
| --- | --- | --- | --- |
| Toán | 6,75 | 6,98 | -0,24 |
| Ngữ văn | 7,76 | 6,65 | 1,10 |
| Ngoại ngữ | 6,20 | 6,73 | -0,53 |
| Vật lý | 6,81 | 6,34 | 0,47 |
| Hóa học | 6,22 | 6,49 | -0,27 |
| Sinh học | 5,91 | 6,22 | -0,31 |
| Lịch sử | 6,62 | 6,62 | -0,00 |
| Địa lý | 7,06 | 7,20 | -0,14 |
| GDCD | 8,12 | 8,31 | -0,19 |

Hà Nội có lợi thế nổi bật ở Ngữ văn, cao hơn TP. Hồ Chí Minh 1,10 điểm, và ở Vật lý, cao hơn 0,47 điểm. Đây là hai khác biệt lớn nhất theo hướng Hà Nội cao hơn.

TP. Hồ Chí Minh cao hơn ở Toán, Ngoại ngữ, Hóa học, Sinh học, Địa lý và GDCD. Chênh lệch lớn nhất theo hướng TP. Hồ Chí Minh cao hơn là Ngoại ngữ, với khoảng cách 0,53 điểm. Lịch sử gần như cân bằng giữa hai thành phố.

Kết quả này cho thấy hai trung tâm lớn có cấu trúc thế mạnh khác nhau. Vì vậy, khi dashboard so sánh địa phương, không nên chỉ dùng một chỉ số tổng hợp duy nhất; cần tách theo môn để tránh che mất các khác biệt quan trọng.

### 3. Đề thi có phân hóa học sinh tốt hay không?

Phân loại sử dụng hai ngưỡng trung bình toàn bộ môn: điểm trung bình chung của 9 môn là 6,50 và độ lệch chuẩn trung bình là 1,52. Điểm trung bình cao hơn được hiểu là đề dễ hơn; độ lệch chuẩn cao hơn được hiểu là khả năng phân hóa tốt hơn.

| Môn | Điểm trung bình | Độ lệch chuẩn | Nhóm đánh giá |
| --- | --- | --- | --- |
| GDCD | 8,19 | 1,10 | Dễ và phân hóa kém |
| Ngữ văn | 6,75 | 1,36 | Dễ và phân hóa kém |
| Địa lý | 6,75 | 1,26 | Dễ và phân hóa kém |
| Hóa học | 6,69 | 1,58 | Dễ và phân hóa tốt |
| Vật lý | 6,65 | 1,50 | Dễ và phân hóa kém |
| Toán | 6,48 | 1,68 | Khó và phân hóa tốt |
| Lịch sử | 5,87 | 1,71 | Khó và phân hóa tốt |
| Sinh học | 5,77 | 1,44 | Khó và phân hóa kém |
| Ngoại ngữ | 5,33 | 2,01 | Khó và phân hóa tốt |

Có 4/9 môn đạt mức phân hóa tốt: Ngoại ngữ, Lịch sử, Toán và Hóa học. Trong đó, Ngoại ngữ là môn phân hóa mạnh nhất nhưng cũng là môn có điểm trung bình thấp nhất. Toán và Lịch sử cũng đóng vai trò phân loại tốt vì có độ lệch chuẩn cao hơn ngưỡng trung bình.

Có 4 môn thuộc nhóm dễ và phân hóa kém: GDCD, Ngữ văn, Địa lý và Vật lý. Các môn này có điểm trung bình cao nhưng phổ điểm tập trung hơn, nên khả năng tách biệt thí sinh mạnh - yếu không rõ bằng các môn có độ lệch chuẩn cao. Sinh học nằm ở nhóm khó và phân hóa kém, cần được xem xét riêng vì điểm trung bình thấp nhưng độ phân tán chưa đủ tốt.

Kết luận chung là đề thi có khả năng phân hóa ở một số môn trọng điểm, nhưng chưa đồng đều trên toàn bộ hệ thống môn thi. Nếu mục tiêu là tăng năng lực phân loại phục vụ xét tuyển, các môn có điểm cao và độ lệch chuẩn thấp cần được xem xét về cấu trúc câu hỏi, tỷ lệ câu vận dụng và độ phủ mức độ khó.

## Kết luận chính

Quy mô kỳ thi THPT Quốc gia tăng rõ rệt trong giai đoạn 2020-2024, với năm 2024 đạt hơn 1,06 triệu thí sinh. KHXH tiếp tục là tổ hợp phổ biến nhất, trong khi nhóm không hoàn thành đầy đủ một tổ hợp cũng tăng dần và cần được theo dõi.

Về điểm số, GDCD là môn có mặt bằng điểm cao nhất nhưng phân hóa yếu nhất. Ngoại ngữ là môn có mặt bằng điểm thấp nhất nhưng phân hóa mạnh nhất. Các môn KHXH có tương quan nội bộ cao hơn KHTN, cho thấy kết quả trong nhóm này có xu hướng đi cùng nhau rõ hơn.

Về địa phương, Hà Nội và TP. Hồ Chí Minh là hai trung tâm thí sinh lớn nhất nhưng có thế mạnh môn học khác nhau. Hà Nội nổi bật ở Ngữ văn và Vật lý, trong khi TP. Hồ Chí Minh cao hơn ở Ngoại ngữ và nhiều môn còn lại. Đây là insight quan trọng cho phần đối chuẩn địa phương trong dashboard.

Về chất lượng đề thi, 4/9 môn có khả năng phân hóa tốt. Kết quả này đủ để dashboard kể được câu chuyện về phân loại năng lực, nhưng cũng chỉ ra rằng chất lượng phân hóa chưa đồng đều giữa các môn.

## Hạn chế và lưu ý diễn giải

Tỉnh/thành được suy ra từ mã số báo danh, không phải từ địa chỉ cư trú hay trường học của thí sinh. Do đó, phân tích địa phương phản ánh đơn vị đăng ký/dự thi theo mã số báo danh nhiều hơn là nơi cư trú thực tế.

Năm 2020 có 56.738 bản ghi không ánh xạ được tỉnh/thành do mã `00`; các phân tích địa phương chi tiết nên ưu tiên giai đoạn 2021-2024 hoặc loại nhóm chưa xác định khỏi so sánh tỉnh/thành.

Phân loại KHTN/KHXH được suy luận từ sự hiện diện đầy đủ của ba môn trong từng nhóm. Đây là cách nhất quán với dashboard, nhưng vẫn có thể khác với tổ hợp xét tuyển đại học thực tế của từng thí sinh.
