# Source File Hash Check — Human-edited version
# Session 02 (17/04/2026) | Edited by: Nguyễn Thanh Owen
# Changes from AI version: all 7 files, file existence check, size in KB

import hashlib, os

SOURCE_FILES = {
    "thpt2020.csv": "THPT_Dashboard/data/raw/thpt2020.csv",
    "thpt2021.csv": "THPT_Dashboard/data/raw/thpt2021.csv",
    "thpt2022.csv": "THPT_Dashboard/data/raw/thpt2022.csv",
    "thpt2023.csv": "THPT_Dashboard/data/raw/thpt2023.csv",
    "thpt2024.csv": "THPT_Dashboard/data/raw/thpt2024.csv",
    "vn_geo.json":  "THPT_Dashboard/data/vn_geo.json",
    "mavung.csv":   "THPT_Dashboard/data/mavung.csv",
}

print(f"{'FILE':<20} {'MD5 HASH':<35} {'SIZE (KB)':>10}")
print("-" * 70)
for name, path in SOURCE_FILES.items():
    if os.path.exists(path):
        with open(path, 'rb') as f:
            h = hashlib.md5(f.read()).hexdigest()
        size_kb = os.path.getsize(path) / 1024
        print(f"{name:<20} {h:<35} {size_kb:>10.1f}")
    else:
        print(f"{name:<20} {'FILE NOT FOUND':<35} {'N/A':>10}")

print("-" * 70)
print("Saved to: logs/source_hashes.txt")
print("Date:", __import__('datetime').datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
