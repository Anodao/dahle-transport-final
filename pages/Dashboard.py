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

# --- CSS VOOR EEN PROFESSIONEEL DASHBOARD ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    .stApp { background-color: #0e1117; }
    
    /* Dahle Paars Banner */
    .header-banner {
        background-color: #894b9d;
        padding: 25px;
        border-radius: 10px;
        margin-bottom: 25px;
    }
    
    /* Custom Card Design */
    .customer-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
        transition: transform 0.2s;
    }
    .customer-card:hover { border-color: #894b9d; transform: translateY(-2px); }
    
    .customer-name { color: #894b9d; font-size: 20px; font-weight: 700; margin-bottom: 15px; }
    .metric-row { display: flex; justify-content: space-between; border-top: 1px solid #30363d; padding-top: 12px; }
    .metric-box { text-align: center; flex: 1; }
    .metric-label { color: #8b949e; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; }
    .metric-value { color: #ffffff; font-size: 16px; font-weight: 600; }
    
    /* Terugknop styling */
    div.stButton > button { border-radius: 6px; font-weight: 600; }
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
    fuel_price = st.slider("Current Diesel Price (NOK/L)", 15.0, 30.0, 20.5)

# --- DATA VERWERKING ---
response = supabase.table("orders").select("*").execute()
df = pd.DataFrame(response.data)

# Simulatie van data voor de berekeningen
if 'co2_emission_kg' not in df.columns:
    import numpy as np
    np.random.seed(42)
    df['co2_emission_kg'] = np.random.uniform(40, 150, size=len(df))

# 1. Brandstof kosten berekening
df['liters'] = df['co2_emission_kg'] / 2.68
df['fuel_cost'] = df['liters'] * fuel_price

# 2. Omzet simulatie (Revenue) - Nodig om winst te berekenen
# We gaan uit van een basis tarief + een bedrag per kg CO2 (als proxy voor afstand/gewicht)
df['revenue'] = 1500 + (df['co2_emission_kg'] * 15) 

# 3. Winst en Marge berekening
df['profit'] = df['revenue'] - df['fuel_cost']
df['margin_pct'] = (df['profit'] / df['revenue']) * 100

# --- KPI SECTIE ---
st.write("### 📊 Key Performance Indicators")
k1, k2, k3, k4 = st.columns(4)
total_profit = df['profit'].sum()
avg_margin = df['margin_pct'].mean()

k1.metric("Total Fuel Cost", f"{df['fuel_cost'].sum():,.0f} NOK")
k2.metric("Total Profit", f"{total_profit:,.0f} NOK", delta=f"{avg_margin:.1f}% Margin")
k3.metric("CO₂ Emissions", f"{df['co2_emission_kg'].sum():,.0f} kg")
k4.metric("Shipments", len(df))

st.write("---")

# --- GRAFIEKEN ---
col_left, col_right = st.columns(2)

with col_left:
    st.write("### 📈 Profit per Customer")
    df_chart = df.groupby('company')['profit'].sum().reset_index().sort_values('profit', ascending=False)
    fig_profit = px.bar(df_chart, x='company', y='profit', color_discrete_sequence=['#894b9d'], template="plotly_dark")
    st.plotly_chart(fig_profit, use_container_width=True)

with col_right:
    st.write("### 🍃 Emission Distribution")
    fig_pie = px.pie(df, values='co2_emission_kg', names='company', hole=0.4, color_discrete_sequence=px.colors.sequential.Purp, template="plotly_dark")
    st.plotly_chart(fig_pie, use_container_width=True)

st.write("---")

# --- CUSTOMER CARDS (NU ONDERAAN) ---
st.write("### 🏢 Cost & Margin Breakdown per Customer")
st.caption("Detailed financial performance per client based on current fuel prices.")

# Groepeer data voor de kaarten
customer_group = df.groupby('company').agg({
    'id': 'count',
    'fuel_cost': 'sum',
    'profit': 'sum',
    'margin_pct': 'mean'
}).reset_index().sort_values('profit', ascending=False)

# Loop door de klanten voor de kaarten
for _, row in customer_group.iterrows():
    # Kleur bepalen voor marge (groen als het hoog is)
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
                <div class="metric-label">Total Profit</div>
                <div class="metric-value" style="color: #27ae60;">{row['profit']:,.0f} NOK</div>
            </div>
            <div class="metric-box">
                <div class="metric-label">Margin %</div>
                <div class="metric-value" style="color: {margin_color};">{row['margin_pct']:.1f}%</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
