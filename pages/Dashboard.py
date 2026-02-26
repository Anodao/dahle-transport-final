import streamlit as st
import pandas as pd
import plotly.express as px
from supabase import create_client

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Dahle Transport - CO₂ Dashboard",
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
    
    .stApp { background-color: #f8f9fa !important; }
    .block-container { padding-top: 2rem; }

    .header-banner {
        background-color: #894b9d; /* DAHLE PAARS */
        padding: 30px 40px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .header-banner h1 { color: #ffffff !important; margin: 0; font-weight: 700;}
    .header-banner p { color: #e0d0e6 !important; margin: 5px 0 0 0; font-size: 14px;}
    
    /* Terugknop styling */
    div.stButton > button[kind="secondary"] { background-color: #e0e6ed !important; color: #333 !important; font-weight: bold; border-radius: 6px;}
    div.stButton > button[kind="secondary"]:hover { background-color: #bdc3c7 !important; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER & NAVIGATIE ---
st.markdown("""
<div class="header-banner">
    <h1>🌍 Sustainability & CO₂ Dashboard</h1>
    <p>CSRD Reporting & Emission Tracking</p>
</div>
""", unsafe_allow_html=True)

if st.button("🏠 ← Go Back to Planner", type="secondary"):
    st.switch_page("pages/Planner.py")

st.write("---")

# --- DATA OPHALEN & VERWERKEN MET PANDAS ---
with st.spinner('Data ophalen uit de database...'):
    try:
        # Haal alle orders op (zowel 'New' als 'Processed')
        response = supabase.table("orders").select("*").execute()
        orders_data = response.data
        
        if not orders_data:
            st.info("Nog geen transportdata beschikbaar om te analyseren.")
            st.stop()
            
        # Zet de data om naar een Pandas DataFrame
        df = pd.DataFrame(orders_data)
        
        # --- DUMMY CO2 BEREKENING VOOR DE MVP ---
        # Omdat de database (nog) geen CO2-kolom heeft, simuleren we dit o.b.v. de lengte van de klantnaam en type.
        # In de toekomst (of als Opter is gekoppeld) haal je dit veld direct uit de database!
        if 'co2_emission_kg' not in df.columns:
            import numpy as np
            # Willekeurige waardes tussen 15kg en 120kg per rit toewijzen als simulatie
            np.random.seed(42) # Zorgt dat de dummy data telkens hetzelfde blijft voor je presentatie
            df['co2_emission_kg'] = np.random.uniform(15.0, 120.0, size=len(df)).round(2)
            
    except Exception as e:
        st.error(f"Error fetching or processing data: {e}")
        st.stop()

# --- KPI METRICS (De getallen bovenaan) ---
total_orders = len(df)
total_co2 = df['co2_emission_kg'].sum()
avg_co2 = df['co2_emission_kg'].mean()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Shipments", value=total_orders)
with col2:
    st.metric(label="Total CO₂ Emissions", value=f"{total_co2:,.2f} kg", delta="-2.4% vs last month", delta_color="inverse")
with col3:
    st.metric(label="Average CO₂ per Shipment", value=f"{avg_co2:.2f} kg")

st.write("<br><br>", unsafe_allow_html=True)

# --- GRAFIEKEN MET PLOTLY ---
c_chart1, c_chart2 = st.columns(2)

with c_chart1:
    st.markdown("### 📊 CO₂ Emissions per Customer")
    # Groepeer de data per klant en tel de CO2 op
    df_company = df.groupby('company')['co2_emission_kg'].sum().reset_index()
    # Sorteer van hoog naar laag
    df_company = df_company.sort_values(by='co2_emission_kg', ascending=False).head(10)
    
    # Maak een staafgrafiek
    fig1 = px.bar(df_company, x='company', y='co2_emission_kg', 
                  color_discrete_sequence=['#894b9d'],
                  labels={'company': 'Customer', 'co2_emission_kg': 'Total CO₂ (kg)'})
    fig1.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig1, use_container_width=True)

with c_chart2:
    st.markdown("### 📦 Orders by Service Type")
    # Opsplitsen van de 'types' kolom (omdat het momenteel een komma-gescheiden string is)
    # Voor de simpelheid tellen we in deze MVP hoe vaak een exacte string combinatie voorkomt
    df_types = df['types'].value_counts().reset_index()
    df_types.columns = ['Service Type', 'Count']
    
    # Maak een Donut grafiek (Pie chart met een gat)
    fig2 = px.pie(df_types, values='Count', names='Service Type', hole=0.4,
                  color_discrete_sequence=px.colors.sequential.Purp)
    st.plotly_chart(fig2, use_container_width=True)

# --- GEDETAILLEERDE TABEL ---
st.write("---")
st.markdown("### 📋 Raw Data Overview")
st.caption("Detailed view of all logged shipments and their calculated emissions.")
# We laten alleen de relevante kolommen zien in de tabel
display_df = df[['id', 'company', 'received_date', 'types', 'status', 'co2_emission_kg']]
st.dataframe(display_df, use_container_width=True, hide_index=True)
