import streamlit as st
import pandas as pd
import plotly.express as px
from supabase import create_client

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Dahle Transport - CO₂ & Cost Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- SUPABASE CONNECTIE ---
@st.cache_resource
def init_connection():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

try:
    supabase = init_connection()
except Exception as e:
    st.error("⚠️ Database connection failed. Please check your secrets.toml file.")
    st.stop()

# --- CSS STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }
    
    [data-testid="collapsedControl"] { display: none !important; }
    [data-testid="stSidebar"] { display: none !important; }
    header[data-testid="stHeader"] { display: none !important; }
    
    .block-container { padding-top: 2rem; }
    
    .header-banner {
        background-color: #894b9d;
        padding: 30px 40px;
        border-radius: 12px;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .header-banner h1 { color: #ffffff !important; margin: 0; font-weight: 700;}
    .header-banner p { color: #e0d0e6 !important; margin: 5px 0 0 0; font-size: 14px;}
    
    div.stButton > button[kind="secondary"] { font-weight: bold; border-radius: 6px; margin-bottom: 20px;}
    </style>
""", unsafe_allow_html=True)

# --- HEADER & NAVIGATIE ---
st.markdown("""
<div class="header-banner">
    <h1>🌍 Sustainability & Fuel Cost Dashboard</h1>
    <p>CSRD Reporting, Emission Tracking & Financial Impact</p>
</div>
""", unsafe_allow_html=True)

if st.button("🏠 ← Go Back to Planner", type="secondary"):
    st.switch_page("pages/Planner.py")

# --- DATA OPHALEN & VERWERKEN ---
with st.spinner('Fetching database records...'):
    try:
        response = supabase.table("orders").select("*").execute()
        orders_data = response.data
        
        if not orders_data:
            st.info("No transport data available yet.")
            st.stop()
            
        df = pd.DataFrame(orders_data)
        
        # 1. Dummy CO2 data genereren als de kolom nog niet bestaat
        if 'co2_emission_kg' not in df.columns:
            import numpy as np
            np.random.seed(42) 
            df['co2_emission_kg'] = np.random.uniform(15.0, 120.0, size=len(df)).round(2)
        
        # 2. FINANCIËLE BEREKENING TOEVOEGEN
        DIESEL_PRICE_NOK = 20.50  # Gemiddelde dieselprijs in Noorwegen (pas aan indien nodig)
        CO2_PER_LITER = 2.68      # 1 liter diesel = ~2.68 kg CO2
        
        # Bereken de liters en de uiteindelijke kosten
        df['fuel_liters'] = df['co2_emission_kg'] / CO2_PER_LITER
        df['fuel_cost_nok'] = (df['fuel_liters'] * DIESEL_PRICE_NOK).round(2)
            
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        st.stop()

# --- KPI METRICS ---
total_orders = len(df)
total_co2 = df['co2_emission_kg'].sum()
total_fuel_cost = df['fuel_cost_nok'].sum()
avg_co2 = df['co2_emission_kg'].mean()

# We maken nu 4 kolommen in plaats van 3, zodat de kosten er mooi naast passen!
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Total Shipments", value=total_orders)
with col2:
    st.metric(label="Total CO₂ Emissions", value=f"{total_co2:,.0f} kg")
with col3:
    st.metric(label="Avg. CO₂ per Shipment", value=f"{avg_co2:.1f} kg")
with col4:
    # Nieuwe financiële metric
    st.metric(label="Estimated Fuel Cost", value=f"{total_fuel_cost:,.2f} NOK", delta="Based on 20.50 NOK/L", delta_color="off")

st.write("<br><br>", unsafe_allow_html=True)

# --- GRAFIEKEN MET PLOTLY ---
c_chart1, c_chart2 = st.columns(2, gap="large")

with c_chart1:
    st.markdown("### 📊 Financial Impact & CO₂ per Customer")
    # We tonen nu de kosten in de grafiek in plaats van alleen de CO2
    df_company = df.groupby('company').agg({'co2_emission_kg':'sum', 'fuel_cost_nok':'sum'}).reset_index()
    df_company = df_company.sort_values(by='fuel_cost_nok', ascending=False).head(10)
    
    fig1 = px.bar(df_company, x='company', y='fuel_cost_nok', 
                  color_discrete_sequence=['#894b9d'],
                  labels={'company': 'Customer', 'fuel_cost_nok': 'Estimated Fuel Cost (NOK)'},
                  hover_data=['co2_emission_kg']) # Toon de CO2 nog wel als je er met de muis overheen gaat!
    
    st.plotly_chart(fig1, use_container_width=True, theme="streamlit")

with c_chart2:
    st.markdown("### 📦 Orders by Service Type")
    df_types = df['types'].value_counts().reset_index()
    df_types.columns = ['Service Type', 'Count']
    
    fig2 = px.pie(df_types, values='Count', names='Service Type', hole=0.4,
                  color_discrete_sequence=px.colors.sequential.Purp)
                  
    st.plotly_chart(fig2, use_container_width=True, theme="streamlit")
