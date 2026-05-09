# Run this script then screenshot the terminal output
# Screenshot 1 → save as session01_combined_info.png
# Screenshot 2 → save as session01_dtype_check.png
#
# How to run:
#   cd c:\Users\Vu\schoolProject\CSC100800\CSC10080\Final
#   python logs/evidence/capture_session01.py

import pandas as pd
import glob
import os

DATA_DIR = "THPT_Dashboard/data/raw"

# Normalize all column name variants to one standard name
COL_MAP = {
    # SBD
    "SBD": "sbd",
    # Toán
    "Toan": "toan",
    # Ngữ Văn
    "NguVan": "ngu_van", "Ngu_Van": "ngu_van",
    # Vật lý
    "VatLy": "vat_ly", "Vat_Ly": "vat_ly", "vat_li": "vat_ly",
    # Hóa học
    "HoaHoc": "hoa_hoc", "Hoa_Hoc": "hoa_hoc",
    # Sinh học
    "SinhHoc": "sinh_hoc", "Sinh_Hoc": "sinh_hoc",
    # Lịch sử
    "LichSu": "lich_su", "Lich_Su": "lich_su",
    # Địa lý
    "DiaLy": "dia_ly", "Dia_Ly": "dia_ly", "dia_li": "dia_ly",
    # GDCD
    "GDCD": "gdcd",
    # Ngoại ngữ
    "NgoaiNgu": "ngoai_ngu", "Ngoai_Ngu": "ngoai_ngu",
    # Mã môn ngoại ngữ
    "MaMonNgoaiNgu": "ma_ngoai_ngu",
    # Cụm thi
    "Cum_Thi": "cum_thi",
}

SCORE_COLS = ['toan', 'ngu_van', 'ngoai_ngu', 'vat_ly',
              'hoa_hoc', 'sinh_hoc', 'lich_su', 'dia_ly', 'gdcd']

# ── Load & normalize each file ───────────────────────────────────────────────
files = sorted(glob.glob(os.path.join(DATA_DIR, "thpt*.csv")))
dfs = []
for f in files:
    df = pd.read_csv(f, dtype={"sbd": str, "SBD": str})
    df.rename(columns=COL_MAP, inplace=True)
    year = int(os.path.basename(f).replace("thpt", "").replace(".csv", ""))
    df["nam"] = year
    # keep only standard columns that exist in this file
    keep = ["sbd", "nam"] + [c for c in SCORE_COLS if c in df.columns]
    dfs.append(df[keep])

combined = pd.concat(dfs, ignore_index=True)

# ════════════════════════════════════════════════════════════════════════════
# SCREENSHOT 1 — session01_combined_info.png
# ════════════════════════════════════════════════════════════════════════════
present = [c for c in SCORE_COLS if c in combined.columns]

print("=" * 55)
print("DATASET OVERVIEW (after column normalization)")
print("=" * 55)
print(f"Tổng dòng          : {len(combined):,}")
print(f"Số cột chuẩn hóa   : {len(combined.columns)}")
print(f"Các cột            : {list(combined.columns)}")
print(f"Dòng trùng (sbd+nam): {combined.duplicated(subset=['sbd','nam']).sum():,}")
print()
print("Missing theo cột điểm:")
print(combined[present].isnull().sum().to_string())
print("=" * 55)

# ── TAKE SCREENSHOT 1 HERE ───────────────────────────────────────────────────
input("\n>>> Screenshot 1 done? Press Enter to continue to Screenshot 2...\n")

# ── Cast score columns ───────────────────────────────────────────────────────
for col in present:
    combined[col] = pd.to_numeric(combined[col], errors="coerce")

mask_invalid = (
    (combined[present] < 0).any(axis=1) |
    (combined[present] > 10).any(axis=1)
)
combined = combined[~mask_invalid].reset_index(drop=True)

# ════════════════════════════════════════════════════════════════════════════
# SCREENSHOT 2 — session01_dtype_check.png
# ════════════════════════════════════════════════════════════════════════════
print("=" * 55)
print("DTYPE & RANGE CHECK (after cast)")
print("=" * 55)
print(f"Dòng còn lại sau lọc: {len(combined):,}")
print()
print("Kiểu dữ liệu:")
print(combined[present].dtypes.to_string())
print()
print("Min / Max từng cột điểm:")
print(combined[present].agg(['min', 'max']).to_string())
print("=" * 55)

# ── TAKE SCREENSHOT 2 HERE ───────────────────────────────────────────────────
print("\nDone.")
