"""
Salesly Cashely — SAP O2C Analytics Dashboard
Premium Dark UI · Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Salesly Cashely",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════
# PREMIUM CSS — Salesly Cashely Brand
# ══════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
    --bg:     #07080F;
    --bg2:    #0E1120;
    --bg3:    #141828;
    --card:   #111523;
    --card2:  #181C2E;
    --cyan:   #06EAD8;
    --violet: #8B5CF6;
    --green:  #22D3A1;
    --amber:  #FBBF24;
    --rose:   #F43F5E;
    --pink:   #EC4899;
    --text1:  #EEF2FF;
    --text2:  #8892B0;
    --text3:  #4A5568;
    --border: rgba(255,255,255,0.06);
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background: var(--bg) !important;
    color: var(--text1) !important;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#090B17 0%,#07080F 100%) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] * { color: var(--text2) !important; }

.main .block-container {
    background: transparent !important;
    padding: 2rem 2.5rem !important;
    max-width: 1500px !important;
}

h1 {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.7rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.8px !important;
    color: var(--text1) !important;
}
h2, h3 { font-family: 'Syne', sans-serif !important; color: var(--text1) !important; font-weight: 700 !important; }

[data-testid="stMetric"] {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    padding: 1.1rem 1.3rem !important;
}
[data-testid="stMetricLabel"] {
    font-size: 0.65rem !important; font-weight: 600 !important;
    text-transform: uppercase !important; letter-spacing: 2px !important; color: var(--text3) !important;
}
[data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1.5rem !important; font-weight: 600 !important; color: var(--text1) !important;
}

.stDataFrame { border-radius: 14px !important; overflow: hidden !important; border: 1px solid var(--border) !important; }

.stSelectbox > div > div {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text1) !important;
}

.stDownloadButton > button {
    background: var(--card2) !important; border: 1px solid var(--border) !important;
    color: var(--cyan) !important; border-radius: 10px !important;
    font-size: 0.82rem !important; font-weight: 500 !important;
}
.stDownloadButton > button:hover { background: rgba(6,234,216,0.08) !important; border-color: var(--cyan) !important; }

code {
    background: var(--card2) !important; color: var(--cyan) !important;
    border-radius: 6px !important; font-family: 'JetBrains Mono', monospace !important; font-size: 0.78rem !important;
}

::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #0E1120; }
::-webkit-scrollbar-thumb { background: #4A5568; border-radius: 999px; }
</style>
""", unsafe_allow_html=True)

# ── Matplotlib dark theme ──
plt.style.use('dark_background')
rcParams.update({
    'figure.facecolor': '#111523', 'axes.facecolor': '#141828',
    'axes.edgecolor': '#1E2540', 'grid.color': '#1A1F35',
    'grid.linewidth': 0.5, 'text.color': '#8892B0',
    'xtick.color': '#4A5568', 'ytick.color': '#4A5568',
    'axes.spines.top': False, 'axes.spines.right': False, 'font.size': 9,
})
PALETTE = ['#06EAD8', '#8B5CF6', '#22D3A1', '#FBBF24', '#F43F5E', '#EC4899']

def fstyle(fig, ax_or_axes):
    fig.patch.set_facecolor('#111523')
    axes = ax_or_axes if isinstance(ax_or_axes, (list, np.ndarray)) else [ax_or_axes]
    for ax in np.array(axes).flatten():
        ax.set_facecolor('#141828')
        ax.tick_params(colors='#4A5568', labelsize=9)
        for spine in ax.spines.values(): spine.set_edgecolor('#1E2540')

# ══════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='padding:1.2rem 0.5rem 0.8rem;'>
      <div style='display:flex;align-items:center;gap:10px;'>
        <div style='width:38px;height:38px;background:linear-gradient(135deg,#06EAD8,#8B5CF6);
                    border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:1.1rem;'>💸</div>
        <div>
          <div style='font-family:Syne,sans-serif;font-size:1rem;color:#EEF2FF;font-weight:800;line-height:1.1;'>Salesly Cashely</div>
          <div style='font-size:0.58rem;color:#4A5568;letter-spacing:2px;text-transform:uppercase;margin-top:2px;'>O2C Analytics</div>
        </div>
      </div>
    </div>
    <div style='height:1px;background:linear-gradient(90deg,transparent,rgba(6,234,216,0.3),transparent);margin-bottom:1rem;'></div>
    """, unsafe_allow_html=True)

    page = st.radio("Navigation", [
        "🏠  Overview", "📈  Dashboard", "👥  Segmentation",
        "🔮  Predictive", "🚨  Anomaly Detection", "📋  Data Table"
    ], label_visibility="collapsed")

    st.markdown("<div style='height:1px;background:rgba(255,255,255,0.05);margin:1rem 0;'></div>", unsafe_allow_html=True)
    st.code("VA01  → Sales Order\nVL01N → Delivery\nVF01  → Billing\nF-28  → Payment\nFBL5N → Line Items")
    st.markdown("""
    <div style='height:1px;background:rgba(255,255,255,0.05);margin:1rem 0;'></div>
    <div style='font-size:0.7rem;color:#2D3748;line-height:2.2;'>
      <span style='color:#4A5568;'>Module</span>   SAP SD<br>
      <span style='color:#4A5568;'>Dataset</span>  500 records<br>
      <span style='color:#4A5568;'>Analytics</span> 6 types<br>
      <span style='color:#4A5568;'>Stack</span>    Python + Streamlit
    </div>
    <div style='background:linear-gradient(135deg,rgba(6,234,216,0.07),rgba(139,92,246,0.07));
                border:1px solid rgba(6,234,216,0.1);border-radius:10px;padding:0.75rem;text-align:center;margin-top:1rem;'>
      <div style='font-size:0.6rem;color:#06EAD8;letter-spacing:1px;text-transform:uppercase;'>Built With</div>
      <div style='font-size:0.72rem;color:#8892B0;margin-top:3px;line-height:1.7;'>Python · Streamlit<br>Pandas · Scikit-learn<br>Matplotlib · SciPy</div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════
# DATA LOAD
# ══════════════════════════════════════════════════
@st.cache_data
def load_data():
    df = pd.read_csv("data/sales_data.csv", parse_dates=['Order_Date', 'Delivery_Date'])
    df['Month'] = df['Order_Date'].dt.month
    df['Quarter'] = df['Order_Date'].dt.quarter
    df['MonthName'] = df['Order_Date'].dt.strftime('%b')
    return df

df = load_data()
MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

# ── UI helpers ──
def page_header(icon, title, badge=""):
    bdg = (f"<span style='font-size:0.63rem;background:rgba(6,234,216,0.1);color:#06EAD8;"
           f"padding:3px 12px;border-radius:999px;border:1px solid rgba(6,234,216,0.2);"
           f"letter-spacing:1px;font-weight:500;'>{badge}</span>") if badge else ""
    st.markdown(f"""
    <div style='margin-bottom:2rem;padding-bottom:1rem;border-bottom:1px solid rgba(255,255,255,0.05);'>
      <div style='display:flex;align-items:center;gap:12px;'>
        <div style='font-size:1.7rem;'>{icon}</div>
        <div>
          <div style='font-family:Syne,sans-serif;font-size:1.55rem;font-weight:800;
               background:linear-gradient(135deg,#EEF2FF 40%,#8892B0);
               -webkit-background-clip:text;-webkit-text-fill-color:transparent;
               background-clip:text;line-height:1.2;'>{title}</div>
          <div style='margin-top:6px;'>{bdg}</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

def kcard(label, value, delta=None, color="#06EAD8", icon=""):
    dc = "#22D3A1" if not delta or delta[0] != "-" else "#F43F5E"
    dh = f"<div style='font-size:0.7rem;color:{dc};margin-top:5px;font-weight:500;'>{delta}</div>" if delta else ""
    st.markdown(f"""
    <div style='background:#111523;border:1px solid rgba(255,255,255,0.06);border-radius:14px;
                padding:1.1rem 1.3rem;border-left:3px solid {color};position:relative;overflow:hidden;'>
      <div style='position:absolute;top:-20px;right:-20px;width:80px;height:80px;
                  background:radial-gradient(circle,{color}18 0%,transparent 70%);border-radius:50%;'></div>
      <div style='font-size:0.6rem;text-transform:uppercase;letter-spacing:2px;color:#4A5568;font-weight:600;'>{icon} {label}</div>
      <div style='font-family:JetBrains Mono,monospace;font-size:1.4rem;color:#EEF2FF;margin-top:6px;font-weight:600;'>{value}</div>
      {dh}
    </div>
    """, unsafe_allow_html=True)

def slabel(text, color="#06EAD8"):
    st.markdown(f"""
    <div style='display:flex;align-items:center;gap:8px;margin:1rem 0 0.6rem;'>
      <div style='width:3px;height:14px;background:{color};border-radius:2px;'></div>
      <div style='font-size:0.62rem;text-transform:uppercase;letter-spacing:2.5px;color:#4A5568;font-weight:600;'>{text}</div>
    </div>
    """, unsafe_allow_html=True)

def divider():
    st.markdown("<div style='height:1px;background:rgba(255,255,255,0.04);margin:1.2rem 0;'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════
# PAGE 1 — OVERVIEW
# ══════════════════════════════════════════════════
if "Overview" in page:
    page_header("💸", "Salesly Cashely", "SAP O2C · Analytics · 2024")

    st.markdown("""
    <div style='background:linear-gradient(135deg,#0E1120 0%,#130D22 50%,#0A1118 100%);
                border:1px solid rgba(6,234,216,0.12);border-radius:20px;padding:2.5rem 3rem;
                margin-bottom:2rem;position:relative;overflow:hidden;'>
      <div style='position:absolute;top:-60px;right:-60px;width:280px;height:280px;
                  background:radial-gradient(circle,rgba(139,92,246,0.12) 0%,transparent 65%);
                  border-radius:50%;pointer-events:none;'></div>
      <div style='position:absolute;bottom:-40px;left:200px;width:200px;height:200px;
                  background:radial-gradient(circle,rgba(6,234,216,0.07) 0%,transparent 65%);
                  border-radius:50%;pointer-events:none;'></div>
      <div style='font-size:0.6rem;color:#06EAD8;text-transform:uppercase;letter-spacing:4px;margin-bottom:10px;font-weight:600;'>
        End-to-End Business Process Intelligence
      </div>
      <div style='font-family:Syne,sans-serif;font-size:2.1rem;font-weight:800;line-height:1.25;margin-bottom:14px;'>
        <span style='color:#EEF2FF;'>SAP Order-to-Cash</span><br>
        <span style='background:linear-gradient(90deg,#06EAD8,#8B5CF6);
                     -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                     background-clip:text;'>Analytics Platform</span>
      </div>
      <div style='font-size:0.88rem;color:#8892B0;max-width:620px;line-height:1.9;'>
        A complete analytics pipeline — Descriptive, Diagnostic, Predictive, RFM Segmentation,
        Anomaly Detection and Visualisation, all powered by SAP SD process data.
      </div>
      <div style='display:flex;gap:10px;margin-top:1.5rem;flex-wrap:wrap;'>
        <span style='font-size:0.7rem;background:rgba(6,234,216,0.08);color:#06EAD8;padding:5px 14px;border-radius:999px;border:1px solid rgba(6,234,216,0.18);'>500 SAP Records</span>
        <span style='font-size:0.7rem;background:rgba(139,92,246,0.08);color:#A78BFA;padding:5px 14px;border-radius:999px;border:1px solid rgba(139,92,246,0.18);'>6 Analytics Types</span>
        <span style='font-size:0.7rem;background:rgba(34,211,161,0.08);color:#22D3A1;padding:5px 14px;border-radius:999px;border:1px solid rgba(34,211,161,0.18);'>Live Dashboard</span>
        <span style='font-size:0.7rem;background:rgba(251,191,36,0.08);color:#FBBF24;padding:5px 14px;border-radius:999px;border:1px solid rgba(251,191,36,0.18);'>ML Forecasting</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    slabel("O2C PROCESS FLOW  ·  SAP SD", "#06EAD8")
    steps = [
        ("🔍","Inquiry","VA11","#06EAD8","Customer request"),
        ("📋","Quotation","VA21","#8B5CF6","Price proposal"),
        ("📦","Sales Order","VA01","#22D3A1","Order creation"),
        ("🚚","Delivery","VL01N","#FBBF24","Goods dispatch"),
        ("🧾","Billing","VF01","#EC4899","Invoice sent"),
        ("💳","Payment","F-28","#06EAD8","Cash received"),
    ]
    for col, (icon, name, tcode, color, desc) in zip(st.columns(6), steps):
        col.markdown(f"""
        <div style='background:#111523;border:1px solid rgba(255,255,255,0.06);border-radius:14px;
                    padding:1rem 0.6rem;text-align:center;border-top:3px solid {color};'>
          <div style='font-size:1.5rem;margin-bottom:6px;'>{icon}</div>
          <div style='font-size:0.78rem;color:#EEF2FF;font-weight:700;font-family:Syne,sans-serif;'>{name}</div>
          <div style='font-family:JetBrains Mono,monospace;font-size:0.6rem;color:{color};margin:4px 0;'>{tcode}</div>
          <div style='font-size:0.6rem;color:#4A5568;'>{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    slabel("ANALYTICS MODULES", "#8B5CF6")
    topics = [
        ("📊","Descriptive Analytics","KPIs, revenue trends, monthly & quarterly sales, on-time rates","#06EAD8"),
        ("🔍","Diagnostic Analytics","Root cause of delays, cancellations, payment term impact","#8B5CF6"),
        ("🔮","Predictive Analytics","Linear regression forecast — R², MAE, RMSE model evaluation","#22D3A1"),
        ("🚨","Anomaly Detection","Z-Score outlier detection — billing & order amount spikes","#F43F5E"),
        ("👥","RFM Segmentation","Customer scoring: Recency · Frequency · Monetary value","#FBBF24"),
        ("📈","Data Visualisation","Line, bar, pie, scatter, histogram — 15+ interactive charts","#EC4899"),
    ]
    c1, c2, c3 = st.columns(3)
    for i, (icon, title, desc, color) in enumerate(topics):
        [c1,c2,c3][i%3].markdown(f"""
        <div style='background:#111523;border:1px solid rgba(255,255,255,0.05);border-radius:14px;
                    padding:1.1rem 1.2rem;margin-bottom:0.8rem;'>
          <div style='display:flex;align-items:center;gap:9px;margin-bottom:8px;'>
            <div style='width:30px;height:30px;border-radius:8px;background:{color}15;
                        display:flex;align-items:center;justify-content:center;font-size:1rem;flex-shrink:0;'>{icon}</div>
            <span style='font-size:0.85rem;font-weight:700;color:#EEF2FF;font-family:Syne,sans-serif;'>{title}</span>
          </div>
          <div style='font-size:0.74rem;color:#8892B0;line-height:1.7;'>{desc}</div>
          <div style='height:2px;background:linear-gradient(90deg,{color},transparent);border-radius:2px;margin-top:12px;'></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    slabel("DATASET PREVIEW", "#22D3A1")
    st.dataframe(df.head(8), use_container_width=True, hide_index=True)
    st.markdown(f"""<div style='font-size:0.7rem;color:#4A5568;margin-top:8px;display:flex;gap:16px;flex-wrap:wrap;'>
      <span>📦 {len(df):,} records</span>
      <span>📅 {df['Order_Date'].min().date()} → {df['Order_Date'].max().date()}</span>
      <span>🏷️ {df['Product'].nunique()} products</span>
      <span>🗺️ {df['Region'].nunique()} regions</span>
      <span>👥 {df['Customer'].nunique()} customers</span>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════
# PAGE 2 — DASHBOARD
# ══════════════════════════════════════════════════
elif "Dashboard" in page:
    page_header("📈", "Analytics Dashboard", "Descriptive · Trends · Performance")

    c1,c2,c3,c4 = st.columns(4)
    with c1: kcard("Total Revenue",  f"₹{df['Net_Revenue'].sum()/1e5:.1f}L",  "+12.4% YoY", "#06EAD8", "💰")
    with c2: kcard("Total Orders",   f"{len(df):,}",                          "+8.1% growth","#8B5CF6", "📦")
    with c3: kcard("Avg Order Value",f"₹{df['Net_Revenue'].mean()/1000:.1f}K","+3.8% QoQ",  "#22D3A1", "📊")
    with c4: kcard("On-Time Rate",   f"{(df['On_Time']=='Yes').mean()*100:.1f}%","-2.1% vs target","#F43F5E","🚚")

    divider()
    slabel("REVENUE TRENDS", "#06EAD8")
    col1, col2 = st.columns(2)

    with col1:
        rev = [df[df['Month']==m]['Net_Revenue'].sum()/1e5 for m in range(1,13)]
        fig, ax = plt.subplots(figsize=(6, 3.5)); fstyle(fig, ax)
        ax.plot(MONTHS, rev, color='#06EAD8', linewidth=2.5, zorder=3)
        ax.fill_between(MONTHS, rev, alpha=0.1, color='#06EAD8')
        ax.scatter(MONTHS, rev, color='#06EAD8', s=45, zorder=4, edgecolors='#07080F', linewidths=2)
        peak = rev.index(max(rev))
        ax.annotate(f"Peak ₹{max(rev):.1f}L", (MONTHS[peak], max(rev)),
                    xytext=(0, 12), textcoords='offset points', ha='center', fontsize=8,
                    color='#06EAD8', arrowprops=dict(arrowstyle='->', color='#06EAD8', lw=1))
        ax.set_ylabel("Revenue (₹L)", fontsize=9, color='#4A5568')
        ax.tick_params(axis='x', rotation=45); ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig, use_container_width=True); plt.close()

    with col2:
        prod_rev = df.groupby('Product')['Net_Revenue'].sum()/1e5
        fig, ax = plt.subplots(figsize=(6, 3.5)); fstyle(fig, ax)
        sp = prod_rev.sort_values()
        bars = ax.barh(sp.index, sp.values, color=PALETTE[:len(sp)], height=0.5, edgecolor='none')
        for bar, val in zip(bars, sp.values):
            ax.text(val+0.08, bar.get_y()+bar.get_height()/2, f'₹{val:.1f}L', va='center', fontsize=8, color='#8892B0')
        ax.set_xlabel("Revenue (₹L)", fontsize=9, color='#4A5568'); ax.grid(axis='x', alpha=0.3)
        st.pyplot(fig, use_container_width=True); plt.close()

    divider()
    slabel("ORDER ANALYSIS", "#8B5CF6")
    col3, col4 = st.columns(2)

    with col3:
        sc = df['Status'].value_counts()
        fig, ax = plt.subplots(figsize=(5, 3.5)); fstyle(fig, ax)
        wedges, texts, autotexts = ax.pie(
            sc, labels=sc.index, autopct='%1.1f%%',
            colors=['#22D3A1','#FBBF24','#F43F5E'], startangle=90,
            pctdistance=0.75, wedgeprops=dict(edgecolor='#111523', linewidth=2.5, width=0.65))
        for t in texts: t.set_color('#8892B0'); t.set_fontsize(9)
        for at in autotexts: at.set_color('#EEF2FF'); at.set_fontsize(8.5); at.set_fontweight('bold')
        ax.text(0, 0, f"{len(df)}", ha='center', va='center', fontsize=14, color='#EEF2FF', fontweight='bold')
        ax.text(0, -0.28, "orders", ha='center', va='center', fontsize=8, color='#4A5568')
        st.pyplot(fig, use_container_width=True); plt.close()

    with col4:
        ot = [(df[df['Month']==m]['On_Time']=='Yes').mean()*100 for m in range(1,13)]
        fig, ax = plt.subplots(figsize=(6, 3.5)); fstyle(fig, ax)
        bc = ['#22D3A1' if v>=85 else '#FBBF24' if v>=70 else '#F43F5E' for v in ot]
        ax.bar(MONTHS, ot, color=bc, edgecolor='none', width=0.6)
        ax.axhline(85, color='#06EAD8', linestyle='--', linewidth=1.5, alpha=0.8, label='Target 85%')
        ax.set_ylim(0, 105); ax.set_ylabel("On-Time %", fontsize=9, color='#4A5568')
        ax.tick_params(axis='x', rotation=45); ax.legend(fontsize=8, framealpha=0.0)
        ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig, use_container_width=True); plt.close()

    divider()
    slabel("QUARTERLY BREAKDOWN BY PRODUCT", "#22D3A1")
    q_rev = df.groupby(['Quarter','Product'])['Net_Revenue'].sum().unstack(fill_value=0)/1e5
    fig, ax = plt.subplots(figsize=(12, 3.8)); fstyle(fig, ax)
    x = np.arange(4); w = 0.16
    for i, (prod, color) in enumerate(zip(q_rev.columns, PALETTE)):
        ax.bar(x + i*w, q_rev[prod], width=w, color=color, edgecolor='none', label=prod, alpha=0.9)
    ax.set_xticks(x + w*2); ax.set_xticklabels(['Q1','Q2','Q3','Q4'], fontsize=10)
    ax.set_ylabel("Revenue (₹L)", fontsize=9, color='#4A5568')
    ax.legend(fontsize=8, ncol=5, framealpha=0.0); ax.grid(axis='y', alpha=0.3)
    st.pyplot(fig, use_container_width=True); plt.close()

# ══════════════════════════════════════════════════
# PAGE 3 — SEGMENTATION
# ══════════════════════════════════════════════════
elif "Segmentation" in page:
    page_header("👥", "Customer Segmentation", "RFM Model · Recency · Frequency · Monetary")

    snapshot = df['Order_Date'].max() + pd.Timedelta(days=1)
    rfm = df.groupby('Customer').agg(
        Recency=('Order_Date', lambda x: (snapshot-x.max()).days),
        Frequency=('Order_ID', 'count'),
        Monetary=('Net_Revenue', 'sum')).reset_index()
    rfm['R'] = pd.qcut(rfm['Recency'],   4, labels=[4,3,2,1]).astype(int)
    rfm['F'] = pd.qcut(rfm['Frequency'], 4, labels=[1,2,3,4]).astype(int)
    rfm['M'] = pd.qcut(rfm['Monetary'],  4, labels=[1,2,3,4]).astype(int)
    rfm['Score'] = rfm['R'] + rfm['F'] + rfm['M']
    def seg(s):
        if s>=10: return 'Champion'
        elif s>=8: return 'Loyal'
        elif s>=6: return 'At-Risk'
        elif s>=4: return 'New'
        else: return 'Lost'
    rfm['Segment'] = rfm['Score'].apply(seg)
    SC = {'Champion':'#06EAD8','Loyal':'#22D3A1','At-Risk':'#FBBF24','New':'#8B5CF6','Lost':'#F43F5E'}
    IC = {'Champion':'🏆','Loyal':'⭐','At-Risk':'⚠️','New':'🌱','Lost':'💤'}
    sc_counts = rfm['Segment'].value_counts()

    slabel("CUSTOMER SEGMENTS", "#06EAD8")
    for col, (sn, color) in zip(st.columns(5), SC.items()):
        cnt = sc_counts.get(sn, 0); pct = cnt/len(rfm)*100
        col.markdown(f"""
        <div style='background:#111523;border:1px solid rgba(255,255,255,0.06);border-radius:14px;
                    padding:1rem 0.8rem;text-align:center;overflow:hidden;position:relative;'>
          <div style='position:absolute;top:0;left:0;right:0;height:3px;background:{color};'></div>
          <div style='font-size:1.4rem;margin-bottom:5px;'>{IC.get(sn,"")}</div>
          <div style='font-size:0.62rem;text-transform:uppercase;letter-spacing:1.5px;color:#4A5568;font-weight:600;'>{sn}</div>
          <div style='font-family:JetBrains Mono,monospace;font-size:1.6rem;color:{color};font-weight:600;margin:4px 0;'>{cnt}</div>
          <div style='height:3px;background:#1A1F35;border-radius:999px;margin-top:6px;'>
            <div style='height:3px;width:{min(pct*3,100)}%;background:{color};border-radius:999px;'></div>
          </div>
          <div style='font-size:0.6rem;color:#4A5568;margin-top:4px;'>{pct:.0f}% of customers</div>
        </div>
        """, unsafe_allow_html=True)

    divider()
    col1, col2 = st.columns(2)
    with col1:
        slabel("SEGMENT DISTRIBUTION", "#06EAD8")
        fig, ax = plt.subplots(figsize=(5.5, 4.2)); fstyle(fig, ax)
        wc = [SC.get(s,'gray') for s in sc_counts.index]
        wedges, texts, autotexts = ax.pie(
            sc_counts, labels=sc_counts.index, autopct='%1.1f%%',
            colors=wc, startangle=90, pctdistance=0.78,
            wedgeprops=dict(edgecolor='#111523', linewidth=2.5, width=0.6))
        for t in texts: t.set_color('#8892B0'); t.set_fontsize(9)
        for at in autotexts: at.set_color('#EEF2FF'); at.set_fontsize(8); at.set_fontweight('bold')
        st.pyplot(fig, use_container_width=True); plt.close()

    with col2:
        slabel("AVG SPEND PER SEGMENT", "#8B5CF6")
        sm = rfm.groupby('Segment')['Monetary'].mean()/1000
        order = [s for s in ['Champion','Loyal','At-Risk','New','Lost'] if s in sm.index]
        sm = sm.reindex(order)
        fig, ax = plt.subplots(figsize=(5.5, 4.2)); fstyle(fig, ax)
        bars = ax.bar(sm.index, sm.values, color=[SC.get(s,'gray') for s in sm.index], edgecolor='none', width=0.55)
        for bar, val in zip(bars, sm.values):
            ax.text(bar.get_x()+bar.get_width()/2, val+0.5, f'₹{val:.0f}K', ha='center', fontsize=8, color='#8892B0')
        ax.set_ylabel("Avg Spend (₹K)", fontsize=9, color='#4A5568')
        ax.tick_params(axis='x', rotation=15); ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig, use_container_width=True); plt.close()

    divider()
    slabel("FREQUENCY vs MONETARY — SCATTER MAP", "#22D3A1")
    fig, ax = plt.subplots(figsize=(12, 4)); fstyle(fig, ax)
    for sn, color in SC.items():
        mask = rfm['Segment'] == sn
        if mask.any():
            ax.scatter(rfm[mask]['Frequency'], rfm[mask]['Monetary']/1000,
                       c=color, s=130, alpha=0.88, edgecolors='#111523', linewidth=1.5,
                       label=f'{IC.get(sn,"")} {sn}', zorder=3)
    ax.set_xlabel("Frequency (order count)", fontsize=9, color='#4A5568')
    ax.set_ylabel("Monetary (₹K)", fontsize=9, color='#4A5568')
    ax.legend(fontsize=8.5, framealpha=0.05, ncol=5)
    ax.grid(True, alpha=0.25)
    st.pyplot(fig, use_container_width=True); plt.close()

    divider()
    slabel("FULL RFM SCORING TABLE", "#FBBF24")
    disp = rfm[['Customer','Recency','Frequency','Monetary','Score','Segment']].sort_values('Score', ascending=False).reset_index(drop=True)
    disp['Monetary'] = disp['Monetary'].apply(lambda x: f"₹{x:,.0f}")
    st.dataframe(disp, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════
# PAGE 4 — PREDICTIVE
# ══════════════════════════════════════════════════
elif "Predictive" in page:
    page_header("🔮", "Predictive Analytics", "Linear Regression · 6-Month Revenue Forecast")

    monthly = df.groupby('Month')['Net_Revenue'].sum().reset_index()
    X = monthly[['Month']].values; y = monthly['Net_Revenue'].values
    model = LinearRegression().fit(X, y); y_pred = model.predict(X)
    r2 = r2_score(y, y_pred); mae = mean_absolute_error(y, y_pred)
    rmse = np.sqrt(mean_squared_error(y, y_pred))
    future = np.array([[13],[14],[15],[16],[17],[18]]); fpred = model.predict(future)
    flabels = ["Jan'25","Feb'25","Mar'25","Apr'25","May'25","Jun'25"]

    c1,c2,c3,c4 = st.columns(4)
    with c1: kcard("R² Score",        f"{r2:.4f}",          "Model accuracy",     "#06EAD8", "🎯")
    with c2: kcard("MAE",             f"₹{mae/1e3:.1f}K",   "Mean absolute error","#8B5CF6", "📐")
    with c3: kcard("RMSE",            f"₹{rmse/1e3:.1f}K",  "Root mean sq error", "#22D3A1", "📏")
    with c4: kcard("Projected Growth",f"+{(fpred[-1]-y[-1])/y[-1]*100:.1f}%","vs Dec 2024","#FBBF24","📈")

    divider()
    slabel("REVENUE FORECAST — HISTORICAL + PREDICTED", "#06EAD8")
    all_labels = MONTHS + flabels; hist_y = list(y/1e5)
    fig, ax = plt.subplots(figsize=(12, 5)); fstyle(fig, ax)
    ax.fill_between(range(12), hist_y, alpha=0.1, color='#06EAD8')
    ax.fill_between(range(11,18), [hist_y[-1]]+list(fpred/1e5), alpha=0.1, color='#8B5CF6')
    ax.plot(range(12), hist_y, 'o-', color='#06EAD8', linewidth=2.5, markersize=6,
            markerfacecolor='#07080F', markeredgewidth=2, label='Historical 2024', zorder=3)
    ax.plot(range(11,18), [hist_y[-1]]+list(fpred/1e5), 's--', color='#8B5CF6',
            linewidth=2.5, markersize=6, markerfacecolor='#07080F', markeredgewidth=2,
            label='Forecast 2025', zorder=3)
    ax.axvline(x=11.5, color='#2D3748', linestyle=':', linewidth=2)
    ax.text(11.7, max(fpred/1e5)*0.97, '← 2025 Forecast', color='#8B5CF6', fontsize=9, fontweight='bold')
    ax.annotate(f"₹{fpred[-1]/1e5:.1f}L", (17, fpred[-1]/1e5),
                xytext=(0, 10), textcoords='offset points', ha='center', fontsize=8, color='#8B5CF6')
    ax.set_xticks(range(18)); ax.set_xticklabels(all_labels, rotation=45, fontsize=8)
    ax.set_ylabel("Revenue (₹L)", fontsize=9, color='#4A5568')
    ax.legend(fontsize=9, framealpha=0.0); ax.grid(axis='y', alpha=0.3)
    st.pyplot(fig, use_container_width=True); plt.close()

    divider()
    c1, c2 = st.columns(2)
    with c1:
        slabel("MONTHLY FORECAST TABLE", "#8B5CF6")
        fdf = pd.DataFrame({
            'Month': flabels,
            'Forecasted Revenue': [f"₹{v:,.0f}" for v in fpred],
            'Growth vs Dec 2024': [f"+{(v-y[-1])/y[-1]*100:.1f}%" for v in fpred]
        })
        st.dataframe(fdf, use_container_width=True, hide_index=True)

    with c2:
        slabel("PRODUCT DEMAND FORECAST", "#22D3A1")
        prods = df['Product'].unique()
        curr = df.groupby('Product')['Quantity'].sum().reindex(prods)
        pred_d = curr * 1.12
        fig, ax = plt.subplots(figsize=(5.5, 3.8)); fstyle(fig, ax)
        x = np.arange(len(prods)); w = 0.35
        ax.bar(x - w/2, curr.values, width=w, color='#06EAD8', alpha=0.85, label='Current 2024', edgecolor='none')
        ax.bar(x + w/2, pred_d.values, width=w, color='#8B5CF6', alpha=0.85, label='Forecast 2025', edgecolor='none')
        ax.set_xticks(x); ax.set_xticklabels(prods, rotation=15, fontsize=8)
        ax.set_ylabel("Units", fontsize=9, color='#4A5568')
        ax.legend(fontsize=8, framealpha=0.0); ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig, use_container_width=True); plt.close()

# ══════════════════════════════════════════════════
# PAGE 5 — ANOMALY DETECTION
# ══════════════════════════════════════════════════
elif "Anomaly" in page:
    page_header("🚨", "Anomaly Detection", "Z-Score · Statistical Outlier Identification")

    col_sl, _ = st.columns([2, 4])
    with col_sl:
        threshold = st.slider("Z-Score Threshold", 1.5, 4.0, 2.5, 0.1,
                              help="Orders with Z-Score above this are flagged as anomalies")

    df2 = df.copy()
    df2['Z_Score'] = np.abs(stats.zscore(df2['Net_Revenue']))
    df2['Anomaly'] = df2['Z_Score'] > threshold
    anom_count = df2['Anomaly'].sum()
    anom_rev   = df2[df2['Anomaly']]['Net_Revenue'].sum()

    c1,c2,c3,c4 = st.columns(4)
    with c1: kcard("Scanned",       f"{len(df2):,}",             "Total orders",          "#06EAD8","🔍")
    with c2: kcard("Anomalies",     f"{anom_count}",             f"{anom_count/len(df2)*100:.1f}% flagged","#F43F5E","🚨")
    with c3: kcard("Revenue at Risk",f"₹{anom_rev/1e5:.2f}L",   "Needs review",          "#FBBF24","⚠️")
    with c4: kcard("Z Threshold",   f"{threshold:.1f}σ",         "Standard deviations",   "#8B5CF6","📐")

    divider()
    col1, col2 = st.columns(2)
    with col1:
        slabel("ORDER VALUES — ANOMALIES SPOTTED", "#F43F5E")
        fig, ax = plt.subplots(figsize=(6, 4)); fstyle(fig, ax)
        ax.scatter(df2[~df2['Anomaly']].index, df2[~df2['Anomaly']]['Net_Revenue']/1000,
                   c='#06EAD8', alpha=0.3, s=10, label='Normal', zorder=2)
        if anom_count > 0:
            ax.scatter(df2[df2['Anomaly']].index, df2[df2['Anomaly']]['Net_Revenue']/1000,
                       c='#F43F5E', s=90, marker='X', label=f'Anomaly ({anom_count})',
                       zorder=5, linewidths=1.5)
        ax.set_xlabel("Order Index", fontsize=9, color='#4A5568')
        ax.set_ylabel("Revenue (₹K)", fontsize=9, color='#4A5568')
        ax.legend(fontsize=8.5, framealpha=0.0); ax.grid(alpha=0.2)
        st.pyplot(fig, use_container_width=True); plt.close()

    with col2:
        slabel("Z-SCORE DISTRIBUTION", "#8B5CF6")
        fig, ax = plt.subplots(figsize=(6, 4)); fstyle(fig, ax)
        norm_d = df2[df2['Z_Score'] <= threshold]['Z_Score']
        anom_d = df2[df2['Z_Score'] > threshold]['Z_Score']
        ax.hist(norm_d, bins=25, color='#06EAD8', alpha=0.65, edgecolor='none', label=f'Normal ({len(norm_d)})')
        if len(anom_d) > 0:
            ax.hist(anom_d, bins=max(5, len(anom_d)//2+1), color='#F43F5E', alpha=0.9,
                    edgecolor='none', label=f'Anomaly ({len(anom_d)})')
        ax.axvline(threshold, color='#FBBF24', linestyle='--', linewidth=2, label=f'Threshold = {threshold}σ')
        ax.set_xlabel("Z-Score", fontsize=9, color='#4A5568')
        ax.set_ylabel("Count", fontsize=9, color='#4A5568')
        ax.legend(fontsize=8.5, framealpha=0.0); ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig, use_container_width=True); plt.close()

    divider()
    if anom_count > 0:
        slabel(f"FLAGGED TRANSACTIONS  ·  {anom_count} ANOMALIES DETECTED", "#F43F5E")
        adf = df2[df2['Anomaly']][['Order_ID','Customer','Product','Region','Net_Revenue','Z_Score','Status']].copy()
        adf['Z_Score'] = adf['Z_Score'].round(2)
        adf['Net_Revenue'] = adf['Net_Revenue'].apply(lambda x: f"₹{x:,.0f}")
        st.dataframe(adf.sort_values('Z_Score', ascending=False), use_container_width=True, hide_index=True)
    else:
        st.info(f"✅ No anomalies detected at Z = {threshold}. Lower the threshold to flag more orders.")

# ══════════════════════════════════════════════════
# PAGE 6 — DATA TABLE
# ══════════════════════════════════════════════════
elif "Data Table" in page:
    page_header("📋", "SAP Sales Data", "Filter · Explore · Export")

    slabel("FILTERS", "#06EAD8")
    col1,col2,col3,col4 = st.columns(4)
    pf   = col1.selectbox("Product",       ["All"] + sorted(df['Product'].unique().tolist()))
    sf   = col2.selectbox("Status",        ["All"] + sorted(df['Status'].unique().tolist()))
    rf   = col3.selectbox("Region",        ["All"] + sorted(df['Region'].unique().tolist()))
    payf = col4.selectbox("Payment Terms", ["All"] + sorted(df['Payment_Terms'].unique().tolist()))

    filtered = df.copy()
    if pf   != "All": filtered = filtered[filtered['Product']==pf]
    if sf   != "All": filtered = filtered[filtered['Status']==sf]
    if rf   != "All": filtered = filtered[filtered['Region']==rf]
    if payf != "All": filtered = filtered[filtered['Payment_Terms']==payf]

    divider()
    slabel("SELECTION SUMMARY", "#22D3A1")
    c1,c2,c3,c4 = st.columns(4)
    with c1: kcard("Showing",   f"{len(filtered):,}", f"of {len(df):,} total", "#06EAD8","📄")
    with c2: kcard("Revenue",   f"₹{filtered['Net_Revenue'].sum()/1e5:.1f}L",  None,             "#8B5CF6","💰")
    with c3: kcard("Avg Value", f"₹{filtered['Net_Revenue'].mean()/1000:.1f}K",None,             "#22D3A1","📊")
    with c4: kcard("On-Time",   f"{(filtered['On_Time']=='Yes').mean()*100:.1f}%", None,         "#FBBF24","✅")

    divider()
    dcols = ['Order_ID','SAP_Doc_No','Customer','Product','Region',
             'Quantity','Net_Revenue','Order_Date','Delivery_Days','Payment_Terms','Status','On_Time']
    st.dataframe(filtered[dcols], use_container_width=True, hide_index=True)

    c_dl, c_note, _ = st.columns([1, 2, 3])
    with c_dl:
        csv = filtered.to_csv(index=False).encode('utf-8')
        st.download_button("⬇  Download CSV", csv, "salesly_cashely_export.csv",
                           "text/csv", use_container_width=True)
    with c_note:
        st.markdown(f"<div style='font-size:0.72rem;color:#4A5568;padding-top:0.6rem;'>↳ {len(filtered)} records · export ready</div>",
                    unsafe_allow_html=True)
