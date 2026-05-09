# Debug Analysis — Choropleth thiếu tỉnh & Chatbot encode lỗi — Session 08 (08/05/2026)

**Prompt received at:** 10:51:39
**Responded by:** Claude (claude-sonnet-4-6)

---

## Lỗi 3: Choropleth thiếu màu 4 tỉnh

### Tỉnh bị ảnh hưởng
- "Bà Rịa - Vũng Tàu"
- "Thừa Thiên Huế"
- "Đắk Lắk"
- "Đắk Nông"

### Chẩn đoán

**Nguyên nhân gốc:** `px.choropleth_mapbox` dùng `locations='ten_tinh'` để khớp với `featureidkey='properties.NAME_1'` trong GeoJSON. GeoJSON từ SimpleMaps lưu tên tỉnh dưới dạng ASCII không dấu (ví dụ: "Ba Ria - Vung Tau"), nhưng DataFrame dùng tên tiếng Việt đầy đủ ("Bà Rịa - Vũng Tàu"). Khi `locations` không tìm thấy key tương ứng trong GeoJSON features, tỉnh đó không được tô màu.

### Sửa chữa đề xuất

```python
# Cách 1: Dùng unidecode để chuẩn hóa tự động
from unidecode import unidecode
df['ten_tinh_norm'] = df['ten_tinh'].apply(unidecode)
geo_names_norm = {unidecode(feat['properties']['NAME_1']): feat['properties']['NAME_1']
                  for feat in geojson['features']}
df['ten_tinh_geo'] = df['ten_tinh_norm'].map(geo_names_norm)
```

**Ghi chú từ nhóm:** Team quyết định dùng mapping thủ công (`NAME_FIX` dict) thay vì `unidecode` tự động — lý do: `unidecode` có thể dịch sai tên riêng trong một số trường hợp (ví dụ: "Hòa Bình" → "Hoa Binh" khớp, nhưng "TP Hồ Chí Minh" → "TP Ho Chi Minh" có thể không khớp với "Ho Chi Minh City"). Mapping thủ công chính xác hơn cho 63 tỉnh cố định.

---

## Lỗi 4: Chatbot gửi ảnh Plotly lên Gemini bị lỗi "Invalid image data"

### Chẩn đoán

**Nguyên nhân gốc:** Code cũ dùng `st.pyplot()` để render biểu đồ và lấy buffer. Tuy nhiên `st.pyplot()` dành cho Matplotlib, không phải Plotly. Khi dùng với Plotly figure, buffer trả về không đúng định dạng PNG — Gemini API từ chối nhận do `Content-Type` không hợp lệ hoặc byte sequence bị corrupt.

### Sửa chữa đề xuất

```python
import base64, io
buf = io.BytesIO()
fig.write_image(buf, format='png')
img_b64 = base64.b64encode(buf.getvalue()).decode()
```

**Ghi chú từ nhóm:** Team dùng `plotly.io.to_image(fig, format='png')` thay vì `fig.write_image(buf)` — lý do: `pio.to_image` trả bytes trực tiếp (không cần BytesIO buffer), code gọn hơn và không có nguy cơ buffer position issue. Thêm `scale=2` để ảnh gửi Gemini có độ phân giải cao hơn (2× standard), giúp Gemini đọc được chi tiết biểu đồ tốt hơn.

---

## Tóm tắt

| Lỗi | Nguyên nhân | Fix |
|---|---|---|
| 4 tỉnh không có màu trên bản đồ | Tên tỉnh tiếng Việt không khớp key ASCII trong GeoJSON | `TINH_MAP` dict thủ công 6 tỉnh bị lệch tên |
| Chatbot "Invalid image data" | `st.pyplot()` không tương thích với Plotly figure | `pio.to_image(fig, format='png', scale=2)` |

---

## Trạng thái sau sửa

- Choropleth: 63/63 tỉnh có màu ✅
- Chatbot: gửi ảnh thành công, Gemini phân tích và trả lời ✅
