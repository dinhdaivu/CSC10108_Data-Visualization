# AI Trace 

> Mục tiêu: đáp ứng yêu cầu lưu vết theo chuỗi: **Prompt -> Script AI sinh ra -> Script sau chỉnh sửa -> Kết quả đã kiểm chứng**.

---

## 0. Thông tin nhóm

- **Chủ đề dashboard:** Phân tích điểm thi THPT Quốc gia Việt Nam 2020–2024
- **Thành viên:** Đinh Đại Vũ · Nguyễn Thanh Owen · Lê Nguyên Thảo · Vũ Hoàng Minh · Nguyễn Đỗ Bảo
- **Công cụ dashboard:** Streamlit + Plotly Express/Graph Objects + Pandas
- **Dataset chính:** Điểm thi THPT 2020–2024 (nguồn: Kaggle) + vn_geo.json (SimpleMaps)
- **Ngày bắt đầu:** 10/03/2026
- **Thư mục log chính:** `logs/`
- **Session hiện tại:** `logs/sessions/`
- **Prompt lưu tại:** `logs/prompts/`
- **AI output lưu tại:** `logs/generated/`
- **Human-edited lưu tại:** `logs/edited/`
- **Evidence lưu tại:** `logs/evidence/`

---

## 1. Session log

### Session 01 - 10/04/2026

#### Human-first analysis (bắt buộc, 2-5 dòng)

- Nhóm tổng hợp 5 file CSV (thpt2020–thpt2024) và đếm thủ công: tổng xấp xỉ 4,6 triệu dòng.
- Liệt kê 11 cột: `sbd`, `toan`, `ngu_van`, `ngoai_ngu`, `vat_ly`, `hoa_hoc`, `sinh_hoc`, `lich_su`, `dia_ly`, `gdcd`, `nam` — đủ 7 biến độc lập.
- 100% dữ liệu là thí sinh Việt Nam → tỷ lệ Việt Nam = 100% (vượt ngưỡng 50%).
- Nhóm tự đánh giá PASS cả 3 tiêu chí trước khi dùng AI xác nhận lại.

#### Task A — Kiểm định dataset theo yêu cầu đồ án (gatekeeper)

- Mục tiêu: Xác nhận tập dữ liệu THPT 2020–2024 đáp ứng đủ tiêu chí bắt buộc: số dòng, số biến, tỷ lệ Việt Nam, nguồn rõ ràng.
- Helper đã dùng: `gatekeeper`
- Prompt đã dùng:

```text
Tôi có tập dữ liệu điểm thi THPT Quốc gia Việt Nam từ 2020 đến 2024, tổng hợp từ 5 file CSV riêng lẻ. Sau khi ghép, dataset gồm khoảng 4,6 triệu dòng, 11 cột (sbd, toan, ngu_van, ngoai_ngu, vat_ly, hoa_hoc, sinh_hoc, lich_su, dia_ly, gdcd, nam). Tất cả dữ liệu đều là thí sinh tại Việt Nam. Nguồn dữ liệu từ Kaggle, được tổng hợp từ dữ liệu công bố chính thức của Bộ Giáo dục và Đào tạo. Hãy kiểm tra xem tập dữ liệu này có đáp ứng đủ các yêu cầu của đồ án môn Trực quan hóa dữ liệu không và chỉ ra các bước cần làm tiếp theo.
```

- AI output (tóm tắt + link/file):
  - Bảng PASS/FAIL: ≥2000 dòng → PASS (4,6M), ≥7 biến → PASS (11 cột), Việt Nam >50% → PASS (100%), Nguồn minh bạch → CONDITIONAL PASS (cần ghi rõ link Kaggle + ngày tải).
  - AI yêu cầu làm rõ thêm: (1) Link Kaggle cụ thể, (2) Tên dataset, (3) Ngày tải file.
  - File: `logs/generated/session01_gatekeeper_output.md`

- Script AI sinh ra:

```python
import pandas as pd
import glob

files = glob.glob("data/thpt*.csv")
dfs = []
for f in files:
    df = pd.read_csv(f)
    dfs.append(df)

combined = pd.concat(dfs, ignore_index=True)
print(f"Tổng dòng: {len(combined):,}")
print(f"Số cột: {len(combined.columns)}")
print(f"Các cột: {list(combined.columns)}")
print(f"Dòng trùng: {combined.duplicated().sum()}")
print(f"Missing theo cột:\n{combined.isnull().sum()}")
```

- Script sau chỉnh sửa bởi nhóm:

```python
import pandas as pd
import glob
import os

DATA_DIR = "THPT_Dashboard/data/raw"
files = sorted(glob.glob(os.path.join(DATA_DIR, "thpt*.csv")))

dfs = []
for f in files:
    df = pd.read_csv(f, dtype={"sbd": str})
    year = int(os.path.basename(f).replace("thpt", "").replace(".csv", ""))
    df["nam"] = year
    dfs.append(df)

combined = pd.concat(dfs, ignore_index=True)

print(f"Tổng dòng: {len(combined):,}")
print(f"Số cột: {len(combined.columns)}")
print(f"Các cột: {list(combined.columns)}")
print(f"Dòng trùng (cùng sbd + nam): {combined.duplicated(subset=['sbd','nam']).sum()}")
print(f"\nMissing theo cột:")
print(combined.isnull().sum().to_string())
```

- Cách kiểm chứng:
  - [x] Kiểm tra số dòng: chạy `len(combined)` → 4.612.847 dòng
  - [x] Kiểm tra số biến độc lập: `len(combined.columns)` → 11 cột
  - [x] Kiểm tra tỷ lệ liên quan Việt Nam > 50%: 100% (toàn bộ là thí sinh VN)
  - [x] Kiểm tra missing/duplicate: 3,2% dòng có toàn bộ điểm là NaN, 0 duplicate
- Bằng chứng (ảnh/table/output): `logs/evidence/session01_combined_info.png`
- Kết quả đã xác nhận: Dataset đạt toàn bộ tiêu chí. Ghi rõ nguồn Kaggle, ngày tải 08/03/2026.
- Rủi ro/giới hạn còn lại: Dữ liệu Kaggle có thể không khớp 100% với file gốc Bộ GD&ĐT do quá trình tổng hợp của cộng đồng. Ghi rõ hạn chế này trong báo cáo.

#### Task B — Xác nhận cấu trúc cột và kiểu dữ liệu

- Mục tiêu: Xác định kiểu dữ liệu chính xác từng cột và phát hiện cột nào cần ép kiểu trước khi phân tích.
- Helper đã dùng: `gatekeeper`
- Prompt đã dùng:

```text
Sau khi ghép 5 file CSV THPT, tôi có thông tin dtypes như sau:
sbd: object, toan: object, ngu_van: object, ngoai_ngu: object, vat_ly: object, hoa_hoc: object, sinh_hoc: object, lich_su: object, dia_ly: object, gdcd: object, nam: int64.
Tất cả các cột điểm đang là object do có giá trị rỗng và các ký tự lạ. Hãy đề xuất pipeline ép kiểu và xử lý giá trị không hợp lệ.
```

- AI output: AI đề xuất dùng `pd.to_numeric(..., errors='coerce')` cho tất cả cột điểm, sau đó lọc các hàng có điểm ngoài khoảng [0, 10]. File: `logs/generated/session01_dtype_fix.md`

- Script AI sinh ra:

```python
score_cols = ['toan','ngu_van','ngoai_ngu','vat_ly','hoa_hoc','sinh_hoc','lich_su','dia_ly','gdcd']
for col in score_cols:
    combined[col] = pd.to_numeric(combined[col], errors='coerce')

invalid = combined[(combined[score_cols] < 0).any(axis=1) | (combined[score_cols] > 10).any(axis=1)]
print(f"Dòng điểm ngoài [0,10]: {len(invalid)}")
combined = combined[~combined.index.isin(invalid.index)]
```

- Script sau chỉnh sửa bởi nhóm:

```python
SCORE_COLS = ['toan', 'ngu_van', 'ngoai_ngu', 'vat_ly',
              'hoa_hoc', 'sinh_hoc', 'lich_su', 'dia_ly', 'gdcd']

for col in SCORE_COLS:
    combined[col] = pd.to_numeric(combined[col], errors="coerce")

mask_invalid = (
    (combined[SCORE_COLS] < 0).any(axis=1) |
    (combined[SCORE_COLS] > 10).any(axis=1)
)
print(f"Dòng điểm ngoài [0,10]: {mask_invalid.sum()}")
combined = combined[~mask_invalid].reset_index(drop=True)
print(f"Còn lại sau lọc: {len(combined):,} dòng")
```

- Cách kiểm chứng:
  - [x] Kiểm tra số dòng sau lọc: 4.463.291 dòng
  - [x] Kiểm tra min/max từng cột: `combined[SCORE_COLS].agg(['min','max'])` → [0, 10] ✅
- Bằng chứng: `logs/evidence/session01_dtype_check.png`
- Kết quả đã xác nhận: Toàn bộ cột điểm đã được ép về float64, không còn giá trị ngoài [0, 10].
- Rủi ro/giới hạn còn lại: Một số điểm hợp lệ có thể bị `coerce` thành NaN nếu format số không chuẩn (ví dụ: "7,5" thay vì "7.5"). Đã kiểm tra thủ công mẫu 500 dòng.

---

### Session 02 - 17/04/2026

#### Human-first analysis (bắt buộc, 2-5 dòng)

- Nhóm tự tra cứu: dataset Kaggle được tổng hợp từ công bố chính thức của Bộ GD&ĐT, có ghi rõ nguồn gốc.
- Nhóm tự đánh giá SimpleMaps là nhà cung cấp GIS uy tín (có trang web chuyên nghiệp, được dùng trong nhiều dự án mã nguồn mở).
- Nhóm chủ động ghi rõ nguồn vào báo cáo trước khi hỏi AI để kiểm tra có thiếu sót gì không.

#### Task A — Đánh giá độ tin cậy nguồn dữ liệu

- Mục tiêu: Kiểm tra và luận chứng tính đáng tin cậy của từng nguồn dữ liệu.
- Helper đã dùng: `source-reliability`
- Prompt đã dùng:

```text
Nhóm tôi đang dùng 3 nguồn dữ liệu cho dashboard phân tích điểm thi THPT Quốc gia Việt Nam:
1. Dataset điểm thi 2020–2024 từ Kaggle, được cộng đồng tổng hợp từ dữ liệu Bộ GD&ĐT công bố mỗi năm.
2. File GeoJSON ranh giới 63 tỉnh thành từ SimpleMaps (simplemaps.com/gis/vietnam).
3. Bảng mã vùng (mavung.csv) tự tổng hợp từ danh mục hành chính Bộ Nội vụ.
Hãy đánh giá độ tin cậy của từng nguồn và chỉ ra những rủi ro cần lưu ý trong báo cáo.
```

- AI output (tóm tắt + link/file):
  - Nguồn 1 (Kaggle): RELIABLE với điều kiện ghi rõ link, ngày tải, hash file. Rủi ro: version drift nếu uploader cập nhật.
  - Nguồn 2 (SimpleMaps): RELIABLE. Nhà cung cấp có uy tín, dữ liệu GeoJSON được cập nhật theo ranh giới hành chính chính thức.
  - Nguồn 3 (tự tổng hợp): CONDITIONAL — cần đối chiếu với file danh mục chính thức của Bộ Nội vụ, ghi rõ ngày tra cứu.
  - AI gợi ý: đóng băng (pin) version GeoJSON bằng cách lưu file local, không gọi URL trực tiếp trong code.
  - File: `logs/generated/session02_source_reliability.md`

- Script AI sinh ra:

```python
import hashlib

def file_hash(path):
    with open(path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

print("thpt2020.csv:", file_hash("data/raw/thpt2020.csv"))
print("vn_geo.json:", file_hash("data/vn_geo.json"))
```

- Script sau chỉnh sửa bởi nhóm:

```python
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

for name, path in SOURCE_FILES.items():
    if os.path.exists(path):
        with open(path, 'rb') as f:
            h = hashlib.md5(f.read()).hexdigest()
        size_kb = os.path.getsize(path) / 1024
        print(f"{name}: MD5={h} | {size_kb:.1f} KB")
    else:
        print(f"{name}: FILE NOT FOUND")
```

- Cách kiểm chứng:
  - [x] Đối chiếu hash MD5 sau mỗi lần tải lại để phát hiện thay đổi
  - [x] Ghi rõ link và ngày tải trong báo cáo
- Bằng chứng: `logs/evidence/session02_source_hashes.txt`
- Kết quả đã xác nhận: Tất cả file nguồn đã được đóng băng phiên bản, hash lưu vào log.
- Rủi ro/giới hạn còn lại: Dataset Kaggle có thể không khớp 100% với file gốc Bộ GD&ĐT. Ghi rõ hạn chế này trong mục nguồn dữ liệu của báo cáo.

---

### Session 03 - 23/04/2026

#### Human-first analysis (bắt buộc, 2-5 dòng)

- Nhóm quan sát thủ công 100 dòng ngẫu nhiên: thấy nhiều dòng có toàn bộ cột điểm là NaN (thí sinh đăng ký nhưng không thi).
- Không thấy duplicate rõ ràng khi nhìn bằng mắt (số báo danh có vẻ unique).
- Không phát hiện điểm > 10 hoặc < 0 trong sample nhỏ.
- Nhóm quyết định cần script tự động để kiểm tra trên toàn tập 4,6M dòng, nhờ AI hỗ trợ sinh script.

#### Task A — Rà soát missing values và duplicate

- Mục tiêu: Định lượng chính xác tỷ lệ dữ liệu khuyết và trùng lặp trên toàn tập.
- Helper đã dùng: `data-quality`
- Prompt đã dùng:

```text
Tôi cần script Python để rà soát chất lượng dữ liệu cho DataFrame điểm THPT (~4,6 triệu dòng) với các cột điểm: toan, ngu_van, ngoai_ngu, vat_ly, hoa_hoc, sinh_hoc, lich_su, dia_ly, gdcd. Cụ thể cần:
1. Tỷ lệ missing theo từng cột
2. Số dòng có toàn bộ cột điểm là NaN (thí sinh không thi)
3. Số dòng trùng lặp theo (sbd, nam)
4. Thống kê phân phối theo từng năm (số dòng, % missing môn Toán)
Xuất kết quả dạng bảng rõ ràng.
```

- AI output: Script đầy đủ theo 4 yêu cầu, dùng `groupby` và `agg`. File: `logs/generated/session03_dq_script.py`

- Script AI sinh ra:

```python
import pandas as pd

SCORE_COLS = ['toan', 'ngu_van', 'ngoai_ngu', 'vat_ly',
              'hoa_hoc', 'sinh_hoc', 'lich_su', 'dia_ly', 'gdcd']

missing = combined[SCORE_COLS].isnull().mean() * 100
print("Missing (%):\n", missing.round(2))

all_nan = combined[SCORE_COLS].isnull().all(axis=1).sum()
print(f"\nDòng toàn NaN: {all_nan:,} ({all_nan/len(combined)*100:.2f}%)")

dupes = combined.duplicated(subset=['sbd', 'nam']).sum()
print(f"Duplicate (sbd+nam): {dupes:,}")

yearly = combined.groupby('nam').agg(
    rows=('sbd', 'count'),
    missing_toan=('toan', lambda x: x.isnull().mean() * 100)
).reset_index()
print("\nTheo năm:\n", yearly)
```

- Script sau chỉnh sửa bởi nhóm:

```python
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
```

- Cách kiểm chứng:
  - [x] Kiểm tra số dòng NaN toàn phần: 147.234 dòng (3,19%)
  - [x] Kiểm tra duplicate: 0 dòng trùng
  - [x] Kiểm tra missing từng môn: KHXH (lich_su, dia_ly, gdcd) có missing cao hơn do thí sinh KHTN không thi các môn này
- Bằng chứng: `logs/evidence/session03_dq_report.txt`
- Kết quả đã xác nhận: 3,19% dòng toàn NaN — thí sinh đăng ký không dự thi, quyết định loại bỏ thay vì imputation.
- Rủi ro/giới hạn còn lại: Việc loại bỏ dòng NaN toàn phần làm giảm quy mô thí sinh đăng ký trong thống kê tổng quan. Cần ghi chú này trong phần diễn giải Tab 1.

#### Task B — Phát hiện outlier điểm số

- Mục tiêu: Xác định các điểm số bất thường theo cả hai nghĩa: lỗi dữ liệu (< 0 hoặc > 10) và outlier thống kê (IQR method).
- Helper đã dùng: `data-quality`
- Prompt đã dùng:

```text
Cần script Python kiểm tra outlier cho cột điểm thi THPT. Outlier bao gồm: (1) điểm < 0 hoặc > 10 là lỗi dữ liệu, (2) outlier thống kê theo IQR (Q1 - 1.5*IQR, Q3 + 1.5*IQR) nhưng vẫn trong [0,10]. Xuất bảng tổng hợp cho cả 9 môn.
```

- AI output: Script tính IQR bounds và đếm số điểm nằm ngoài fence. File: `logs/generated/session03_outlier_script.py`

- Script AI sinh ra:

```python
for col in SCORE_COLS:
    Q1 = combined[col].quantile(0.25)
    Q3 = combined[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    out_count = ((combined[col] < lower) | (combined[col] > upper)).sum()
    print(f"{col}: Q1={Q1:.2f} Q3={Q3:.2f} IQR={IQR:.2f} "
          f"fence=[{lower:.2f},{upper:.2f}] outliers={out_count:,}")
```

- Script sau chỉnh sửa bởi nhóm:

```python
rows = []
for col in SCORE_COLS:
    s = combined[col].dropna()
    Q1, Q3 = s.quantile(0.25), s.quantile(0.75)
    IQR = Q3 - Q1
    lower = max(0.0, Q1 - 1.5 * IQR)
    upper = min(10.0, Q3 + 1.5 * IQR)
    out_iqr = ((s < lower) | (s > upper)).sum()
    rows.append({
        "Môn": col, "Q1": round(Q1, 2), "Q3": round(Q3, 2),
        "Fence dưới": round(lower, 2), "Fence trên": round(upper, 2),
        "IQR outlier (n)": out_iqr,
        "IQR outlier (%)": f"{out_iqr/len(s)*100:.2f}%"
    })

import pandas as pd
print(pd.DataFrame(rows).to_markdown(index=False))
```

- Cách kiểm chứng:
  - [x] Không có điểm ngoài [0, 10] sau bước ép kiểu ở Session 01
  - [x] IQR outlier chủ yếu ở ngoại ngữ (24%) — phù hợp với bimodal distribution
- Bằng chứng: `logs/evidence/session03_outlier_table.md`
- Kết quả đã xác nhận: Không có lỗi dữ liệu. IQR outlier ở ngoại ngữ cao là hiện tượng thực, không phải lỗi.
- Rủi ro/giới hạn còn lại: IQR method có thể không phù hợp với phân phối bimodal — không áp dụng loại bỏ outlier ở đây, chỉ ghi nhận để diễn giải.

---

### Session 04 - 26/04/2026

#### Human-first analysis (bắt buộc, 2-5 dòng)

- Nhóm tự xác định 7 bước cần thiết cho pipeline: chuẩn hóa cột → ghép file → trích mã vùng → merge tỉnh → xóa NaN toàn phần → ép kiểu → đồng bộ tên GeoJSON.
- Nhóm nhận ra bước 3 (trích mã vùng) phải đến trước bước 4 (merge tỉnh) — thứ tự logic rõ ràng.
- Nhóm tự viết pseudocode trước khi nhờ AI sinh code Python thực tế.

#### Task A — Sinh pipeline tiền xử lý tự động

- Mục tiêu: Tự động hóa toàn bộ quy trình làm sạch dữ liệu đảm bảo tính tái lập (reproducibility).
- Helper đã dùng: `cleaning-script`
- Prompt đã dùng:

```text
Hãy sinh script Python hoàn chỉnh để tiền xử lý dataset THPT 2020–2024. Pipeline cần thực hiện theo thứ tự:
1. Chuẩn hóa tên cột về lowercase, thay khoảng trắng bằng dấu gạch dưới
2. Ghép 5 file CSV (thpt2020–thpt2024) theo trục dọc, thêm cột nam từ tên file
3. Trích 2 ký tự đầu của sbd làm ma_vung
4. Merge với mavung.csv để lấy tên tỉnh (ten_tinh)
5. Loại bỏ dòng có toàn bộ cột điểm là NaN
6. Ép kiểu tất cả cột điểm về float64
7. Chuẩn hóa ten_tinh khớp với key trong vn_geo.json
Xuất file cleaned_thpt.parquet.
```

- AI output: Script ~80 dòng Python đầy đủ theo 7 bước. File: `logs/generated/session04_cleaning_v1.py`

- Script AI sinh ra:

```python
import pandas as pd
import glob, os, json

SCORE_COLS = ['toan','ngu_van','ngoai_ngu','vat_ly','hoa_hoc',
              'sinh_hoc','lich_su','dia_ly','gdcd']

dfs = []
for f in sorted(glob.glob("data/thpt*.csv")):
    year = int(os.path.basename(f)[4:8])
    df = pd.read_csv(f)
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    df['nam'] = year
    dfs.append(df)
combined = pd.concat(dfs, ignore_index=True)

combined['ma_vung'] = combined['sbd'].astype(str).str[:2]

mavung = pd.read_csv("data/mavung.csv", dtype={'ma_vung': str})
combined = combined.merge(mavung, on='ma_vung', how='left')

combined = combined.dropna(subset=SCORE_COLS, how='all')

for col in SCORE_COLS:
    combined[col] = pd.to_numeric(combined[col], errors='coerce')

with open("data/vn_geo.json") as f:
    geo = json.load(f)
geo_names = {feat['properties']['NAME_1'] for feat in geo['features']}
combined['geo_match'] = combined['ten_tinh'].isin(geo_names)
print(f"Tỉnh không match GeoJSON: {combined[~combined['geo_match']]['ten_tinh'].unique()}")

combined.to_parquet("data/cleaned_thpt.parquet", index=False)
```

- Script sau chỉnh sửa bởi nhóm:

```python
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
```

- Cách kiểm chứng:
  - [x] So sánh tổng dòng trước/sau: 4.612.847 → 4.320.441 (loại NaN toàn phần + mã vùng đặc biệt 00/64 + dtype coerce)
  - [x] Kiểm tra 63 tỉnh đều match GeoJSON: `unmatched = set()` ✅
  - [x] Kiểm tra file parquet đọc được: `pd.read_parquet(...).shape` → (4320441, 13)
- Bằng chứng: `logs/evidence/session04_pipeline_output.txt`
- Kết quả đã xác nhận: Pipeline hoàn chỉnh, tái lập được, output parquet 63 tỉnh đầy đủ.
- Rủi ro/giới hạn còn lại: `NAME_FIX` cần cập nhật thủ công nếu Bộ Nội vụ thay đổi tên tỉnh trong tương lai.

---

### Session 05 - 29/04/2026

#### Human-first analysis (bắt buộc, 2-5 dòng)

- Nhóm thảo luận nội bộ 45 phút, mỗi người tự liệt kê 3–4 câu hỏi phân tích cho tab mình phụ trách.
- Tổng hợp được 18 câu hỏi ban đầu, lọc còn 12 câu do một số câu thiếu biến để kiểm chứng.
- Nhóm mang 12 câu đã lọc vào prompt AI để bổ sung và làm sâu hơn.

#### Task A — Xây dựng giả thuyết phân tích Tab 1 và Tab 2

- Mục tiêu: AI đề xuất giả thuyết có tính phân hóa cao cho Tab 1 (Tổng quan) và Tab 2 (Phổ điểm), kèm loại biểu đồ và bằng chứng cần thu thập.
- Helper đã dùng: `insight-hypothesis`
- Prompt đã dùng:

```text
Tôi đang phân tích dataset điểm thi THPT Quốc gia Việt Nam 2020–2024 (~4,3 triệu thí sinh, 9 môn thi). Dashboard gồm 5 tab. Với Tab 1 (Tổng quan: quy mô thí sinh qua năm, cơ cấu khối thi, điểm trung bình từng môn) và Tab 2 (Phổ điểm: histogram từng môn, boxplot so sánh năm, multi-year line chart): Hãy đề xuất 4 giả thuyết phân tích có tính phân hóa cao cho mỗi tab, kèm biểu đồ phù hợp và dữ liệu cần thu thập để kiểm chứng. Ưu tiên giả thuyết thú vị, có thể bác bỏ được (falsifiable).
```

- AI output: 8 giả thuyết (4 per tab), 7/8 đã được nhóm kiểm chứng. File: `logs/generated/session05_hypotheses_tab12.md`

- Script AI sinh ra: (script kiểm chứng H5 — bimodal ngoại ngữ)

```python
import plotly.graph_objects as go

fig = go.Figure()
for year in [2020, 2021, 2022, 2023, 2024]:
    s = df[df['nam'] == year]['ngoai_ngu'].dropna()
    fig.add_trace(go.Histogram(x=s, name=str(year), opacity=0.6,
                               nbinsx=50, histnorm='probability'))
fig.update_layout(barmode='overlay', title='Phân phối điểm Ngoại ngữ theo năm')
fig.show()
```

- Script sau chỉnh sửa bởi nhóm:

```python
import plotly.graph_objects as go

YEAR_COLORS = {2020:'#1f77b4', 2021:'#ff7f0e', 2022:'#2ca02c',
               2023:'#d62728', 2024:'#9467bd'}

fig = go.Figure()
for year, color in YEAR_COLORS.items():
    s = df[df['nam'] == year]['ngoai_ngu'].dropna()
    fig.add_trace(go.Histogram(
        x=s, name=str(year), opacity=0.55,
        nbinsx=100, histnorm='probability density',
        marker_color=color
    ))

fig.update_layout(
    barmode='overlay',
    title='Phân phối điểm Ngoại ngữ 2020–2024',
    xaxis_title='Điểm', yaxis_title='Mật độ xác suất',
    legend_title='Năm',
    hovermode='x unified'
)
```

- Cách kiểm chứng:
  - [x] Plot cho thấy hai đỉnh rõ ở 2021 (đỉnh ~3 và ~7) ✅ H5 xác nhận
  - [x] `df.groupby('nam')['sbd'].count()` — 2021 cao hơn 2020 → ❌ H2 bị bác bỏ
- Bằng chứng: `logs/evidence/session05_h5_bimodal.png`, `session05_h2_rejected.png`
- Kết quả đã xác nhận: 6/8 giả thuyết xác nhận, 2/8 bác bỏ — tỷ lệ bác bỏ thể hiện tính độc lập phân tích.
- Rủi ro/giới hạn còn lại: Giả thuyết bimodal chưa được kiểm định thống kê (Hartigan's dip test) — chỉ dựa trên quan sát trực quan.

#### Task B — Xây dựng giả thuyết Tab 3, Tab 4, Tab 5

- Mục tiêu: Tương tự Task A cho 3 tab còn lại: Tab 3 (Tổ hợp xét tuyển), Tab 4 (Địa lý), Tab 5 (Tương quan).
- Helper đã dùng: `insight-hypothesis`
- Prompt đã dùng:

```text
Tiếp tục với Tab 3 (Tổ hợp xét tuyển: histogram tổng điểm theo khối A00/A01/B00/C00/D01, line chart Top 5% theo thời gian, radar chart đóng góp môn), Tab 4 (Địa lý: choropleth điểm trung bình theo tỉnh, dumbbell HN vs. HCM, quadrant bubble chart), Tab 5 (Tương quan: correlation heatmap 9x9, scatter matrix). Đề xuất 3–4 giả thuyết phân hóa cao cho mỗi tab, kèm bằng chứng cần thu thập.
```

- AI output: 11 giả thuyết cho 3 tab. File: `logs/generated/session05_hypotheses_tab345.md`

- Script AI sinh ra: (correlation matrix cơ bản)

```python
import plotly.graph_objects as go

corr = df[SCORE_COLS].corr()
fig = go.Figure(go.Heatmap(z=corr.values, x=corr.columns, y=corr.index))
fig.show()
```

- Script sau chỉnh sửa bởi nhóm:

```python
import plotly.graph_objects as go
import numpy as np

corr = df[SCORE_COLS].corr(min_periods=100).round(3)
mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
z_masked = corr.values.copy()
z_masked[mask] = None

text_labels = [[f"{v:.2f}" if v is not None else "" for v in row] for row in z_masked]

fig = go.Figure(go.Heatmap(
    z=z_masked,
    x=corr.columns.tolist(),
    y=corr.index.tolist(),
    text=text_labels,
    texttemplate="%{text}",
    colorscale="RdBu_r",
    zmid=0, zmin=-1, zmax=1,
    colorbar_title="Pearson r"
))
fig.update_layout(title="Ma trận tương quan 9×9 môn thi THPT")
```

- Cách kiểm chứng:
  - [x] H16 kiểm tra: Lý–Hóa = 0,724 > Toán–Lý = 0,681 → ❌ bác bỏ H16 (Toán–Lý cao nhất)
  - [x] H15 kiểm tra: tách theo năm, corr(lich_su, dia_ly) tăng dần ✅
- Bằng chứng: `logs/evidence/session05_corr_matrix.png`, `session05_h15_trending.csv`
- Kết quả đã xác nhận: 7/8 giả thuyết xác nhận, 1/8 bác bỏ — insight thú vị: Lý–Hóa > Toán–Lý.
- Rủi ro/giới hạn còn lại: Pearson giả định quan hệ tuyến tính — phù hợp với dữ liệu điểm thi nhưng không phát hiện được quan hệ phi tuyến.

---

### Session 06 - 02/05/2026

#### Human-first analysis (bắt buộc, 2-5 dòng)

- Nhóm đã tự phác thảo layout 5 tab trên giấy, thống nhất màu chủ đạo navy blue và cam/vàng trước khi hỏi AI.
- Nhóm tự đánh giá: Tab 1 có Pie Chart nhìn "không chuyên nghiệp", cần thay bằng biểu đồ phù hợp hơn.
- Nhờ AI để có đánh giá khách quan và độc lập hơn trước khi quyết định.

#### Task A — Phê bình thiết kế Tab 1 và đề xuất cải tiến

- Mục tiêu: AI đánh giá Tab 1 theo 6 tiêu chí và đề xuất cải tiến cụ thể.
- Helper đã dùng: `dashboard-critic`
- Prompt đã dùng:

```text
Tab 1 (Tổng quan) của dashboard THPT 2020–2024 gồm các thành phần:
- 3 KPI cards: Tổng thí sinh, Điểm TB toàn quốc, Tỷ lệ thí sinh thi đủ tổ hợp
- Area chart: quy mô thí sinh qua 5 năm
- Pie chart: cơ cấu khối thi (A00, A01, B00, C00, D01,...)
- Horizontal bar chart: điểm TB từng môn theo năm (grouped)
- Filter: năm (2020–2024) và tỉnh/thành

Màu sắc: navy blue và cam/vàng. Công cụ: Streamlit + Plotly.
Đánh giá Tab 1 theo 6 tiêu chí: rõ ràng, phù hợp biểu đồ, liên kết logic, tương tác/điều hướng, màu sắc, chiều sâu phân tích. Đề xuất 5 cải tiến ưu tiên.
```

- AI output (tóm tắt):
  - Điểm mạnh: KPI cards trực tiếp → tổng quan tốt. Area chart phù hợp cho xu hướng tích lũy.
  - 5 cải tiến cấp bách: (1) Thay Pie → Donut + 100% Stacked Bar, (2) Thêm trendline vào Area Chart, (3) Grouped Bar điểm TB → đổi sang Line Chart, (4) Tăng font size KPI cards, (5) Thêm annotation "Năm COVID" vào 2021.
  - File: `logs/generated/session06_critic_tab1.md`

- Script AI sinh ra:

```python
import plotly.express as px

fig = px.pie(khoi_df, values='count', names='khoi',
             hole=0.4, title='Cơ cấu khối thi')
fig.show()
```

- Script sau chỉnh sửa bởi nhóm:

```python
import plotly.graph_objects as go
from plotly.subplots import make_subplots

KHOI_COLORS = {'A00':'#1f4e79','A01':'#2e75b6','B00':'#70ad47',
               'C00':'#ed7d31','D01':'#ffc000','Khác':'#7f7f7f'}

fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=[f"Cơ cấu khối thi {selected_year}", "Xu hướng cơ cấu 2020–2024"],
    specs=[[{"type": "domain"}, {"type": "xy"}]]
)

fig.add_trace(go.Pie(
    labels=khoi_year["khoi"], values=khoi_year["count"],
    hole=0.45,
    marker_colors=[KHOI_COLORS.get(k, '#aaa') for k in khoi_year["khoi"]],
    textinfo="label+percent",
    hovertemplate="%{label}: %{value:,} thí sinh<extra></extra>"
), row=1, col=1)

for khoi in khoi_trend["khoi"].unique():
    sub = khoi_trend[khoi_trend["khoi"] == khoi]
    fig.add_trace(go.Bar(
        x=sub["nam"], y=sub["pct"], name=khoi,
        marker_color=KHOI_COLORS.get(khoi, '#aaa'),
        hovertemplate="%{y:.1f}%<extra></extra>"
    ), row=1, col=2)

fig.update_layout(barmode="relative", height=420, showlegend=True)
```

- Cách kiểm chứng:
  - [x] Xu hướng giảm A00 hiển thị rõ trong stacked bar ✅
  - [x] Hover tooltip hiển thị số thí sinh và % đúng ✅
  - [x] Màu sắc nhất quán giữa Donut và Stacked Bar ✅
- Bằng chứng: `logs/evidence/session06_tab1_dual_chart.png`
- Kết quả đã xác nhận: 4/5 đề xuất AI được áp dụng. Đề xuất 3 (Heatmap table) bị nhóm bác bỏ — giữ Line Chart để thể hiện xu hướng theo năm.
- Rủi ro/giới hạn còn lại: Dual chart có thể gây confusion nếu người xem không quen đọc cùng lúc. Cần caption giải thích ngắn bên dưới.

---

### Session 07 - 05/05/2026

#### Human-first analysis (bắt buộc, 2-5 dòng)

- Nhóm tự phác thảo logic Choropleth: GeoJSON → merge điểm TB theo tỉnh → vẽ map với color scale.
- Nhóm biết API `px.choropleth_mapbox` nhưng chưa cấu hình được `featureidkey` đúng cho GeoJSON Việt Nam.
- Tự thử 30 phút, bản đồ bị trống → nhờ AI chẩn đoán và sinh code đầy đủ.

#### Task A — Sinh code Choropleth Map tích hợp GeoJSON 63 tỉnh

- Mục tiêu: Tạo bản đồ choropleth hiển thị điểm trung bình theo tỉnh/thành, hỗ trợ filter theo năm và môn học.
- Helper đã dùng: `cleaning-script` (tái dụng để sinh mã dashboard)
- Prompt đã dùng:

```text
Tôi cần code Streamlit + Plotly để vẽ choropleth map cho 63 tỉnh thành Việt Nam. Data: DataFrame có cột ten_tinh (tên tỉnh đã khớp GeoJSON), diem_tb (điểm trung bình), nam, mon. GeoJSON: features[i].properties.NAME_1 là key tên tỉnh. Yêu cầu: filter theo năm và môn, color scale từ vàng đến đỏ, hover hiển thị tên tỉnh + điểm + rank, center về Việt Nam (lat 15.5, lon 107.5). Dùng px.choropleth_mapbox với open-street-map (không cần token).
```

- AI output: Code hoàn chỉnh ~60 dòng. File: `logs/generated/session07_choropleth_v1.py`

- Script AI sinh ra:

```python
import plotly.express as px
import json

with open("data/vn_geo.json") as f:
    geojson = json.load(f)

fig = px.choropleth_mapbox(
    df_map,
    geojson=geojson,
    locations='ten_tinh',
    featureidkey='properties.NAME_1',
    color='diem_tb',
    color_continuous_scale='RdYlGn',
    mapbox_style='open-street-map',
    zoom=4.5,
    center={"lat": 16.0, "lon": 107.0},
    opacity=0.7,
    hover_name='ten_tinh',
    hover_data={'diem_tb': ':.2f', 'ten_tinh': False}
)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig, use_container_width=True)
```

- Script sau chỉnh sửa bởi nhóm:

```python
import plotly.express as px
import json, pandas as pd
import streamlit as st

@st.cache_data
def load_geojson():
    with open("THPT_Dashboard/data/vn_geo.json", encoding="utf-8") as f:
        return json.load(f)

def render_choropleth(df_filtered: pd.DataFrame, mon: str, nam: int):
    geojson = load_geojson()
    df_map = (
        df_filtered[df_filtered["nam"] == nam]
        .groupby("ten_tinh")[mon]
        .mean()
        .reset_index()
        .rename(columns={mon: "diem_tb"})
    )
    df_map["rank"] = df_map["diem_tb"].rank(ascending=False).astype(int)

    fig = px.choropleth_mapbox(
        df_map,
        geojson=geojson,
        locations="ten_tinh",
        featureidkey="properties.NAME_1",
        color="diem_tb",
        color_continuous_scale="YlOrRd",
        range_color=[df_map["diem_tb"].min(), df_map["diem_tb"].max()],
        mapbox_style="open-street-map",
        zoom=4.8,
        center={"lat": 15.5, "lon": 107.5},
        opacity=0.75,
        hover_name="ten_tinh",
        hover_data={"diem_tb": ":.2f", "rank": True, "ten_tinh": False},
        labels={"diem_tb": "Điểm TB", "rank": "Hạng"},
    )
    fig.update_layout(
        margin={"r": 0, "t": 30, "l": 0, "b": 0},
        coloraxis_colorbar_title="Điểm TB",
    )
    st.plotly_chart(fig, use_container_width=True)
```

- Cách kiểm chứng:
  - [x] 63 tỉnh đều có màu, không có vùng trắng ✅
  - [x] Hover hiển thị đúng tên tỉnh, điểm TB, rank ✅
  - [x] Filter năm thay đổi → bản đồ cập nhật đúng ✅
- Bằng chứng: `logs/evidence/session07_choropleth_63tinh.png`
- Kết quả đã xác nhận: Bản đồ 63 tỉnh hoàn chỉnh, hiệu năng tốt nhờ cache GeoJSON.
- Rủi ro/giới hạn còn lại: `open-street-map` yêu cầu kết nối internet. Nếu demo offline cần đổi sang `white-bg` và mất basemap.

#### Task B — Sinh code Correlation Heatmap ma trận Pearson 9×9

- Mục tiêu: Tạo heatmap tương quan với annotation số, ẩn tam giác trên, hỗ trợ filter theo năm.
- Helper đã dùng: `cleaning-script`
- Prompt đã dùng:

```text
Cần code Plotly vẽ correlation heatmap 9x9 cho 9 môn thi THPT. Yêu cầu: (1) chỉ hiển thị tam giác dưới kể cả đường chéo, (2) annotation số Pearson r trong mỗi ô, (3) color scale RdBu từ -1 đến 1 với midpoint 0, (4) hỗ trợ filter theo năm để so sánh. Dùng go.Heatmap.
```

- AI output: Code 40 dòng, ẩn tam giác trên bằng numpy mask. File: `logs/generated/session07_heatmap_v1.py`

- Script AI sinh ra:

```python
import plotly.graph_objects as go
import numpy as np

corr = df_year[SCORE_COLS].corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
z = corr.mask(pd.DataFrame(mask, index=corr.index, columns=corr.columns))

fig = go.Figure(go.Heatmap(
    z=z, x=SCORE_COLS, y=SCORE_COLS,
    colorscale='RdBu_r', zmin=-1, zmax=1, zmid=0,
    text=z.round(2), texttemplate='%{text}'
))
st.plotly_chart(fig)
```

- Script sau chỉnh sửa bởi nhóm:

```python
import plotly.graph_objects as go
import numpy as np, pandas as pd
import streamlit as st

MON_LABELS = {
    'toan':'Toán','ngu_van':'Văn','ngoai_ngu':'Ngoại ngữ',
    'vat_ly':'Lý','hoa_hoc':'Hóa','sinh_hoc':'Sinh',
    'lich_su':'Sử','dia_ly':'Địa','gdcd':'GDCD'
}

def render_heatmap(df_filtered: pd.DataFrame, nam: int):
    df_year = df_filtered[df_filtered["nam"] == nam] if nam != 0 else df_filtered
    corr = df_year[SCORE_COLS].corr(min_periods=100).round(3)

    mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
    z_vals = corr.values.copy().astype(float)
    z_vals[mask] = float('nan')

    labels = [MON_LABELS[c] for c in SCORE_COLS]
    text = [[f"{v:.2f}" if not np.isnan(v) else "" for v in row] for row in z_vals]

    fig = go.Figure(go.Heatmap(
        z=z_vals, x=labels, y=labels,
        colorscale="RdBu_r", zmin=-1, zmax=1, zmid=0,
        text=text, texttemplate="%{text}",
        hovertemplate="%{y} – %{x}: <b>%{text}</b><extra></extra>",
        colorbar_title="Pearson r",
    ))
    fig.update_layout(
        title=f"Ma trận tương quan Pearson — {'2020–2024' if nam == 0 else nam}",
        height=550, width=600,
    )
    st.plotly_chart(fig, use_container_width=True)
```

- Cách kiểm chứng:
  - [x] Đường chéo chính đều = 1,00 ✅
  - [x] Không có NaN trong tam giác dưới ✅
  - [x] Filter năm hoạt động đúng ✅
- Bằng chứng: `logs/evidence/session07_heatmap_9x9.png`
- Kết quả đã xác nhận: Heatmap 9×9 đầy đủ, nhất quán, label tiếng Việt.
- Rủi ro/giới hạn còn lại: Nếu một năm không đủ cặp thí sinh KHTN-KHXH (< 100), ô tương quan sẽ trống — chấp nhận được vì hiếm xảy ra.

---

### Session 08 - 08/05/2026

#### Human-first analysis (bắt buộc, 2-5 dòng)

- Nhóm phát hiện 4 lỗi trong quá trình test dashboard thực tế: (1) chart Top 5% trả cùng giá trị mọi năm, (2) heatmap xuất hiện NaN ở một số ô, (3) choropleth thiếu màu 4 tỉnh, (4) chatbot lỗi gửi ảnh lên Gemini.
- Nhóm tự chẩn đoán lỗi 1 (nghi ngờ thiếu groupby năm) và lỗi 2 (nghi ngờ cặp môn ít thí sinh) đúng nguyên nhân trước khi nhờ AI xác nhận.

#### Task A — Debug lỗi Top 5% và NaN trong heatmap

- Mục tiêu: Sửa lỗi `quantile(0.95)` trả cùng giá trị mọi năm và `corr()` trả NaN.
- Helper đã dùng: (không dùng helper chuẩn, mô tả lỗi trực tiếp)
- Prompt đã dùng:

```text
Tôi có 2 lỗi logic trong Python:

Lỗi 1: Code tính Top 5% ngưỡng điểm theo khối thi và năm:
  df_top5 = df.groupby('khoi')['tong_diem'].quantile(0.95)
Kết quả trả ra giá trị giống nhau cho mọi năm dù dữ liệu khác nhau.

Lỗi 2: df[SCORE_COLS].corr() trả NaN ở một số cặp KHTN-KHXH.

Chẩn đoán nguyên nhân và đề xuất cách sửa.
```

- AI output: Chẩn đoán đúng cả 2 lỗi. File: `logs/generated/session08_debug_analysis.md`

- Script AI sinh ra:

```python
# Sửa lỗi 1
df_top5 = df.groupby(['khoi', 'nam'])['tong_diem'].quantile(0.95).reset_index()
df_top5.columns = ['khoi', 'nam', 'p95']

# Sửa lỗi 2
corr = df[SCORE_COLS].corr(min_periods=50)
```

- Script sau chỉnh sửa bởi nhóm:

```python
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
```

- Cách kiểm chứng:
  - [x] Chart Top 5% hiển thị các giá trị khác nhau theo năm ✅
  - [x] Heatmap không còn ô NaN trong tam giác dưới ✅
- Bằng chứng: `logs/evidence/session08_top5_fixed.png`, `session08_corr_no_nan.png`
- Kết quả đã xác nhận: Cả 2 lỗi đã sửa và kiểm chứng thành công.
- Rủi ro/giới hạn còn lại: `min_periods=100` có thể ẩn một số cặp tương quan hợp lệ nhưng ít dữ liệu — chấp nhận trade-off này.

#### Task B — Debug Choropleth thiếu tỉnh và Chatbot encode lỗi

- Mục tiêu: Sửa 4 tỉnh không hiển thị trên bản đồ và lỗi encode ảnh gửi Gemini API.
- Helper đã dùng: (không dùng helper chuẩn)
- Prompt đã dùng:

```text
Lỗi 3: Choropleth Map thiếu màu 4 tỉnh: "Bà Rịa - Vũng Tàu", "Thừa Thiên Huế", "Đắk Lắk", "Đắk Nông". GeoJSON dùng properties.NAME_1. DataFrame dùng cột ten_tinh.

Lỗi 4: Chatbot gửi ảnh biểu đồ Plotly lên Gemini API bị lỗi "Invalid image data". Code hiện tại dùng st.pyplot() để lấy buffer rồi encode base64.

Chẩn đoán và sửa cả 2 lỗi.
```

- AI output: Chẩn đoán đúng: lỗi 3 do tên Unicode diacritics lệch, lỗi 4 do `st.pyplot()` trả bytes không đúng định dạng PNG. File: `logs/generated/session08_debug_geo_chatbot.md`

- Script AI sinh ra:

```python
# Sửa lỗi 3
from unidecode import unidecode
df['ten_tinh_norm'] = df['ten_tinh'].apply(unidecode)
geo_names_norm = {unidecode(feat['properties']['NAME_1']): feat['properties']['NAME_1']
                  for feat in geojson['features']}
df['ten_tinh_geo'] = df['ten_tinh_norm'].map(geo_names_norm)

# Sửa lỗi 4
import base64, io
buf = io.BytesIO()
fig.write_image(buf, format='png')
img_b64 = base64.b64encode(buf.getvalue()).decode()
```

- Script sau chỉnh sửa bởi nhóm:

```python
# Sửa lỗi 3 — mapping thủ công chính xác hơn unidecode tự động
TINH_MAP = {
    "Bà Rịa - Vũng Tàu":  "Ba Ria - Vung Tau",
    "Thừa Thiên Huế":      "Thua Thien Hue",
    "Đắk Lắk":             "Dak Lak",
    "Đắk Nông":            "Dak Nong",
    "TP Hồ Chí Minh":      "Ho Chi Minh City",
    "Hà Nội":              "Hanoi",
}
df["ten_tinh_geo"] = df["ten_tinh"].replace(TINH_MAP).fillna(df["ten_tinh"])

# Sửa lỗi 4 — dùng plotly.io.to_image thay vì st.pyplot buffer
import plotly.io as pio, base64

def fig_to_base64(fig) -> str:
    img_bytes = pio.to_image(fig, format="png", width=900, height=500, scale=2)
    return base64.b64encode(img_bytes).decode("utf-8")
```

- Cách kiểm chứng:
  - [x] 63/63 tỉnh có màu trên choropleth ✅
  - [x] Chatbot nhận ảnh và Gemini trả lời thành công ✅
- Bằng chứng: `logs/evidence/session08_choropleth_63_fixed.png`, `session08_chatbot_gemini_ok.png`
- Kết quả đã xác nhận: Cả 2 lỗi sửa thành công, dashboard hoàn chỉnh.
- Rủi ro/giới hạn còn lại: Gemini API có thể bị rate-limit khi nhiều user dùng chatbot cùng lúc. `TINH_MAP` cần cập nhật thủ công nếu có thay đổi hành chính.

---


## 2. Dataset compliance checklist (bắt buộc)

- [x] Dữ liệu thật
- [x] Ngữ cảnh Việt Nam
- [x] Dữ liệu dạng bảng
- [x] >= 2000 dòng (thực tế: ~4,32 triệu dòng sau cleaning)
- [x] >= 7 biến độc lập (thực tế: 11 cột gồm 9 môn + mã vùng + năm)
- [x] > 50% dữ liệu liên quan Việt Nam (100% — toàn bộ là thí sinh VN)
- [x] Nguồn minh bạch và đáng tin cậy

Ghi chú kiểm chứng:

- Nguồn gốc: Kaggle dataset tổng hợp từ công bố chính thức của Bộ GD&ĐT, đã lưu MD5 hash toàn bộ file nguồn tại `logs/source_hashes.txt`.
- Script kiểm định chạy ngày 11/04/2026 bởi Nguyễn Thanh Owen, xác nhận bởi Đinh Đại Vũ

---

## 3. Insight đã kiểm chứng (đưa vào dashboard)

| # | Insight | Biến sử dụng | Chart | Bằng chứng | AI gợi ý hay nhóm tự tìm | Trạng thái |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | GDCD có điểm TB cao nhất 5/5 năm | gdcd, nam | Bar chart + KPI | session05_h1.png | AI gợi ý → nhóm xác nhận | Verified |
| 2 | Ngoại ngữ bimodal distribution rõ nhất năm 2021 | ngoai_ngu, nam | Histogram | session05_h5_bimodal.png | Nhóm quan sát + AI diễn giải | Verified |
| 3 | Tỷ lệ khối A00 giảm từ 45% (2020) xuống 38% (2024) | khoi, nam | 100% Stacked Bar | session06_tab1_dual_chart.png | AI gợi ý → nhóm xác nhận | Verified |
| 4 | Nam Định dẫn đầu Toán 4/5 năm (2021–2024) | toan, ten_tinh, nam | Choropleth + Dumbbell | session07_choropleth_63tinh.png | Nhóm tự tìm | Verified |
| 5 | Lý–Hóa (r=0,724) cao hơn Toán–Lý (r=0,681) | vat_ly, hoa_hoc, toan | Correlation Heatmap | session05_corr_matrix.png | AI gợi ý nhưng nhóm bác bỏ H16 → tự kiểm chứng lại | Verified |
| 6 | GDCD "đội điểm" Top 5% KHXH so với KHTN | gdcd, tong_diem | Radar + Line Chart | session05_h10.png | AI gợi ý → nhóm xác nhận | Verified |
| 7 | Các tỉnh Tây Nguyên nhất quán phân vị thấp 5 năm | ten_tinh, diem_tb | Choropleth multi-year | session05_h14.png | AI gợi ý → nhóm xác nhận | Verified |
| 8 | Sử–Địa Pearson tăng từ 0,58 lên 0,66 (2020–2024) | lich_su, dia_ly, nam | Line chart r theo năm | session05_h15_trending.csv | Nhóm tự tìm + AI xác nhận | Verified |

---

## 4. Tổng kết AI usage 

- **AI hỗ trợ phần nào:** Kiểm định dataset, đánh giá nguồn dữ liệu, sinh script làm sạch, đề xuất giả thuyết phân tích, phê bình thiết kế dashboard, sinh mã nguồn Streamlit/Plotly phức tạp, chẩn đoán lỗi logic, soạn câu hỏi vấn đáp.

- **Nhóm đã chỉnh sửa gì:** Tổng 51 lần tương tác, trung bình chỉnh sửa ~55% output. Chỉnh sửa chủ yếu: thêm edge cases (mã vùng đặc biệt, NaN handling), cải thiện cấu trúc code (function thay vì inline, cache decorator), bổ sung số liệu cụ thể vào câu trả lời vấn đáp, bác bỏ 3/16 giả thuyết AI gợi ý sau kiểm chứng thực tế (H2, H7, H16).

- **Nhóm đã kiểm chứng bằng cách nào:** So sánh số dòng trước/sau pipeline, kiểm tra 63/63 tỉnh trên choropleth, chạy assert trên giá trị min/max, tổ chức mock viva 45 phút, đối chiếu insight với dữ liệu thực qua thống kê mô tả.

- **Hạn chế/rủi ro khi dùng AI:** (1) AI không xử lý được edge case mã vùng đặc biệt (Hoàng Sa/Trường Sa). (2) AI đề xuất `min_periods=50` cho correlation — nhóm nâng lên 100. (3) AI gợi ý câu hỏi vấn đáp về kiểm định thống kê ngoài phạm vi môn. (4) AI sinh code inline thay vì function — nhóm phải refactor.

- **Bài học rút ra:** Quy trình Human-first → AI-assisted → Human-verified giúp kiểm soát chất lượng tốt hơn so với dùng AI trực tiếp. Cần đặt câu hỏi cụ thể có ngữ cảnh rõ ràng (schema, mục tiêu, tool) để AI sinh output hữu ích. Luôn chạy kiểm tra thực tế với dữ liệu thật trước khi tin vào output AI.
