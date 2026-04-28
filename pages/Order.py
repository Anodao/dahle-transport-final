import streamlit as st
import time
import requests
import pandas as pd
import pydeck as pdk
from datetime import datetime
from supabase import create_client
import extra_streamlit_components as stx
import math

# --- PAGE CONFIG ---
st.set_page_config(page_title="Dahle Transport - Order", layout="wide", initial_sidebar_state="collapsed")

# =========================================================
# 1. DIRECTE CSS INJECTIE 
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
* { font-family: 'Montserrat', sans-serif; }

/* VERBERG STREAMLIT BRANDING */
[data-testid="collapsedControl"], [data-testid="stSidebar"], header[data-testid="stHeader"] { display: none !important; }
footer { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
div[class^="viewerBadge"] { display: none !important; }
.block-container { padding-top: 110px; }

/* NAVBAR CSS */
.navbar { position: fixed; top: 0; left: 0; width: 100%; height: 90px; background-color: white; z-index: 999; border-bottom: 1px solid #eaeaea; display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; padding: 0 40px; box-shadow: 0 2px 10px rgba(0,0,0,0.03); }
.nav-logo { display: flex; justify-content: flex-start; margin-left: 20px; }
.nav-logo a { display: inline-block; height: 48px; text-decoration: none; cursor: pointer; }
.nav-logo img { height: 100%; width: auto; display: block; transition: transform 0.2s ease-in-out; }
.nav-links { display: flex; gap: 28px; font-size: 15px; font-weight: 600; justify-content: center; align-items: center;}
.nav-links a, .nav-links span { text-decoration: none; color: #111111 !important; cursor: pointer; }
.nav-text-dropdown { position: relative; display: inline-block; cursor: pointer; }
.nav-text-dropbtn { background: transparent; border: none; font-size: 15px; font-weight: 600; color: #111111 !important; cursor: pointer; padding: 0; display: flex; align-items: center; gap: 4px; }
.nav-text-dropdown-content { display: none; position: absolute; top: 100%; left: 50%; transform: translateX(-50%); background-color: #ffffff; min-width: 180px; box-shadow: 0px 8px 24px rgba(0,0,0,0.12); border-radius: 12px; z-index: 1000; }
.nav-text-dropdown:hover .nav-text-dropdown-content { display: block; }
.nav-cta { display: flex; justify-content: flex-end; gap: 15px; align-items: center; }
.cta-btn-purple { background-color: #894b9d !important; color: white !important; padding: 10px 24px; border-radius: 50px; text-decoration: none !important; font-weight: 600; font-size: 13px; }
.cta-btn-outline { background-color: transparent !important; color: #894b9d !important; padding: 10px 20px; border-radius: 50px; text-decoration: none !important; font-weight: 600; font-size: 13px; border: 2px solid #894b9d; }

/* INPUT STYLING */
div[data-baseweb="input"], div[data-baseweb="select"], div[data-baseweb="textarea"] { background-color: #333; border-radius: 8px; }
div[data-baseweb="input"] input, div[data-baseweb="textarea"] textarea { color: white; }
label { color: #ccc !important; font-weight: 600; font-size: 14px !important;}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 2. INIT & TAAL COOKIES
# =========================================================
cookie_manager = stx.CookieManager()

if 'cookie_retry' not in st.session_state:
    st.session_state.cookie_retry = True
    time.sleep(0.3)
    st.rerun()

saved_lang = cookie_manager.get('dahle_lang')
if "lang" in st.query_params:
    url_lang = st.query_params["lang"]
    if url_lang in ["no", "en", "sv", "da"]:
        if url_lang != saved_lang:
            cookie_manager.set("dahle_lang", url_lang, key="set_lang_safe")
        st.session_state.language = url_lang
elif saved_lang:
    st.session_state.language = saved_lang
else:
    st.session_state.language = "no"

lang = st.session_state.language
lang_displays = {"no": "Norsk", "en": "English", "sv": "Svenska", "da": "Dansk"}
current_lang_display = lang_displays.get(lang, "Norsk")

# =========================================================
# 3. ROBUUSTE KAART & ZOEK FUNCTIES
# =========================================================
@st.cache_data(ttl=3600, show_spinner=False)
def get_coordinates(street, zip_code, city):
    if len(city) < 2: return None
    headers = {'User-Agent': 'DahleTransportMap/12.0'}
    url = "https://nominatim.openstreetmap.org/search"
    queries = [f"{street}, {city}, Norway", f"{zip_code} {city}, Norway", f"{city}, Norway", f"{street}, {city}"]
    for q in queries:
        try:
            r = requests.get(url, params={'q': q, 'format': 'json', 'limit': 1}, headers=headers, timeout=2).json()
            if r: return float(r[0]['lat']), float(r[0]['lon'])
        except: continue
    return None

@st.cache_data(ttl=3600, show_spinner=False)
def get_route_data(coord1, coord2):
    if not coord1 or not coord2: return None, None
    url = f"https://router.project-osrm.org/route/v1/driving/{coord1[1]},{coord1[0]};{coord2[1]},{coord2[0]}?overview=full&geometries=geojson"
    try:
        resp = requests.get(url, timeout=3).json()
        if resp.get("code") == "Ok":
            return resp["routes"][0]["distance"] / 1000.0, resp["routes"][0]["geometry"]["coordinates"]
    except: pass
    return None, None

def calculate_zoom(coord1, coord2):
    """Berekent het ideale zoomniveau op basis van de afstand tussen twee punten."""
    if not coord1 or not coord2: return 4.0
    lat_diff = abs(coord1[0] - coord2[0])
    lon_diff = abs(coord1[1] - coord2[1])
    max_diff = max(lat_diff, lon_diff)
    
    if max_diff < 0.02: return 13.5  # Zeer dichtbij (binnen wijk)
    if max_diff < 0.1:  return 11.0  # Stadniveau
    if max_diff < 0.5:  return 9.0   # Regionaal
    if max_diff < 2.0:  return 7.5   # Provinciaal
    if max_diff < 5.0:  return 6.0   # Landelijk
    return 4.5 # Scandinavië-breed

# =========================================================
# 4. WOORDENBOEK
# =========================================================
translations = {
    "no": {"nav_home": "Hjem", "nav_contact": "Kontakt", "menu_title": "Sider ⌄", "nav_portal": "KUNDEPORTAL", "nav_contact_btn": "TA KONTAKT", "menu_login": "Kundeportal", "menu_order": "Ny bestilling", "menu_dash": "Performance Dashboard", "menu_plan": "Intern Planner", "c_tr": "Transport", "lbl_pcs": "stk", "calc_note_pal": "Frakten er beregnet etter plass/antall.", "calc_note_we": "Frakten er beregnet etter totalvekt."},
    "en": {"nav_home": "Home", "nav_contact": "Contact", "menu_title": "Pages ⌄", "nav_portal": "CUSTOMER PORTAL", "nav_contact_btn": "CONTACT US", "menu_login": "Customer Portal", "menu_order": "New Order", "menu_dash": "Performance Dashboard", "menu_plan": "Internal Planner", "c_tr": "Freight", "lbl_pcs": "pcs", "calc_note_pal": "Freight is calculated by space/quantity.", "calc_note_we": "Freight is calculated by total weight."}
}
t = translations.get(lang, translations["en"])

# NAVBAR
dropdown_links = f'<a href="/Login?lang={lang}" target="_self">{t["menu_login"]}</a><a href="/Dashboard?lang={lang}" target="_self">{t["menu_dash"]}</a>'
html_navbar = f"""<div class="navbar"><div class="nav-logo"><a><img src="https://cloud-1de12d.becdn.net/media/original/964295c9ae8e693f8bb4d6b70862c2be/logo-website-top-png-1-.webp"></a></div><div class="nav-links"><span>{t['nav_home']}</span><div class="nav-text-dropdown"><button class="nav-text-dropbtn">{t['menu_title']}</button><div class="nav-text-dropdown-content">{dropdown_links}</div></div></div><div class="nav-cta"><div class="lang-dropdown"><button class="lang-dropbtn">{current_lang_display} ⌄</button></div><a class="cta-btn-outline">{t['nav_portal']}</a><a class="cta-btn-purple">{t['nav_contact_btn']}</a></div></div>"""
st.markdown(html_navbar, unsafe_allow_html=True)

# FORMULIER
col_main, col_calc = st.columns([6, 3], gap="large")

with col_main:
    with st.container(border=True):
        st.markdown("### Route Information")
        c1, c2 = st.columns(2)
        with c1:
            p_street = st.text_input("Pickup Street Address *", value="Ytre Ringvei 54A")
            cp1, cp2 = st.columns(2)
            p_zip = cp1.text_input("Pickup Zip Code *", value="7100")
            p_city = cp2.text_input("Pickup City *", value="Rissa")
        with c2:
            d_street = st.text_input("Delivery Street Address *", value="Prinsens gate 49")
            cd1, cd2 = st.columns(2)
            d_zip = cd1.text_input("Delivery Zip Code *", value="7011")
            d_city = cd2.text_input("Delivery City *", value="Trondheim")

    st.write("")
    
    # --- KAART LOGICA ---
    p_coords = get_coordinates(p_street, p_zip, p_city)
    d_coords = get_coordinates(d_street, d_zip, d_city)
    
    layers = []
    points = []
    if p_coords: points.append({"pos": [p_coords[1], p_coords[0]], "name": "A"})
    if d_coords: points.append({"pos": [d_coords[1], d_coords[0]], "name": "B"})
    
    # Verfijnde Paarse Markers
    if points:
        layers.append(pdk.Layer(
            "ScatterplotLayer", 
            data=points, 
            get_position="pos", 
            get_fill_color=[137, 75, 157, 255], 
            get_radius=200,             # Veel kleinere cirkels
            radius_min_pixels=5,        # Duidelijk maar niet lomp
            radius_max_pixels=12
        ))

    # De Lijn en Dynamische Zoom
    center_lat, center_lon, zoom = 64.0, 10.0, 3.5
    if p_coords and d_coords:
        dist, route_geom = get_route_data(p_coords, d_coords)
        if route_geom:
            layers.append(pdk.Layer("PathLayer", data=[{"path": route_geom}], get_path="path", get_color=[137, 75, 157, 200], width_min_pixels=4))
        else:
            layers.append(pdk.Layer("ArcLayer", data=[{"s": [p_coords[1], p_coords[0]], "t": [d_coords[1], d_coords[0]]}], get_source_position="s", get_target_position="t", get_source_color=[137, 75, 157, 180], get_target_color=[137, 75, 157, 180], get_width=5))
        
        center_lat = (p_coords[0] + d_coords[0]) / 2
        center_lon = (p_coords[1] + d_coords[1]) / 2
        zoom = calculate_zoom(p_coords, d_coords)
    elif p_coords:
        center_lat, center_lon, zoom = p_coords[0], p_coords[1], 11.0
    elif d_coords:
        center_lat, center_lon, zoom = d_coords[0], d_coords[1], 11.0

    st.pydeck_chart(pdk.Deck(
        map_style="dark", 
        initial_view_state=pdk.ViewState(latitude=center_lat, longitude=center_lon, zoom=zoom, pitch=0),
        layers=layers
    ))

with col_calc:
    st.markdown("### ESTIMATED COST")
    # Hier kun je de prijsberekening toevoegen zoals in de vorige versies
