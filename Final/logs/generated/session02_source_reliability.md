# Source Reliability Assessment — Session 02 (17/04/2026)

**Prompt received at:** 09:31:07
**Helper:** source-reliability
**Responded by:** Claude (claude-sonnet-4-6)

---

## 1) Input snapshot

- Nguồn 1: Kaggle — điểm thi THPT 2020–2024 (cộng đồng tổng hợp từ Bộ GD&ĐT)
- Nguồn 2: SimpleMaps — GeoJSON ranh giới 63 tỉnh thành Việt Nam
- Nguồn 3: mavung.csv — tự tổng hợp từ danh mục hành chính Bộ Nội vụ

---

## 2) Đánh giá từng nguồn

### Nguồn 1 — Kaggle THPT 2020–2024

**Đánh giá: RELIABLE (có điều kiện)**

| Tiêu chí | Nhận xét |
|---|---|
| Tính xác thực | Dữ liệu gốc từ Bộ GD&ĐT công bố hàng năm trên website chính thức |
| Tính minh bạch | Kaggle listing ghi rõ nguồn gốc, có discussion thread kiểm chứng |
| Rủi ro chính | Version drift — uploader có thể cập nhật file mà không thông báo |
| Khuyến nghị | Lưu MD5 hash file tại thời điểm tải, ghi rõ ngày tải trong báo cáo |

### Nguồn 2 — SimpleMaps GeoJSON

**Đánh giá: RELIABLE**

| Tiêu chí | Nhận xét |
|---|---|
| Uy tín nhà cung cấp | SimpleMaps là nhà cung cấp GIS dữ liệu chuyên nghiệp, được dùng trong nhiều dự án quốc tế |
| Tính cập nhật | Dữ liệu phản ánh ranh giới hành chính hiện hành (sau sáp nhập 2008) |
| Rủi ro chính | Tên tỉnh trong GeoJSON dùng ký tự ASCII — cần mapping với tên tiếng Việt trong dataset |
| Khuyến nghị | Lưu file local, không gọi URL runtime. Pin version bằng MD5 hash |

### Nguồn 3 — mavung.csv (tự tổng hợp)

**Đánh giá: CONDITIONAL RELIABLE**

| Tiêu chí | Nhận xét |
|---|---|
| Tính xác thực | Dựa trên danh mục hành chính Bộ Nội vụ — nguồn gốc đáng tin cậy |
| Rủi ro chính | Quá trình nhập thủ công có thể có lỗi chính tả hoặc thiếu mã vùng đặc biệt |
| Khuyến nghị | Đối chiếu chéo với mã vùng từ sbd trong dataset để xác nhận coverage 100% |

---

## 3) Priority actions

1. Ghi link Kaggle đầy đủ + ngày tải 08/04/2026 vào báo cáo
2. Chạy script hash tất cả file nguồn → lưu vào `logs/source_hashes.txt`
3. Đóng băng `vn_geo.json` local, không import từ CDN
4. Kiểm tra mavung.csv cover đủ 63 tỉnh + các mã đặc biệt
5. Thêm mục "Data Limitations" vào báo cáo ghi rõ hạn chế của dữ liệu Kaggle

---

## 4) Manual verification checklist

- [ ] Đối chiếu tổng số thí sinh 2024 với công bố chính thức Bộ GD&ĐT (khoảng 1,07 triệu)
- [ ] Kiểm tra coverage mã vùng: `combined['ma_vung'].nunique()` phải = 63 (+ mã đặc biệt)
- [ ] Chạy `file_hash()` trên tất cả 7 file nguồn và lưu kết quả

---

## 5) Block dán vào `ai-trace.md`

```
- Helper: source-reliability
- Kết quả: Kaggle RELIABLE (cần hash), SimpleMaps RELIABLE, mavung.csv CONDITIONAL
- Hành động: script hash 7 file nguồn, thêm Data Limitations vào báo cáo
- File output: logs/generated/session02_source_reliability.md
```
