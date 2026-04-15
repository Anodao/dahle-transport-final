import requests
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from supabase import create_client
import numpy as np

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Dahle Transport - Performance Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- POP-UP FUNCTIE ---
@st.dialog("🔍 Order History & Details")
def show_order_history(company_name, df):
    st.markdown(f"### {company_name}")
    st.write("Hier is het overzicht van alle afgehandelde orders voor deze specifieke klant.")
    st.write("---")
    
    cust_orders = df[df['company'] == company_name].sort_values('parsed_date', ascending=False)
    
    for _, order in cust_orders.iterrows():
        o_date = order['parsed_date'].strftime('%Y-%m-%d') if pd.notnull(order['parsed_date']) else "N/A"
        status = order.get('status', 'Unknown')
        
        with st.container(border=True):
            st.markdown(f"**Order #{order['id']}** — {o_date} `({status})`")
            st.write(f"🛣️ **Route:** {order.get('pickup_city', '-')} ➔ {order.get('delivery_city', '-')}")
            st.write(f"💰 **Profit:** {order['profit']:,.0f} NOK | **Margin:** {order['margin_pct']:.1f}%")

# --- LIVE API FUNCTIE VOOR DIESEL & GAS ---
@st.cache_data(ttl=3600)
def get_live_fuel_prices():
    url = "https://api.collectapi.com/gasPrice/europeanCountries"
    headers = {
        # JOUW NIEUWE API KEY IS HIER INGEVULD:
        'authorization': "apikey 40xj3EeeCTOZVeAjO2pEmj:7sLuMmcz7WUnrEdHaGiXyR",
        'content-type': "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        for country in data.get('result', []):
            if country['country'].lower() == 'norway':
                # FIX: vervang de komma door een punt zodat Python kan rekenen
                ruwe_diesel = country['diesel'].replace(',', '.')
                ruwe_gas = country['gasoline'].replace(',', '.')
                
                # Omrekenen van EUR naar NOK (koers 11.5)
                diesel_nok = round(float(ruwe_diesel) * 11.5, 2) 
                gas_nok = round(float(ruwe_gas) * 11.5, 2) 
                
                return {"diesel": diesel_nok, "gas": gas_nok}
                
    except Exception as e:
        print(f"API Error: {e}")
        
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

    .stApp { background-color: #111111 !important; }
    .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown li { color: #ffffff !important; }
    div[data-testid="stMetricValue"], div[data-testid="stMetricLabel"] { color: #ffffff !important; }

    [data-testid="collapsedControl"], [data-testid="stSidebar"], header[data-testid="stHeader"] { display: none !important; }
    
    .block-container { padding-top: 110px; }
    .navbar {
        position: fixed; top: 0; left: 0; width: 100%; height: 90px;
        background-color: #ffffff !important; z-index: 999; border-bottom: 1px solid #eaeaea; 
        display: grid; grid-template-columns: 1fr auto 1fr; align-items: center;
        padding: 0 40px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    .nav-logo a { display: inline-block; height: 48px; text-decoration: none; cursor: pointer; }
    .nav-logo img { height: 100%; width: auto; display: block; transition: transform 0.2s ease-in-out; }
    .nav-logo a:hover img { transform: scale(1.05); } 
    .nav-links { display: flex; gap: 28px; font-size: 15px; font-weight: 500; justify-content: center;}
    .nav-links a, .nav-links span { text-decoration: none; color: #111111 !important; cursor: pointer; transition: color 0.2s;}
    .nav-links span:hover { color: #894b9d !important; }
    .nav-cta { display: flex; justify-content: flex-end; gap: 15px; align-items: center; }
    
    .cta-btn { background-color: #894b9d !important; color: white !important; padding: 10px 24px; border-radius: 50px; text-decoration: none !important; font-weight: 600; font-size: 13px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); white-space: nowrap;}
    .cta-btn-outline { background-color: transparent !important; color: #894b9d !important; padding: 10px 20px; border-radius: 50px; text-decoration: none !important; font-weight: 600; font-size: 13px; border: 2px solid #894b9d; white-space: nowrap;}

    .header-banner { background-color: #723e83 !important; padding: 30px 40px; border-radius: 12px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.2); }
    .header-banner h1, .header-banner p { color: #ffffff !important; }
    .header-banner h1 { margin: 0; font-weight: 700; }
    .header-banner p { margin: 5px 0 0 0; font-size: 14px;}
    
    div[data-baseweb="select"] > div, div[data-baseweb="base-input"] { background-color: #212529 !important; border: 1px solid #333333 !important; border-radius: 6px !important; }
    .stSelectbox div[data-baseweb="select"] span, .stSelectbox div[data-baseweb="select"] div, .stDateInput input { color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; }
    label[data-testid="stWidgetLabel"] { color: #ffffff !important; font-weight: 600; font-size: 14px; }
    
    div[data-testid="stVerticalBlockBorderWrapper"] { background-color: #1a1a1a; border: 1px solid #333333; border-radius: 10px; padding: 15px; }
    div[data-testid="stAlert"] * { color: #b3d7ff !important; background-color: #0c355c !important; border-color: #0c355c !important;}
    </style>
    
    <div class="navbar">
        <div class="nav-logo">
            <a href="/" target="_self"><img src="https://cloud-1de12d.becdn.net/media/original/964295c9ae8e693f8bb4d6b70862c2be/logo-website-top-png-1-.webp"></a>
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
st.markdown('<div class="header-banner"><h1>Performance & Margin Analysis</h1><p>Financial impact and sustainability tracking</p></div>', unsafe_allow_html=True)

# --- DATUM LOGICA ---
today = datetime.now().date()
start_of_week = today - timedelta(days=today.weekday())
start_of_last_week = start_of_week - timedelta(days=7)
start_of_month = today.replace(day=1)

# --- GLOBAL PRIJZEN OPHALEN ---
live_prices = get_live_fuel_prices()
fuel_price = live_prices["diesel"]

# --- FILTER & API PRIJS UI ---
c_filter, c_input = st.columns([1, 2], gap="large")

with c_filter:
    filter_optie = st.selectbox("📅 Filter by date:", ["All orders", "Today", "This week", "Last week", "This month", "Custom date..."])
    custom_dates = []
    if filter_optie == "Custom date...":
        custom_dates = st.date_input("Select a date range:", value=today)

with c_input:
    # --- DATA SIMULATIE VOOR DE GRAFIEKJES ---
    dates = pd.date_range(end=today, periods=30)
    np.random.seed(int(today.strftime('%Y%m%d'))) 
    
    d_fluct = np.random.uniform(-0.3, 0.3, 30).cumsum()
    d_history = live_prices['diesel'] + d_fluct - d_fluct[-1]
    df_d = pd.DataFrame({'Date': dates, 'Price': d_history})
    
    g_fluct = np.random.uniform(-0.4, 0.4, 30).cumsum()
    g_history = live_prices['gas'] + g_fluct - g_fluct[-1]
    df_g = pd.DataFrame({'Date': dates, 'Price': g_history})

    # --- HULPFUNCTIE VOOR GEDETAILLEERDE GRAFIEK (Aangepast!) ---
    def make_detailed_chart(df, color):
        fig = px.line(df, x='Date', y='Price', template="plotly_dark")
        fig.update_layout(
            # Iets meer marge boven en rechts voor labels
            margin=dict(l=50, r=20, t=30, b=50), 
            height=200, # Veel hoger om assen kwijt te kunnen
            
            # --- ASSEN AAN ZETTEN EN FORMATTEREN ---
            xaxis=dict(
                visible=True, 
                title="Datum", 
                tickformat="%d %b", # Dag en Maand (bijv. 14 apr)
                showgrid=True,
                gridcolor="#333"
            ), 
            yaxis=dict(
                visible=True, 
                title="Prijs (NOK)", 
                tickformat=".2f NOK", # Afronden op 2 decimalen met NOK erachter
                showgrid=True,
                gridcolor="#333"
            ),
            
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            # Strakke pop-up (tooltip) behouden
            hoverlabel=dict(font_size=13, font_family="Montserrat") 
        )
        fig.update_traces(
            line_color=color, 
            line_width=3,
            # minimalistische tooltip
            hovertemplate="<b>%{x|%d %b %Y}</b><br>%{y:.2f} NOK<extra></extra>"
        )
        return fig
    
    f1, f2 = st.columns(2)
    with f1:
        # Stap 1: Kader maken
        with st.container(border=True):
            # Stap 2: Metric bovenin (geen kolommen meer nodig!)
            st.metric("⛽ Diesel (per Liter)", f"{live_prices['diesel']:.2f} NOK", "Actueel via API")
            
            # Stap 3: Gedetailleerde grafiek eronder over de volle breedte
            st.plotly_chart(make_detailed_chart(df_d, '#3498db'), use_container_width=True, config={'displayModeBar': False})
                
    with f2:
        # Stap 1: Kader maken
        with st.container(border=True):
            # Stap 2: Metric bovenin
            st.metric("🚗 Gas/Petrol (per Liter)", f"{live_prices['gas']:.2f} NOK", "Actueel via API")
            
            # Stap 3: Gedetailleerde grafiek eronder
            st.plotly_chart(make_detailed_chart(df_g, '#e67e22'), use_container_width=True, config={'displayModeBar': False})

st.write("---")

# --- DATA VERWERKING ---
# [De rest van de code blijft ongewijzigd...]
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
    np.random.seed(42)
    df['co2_emission_kg'] = np.random.uniform(40, 150, size=len(df))

CO2_PER_LITER = 2.68
df['liters'] = df['co2_emission_kg'] / CO2_PER_LITER
df['fuel_cost'] = df['liters'] * fuel_price
df['revenue'] = 1500 + (df['co2_emission_kg'] * 15) 
df['profit'] = df['revenue'] - df['fuel_cost']
df['margin_pct'] = (df['profit'] / df['revenue']) * 100

if 'received_date' in df.columns:
    df['parsed_date'] = pd.to_datetime(df['received_date'], errors='coerce').dt.date

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

# --- GRAFIEKEN ---
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
        fig_line = px.line(df_trend, x='date', y='profit', markers=True, color_discrete_sequence=['#27ae60'], template="plotly_dark")
        fig_line.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", xaxis_title="Date", yaxis_title="Daily Profit (NOK)")
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("No date data available to generate a trendline.")

st.write("---")

# --- CUSTOMER CARDS ---
st.write("### Detailed Cost & Margin Breakdown")
st.info("ℹ️ How is profit calculated? Profit = Estimated Revenue - Fuel Costs. The Margin % shows the percentage of revenue that remains as profit.")

customer_group = filtered_df.groupby('company').agg(
    total_orders=('id', 'count'),
    total_fuel=('fuel_cost', 'sum'),
    total_profit=('profit', 'sum'),
    avg_margin=('margin_pct', 'mean'),
    last_date=('parsed_date', 'max')
).reset_index().sort_values(by='last_date', ascending=False).reset_index(drop=True)

card_col1, card_col2 = st.columns(2)

for i, row in customer_group.iterrows():
    target_col = card_col1 if i % 2 == 0 else card_col2
    
    with target_col:
        with st.container(border=True):
            margin_color = "#27ae60" if row['avg_margin'] > 85 else "#e67e22"
            last_date_str = row['last_date'].strftime('%Y-%m-%d') if pd.notnull(row['last_date']) else "Onbekend"
            
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
            
            if st.button(f"🔍 View Orders", key=f"popup_{row['company']}", use_container_width=True):
                show_order_history(row['company'], filtered_df)
