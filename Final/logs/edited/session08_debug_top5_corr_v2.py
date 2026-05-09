# Debug Fix: Top 5% quantile + Correlation NaN — Human-edited version
# Session 08 (08/05/2026) | Edited by: Nguyễn Đỗ Bảo
# Changes from AI version: added p5/p50 for range chart, increased min_periods
#   to 100 (AI used 50), added NaN pair diagnostic print

import pandas as pd
import numpy as np

SCORE_COLS = ['toan', 'ngu_van', 'ngoai_ngu', 'vat_ly', 'hoa_hoc',
              'sinh_hoc', 'lich_su', 'dia_ly', 'gdcd']

# Sửa lỗi 1 — thêm nam vào groupby, tính thêm p5 và p50 cho range chart
df_percentiles = (
    df[df["khoi"].notna()]
    .groupby(["khoi", "nam"])["tong_diem"]
    .agg(
        p5=lambda x: x.quantile(0.05),
        p50=lambda x: x.quantile(0.50),
        p95=lambda x: x.quantile(0.95),
        mean="mean"
    )
    .reset_index()
)

# Sửa lỗi 2 — tăng min_periods lên 100 (không phải 50 của AI)
corr = df[SCORE_COLS].corr(min_periods=100)
nan_pairs = [(c1, c2) for c1 in SCORE_COLS for c2 in SCORE_COLS
             if pd.isna(corr.loc[c1, c2]) and c1 != c2]
if nan_pairs:
    print(f"[WARN] {len(nan_pairs)} cặp NaN: {nan_pairs[:3]}...")
