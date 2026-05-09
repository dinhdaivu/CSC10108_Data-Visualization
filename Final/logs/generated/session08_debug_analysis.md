# Debug Analysis — Lỗi Top 5% & NaN Heatmap — Session 08 (08/05/2026)

**Prompt received at:** 09:14:22
**Responded by:** Claude (claude-sonnet-4-6)

---

## Lỗi 1: Top 5% trả cùng giá trị mọi năm

### Chẩn đoán

```python
# Code lỗi:
df_top5 = df.groupby('khoi')['tong_diem'].quantile(0.95)
```

**Nguyên nhân gốc:** `groupby('khoi')` chỉ nhóm theo khối thi, không nhóm theo năm. Kết quả là `quantile(0.95)` tính trên toàn bộ 5 năm gộp lại cho mỗi khối — nên giá trị giống nhau khi filter theo từng năm (vì DataFrame không thay đổi).

### Sửa chữa đề xuất

```python
# Phiên bản sửa:
df_top5 = df.groupby(['khoi', 'nam'])['tong_diem'].quantile(0.95).reset_index()
df_top5.columns = ['khoi', 'nam', 'p95']
```

**Giải thích:** Thêm `'nam'` vào groupby key — quantile tính riêng cho mỗi cặp (khối, năm).

---

## Lỗi 2: `corr()` trả NaN ở một số cặp KHTN-KHXH

### Chẩn đoán

**Nguyên nhân gốc:** Thí sinh KHTN chỉ thi `vat_ly, hoa_hoc, sinh_hoc` — các cột KHXH (`lich_su, dia_ly, gdcd`) của họ là `NaN`. Ngược lại, thí sinh KHXH có các cột KHTN là `NaN`. Khi tính `corr()` giữa một cột KHTN và một cột KHXH, Pandas yêu cầu cả hai cột phải có giá trị không-NaN trên cùng một dòng → số lượng cặp hợp lệ rất ít → `corr()` trả `NaN` nếu không đủ data points.

Mặc định `min_periods=1` — chỉ cần 1 dòng có cả 2 giá trị là tính được. Nhưng nếu không có dòng nào thi cả KHTN lẫn KHXH, kết quả là NaN.

### Sửa chữa đề xuất

```python
# Phiên bản sửa:
corr = df[SCORE_COLS].corr(min_periods=50)
```

**Giải thích:** `min_periods=50` yêu cầu ít nhất 50 dòng hợp lệ để tính correlation. Nếu ít hơn, trả NaN (chấp nhận được) thay vì tính từ quá ít dữ liệu.

**Ghi chú từ nhóm:** Team quyết định dùng `min_periods=100` (chặt hơn đề xuất AI = 50) để đảm bảo tính đáng tin cậy thống kê cao hơn.

---

## Tóm tắt

| Lỗi | Nguyên nhân | Fix |
|---|---|---|
| Top 5% giống nhau mọi năm | Thiếu `'nam'` trong groupby key | `groupby(['khoi','nam'])` |
| Heatmap NaN ở KHTN-KHXH pairs | Không có thí sinh thi đồng thời cả 2 nhóm | `corr(min_periods=100)` |
