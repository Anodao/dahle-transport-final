import requests
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from supabase import create_client
import numpy as np
import time
import extra_streamlit_components as stx

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Dahle Transport - Performance Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# 1. DIRECTE CSS INJECTIE 
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; margin: 0; padding: 0; }
.stApp { background-color: #111111 !important; }
.block-container { padding-top: 130px !important; max-width: 100% !important; margin-top: 0px; padding-left: 5%; padding-right: 5%; }
.stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown li { color: #ffffff !important; }
div[data-testid="stMetricValue"], div[data-testid="stMetricLabel"] { color: #ffffff !important; }

/* VERBERG STREAMLIT BRANDING VOLLEDIG */
[data-testid="collapsedControl"], [data-testid="stSidebar"], header[data-testid="stHeader"] { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
footer { display: none !important; }
div[class^="viewerBadge"] { display: none !important; }

/* NAVBAR CSS */
.navbar { position: fixed; top: 0; left: 0; width: 100%; height: 90px; background-color: #ffffff !important; z-index: 999; display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; padding: 0 40px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
.nav-logo { display: flex; justify-content: flex-start; margin-left: 20px; }
.nav-logo a { display: inline-block; height: 48px; text-decoration: none; cursor: pointer; }
.nav-logo img { height: 100%; width: auto; display: block; transition: transform 0.2s ease-in-out; }
.nav-logo a:hover img { transform: scale(1.05); } 

.nav-links { display: flex; gap: 28px; font-size: 15px; font-weight: 600; justify-content: center; align-items: center;}
.nav-links a, .nav-links span { text-decoration: none; color: #111111 !important; cursor: pointer; transition: color 0.2s;}
.nav-links span:hover { color: #894b9d !important; }

/* HET NIEUWE TEKST-DROPDOWN MENU NAAST 'CONTACT' */
.nav-text-dropdown { position: relative; display: inline-block; cursor: pointer; padding-bottom: 20px; margin-bottom: -20px; }
.nav-text-dropbtn { background: transparent; border: none; font-size: 15px; font-weight: 600; color: #111111 !important; cursor: pointer; padding: 0; font-family: inherit; transition: color 0.2s; display: flex; align-items: center; gap: 4px; }
.nav-text-dropdown:hover .nav-text-dropbtn { color: #894b9d !important; }
.nav-text-dropdown-content { display: none; position: absolute; top: 40px; left: 50%; transform: translateX(-50%); background-color: #ffffff; min-width: 180px; box-shadow: 0px 8px 24px rgba(0,0,0,0.12); border-radius: 12px; border: 1px solid #eaeaea; z-index: 1000; overflow: hidden; }
.nav-text-dropdown-content a { color: #111111 !important; padding: 12px 16px; text-decoration: none; display: block; font-size: 14px; font-weight: 500; text-align: left; transition: background-color 0.2s; }
.nav-text-dropdown-content a:hover { background-color: #f4e9f7; color: #894b9d !important; }
.nav-text-dropdown:hover .nav-text-dropdown-content { display: block; }

/* DE KNOPPEN RECHTS */
.nav-cta { display: flex; justify-content: flex-end; gap: 15px; align-items: center; }
.cta-btn-purple { background-color: #894b9d !important; color: white !important; padding: 10px 24px; border-radius: 50px; text-decoration: none !important; font-weight: 600; font-size: 13px; transition: background-color 0.2s; white-space: nowrap;}
.cta-btn-purple:hover { background-color: #723e83 !important; }
.cta-btn-outline { background-color: transparent !important; color: #894b9d !important; padding: 10px 20px; border-radius: 50px; text-decoration: none !important; font-weight: 600; font-size: 13px; border: 2px solid #894b9d; max-width: 250px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;}
.cta-btn-outline:hover { background-color: #f4e9f7 !important; }

/* TAAL DROPDOWN */
.lang-dropdown { position: relative; display: inline-block; margin-right: 10px; padding-bottom: 15px; margin-bottom: -15px; }
.lang-dropbtn { background-color: #f8f9fa; color: #111; font-weight: 600; font-size: 13px; border: 1px solid #eaeaea; border-radius: 20px; padding: 8px 16px; cursor: pointer; display: flex; align-items: center; gap: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.03); transition: all 0.2s ease; }
.lang-dropbtn:hover { background-color: #eaeaea; }
.lang-dropdown-content { display: none; position: absolute; background-color: #ffffff; min-width: 140px; box-shadow: 0px 8px 24px rgba(0,0,0,0.12); border-radius: 12px; border: 1px solid #eaeaea; z-index: 1000; top: 100%; right: 0; margin-top: 5px; overflow: hidden; }
.lang-dropdown-content a { color: #111 !important; padding: 12px 16px; text-decoration: none; display: flex; align-items: center; gap: 10px; font-size: 14px; font-weight: 500; transition: background-color 0.2s; }
.lang-dropdown-content a:hover { background-color: #f4e9f7; color: #894b9d !important; }
.lang-dropdown:hover .lang-dropdown-content { display: block; }

/* Dashboard elementen styling */
div[data-baseweb="select"] > div, div[data-baseweb="base-input"] { background-color: #212529 !important; border: 1px solid #333333 !important; border-radius: 6px !important; }
.stSelectbox div[data-baseweb="select"] span, .stSelectbox div[data-baseweb="select"] div, .stDateInput input { color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; }
label[data-testid="stWidgetLabel"] p { color: #ffffff !important; font-weight: 600; font-size: 14px; }
div[data-testid="stVerticalBlockBorderWrapper"] { background-color: #1a1a1a !important; border: 1px solid #333333 !important; border-radius: 10px !important; padding: 15px !important; }
div[data-testid="stAlert"] * { color: #b3d7ff !important; background-color: #0c355c !important; border-color: #0c355c !important;}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 2. INIT COOKIE MANAGER & TAAL LOGICA
# =========================================================
cookie_manager = stx.CookieManager()

saved_lang = cookie_manager.get('dahle_lang')
if 'language' not in st.session_state:
    st.session_state.language = saved_lang if saved_lang else "no"

if "lang" in st.query_params:
    gekozen_taal = st.query_params["lang"]
    if gekozen_taal in ["no", "en", "sv", "da"]:
        st.session_state.language = gekozen_taal
        cookie_manager.set("dahle_lang", gekozen_taal, key="set_lang_safe")
    st.query_params.clear()
    st.rerun()

lang = st.session_state.language 
lang_displays = { "no": "🇳🇴 Norsk", "en": "🇬🇧 English", "sv": "🇸🇪 Svenska", "da": "🇩🇰 Dansk" }
current_lang_display = lang_displays.get(lang, "🇳🇴 Norsk")

# =========================================================
# 3. WOORDENBOEK
# =========================================================
translations = {
    "no": { 
        "nav_home": "Hjem", "nav_about": "Om oss", "nav_services": "Tjenester", "nav_gallery": "Galleri", "nav_contact": "Kontakt", 
        "menu_title": "Sider ⌄", "menu_dash": "Performance Dashboard", "menu_plan": "Intern Planner",
        "nav_portal": "KUNDEPORTAL", "nav_contact_btn": "TA KONTAKT", 
        "fuel_lbl": "⛽ Diesel (per Liter)", "gas_lbl": "🚗 Bensin (per Liter)", "api_txt": "Sist oppdatert via API",
        "perf_sum": "### Oppsummering", "filter_lbl": "📅 Filtrer etter dato:",
        "opt_all": "Alle bestillinger", "opt_today": "I dag", "opt_week": "Denne uken", "opt_lweek": "Forrige uke", "opt_month": "Denne måneden", "opt_custom": "Egendefinert dato...",
        "tot_fuel": "Total Drivstoffkostnad", "tot_profit": "Total Fortjeneste", "avg_margin": "Gjennomsnittlig margin",
        "co2_foot": "CO₂ Fotavtrykk", "act_ship": "Aktive Forsendelser",
        "prof_cust": "### Lønnsomhet per Kunde", "prof_trend": "### Fortjenesteutvikling",
        "det_brk": "### Detaljert Kostnads- og Marginsoversikt",
        "info_calc": "ℹ️ Hvordan beregnes fortjeneste? Fortjeneste = Estimert inntekt - Drivstoffkostnader. Margin % viser prosentandelen av inntekten som er fortjeneste.",
        "shipments": "FORSENDELSER", "fuel_cost": "DRIVSTOFF", "net_profit": "NETTO FORTJENESTE", "margin": "MARGIN %",
        "btn_view": "🔍 Se Bestillinger", "last_order": "Siste bestilling:", "unknown": "Ukjent",
        "dialog_title": "🔍 Ordrehistorikk og Detaljer", "dialog_sub": "Her er en oversikt over alle fullførte bestillinger for denne spesifikke kunden.",
        "route": "Rute:", "profit": "Fortjeneste:", "margin_lbl": "Margin:"
    },
    "en": { 
        "nav_home": "Home", "nav_about": "About us", "nav_services": "Services", "nav_gallery": "Gallery", "nav_contact": "Contact", 
        "menu_title": "Pages ⌄", "menu_dash": "Performance Dashboard", "menu_plan": "Internal Planner",
        "nav_portal": "CUSTOMER PORTAL", "nav_contact_btn": "CONTACT US", 
        "fuel_lbl": "⛽ Diesel (per Liter)", "gas_lbl": "🚗 Petrol (per Liter)", "api_txt": "Live via API",
        "perf_sum": "### Performance Summary", "filter_lbl": "📅 Filter by date:",
        "opt_all": "All orders", "opt_today": "Today", "opt_week": "This week", "opt_lweek": "Last week", "opt_month": "This month", "opt_custom": "Custom date...",
        "tot_fuel": "Total Fuel Cost", "tot_profit": "Total Profit", "avg_margin": "Avg. Margin",
        "co2_foot": "CO₂ Footprint", "act_ship": "Active Shipments",
        "prof_cust": "### Profitability per Customer", "prof_trend": "### Profit Trend Over Time",
        "det_brk": "### Detailed Cost & Margin Breakdown",
        "info_calc": "ℹ️ How is profit calculated? Profit = Estimated Revenue - Fuel Costs. The Margin % shows the percentage of revenue that remains as profit.",
        "shipments": "SHIPMENTS", "fuel_cost": "FUEL COST", "net_profit": "NET PROFIT", "margin": "MARGIN %",
        "btn_view": "🔍 View Orders", "last_order": "Last order:", "unknown": "Unknown",
        "dialog_title": "🔍 Order History & Details", "dialog_sub": "Here is the overview of all completed orders for this specific customer.",
        "route": "Route:", "profit": "Profit:", "margin_lbl": "Margin:"
    },
    "sv": { 
        "nav_home": "Hem", "nav_about": "Om oss", "nav_services": "Tjänster", "nav_gallery": "Galleri", "nav_contact": "Kontakt", 
        "menu_title": "Sidor ⌄", "menu_dash": "Performance Dashboard", "menu_plan": "Intern Planner",
        "nav_portal": "KUNDPORTAL", "nav_contact_btn": "KONTAKTA OSS", 
        "fuel_lbl": "⛽ Diesel (per Liter)", "gas_lbl": "🚗 Bensin (per Liter)", "api_txt": "Senast uppdaterad via API",
        "perf_sum": "### Prestandasammanfattning", "filter_lbl": "📅 Filtrera efter datum:",
        "opt_all": "Alla beställningar", "opt_today": "I dag", "opt_week": "Denna vecka", "opt_lweek": "Förra veckan", "opt_month": "Denna månad", "opt_custom": "Anpassat datum...",
        "tot_fuel": "Total bränslekostnad", "tot_profit": "Total vinst", "avg_margin": "Genomsnittlig marginal",
        "co2_foot": "CO₂ Fotavtryck", "act_ship": "Aktiva Försändelser",
        "prof_cust": "### Lönsamhet per Kund", "prof_trend": "### Vinstutveckling över tid",
        "det_brk": "### Detaljerad Kostnads- och Marginalöversikt",
        "info_calc": "ℹ️ Hur beräknas vinsten? Vinst = Uppskattad intäkt - Bränslekostnader. Marginal % visar procentandelen av intäkten som är vinst.",
        "shipments": "FÖRSÄNDELSER", "fuel_cost": "BRÄNSLE", "net_profit": "NETTOVINST", "margin": "MARGINAL %",
        "btn_view": "🔍 Visa Beställningar", "last_order": "Senaste beställning:", "unknown": "Okänd",
        "dialog_title": "🔍 Orderhistorik och Detaljer", "dialog_sub": "Här är en översikt över alla slutförda beställningar för denna specifika kund.",
        "route": "Rutt:", "profit": "Vinst:", "margin_lbl": "Marginal:"
    },
    "da": { 
        "nav_home": "Hjem", "nav_about": "Om os", "nav_services": "Tjenester", "nav_gallery": "Galleri", "nav_contact": "Kontakt", 
        "menu_title": "Sider ⌄", "menu_dash": "Performance Dashboard", "menu_plan": "Intern Planner",
        "nav_portal": "KUNDEPORTAL", "nav_contact_btn": "KONTAKT OS", 
        "fuel_lbl": "⛽ Diesel (pr. Liter)", "gas_lbl": "🚗 Benzin (pr. Liter)", "api_txt": "Senest opdateret via API",
        "perf_sum": "### Resultatoversigt", "filter_lbl": "📅 Filtrer efter dato:",
        "opt_all": "Alle bestillinger", "opt_today": "I dag", "opt_week": "Denne uge", "opt_lweek": "Sidste uge", "opt_month": "Denne måned", "opt_custom": "Brugerdefineret dato...",
        "tot_fuel": "Samlede Brændstofomkostninger", "tot_profit": "Samlet Fortjeneste", "avg_margin": "Gennemsnitlig margin",
        "co2_foot": "CO₂ Fodaftryk", "act_ship": "Aktive Forsendelser",
        "prof_cust": "### Lønsomhed pr. Kunde", "prof_trend": "### Fortjenesteudvikling over tid",
        "det_brk": "### Detaljeret Omkostnings- og Marginoversigt",
        "info_calc": "ℹ️ Hvordan beregnes fortjeneste? Fortjeneste = Estimeret indtægt - Brændstofomkostninger. Margin % viser den procentdel af indtægten, der er fortjeneste.",
        "shipments": "FORSENDELSER", "fuel_cost": "BRÆNDSTOF", "net_profit": "NETTO FORTJENESTE", "margin": "MARGIN %",
        "btn_view": "🔍 Se Bestillinger", "last_order": "Seneste bestilling:", "unknown": "Ukendt",
        "dialog_title": "🔍 Ordrehistorik og Detaljer", "dialog_sub": "Her er en oversigt over alle gennemførte bestillinger for denne specifikke kunde.",
        "route": "Rute:", "profit": "Fortjeneste:", "margin_lbl": "Margin:"
    }
}
t = translations[lang]

# =========================================================
# 4. DATABASE & AUTHENTICATIE
# =========================================================
@st.cache_resource
def init_connection():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

supabase = init_connection()

if 'user' not in st.session_state:
    st.session_state.user = None

acc_token = cookie_manager.get('dahle_acc')
ref_token = cookie_manager.get('dahle_ref')

if st.session_state.get('user') is None and acc_token and ref_token:
    try:
        session = supabase.auth.set_session(acc_token, ref_token)
        st.session_state.user = session.user
    except Exception:
        pass

if st.session_state.get('user'):
    try:
        prof_res = supabase.table("profiles").select("company_name").eq("id", st.session_state.user.id).execute()
        if prof_res.data:
            st.session_state.company_name = prof_res.data[0]["company_name"]
    except: pass


# =========================================================
# 5. NAVBAR SAMENSTELLEN
# =========================================================
if st.session_state.get('user') is not None and 'company_name' in st.session_state:
    icoon = "<svg style='width:16px; height:16px; margin-right:8px; vertical-align:-2px; fill:currentColor;' viewBox='0 0 640 512'><path d='M224 256A128 128 0 1 0 224 0a128 128 0 1 0 0 256zm-45.7 48C79.8 304 0 383.8 0 482.3C0 498.7 13.3 512 29.7 512H322.8c-3.1-8.8-3.7-18.4-1.4-27.8l15-60.1c2.8-11.3 8.6-21.5 16.8-29.7l40.3-40.3c-32.4-31.6-78-50.1-126.5-50.1H178.3zm212.8-38.1l-40.3 40.3c-15.9 15.9-27.2 35.8-32.5 57.2l-15 60.1c-1.3 5.3-.2 10.9 3.1 15.3s8.5 7.1 14 7.1H592c5.5 0 10.7-2.7 14-7.1s4.4-10 3.1-15.3l-15-60.1c-5.3-21.4-16.6-41.3-32.5-57.2l-40.3-40.3c-23.4-23.4-60.6-23.4-84 0zM456 432c-13.3 0-24-10.7-24-24s10.7-24 24-24s24 10.7 24 24s-10.7 24-24 24z'/></svg>"
    knop_tekst = f"{icoon}{st.session_state.company_name}"
else:
    knop_tekst = t['nav_portal']

html_navbar = f"""
<div class="navbar">
<div class="nav-logo">
<a href="/?lang={lang}" target="_self">
<img src="https://cloud-1de12d.becdn.net/media/original/964295c9ae8e693f8bb4d6b70862c2be/logo-website-top-png-1-.webp">
</a>
</div>
<div class="nav-links">
<a href="/?lang={lang}" target="_self"><span>{t['nav_home']}</span></a>
<span>{t['nav_about']}</span>
<span>{t['nav_services']}</span>
<span>{t['nav_gallery']}</span>
<span>{t['nav_contact']}</span>
<div class="nav-text-dropdown">
<button class="nav-text-dropbtn">{t['menu_title']}</button>
<div class="nav-text-dropdown-content">
<a href="/Dashboard?lang={lang}" target="_self">📈 {t['menu_dash']}</a>
<a href="/Planner?lang={lang}" target="_self">📅 {t['menu_plan']}</a>
</div>
</div>
</div>
<div class="nav-cta">
<div class="lang-dropdown">
<button class="lang-dropbtn">{current_lang_display} ⌄</button>
<div class="lang-dropdown-content">
<a href="?lang=en" target="_self">🇬🇧 English</a>
<a href="?lang=no" target="_self">🇳🇴 Norsk</a>
<a href="?lang=sv" target="_self">🇸🇪 Svenska</a>
<a href="?lang=da" target="_self">🇩🇰 Dansk</a>
</div>
</div>
<a href="/Login?lang={lang}" target="_self" class="cta-btn-outline">{knop_tekst}</a>
<a href="/?lang={lang}" target="_self" class="cta-btn-purple">{t['nav_contact_btn']}</a>
</div>
</div>
"""
st.markdown(html_navbar, unsafe_allow_html=True)


# =========================================================
# 6. POP-UP & API FUNCTIES (Vanuit jouw code)
# =========================================================
@st.dialog(t['dialog_title'])
def show_order_history(company_name, df):
    st.markdown(f"### {company_name}")
    st.write(t['dialog_sub'])
    st.write("---")
    
    cust_orders = df[df['company'] == company_name].sort_values('parsed_date', ascending=False)
    
    for _, order in cust_orders.iterrows():
        o_date = order['parsed_date'].strftime('%Y-%m-%d') if pd.notnull(order['parsed_date']) else "N/A"
        status = order.get('status', 'Unknown')
        
        with st.container(border=True):
            st.markdown(f"**Order #{order['id']}** — {o_date} `({status})`")
            st.write(f"🛣️ **{t['route']}** {order.get('pickup_city', '-')} ➔ {order.get('delivery_city', '-')}")
            st.write(f"💰 **{t['profit']}** {order['profit']:,.0f} NOK | **{t['margin_lbl']}** {order['margin_pct']:.1f}%")


@st.cache_data(ttl=3600)
def get_live_fuel_prices():
    url = "https://api.collectapi.com/gasPrice/europeanCountries"
    headers = {
        'authorization': "apikey 40xj3EeeCTOZVeAjO2pEmj:7sLuMmcz7WUnrEdHaGiXyR",
        'content-type': "application/json"
    }
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        for country in data.get('result', []):
            if country['country'].lower() == 'norway':
                ruwe_diesel = country['diesel'].replace(',', '.')
                ruwe_gas = country['gasoline'].replace(',', '.')
                diesel_nok = round(float(ruwe_diesel) * 11.5, 2) 
                gas_nok = round(float(ruwe_gas) * 11.5, 2) 
                return {"diesel": diesel_nok, "gas": gas_nok}
    except Exception as e:
        print(f"API Error: {e}")
    return {"diesel": 20.50, "gas": 21.50} 

# ==========================================
# 7. DASHBOARD LOGICA (Jouw Code!)
# ==========================================
today = datetime.now().date()
start_of_week = today - timedelta(days=today.weekday())
start_of_last_week = start_of_week - timedelta(days=7)
start_of_month = today.replace(day=1)

live_prices = get_live_fuel_prices()
fuel_price = live_prices["diesel"]

dates = pd.date_range(end=today, periods=30)
np.random.seed(int(today.strftime('%Y%m%d'))) 

d_fluct = np.random.uniform(-0.3, 0.3, 30).cumsum()
d_history = live_prices['diesel'] + d_fluct - d_fluct[-1]
df_d = pd.DataFrame({'Date': dates, 'Price': d_history})

g_fluct = np.random.uniform(-0.4, 0.4, 30).cumsum()
g_history = live_prices['gas'] + g_fluct - g_fluct[-1]
df_g = pd.DataFrame({'Date': dates, 'Price': g_history})

def make_compact_detailed_chart(df, color):
    fig = px.line(df, x='Date', y='Price', template="plotly_dark")
    fig.update_layout(
        margin=dict(l=35, r=10, t=10, b=30), height=130, 
        xaxis=dict(visible=True, title=None, tickformat="%d %b", showgrid=False, tickfont=dict(size=10)), 
        yaxis=dict(visible=True, title=None, tickformat=".1f", showgrid=True, gridcolor="#333", tickfont=dict(size=10)),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", showlegend=False, hoverlabel=dict(font_size=13, font_family="Montserrat") 
    )
    fig.update_traces(line_color=color, line_width=3, hovertemplate="<b>%{x|%d %b %Y}</b><br>%{y:.2f} NOK<extra></extra>")
    return fig

st.write("")
f1, f2 = st.columns(2, gap="large")
with f1:
    with st.container(border=True):
        c_text, c_chart = st.columns([1, 1.5]) 
        with c_text: st.metric(t['fuel_lbl'], f"{live_prices['diesel']:.2f} NOK", t['api_txt'])
        with c_chart: st.plotly_chart(make_compact_detailed_chart(df_d, '#3498db'), use_container_width=True, config={'displayModeBar': False})
with f2:
    with st.container(border=True):
        c_text, c_chart = st.columns([1, 1.5])
        with c_text: st.metric(t['gas_lbl'], f"{live_prices['gas']:.2f} NOK", t['api_txt'])
        with c_chart: st.plotly_chart(make_compact_detailed_chart(df_g, '#e67e22'), use_container_width=True, config={'displayModeBar': False})

st.write("---")

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

c_title, c_filter = st.columns([2.5, 1])
with c_title: st.write(t['perf_sum'])
with c_filter:
    filter_optie = st.selectbox(t['filter_lbl'], [t['opt_all'], t['opt_today'], t['opt_week'], t['opt_lweek'], t['opt_month'], t['opt_custom']])
    custom_dates = []
    if filter_optie == t['opt_custom']:
        custom_dates = st.date_input("Select a date range:", value=today)

filtered_df = df.copy()

if 'parsed_date' in df.columns:
    if filter_optie == t['opt_today']: filtered_df = df[df['parsed_date'] == today]
    elif filter_optie == t['opt_week']: filtered_df = df[df['parsed_date'] >= start_of_week]
    elif filter_optie == t['opt_lweek']: filtered_df = df[(df['parsed_date'] >= start_of_last_week) & (df['parsed_date'] < start_of_week)]
    elif filter_optie == t['opt_month']: filtered_df = df[df['parsed_date'] >= start_of_month]
    elif filter_optie == t['opt_custom']:
        if isinstance(custom_dates, tuple) and len(custom_dates) == 2: filtered_df = df[(df['parsed_date'] >= custom_dates[0]) & (df['parsed_date'] <= custom_dates[1])]
        elif isinstance(custom_dates, tuple) and len(custom_dates) == 1: filtered_df = df[df['parsed_date'] == custom_dates[0]]
        else: filtered_df = df[df['parsed_date'] == custom_dates]

if filtered_df.empty:
    st.warning("📊 No orders found for this specific date range. Please adjust your filter.")
    st.stop()

k1, k2, k3, k4 = st.columns(4)
total_profit = filtered_df['profit'].sum()
avg_margin = filtered_df['margin_pct'].mean()

k1.metric(t['tot_fuel'], f"{filtered_df['fuel_cost'].sum():,.0f} NOK")
k2.metric(t['tot_profit'], f"{total_profit:,.0f} NOK", delta=f"{avg_margin:.1f}% {t['avg_margin']}")
k3.metric(t['co2_foot'], f"{filtered_df['co2_emission_kg'].sum():,.0f} kg")
k4.metric(t['act_ship'], len(filtered_df))

st.write("---")
st.write("") 
col_left, col_right = st.columns(2, gap="large")

with col_left:
    st.write(t['prof_cust'])
    df_chart = filtered_df.groupby('company')['profit'].sum().reset_index().sort_values('profit', ascending=False)
    fig_profit = px.bar(df_chart, x='company', y='profit', color_discrete_sequence=['#c48bd6'], template="plotly_dark")
    fig_profit.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", xaxis_title="Customer", yaxis_title="Net Profit (NOK)")
    st.plotly_chart(fig_profit, use_container_width=True)

with col_right:
    st.write(t['prof_trend'])
    if 'parsed_date' in filtered_df.columns:
        df_trend = filtered_df.groupby('parsed_date')['profit'].sum().reset_index()
        df_trend = df_trend.rename(columns={'parsed_date': 'date'})
        fig_line = px.line(df_trend, x='date', y='profit', markers=True, color_discrete_sequence=['#27ae60'], template="plotly_dark")
        fig_line.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", xaxis_title="Date", yaxis_title="Daily Profit (NOK)")
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("No date data available to generate a trendline.")

st.write("---")
st.write(t['det_brk'])
st.info(t['info_calc'])

customer_group = filtered_df.groupby('company').agg(
    total_orders=('id', 'count'), total_fuel=('fuel_cost', 'sum'), total_profit=('profit', 'sum'),
    avg_margin=('margin_pct', 'mean'), last_date=('parsed_date', 'max')
).reset_index().sort_values(by='last_date', ascending=False).reset_index(drop=True)

card_col1, card_col2 = st.columns(2)

for i, row in customer_group.iterrows():
    target_col = card_col1 if i % 2 == 0 else card_col2
    with target_col:
        with st.container(border=True):
            margin_color = "#27ae60" if row['avg_margin'] > 85 else "#e67e22"
            last_date_str = row['last_date'].strftime('%Y-%m-%d') if pd.notnull(row['last_date']) else t['unknown']
            
            st.markdown(f"""
            <div style="padding-bottom: 10px;">
                <div style="font-size: 18px; font-weight: 700; color: #ffffff; margin-bottom: 5px; border-bottom: 2px solid #333; padding-bottom: 8px;">
                    {row['company']} <span style="font-size: 13px; color: #888; font-weight: 400; float: right; margin-top: 4px;">{t['last_order']} {last_date_str}</span>
                </div>
                <div style="display: flex; justify-content: space-between; text-align: center; margin-top: 15px;">
                    <div style="flex: 1;"><div style="font-size: 12px; color: #b0b0b0; font-weight: 600;">{t['shipments']}</div><div style="font-size: 16px; font-weight: 700; color: #fff;">{row['total_orders']}</div></div>
                    <div style="flex: 1;"><div style="font-size: 12px; color: #b0b0b0; font-weight: 600;">{t['fuel_cost']}</div><div style="font-size: 16px; font-weight: 700; color: #fff;">{row['total_fuel']:,.0f} NOK</div></div>
                    <div style="flex: 1;"><div style="font-size: 12px; color: #b0b0b0; font-weight: 600;">{t['net_profit']}</div><div style="font-size: 16px; font-weight: 700; color: #27ae60;">{row['total_profit']:,.0f} NOK</div></div>
                    <div style="flex: 1;"><div style="font-size: 12px; color: #b0b0b0; font-weight: 600;">{t['margin']}</div><div style="font-size: 16px; font-weight: 700; color: {margin_color};">{row['avg_margin']:.1f}%</div></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(t['btn_view'], key=f"popup_{row['company']}", use_container_width=True):
                show_order_history(row['company'], filtered_df)
