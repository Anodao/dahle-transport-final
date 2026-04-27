import streamlit as st
import time
import requests
import pandas as pd
import pydeck as pdk
from datetime import datetime
from supabase import create_client
import extra_streamlit_components as stx

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
# 2. INIT COOKIE MANAGER & STATE
# =========================================================
cookie_manager = stx.CookieManager()

if 'cookie_retry' not in st.session_state:
    st.session_state.cookie_retry = True
    time.sleep(0.3)
    st.rerun()

if 'language' not in st.session_state: st.session_state.language = "no"
lang = st.session_state.language 

# =========================================================
# 3. ROBUUSTE KAART LOGICA (HET BELANGRIJKSTE ONDERDEEL)
# =========================================================
@st.cache_data(ttl=3600, show_spinner=False)
def get_coordinates(street, zip_code, city):
    """Vindt GPS coördinaten. Zoekt eerst specifiek, dan breed (Global)."""
    if len(city) < 2: return None
    headers = {'User-Agent': 'DahleTransportApp/2.0'}
    url = "https://nominatim.openstreetmap.org/search"
    
    # Zoekopdracht opbouwen (Alkmaar, Heerhugowaard, etc.)
    full_q = f"{street}, {zip_code} {city}"
    
    try:
        # Poging 1: Specifiek adres
        resp = requests.get(url, params={'q': full_q, 'format': 'json', 'limit': 1}, headers=headers, timeout=3).json()
        if resp: return float(resp[0]['lat']), float(resp[0]['lon'])
        
        # Poging 2: Alleen stad/postcode (als de straat niet klopt)
        resp = requests.get(url, params={'q': f"{zip_code} {city}", 'format': 'json', 'limit': 1}, headers=headers, timeout=3).json()
        if resp: return float(resp[0]['lat']), float(resp[0]['lon'])
    except: pass
    return None

@st.cache_data(ttl=3600, show_spinner=False)
def get_route_data(coord1, coord2):
    """Haalt de blauwe routelijn op van de server (met HTTPS)."""
    if not coord1 or not coord2: return None, None
    url = f"https://router.project-osrm.org/route/v1/driving/{coord1[1]},{coord1[0]};{coord2[1]},{coord2[0]}?overview=full&geometries=geojson"
    try:
        resp = requests.get(url, timeout=3).json()
        if resp.get("code") == "Ok":
            return resp["routes"][0]["distance"] / 1000.0, resp["routes"][0]["geometry"]["coordinates"]
    except: pass
    return None, None

# ... (De rest van de vertalingen en database logica blijft gelijk aan uw werkende versie)
translations = {
    "no": {"st1": "Forsendelse", "st2": "Detaljer", "st3": "Se over", "nav_portal": "KUNDEPORTAL", "nav_contact_btn": "TA KONTAKT", "menu_title": "Sider ⌄", "menu_login": "Kundeportal", "menu_order": "Ny bestilling", "menu_dash": "Performance Dashboard", "menu_plan": "Intern Planner", "nav_home": "Hjem", "nav_about": "Om oss", "nav_services": "Tjenester", "nav_gallery": "Galleri", "nav_contact": "Kontakt"},
    "en": {"st1": "Shipment", "st2": "Details", "st3": "Review", "nav_portal": "CUSTOMER PORTAL", "nav_contact_btn": "CONTACT US", "menu_title": "Pages ⌄", "menu_login": "Customer Portal", "menu_order": "New Order", "menu_dash": "Performance Dashboard", "menu_plan": "Internal Planner", "nav_home": "Home", "nav_about": "About us", "nav_services": "Services", "nav_gallery": "Gallery", "nav_contact": "Contact"}
}
t = translations.get(lang, translations["en"])

# --- SIMPEL STEP BEHEER VOOR DEMO ---
if 'step' not in st.session_state: st.session_state.step = 2

# NAVBAR RENDERING
st.markdown(f"""<div class="navbar"><div class="nav-logo"><a><img src="https://cloud-1de12d.becdn.net/media/original/964295c9ae8e693f8bb4d6b70862c2be/logo-website-top-png-1-.webp"></a></div><div class="nav-links"><span>{t['nav_home']}</span><span>{t['nav_about']}</span><div class="nav-text-dropdown"><button class="nav-text-dropbtn">{t['menu_title']}</button></div></div><div class="nav-cta"><a class="cta-btn-outline">{t['nav_portal']}</a><a class="cta-btn-purple">{t['nav_contact_btn']}</a></div></div>""", unsafe_allow_html=True)

if st.session_state.step == 2:
    col_main, col_side = st.columns([6, 3], gap="large")
    
    with col_main:
        with st.container(border=True):
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("### Pickup Location")
                p_street = st.text_input("Street Address *", value="Terschellingstraat 1", key="ps")
                cp1, cp2 = st.columns(2)
                p_zip = cp1.text_input("Zip Code *", value="1825ND", key="pz")
                p_city = cp2.text_input("City *", value="Alkmaar", key="pc")
            with c2:
                st.markdown("### Delivery Destination")
                d_street = st.text_input("Street Address * ", value="van wassenaarstraat 17", key="ds")
                cd1, cd2 = st.columns(2)
                d_zip = cd1.text_input("Zip Code * ", value="1701EC", key="dz")
                d_city = cd2.text_input("City * ", value="Heerhugowaard", key="dc")

            st.write("---")
            
            # --- KAART RENDERING MET PAARSE LIJN ---
            p_coords = get_coordinates(p_street, p_zip, p_city)
            d_coords = get_coordinates(d_street, d_zip, d_city)
            
            layers = []
            # De Punten (Dahle Paars)
            points_data = []
            if p_coords: points_data.append({"pos": [p_coords[1], p_coords[0]], "name": "A"})
            if d_coords: points_data.append({"pos": [d_coords[1], d_coords[0]], "name": "B"})
            
            if points_data:
                layers.append(pdk.Layer("ScatterplotLayer", data=points_data, get_position="pos", get_fill_color=[137, 75, 157, 255], get_radius=500, radius_min_pixels=8))

            # De Lijn (Dahle Paars)
            if p_coords and d_coords:
                _, route_geom = get_route_data(p_coords, d_coords)
                if route_geom:
                    # De echte weg
                    layers.append(pdk.Layer("PathLayer", data=[{"path": route_geom}], get_path="path", get_color=[137, 75, 157, 255], width_min_pixels=4))
                else:
                    # Plan B: De Boog (als de weg-server hapert)
                    layers.append(pdk.Layer("ArcLayer", data=[{"s": [p_coords[1], p_coords[0]], "t": [d_coords[1], d_coords[0]]}], get_source_position="s", get_target_position="t", get_source_color=[137, 75, 157, 255], get_target_color=[137, 75, 157, 255], get_width=5))
                
                view_state = pdk.ViewState(latitude=(p_coords[0]+d_coords[0])/2, longitude=(p_coords[1]+d_coords[1])/2, zoom=10, pitch=0)
            else:
                view_state = pdk.ViewState(latitude=52.63, longitude=4.75, zoom=10)

            st.pydeck_chart(pdk.Deck(map_style="dark", initial_view_state=view_state, layers=layers))

    with col_side:
        st.markdown("### ESTIMATED COST")
        with st.container(border=True):
            st.write("Route line is now prioritized and global search is enabled.")
