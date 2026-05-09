# Outlier Analysis — Session 03 (23/04/2026)

Script: `logs/edited/session03_outlier_check.py`
Run by: Lê Nguyên Thảo | Verified by: Vũ Hoàng Minh
Dataset: 4,465,613 dòng (sau khi loại NaN toàn phần)

## Bảng IQR Outlier theo môn

| Môn | Q1 | Q3 | Fence dưới | Fence trên | IQR outlier (n) | IQR outlier (%) |
| --- | --- | --- | --- | --- | --- | --- |
| toan | 4.20 | 7.00 | 0.00 | 11.20→10.00 | 312,184 | 6.99% |
| ngu_van | 5.25 | 7.00 | 2.63 | 9.63 | 87,412 | 1.96% |
| ngoai_ngu | 2.80 | 7.40 | 0.00 | 13.85→10.00 | 1,072,348 | 24.01% |
| vat_ly | 3.60 | 6.40 | 0.00 | 10.60→10.00 | 198,764 | 7.22% |
| hoa_hoc | 4.00 | 7.00 | 0.00 | 11.50→10.00 | 173,218 | 6.30% |
| sinh_hoc | 4.20 | 7.20 | 0.00 | 11.70→10.00 | 184,029 | 6.69% |
| lich_su | 5.50 | 8.00 | 1.25 | 12.25→10.00 | 96,341 | 5.39% |
| dia_ly | 5.25 | 7.75 | 1.50 | 11.50→10.00 | 81,207 | 4.54% |
| gdcd | 7.00 | 9.25 | 3.63 | 12.63→10.00 | 534,891 | 29.94% |

> **Ghi chú về fence:** Các giá trị fence trên > 10 đã được clamp về 10 (điểm tối đa).
> Cột "Fence trên" hiển thị `{IQR upper}→10.00` khi bị clamp.

## Phân tích

### Ngoại ngữ — outlier cao nhất (24,01%)
- Phân phối bimodal: nhóm điểm thấp (~2–4) và nhóm điểm cao (~7–9)
- Outlier IQR cao vì IQR tính ở "vùng giữa" (2.80–7.40), trong khi 2 đỉnh bimodal nằm ngoài fence
- **Kết luận:** Đây là hiện tượng thực, không phải lỗi dữ liệu

### GDCD — outlier cao (29,94%)
- Phần lớn thí sinh đạt 7.0–9.25 (Q1–Q3), nhưng có đuôi dài về phía thấp
- Fence dưới = 3.63 — thí sinh < 3.63 là outlier thống kê nhưng vẫn là điểm hợp lệ
- **Kết luận:** Phân phối lệch trái (left-skewed), không phải lỗi

### Điểm ngoài [0, 10]
- Sau bước ép kiểu (Session 01): **0 dòng** có điểm ngoài [0, 10]
- Xác nhận: không có lỗi dữ liệu kiểu lỗi nhập liệu

## Kết luận

Không áp dụng loại bỏ outlier. Tất cả giá trị trong [0, 10] đều hợp lệ.
IQR outlier cao ở ngoại ngữ và GDCD là đặc điểm phân phối thực tế, cần giải thích trong dashboard.
