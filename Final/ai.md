# 5.1 Ứng dụng AI trong quá trình thiết kế

---

##  Tổng quan về chiến lược tích hợp AI

Trong quá trình thực hiện đồ án, nhóm xác định Trí tuệ Nhân tạo (AI)
không chỉ là một công cụ hỗ trợ đơn thuần mà là một thành phần cộng
tác xuyên suốt toàn bộ vòng đời phát triển hệ thống — từ giai đoạn
kiểm định dữ liệu đầu vào, thiết kế biểu đồ, sinh mã nguồn, cho đến
chuẩn bị nội dung vấn đáp cuối kỳ.

Để đảm bảo tính minh bạch, có thể kiểm chứng và tránh phụ thuộc mù
quáng vào đầu ra của AI, nhóm áp dụng nguyên tắc **"Human-first,
AI-assisted"**: mọi phân tích và quyết định thiết kế đều được nhóm
thảo luận độc lập trước, sau đó mới sử dụng AI để xác nhận, bổ sung
hoặc phê bình. Toàn bộ vòng tương tác được ghi nhận bắt buộc theo
chuỗi truy vết:

```
Prompt → Script AI sinh ra → Script sau khi nhóm chỉnh sửa → Kết quả đã kiểm chứng
```

Chuỗi này được lưu tập trung trong file `ai-trace.md` và thư mục
`logs/`, phục vụ báo cáo minh bạch về mức độ can thiệp của AI trong
từng hạng mục công việc.

---

## 5.1.1 Hệ thống AI Prompt Helper chuẩn hóa

Nhóm thiết kế và lưu trữ một bộ **7 Prompt Helper chuyên biệt** trong
thư mục `.github/prompts/`, mỗi helper phục vụ một giai đoạn cụ thể
trong quy trình phát triển. Việc chuẩn hóa prompt giúp đảm bảo tính
nhất quán trong các phiên làm việc khác nhau và giữa các thành viên
trong nhóm.

### 5.1.1.1 `gatekeeper` — Kiểm định dataset đầu vào

**Mục tiêu:** Xác minh tập dữ liệu thô đáp ứng đầy đủ các tiêu chí
bắt buộc của đồ án trước khi tiến hành bất kỳ bước xử lý nào.

**Nội dung kiểm định:**

- Tổng số dòng dữ liệu ≥ 2.000 bản ghi
- Số biến độc lập ≥ 7 cột
- Tỷ lệ dữ liệu liên quan đến Việt Nam > 50% toàn tập
- Nguồn dữ liệu rõ ràng, có thể trích dẫn học thuật

**Kết quả áp dụng:** Nhóm xác nhận tập dữ liệu tổng hợp từ
`thpt2020.csv` đến `thpt2024.csv` đạt hơn 4,6 triệu bản ghi, 11 biến
chính, 100% dữ liệu Việt Nam — vượt toàn bộ ngưỡng yêu cầu.

---

###  5.1.1.2 `source-reliability` — Đánh giá độ tin cậy nguồn dữ liệu

**Mục tiêu:** Kiểm tra và luận chứng tính đáng tin cậy, minh bạch của
từng nguồn dữ liệu được sử dụng.

**Các nguồn được đánh giá:**

| Nguồn | Nền tảng | Đánh giá |
|---|---|---|
| Điểm thi THPT 2020–2024 | Kaggle | Dữ liệu gốc từ Bộ GD&ĐT, cộng đồng kiểm chứng |
| Tọa độ ranh giới hành chính | SimpleMaps | Nhà cung cấp bản đồ GIS uy tín quốc tế |
| Mã vùng tỉnh/thành | Tự tổng hợp | Đối chiếu với danh mục hành chính chính thức |

**Kết quả áp dụng:** AI đề xuất bổ sung ghi chú nguồn trích dẫn trong
báo cáo và khuyến nghị cố định phiên bản file `vn_geo.json` để tránh
thay đổi ngoài ý muốn.

---

###  5.1.1.3 `data-quality` — Rà soát chất lượng dữ liệu

**Mục tiêu:** Phát hiện và định lượng các vấn đề chất lượng dữ liệu
trước khi đưa vào phân tích.

**Các hạng mục kiểm tra:**

- **Giá trị khuyết thiếu (Missing values):** Xác định các dòng có toàn
  bộ cột điểm bằng `NaN` — tương ứng thí sinh đăng ký nhưng không dự
  thi
- **Giá trị trùng lặp (Duplicates):** Kiểm tra số báo danh xuất hiện
  nhiều lần trong cùng năm
- **Ngoại lệ (Outliers):** Rà soát điểm số nằm ngoài khoảng [0, 10]
  do lỗi nhập liệu

**Kết quả áp dụng:** AI sinh script phát hiện ~3,2% dòng rỗng toàn
phần trên tập 2020–2024. Nhóm quyết định loại bỏ các dòng này thay vì
imputation do tính chất dữ liệu thi cử.

---

###  5.1.1.4 `cleaning-script` — Sinh pipeline tiền xử lý tự động

**Mục tiêu:** Tự động hóa quy trình làm sạch và chuẩn hóa dữ liệu
bằng Pandas, đảm bảo tính tái lập (reproducibility).

**Các bước pipeline AI đề xuất:**

```python
# 1. Chuẩn hóa tên cột về định dạng thống nhất
# 2. Ghép nối 5 file CSV theo trục dọc (pd.concat)
# 3. Trích xuất mã vùng từ 2 ký tự đầu số báo danh
# 4. Merge với bảng mavung.csv để lấy tên tỉnh/thành
# 5. Loại bỏ dòng NaN toàn phần
# 6. Ép kiểu dữ liệu điểm về float64
# 7. Đồng bộ tên địa phương với vn_geo.json
```

**Kết quả áp dụng:** Nhóm chỉnh sửa thứ tự bước 3 và 4, bổ sung xử
lý edge case cho mã vùng không khớp (ví dụ: "Hoàng Sa", "Trường Sa"),
sau đó kiểm chứng bằng cách so sánh tổng dòng trước và sau cleaning.

---

###  5.1.1.5 `insight-hypothesis` — Xây dựng giả thuyết phân tích

**Mục tiêu:** Với mỗi tab dashboard, AI được yêu cầu đề xuất 8 giả
thuyết phân tích có tính phân hóa cao, kèm theo loại biểu đồ phù hợp
và bằng chứng cần thu thập.

**Ví dụ giả thuyết được AI đề xuất và nhóm kiểm chứng:**

| Tab | Giả thuyết | Kết quả kiểm chứng |
|---|---|---|
| Tab 1 | GDCD luôn là môn có điểm TB cao nhất | ✅ Xác nhận, 5/5 năm |
| Tab 2 | Ngoại ngữ có phân phối bimodal | ✅ Rõ rệt năm 2021 |
| Tab 3 | GDCD là "bias variable" trong KHXH | ✅ Top 5% KHXH cao hơn KHTN |
| Tab 4 | Nam Định dẫn đầu Toán nhiều năm liên tiếp | ✅ 4/5 năm (2021–2024) |
| Tab 5 | Sử–Địa có tương quan Pearson tăng dần | ✅ Tăng từ 0,58 lên 0,66 |

> **Lưu ý:** Nhóm bác bỏ 3/16 giả thuyết (H2, H7, H16) sau khi kiểm
> chứng thực tế với dữ liệu, thể hiện tính độc lập phân tích của nhóm
> so với đầu ra AI.

---

###  5.1.1.6 `dashboard-critic` — Phê bình thiết kế dashboard độc lập

**Mục tiêu:** Sau khi hoàn thiện mỗi tab, nhóm sử dụng helper này để
AI đóng vai trò "người phê bình độc lập" — đánh giá theo 6 tiêu chí:
tính rõ ràng, phù hợp loại biểu đồ, liên kết logic giữa các visual,
tương tác/điều hướng, sử dụng màu sắc, và chiều sâu phân tích.

**Các cải tiến nhóm áp dụng từ phản hồi AI:**

- Chuyển bản đồ từ dạng điểm sang Choropleth để thể hiện mật độ tốt
  hơn
- Thêm tính năng hover tooltip chi tiết trên tất cả biểu đồ Plotly
- Sắp xếp lại thứ tự Tab từ tổng quan → vi mô → không gian → thống kê
- Thay Pie Chart ban đầu bằng Donut + 100% Stacked Bar (Dual-chart
  design) cho Tab 1 phần cơ cấu khối thi

---

## 5.1.2 AI hỗ trợ lựa chọn loại biểu đồ phù hợp

Một trong những thách thức cốt lõi của trực quan hóa dữ liệu là lựa
chọn đúng loại biểu đồ cho từng bài toán phân tích. Nhóm sử dụng AI
như một cố vấn thiết kế, trình bày bài toán phân tích cụ thể và yêu
cầu AI đề xuất có luận chứng.

**Bảng quyết định biểu đồ được AI tư vấn và nhóm phê duyệt:**

| Bài toán phân tích | Biểu đồ AI đề xuất | Lý do | Nhóm chấp thuận |
|---|---|---|:---:|
| Quy mô thí sinh theo thời gian | Area Chart | Nhấn mạnh tích lũy diện tích, rõ hơn Line Chart | ✅ |
| Phân phối điểm từng môn | Histogram | Thể hiện hình dáng phân phối tần suất | ✅ |
| Mức độ phân hóa đề thi | Boxplot | Bộc lộ median, IQR và outlier đồng thời | ✅ |
| Phổ điểm nhiều năm | Multi-year Line Chart | So sánh trực tiếp hình dáng đường cong | ✅ |
| Phân bố điểm theo tỉnh | Choropleth Map | Mã hóa không gian địa lý bằng màu sắc | ✅ |
| Đóng góp môn trong tổ hợp | Radar Chart | Biểu diễn đa trục trong cùng không gian | ✅ |
| Đối chuẩn HN vs. HCM | Dumbbell Chart | Tối ưu cho so sánh cặp giá trị | ✅ |
| Phân hóa & độ khó đề thi | Quadrant Bubble Chart | Phân vùng 4 góc chiến lược, bubble = quy mô | ✅ |
| Cơ cấu khối thi tĩnh | Donut Chart | Tỷ trọng phần trăm trong một thời điểm | ✅ |
| Xu hướng cơ cấu nhiều năm | 100% Stacked Bar | Dàn trải tỷ trọng theo trục thời gian | ✅ |

Trong một số trường hợp, AI ban đầu đề xuất Scatter Plot cho bài toán
tương quan nhưng nhóm đã quyết định ưu tiên Correlation Heatmap (dựa
trên Pearson) để biểu diễn đồng thời toàn bộ 9×9 cặp môn học — quyết
định này phản ánh sự phán xét độc lập của nhóm vượt ra ngoài gợi ý
ban đầu của AI.

---

## 5.1.3 AI hỗ trợ thiết kế giao diện và hệ thống màu sắc

Nhóm sử dụng AI để xây dựng một hệ thống thiết kế thị giác (visual
design system) nhất quán xuyên suốt 5 tab, đảm bảo người dùng có trải
nghiệm liền mạch khi điều hướng giữa các phân hệ.

**Các quyết định thiết kế được AI tư vấn:**

- **Bảng màu chủ đạo:** AI đề xuất dải màu xanh đậm (navy blue) làm
  màu định danh thương hiệu cho toàn dashboard, kết hợp màu cam/vàng
  làm màu nhấn (accent) — tạo độ tương phản cao đảm bảo khả năng đọc
  cho người dùng khiếm thị màu sắc một phần.

- **Nguyên tắc màu có ý nghĩa (Semantic color encoding):**
  - Xanh đậm → nhóm KHTN
  - Cam/Vàng → nhóm KHXH
  - Đỏ/Cam nóng → vùng điểm cao, mật độ cao trên Choropleth
  - Xanh nhạt → vùng điểm thấp, cold spots

- **Cấu trúc layout:** AI gợi ý sử dụng hệ thống 3 cột metric KPI ở
  hàng đầu mỗi tab (hiển thị tổng thí sinh, điểm trung bình, tỷ lệ
  key) trước khi dẫn vào các biểu đồ chi tiết bên dưới, theo mô hình
  "Overview → Detail" chuẩn Information Design.

- **Typography và nhãn:** Đề xuất rút gọn nhãn dài (ví dụ: "Giáo dục
  công dân" → "GDCD") trên trục biểu đồ để tránh chồng chéo, đặc
  biệt trong Horizontal Bar Chart có nhiều danh mục.

---

## 5.1.4 AI hỗ trợ sinh mã nguồn Streamlit và Plotly

AI đóng vai trò quan trọng trong việc rút ngắn thời gian phát triển mã
nguồn, đặc biệt với các thành phần kỹ thuật phức tạp như Choropleth
Map tích hợp GeoJSON hay Quadrant Chart kết hợp Bubble.

**Quy trình sinh mã chuẩn của nhóm:**

```
1. Nhóm tự viết pseudocode / logic thuật toán
2. Mô tả yêu cầu kỹ thuật cho AI (input data format,
   output chart type, filter interaction)
3. AI sinh mã Streamlit + Plotly hoàn chỉnh
4. Nhóm review, chỉnh sửa và kiểm thử thực tế với dữ liệu
5. Ghi nhận diff (trước/sau chỉnh sửa) vào ai-trace.md
```

**Các module mã nguồn AI hỗ trợ sinh và nhóm hiệu chỉnh:**

| Module | Nội dung AI sinh | Chỉnh sửa của nhóm |
|---|---|---|
| Choropleth Map | Vẽ bản đồ `px.choropleth_mapbox` với GeoJSON | Đồng bộ key tên tỉnh, thêm hover template tùy chỉnh |
| Correlation Heatmap | Ma trận Pearson `go.Heatmap` | Ẩn tam giác trên, thêm annotation số liệu trong ô |
| Vision Chatbot | Luồng gửi ảnh base64 lên Gemini API | Thêm fallback khi API timeout, giới hạn context window |
| Boxplot đa năm | `go.Box` overlay nhiều năm | Thêm color map theo năm, toggle legend |
| Radar Chart | `go.Scatterpolar` cho Top 5% vs. Trung bình | Chuẩn hóa trục về cùng scale 0–10 |
| 100% Stacked Bar | `px.bar` với `barnorm="percent"` | Thêm data label phần trăm trong cột, format tooltip |

---

## 5.1.5 AI hỗ trợ phân tích và diễn giải dữ liệu

Ngoài vai trò kỹ thuật, AI còn được sử dụng như một công cụ phân tích
thứ cấp — giúp nhóm kiểm tra lại các nhận định ban đầu và mở rộng
chiều sâu diễn giải.

**Quy trình phân tích có AI hỗ trợ:**

1. Nhóm tự quan sát và ghi nhận nhận xét sơ bộ từ biểu đồ
2. Mô tả hình dáng biểu đồ cho AI (dưới dạng văn bản hoặc hình ảnh)
   và yêu cầu diễn giải thống kê
3. Đối chiếu diễn giải của AI với nhận xét của nhóm — ghi nhận điểm
   đồng thuận và bất đồng
4. Nhóm đưa ra kết luận cuối cùng dựa trên cả hai nguồn

**Ví dụ minh họa — Phân tích phổ điểm Ngoại ngữ 2021:**

| Giai đoạn | Nội dung |
|---|---|
| Nhóm quan sát | Biểu đồ có hình dạng bất thường, không phải hình chuông |
| AI diễn giải | Hiện tượng Bimodal distribution, phản ánh phân hóa năng lực giữa thí sinh thành thị và nông thôn |
| Nhóm kiểm chứng | Tách dữ liệu theo địa phương, xác nhận đô thị lớn tạo đỉnh cao, tỉnh nhỏ tạo đỉnh thấp |
| Kết luận cuối | Bổ sung phân tích chiều sâu về bất bình đẳng giáo dục ngoại ngữ |

---

## 5.1.6 AI hỗ trợ kiểm tra logic và debug

Trong quá trình phát triển, nhóm gặp một số lỗi logic trong tính toán
chỉ số phức tạp. AI được sử dụng như một công cụ debug thứ cấp, không
thay thế cho quá trình test thủ công của nhóm.

**Các vấn đề logic được AI hỗ trợ giải quyết:**

| Lỗi | Nguyên nhân (AI chẩn đoán) | Cách khắc phục |
|---|---|---|
| Top 5% trả cùng giá trị mọi năm | Dùng `quantile(0.95)` trên toàn tập thay vì `groupby(năm)` | Thêm `groupby(['nam', 'khoi'])` trước khi gọi quantile |
| Correlation matrix trả về NaN | Thí sinh không thi đồng thời KHTN lẫn KHXH → cột toàn NaN | Bổ sung `min_periods=100` vào `df.corr()` |
| Choropleth thiếu 4 tỉnh | Tên tỉnh trong GeoJSON lệch ký tự so với DataFrame | Chuẩn hóa tên bằng `unidecode` + mapping thủ công |
| Chatbot lỗi encode ảnh | `st.pyplot` trả buffer không tương thích base64 | Chuyển sang `plotly.io.to_image(fig, format='png')` |

Mỗi lỗi được khắc phục đều đi qua quy trình: nhóm hiểu rõ nguyên nhân
gốc → chỉnh sửa code → kiểm thử lại với dữ liệu thực — không áp dụng
bản sửa lỗi của AI một cách mù quáng.

---

## 5.1.7 Quy trình lưu vết AI — file `ai-trace.md`

Theo yêu cầu của đồ án, toàn bộ quá trình tương tác với AI được ghi
nhận đầy đủ trong file `ai-trace.md` theo cấu trúc chuẩn hóa:

```
Session [N] — [dd/mm/yyyy]
├── Human-first analysis (bắt buộc, 2–5 dòng nhóm tự phân tích)
├── Task A
│   ├── Helper đã dùng
│   ├── Prompt gốc 
│   ├── AI output (tóm tắt + file)
│   ├── Script AI sinh ra
│   ├── Script sau chỉnh sửa của nhóm
│   ├── Cách kiểm chứng
│   ├── Bằng chứng (ảnh/bảng/output)
│   └── Rủi ro/giới hạn còn lại
└── Task B ...
```
