import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="Hệ thống Phân tích Điểm thi", layout="wide")

# Tùy chỉnh CSS để khung Dashboard gọn gàng hơn
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- 2. HÀM LOAD DỮ LIỆU TỐI ƯU ---
@st.cache_data
def load_all_data():
    all_df = []
    for year in [2021, 2022, 2023, 2024]:
        path = f"data/thpt{year}.csv"
        if os.path.exists(path):
            df_y = pd.read_csv(path, low_memory=False)
            df_y['Nam'] = year
            all_df.append(df_y)
    return pd.concat(all_df, ignore_index=True) if all_df else pd.DataFrame()

df = load_all_data()

# Dừng chương trình cảnh báo nếu không có dữ liệu
if df.empty:
    st.error("Không tìm thấy dữ liệu. Vui lòng kiểm tra lại thư mục 'data' và các file CSV.")
    st.stop()

# --- 3. SIDEBAR / BỘ LỌC TẬP TRUNG ---
st.sidebar.header("🎯 Điều khiển Dashboard")
subjects = ['Toan', 'NguVan', 'NgoaiNgu', 'VatLy', 'HoaHoc', 'SinhHoc', 'LichSu', 'DiaLy', 'GDCD']
selected_sub = st.sidebar.selectbox("Chọn môn học phân tích", subjects)
year_range = st.sidebar.slider("Khoảng năm phân tích", 2021, 2024, (2021, 2024))

# Lọc dữ liệu theo lựa chọn
df_filtered = df[(df['Nam'] >= year_range[0]) & (df['Nam'] <= year_range[1])].dropna(subset=[selected_sub])

# --- 4. GIAO DIỆN CHÍNH ---
st.title(f"📊 Dashboard Phân tích Môn {selected_sub}")

# HÀNG 1: KPI CARDS
# Lấy dữ liệu năm gần nhất để hiển thị số liệu tức thời
latest_year = year_range[1]
df_latest = df_filtered[df_filtered['Nam'] == latest_year]

m1, m2, m3, m4 = st.columns(4)

if not df_latest.empty:
    avg = df_latest[selected_sub].mean()
    
    # [ĐÃ SỬA LỖI]: Tính Mode an toàn, chống crash khi dữ liệu rỗng
    modes = df_latest[selected_sub].mode()
    mode = modes.iloc[0] if not modes.empty else 0
    
    pass_rate = (df_latest[selected_sub] >= 5).mean() * 100
    top_rate = (df_latest[selected_sub] >= 8).mean() * 100

    m1.metric("Điểm Trung Bình", f"{avg:.2f}", f"{avg - 5:.1f} vs Yêu cầu")
    m2.metric("Điểm Phổ Biến (Mode)", f"{mode:.1f}")
    m3.metric("Tỷ lệ Trên Trung Bình", f"{pass_rate:.1f}%")
    m4.metric("Tỷ lệ Điểm Giỏi (>=8)", f"{top_rate:.1f}%")

st.markdown("---")

# HÀNG 2: BIỂU ĐỒ XU HƯỚNG VÀ PHỔ ĐIỂM (2 CỘT)
c1, c2 = st.columns(2)

with c1:
    st.subheader("📈 Xu hướng qua các năm")
    trend_data = df_filtered.groupby('Nam')[selected_sub].mean().reset_index()
    fig_line = px.line(trend_data, x='Nam', y=selected_sub, markers=True, template="plotly_white")
    fig_line.update_layout(xaxis=dict(tickmode='linear'))
    # [ĐÃ CẬP NHẬT CÚ PHÁP MỚI CỦA STREAMLIT]
    st.plotly_chart(fig_line, width="stretch")

with c2:
    st.subheader(f"🎯 Phân phối điểm năm {latest_year}")
    fig_hist = px.histogram(df_latest, x=selected_sub, nbins=20, text_auto=True, template="plotly_white")
    # [ĐÃ CẬP NHẬT CÚ PHÁP MỚI CỦA STREAMLIT]
    st.plotly_chart(fig_hist, width="stretch")

# HÀNG 3: CẤU TRÚC HỌC LỰC (TOÀN CHIỀU RỘNG)
st.subheader("🧱 Cấu trúc học lực theo nhóm điểm (%)")

# Logic chia nhóm
bins = [-1, 4.99, 7.99, 10]
labels = ['Dưới 5', '5 - 8', 'Trên 8']
df_filtered['Nhom'] = pd.cut(df_filtered[selected_sub], bins=bins, labels=labels)

# Tính toán tỷ lệ % theo năm
struct_data = df_filtered.groupby(['Nam', 'Nhom'], observed=False).size().reset_index(name='Count')
struct_data['Percent'] = struct_data.groupby('Nam')['Count'].transform(lambda x: (x/x.sum())*100)

fig_struct = px.bar(struct_data, x='Nam', y='Percent', color='Nhom', 
                    text_auto='.1f', barmode='stack',
                    color_discrete_map={'Dưới 5': '#EF553B', '5 - 8': '#636EFA', 'Trên 8': '#00CC96'})
# [ĐÃ CẬP NHẬT CÚ PHÁP MỚI CỦA STREAMLIT]
st.plotly_chart(fig_struct, width="stretch")