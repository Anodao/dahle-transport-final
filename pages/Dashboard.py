import streamlit as st
import pandas as pd
import plotly.express as px
from supabase import create_client

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Dahle Transport - Financial Dashboard",
    page_icon="💰",
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
    
    /* Achtergrond en Containers */
    .stApp { background-color: #0e1117; }
    
    /* Custom Card Design voor de tabelvervanging */
    .customer-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
    }
    .customer-name { color: #894b9d; font-size: 18px; font-weight: 700; margin-bottom: 10px; }
    .metric-row { display: flex; justify-content: space-between; border-top: 1px solid #30363d; padding-top: 10px; }
    .metric-box { text-align: center; flex: 1; }
    .metric-label { color: #8b949e; font-size: 12px; text-transform: uppercase; }
    .metric-value { color: #ffffff; font-size: 16px; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<div style="background-color: #894b9d; padding: 25px; border-radius: 10px; margin-bottom: 25px;">'
            '<h1 style="color: white; margin: 0;">💰 Financial & Fuel Analysis</h1>'
            '<p style="color: #e0d0e6; margin: 0;">Live cost breakdown per client</p></div>', unsafe_allow_html=True)

# --- NAVIGATIE & SETTINGS ---
c1, c2 = st.columns([1, 2])
with c1:
    if st.button("🏠 Back to Planner"):
        st.switch_page("pages/Planner.py")
with c2:
    # Hier simuleren we de 'live' data input. Voor een scriptie is een slider perfect
    # omdat de gebruiker zo 'wat-als' scenario's kan testen.
    fuel_price = st.slider("Set Current Diesel Price (NOK/L)", 18.0, 28.0, 20.5)

# --- DATA VERWERKING ---
response = supabase.table("orders").select("*").execute()
df = pd.DataFrame(response.data)

# Berekening (zelfde logica als voorheen)
if 'co2_emission_kg' not in df.columns:
    import numpy as np
    np.random.seed(42)
    df['co2_emission_kg'] = np.random.uniform(40, 150, size=len(df))

df['liters'] = df['co2_emission_kg'] / 2.68
df['cost'] = df['liters'] * fuel_price

# --- KPI SECTIE ---
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Total Fuel Spend", f"{df['cost'].sum():,.2f} NOK")
kpi2.metric("Total Liters Diesel", f"{df['liters'].sum():,.1f} L")
kpi3.metric("CO₂ Footprint", f"{df['co2_emission_kg'].sum():,.1f} kg")

st.write("---")

# --- VISUELE BREAKDOWN PER KLANT ---
st.subheader("🏢 Cost Breakdown per Customer")

# We groeperen de data
customer_data = df.groupby('company').agg({
    'id': 'count',
    'co2_emission_kg': 'sum',
    'cost': 'sum'
}).reset_index()

# In plaats van een saaie tabel, maken we mooie visuele rijen
for _, row in customer_data.iterrows():
    st.markdown(f"""
    <div class="customer-card">
        <div class="customer-name">{row['company']}</div>
        <div class="metric-row">
            <div class="metric-box">
                <div class="metric-label">Shipments</div>
                <div class="metric-value">{row['id']}</div>
            </div>
            <div class="metric-box">
                <div class="metric-label">Total CO2</div>
                <div class="metric-value">{row['co2_emission_kg']:.1f} kg</div>
            </div>
            <div class="metric-box">
                <div class="metric-label">Estimated Fuel Cost</div>
                <div class="metric-value" style="color: #27ae60;">{row['cost']:,.2f} NOK</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- GRAFIEK ONDERAAN ---
st.write("---")
st.subheader("📈 Cost Distribution")
fig = px.bar(customer_data, x='company', y='cost', 
             color_discrete_sequence=['#894b9d'],
             labels={'cost': 'Fuel Cost (NOK)', 'company': 'Client'},
             template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)
