# Choropleth Map Component — Human-edited version
# Session 07 (05/05/2026) | Edited by: Đinh Đại Vũ
# Changes from AI version: added @st.cache_data, render_choropleth() function,
#   rank column, corrected center coords (15.5, 107.5), YlOrRd color scale

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
