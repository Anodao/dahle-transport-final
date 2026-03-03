import streamlit as st
import pandas as pd
import plotly.express as px
from supabase import create_client

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Dahle Transport - Performance Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- SUPABASE CONNECTIE ---
@st.cache_resource
def init_connection():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

supabase = init_connection()

# --- CSS STYLING GLOBAL & NAVBAR HTML ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }

    /* --- Lichte Achtergrond (Net als Planner) --- */
    .stApp { background-color: #f8f9fa !important; }
    .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 { color: #111111 !important; }
    div[data-testid="stMetricValue"], div[data-testid="stMetricLabel"] { color: #111111 !important; }

    /* --- HEADER & SIDEBAR FIX --- */
    [data-testid="collapsedControl"] { display: none !important; }
    [data-testid="stSidebar"] { display: none !important; }
    header[data-testid="stHeader"] { background: transparent !important; pointer-events: none !important; display: none !important;}
    
    /* --- NAVBAR --- */
    .block-container { padding-top: 110px; }
    .navbar {
        position: fixed; top: 0; left: 0; width: 100%; height: 90px;
        background-color: white; z-index: 999; border-bottom: 1px solid #eaeaea; 
        display: grid; grid-template-columns: 1fr auto 1fr; align-items: center;
        padding: 0 40px; box-shadow: 0 2px 10px rgba(0,0,0,0.03);
    }
    .nav-logo { display: flex; justify-content: flex-start; }
    .nav-logo a { display: inline-block; height: 48px; text-decoration: none; cursor: pointer; }
    .nav-logo img { height: 100%; width: auto; display: block; transition: transform 0.2s ease-in-out; }
    .nav-logo a:hover img { transform: scale(1.05); } 
    .nav-links { display: flex; gap: 28px; font-size: 15px; font-weight: 500; color: #000000; justify-content: center;}
    .nav-links a { text-decoration: none; color: inherit; }
    .nav-links span { cursor: pointer; transition: color 0.2s; }
    .nav-links span:hover { color: #894b9d; }
    .nav-cta { display: flex; justify-content: flex-end; gap: 15px; align-items: center; }
    
    /* Knoppen styling */
    .cta-btn { 
        background-color: #894b9d; color: white !important; padding: 10px 24px;
        border-radius: 50px; text-decoration: none !important; font-weight: 600; 
        font-size: 13px; letter-spacing: 0.5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        cursor: pointer; transition: background-color 0.2s; white-space: nowrap;
    }
    .cta-btn:hover { background-color: #723e83; }

    .cta-btn-outline {
        background-color: transparent; color: #894b9d !important; padding: 10px 20px;
        border-radius: 50px; text-decoration: none !important; font-weight: 600; 
        font-size: 13px; letter-spacing: 0.5px; border: 2px solid #894b9d;
        cursor: pointer; transition: all 0.2s; white-space: nowrap;
    }
    .cta-btn-outline:hover { background-color: #894b9d; color: white !important; }

    /* Streamlit Specifieke Knoppen (Back knop) */
    div.stButton > button { background-color: #e0e6ed !important; color: #333 !important; border: none; font-weight: bold; border-radius: 6px;}
    div.stButton > button:hover { background-color: #bdc3c7 !important; }

    /* Header Banner */
    .header-banner {
        background-color: #894b9d;
        padding: 30px 40px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Slider/Input fix voor lichte achtergrond */
    .stSlider div[data-baseweb="slider"] { color: #894b9d !important; }
    label[data-testid="stWidgetLabel"] { color: #333333 !important; font-weight: 600; }

    /* --- DE FIX VOOR JOUW CUSTOMER CARDS --- */
    .customer-card {
        background-color: #ffffff;
        border: 1px solid #d1d5db;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
    .customer-name {
        font-size: 18px;
        font-weight: 700;
        color: #111111;
        margin-bottom: 15px;
        border-bottom: 2px solid #f0f2f6;
        padding-bottom: 8px;
    }
    .metric-row {
        display: flex;
        justify-content: space-between;
        gap: 10px;
    }
    .metric-box {
        flex: 1;
        display: flex;
        flex-direction: column;
    }
    .metric-label {
        font-size: 12px;
        color: #6b7280;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    .metric-value {
        font-size: 16px;
        font-weight: 700;
        color: #111111;
    }
    </style>
    
    <div class="navbar">
        <div class="nav-logo">
            <a href="/" target="_self" title="Go back to Home">
                <img src="https://cloud-1de12d.becdn.net/media/original/964295c9ae8e693f8bb4d6b70862c2be/logo-website-top-png-1-.webp" alt="Dahle Transport Logo">
            </a>
        </div>
        <div class="nav-links">
            <a href="/"><span>Hjem</span></a>
            <span>Om oss</span><span>Tjenester</span><span>Galleri</span><span>Kontakt</span>
        </div>
        <div class="nav-cta">
            <a href="/Opter_Portal" target="_self" class="cta-btn-outline">OPTER LOGIN</a>
            <a href="/" target="_self" class="cta-btn">TA KONTAKT</a>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<div class="header-banner">'
            '<h1 style="color: white; margin: 0;">Performance & Margin Analysis</h1>'
            '<p style="color: #e0d0e6; margin: 0;">Financial impact and sustainability tracking</p></div>', unsafe_allow_html=True)

# --- NAVIGATIE & INPUT ---
c_nav, c_input = st.columns([1, 2])
with c_nav:
    if st.button("← Back to Planner"):
        st.switch_page("pages/Planner.py")
with c_input:
    fuel_price = st.slider("Live Market Diesel Price (NOK/L)", 15.0, 30.0, 20.5)

# --- DATA VERWERKING ---
try:
    response = supabase.table("orders").select("*").execute()
    df = pd.DataFrame(response.data)
except Exception as e:
    st.error("Error loading data from database.")
    st.stop()

if df.empty:
    st.info("No order data available to generate the dashboard.")
    st.stop()

if 'co2_emission_kg' not in df.columns:
    import numpy as np
    np.random.seed(42)
    df['co2_emission_kg'] = np.random.uniform(40, 150, size=len(df))

# --- DE BEREKENINGEN ---
CO2_PER_LITER = 2.68
df['liters'] = df['co2_emission_kg'] / CO2_PER_LITER
df['fuel_cost'] = df['liters'] * fuel_price

df['revenue'] = 1500 + (df['co2_emission_kg'] * 15) 
df['profit'] = df['revenue'] - df['fuel_cost']
df['margin_pct'] = (df['profit'] / df['revenue']) * 100

# --- KPI SECTIE ---
st.write("### Performance Summary")
k1, k2, k3, k4 = st.columns(4)
total_profit = df['profit'].sum()
avg_margin = df['margin_pct'].mean()

k1.metric("Total Fuel Cost", f"{df['fuel_cost'].sum():,.0f} NOK")
k2.metric("Total Profit", f"{total_profit:,.0f} NOK", delta=f"{avg_margin:.1f}% Avg. Margin")
k3.metric("CO₂ Footprint", f"{df['co2_emission_kg'].sum():,.0f} kg")
k4.metric("Active Shipments", len(df))

st.write("---")

# --- GRAFIEKEN (STAAF + LIJN) ---
st.write("") 
col_left, col_right = st.columns(2, gap="large")

with col_left:
    st.write("### Profitability per Customer")
    df_chart = df.groupby('company')['profit'].sum().reset_index().sort_values('profit', ascending=False)
    
    # We gebruiken nu een Lichte template voor de grafieken zodat ze bij de achtergrond passen
    fig_profit = px.bar(df_chart, x='company', y='profit', color_discrete_sequence=['#894b9d'], template="plotly_white")
    fig_profit.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", xaxis_title="Customer", yaxis_title="Net Profit (NOK)")
    st.plotly_chart(fig_profit, use_container_width=True)

with col_right:
    st.write("### Profit Trend Over Time")
    
    if 'received_date' in df.columns:
        df['date'] = pd.to_datetime(df['received_date'], errors='coerce').dt.date
        df_trend = df.groupby('date')['profit'].sum().reset_index()
        
        fig_line = px.line(df_trend, x='date', y='profit', markers=True, 
                           color_discrete_sequence=['#27ae60'], template="plotly_white")
        fig_line.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", xaxis_title="Date", yaxis_title="Daily Profit (NOK)")
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("No date data available to generate a trendline.")

st.write("---")

# --- CUSTOMER CARDS (ONDERAAN) ---
st.write("### Detailed Cost & Margin Breakdown")
st.info("How is profit calculated? Profit = Estimated Revenue - Fuel Costs. The Margin % shows the percentage of revenue that remains as profit.")

customer_group = df.groupby('company').agg({
    'id': 'count',
    'fuel_cost': 'sum',
    'profit': 'sum',
    'margin_pct': 'mean'
}).reset_index().sort_values('profit', ascending=False)

card_col1, card_col2 = st.columns(2)
for i, (index, row) in enumerate(customer_group.iterrows()):
    target_col = card_col1 if i % 2 == 0 else card_col2
    with target_col:
        margin_color = "#27ae60" if row['margin_pct'] > 85 else "#e67e22"
        # Dankzij de toegevoegde CSS worden deze div's nu prachtig weergegeven!
        st.markdown(f"""
        <div class="customer-card">
            <div class="customer-name">{row['company']}</div>
            <div class="metric-row">
                <div class="metric-box">
                    <div class="metric-label">Shipments</div>
                    <div class="metric-value">{row['id']}</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">Fuel Cost</div>
                    <div class="metric-value">{row['fuel_cost']:,.0f} NOK</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">Net Profit</div>
                    <div class="metric-value" style="color: #27ae60;">{row['profit']:,.0f} NOK</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">Margin %</div>
                    <div class="metric-value" style="color: {margin_color};">{row['margin_pct']:.1f}%</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
