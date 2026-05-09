# Data Quality Check Script — Human-edited version
# Session 03 (23/04/2026) | Edited by: Lê Nguyên Thảo
# Changes from AI version: section headers, keep=False for duplicate, yearly stats 3 cols

import pandas as pd

SCORE_COLS = ['toan', 'ngu_van', 'ngoai_ngu', 'vat_ly',
              'hoa_hoc', 'sinh_hoc', 'lich_su', 'dia_ly', 'gdcd']

print("=" * 55)
print("1. TỶ LỆ MISSING THEO CỘT (%)")
print("=" * 55)
missing_pct = combined[SCORE_COLS].isnull().mean().mul(100).round(2)
print(missing_pct.to_string())

print("\n" + "=" * 55)
print("2. DÒNG CÓ TOÀN BỘ ĐIỂM LÀ NaN")
print("=" * 55)
all_nan_mask = combined[SCORE_COLS].isnull().all(axis=1)
print(f"Số dòng: {all_nan_mask.sum():,}  ({all_nan_mask.mean()*100:.2f}%)")

print("\n" + "=" * 55)
print("3. DUPLICATE THEO (sbd, nam)")
print("=" * 55)
dup_mask = combined.duplicated(subset=['sbd', 'nam'], keep=False)
print(f"Số dòng trùng: {dup_mask.sum():,}")

print("\n" + "=" * 55)
print("4. THỐNG KÊ THEO NĂM")
print("=" * 55)
yearly_stats = combined.groupby('nam').agg(
    total=('sbd', 'count'),
    miss_toan=('toan', lambda x: f"{x.isnull().mean()*100:.1f}%"),
    miss_ngoai_ngu=('ngoai_ngu', lambda x: f"{x.isnull().mean()*100:.1f}%"),
    miss_lich_su=('lich_su', lambda x: f"{x.isnull().mean()*100:.1f}%"),
).reset_index()
print(yearly_stats.to_string(index=False))
