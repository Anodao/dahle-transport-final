import streamlit as st
from supabase import create_client
import extra_streamlit_components as stx
import time
import requests
import pydeck as pdk

st.set_page_config(page_title="Dahle Transport - Planner", layout="wide", initial_sidebar_state="collapsed")

# =========================================================
# 1. DIRECTE CSS INJECTIE
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; margin: 0; padding: 0; }
.stApp { background-color: #111111 !important; }
.block-container { padding-top: 105px !important; max-width: 100% !important; margin-top: 0px; padding-left: 5%; padding-right: 5%; }
.stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown li { color: #ffffff !important; }
[data-testid="collapsedControl"], [data-testid="stSidebar"], header[data-testid="stHeader"], [data-testid="stToolbar"], footer, div[class^="viewerBadge"] { display: none !important; }
.navbar { position: fixed; top: 0; left: 0; width: 100%; height: 90px; background-color: #ffffff !important; z-index: 999; display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; padding: 0 40px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
.nav-logo a { display: inline-block; height: 48px; text-decoration: none; cursor: pointer; }
.nav-logo img { height: 100%; width: auto; display: block; transition: transform 0.2s ease-in-out; }
.nav-logo a:hover img { transform: scale(1.05); } 
.nav-links { display: flex; gap: 28px; font-size: 15px; font-weight: 600; justify-content: center; align-items: center;}
.nav-links a, .nav-links span { text-decoration: none; color: #111111 !important; cursor: pointer; transition: color 0.2s;}
.nav-links span:hover { color: #894b9d !important; }
.nav-text-dropdown { position: relative; display: inline-block; cursor: pointer; padding-bottom: 20px; margin-bottom: -20px; }
.nav-text-dropbtn { background: transparent; border: none; font-size: 15px; font-weight: 600; color: #111111 !important; cursor: pointer; padding: 0; font-family: inherit; transition: color 0.2s; display: flex; align-items: center; gap: 4px; }
.nav-text-dropdown:hover .nav-text-dropbtn { color: #894b9d !important; }
.nav-text-dropdown::after { content: ''; position: absolute; top: 100%; left: 0; width: 100%; height: 30px; background: transparent; display: none; }
.nav-text-dropdown:hover::after { display: block; }
.nav-text-dropdown-content { display: none; position: absolute; top: calc(100% + 10px); left: 50%; transform: translateX(-50%); background-color: #ffffff; min-width: 180px; box-shadow: 0px 8px 24px rgba(0,0,0,0.12); border-radius: 12px; border: 1px solid #eaeaea; z-index: 1000; overflow: hidden; }
.nav-text-dropdown-content a { color: #111111 !important; padding: 12px 16px; text-decoration: none; display: block; font-size: 14px; font-weight: 500; text-align: left; transition: background-color 0.2s; border-bottom: none !important; }
.nav-text-dropdown-content a:hover { background-color: #f4e9f7; color: #894b9d !important; }
.nav-text-dropdown:hover .nav-text-dropdown-content { display: block; }
.nav-cta { display: flex; justify-content: flex-end; gap: 15px; align-items: center; }
.cta-btn-purple { background-color: #894b9d !important; color: white !important; padding: 10px 24px; border-radius: 50px; text-decoration: none !important; font-weight: 600; font-size: 13px; transition: background-color 0.2s; white-space: nowrap;}
.cta-btn-purple:hover { background-color: #723e83 !important; }
.cta-btn-outline { background-color: transparent !important; color: #894b9d !important; padding: 10px 20px; border-radius: 50px; text-decoration: none !important; font-weight: 600; font-size: 13px; border: 2px solid #894b9d; max-width: 250px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;}
.cta-btn-outline:hover { background-color: #f4e9f7 !important; }
.lang-dropdown { position: relative; display: inline-block; margin-right: 10px; }
.lang-dropbtn { background-color: #f8f9fa; color: #111; font-weight: 600; font-size: 13px; border: 1px solid #eaeaea; border-radius: 20px; padding: 8px 16px; cursor: pointer; display: flex; align-items: center; gap: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.03); transition: all 0.2s ease; }
.lang-dropbtn:hover { background-color: #eaeaea; }
.lang-dropdown::after { content: ''; position: absolute; top: 100%; right: 0; width: 140px; height: 30px; background: transparent; display: none; z-index: 999; }
.lang-dropdown:hover::after { display: block; }
.lang-dropdown-content { display: none; position: absolute; background-color: #ffffff; min-width: 140px; box-shadow: 0px 8px 24px rgba(0,0,0,0.12); border-radius: 12px; border: 1px solid #eaeaea; z-index: 1000; top: calc(100% + 10px); right: 0; margin-top: 0; overflow: hidden; }
.lang-dropdown-content a { color: #111 !important; padding: 12px 16px; text-decoration: none; display: flex; align-items: center; gap: 10px; font-size: 14px; font-weight: 500; transition: background-color 0.2s; }
.lang-dropdown-content a:hover { background-color: #f4e9f7; color: #894b9d !important; }
.lang-dropdown:hover .lang-dropdown-content { display: block; }
div[data-baseweb="select"] > div, div[data-baseweb="base-input"], div[data-baseweb="textarea"] { background-color: #1e1e1e !important; border: 1px solid #333333 !important; border-radius: 6px !important; }
.stSelectbox div[data-baseweb="select"] span, .stSelectbox div[data-baseweb="select"] div, .stDateInput input, div[data-baseweb="textarea"] textarea { color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; }
label[data-testid="stWidgetLabel"] p { color: #ffffff !important; font-weight: 600; font-size: 14px; }

/* FIX: Containers groeien nu dynamisch mee zonder tekst af te snijden */
div[data-testid="stVerticalBlockBorderWrapper"] { background-color: #1a1a1a !important; border: 1px solid #333333 !important; border-radius: 10px !important; padding: 15px !important; overflow: visible !important;}
.admin-note-box { word-wrap: break-word !important; overflow-wrap: break-word !important; white-space: pre-wrap !important; }

div[data-testid="stMetric"] { background-color: #161616 !important; border: 1px solid #333 !important; padding: 15px !important; border-radius: 8px !important; }
div[data-testid="stMetricValue"] { font-size: 36px !important; font-weight: 700 !important; }

/* KNOPPEN STYLING */
div.stButton > button[kind="primary"] { background: linear-gradient(135deg, #b070c6 0%, #894b9d 100%) !important; color: #ffffff !important; border: 2px solid transparent !important; border-radius: 6px !important; padding: 10px 24px !important; font-weight: 600 !important; font-size: 14px !important; width: 100% !important; transition: all 0.3s ease !important; }
div.stButton > button[kind="primary"]:hover { background: #ffffff !important; color: #894b9d !important; border: 2px solid #894b9d !important; }
div.stButton > button[kind="secondary"] { background: transparent !important; color: #e0c2ed !important; border: 1px solid #894b9d !important; border-radius: 6px !important; padding: 10px 24px !important; font-weight: 600 !important; font-size: 14px !important; width: 100% !important; transition: all 0.3s ease !important; }
div.stButton > button[kind="secondary"]:hover { background: #894b9d !important; color: white !important; }

.finance-card { padding: 16px; border-radius: 10px; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
.finance-title { color: #fff; font-size: 18px; font-weight: 700; margin-bottom: 12px; display: flex; align-items: center; gap: 10px; }
.finance-row { display: flex; align-items: center; font-size: 15px; color: #ddd; margin-bottom: 8px; }
.finance-val { font-weight: bold; color: #fff; margin-left: 5px; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# MAP, DISTANCE LOGIC
# =========================================================
@st.cache_data(ttl=3600, show_spinner=False)
def get_coordinates(street, zip_code, city):
    if len(city) < 2: return None
    headers = {'User-Agent': 'DahleApp/2.0'}
    url = "https://nominatim.openstreetmap.org/search"
    queries = [
        f"{street}, {zip_code} {city}",
        f"{street}, {city}",
        f"{zip_code} {city}",
        f"{city}"
    ]
    for q in queries:
        try:
            r = requests.get(url, params={'q': q, 'format': 'json', 'limit': 1}, headers=headers, timeout=2).json()
            if r and len(r) > 0: return float(r[0]['lat']), float(r[0]['lon'])
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
    if not coord1 or not coord2: return 4.0
    lat_diff = abs(coord1[0] - coord2[0])
    lon_diff = abs(coord1[1] - coord2[1])
    max_diff = max(lat_diff, lon_diff)
    
    if max_diff < 0.05: return 12.0
    if max_diff < 0.2:  return 10.0
    if max_diff < 1.0:  return 7.5 
    if max_diff < 5.0:  return 5.5 
    if max_diff < 15.0: return 4.0 
    return 3.0

@st.cache_data(show_spinner=False)
def get_route_distance(city1, city2):
    if not city1 or not city2: return 0
    c1, c2 = str(city1).lower(), str(city2).lower()
    
    fosen = ['rissa', 'stadsbygd', 'bjugn', 'brekstad', 'åfjord']
    if ("trondheim" in c1 and any(f in c2 for f in fosen)) or ("trondheim" in c2 and any(f in c1 for f in fosen)): return 45
    if ("'s-gravenzande" in c1 and "heerhugowaard" in c2) or ("heerhugowaard" in c1 and "'s-gravenzande" in c2): return 102
        
    headers = {'User-Agent': 'DahleApp/2.0'}
    url = "https://nominatim.openstreetmap.org/search"
    try:
        r1 = requests.get(url, params={'q': city1, 'format': 'json', 'limit': 1}, headers=headers, timeout=2).json()
        r2 = requests.get(url, params={'q': city2, 'format': 'json', 'limit': 1}, headers=headers, timeout=2).json()
        if r1 and r2:
            lat1, lon1 = float(r1[0]['lat']), float(r1[0]['lon'])
            lat2, lon2 = float(r2[0]['lat']), float(r2[0]['lon'])
            osrm = f"https://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=false"
            resp = requests.get(osrm, timeout=2).json()
            if resp.get('code') == 'Ok':
                return int(resp['routes'][0http://googleusercontent.com/image_generation_content/0
