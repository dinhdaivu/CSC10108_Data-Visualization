# Data Cleaning Pipeline — Human-edited version
# Session 04 (26/04/2026) | Edited by: Nguyễn Thanh Owen
# Changes from AI version: correct data paths, add NAME_FIX mapping,
#   exclude invalid ma_vung codes 00/64, explicit utf-8 for JSON

import pandas as pd
import glob, os, json
from unidecode import unidecode

SCORE_COLS = ['toan', 'ngu_van', 'ngoai_ngu', 'vat_ly', 'hoa_hoc',
              'sinh_hoc', 'lich_su', 'dia_ly', 'gdcd']

NAME_FIX = {
    "Bà Rịa - Vũng Tàu": "Ba Ria - Vung Tau",
    "Thừa Thiên Huế":     "Thua Thien Hue",
    "Đắk Lắk":            "Dak Lak",
    "Đắk Nông":           "Dak Nong",
    "TP Hồ Chí Minh":     "Ho Chi Minh City",
    "Hà Nội":             "Hanoi",
}
EXCLUDE_CODES = {"00", "64"}  # Hoàng Sa, Trường Sa — không có trong GeoJSON

dfs = []
for f in sorted(glob.glob("THPT_Dashboard/data/raw/thpt*.csv")):
    year = int(os.path.basename(f).replace("thpt", "").replace(".csv", ""))
    df = pd.read_csv(f, dtype={"sbd": str})
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    df["nam"] = year
    dfs.append(df)

combined = pd.concat(dfs, ignore_index=True)
combined["ma_vung"] = combined["sbd"].str[:2]
combined = combined[~combined["ma_vung"].isin(EXCLUDE_CODES)]

mavung = pd.read_csv("THPT_Dashboard/data/mavung.csv", dtype={"ma_vung": str})
combined = combined.merge(mavung, on="ma_vung", how="left")

combined = combined.dropna(subset=SCORE_COLS, how="all")

for col in SCORE_COLS:
    combined[col] = pd.to_numeric(combined[col], errors="coerce")

combined["ten_tinh"] = combined["ten_tinh"].replace(NAME_FIX)

with open("THPT_Dashboard/data/vn_geo.json", encoding="utf-8") as f:
    geo = json.load(f)
geo_names = {feat["properties"]["NAME_1"] for feat in geo["features"]}
unmatched = set(combined["ten_tinh"].dropna().unique()) - geo_names
if unmatched:
    print(f"[WARN] Tỉnh chưa match GeoJSON: {unmatched}")

combined.to_parquet("THPT_Dashboard/data/cleaned_thpt.parquet", index=False)
print(f"Done. Lưu {len(combined):,} dòng → cleaned_thpt.parquet")
