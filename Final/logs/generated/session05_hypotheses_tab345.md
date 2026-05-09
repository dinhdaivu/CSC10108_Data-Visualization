# Insight Hypotheses — Tab 3, 4, 5 — Session 05 (29/04/2026)

**Prompt received at:** 11:15:04
**Helper:** insight-hypothesis
**Responded by:** Claude (claude-sonnet-4-6)

---

## Tab 3 — Tổ hợp xét tuyển

### H9: Khối A01 đang thu hẹp khoảng cách Top 5% với khối A00
- **Loại biểu đồ:** Line Chart (Top 5% percentile × năm, theo khối)
- **Bằng chứng cần thu thập:** `groupby(['khoi','nam'])['tong_diem'].quantile(0.95)`
- **Tính falsifiable:** Có — khoảng cách có thể tăng nếu A00 ngày càng cạnh tranh hơn
- **Lý do thú vị:** A01 thêm Tiếng Anh thay Hóa — nếu Top 5% tăng, phản ánh học sinh giỏi Anh ngày càng nhiều

### H10: GDCD là "bias variable" đẩy điểm tổng KHXH cao hơn thực tế năng lực
- **Loại biểu đồ:** Radar Chart (đóng góp từng môn trong Top 5% KHXH vs. KHTN)
- **Bằng chứng cần thu thập:** So sánh mean từng môn trong tổ hợp KHXH và KHTN ở Top 5%
- **Tính falsifiable:** Có — nếu GDCD không đặc biệt cao trong KHXH, giả thuyết bị bác bỏ
- **Lý do thú vị:** Gợi ý bất bình đẳng trong cơ chế tuyển sinh giữa hai nhóm ngành

### H11: Tổng điểm khối B00 có phương sai nhỏ nhất so với A00, C00, D01
- **Loại biểu đồ:** Histogram (tổng điểm từng khối) hoặc Boxplot
- **Bằng chứng cần thu thập:** `df[df['khoi']=='B00']['tong_diem'].std()` so với các khối khác
- **Tính falsifiable:** Có — C00 hoặc D01 có thể có phương sai nhỏ hơn
- **Lý do thú vị:** Phương sai nhỏ → phân phối điểm tập trung → đề ít phân hóa

---

## Tab 4 — Phân tích địa lý

### H12: Nam Định dẫn đầu điểm Toán nhiều năm liên tiếp (≥ 3/5 năm)
- **Loại biểu đồ:** Choropleth Map (màu đậm nhất ở Nam Định) + Dumbbell Chart
- **Bằng chứng cần thu thập:** `groupby(['ten_tinh','nam'])['toan'].mean()` → rank theo năm
- **Tính falsifiable:** Có — Hà Nội hoặc TP.HCM có thể dẫn đầu
- **Lý do thú vị:** Nam Định nổi tiếng là "vùng đất học" — đây là kiểm chứng thực tế

### H13: TP.HCM không dẫn đầu điểm TB dù có quy mô thí sinh lớn nhất
- **Loại biểu đồ:** Quadrant Bubble Chart (trục X: điểm TB, trục Y: số thí sinh, bubble size: quy mô)
- **Bằng chứng cần thu thập:** Rank điểm TB TP.HCM so với Hà Nội, Nam Định, Hải Phòng
- **Tính falsifiable:** Có — TP.HCM có thể dẫn đầu một số môn
- **Lý do thú vị:** Quy mô lớn thường kéo mean xuống do phân phối rộng hơn

### H14: Các tỉnh Tây Nguyên (Đắk Lắk, Đắk Nông, Gia Lai, Kon Tum, Lâm Đồng) nhất quán nằm phân vị thấp 5/5 năm
- **Loại biểu đồ:** Choropleth multi-year (animation) hoặc heatmap tỉnh × năm
- **Bằng chứng cần thu thập:** Rank tỉnh theo điểm TB Toán và Văn từ 2020 đến 2024
- **Tính falsifiable:** Có — Lâm Đồng có đô thị Đà Lạt, có thể không ở phân vị thấp
- **Lý do thú vị:** Phản ánh bất bình đẳng giáo dục theo vùng địa lý kéo dài nhiều năm

---

## Tab 5 — Tương quan môn học

### H15: Tương quan Pearson giữa Sử–Địa tăng dần từ 2020 đến 2024
- **Loại biểu đồ:** Line Chart (hệ số Pearson × năm)
- **Bằng chứng cần thu thập:** `df.groupby('nam').apply(lambda x: x['lich_su'].corr(x['dia_ly']))`
- **Tính falsifiable:** Có — tương quan có thể dao động, không có xu hướng rõ
- **Lý do thú vị:** Tăng tương quan → thí sinh học 2 môn cùng chiến lược, hoặc đề ngày càng tương đồng

### H16: Cặp Toán–Lý có tương quan Pearson cao nhất trong nhóm KHTN
- **Loại biểu đồ:** Correlation Heatmap 9×9
- **Bằng chứng cần thu thập:** Ma trận Pearson toàn bộ 9 môn
- **Tính falsifiable:** Có — Lý–Hóa có thể cao hơn Toán–Lý
- **Lý do thú vị:** Kiểm tra liên hệ logic: Toán là nền tảng Lý, nhưng Lý–Hóa chia sẻ phong cách bài tập tương tự hơn

---

> **Lưu ý của AI:** Giả thuyết H10 và H12 có tiềm năng trở thành insight nổi bật nhất của dashboard — nhóm nên ưu tiên kiểm chứng hai giả thuyết này trước. H16 có thể bị bác bỏ (Lý–Hóa thường cao hơn trong thực tế) — nếu bác bỏ được, đây là finding thú vị để trình bày trong vấn đáp.
