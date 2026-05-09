# Insight Hypotheses — Tab 1 & Tab 2 — Session 05 (29/04/2026)

**Prompt received at:** 10:28:13
**Helper:** insight-hypothesis
**Responded by:** Claude (claude-sonnet-4-6)

---

## Tab 1 — Tổng quan

### H1: GDCD là môn có điểm trung bình cao nhất mọi năm
- **Loại biểu đồ:** Grouped Bar Chart (điểm TB từng môn × năm)
- **Bằng chứng cần thu thập:** `df.groupby('nam')[SCORE_COLS].mean()` → so sánh rank của GDCD
- **Tính falsifiable:** Có — nếu một năm Văn hay Địa cao hơn GDCD, giả thuyết bị bác bỏ
- **Lý do thú vị:** GDCD thường bị xem là môn "dễ", nếu xác nhận được → minh chứng cho cách ra đề

### H2: Quy mô thí sinh giảm sau COVID-19 (2021 thấp hơn 2020)
- **Loại biểu đồ:** Area Chart (số thí sinh qua 5 năm)
- **Bằng chứng cần thu thập:** `df.groupby('nam')['sbd'].count()`
- **Tính falsifiable:** Có — đây là giả thuyết kinh tế-xã hội, có thể đúng hoặc sai
- **Lý do thú vị:** COVID có thể làm gián đoạn việc học nhưng không nhất thiết làm giảm số thí sinh

### H3: Tỷ lệ khối A00 giảm dần do xu hướng chọn KHXH tăng
- **Loại biểu đồ:** 100% Stacked Bar Chart (cơ cấu khối thi × năm)
- **Bằng chứng cần thu thập:** Tính tỷ lệ mỗi khối thi theo năm
- **Tính falsifiable:** Có — tỷ lệ A00 có thể tăng nếu xu hướng ngược lại
- **Lý do thú vị:** Phản ánh định hướng nghề nghiệp của học sinh theo thời gian

### H4: Toán là môn có điểm TB thấp nhất trong nhóm môn KHTN
- **Loại biểu đồ:** Bar Chart hoặc Line Chart (điểm TB 5 môn KHTN)
- **Bằng chứng cần thu thập:** `df.groupby('nam')[['toan','vat_ly','hoa_hoc','sinh_hoc']].mean()`
- **Tính falsifiable:** Có — Vật lý hoặc Hóa có thể thấp hơn một số năm
- **Lý do thú vị:** Toán là môn cơ sở quan trọng nhất, nếu điểm TB thấp nhất → tín hiệu đáng lo ngại

---

## Tab 2 — Phổ điểm từng môn

### H5: Ngoại ngữ có phân phối bimodal rõ nhất, đặc biệt năm 2021
- **Loại biểu đồ:** Histogram (probability density, overlay nhiều năm)
- **Bằng chứng cần thu thập:** Vẽ histogram ngoại ngữ từng năm, quan sát số đỉnh
- **Tính falsifiable:** Có — nếu phân phối đơn đỉnh (unimodal), giả thuyết bị bác bỏ
- **Lý do thú vị:** Bimodal phản ánh khoảng cách năng lực giữa thị thành và nông thôn

### H6: Điểm Ngữ Văn có phân phối chuẩn (bell curve) nhất trong tất cả các môn
- **Loại biểu đồ:** Histogram với KDE overlay
- **Bằng chứng cần thu thập:** Kiểm tra skewness và kurtosis của phân phối Văn
- **Tính falsifiable:** Có — GDCD hoặc Địa có thể có phân phối chuẩn hơn
- **Lý do thú vị:** Văn là môn tự luận — phân phối chuẩn gợi ý chấm điểm nhất quán

### H7: Hóa học có IQR nhỏ nhất trong nhóm môn KHTN (đề ít phân hóa)
- **Loại biểu đồ:** Boxplot (overlay nhiều năm)
- **Bằng chứng cần thu thập:** Tính IQR = Q3 - Q1 cho 4 môn KHTN
- **Tính falsifiable:** Có — Sinh học có thể có IQR nhỏ hơn
- **Lý do thú vị:** IQR nhỏ = đề ít phân hóa, điểm số tập trung ở vùng trung bình

### H8: Phổ điểm năm 2022 dịch sang phải (điểm cao hơn) so với năm 2020
- **Loại biểu đồ:** Multi-year Line Chart (density curves)
- **Bằng chứng cần thu thập:** So sánh mean và median giữa 2020 và 2022 cho từng môn
- **Tính falsifiable:** Có — nếu phổ 2022 không dịch phải, giả thuyết bị bác bỏ
- **Lý do thú vị:** Có thể phản ánh điều chỉnh độ khó đề thi sau 2 năm COVID

---

> **Lưu ý của AI:** Các giả thuyết trên được thiết kế để có tính phân hóa cao và kiểm chứng được bằng dữ liệu thực. Nhóm nên chạy kiểm chứng độc lập trước khi kết luận. Một số giả thuyết có thể bị bác bỏ — đây là kết quả phân tích hợp lệ, không phải thất bại.
