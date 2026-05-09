# Dashboard Critique — Tab 1 — Session 06 (02/05/2026)

**Prompt received at:** 10:02:45
**Helper:** dashboard-critic
**Responded by:** Claude (claude-sonnet-4-6)

---

## 1) Input snapshot

- Tab 1 gồm: 3 KPI cards, Area Chart (quy mô), Pie Chart (cơ cấu khối), Horizontal Bar Chart (điểm TB)
- Màu sắc: navy blue + cam/vàng
- Filter: năm (2020–2024) và tỉnh/thành
- Công cụ: Streamlit + Plotly

---

## 2) Core analysis

### 3 điểm mạnh

1. **KPI cards** ở đầu tab → người dùng nắm ngay 3 chỉ số quan trọng nhất trước khi đọc biểu đồ
2. **Area Chart** phù hợp cho xu hướng tích lũy theo thời gian — nhấn mạnh tổng diện tích tốt hơn Line Chart
3. **Màu sắc navy + cam** tạo độ tương phản tốt, đọc được cho người khiếm thị màu một phần

### 5 cải tiến cấp bách (theo thứ tự ưu tiên)

| # | Vấn đề | Giải pháp |
|---|---|---|
| 1 | **Pie Chart không thể hiện được xu hướng theo thời gian** | Thay bằng Donut Chart (thời điểm hiện tại) + 100% Stacked Bar (xu hướng nhiều năm) — dual chart |
| 2 | **Area Chart thiếu annotation sự kiện quan trọng** | Thêm annotation "Thi trực tiếp sau COVID" tại năm 2022, "Đổi phương thức thi" tại 2025 |
| 3 | **Grouped Bar Chart điểm TB quá nhiều thanh** (9 môn × 5 năm = 45 cột) | Đổi sang Line Chart với 1 line/môn, trục X là năm — dễ đọc xu hướng hơn nhiều |
| 4 | **Font size KPI cards quá nhỏ** trên màn hình 1366×768 | Tăng font size metric lên ≥ 32px, label lên ≥ 14px |
| 5 | **Không có text description** giải thích từng biểu đồ | Thêm `st.caption()` 1–2 câu bên dưới mỗi chart, giải thích insight chính |

### Cải tiến cụ thể

- Đối với dual chart: Donut bên trái (snapshot năm được chọn) + Stacked Bar bên phải (trend 2020–2024)
- Dùng chung `KHOI_COLORS` dict để màu nhất quán giữa 2 chart
- Stacked Bar dùng `barnorm="percent"` với `barmode="stack"` để trục Y là 0–100%

---

## 3) Priority actions

1. Tạo `make_subplots(1,2, specs=[["domain","xy"]])` cho dual chart Donut + Stacked Bar
2. Thêm vertical line annotation lên Area Chart tại x=2021 (COVID), x=2022 (trở lại bình thường)
3. Đổi Horizontal Grouped Bar → Multi-line Chart cho điểm TB
4. Tăng CSS font size KPI: `st.metric()` với CSS override
5. Thêm `st.caption()` hoặc `st.info()` cho mỗi phần

---

## 4) Manual verification checklist

- [ ] Sau khi thay Pie → Dual Chart: kiểm tra tổng % các khối = 100% mỗi năm
- [ ] Màu KHOI_COLORS phải nhất quán giữa Donut và Stacked Bar
- [ ] KPI cards hiển thị đúng số liệu khi filter năm thay đổi
- [ ] Line Chart điểm TB: 9 lines, mỗi line = 1 môn, 5 điểm (2020–2024)

---

## 5) Block dán vào `ai-trace.md`

```
- Helper: dashboard-critic
- Kết quả: 3 điểm mạnh, 5 cải tiến cấp bách
- Áp dụng: 4/5 cải tiến (bỏ đề xuất 3 — giữ Line Chart thay vì Heatmap table)
- File output: logs/generated/session06_critic_tab1.md
```

**Giải thích 60–90 giây cho vấn đáp (tiếng Việt):**

> "Tab 1 là tổng quan dashboard — nhóm dùng 3 KPI cards để người dùng nắm ngay 3 chỉ số quan trọng nhất. Sau khi AI phê bình, nhóm nhận ra Pie Chart không thể hiện được xu hướng theo thời gian, nên thay bằng Dual Chart gồm Donut bên trái hiển thị cơ cấu khối thi của năm đang chọn, và 100% Stacked Bar bên phải hiển thị xu hướng thay đổi qua 5 năm. Đề xuất đổi Grouped Bar sang Heatmap table bị nhóm bác bỏ — chọn Line Chart để thể hiện xu hướng rõ hơn."
