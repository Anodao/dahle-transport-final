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

# --- CSS: ULTIEME SIDEBAR & HEADER VERWIJDERING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    /* VERWIJDER DE HELE BOVENBALK (Inclusief het >> icoontje) */
    header[data-testid="stHeader"] {
        visibility: hidden;
        height: 0%;
    }
    
    /* VERWIJDER DE SIDEBAR VOLLEDIG */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* Zorg dat de content bovenaan begint nu de header weg is */
    .block-container {
        padding-top: 1rem;
        max-width: 95%;
    }

    .stApp { background-color: #0e1117; }
    
    .header-banner {
        background-color: #894b9d;
        padding: 25px;
        border-radius: 10px;
        margin-bottom: 25px;
    }
    
    .customer-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
    }
    
    .customer-name { color: #894b9d; font-size: 18px; font-weight: 700; margin-bottom: 12px; }
    .metric-row { display: flex; justify-content: space-between; border-top: 1px solid #30363d; padding-top: 12px; }
    .metric-box { text-align: center; flex: 1; }
    .metric-label { color: #8b949e; font-size: 11px; text-transform: uppercase; }
    .metric-value { color: #ffffff; font-size: 15px; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<div class="header-banner">'
            '<h1 style="color: white; margin: 0;">📈 Performance & Margin Analysis</h1>'
            '<p style="color: #e0d0e6; margin: 0;">Financial impact and sustainability tracking</p></div>', unsafe_allow_html=True)

# --- NAVIGATIE & INPUT ---
c_nav, c_input = st.columns([1, 2])
with c_nav:
    if st.button("🏠 Back to Planner"):
        st.switch_page("pages/Planner.py")
with c_input:
    fuel_price = st.slider("Live Market Diesel Price (NOK/L)", 15.0, 30.0, 20.5)

# --- DATA VERWERKING ---
response = supabase.table("orders").select("*").execute()
df = pd.DataFrame(response.data)

if 'co2_emission_kg' not in df.columns:
    import numpy as np
    np.random.seed(42)
    df['co2_emission_kg'] = np.random.uniform(40, 150, size=len(df))

# --- DE BEREKENINGEN ---
CO2_PER_LITER = 2.68
df['liters'] = df['co2_emission_kg'] / CO2_PER_LITER
df['fuel_cost'] = df['liters'] * fuel_price

# We simuleren omzet: een vast starttarief van 1500 NOK + 15 NOK per kg CO2 (afstand-proxy)
df['revenue'] = 1500 + (df['co2_emission_kg'] * 15) 
df['profit'] = df['revenue'] - df['fuel_cost']
df['margin_pct'] = (df['profit'] / df['revenue']) * 100

# --- KPI SECTIE ---
st.write("### 📊 Performance Summary")
k1, k2, k3, k4 = st.columns(4)
total_profit = df['profit'].sum()
avg_margin = df['margin_pct'].mean()

k1.metric("Total Fuel Cost", f"{df['fuel_cost'].sum():,.0f} NOK")
k2.metric("Total Profit", f"{total_profit:,.0f} NOK", delta=f"{avg_margin:.1f}% Avg. Margin")
k3.metric("CO₂ Footprint", f"{df['co2_emission_kg'].sum():,.0f} kg")
k4.metric("Active Shipments", len(df))

st.write("---")

# --- GRAFIEKEN ---
col_left, col_right = st.columns(2)
with col_left:
    st.write("### 📈 Profitability per Customer")
    df_chart = df.groupby('company')['profit'].sum().reset_index().sort_values('profit', ascending=False)
    fig_profit = px.bar(df_chart, x='company', y='profit', color_discrete_sequence=['#894b9d'], template="plotly_dark")
    fig_profit.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_profit, use_container_width=True)

with col_right:
    st.write("### 🍃 Emission Share")
    fig_pie = px.pie(df, values='co2_emission_kg', names='company', hole=0.4, color_discrete_sequence=px.colors.sequential.Purp, template="plotly_dark")
    fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_pie, use_container_width=True)

st.write("---")

# --- CUSTOMER CARDS (ONDERAAN) ---
st.write("### 🏢 Detailed Cost & Margin Breakdown")
st.info("ℹ️ **How is profit calculated?** Profit = Estimated Revenue - Fuel Costs. The Margin % shows the percentage of revenue that remains as profit.")

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
