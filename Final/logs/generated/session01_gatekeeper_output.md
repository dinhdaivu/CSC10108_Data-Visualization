# Gatekeeper Output — Session 01 (10/04/2026)

**Prompt received at:** 09:14:22
**Helper:** gatekeeper
**Responded by:** Claude (claude-sonnet-4-6)

---

## 1) Input snapshot

- Dataset: Điểm thi THPT Quốc gia Việt Nam 2020–2024
- Số dòng ước tính: ~4,6 triệu (ghép từ 5 file CSV)
- Số cột: 11 (sbd, toan, ngu_van, ngoai_ngu, vat_ly, hoa_hoc, sinh_hoc, lich_su, dia_ly, gdcd, nam)
- Nguồn: Kaggle — tổng hợp từ công bố chính thức Bộ GD&ĐT
- Tỷ lệ Việt Nam: 100% (toàn bộ là thí sinh VN)

---

## 2) Core analysis — PASS/FAIL

| Tiêu chí | Yêu cầu | Giá trị thực tế | Trạng thái |
|---|---|---|---|
| Số dòng | ≥ 2.000 | ~4.600.000 | ✅ PASS |
| Số biến độc lập | ≥ 7 | 9 môn + ma_vung + nam = 11 | ✅ PASS |
| Tỷ lệ Việt Nam | > 50% | 100% | ✅ PASS |
| Dữ liệu dạng bảng | Có | CSV tabular | ✅ PASS |
| Nguồn minh bạch | Có thể trích dẫn | Kaggle (cần ghi link + ngày tải) | ⚠️ CONDITIONAL |
| Dữ liệu thật | Có | Dữ liệu thi cử chính thức | ✅ PASS |

**Thông tin cần bổ sung:**
1. Link Kaggle đầy đủ (tên dataset + URL)
2. Ngày tải file (để ghi trong báo cáo)
3. Tên người upload dataset (để trích dẫn)

---

## 3) Priority actions

1. Ghi rõ link Kaggle và ngày tải vào phần nguồn dữ liệu của báo cáo
2. Chạy script kiểm tra `len(df)`, `df.columns`, `df.duplicated().sum()` để xác nhận số liệu
3. Kiểm tra tỷ lệ missing values theo từng cột (thí sinh không thi một số môn là bình thường)
4. Xác nhận kiểu dữ liệu các cột điểm (có thể là object do giá trị rỗng)
5. Lưu MD5 hash của các file CSV để đảm bảo tính toàn vẹn dữ liệu

---

## 4) Manual verification checklist

- [ ] Chạy `df.info()` và đối chiếu số dòng với bảng trên
- [ ] Kiểm tra `df['sbd'].nunique()` — nên gần bằng số dòng (unique per year)
- [ ] Xác nhận không có cột điểm âm hoặc > 10
- [ ] So sánh tổng thí sinh với thông tin công bố chính thức của Bộ GD&ĐT

---

## 5) Block dán vào `ai-trace.md`

```
- Helper: gatekeeper
- Kết quả: PASS tất cả tiêu chí bắt buộc
- Cần bổ sung: link Kaggle + ngày tải vào báo cáo
- File output: logs/generated/session01_gatekeeper_output.md
```
