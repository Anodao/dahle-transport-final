import streamlit as st
import time
import requests
import pandas as pd
import pydeck as pdk
from datetime import datetime
from supabase import create_client

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Dahle Transport - Order",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS STYLING GLOBAL & NAVBAR HTML ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
* { font-family: 'Montserrat', sans-serif; }
[data-testid="collapsedControl"], [data-testid="stSidebar"], header[data-testid="stHeader"] { display: none !important; }
footer { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
div[class^="viewerBadge"] { display: none !important; }
.block-container { padding-top: 110px; }
.navbar { position: fixed; top: 0; left: 0; width: 100%; height: 90px; background-color: white; z-index: 999; border-bottom: 1px solid #eaeaea; display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; padding: 0 40px; box-shadow: 0 2px 10px rgba(0,0,0,0.03); }
.nav-logo { display: flex; justify-content: flex-start; }
.nav-logo a { display: inline-block; height: 48px; text-decoration: none; cursor: pointer; }
.nav-logo img { height: 100%; width: auto; display: block; transition: transform 0.2s ease-in-out; }
.nav-logo a:hover img { transform: scale(1.05); } 
.nav-links { display: flex; gap: 28px; font-size: 15px; font-weight: 500; color: #000000; justify-content: center;}
.nav-links a { text-decoration: none; color: inherit; }
.nav-links span { cursor: pointer; transition: color 0.2s; }
.nav-links span:hover { color: #894b9d; }
.nav-cta { display: flex; justify-content: flex-end; gap: 15px; align-items: center; }
.cta-btn { background-color: #894b9d; color: white !important; padding: 10px 24px; border-radius: 50px; text-decoration: none !important; font-weight: 600; font-size: 13px; letter-spacing: 0.5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); cursor: pointer; transition: background-color 0.2s; white-space: nowrap; }
.cta-btn:hover { background-color: #723e83; }
.cta-btn-outline { background-color: transparent; color: #894b9d !important; padding: 10px 20px; border-radius: 50px; text-decoration: none !important; font-weight: 600; font-size: 13px; letter-spacing: 0.5px; border: 2px solid #894b9d; cursor: pointer; transition: all 0.2s; white-space: nowrap; }
.cta-btn-outline:hover { background-color: #894b9d; color: white !important; }
.step-wrapper { display: flex; justify-content: center; align-items: flex-start; margin-bottom: 30px; margin-top: 10px; gap: 15px; }
.step-item { display: flex; flex-direction: column; align-items: center; width: 80px; }
.step-circle { width: 40px; height: 40px; border-radius: 50%; border: 2px solid #555; display: flex; justify-content: center; align-items: center; font-weight: 700; font-size: 16px; color: #aaa; background-color: #262626; margin-bottom: 10px; z-index: 2; transition: 0.3s; }
.step-label { font-size: 13px; font-weight: 600; color: #888; text-align: center; }
.step-line { height: 2px; width: 60px; background-color: #444; margin-top: 20px; }
.step-item.active .step-circle { border-color: #ffffff; background-color: #ffffff; color: #000000; }
.step-item.active .step-label { color: #ffffff; }
.step-item.completed .step-circle { border-color: #894b9d; background-color: #894b9d; color: white; }
.step-item.completed .step-label { color: #894b9d; }
.line-completed { background-color: #894b9d; }
div.stButton > button[kind="primary"] { background: linear-gradient(135deg, #b070c6 0%, #894b9d 100%) !important; color: #ffffff !important; border: 2px solid transparent !important; border-radius: 6px !important; padding: 14px 28px !important; font-weight: 600 !important; font-size: 15px !important; box-shadow: 0 4px 14px 0 rgba(137, 75, 157, 0.4) !important; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important; width: 100% !important; white-space: nowrap !important; }
div.stButton > button[kind="primary"]:hover { background: #ffffff !important; color: #894b9d !important; border: 2px solid #894b9d !important; transform: translateY(-2px) !important; box-shadow: 0 8px 24px rgba(137, 75, 157, 0.6) !important; }
div.stButton > button[kind="secondary"] { background: transparent !important; color: #e0c2ed !important; padding: 14px 24px !important; border-radius: 6px !important; font-weight: 600 !important; font-size: 14px !important; border: 2px solid #894b9d !important; transition: all 0.3s ease !important; width: 100% !important; white-space: nowrap !important; }
div.stButton > button[kind="secondary"]:hover { background: #ffffff !important; border-color: #894b9d !important; color: #894b9d !important; transform: translateY(-2px) !important; box-shadow: 0 4px 12px rgba(137, 75, 157, 0.3) !important; }
div[data-baseweb="input"], div[data-baseweb="select"], div[data-baseweb="textarea"] { background-color: #333; border-radius: 8px; }
div[data-baseweb="input"] input, div[data-baseweb="textarea"] textarea { color: white; }
label { color: #ccc !important; font-weight: 600; font-size: 14px !important;}
div[data-baseweb="select"] div { color: white; background-color: #333;}
</style>
<div class="navbar">
    <div class="nav-logo"><a href="/?reset=true" target="_self" title="Go back to Home"><img src="https://cloud-1de12d.becdn.net/media/original/964295c9ae8e693f8bb4d6b70862c2be/logo-website-top-png-1-.webp" alt="Dahle Transport Logo"></a></div>
    <div class="nav-links"><a href="/?reset=true" target="_self"><span>Hjem</span></a><span>Om oss</span><span>Tjenester</span><span>Galleri</span><span>Kontakt</span></div>
    <div class="nav-cta"><a href="/Login" target="_self" class="cta-btn-outline">KUNDEPORTAL</a><a href="/?reset=true" target="_self" class="cta-btn">TA KONTAKT</a></div>
</div>
""", unsafe_allow_html=True)

# --- SUPABASE CONNECTIE ---
@st.cache_resource
def init_connection():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

try:
    supabase = init_connection()
except Exception as e:
    st.error("⚠️ Database connection failed.")

# --- CHECK LIVE LOGIN STATUS ---
current_session = supabase.auth.get_session()
if current_session:
    st.session_state.user = current_session.user
else:
    st.session_state.user = None

current_user_id = st.session_state.user.id if st.session_state.user else "guest"

# =========================================================================
# DE FIX: FORCEER OVERSCHRIJVING VAN HET GEHEUGEN ALS DE GEBRUIKER WISSELT
# =========================================================================
if st.session_state.get('last_seen_user_id') != current_user_id:
    # 1. Haal de gegevens op uit de database
    prof = {}
    if current_user_id != "guest":
        try:
            prof_res = supabase.table("profiles").select("*").eq("id", current_user_id).execute()
            if prof_res.data:
                prof = prof_res.data[0]
        except:
            pass

    name_parts = str(prof.get('contact_name', '')).split(' ', 1)
    f_name = name_parts[0] if name_parts else ''
    l_name = name_parts[1] if len(name_parts) > 1 else ''

    # 2. Overschrijf de Streamlit Session State KEIHARD met deze data
    st.session_state['comp_name'] = str(prof.get('company_name') or '')
    st.session_state['comp_reg'] = ''
    st.session_state['comp_addr'] = str(prof.get('address') or '')
    st.session_state['comp_pc'] = str(prof.get('zip_code') or '')
    st.session_state['comp_city'] = str(prof.get('city') or '')
    st.session_state['comp_country'] = 'Norway'
    
    st.session_state['cont_fn'] = f_name
    st.session_state['cont_ln'] = l_name
    st.session_state['cont_email'] = st.session_state.user.email if current_user_id != "guest" else ''
    st.session_state['cont_code'] = '+47'
    st.session_state['cont_phone'] = str(prof.get('phone') or '')
    st.session_state['cont_info'] = ''
    
    st.session_state['p_addr'] = str(prof.get('address') or '')
    st.session_state['p_zip'] = str(prof.get('zip_code') or '')
    st.session_state['p_city'] = str(prof.get('city') or '')
    st.session_state['d_addr'] = str(prof.get('del_address') or '')
    st.session_state['d_zip'] = str(prof.get('del_zip') or '')
    st.session_state['d_city'] = str(prof.get('del_city') or '')
    
    # 3. Zorg dat we weten dat we deze stap gehad hebben
    st.session_state['last_seen_user_id'] = current_user_id


# --- OVERIGE SESSION STATES (Niet gerelateerd aan profiel) ---
if 'orders' not in st.session_state: st.session_state.orders = []
if 'step' not in st.session_state: st.session_state.step = 1
if 'selected_types' not in st.session_state: st.session_state.selected_types = []
if 'temp_order' not in st.session_state: st.session_state.temp_order = {}
if 'show_error' not in st.session_state: st.session_state.show_error = False
if 'is_submitted' not in st.session_state: st.session_state.is_submitted = False
if 'validate_step2' not in st.session_state: st.session_state.validate_step2 = False
if 'scroll_up' not in st.session_state: st.session_state.scroll_up = False

# Basis states voor de checkboxes
default_checks = ['chk_parcels', 'chk_freight', 'chk_mail', 'pd_oversized', 'cf_pal', 'cf_full', 'cf_lc']
for k in default_checks:
    if k not in st.session_state: st.session_state[k] = False

if 'pd_weight' not in st.session_state: st.session_state['pd_weight'] = 1.0
if 'cf_weight' not in st.session_state: st.session_state['cf_weight'] = 100
if 'mdm_weight' not in st.session_state: st.session_state['mdm_weight'] = 0.5

default_keys = {
    'comp_name': '', 'comp_reg': '', 'comp_addr': '', 'comp_pc': '', 'comp_city': '', 'comp_country': 'Norway',
    'cont_fn': '', 'cont_ln': '', 'cont_email': '', 'cont_phone': '', 'cont_code': '+47', 'cont_info': '',
    'p_addr': '', 'p_zip': '', 'p_city': '', 'd_addr': '', 'd_zip': '', 'd_city': ''
}

# --- LOGO RESET TRUCJE ---
def reset_form_state():
    st.session_state.step = 1
    st.session_state.selected_types = [] 
    st.session_state.temp_order = {}
    st.session_state.show_error = False
    st.session_state.is_submitted = False
    st.session_state.validate_step2 = False
    st.session_state.scroll_up = False
    for k, v in default_keys.items():
        st.session_state[k] = v
    st.session_state['last_seen_user_id'] = None 

if "reset" in st.query_params:
    reset_form_state()
    st.query_params.clear()
    st.rerun()

# --- ROUTING API FUNCTIES ---
HQ_COORDS = (63.4305, 10.3951) # Trondheim

@st.cache_data(ttl=3600, show_spinner=False)
def get_coordinates(address_string):
    if len(address_string) < 5: return None
    url = f"https://nominatim.openstreetmap.org/search?q={address_string}&format=json&limit=1"
    headers = {'User-Agent': 'DahleTransportApp/1.0'}
    try:
        resp = requests.get(url, headers=headers).json()
        if resp: return float(resp[0]['lat']), float(resp[0]['lon'])
    except: pass
    return None

@st.cache_data(ttl=3600, show_spinner=False)
def get_route_data(coord1, coord2):
    if not coord1 or not coord2: return None, None
    url = f"http://router.project-osrm.org/route/v1/driving/{coord1[1]},{coord1[0]};{coord2[1]},{coord2[0]}?overview=full&geometries=geojson"
    try:
        resp = requests.get(url).json()
        if resp.get("code") == "Ok":
            dist = resp["routes"][0]["distance"] / 1000.0 
            geom = resp["routes"][0]["geometry"]["coordinates"]
            return dist, geom
    except: pass
    return None, None

# =========================================================
# PRIJS CALCULATIE LOGICA
# =========================================================
def get_live_price():
    total_price = 0
    breakdown = [] 
        
    base_fee = 49
    total_price += base_fee
    breakdown.append(("Base Fee", base_fee))

    weight_cost = 0
    total_weight = 0
    
    if "Parcels & Documents" in st.session_state.selected_types:
        w_p = st.session_state.get('pd_weight', 1.0)
        total_weight += w_p
        weight_cost += (w_p * 8)
        if st.session_state.get('pd_oversized', False): weight_cost += 150 
            
    if "Cargo & Freight" in st.session_state.selected_types:
        w_f = st.session_state.get('cf_weight', 100)
        total_weight += w_f
        weight_cost += (w_f * 3) 
        if st.session_state.get('cf_pal', False): weight_cost += 250
        if st.session_state.get('cf_full', False): weight_cost += 2500
        if st.session_state.get('cf_lc', False): weight_cost += 100

    if "Mail & Direct Marketing" in st.session_state.selected_types:
        w_m = st.session_state.get('mdm_weight', 0.5)
        total_weight += w_m
        weight_cost += (w_m * 15)

    if weight_cost > 0:
        total_price += weight_cost
        breakdown.append((f"Handling & Weight ({total_weight}kg)", weight_cost))

    p_addr = str(st.session_state.get('p_addr') or '').strip()
    p_city = str(st.session_state.get('p_city') or '').strip()
    d_addr = str(st.session_state.get('d_addr') or '').strip()
    d_city = str(st.session_state.get('d_city') or '').strip()

    if len(p_addr) > 3 and len(p_city) > 2 and len(d_addr) > 3 and len(d_city) > 2:
        pickup_string = f"{p_addr}, {str(st.session_state.get('p_zip') or '')} {p_city}"
        delivery_string = f"{d_addr}, {str(st.session_state.get('d_zip') or '')} {d_city}"
        
        pick_coords = get_coordinates(pickup_string)
        del_coords = get_coordinates(delivery_string)
        
        if pick_coords and del_coords:
            dist_hq_pick, _ = get_route_data(HQ_COORDS, pick_coords)
            dist_pick_del, _ = get_route_data(pick_coords, del_coords)
            
            if dist_hq_pick is not None and dist_pick_del is not None:
                total_km = dist_hq_pick + dist_pick_del
                price_per_km = 12 
                transport_cost = total_km * price_per_km
                total_price += transport_cost
                breakdown.append((f"Transport ({total_km:.0f} km)", transport_cost))
                st.session_state.is_worldwide = False
            else:
                ww_base = 2500 
                ww_per_kg = 55 
                ww_cost = ww_base + (total_weight * ww_per_kg)
                total_price += ww_cost
                breakdown.append((f"Worldwide Air Freight ({total_weight}kg)", ww_cost))
                st.session_state.is_worldwide = True
        else: breakdown.append(("Searching address...", 0))
    elif st.session_state.step > 1:
        breakdown.append(("Awaiting route details...", 0))

    return total_price, breakdown

# =========================================================
# DE WEBSITE LOGICA (DYNAMISCHE LAYOUT)
# =========================================================
s = st.session_state.step
def get_class(step_num):
    if s > step_num: return "completed"
    elif s == step_num: return "active"
    return "inactive"
    
line_1 = "line-completed" if s > 1 else ""
line_2 = "line-completed" if s > 2 else ""

tracker_html = f"""<div class="step-wrapper"><div class="step-item {get_class(1)}"><div class="step-circle">1</div><div class="step-label">Shipment</div></div><div class="step-line {line_1}"></div><div class="step-item {get_class(2)}"><div class="step-circle">2</div><div class="step-label">Details</div></div><div class="step-line {line_2}"></div><div class="step-item {get_class(3)}"><div class="step-circle">3</div><div class="step-label">Review</div></div></div>"""

st.markdown(tracker_html, unsafe_allow_html=True)
st.write("") 

if st.session_state.step == 1:
    col_spacer_L, col_main, col_spacer_R = st.columns([1, 6, 1])
    with col_main:
        st.markdown("""
        <style>
        div[data-testid="stVerticalBlockBorderWrapper"] { position: relative !important; border-radius: 12px !important; transition: all 0.3s ease !important; background-color: #1e1e1e !important; border: 2px solid #333 !important; padding: 25px !important; height: 100%; }
        div[data-testid="stVerticalBlockBorderWrapper"]:hover { border-color: #666 !important; background-color: #262626 !important; transform: translateY(-3px); }
        div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stCheckbox"] label::after { content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%; cursor: pointer; z-index: 10; }
        div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stCheckbox"] { margin-bottom: 5px; padding-top: 0px; }
        div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stCheckbox"] label span[role="checkbox"] { transform: scale(1.6); margin-right: 15px; border-color: #888; }
        div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stCheckbox"] label p { font-size: 20px !important; font-weight: 700 !important; color: white !important; }
        </style>
        """, unsafe_allow_html=True)
        
        dynamic_css = ""
        if st.session_state.get('chk_parcels'): dynamic_css += '''div[data-testid="stColumn"]:nth-child(1) div[data-testid="stVerticalBlockBorderWrapper"] { background-color: #ffffff !important; border: 2px solid #ffffff !important; transform: translateY(-5px); box-shadow: 0 10px 30px rgba(255,255,255,0.15) !important; } div[data-testid="stColumn"]:nth-child(1) div[data-testid="stVerticalBlockBorderWrapper"] * { color: #111111 !important; } div[data-testid="stColumn"]:nth-child(1) div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stCheckbox"] label span[role="checkbox"] { background-color: #894b9d !important; border-color: #894b9d !important; }'''
        if st.session_state.get('chk_freight'): dynamic_css += '''div[data-testid="stColumn"]:nth-child(2) div[data-testid="stVerticalBlockBorderWrapper"] { background-color: #ffffff !important; border: 2px solid #ffffff !important; transform: translateY(-5px); box-shadow: 0 10px 30px rgba(255,255,255,0.15) !important; } div[data-testid="stColumn"]:nth-child(2) div[data-testid="stVerticalBlockBorderWrapper"] * { color: #111111 !important; } div[data-testid="stColumn"]:nth-child(2) div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stCheckbox"] label span[role="checkbox"] { background-color: #894b9d !important; border-color: #894b9d !important; }'''
        if st.session_state.get('chk_mail'): dynamic_css += '''div[data-testid="stColumn"]:nth-child(3) div[data-testid="stVerticalBlockBorderWrapper"] { background-color: #ffffff !important; border: 2px solid #ffffff !important; transform: translateY(-5px); box-shadow: 0 10px 30px rgba(255,255,255,0.15) !important; } div[data-testid="stColumn"]:nth-child(3) div[data-testid="stVerticalBlockBorderWrapper"] * { color: #111111 !important; } div[data-testid="stColumn"]:nth-child(3) div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stCheckbox"] label span[role="checkbox"] { background-color: #894b9d !important; border-color: #894b9d !important; }'''
            
        if dynamic_css: st.markdown(f"<style>{dynamic_css}</style>", unsafe_allow_html=True)

        st.markdown("<h3 style='text-align: center; margin-bottom: 5px;'>To find your service match, select all that you ship on a regular basis.</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #888; margin-bottom: 30px;'>Select at least one option to continue</p>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        with c1:
            with st.container(border=True):
                st.checkbox("Parcels & Documents", key="chk_parcels")
                st.markdown("""<span style="display: inline-block; padding: 4px 12px; border: 1px solid #666; border-radius: 20px; font-size: 12px; color: #ccc; margin-bottom: 20px;">Typically up to 31.5kg</span><ul style="font-size: 14px; color: #bbb; line-height: 1.6; padding-left: 20px; margin-bottom: 30px; min-height: 80px;"><li>Light to medium weight shipments</li><li>B2B/B2C</li></ul><div style="text-align: center; font-size: 12px; color: #aaa; border-top: 1px solid #444; padding-top: 20px; margin-top: 30px;">Commonly shipped items:<div style="font-size: 32px; margin-top: 10px; display: flex; gap: 20px; justify-content: center;">✉️ 📦 📚</div></div>""", unsafe_allow_html=True)
        with c2:
            with st.container(border=True):
                st.checkbox("Cargo & Freight", key="chk_freight")
                st.markdown("""<span style="display: inline-block; padding: 4px 12px; border: 1px solid #666; border-radius: 20px; font-size: 12px; color: #ccc; margin-bottom: 20px;">Typically over 31.5kg+</span><ul style="font-size: 14px; color: #bbb; line-height: 1.6; padding-left: 20px; margin-bottom: 30px; min-height: 80px;"><li>Heavier shipments using pallets or containers</li><li>B2B</li></ul><div style="text-align: center; font-size: 12px; color: #aaa; border-top: 1px solid #444; padding-top: 20px; margin-top: 30px;">Commonly shipped items:<div style="font-size: 32px; margin-top: 10px; display: flex; gap: 20px; justify-content: center;">🚛 🏗️</div></div>""", unsafe_allow_html=True)
        with c3:
            with st.container(border=True):
                st.checkbox("Mail & Marketing", key="chk_mail")
                st.markdown("""<span style="display: inline-block; padding: 4px 12px; border: 1px solid #666; border-radius: 20px; font-size: 12px; color: #ccc; margin-bottom: 20px;">Typically up to 2kg</span><ul style="font-size: 14px; color: #bbb; line-height: 1.6; padding-left: 20px; margin-bottom: 30px; min-height: 80px;"><li>Lightweight goods</li><li>International business mail (letters, brochures, books)</li></ul><div style="text-align: center; font-size: 12px; color: #aaa; border-top: 1px solid #444; padding-top: 20px; margin-top: 30px;">Commonly shipped items:<div style="font-size: 32px; margin-top: 10px; display: flex; gap: 20px; justify-content: center;">📭 📄</div></div>""", unsafe_allow_html=True)

        if st.session_state.show_error:
            st.markdown("<p style='text-align: center; color: #ff4b4b; font-weight: bold; margin-top: 20px;'>❌ Please select at least one option.</p>", unsafe_allow_html=True)
        else: st.write("") 
            
        st.markdown("<p style='text-align: center; color: #888; font-size: 13px; margin-bottom: 15px;'>⏱ Typically takes less than 5 minutes.</p>", unsafe_allow_html=True)
        
        c_btn1, c_btn2, c_btn3 = st.columns([1, 2, 1])
        with c_btn2:
            if st.button("Next Step", type="primary", use_container_width=True):
                selected = []
                if st.session_state.get('chk_parcels'): selected.append("Parcels & Documents")
                if st.session_state.get('chk_freight'): selected.append("Cargo & Freight")
                if st.session_state.get('chk_mail'): selected.append("Mail & Direct Marketing")
                if len(selected) == 0:
                    st.session_state.show_error = True
                    st.rerun()
                else:
                    st.session_state.show_error = False
                    st.session_state.selected_types = selected
                    st.session_state.step = 2
                    st.rerun()

else:
    st.markdown("<div id='error-top'></div>", unsafe_allow_html=True)
    if st.session_state.get('scroll_up', False):
        st.components.v1.html("""<script>const doc = window.parent.document; const el = doc.getElementById("error-top"); if(el) { el.scrollIntoView({behavior: "smooth"}); }</script>""", height=0)
        st.session_state.scroll_up = False 
        
    st.markdown("""<style>.step2-panel div[data-testid="stCheckbox"] { justify-content: flex-start; margin-bottom: 5px; position: static; height: auto;} .step2-panel div[data-testid="stCheckbox"] label { display: flex; width: auto; height: auto;} .step2-panel div[data-testid="stCheckbox"] label span[role="checkbox"] { position: static; transform: scale(1.0); margin-right: 10px; border-width: 1px;} .step2-panel div[data-testid="stCheckbox"] label p { display: block; font-size: 14px !important; } .step2-panel button[kind="tertiary"] { color: #888 !important; padding: 0px !important; min-height: 0px !important; margin-top: 15px !important; font-size: 16px !important; } .step2-panel button[kind="tertiary"]:hover { color: #ff4b4b !important; background-color: transparent !important; } .step2-panel div[role="radiogroup"] { gap: 0.5rem; }</style>""", unsafe_allow_html=True)
    
    def req_lbl(key, base_text):
        if st.session_state.validate_step2:
            val = str(st.session_state.get(key) or "")
            if not val.strip(): return f"{base_text} 🚨 :red[(Required)]"
        return base_text

    def email_lbl():
        base = "Work Email *"
        if st.session_state.validate_step2:
            val = str(st.session_state.get('cont_email') or "")
            if not val.strip(): return f"{base} 🚨 :red[(Required)]"
            elif "@" not in val: return f"{base} 🚨 :red[(Missing '@')]"
        return base

    col_spacer_L, col_main, col_calc, col_spacer_R = st.columns([0.5, 6, 2.5, 0.5], gap="large")
    
    with col_main:
        if st.session_state.step == 2:
            st.markdown("<div class='step2-panel'>", unsafe_allow_html=True)
            if not st.session_state.selected_types:
                 st.session_state.step = 1
                 st.rerun()

            aantal_geselecteerd = len(st.session_state.selected_types)
            cols = st.columns(aantal_geselecteerd)
            
            for i, sel in enumerate(st.session_state.selected_types[:]):
                with cols[i]:
                    with st.container(border=True):
                        c_title, c_close = st.columns([8, 1])
                        with c_title: st.markdown(f"#### {sel}")
                        with c_close:
                            if st.button("✖", key=f"btn_close_{sel}", help=f"Remove {sel}", type="tertiary"):
                                st.session_state.selected_types.remove(sel)
                                if sel == "Parcels & Documents": st.session_state.chk_parcels = False
                                if sel == "Cargo & Freight": st.session_state.chk_freight = False
                                if sel == "Mail & Direct Marketing": st.session_state.chk_mail = False
                                st.session_state.validate_step2 = False
                                st.rerun() 

                        if sel == "Parcels & Documents":
                            st.number_input("Total Weight (kg)", min_value=0.5, step=0.5, key="pd_weight")
                            st.checkbox("Oversized / Irregular Shape", key="pd_oversized")
                            
                        elif sel == "Cargo & Freight":
                            cf_lbl = "**Load Type ***"
                            if st.session_state.validate_step2 and not (st.session_state.get('cf_pal') or st.session_state.get('cf_full') or st.session_state.get('cf_lc')):
                                cf_lbl += " 🚨 :red[(Select at least one)]"
                            st.markdown(cf_lbl)
                            st.checkbox("Pallet", key="cf_pal")
                            st.checkbox("Full Container/Truck Load", key="cf_full")
                            st.checkbox("Loose Cargo", key="cf_lc")
                            st.number_input("Total Est. Weight (kg)", min_value=50, step=50, key="cf_weight")
                            
                        elif sel == "Mail & Direct Marketing":
                            st.number_input("Total Weight (kg)", min_value=0.1, step=0.1, key="mdm_weight")
                            
            st.markdown("</div>", unsafe_allow_html=True)
            st.write("")
            
            with st.container(border=True):
                st.markdown("<h3 style='margin-top: 0px;'>🏢 Company & Contact Details</h3>", unsafe_allow_html=True)
                st.write("---")
                c_form_left, c_form_right = st.columns(2, gap="large")
                with c_form_left:
                    st.text_input(req_lbl("comp_name", "Company Name *"), key="comp_name", max_chars=100)
                    st.text_input("Company Registration No. (optional)", key="comp_reg", max_chars=50)
                    st.text_input(req_lbl("comp_addr", "Company Address *"), key="comp_addr", max_chars=150)
                    c_pc, c_city = st.columns(2)
                    with c_pc: st.text_input(req_lbl("comp_pc", "Postal Code *"), key="comp_pc", max_chars=20)
                    with c_city: st.text_input(req_lbl("comp_city", "City *"), key="comp_city", max_chars=100)
                    st.text_input(req_lbl("comp_country", "Country *"), key="comp_country", max_chars=100)
    
                with c_form_right:
                    c_fn, c_ln = st.columns(2)
                    with c_fn: st.text_input(req_lbl("cont_fn", "First Name *"), key="cont_fn", max_chars=50)
                    with c_ln: st.text_input(req_lbl("cont_ln", "Last Name *"), key="cont_ln", max_chars=50)
                    st.text_input(email_lbl(), placeholder="example@email.no", key="cont_email", max_chars=150)
                    phone_lbl = "Phone *"
                    
                    phone_val = str(st.session_state.get('cont_phone') or '').strip()
                    if st.session_state.validate_step2 and not phone_val:
                        phone_lbl += " 🚨 <span style='color:#ff4b4b;'>(Required)</span>"
                    st.markdown(f"<label style='font-size: 14px; font-weight: 600; color: #ccc;'>{phone_lbl}</label>", unsafe_allow_html=True)
                    c_code, c_phone = st.columns([1, 3])
                    with c_code: st.selectbox("Code", ["+47", "+46", "+45", "+31", "+44"], label_visibility="collapsed", key="cont_code")
                    with c_phone: st.text_input("Phone", placeholder="e.g. 123 456 789", label_visibility="collapsed", key="cont_phone", max_chars=20)
    
                st.write("")
                st.markdown("<h3 style='margin-top: 20px;'>📍 Route Information</h3>", unsafe_allow_html=True)
                st.write("---")
                c_route_left, c_route_right = st.columns(2, gap="large")
                with c_route_left:
                    st.markdown("**📤 Pickup Location**")
                    st.text_input(req_lbl("p_addr", "Street Address *"), key="p_addr", max_chars=150)
                    c_p_zip, c_p_city = st.columns(2)
                    with c_p_zip: st.text_input(req_lbl("p_zip", "Zip Code *"), key="p_zip", max_chars=20)
                    with c_p_city: st.text_input(req_lbl("p_city", "City *"), key="p_city", max_chars=100)
                with c_route_right:
                    st.markdown("**📥 Delivery Destination**")
                    st.text_input(req_lbl("d_addr", "Street Address *"), key="d_addr", max_chars=150)
                    c_d_zip, c_d_city = st.columns(2)
                    with c_d_zip: st.text_input(req_lbl("d_zip", "Zip Code *"), key="d_zip", max_chars=20)
                    with c_d_city: st.text_input(req_lbl("d_city", "City *"), key="d_city", max_chars=100)
                    
                st.write("")
                
                # --- LIVE MAP GENERATOR MET ECHTE ROUTE (PYDECK) ---
                p_coords = None
                d_coords = None
                
                p_addr_map = str(st.session_state.get('p_addr') or '').strip()
                p_city_map = str(st.session_state.get('p_city') or '').strip()
                d_addr_map = str(st.session_state.get('d_addr') or '').strip()
                d_city_map = str(st.session_state.get('d_city') or '').strip()
                
                if len(p_addr_map) > 3 and len(p_city_map) > 2:
                    p_coords = get_coordinates(f"{p_addr_map}, {st.session_state.get('p_zip', '')} {p_city_map}")
                        
                if len(d_addr_map) > 3 and len(d_city_map) > 2:
                    d_coords = get_coordinates(f"{d_addr_map}, {st.session_state.get('d_zip', '')} {d_city_map}")
                
                if p_coords or d_coords:
                    layers = []
                    points = []
                    
                    if p_coords: points.append({"pos": [p_coords[1], p_coords[0]], "name": "📤 Pickup"})
                    if d_coords: points.append({"pos": [d_coords[1], d_coords[0]], "name": "📥 Delivery"})
                    
                    layers.append(
                        pdk.Layer(
                            "ScatterplotLayer",
                            data=points,
                            get_position="pos",
                            get_color=[137, 75, 157, 255], 
                            get_radius=1000,
                            radius_min_pixels=6,
                            radius_max_pixels=15,
                            pickable=True
                        )
                    )
                    
                    if p_coords and d_coords:
                        _, route_geom = get_route_data(p_coords, d_coords)
                        
                        if route_geom:
                            layers.append(
                                pdk.Layer(
                                    "PathLayer",
                                    data=[{"path": route_geom}],
                                    get_path="path",
                                    get_color=[137, 75, 157, 200],
                                    width_scale=20,
                                    width_min_pixels=3,
                                    get_width=5
                                )
                            )
                            pitch = 20 
                        else:
                            layers.append(
                                pdk.Layer(
                                    "ArcLayer",
                                    data=[{"source": [p_coords[1], p_coords[0]], "target": [d_coords[1], d_coords[0]]}],
                                    get_source_position="source",
                                    get_target_position="target",
                                    get_source_color=[137, 75, 157, 200],
                                    get_target_color=[137, 75, 157, 200],
                                    get_width=3,
                                    get_tilt=15
                                )
                            )
                            pitch = 45
                            
                        center_lat = (p_coords[0] + d_coords[0]) / 2
                        center_lon = (p_coords[1] + d_coords[1]) / 2
                        zoom = 3.5 
                    else:
                        center_lat = p_coords[0] if p_coords else d_coords[0]
                        center_lon = p_coords[1] if p_coords else d_coords[1]
                        zoom = 10
                        pitch = 0

                    view_state = pdk.ViewState(latitude=center_lat, longitude=center_lon, zoom=zoom, pitch=pitch)
                    st.pydeck_chart(pdk.Deck(layers=layers, initial_view_state=view_state, tooltip={"text": "{name}"}))
                else:
                    st.markdown("<div style='height: 250px; background-color: #1a1a1c; border: 1px solid #333; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #666; font-size: 13px;'>🗺️ Map will appear when you enter an address...</div>", unsafe_allow_html=True)
                
                st.write("---")
                st.text_area("Additional Information (optional)", placeholder="Describe what you ship, approx. weight, any special requirements, etc.", max_chars=300, key="cont_info")

            st.write("")
            st.markdown("<p style='text-align: center; color: #888; font-size: 13px; margin-bottom: 30px;'>If you would like to learn more about how Dahle Transport uses your personal data, please read our privacy notice which you can find in the footer.</p>", unsafe_allow_html=True)
            
            error_container = st.empty()
            missing_fields = False
            
            req_keys = ['comp_name', 'comp_addr', 'comp_pc', 'comp_city', 'cont_fn', 'cont_ln', 'cont_email', 'cont_phone', 'comp_country', 'p_addr', 'p_zip', 'p_city', 'd_addr', 'd_zip', 'd_city']
            for rk in req_keys:
                if not str(st.session_state.get(rk) or '').strip():
                    missing_fields = True
                    break
            
            if "Cargo & Freight" in st.session_state.selected_types:
                if not (st.session_state.get('cf_pal') or st.session_state.get('cf_full') or st.session_state.get('cf_lc')): 
                    missing_fields = True
            
            email_val = str(st.session_state.get('cont_email') or '').strip()
            invalid_email = bool(email_val and "@" not in email_val)

            if st.session_state.validate_step2:
                if missing_fields: error_container.error("⚠️ Please fill in all highlighted mandatory fields (*) before continuing.")
                elif invalid_email: error_container.error("⚠️ Please enter a valid email address containing an '@' symbol.")

            c_back, c_next = st.columns([1, 4])
            if c_back.button("← Go Back", type="secondary", use_container_width=True):
                st.session_state.step = 1
                st.session_state.validate_step2 = False 
                st.rerun()
                
            if c_next.button("Continue to Review →", type="primary", use_container_width=True):
                st.session_state.validate_step2 = True 
                if missing_fields or invalid_email:
                    st.session_state.scroll_up = True
                    st.rerun()
                else:
                    st.session_state.validate_step2 = False 
                    st.session_state.scroll_up = False
                    
                    specs_list = []
                    is_ww = st.session_state.get('is_worldwide', False)
                    region_txt = "Worldwide" if is_ww else "Domestic/European"
                    
                    if "Parcels & Documents" in st.session_state.selected_types:
                        w = st.session_state.get('pd_weight', 1)
                        sz = "Oversized" if st.session_state.get('pd_oversized') else "Standard"
                        specs_list.append(f"📦 **Parcels:** {w}kg ({sz}) ➔ {region_txt}")
                    
                    if "Cargo & Freight" in st.session_state.selected_types:
                        loads = []
                        if st.session_state.get('cf_pal'): loads.append("Pallet")
                        if st.session_state.get('cf_full'): loads.append("Full Container")
                        if st.session_state.get('cf_lc'): loads.append("Loose Cargo")
                        w = st.session_state.get('cf_weight', 100)
                        specs_list.append(f"🚛 **Freight:** {', '.join(loads)} | {w}kg ➔ {region_txt}")
                    
                    if "Mail & Direct Marketing" in st.session_state.selected_types:
                        w = st.session_state.get('mdm_weight', 0.5)
                        specs_list.append(f"📭 **Mail:** {w}kg ➔ {region_txt}")
                    
                    db_info = "\n".join([s.replace("**", "") for s in specs_list])
                    if str(st.session_state.get('cont_info', '')).strip(): 
                        db_info += f"\n\nNotes: {str(st.session_state.get('cont_info')).strip()}"
                    
                    calc_price, calc_breakdown = get_live_price()
                    
                    st.session_state.temp_order = {
                        "company": st.session_state.get('comp_name', ''), 
                        "reg_no": st.session_state.get('comp_reg', ''),
                        "address": f"{st.session_state.get('comp_addr', '')}, {st.session_state.get('comp_pc', '')} {st.session_state.get('comp_city', '')}, {st.session_state.get('comp_country', '')}",
                        "contact_name": f"{st.session_state.get('cont_fn', '')} {st.session_state.get('cont_ln', '')}",
                        "email": st.session_state.get('cont_email', ''),
                        "phone": f"{st.session_state.get('cont_code', '')} {st.session_state.get('cont_phone', '')}",
                        "info_notes": str(st.session_state.get('cont_info', '')).strip(),
                        "specs_list": specs_list,              
                        "db_info": db_info,                    
                        "types": st.session_state.selected_types,
                        "pickup_address": st.session_state.get('p_addr', ''),
                        "pickup_zip": st.session_state.get('p_zip', ''),
                        "pickup_city": st.session_state.get('p_city', ''),
                        "delivery_address": st.session_state.get('d_addr', ''),
                        "delivery_zip": st.session_state.get('d_zip', ''),
                        "delivery_city": st.session_state.get('d_city', ''),
                        "price": calc_price,
                        "price_breakdown": calc_breakdown
                    }
                    st.session_state.step = 3
                    st.rerun()

        elif st.session_state.step == 3:
            o = st.session_state.temp_order
            st.markdown("<h3 style='margin-top: 0px;'>📝 Review your request</h3>", unsafe_allow_html=True)
            st.markdown("<p style='color: #888; font-size: 14px; margin-bottom: 20px;'>Please verify your details below before confirming.</p>", unsafe_allow_html=True)
            
            with st.container(border=True):
                st.markdown("#### 🏢 Company & Contact")
                st.write("---")
                col_s1, col_s2 = st.columns(2)
                with col_s1:
                    st.markdown(f"<span style='color:#888; font-size:12px;'>COMPANY NAME</span><br><b>{o['company']}</b>", unsafe_allow_html=True)
                    st.write("")
                    if o['reg_no']: st.markdown(f"<span style='color:#888; font-size:12px;'>REGISTRATION NO</span><br><b>{o['reg_no']}</b>", unsafe_allow_html=True)
                    st.write("")
                    st.markdown(f"<span style='color:#888; font-size:12px;'>ADDRESS</span><br><b>{o['address']}</b>", unsafe_allow_html=True)
                with col_s2:
                    st.markdown(f"<span style='color:#888; font-size:12px;'>CONTACT PERSON</span><br><b>{o['contact_name']}</b>", unsafe_allow_html=True)
                    st.write("")
                    st.markdown(f"<span style='color:#888; font-size:12px;'>EMAIL</span><br><b>{o['email']}</b>", unsafe_allow_html=True)
                    st.write("")
                    st.markdown(f"<span style='color:#888; font-size:12px;'>PHONE</span><br><b>{o['phone']}</b>", unsafe_allow_html=True)
            
            with st.container(border=True):
                st.markdown("#### 📍 Route Information")
                st.write("---")
                col_s3, col_s4 = st.columns(2)
                with col_s3:
                    st.markdown("<div style='color:#b070c6; font-size:14px; font-weight:bold; margin-bottom: 10px;'>📤 PICKUP LOCATION</div>", unsafe_allow_html=True)
                    st.markdown(f"<span style='color:#888; font-size:12px;'>STREET ADDRESS</span><br><b>{o.get('pickup_address', '-')}</b>", unsafe_allow_html=True)
                    st.write("")
                    st.markdown(f"<span style='color:#888; font-size:12px;'>ZIP CODE & CITY</span><br><b>{o.get('pickup_zip', '-')} {o.get('pickup_city', '-')}</b>", unsafe_allow_html=True)
                with col_s4:
                    st.markdown("<div style='color:#b070c6; font-size:14px; font-weight:bold; margin-bottom: 10px;'>📥 DELIVERY DESTINATION</div>", unsafe_allow_html=True)
                    st.markdown(f"<span style='color:#888; font-size:12px;'>STREET ADDRESS</span><br><b>{o.get('delivery_address', '-')}</b>", unsafe_allow_html=True)
                    st.write("")
                    st.markdown(f"<span style='color:#888; font-size:12px;'>ZIP CODE & CITY</span><br><b>{o.get('delivery_zip', '-')} {o.get('delivery_city', '-')}</b>", unsafe_allow_html=True)
            
            with st.container(border=True):
                st.markdown("#### 📦 Shipment Details")
                st.write("---")
                for spec in o['specs_list']: st.markdown(spec)
                if o['info_notes']:
                    st.write("")
                    st.markdown("<span style='color:#888; font-size:12px;'>ADDITIONAL NOTES</span>", unsafe_allow_html=True)
                    st.info(o['info_notes'])
            
            st.write("")
            if not st.session_state.is_submitted:
                c_b1, c_b2 = st.columns([1, 4])
                with c_b1:
                    if st.button("← Edit Details", type="secondary", use_container_width=True):
                        st.session_state.step = 2
                        st.rerun()
                with c_b2:
                    if st.button("✅ CONFIRM & SEND REQUEST", type="primary", use_container_width=True):
                        db_order = {
                            "company": o['company'], "reg_no": o['reg_no'], "address": o['address'],
                            "contact_name": o['contact_name'], "email": o['email'], "phone": o['phone'],
                            "info": o['db_info'], "types": ", ".join(o['types']), "status": "New",
                            "received_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "pickup_address": o.get('pickup_address', ''), "pickup_zip": o.get('pickup_zip', ''), "pickup_city": o.get('pickup_city', ''),
                            "delivery_address": o.get('delivery_address', ''), "delivery_zip": o.get('delivery_zip', ''), "delivery_city": o.get('delivery_city', ''),
                            "price": o.get('price', 0)
                        }
                        
                        if st.session_state.get('user'):
                            db_order["user_id"] = st.session_state.user.id

                        try:
                            supabase.table("orders").insert(db_order).execute()
                            st.balloons()
                            st.session_state.is_submitted = True
                            st.rerun()
                        except Exception as e:
                            st.error("⚠️ Failed to send order to the database. Ensure the 'price' column exists in your Supabase 'orders' table!")
            else:
                st.success("🎉 Your transport request has been sent successfully! We will get in touch shortly.")
                st.info("You can review your submitted details above.")
                if st.button("← Start a New Request", type="primary", use_container_width=True):
                    reset_form_state()
                    st.rerun()

    with col_calc:
        if st.session_state.step == 3:
            current_price = st.session_state.temp_order.get('price', 0)
            breakdown_lines = st.session_state.temp_order.get('price_breakdown', [])
        else:
            current_price, breakdown_lines = get_live_price()
        
        receipt_items_html = ""
        for name, price in breakdown_lines:
            receipt_items_html += f"""<div style="display: flex; justify-content: space-between; font-size: 13px; color: #bbb; margin-bottom: 8px;"><span>{name}</span><span>{price:,.0f}</span></div>"""
            
        receipt_html = f"""<style>.receipt-card {{ background: #1a1a1c; border: 1px solid #333; border-radius: 12px; padding: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); position: sticky; top: 120px; }}</style><div class="receipt-card"><div style="color: #ffffff; font-size: 15px; font-weight: 600; text-transform: uppercase; letter-spacing: 1.5px; border-bottom: 1px solid #333; padding-bottom: 12px; margin-bottom: 20px;">Estimated Cost</div>{receipt_items_html}<div style="border-bottom: 1px dashed #444; margin: 15px 0;"></div><div style="display: flex; justify-content: space-between; align-items: center;"><span style="font-size: 14px; font-weight: 600; color: #fff;">Total</span><span style="font-size: 26px; font-weight: 700; color: #b070c6;">{current_price:,.0f} <span style="font-size:16px;">NOK</span></span></div><div style="text-align: right; font-size: 11px; color: #666; margin-top: 2px;">Excl. MVA (VAT)</div></div>"""
        st.markdown(receipt_html, unsafe_allow_html=True)

st.write("---")
c_bottom1, c_bottom2, c_bottom3 = st.columns(3, gap="large")
with c_bottom1:
    if st.button("Open Internal Planner System", type="primary", use_container_width=True): st.switch_page("pages/Planner.py")
with c_bottom2:
    if st.button("Open CO2 Dashboard", type="primary", use_container_width=True): st.switch_page("pages/Dashboard.py")
with c_bottom3:
    if st.button("Open Customer Portal", type="primary", use_container_width=True): st.switch_page("pages/Login.py")
