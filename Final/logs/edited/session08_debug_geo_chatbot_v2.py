# Debug Fix: Choropleth thiếu tỉnh + Chatbot encode — Human-edited version
# Session 08 (08/05/2026) | Edited by: Nguyễn Đỗ Bảo
# Changes from AI version: manual TINH_MAP dict instead of unidecode auto,
#   use plotly.io.to_image instead of st.pyplot() buffer

import plotly.io as pio
import base64, pandas as pd

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
def fig_to_base64(fig) -> str:
    img_bytes = pio.to_image(fig, format="png", width=900, height=500, scale=2)
    return base64.b64encode(img_bytes).decode("utf-8")
