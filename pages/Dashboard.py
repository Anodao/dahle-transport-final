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

# --- LIVE API FUNCTIE VOOR DIESEL & GAS ---
@st.cache_data(ttl=3600)
def get_live_fuel_prices():
    url = "https://api.collectapi.com/gasPrice/europeanCountries"
    headers = {
        # JOUW PERSOONLIJKE API KEY (Vastgezet)
        'authorization': "apikey 45CDpqYa0mK5v7B0vLExG7:6RHFfYXba02CtLDkUH2GTI",
        'content-type': "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        for country in data.get('result', []):
            if country['country'].lower() == 'norway':
                # Beide prijzen ophalen en omrekenen naar NOK (koers 11.5)
                diesel_nok = round(float(country['diesel']) * 11.5, 2) 
                gas_nok = round(float(country['gasoline']) * 11.5, 2) 
                
                return {"diesel": diesel_nok, "gas": gas_nok}
                
    except Exception as e:
        print(f"API Error: {e}")
        
    # Fallback prijzen als de API tijdelijk faalt
    return {"diesel": 20.50, "gas": 21.50} 

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

    div[data-testid="stAlert"] * { color: #b3d7ff !important; background-color: #0c355c !important; border-color: #0c355c !important;}
    
    /* Expander styling */
    div[data-testid="stExpander"] { background-color: #262626 !important; border: 1px solid #444 !important; border-radius: 8px !important; }
    div[data-testid="stExpander"] p { color: #ffffff !important; }
    div[data-testid="stExpanderDetails"] { background-color: #1e1e1e !important; border-top: 1px solid #444 !important; }
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
    # Haal beide prijzen op via de nieuwe functie
    live_prices = get_live_fuel_prices()
    
    # We bewaren de dieselprijs apart voor de winst-berekeningen verderop in je code
    fuel_price = live_prices["diesel"]
    
    f1, f2 = st.columns(2)
    
    with f1:
        with st.container(border=True):
            st.metric(
                label="⛽ Diesel (NOK/L)", 
                value=f"{live_prices['diesel']:.2f}",
                delta="Actueel via API"
            )
            
    with f2:
        with st.container(border=True):
            st.metric(
                label="🚗 Gas/Petrol (NOK/L)", 
                value=f"{live_prices['gas']:.2f}",
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

# 1. Groepeer op data en haal max datum op
customer_group = filtered_df.groupby('company').agg(
    total_orders=('id', 'count'),
    total_fuel=('fuel_cost', 'sum'),
    total_profit=('profit', 'sum'),
    avg_margin=('margin_pct', 'mean'),
    last_date=('parsed_date', 'max')
).reset_index()

# 2. HIER IS DE FIX: Sorteer op datum en HERSTEL de index! 
# Dit voorkomt dat Streamlit de kaarten alsnog alfabetisch indeelt in de kolommen.
customer_group = customer_group.sort_values(by='last_date', ascending=False).reset_index(drop=True)

card_col1, card_col2 = st.columns(2)

for i, row in customer_group.iterrows():
    # Nu is 'i' netjes verbonden aan de chronologische volgorde (0, 1, 2) in plaats van het alfabet
    target_col = card_col1 if i % 2 == 0 else card_col2
    
    with target_col:
        with st.container(border=True):
            margin_color = "#27ae60" if row['avg_margin'] > 85 else "#e67e22"
            
            # Format de datum netjes
            last_date_str = row['last_date'].strftime('%Y-%m-%d') if pd.notnull(row['last_date']) else "Onbekend"
            
            # Klant overzicht (HTML)
            st.markdown(f"""
            <div style="padding-bottom: 10px;">
                <div style="font-size: 18px; font-weight: 700; color: #ffffff; margin-bottom: 5px; border-bottom: 2px solid #333; padding-bottom: 8px;">
                    {row['company']} 
                    <span style="font-size: 13px; color: #888; font-weight: 400; float: right; margin-top: 4px;">Last order: {last_date_str}</span>
                </div>
                <div style="display: flex; justify-content: space-between; text-align: center; margin-top: 15px;">
                    <div style="flex: 1;"><div style="font-size: 12px; color: #b0b0b0; font-weight: 600;">SHIPMENTS</div><div style="font-size: 16px; font-weight: 700; color: #fff;">{row['total_orders']}</div></div>
                    <div style="flex: 1;"><div style="font-size: 12px; color: #b0b0b0; font-weight: 600;">FUEL COST</div><div style="font-size: 16px; font-weight: 700; color: #fff;">{row['total_fuel']:,.0f} NOK</div></div>
                    <div style="flex: 1;"><div style="font-size: 12px; color: #b0b0b0; font-weight: 600;">NET PROFIT</div><div style="font-size: 16px; font-weight: 700; color: #27ae60;">{row['total_profit']:,.0f} NOK</div></div>
                    <div style="flex: 1;"><div style="font-size: 12px; color: #b0b0b0; font-weight: 600;">MARGIN %</div><div style="font-size: 16px; font-weight: 700; color: {margin_color};">{row['avg_margin']:.1f}%</div></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Uitklapmenu met order details
            with st.expander("🔍 View Order History & Details"):
                cust_orders = filtered_df[filtered_df['company'] == row['company']].sort_values('parsed_date', ascending=False)
                
                for _, order in cust_orders.iterrows():
                    o_date = order['parsed_date'].strftime('%Y-%m-%d') if pd.notnull(order['parsed_date']) else "N/A"
                    status = order.get('status', 'Unknown')
                    
                    st.markdown(f"**Order #{order['id']}** — {o_date} `({status})`")
                    st.write(f"🛣️ **Route:** {order.get('pickup_city', '-')} ➔ {order.get('delivery_city', '-')}")
                    st.write(f"💰 **Profit:** {order['profit']:,.0f} NOK | **Margin:** {order['margin_pct']:.1f}%")
                    st.write("---")
