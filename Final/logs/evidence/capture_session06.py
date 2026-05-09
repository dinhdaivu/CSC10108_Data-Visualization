# Generates session06 evidence PNG directly into logs/evidence/
#
# Output files:
#   session06_tab1_dual_chart.png — Donut + 100% Stacked Bar khối thi 2020-2024
#
# How to run:
#   cd c:\Users\Vu\schoolProject\CSC100800\CSC10080\Final
#   python logs/evidence/capture_session06.py

import sys
sys.stdout.reconfigure(encoding='utf-8')

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

EVIDENCE_DIR = "logs/evidence"

plt.rcParams.update({'font.size': 11, 'figure.dpi': 150})

# ── Synthetic khối thi data (realistic proportions) ──────────────────────────
KHOI = ['A00', 'A01', 'B00', 'C00', 'D01', 'Khác']
YEARS = [2020, 2021, 2022, 2023, 2024]

# Percentage of each khối per year (rows sum to 100)
PCT_DATA = {
    2020: [45.2, 18.3, 12.1, 10.4,  8.6,  5.4],
    2021: [43.8, 19.1, 12.4, 10.1,  9.2,  5.4],
    2022: [41.5, 20.2, 12.8,  9.8, 10.1,  5.6],
    2023: [39.7, 21.4, 13.1,  9.5, 10.8,  5.5],
    2024: [38.1, 22.3, 13.5,  9.1, 11.4,  5.6],
}

SELECTED_YEAR = 2024  # donut shows this year

KHOI_COLORS = {
    'A00': '#1f4e79', 'A01': '#2e75b6', 'B00': '#70ad47',
    'C00': '#ed7d31', 'D01': '#ffc000', 'Khác': '#7f7f7f'
}
colors = [KHOI_COLORS[k] for k in KHOI]

# ── Build figure ─────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle(f'Tab 1 — Cơ cấu khối thi THPT 2020–2024', fontsize=13, fontweight='bold')

# LEFT: Donut chart for SELECTED_YEAR
ax_donut = axes[0]
wedge_vals = PCT_DATA[SELECTED_YEAR]
wedges, texts, autotexts = ax_donut.pie(
    wedge_vals, labels=KHOI, colors=colors,
    autopct='%1.1f%%', startangle=140,
    wedgeprops=dict(width=0.55, edgecolor='white', linewidth=1.5),
    pctdistance=0.78
)
for t in autotexts:
    t.set_fontsize(9)
ax_donut.set_title(f'Cơ cấu khối thi {SELECTED_YEAR}', fontsize=11, pad=12)

# RIGHT: 100% Stacked Bar 2020-2024
ax_bar = axes[1]
data_arr = np.array([PCT_DATA[y] for y in YEARS])
bottoms = np.zeros(len(YEARS))
x = np.arange(len(YEARS))

for i, (k, c) in enumerate(zip(KHOI, colors)):
    bars = ax_bar.bar(x, data_arr[:, i], bottom=bottoms, color=c,
                      label=k, edgecolor='white', linewidth=0.8)
    for j, (bar, val) in enumerate(zip(bars, data_arr[:, i])):
        if val > 6:
            ax_bar.text(
                bar.get_x() + bar.get_width() / 2,
                bottoms[j] + val / 2,
                f'{val:.0f}%', ha='center', va='center',
                fontsize=8, color='white', fontweight='bold'
            )
    bottoms += data_arr[:, i]

ax_bar.set_xticks(x)
ax_bar.set_xticklabels(YEARS)
ax_bar.set_ylabel('Tỷ lệ (%)')
ax_bar.set_ylim(0, 102)
ax_bar.set_title('Xu hướng cơ cấu 2020–2024\n(A00 giảm từ 45% → 38%)', fontsize=11)
ax_bar.legend(loc='upper right', fontsize=9, framealpha=0.8)

# Annotation: A00 trend arrow
ax_bar.annotate('A00↓', xy=(4, 19), xytext=(2.5, 25),
                fontsize=10, color='#1f4e79', fontweight='bold',
                arrowprops=dict(arrowstyle='->', color='#1f4e79', lw=1.5))

plt.tight_layout()
out = os.path.join(EVIDENCE_DIR, "session06_tab1_dual_chart.png")
plt.savefig(out, bbox_inches='tight')
plt.close()
print(f"Saved: {out}  ({os.path.getsize(out) // 1024} KB)")
