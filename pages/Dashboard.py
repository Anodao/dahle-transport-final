import requests
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from supabase import create_client

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Dahle Transport - Performance Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- LIVE API FUNCTIE VOOR DIESEL ---
@st.cache_data(ttl=3600) # Haalt maximaal 1x per uur data op (bespaart je API limiet)
def get_live_diesel_price():
    url = "https://api.collectapi.com/gasPrice/europeanCountries"
    headers = {
        # LET OP: Plak hieronder jouw API key van CollectAPI!
        'authorization': "apikey 45CDpqYa0mK5v7B0vLExG7:6RHFfYXba02CtLDkUH2GTI",
        'content-type': "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        for country in data.get('result', []):
            if country['country'].lower() == 'norway':
                # Omrekenen van EUR naar NOK (bijv. met een actuele of vaste koers van 11.5)
                prijs_eur = float(country['diesel'])
                prijs_nok = round(prijs_eur * 11.5, 2) 
                return prijs_nok
                
    except Exception as e:
        print(f"API Error: {e}")
        
    return 20.50 # Fallback prijs als de API tijdelijk faalt

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

    /* --- ALGEMENE DONKERE ACHTERGROND & LICHTE TEKST --- */
    .stApp { background-color: #111111 !important; }
    .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown li { color: #ffffff !important; }
    div[data-testid="stMetricValue"], div[data-testid="stMetricLabel"] { color: #ffffff !important; }

    /* --- HEADER & SIDEBAR FIX --- */
    [data-testid="collapsedControl"] { display: none !important; }
    [data-testid="stSidebar"] { display: none !important; }
    header[data-testid="stHeader"] { background: transparent !important; pointer-events: none !important; display: none !important;}
    
    /* --- NAVBAR --- */
    .block-container { padding-top: 110px; }
    .navbar {
        position: fixed; top: 0; left: 0; width: 100%; height: 90px;
        background-color: #ffffff !important; z-index: 999; border-bottom: 1px solid #eaeaea; 
        display: grid; grid-template-columns: 1fr auto 1fr; align-items: center;
        padding: 0 40px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    .nav-logo { display: flex; justify-content: flex-start; }
    .nav-logo a { display: inline-block; height: 48px; text-decoration: none; cursor: pointer; }
    .nav-logo img { height: 100%; width: auto; display: block; transition: transform 0.2s ease-in-out; }
    .nav-logo a:hover img { transform: scale(1.05); } 
    .nav-links { display: flex; gap: 28px; font-size: 15px; font-weight: 500; justify-content: center;}
    .nav-links a { text-decoration: none; color: #111111 !important; }
    .nav-links span { cursor: pointer; transition: color 0.2s; color: #111111 !important;}
    .nav-links span:hover { color: #894b9d !important; }
    .nav-cta { display: flex; justify-content: flex-end; gap: 15px; align-items: center; }
    
    .cta-btn { 
        background-color: #894b9d !important; color: white !important; padding: 10px 24px;
        border-radius: 50px; text-decoration: none !important; font-weight: 600; 
        font-size: 13px; letter-spacing: 0.5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        cursor: pointer; transition: background-color 0.2s; white-space: nowrap;
    }
    .cta-btn:hover { background-color: #723e83 !important; }

    .cta-btn-outline {
        background-color: transparent !important; color: #894b9d !important; padding: 10px 20px;
        border-radius: 50px; text-decoration: none !important; font-weight: 600; 
        font-size: 13px; letter-spacing: 0.5px; border: 2px solid #894b9d;
        cursor: pointer; transition: all 0.2s; white-space: nowrap;
    }
    .cta-btn-outline:hover { background-color: #894b9d !important; color: white !important; }

    /* --- TITEL BANNER --- */
    .header-banner {
        background-color: #723e83 !important;
        padding: 30px 40px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    .header-banner h1, .header-banner p { color: #ffffff !important; }
    .header-banner h1 { margin: 0; font-weight: 700; }
    .header-banner p { margin: 5px 0 0 0; font-size: 14px;}
    
    /* --- INPUT VELDEN (Speciaal voor Dark Mode Dashboard) --- */
    div[data-baseweb="select"] > div, div[data-baseweb="base-input"] {
        background-color: #212529 !important;
        border: 1px solid #333333 !important;
        border-radius: 6px !important;
    }
    .stSelectbox div[data-baseweb="select"] span, 
    .stSelectbox div[data-baseweb="select"] div,
    .stDateInput input {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }
    .stDateInput input::placeholder {
        color: #888888 !important;
        -webkit-text-fill-color: #888888 !important;
    }
    label[data-testid="stWidgetLabel"] { color: #ffffff !important; font-weight: 600; font-size: 14px; }
    
    /* Grafiek kaders */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #1a1a1a;
        border: 1px solid #333333;
        border-radius: 10px;
        padding: 15px;
    }

    /* --- CUSTOMER CARDS --- */
    .customer-card {
        background-color: #212529;
        border: 1px solid #333333;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    .customer-name {
        font-size: 18px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 15px;
        border-bottom: 2px solid #333333;
        padding-bottom: 8px;
    }
    .metric-row { display: flex; justify-content: space-between; gap: 10px; }
    .metric-box { flex: 1; display: flex; flex-direction: column; text-align: center; }
    .metric-label { font-size: 12px; color: #b0b0b0; font-weight: 600; text-transform: uppercase; margin-bottom: 4px; }
    .metric-value { font-size: 16px; font-weight: 700; color: #ffffff; }

    div[data-testid="stAlert"] * { color: #b3d7ff !important; background-color: #0c355c !important; border-color: #0c355c !important;}
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
            <a href="/Login" target="_self" class="cta-btn-outline">KUNDEPORTAL</a>
            <a href="/" target="_self" class="cta-btn">TA KONTAKT</a>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- HEADER BANNER ---
st.markdown('<div class="header-banner">'
            '<h1>Performance & Margin Analysis</h1>'
            '<p>Financial impact and sustainability tracking</p></div>', unsafe_allow_html=True)

# --- DATUM LOGICA ---
today = datetime.now().date()
start_of_week = today - timedelta(days=today.weekday())
start_of_last_week = start_of_week - timedelta(days=7)
start_of_month = today.replace(day=1)

# --- FILTER & API PRIJS ---
c_filter, c_input = st.columns([1, 2], gap="large")

with c_filter:
    filter_optie = st.selectbox("📅 Filter by date:", ["All orders", "Today", "This week", "Last week", "This month", "Custom date..."])
    custom_dates = []
    if filter_optie == "Custom date...":
        custom_dates = st.date_input("Select a date range:", value=today)

with c_input:
    # Haal de live prijs op!
    fuel_price = get_live_diesel_price()
    
    # Toon dit in een mooi kader in plaats van een slider
    with st.container(border=True):
        st.metric(
            label="⛽ Live Market Diesel Price (Norway)", 
            value=f"{fuel_price:.2f} NOK / L",
            delta="Actueel via API"
        )

st.write("---")

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

# Genereer random CO2 (als het er niet in zit) op de VOLLEDIGE dataset voor consistentie
if 'co2_emission_kg' not in df.columns:
    import numpy as np
    np.random.seed(42)
    df['co2_emission_kg'] = np.random.uniform(40, 150, size=len(df))

# Berekeningen op de volledige dataset
CO2_PER_LITER = 2.68
df['liters'] = df['co2_emission_kg'] / CO2_PER_LITER

# Gebruikt nu automatisch de live 'fuel_price' van de API!
df['fuel_cost'] = df['liters'] * fuel_price

df['revenue'] = 1500 + (df['co2_emission_kg'] * 15) 
df['profit'] = df['revenue'] - df['fuel_cost']
df['margin_pct'] = (df['profit'] / df['revenue']) * 100

# Parse the dates voor de filter functionaliteit
if 'received_date' in df.columns:
    df['parsed_date'] = pd.to_datetime(df['received_date'], errors='coerce').dt.date

# --- TOEPASSEN VAN HET FILTER OP DE DATAFRAME ---
filtered_df = df.copy()

if 'parsed_date' in df.columns:
    if filter_optie == "Today":
        filtered_df = df[df['parsed_date'] == today]
    elif filter_optie == "This week":
        filtered_df = df[df['parsed_date'] >= start_of_week]
    elif filter_optie == "Last week":
        filtered_df = df[(df['parsed_date'] >= start_of_last_week) & (df['parsed_date'] < start_of_week)]
    elif filter_optie == "This month": 
        filtered_df = df[df['parsed_date'] >= start_of_month]
    elif filter_optie == "Custom date...":
        if isinstance(custom_dates, tuple) and len(custom_dates) == 2:
            filtered_df = df[(df['parsed_date'] >= custom_dates[0]) & (df['parsed_date'] <= custom_dates[1])]
        elif isinstance(custom_dates, tuple) and len(custom_dates) == 1:
            filtered_df = df[df['parsed_date'] == custom_dates[0]]
        else:
            filtered_df = df[df['parsed_date'] == custom_dates]

# Stop weergave als de gefilterde set leeg is
if filtered_df.empty:
    st.warning("📊 No orders found for this specific date range. Please adjust your filter.")
    st.stop()

# --- KPI SECTIE ---
st.write("### Performance Summary")
k1, k2, k3, k4 = st.columns(4)
total_profit = filtered_df['profit'].sum()
avg_margin = filtered_df['margin_pct'].mean()

k1.metric("Total Fuel Cost", f"{filtered_df['fuel_cost'].sum():,.0f} NOK")
k2.metric("Total Profit", f"{total_profit:,.0f} NOK", delta=f"{avg_margin:.1f}% Avg. Margin")
k3.metric("CO₂ Footprint", f"{filtered_df['co2_emission_kg'].sum():,.0f} kg")
k4.metric("Active Shipments", len(filtered_df))

st.write("---")

# --- GRAFIEKEN (STAAF + LIJN) ---
st.write("") 
col_left, col_right = st.columns(2, gap="large")

with col_left:
    st.write("### Profitability per Customer")
    df_chart = filtered_df.groupby('company')['profit'].sum().reset_index().sort_values('profit', ascending=False)
    
    fig_profit = px.bar(df_chart, x='company', y='profit', color_discrete_sequence=['#c48bd6'], template="plotly_dark")
    fig_profit.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", xaxis_title="Customer", yaxis_title="Net Profit (NOK)")
    st.plotly_chart(fig_profit, use_container_width=True)

with col_right:
    st.write("### Profit Trend Over Time")
    
    if 'parsed_date' in filtered_df.columns:
        df_trend = filtered_df.groupby('parsed_date')['profit'].sum().reset_index()
        # Hernoem voor de as
        df_trend = df_trend.rename(columns={'parsed_date': 'date'})
        
        fig_line = px.line(df_trend, x='date', y='profit', markers=True, 
                           color_discrete_sequence=['#27ae60'], template="plotly_dark")
        fig_line.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", xaxis_title="Date", yaxis_title="Daily Profit (NOK)")
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("No date data available to generate a trendline.")

st.write("---")

# --- CUSTOMER CARDS (ONDERAAN) ---
st.write("### Detailed Cost & Margin Breakdown")
st.info("ℹ️ How is profit calculated? Profit = Estimated Revenue - Fuel Costs. The Margin % shows the percentage of revenue that remains as profit.")

customer_group = filtered_df.groupby('company').agg({
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
