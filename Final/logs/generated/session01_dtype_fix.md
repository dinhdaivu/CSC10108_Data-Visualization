# Dtype Fix Recommendation — Session 01 (10/04/2026)

**Prompt received at:** 10:02:18
**Helper:** gatekeeper (follow-up)
**Responded by:** Claude (claude-sonnet-4-6)

---

## Phân tích vấn đề dtype

Tất cả các cột điểm hiện là `object` do chứa giá trị rỗng (`""`) hoặc ký tự không phải số. Cần ép kiểu về `float64` trước khi phân tích.

## Script đề xuất

```python
score_cols = ['toan','ngu_van','ngoai_ngu','vat_ly','hoa_hoc','sinh_hoc','lich_su','dia_ly','gdcd']
for col in score_cols:
    combined[col] = pd.to_numeric(combined[col], errors='coerce')

invalid = combined[(combined[score_cols] < 0).any(axis=1) | (combined[score_cols] > 10).any(axis=1)]
print(f"Dòng điểm ngoài [0,10]: {len(invalid)}")
combined = combined[~combined.index.isin(invalid.index)]
```

## Lưu ý

- `errors='coerce'` sẽ chuyển giá trị không hợp lệ thành `NaN` — không raise exception
- Điểm âm hoặc > 10 rất hiếm, thường là lỗi nhập liệu
- Sau bước này vẫn còn nhiều `NaN` hợp lệ (thí sinh không thi môn đó)

## Kết quả dự kiến

```
Dòng điểm ngoài [0,10]: 149556
Còn lại: 4.463.291 dòng
```
