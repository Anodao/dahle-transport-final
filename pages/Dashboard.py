import streamlit as st
import pandas as pd
import time
from supabase import create_client
import extra_streamlit_components as stx

# --- PAGE CONFIG ---
st.set_page_config(page_title="Dahle Transport - CO2 Dashboard", page_icon="🌱", layout="wide", initial_sidebar_state="collapsed")

# =========================================================
# 0. DEMO ZIJBALK NAVIGATIE
# =========================================================
with st.sidebar:
    st.markdown("### 🧭 Demo Navigasjon")
    try: st.page_link("Home.py", label="Home (Forside)", icon="🏠")
    except: pass
    try: st.page_link("pages/Login.py", label="Kundeportal (Login)", icon="🔐")
    except: pass
    try: st.page_link("pages/Order.py", label="Ny bestilling (Order)", icon="📦")
    except: pass
    try: st.page_link("pages/Planner.py", label="Internt System", icon="📅")
    except: pass
    try: st.page_link("pages/Dashboard.py", label="CO2 Dashboard", icon="🌱")
    except: pass

# =========================================================
# 1. DIRECTE CSS INJECTIE 
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; margin: 0; padding: 0; }
.stApp { background-color: #111111 !important; }
.block-container { padding-top: 130px !important; max-width: 1200px; }
.stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown li { color: #ffffff !important; }
div[data-testid="stMetricValue"], div[data-testid="stMetricLabel"] { color: #ffffff !important; }

/* FIX 1: DE PIEPKLEINE 70px HEADER */
header[data-testid="stHeader"] { width: 70px !important; background-color: transparent !important; box-shadow: none !important; z-index: 99999 !important; }
[data-testid="stToolbar"] { display: none !important; }
footer { display: none !important; }
div[class^="viewerBadge"] { display: none !important; }

/* NAVBAR CSS */
.navbar { position: fixed; top: 0; left: 0; width: 100%; height: 90px; background-color: #ffffff !important; z-index: 999; border-bottom: 1px solid #eaeaea; display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; padding: 0 40px; box-shadow: 0 2px 10px rgba(0,0,0,0.03); }
.nav-logo { margin-left: 60px; display: flex; justify-content: flex-start; } 
.nav-logo img { height: 48px; width: auto; transition: transform 0.2s; }
.nav-links { display: flex; gap: 28px; font-size: 15px; font-weight: 600; justify-content: center; }
.nav-links a, .nav-links span { text-decoration: none; color: #111111 !important; cursor: pointer; transition: color 0.2s;}
.nav-links span:hover { color: #894b9d !important; }
.nav-cta { display: flex; justify-content: flex-end; gap: 15px; align-items: center; }
.cta-btn { background-color: #894b9d !important; color: white !important; padding: 10px 24px; border-radius: 50px; text-decoration: none !important; font-weight: 600; font-size: 13px; white-space: nowrap; transition: 0.2s;}
.cta-btn:hover { background-color: #723e83 !important; }
.cta-btn-outline { background-color: transparent !important; color: #894b9d !important; padding: 10px 20px; border-radius: 50px; text-decoration: none !important; font-weight: 600; font-size: 13px; border: 2px solid #894b9d; white-space: nowrap; max-width: 250px; overflow: hidden; text-overflow: ellipsis;}

/* FIX 2: DROPDOWN MENU */
.lang-dropdown { position: relative; display: inline-block; margin-right: 10px; padding-bottom: 15px; margin-bottom: -15px; }
.lang-dropbtn { background-color: #f8f9fa; color: #111; font-weight: 600; font-size: 13px; border: 1px solid #eaeaea; border-radius: 20px; padding: 8px 16px; cursor: pointer; display: flex; align-items: center; gap: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.03); transition: all 0.2s ease; }
.lang-dropbtn:hover { background-color: #eaeaea; }
.lang-dropdown-content { display: none; position: absolute; background-color: #ffffff; min-width: 140px; box-shadow: 0px 8px 24px rgba(0,0,0,0.12); border-radius: 12px; border: 1px solid #eaeaea; z-index: 1000; top: 100%; right: 0; overflow: hidden; }
.lang-dropdown-content a { color: #111 !important; padding: 12px 16px; text-decoration: none; display: flex; align-items: center; gap: 10px; font-size: 14px; font-weight: 500; transition: background-color 0.2s; }
.lang-dropdown-content a:hover { background-color: #f4e9f7; color: #894b9d !important; }
.lang-dropdown:hover .lang-dropdown-content { display: block; }

/* DASHBOARD SPECIFIC STYLING */
div[data-testid="stMetric"] { background-color: #1e1e1e !important; border: 1px solid #333333 !important; border-radius: 12px !important; padding: 20px !important; box-shadow: 0 4px 10px rgba(0,0,0,0.2) !important; }
div[data-testid="stMetricValue"] { color: #894b9d !important; font-weight: 700 !important; font-size: 32px !important; }
div[data-testid="stMetricDelta"] svg { fill: #00cc96 !important; }
</style>
""", unsafe_allow_html=True)


# =========================================================
# 2. VEILIGE TAAL LOGICA (Zonder trage cookies!)
# =========================================================
if 'language' not in st.session_state:
    st.session_state.language = "no"

if "lang" in st.query_params:
    url_lang = st.query_params["lang"]
    if url_lang in ["no", "en", "sv", "da"]:
        st.session_state.language = url_lang

lang = st.session_state.language

lang_displays = { "no": "🇳🇴 Norsk", "en": "🇬🇧 English", "sv": "🇸🇪 Svenska", "da": "🇩🇰 Dansk" }
current_lang_display = lang_displays.get(lang, "🇳🇴 Norsk")


# =========================================================
# 3. HET DASHBOARD WOORDENBOEK
# =========================================================
translations = {
    "no": {
        "nav_home": "Hjem", "nav_about": "Om oss", "nav_services": "Tjenester", "nav_gallery": "Galleri", "nav_contact": "Kontakt", "nav_portal": "KUNDEPORTAL", "nav_contact_btn": "TA KONTAKT",
        "dash_title": "🌱 CO2 Dashboard", "dash_sub": "Følg med på din bedrifts miljøpåvirkning og utslippshistorikk.",
        "m_tot": "Totalt utslipp (kg CO2)", "m_sav": "Spart utslipp (kg CO2)", "m_eff": "Gjennomsnittlig ruteeffektivitet",
        "c_title": "📊 Utslippsutvikling per måned",
        "info_box": "ℹ️ **Slik beregner vi dette:** Beregningene er basert på kjørelengde, lastvekt, og våre optimaliserte ruter via OSRM-routing.",
        "months": ["Jan", "Feb", "Mar", "Apr", "Mai", "Jun"]
    },
    "en": {
        "nav_home": "Home", "nav_about": "About us", "nav_services": "Services", "nav_gallery": "Gallery", "nav_contact": "Contact", "nav_portal": "CUSTOMER PORTAL", "nav_contact_btn": "CONTACT US",
        "dash_title": "🌱 CO2 Dashboard", "dash_sub": "Track your company's environmental impact and emission history.",
        "m_tot": "Total Emissions (kg CO2)", "m_sav": "Saved Emissions (kg CO2)", "m_eff": "Average Route Efficiency",
        "c_title": "📊 Emission trend per month",
        "info_box": "ℹ️ **How we calculate this:** Calculations are based on mileage, cargo weight, and our optimized routes using OSRM routing.",
        "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    },
    "sv": {
        "nav_home": "Hem", "nav_about": "Om oss", "nav_services": "Tjänster", "nav_gallery": "Galleri", "nav_contact": "Kontakt", "nav_portal": "KUNDPORTAL", "nav_contact_btn": "KONTAKTA OSS",
        "dash_title": "🌱 CO2 Dashboard", "dash_sub": "Följ ditt företags miljöpåverkan och utsläppshistorik.",
        "m_tot": "Totala utsläpp (kg CO2)", "m_sav": "Sparade utsläpp (kg CO2)", "m_eff": "Genomsnittlig rutteffektivitet",
        "c_title": "📊 Utsläppsutveckling per månad",
        "info_box": "ℹ️ **Så här beräknar vi detta:** Beräkningarna baseras på körsträcka, lastvikt och våra optimerade rutter via OSRM-routing.",
        "months": ["Jan", "Feb", "Mar", "Apr", "Maj", "Jun"]
    },
    "da": {
        "nav_home": "Hjem", "nav_about": "Om os", "nav_services": "Tjenester", "nav_gallery": "Galleri", "nav_contact": "Kontakt", "nav_portal": "KUNDEPORTAL", "nav_contact_btn": "KONTAKT OS",
        "dash_title": "🌱 CO2 Dashboard", "dash_sub": "Følg med i din virksomheds miljøpåvirkning og udledningshistorik.",
        "m_tot": "Samlede udledninger (kg CO2)", "m_sav": "Sparede udledninger (kg CO2)", "m_eff": "Gennemsnitlig ruteeffektivitet",
        "c_title": "📊 Udledningsudvikling pr. måned",
        "info_box": "ℹ️ **Sådan beregner vi dette:** Beregningerne er baseret på kilometertal, lastvægt og vores optimerede ruter via OSRM-routing.",
        "months": ["Jan", "Feb", "Mar", "Apr", "Maj", "Jun"]
    }
}
t = translations[lang]

# =========================================================
# 4. DATABASE & AUTHENTICATIE 
# =========================================================
cookie_manager = stx.CookieManager()

def init_connection():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

if 'supabase_client' not in st.session_state:
    try: st.session_state.supabase_client = init_connection()
    except Exception as e: pass

supabase = st.session_state.supabase_client

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

# Haal bedrijfsnaam op voor Navbar
if st.session_state.get('user'):
    try:
        prof_res = supabase.table("profiles").select("company_name").eq("id", st.session_state.user.id).execute()
        if prof_res.data:
            st.session_state.company_name = prof_res.data[0]["company_name"]
    except: pass


# =========================================================
# 5. NAVBAR TEKENEN
# =========================================================
if st.session_state.get('user') is not None and 'company_name' in st.session_state:
    icoon = "<svg style='width:16px; height:16px; margin-right:8px; vertical-align:-2px; fill:currentColor;' viewBox='0 0 640 512'><path d='M224 256A128 128 0 1 0 224 0a128 128 0 1 0 0 256zm-45.7 48C79.8 304 0 383.8 0 482.3C0 498.7 13.3 512 29.7 512H322.8c-3.1-8.8-3.7-18.4-1.4-27.8l15-60.1c2.8-11.3 8.6-21.5 16.8-29.7l40.3-40.3c-32.4-31.6-78-50.1-126.5-50.1H178.3zm212.8-38.1l-40.3 40.3c-15.9 15.9-27.2 35.8-32.5 57.2l-15 60.1c-1.3 5.3-.2 10.9 3.1 15.3s8.5 7.1 14 7.1H592c5.5 0 10.7-2.7 14-7.1s4.4-10 3.1-15.3l-15-60.1c-5.3-21.4-16.6-41.3-32.5-57.2l-40.3-40.3c-23.4-23.4-60.6-23.4-84 0zM456 432c-13.3 0-24-10.7-24-24s10.7-24 24-24s24 10.7 24 24s-10.7 24-24 24z'/></svg>"
    knop_tekst = f"{icoon}{st.session_state.company_name}"
else:
    knop_tekst = t['nav_portal']

html_navbar = f"""
<div class="navbar">
<div class="nav-logo"><a href="/?lang={lang}&reset=true" target="_self"><img src="https://cloud-1de12d.becdn.net/media/original/964295c9ae8e693f8bb4d6b70862c2be/logo-website-top-png-1-.webp"></a></div>
<div class="nav-links">
<a href="/?lang={lang}&reset=true" target="_self"><span>{t['nav_home']}</span></a>
<span>{t['nav_about']}</span>
<span>{t['nav_services']}</span>
<span>{t['nav_gallery']}</span>
<span>{t['nav_contact']}</span>
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
<a href="/?lang={lang}&reset=true" target="_self" class="cta-btn">{t['nav_contact_btn']}</a>
</div>
</div>
"""
st.markdown(html_navbar, unsafe_allow_html=True)


# =========================================================
# 6. DASHBOARD INHOUD
# =========================================================

st.markdown(f"<h2 style='color: #b070c6; margin-bottom: 0px;'>{t['dash_title']}</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='color: #aaaaaa; margin-bottom: 40px;'>{t['dash_sub']}</p>", unsafe_allow_html=True)

# Dummy Data (Past zich aan op basis van taal)
m1, m2, m3 = st.columns(3)
m1.metric(t['m_tot'], "1,245.8", "-12% vs last month")
m2.metric(t['m_sav'], "312.4", "+5% vs last month")
m3.metric(t['m_eff'], "94%", "+2% optimized")

st.write("---")
st.write("")

st.markdown(f"#### {t['c_title']}")

# Maak een simpele grafiek met Pandas
emissions_data = [450, 420, 390, 400, 350, 310]
chart_df = pd.DataFrame(
    emissions_data, 
    index=t['months'], 
    columns=['CO2']
)

# Streamlit line chart met onze paarse huisstijl kleur
st.line_chart(chart_df, color="#894b9d", height=350)

st.write("")
st.info(t['info_box'])
