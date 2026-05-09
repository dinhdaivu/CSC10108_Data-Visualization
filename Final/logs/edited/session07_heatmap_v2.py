# Correlation Heatmap Component — Human-edited version
# Session 07 (05/05/2026) | Edited by: Đinh Đại Vũ
# Changes from AI version: added MON_LABELS dict, render_heatmap() function,
#   min_periods=100, proper NaN masking with k=1, Vietnamese hover template

import plotly.graph_objects as go
import numpy as np, pandas as pd
import streamlit as st

SCORE_COLS = ['toan', 'ngu_van', 'ngoai_ngu', 'vat_ly', 'hoa_hoc',
              'sinh_hoc', 'lich_su', 'dia_ly', 'gdcd']

MON_LABELS = {
    'toan': 'Toán', 'ngu_van': 'Văn', 'ngoai_ngu': 'Ngoại ngữ',
    'vat_ly': 'Lý', 'hoa_hoc': 'Hóa', 'sinh_hoc': 'Sinh',
    'lich_su': 'Sử', 'dia_ly': 'Địa', 'gdcd': 'GDCD'
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
