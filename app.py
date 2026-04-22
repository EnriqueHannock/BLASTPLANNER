"""
MUBAS Blast Designer - Production Blast Planning Tool
Group 4 | BMEN 5 | Malawi University of Business and Applied Sciences
"""

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors as rl_colors
from reportlab.lib.units import inch
import io

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="MUBAS Blast Designer",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  GLOBAL CSS — Engineering Steel/Teal Theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Share+Tech+Mono&family=Exo+2:wght@300;400;600;700&display=swap');

:root {
    --bg-dark:        #07090f;
    --bg-panel:       #0b0e17;
    --bg-card:        #0f1220;
    --bg-input:       #141828;
    --eng-primary:    #1e7db8;
    --eng-accent:     #2aabcc;
    --eng-steel:      #3a6e94;
    --eng-green:      #1a8850;
    --eng-red:        #a03030;
    --eng-cyan:       #1499c4;
    --text-primary:   #c8d4e4;
    --text-muted:     #4e6278;
    --border:         #182035;
    --border-primary: rgba(30,125,184,0.45);
    --glow-primary:   0 0 16px rgba(30,125,184,0.35);
}

html, body, [class*="css"] {
    font-family: 'Exo 2', sans-serif !important;
    background-color: var(--bg-dark) !important;
    color: var(--text-primary) !important;
}
.stApp { background: var(--bg-dark) !important; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #060810 0%, #0a0d18 100%) !important;
    border-right: 2px solid var(--border-primary) !important;
}
[data-testid="stSidebar"] * { color: var(--text-primary) !important; }

[data-testid="stAppViewContainer"] > .main > .block-container {
    padding: 1.5rem 2.5rem !important;
    max-width: 1400px !important;
}

h1, h2, h3 {
    font-family: 'Rajdhani', sans-serif !important;
    letter-spacing: 0.08em !important;
    color: var(--eng-primary) !important;
}
h1 { font-size: 2.4rem !important; font-weight: 700 !important; }
h2 { font-size: 1.7rem !important; font-weight: 600 !important; }
h3 { font-size: 1.3rem !important; }

[data-testid="stNumberInput"] input {
    background: var(--bg-input) !important;
    border: 1px solid var(--border) !important;
    border-radius: 5px !important;
    color: #6ab4d8 !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 1.05rem !important;
    transition: border 0.2s, box-shadow 0.2s !important;
}
[data-testid="stNumberInput"] input:focus {
    border-color: var(--eng-primary) !important;
    box-shadow: var(--glow-primary) !important;
    outline: none !important;
}

label, .stNumberInput label, .stSelectbox label, .stCheckbox label {
    color: var(--text-muted) !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}

/* PRIMARY BUTTON — Steel Blue */
button[kind="primaryFormSubmit"],
button[kind="primary"],
[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, #0d3d5c 0%, #1e7db8 55%, #2490d0 100%) !important;
    color: #ffffff !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    border: 1px solid rgba(30,125,184,0.7) !important;
    border-radius: 6px !important;
    padding: 0.65rem 2.2rem !important;
    box-shadow: 0 4px 18px rgba(30,125,184,0.5), inset 0 1px 0 rgba(255,255,255,0.08) !important;
    transition: transform 0.15s, box-shadow 0.15s !important;
    cursor: pointer !important;
    text-shadow: 0 1px 3px rgba(0,0,0,0.5) !important;
}
button[kind="primaryFormSubmit"]:hover,
[data-testid="baseButton-primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 7px 26px rgba(30,125,184,0.65) !important;
}

/* SECONDARY BUTTON — Dark Teal */
[data-testid="baseButton-secondary"],
button[kind="secondary"] {
    background: linear-gradient(135deg, #0c1e28 0%, #122838 100%) !important;
    color: #4ab0d8 !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    border: 1px solid #1e5070 !important;
    border-radius: 6px !important;
    padding: 0.6rem 1.8rem !important;
    box-shadow: 0 0 12px rgba(30,125,184,0.2) !important;
    transition: transform 0.15s, box-shadow 0.15s !important;
}
[data-testid="baseButton-secondary"]:hover {
    background: linear-gradient(135deg, #122838 0%, #183850 100%) !important;
    color: #78ccee !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 0 22px rgba(30,125,184,0.45) !important;
}

[data-testid="stAlert"] {
    border-radius: 6px !important;
    font-family: 'Exo 2', sans-serif !important;
    border-left-width: 4px !important;
}

hr { border-color: var(--border-primary) !important; opacity: 0.4 !important; }

[data-testid="stTable"] table, .dataframe {
    background: var(--bg-card) !important;
    border-radius: 8px !important;
    overflow: hidden !important;
    border: 1px solid var(--border) !important;
}
[data-testid="stTable"] th, .dataframe thead th {
    background: #0e1828 !important;
    color: var(--eng-primary) !important;
    font-family: 'Rajdhani', sans-serif !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    font-size: 0.88rem !important;
    padding: 0.65rem 1rem !important;
    border-bottom: 1px solid var(--border-primary) !important;
}
[data-testid="stTable"] td, .dataframe tbody td {
    background: var(--bg-card) !important;
    color: var(--text-primary) !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.92rem !important;
    padding: 0.55rem 1rem !important;
    border-bottom: 1px solid var(--border) !important;
}
.dataframe tbody tr:hover td { background: #111828 !important; }

[data-testid="metric-container"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-top: 2px solid var(--eng-primary) !important;
    border-radius: 8px !important;
    padding: 0.8rem 1rem !important;
}
[data-testid="stMetricLabel"] {
    color: var(--text-muted) !important;
    font-family: 'Rajdhani', sans-serif !important;
    letter-spacing: 0.1em !important;
    font-size: 0.8rem !important;
    text-transform: uppercase !important;
}
[data-testid="stMetricValue"] {
    color: var(--eng-accent) !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 1.6rem !important;
}
[data-testid="stMetricDelta"] { font-family: 'Share Tech Mono', monospace !important; }

[data-testid="stExpander"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}

.section-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--eng-primary);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--border-primary);
}

.hero-banner {
    background: linear-gradient(135deg, #06080e 0%, #0d1020 50%, #06080e 100%);
    border: 1px solid var(--border-primary);
    border-left: 4px solid var(--eng-primary);
    border-radius: 12px;
    padding: 1.8rem 2.4rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -40%; right: -5%;
    width: 260px; height: 260px;
    background: radial-gradient(circle, rgba(30,125,184,0.07) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 2.4rem;
    font-weight: 700;
    color: var(--eng-primary);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    line-height: 1.1;
    margin: 0;
}
.hero-subtitle {
    font-family: 'Exo 2', sans-serif;
    font-size: 1rem;
    color: var(--text-muted);
    letter-spacing: 0.05em;
    margin-top: 0.35rem;
}
.hero-badge {
    display: inline-block;
    background: rgba(30,125,184,0.1);
    border: 1px solid var(--border-primary);
    border-radius: 4px;
    padding: 0.2rem 0.8rem;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.76rem;
    color: var(--eng-primary);
    letter-spacing: 0.1em;
    margin-right: 0.4rem;
    margin-top: 0.6rem;
}
.team-chip {
    display: inline-block;
    background: rgba(30,125,184,0.08);
    border: 1px solid rgba(30,125,184,0.3);
    border-radius: 4px;
    padding: 0.25rem 0.75rem;
    font-family: 'Exo 2', sans-serif;
    font-size: 0.85rem;
    color: #4ab0d8;
    margin: 0.2rem;
}
.status-ok {
    background: rgba(26,136,80,0.1);
    border: 1px solid rgba(26,136,80,0.4);
    border-left: 4px solid var(--eng-green);
    border-radius: 6px;
    padding: 0.75rem 1.2rem;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.95rem;
    color: #33bb77;
    margin: 0.5rem 0;
}
.status-fail {
    background: rgba(160,48,48,0.1);
    border: 1px solid rgba(160,48,48,0.4);
    border-left: 4px solid var(--eng-red);
    border-radius: 6px;
    padding: 0.75rem 1.2rem;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.95rem;
    color: #cc4444;
    margin: 0.5rem 0;
}
.input-group-label {
    font-family: 'Rajdhani', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    color: var(--eng-accent);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.4rem 0;
    margin-bottom: 0.2rem;
    border-bottom: 1px dashed rgba(42,171,204,0.35);
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────
if 'history' not in st.session_state:
    st.session_state.history = []

# ─────────────────────────────────────────────
#  PDF GENERATOR
# ─────────────────────────────────────────────
def create_pdf(data: dict, actual_pf: float, pf_target: float) -> io.BytesIO:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, rightMargin=inch*0.75, leftMargin=inch*0.75,
        topMargin=inch, bottomMargin=inch,
    )
    styles = getSampleStyleSheet()
    blue   = rl_colors.HexColor("#1e7db8")
    dark   = rl_colors.HexColor("#0b0e17")
    mid    = rl_colors.HexColor("#0f1220")

    title_style = ParagraphStyle(
        "title", parent=styles["Title"],
        fontName="Helvetica-Bold", fontSize=20,
        textColor=blue, spaceAfter=6, leading=24,
    )
    sub_style = ParagraphStyle(
        "sub", parent=styles["Normal"],
        fontName="Helvetica", fontSize=10,
        textColor=rl_colors.HexColor("#4e6278"), spaceAfter=4,
    )
    heading_style = ParagraphStyle(
        "heading2", parent=styles["Normal"],
        fontName="Helvetica-Bold", fontSize=12,
        textColor=blue, spaceBefore=14, spaceAfter=6,
    )
    body_style = ParagraphStyle(
        "body", parent=styles["Normal"],
        fontName="Helvetica", fontSize=10,
        textColor=rl_colors.HexColor("#c8d4e4"),
    )

    content = [
        Paragraph("MUBAS BLAST DESIGN REPORT", title_style),
        Paragraph("Malawi University of Business and Applied Sciences", sub_style),
        Paragraph(f"Generated: {datetime.now().strftime('%d %B %Y  |  %H:%M:%S')}", sub_style),
        HRFlowable(width="100%", thickness=1, color=blue, spaceAfter=12),
        Paragraph("DESIGN PARAMETERS", heading_style),
    ]

    table_data = [["Parameter", "Value"]]
    for k, v in data.items():
        table_data.append([k, str(v)])

    param_table = Table(table_data, colWidths=[3.5*inch, 3.5*inch])
    param_table.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0), dark),
        ("TEXTCOLOR",     (0,0), (-1,0), blue),
        ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,0), 10),
        ("BOTTOMPADDING", (0,0), (-1,0), 8),
        ("BACKGROUND",    (0,1), (-1,-1), mid),
        ("TEXTCOLOR",     (0,1), (-1,-1), rl_colors.HexColor("#c8d4e4")),
        ("FONTNAME",      (0,1), (-1,-1), "Helvetica"),
        ("FONTSIZE",      (0,1), (-1,-1), 10),
        ("ROWBACKGROUNDS",(0,1), (-1,-1),
            [rl_colors.HexColor("#0f1220"), rl_colors.HexColor("#111828")]),
        ("GRID", (0,0), (-1,-1), 0.5, rl_colors.HexColor("#182035")),
        ("LEFTPADDING",   (0,0), (-1,-1), 12),
        ("RIGHTPADDING",  (0,0), (-1,-1), 12),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ]))
    content.append(param_table)
    content.append(Spacer(1, 16))
    content.append(Paragraph("POWDER FACTOR VALIDATION", heading_style))

    pf_status = "PASS" if abs(actual_pf - pf_target) <= 0.05 else "FAIL"
    pf_color  = rl_colors.HexColor("#22aa55") if "PASS" in pf_status else rl_colors.HexColor("#cc4444")
    pf_style  = ParagraphStyle("pf", parent=body_style, textColor=pf_color, fontName="Helvetica-Bold")
    content.append(Paragraph(
        f"{pf_status} — Actual PF: {actual_pf:.3f} kg/m3  |  Target PF: {pf_target:.3f} kg/m3",
        pf_style
    ))
    content.append(Spacer(1, 16))
    content.append(HRFlowable(width="100%", thickness=0.5,
                               color=rl_colors.HexColor("#182035"), spaceAfter=8))
    content.append(Paragraph(
        "Report produced by MUBAS Blast Designer v2.0  ·  Group 4 · BMEN 5",
        ParagraphStyle("footer", parent=body_style,
                       textColor=rl_colors.HexColor("#2a3858"), fontSize=8)
    ))
    doc.build(content)
    buffer.seek(0)
    return buffer

# ─────────────────────────────────────────────
#  FRAGMENTATION CHART
# ─────────────────────────────────────────────
def draw_fragmentation_chart(x50: float, n_val: float, style_label: str):
    fig, ax = plt.subplots(figsize=(9, 4))
    fig.patch.set_facecolor("#0b0e17")
    ax.set_facecolor("#0f1220")

    sizes   = np.linspace(1, 1000, 300)
    passing = 100 * (1 - np.exp(-0.693 * (sizes / x50) ** n_val))

    ax.fill_between(sizes, passing, alpha=0.12, color="#1e7db8")
    ax.plot(sizes, passing, color="#1e7db8", linewidth=2.5, label=style_label)
    ax.axvline(x50, color="#2aabcc", linestyle="--", linewidth=1.5,
               alpha=0.85, label=f"x50 = {x50:.0f} mm")
    ax.axhline(50, color="#2aabcc", linestyle="--", linewidth=1, alpha=0.45)

    ax.set_xlabel("Fragment Size (mm)", color="#4e6278", fontsize=10)
    ax.set_ylabel("Cumulative Passing (%)", color="#4e6278", fontsize=10)
    ax.set_title("Rosin-Rammler Fragmentation Curve", color="#1e7db8",
                 fontsize=12, fontweight="bold", pad=12)
    ax.tick_params(colors="#4e6278")
    for spine in ax.spines.values():
        spine.set_edgecolor("#182035")
    ax.grid(True, color="#182035", linewidth=0.8, linestyle="--", alpha=0.7)
    ax.set_xlim(0, 1000)
    ax.set_ylim(0, 105)
    ax.legend(facecolor="#0b0e17", edgecolor="#182035",
              labelcolor="#c8d4e4", fontsize=9)
    fig.tight_layout(pad=1.5)
    return fig

# ─────────────────────────────────────────────
#  BLAST GEOMETRY DIAGRAM
# ─────────────────────────────────────────────
def draw_blast_diagram(burden, spacing, h_bench, stemming_len, lc):
    fig, ax = plt.subplots(figsize=(5, 7))
    fig.patch.set_facecolor("#0b0e17")
    ax.set_facecolor("#0f1220")

    scale   = 1.0 / max(h_bench + 1, 1)
    total_d = h_bench

    ax.axhline(0, color="#2a4a6a", linewidth=2.5, zorder=5)
    ax.fill_between([-2, 2], [0, 0],
                    [-total_d*scale - 0.5, -total_d*scale - 0.5],
                    color="#0a1018", alpha=0.7)
    ax.fill_between([-2, 2], [0, 0], [0.6, 0.6],
                    color="#101820", alpha=0.45)

    hw = 0.15
    ax.fill_betweenx([-total_d*scale, 0], [-hw, -hw], [hw, hw],
                     color="#0f1220", alpha=1.0)
    ax.add_patch(mpatches.Rectangle(
        (-hw, -total_d*scale), 2*hw, total_d*scale,
        linewidth=1.5, edgecolor="#243048", facecolor="#0f1220", zorder=6
    ))

    # Stemming
    stem_top = 0
    stem_bot = -stemming_len * scale
    ax.fill_betweenx([stem_bot, stem_top], [-hw, -hw], [hw, hw],
                     color="#3a6080", alpha=0.75, zorder=7)
    ax.text(hw+0.05, (stem_top+stem_bot)/2,
            f"Stemming\n{stemming_len:.1f} m",
            color="#5a90b0", fontsize=7, va="center", fontfamily="monospace")

    # Explosive
    expl_top = stem_bot
    expl_bot = -total_d * scale
    ax.fill_betweenx([expl_bot, expl_top],
                     [-hw+0.02, -hw+0.02], [hw-0.02, hw-0.02],
                     color="#1e7db8", alpha=0.85, zorder=8)
    ax.text(hw+0.05, (expl_top+expl_bot)/2,
            f"Explosive\n{lc:.1f} m",
            color="#1e7db8", fontsize=7, va="center", fontfamily="monospace")

    # Bench height arrow
    ax.annotate("", xy=(-hw-0.18, -h_bench*scale),
                xytext=(-hw-0.18, 0),
                arrowprops=dict(arrowstyle="<->", color="#2aabcc", lw=1.2))
    ax.text(-hw-0.38, -h_bench*scale/2,
            f"H={h_bench:.1f} m",
            color="#2aabcc", fontsize=7, va="center", fontfamily="monospace")

    # Burden arrow
    ax.annotate("", xy=(burden*scale*0.6, 0.35),
                xytext=(0, 0.35),
                arrowprops=dict(arrowstyle="<->", color="#1e7db8", lw=1.5))
    ax.text(burden*scale*0.3, 0.48,
            f"B={burden:.2f} m",
            color="#1e7db8", fontsize=7.5, ha="center", fontfamily="monospace")

    ax.text(-1.7, 0.15, "SURFACE", color="#2a4a6a",
            fontsize=7.5, fontweight="bold", fontfamily="monospace")

    ax.set_xlim(-2, 2)
    ax.set_ylim(-total_d*scale - 0.5, 1.0)
    ax.axis("off")
    ax.set_title("Hole Cross-Section", color="#1e7db8",
                 fontsize=10, fontweight="bold", pad=8)
    fig.tight_layout(pad=1)
    return fig

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:

    # ── LOGO URL INPUT ──
    logo_url = st.text_input(
        "Institution Logo URL",
        value="",
        placeholder="Paste image URL here...",
        help="Direct URL to your institution logo (PNG, JPG, SVG)",
    )
    if logo_url.strip():
        st.markdown(
            f"""<div style='text-align:center; padding:0.5rem 0 0.3rem;'>
            <img src='{logo_url.strip()}'
                 style='max-width:150px; max-height:90px; object-fit:contain;
                        border-radius:6px; border:1px solid rgba(30,125,184,0.2);'
                 onerror="this.style.display='none'">
            </div>""",
            unsafe_allow_html=True,
        )

    st.markdown("""
    <div style='text-align:center; padding:0.8rem 0 0.5rem;'>
        <div style='font-family:Rajdhani,sans-serif; font-size:1.7rem;
                    font-weight:700; color:#1e7db8; letter-spacing:0.1em;
                    margin-top:0.5rem; line-height:1.1;'>
            BLAST<br>DESIGNER
        </div>
        <div style='font-family:Share Tech Mono,monospace; font-size:0.7rem;
                    color:#2a3858; margin-top:0.4rem; letter-spacing:0.12em;'>
            MUBAS · BMEN 5 · v2.0
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("""
    <div style='font-family:Rajdhani,sans-serif; font-weight:700;
                color:#4e6278; font-size:0.78rem; letter-spacing:0.14em;
                text-transform:uppercase; margin-bottom:0.7rem;'>
        Navigation
    </div>
    """, unsafe_allow_html=True)

    nav_items = [
        "Design Inputs",
        "Results & Metrics",
        "Fragmentation",
        "History",
    ]
    for label in nav_items:
        st.markdown(f"""
        <div style='padding:0.45rem 0.8rem; border-radius:5px;
                    background:rgba(30,125,184,0.05);
                    border-left:2px solid rgba(30,125,184,0.3);
                    margin-bottom:0.3rem; font-family:Exo 2,sans-serif;
                    font-size:0.9rem; color:#7898b8;'>
            {label}
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.markdown("""
    <div style='font-family:Rajdhani,sans-serif; font-weight:700;
                color:#4e6278; font-size:0.78rem; letter-spacing:0.14em;
                text-transform:uppercase; margin-bottom:0.6rem;'>
        Quick Reference
    </div>
    """, unsafe_allow_html=True)

    with st.expander("Blasting Formulae"):
        st.markdown("""
        <div style='font-family:Share Tech Mono,monospace; font-size:0.78rem;
                    color:#7898b8; line-height:1.9;'>
        <b style='color:#1e7db8;'>Burden</b><br>B = Kb × d<br><br>
        <b style='color:#1e7db8;'>Spacing</b><br>S = Ks × B<br><br>
        <b style='color:#1e7db8;'>Stemming</b><br>T = 0.7 × B<br><br>
        <b style='color:#1e7db8;'>Charge Wt</b><br>W = π/4 × d² × ρ × Lc<br><br>
        <b style='color:#1e7db8;'>Powder Factor</b><br>PF = W / (B × S × H)
        </div>
        """, unsafe_allow_html=True)

    with st.expander("Constants Used"):
        st.markdown("""
        <div style='font-family:Share Tech Mono,monospace; font-size:0.78rem;
                    color:#7898b8; line-height:1.9;'>
        Kb = 25 &nbsp;(burden factor)<br>
        Ks = 1.25 (spacing ratio)<br>
        Rosin-Rammler fragmentation<br>
        x50 model via UCS scaling
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.markdown("""
    <div style='font-family:Share Tech Mono,monospace; font-size:0.68rem;
                color:#1e2840; text-align:center; line-height:1.7;'>
    © 2025 MUBAS · Group 4<br>
    Mining Engineering Dept.
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HERO BANNER
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div style="display:flex; align-items:flex-start; gap:1.5rem; flex-wrap:wrap;">
        <div style="flex:1; min-width:260px;">
            <p class="hero-title">BLAST DESIGNER</p>
            <p class="hero-subtitle">
                Production Blast Planning &amp; Fragmentation Analysis System
            </p>
            <div style="margin-top:0.7rem;">
                <span class="hero-badge">MUBAS</span>
                <span class="hero-badge">BMEN 5</span>
                <span class="hero-badge">GROUP 4</span>
                <span class="hero-badge">v2.0</span>
            </div>
        </div>
        <div style="display:flex; flex-direction:column; gap:0.3rem; min-width:200px;">
            <div style="font-family:Rajdhani,sans-serif; font-size:0.75rem;
                        color:#4e6278; letter-spacing:0.14em;
                        text-transform:uppercase; margin-bottom:0.3rem;">
                Project Team
            </div>
            <span class="team-chip">Enrique Hannock</span>
            <span class="team-chip">Saidi Ibrahim</span>
            <span class="team-chip">Promise Magola</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  INPUT FORM
# ─────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    DESIGN INPUTS
</div>
""", unsafe_allow_html=True)

with st.form("blast_form", clear_on_submit=False):
    col1, col2, col3 = st.columns([1, 1, 1], gap="large")

    with col1:
        st.markdown('<div class="input-group-label">Hole Geometry</div>',
                    unsafe_allow_html=True)
        d_mm = st.number_input(
            "Hole Diameter (mm)", min_value=32.0, max_value=400.0,
            value=90.0, step=5.0, help="Drill bit diameter in millimetres"
        )
        h_bench = st.number_input(
            "Bench Height (m)", min_value=1.0, max_value=50.0,
            value=9.0, step=0.5, help="Height of the bench face"
        )
        ucs = st.number_input(
            "Rock UCS (MPa)", min_value=30.0, max_value=400.0,
            value=45.0, step=10.0, help="Uniaxial Compressive Strength"
        )

    with col2:
        st.markdown('<div class="input-group-label">Explosive Parameters</div>',
                    unsafe_allow_html=True)
        rho_anfo = st.number_input(
            "ANFO Density (kg/m3)", min_value=400.0, max_value=1500.0,
            value=825.0, step=25.0, help="Bulk density of ANFO explosive"
        )
        pf_target = st.number_input(
            "Target Powder Factor (kg/m3)", min_value=0.1, max_value=2.0,
            value=1.0, step=0.1, help="Desired explosive energy per unit volume"
        )

    with col3:
        st.markdown('<div class="input-group-label">Run Analysis</div>',
                    unsafe_allow_html=True)
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        submitted = st.form_submit_button(
            "RUN CALCULATION",
            use_container_width=True,
            type="primary",
        )

# ─────────────────────────────────────────────
#  CALCULATIONS & RESULTS
# ─────────────────────────────────────────────
if submitted:
    d_m          = d_mm / 1000.0
    kb, ks       = 25.0, 1.25
    burden       = kb * d_m
    spacing      = ks * burden
    primary_stem = 0.7 * burden
    total_depth  = h_bench
    lc           = total_depth - primary_stem
    charge_style = "Single Column"

    volume        = burden * spacing * h_bench
    charge_weight = (np.pi * (d_m ** 2) / 4) * rho_anfo * lc
    actual_pf     = charge_weight / volume if volume > 0 else 0.0
    x50           = 380 * (ucs / 45) ** 0.5
    n_val         = 1.0

    # ── KEY METRICS ──
    st.markdown("""
    <div class="section-header" style="margin-top:1.5rem;">
        RESULTS & METRICS
    </div>
    """, unsafe_allow_html=True)

    m1, m2, m3, m4, m5, m6 = st.columns(6, gap="small")
    m1.metric("Burden",        f"{burden:.2f} m")
    m2.metric("Spacing",       f"{spacing:.2f} m")
    m3.metric("Stemming",      f"{primary_stem:.2f} m")
    m4.metric("Total Depth",   f"{total_depth:.2f} m")
    m5.metric("Charge Weight", f"{charge_weight:.1f} kg")
    m6.metric("Actual PF",     f"{actual_pf:.3f} kg/m3",
              delta=f"{actual_pf - pf_target:+.3f} vs target")

    # ── POWDER FACTOR STATUS ──
    tolerance = 0.05
    if abs(actual_pf - pf_target) <= tolerance:
        st.markdown(f"""
        <div class="status-ok">
            POWDER FACTOR MATCH &nbsp;|&nbsp;
            Actual: {actual_pf:.3f} kg/m3 &nbsp;
            Target: {pf_target:.3f} kg/m3 &nbsp;
            Delta = {actual_pf - pf_target:+.4f} kg/m3 (within +/-{tolerance} tolerance)
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="status-fail">
            POWDER FACTOR MISMATCH &nbsp;|&nbsp;
            Actual: {actual_pf:.3f} kg/m3 &nbsp;
            Target: {pf_target:.3f} kg/m3 &nbsp;
            Delta = {actual_pf - pf_target:+.4f} kg/m3 (exceeds +/-{tolerance} tolerance)
        </div>
        """, unsafe_allow_html=True)

    # ── TABLE + DIAGRAM ──
    st.divider()
    tab_col, diag_col = st.columns([1.4, 1], gap="large")

    with tab_col:
        st.markdown("""
        <div class="section-header">
            PARAMETER SUMMARY
        </div>
        """, unsafe_allow_html=True)

        res_df = pd.DataFrame({
            "Parameter": [
                "Hole Diameter", "Bench Height", "Rock UCS",
                "ANFO Density", "Burden (B)", "Spacing (S)",
                "Primary Stemming (T)", "Charge Length (Lc)",
                "Blast Volume", "Charge Weight",
                "Actual Powder Factor", "Target Powder Factor",
                "Charging Style",
            ],
            "Value": [
                f"{d_mm:.0f} mm",        f"{h_bench:.1f} m",    f"{ucs:.0f} MPa",
                f"{rho_anfo:.0f} kg/m3", f"{burden:.3f} m",     f"{spacing:.3f} m",
                f"{primary_stem:.3f} m", f"{lc:.3f} m",
                f"{volume:.2f} m3",      f"{charge_weight:.2f} kg",
                f"{actual_pf:.4f} kg/m3",f"{pf_target:.4f} kg/m3",
                charge_style,
            ],
            "Status": [
                "INPUT", "INPUT", "INPUT",
                "INPUT", "CALC", "CALC",
                "CALC", "CALC",
                "CALC", "CALC",
                "PF",  "INPUT",
                "OPTION",
            ],
        })
        st.dataframe(res_df, use_container_width=True, hide_index=True)

    with diag_col:
        st.markdown("""
        <div class="section-header">
            HOLE CROSS-SECTION
        </div>
        """, unsafe_allow_html=True)
        fig_diag = draw_blast_diagram(
            burden, spacing, h_bench, primary_stem, lc
        )
        st.pyplot(fig_diag, use_container_width=True)
        plt.close(fig_diag)

    # ── FRAGMENTATION ──
    st.divider()
    st.markdown("""
    <div class="section-header">
        FRAGMENTATION PREDICTION (Rosin-Rammler Model)
    </div>
    """, unsafe_allow_html=True)

    frag_col, info_col = st.columns([2, 1], gap="large")

    with frag_col:
        fig_frag = draw_fragmentation_chart(x50, n_val, charge_style)
        st.pyplot(fig_frag, use_container_width=True)
        plt.close(fig_frag)

    with info_col:
        st.markdown(f"""
        <div style='background:#0f1220; border:1px solid #182035;
                    border-left:3px solid #1e7db8; border-radius:8px;
                    padding:1.2rem; font-family:Share Tech Mono,monospace;
                    font-size:0.88rem; color:#7898b8; line-height:2;'>
            <div style='color:#1e7db8; font-weight:bold; margin-bottom:0.5rem;
                        font-family:Rajdhani,sans-serif; font-size:1rem;
                        letter-spacing:0.1em;'>
                MODEL PARAMETERS
            </div>
            <span style='color:#4e6278;'>Median Fragment Size</span><br>
            <span style='color:#1e7db8;'>x50 = {x50:.1f} mm</span><br><br>
            <span style='color:#4e6278;'>Uniformity Index (n)</span><br>
            <span style='color:#2aabcc;'>{n_val:.2f}</span><br><br>
            <span style='color:#4e6278;'>Rock Strength</span><br>
            <span style='color:#3a8ab8;'>{ucs:.0f} MPa (UCS)</span><br><br>
            <span style='color:#4e6278;'>Charge Style</span><br>
            <span style='color:#1a8850;'>{charge_style}</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**Key Passing Sizes**")
        sizes_check = np.array([50, 100, 200, 300, 500, 800])
        pass_vals   = 100 * (1 - np.exp(-0.693 * (sizes_check / x50) ** n_val))
        pass_df = pd.DataFrame({
            "Size (mm)":  sizes_check,
            "% Passing":  [f"{p:.1f}%" for p in pass_vals],
        })
        st.dataframe(pass_df, use_container_width=True, hide_index=True)

    # ── PDF DOWNLOAD ──
    st.divider()
    report_data = {
        "Hole Diameter (mm)":     f"{d_mm:.0f}",
        "Bench Height (m)":       f"{h_bench:.1f}",
        "Rock UCS (MPa)":         f"{ucs:.0f}",
        "ANFO Density (kg/m3)":   f"{rho_anfo:.0f}",
        "Burden B (m)":           f"{burden:.3f}",
        "Spacing S (m)":          f"{spacing:.3f}",
        "Primary Stemming T (m)": f"{primary_stem:.3f}",
        "Charge Length Lc (m)":   f"{lc:.3f}",
        "Blast Volume (m3)":      f"{volume:.2f}",
        "Charge Weight (kg)":     f"{charge_weight:.2f}",
        "Actual Powder Factor":   f"{actual_pf:.4f} kg/m3",
        "Target Powder Factor":   f"{pf_target:.4f} kg/m3",
        "Charging Style":         charge_style,
        "x50 Fragment Size (mm)": f"{x50:.1f}",
        "Uniformity Index n":     f"{n_val:.2f}",
    }
    pdf_buf = create_pdf(report_data, actual_pf, pf_target)

    dl_col, _, _ = st.columns([1, 2, 2])
    with dl_col:
        st.download_button(
            label="DOWNLOAD PDF REPORT",
            data=pdf_buf,
            file_name=f"MUBAS_Blast_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

    # ── Save to history ──
    st.session_state.history.insert(0, {
        "Time":         datetime.now().strftime("%H:%M:%S"),
        "Dia (mm)":      d_mm,
        "H Bench (m)":   h_bench,
        "Burden (m)":    round(burden, 3),
        "Spacing (m)":   round(spacing, 3),
        "Charge (kg)":   round(charge_weight, 2),
        "Style":         charge_style,
        "Act. PF":       round(actual_pf, 4),
        "Tgt PF":        pf_target,
        "PF Status":     "PASS" if abs(actual_pf - pf_target) <= 0.05 else "FAIL",
    })

# ─────────────────────────────────────────────
#  HISTORY
# ─────────────────────────────────────────────
st.divider()
st.markdown("""
<div class="section-header">
    CALCULATION HISTORY
</div>
""", unsafe_allow_html=True)

if st.session_state.history:
    hist_df = pd.DataFrame(st.session_state.history)
    st.dataframe(hist_df, use_container_width=True, hide_index=True)
    if st.button("CLEAR HISTORY", type="secondary"):
        st.session_state.history = []
        st.rerun()
else:
    st.markdown("""
    <div style='text-align:center; padding:2rem;
                font-family:Share Tech Mono,monospace; font-size:0.9rem;
                color:#1e2840; border:1px dashed #182035;
                border-radius:8px;'>
        No calculations yet. Enter parameters above and click
        <span style='color:#1e7db8;'> RUN CALCULATION</span>.
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.divider()
st.markdown("""
<div style='text-align:center; padding:1rem 0 0.5rem;
            font-family:Share Tech Mono,monospace; font-size:0.75rem;
            color:#1e2840; letter-spacing:0.1em; line-height:2;'>
    MUBAS BLAST DESIGNER &nbsp;|&nbsp; BMEN 5 · GROUP 4 &nbsp;|&nbsp;
    Enrique Hannock · Saidi Ibrahim · Promise Magola<br>
    Malawi University of Business and Applied Sciences &nbsp;·&nbsp;
    Mining Engineering Department
</div>
""", unsafe_allow_html=True)
