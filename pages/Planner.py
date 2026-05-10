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
                return int(resp['routes'][0]['distance'] / 1000.0)
    except: pass
    return 0

# =========================================================
# 2. INIT COOKIE MANAGER & AUTH VERIFICATIE
# =========================================================
cookie_manager = stx.CookieManager()
acc_token = cookie_manager.get('dahle_acc')
ref_token = cookie_manager.get('dahle_ref')

@st.cache_resource
def init_connection():
    return create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])

supabase = init_connection()

if 'role' not in st.session_state: st.session_state.role = "guest"
if 'user' not in st.session_state: st.session_state.user = None
if 'company_name' not in st.session_state: st.session_state.company_name = ""
if 'selected_order_id' not in st.session_state: st.session_state.selected_order_id = None

if st.session_state.get('user') is None and acc_token and ref_token:
    try: st.session_state.user = supabase.auth.set_session(acc_token, ref_token).user
    except: pass

if st.session_state.get('user'):
    if st.session_state.role in ['guest', 'customer'] or not st.session_state.company_name:
        try:
            prof_res = supabase.table("profiles").select("company_name, roles").eq("id", st.session_state.user.id).execute()
            if prof_res.data:
                st.session_state.company_name = prof_res.data[0].get("company_name", "")
                st.session_state.role = str(prof_res.data[0].get("roles", "customer")).strip().lower()
        except: pass

is_employee = st.session_state.get('role') in ['admin', 'employee']

if not is_employee:
    if 'auth_denied_wait' not in st.session_state:
        st.session_state.auth_denied_wait = 0
    if st.session_state.auth_denied_wait < 3: 
        st.session_state.auth_denied_wait += 1
        st.markdown("<div style='text-align: center; margin-top: 150px; color: #888;'><h3>Verifying permissions...</h3></div>", unsafe_allow_html=True)
        time.sleep(0.6) 
        st.rerun()

    html_navbar_empty = f"""<div class="navbar"><div class="nav-logo"><a href="/?lang=no"><img src="https://cloud-1de12d.becdn.net/media/original/964295c9ae8e693f8bb4d6b70862c2be/logo-website-top-png-1-.webp"></a></div></div>"""
    st.markdown(html_navbar_empty, unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: center; margin-top: 120px;'><h1 style='color:#ff4b4b;'>Access Denied</h1><p style='color:#aaa; font-size: 18px;'>You do not have permission to view the internal dashboard.</p></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,1,1])
    with c2: 
        st.markdown(f'<a href="/" target="_self" style="display: block; text-align: center; background-color: transparent; color: #894b9d; padding: 10px 20px; border-radius: 50px; text-decoration: none; font-weight: 600; border: 2px solid #894b9d;">← Back to Home</a>', unsafe_allow_html=True)
    st.stop()

# =========================================================
# POP-UP DIALOG VOOR HET BEWERKEN VAN DE VOLLEDIGE ORDER
# =========================================================
@st.dialog("Edit Order")
def edit_order_modal(order):
    order_id = order['id']
    confirm_key = f"confirm_edit_{order_id}"
    error_key = f"error_edit_{order_id}"
    
    if confirm_key not in st.session_state:
        st.session_state[confirm_key] = False
    if error_key not in st.session_state:
        st.session_state[error_key] = ""

    # CALLBACK FUNCTIES
    def trigger_confirm():
        reason = st.session_state.get(f"e_reason_{order_id}", "")
        if not reason.strip():
            st.session_state[error_key] = "Please provide a reason for this change before saving."
        else:
            st.session_state[error_key] = ""
            st.session_state[confirm_key] = True

    def cancel_confirm():
        st.session_state[confirm_key] = False
        st.session_state[error_key] = ""

    st.write(f"Change details for **Order #{order_id}**.")
    
    # --- Status & Tracking ---
    st.markdown("#### Status & Tracking")
    c_stat1, c_stat2 = st.columns(2)
    status_options = ["New", "In Progress", "Processed", "Delivered", "Cancelled"]
    curr_status = order.get('status', 'New')
    idx = status_options.index(curr_status) if curr_status in status_options else 0
    
    with c_stat1:
        st.selectbox("Status", status_options, index=idx, key=f"e_status_{order_id}")
    with c_stat2:
        st.text_input("Tracking Code", value=order.get('tracking_code', '') or "", key=f"e_track_{order_id}")

    st.write("---")
    
    # --- Adressen ---
    st.markdown("#### From (Pickup)")
    st.text_input("Street", value=order.get('pickup_address', ''), key=f"e_p_addr_{order_id}")
    c1, c2 = st.columns(2)
    with c1: st.text_input("Zip Code", value=order.get('pickup_zip', ''), key=f"e_p_zip_{order_id}")
    with c2: st.text_input("City", value=order.get('pickup_city', ''), key=f"e_p_city_{order_id}")

    st.markdown("#### To (Delivery)")
    st.text_input("Street", value=order.get('delivery_address', ''), key=f"e_d_addr_{order_id}")
    c3, c4 = st.columns(2)
    with c3: st.text_input("Zip Code", value=order.get('delivery_zip', ''), key=f"e_d_zip_{order_id}")
    with c4: st.text_input("City", value=order.get('delivery_city', ''), key=f"e_d_city_{order_id}")

    st.write("---")
    
    # --- Freight Details ---
    st.markdown("#### Freight Details")
    st.text_input("Types (e.g. Cargo & Freight: 1x Pallet)", value=order.get('types', ''), key=f"e_types_{order_id}")
    st.text_area("Additional Info / Notes", value=order.get('info', ''), height=80, key=f"e_info_{order_id}")

    st.write("---")
    
    # --- Admin Note ---
    st.markdown("#### Reason for Change")
    st.text_area("Admin Note (Required) *", value=order.get('edit_reason', ''), placeholder="E.g. Customer called to change delivery street...", height=80, key=f"e_reason_{order_id}")
    st.checkbox("Show this note to the customer on their portal", value=order.get('show_note_to_customer', False), key=f"e_show_{order_id}")

    st.write("")

    if st.session_state[error_key]:
        st.error(st.session_state[error_key])

    if not st.session_state[confirm_key]:
        st.button("Save Changes", type="primary", use_container_width=True, on_click=trigger_confirm, key=f"btn_save_{order_id}")
    else:
        st.warning("⚠️ Are you sure you want to save these changes and notify the customer?")
        col_y, col_n = st.columns(2)
        
        if col_y.button("✅ Yes, Confirm", type="primary", use_container_width=True, key=f"btn_yes_{order_id}"):
            updates = {
                "status": st.session_state[f"e_status_{order_id}"],
                "tracking_code": st.session_state[f"e_track_{order_id}"].strip(),
                "pickup_address": st.session_state[f"e_p_addr_{order_id}"], 
                "pickup_zip": st.session_state[f"e_p_zip_{order_id}"], 
                "pickup_city": st.session_state[f"e_p_city_{order_id}"],
                "delivery_address": st.session_state[f"e_d_addr_{order_id}"], 
                "delivery_zip": st.session_state[f"e_d_zip_{order_id}"], 
                "delivery_city": st.session_state[f"e_d_city_{order_id}"],
                "types": st.session_state[f"e_types_{order_id}"],
                "info": st.session_state[f"e_info_{order_id}"],
                "edit_reason": st.session_state[f"e_reason_{order_id}"].strip(),
                "show_note_to_customer": st.session_state[f"e_show_{order_id}"],
                "has_unread_update": True
            }
            try:
                supabase.table("orders").update(updates).eq("id", order_id).execute()
                st.session_state[confirm_key] = False
                st.session_state[error_key] = ""
                st.rerun() 
            except Exception as e:
                st.error(f"Failed to update database: {e}")
                
        if col_n.button("❌ Cancel", type="secondary", use_container_width=True, on_click=cancel_confirm, key=f"btn_no_{order_id}"):
            pass


# =========================================================
# 3. TAAL LOGICA & NAVBAR
# =========================================================
saved_lang = cookie_manager.get('dahle_lang')

if "lang" in st.query_params:
    url_lang = st.query_params["lang"]
    if url_lang in ["no", "en", "sv", "da"]:
        if url_lang != saved_lang: cookie_manager.set("dahle_lang", url_lang, key="set_lang_safe")
        st.session_state.language = url_lang
elif saved_lang and saved_lang in ["no", "en", "sv", "da"]:
    st.session_state.language = saved_lang
elif 'language' not in st.session_state:
    st.session_state.language = "no"

lang = st.session_state.language 
lang_displays = { "no": "Norsk", "en": "English", "sv": "Svenska", "da": "Dansk" }
current_lang_display = lang_displays.get(lang, "Norsk")

translations = {
    "no": { "nav_home": "Hjem", "nav_about": "Om oss", "nav_services": "Tjenester", "nav_gallery": "Galleri", "nav_contact": "Kontakt", "menu_title": "Sider ⌄", "menu_dash": "Performance Dashboard", "menu_login": "Kundeportal", "menu_order": "Ny bestilling", "nav_portal": "KUNDEPORTAL", "nav_contact_btn": "TA KONTAKT", "stat_title": "📊 Statistikk og KPI-er", "filter_lbl": "Filterperiode:", "opt_30": "Siste 30 dager", "opt_7": "Siste 7 dager", "opt_1": "I dag", "act_req": "Handling kreves", "act_routes": "Aktive ruter", "comp": "Fullført", "canc": "Avbrutt", "tot_ord": "Totale ordrer", "inbox": "Innboks", "pend": "Venter", "prog": "Pågår", "done": "Ferdig", "det_title": "Ordredetaljer", "det_sub": "👈 Velg en ordre fra innboksen for å se detaljer og oppdatere status.", "btn_view": "Vis Ordre", "status_lbl": "Oppdater Status", "btn_save": "Lagre Status", "msg_succ": "Status oppdatert!" },
    "en": { "nav_home": "Home", "nav_about": "About us", "nav_services": "Services", "nav_gallery": "Gallery", "nav_contact": "Contact", "menu_title": "Pages ⌄", "menu_dash": "Performance Dashboard", "menu_login": "Customer Portal", "menu_order": "New Order", "nav_portal": "CUSTOMER PORTAL", "nav_contact_btn": "CONTACT US", "stat_title": "📊 Statistics & KPIs", "filter_lbl": "Filter period:", "opt_30": "Last 30 days", "opt_7": "Last 7 days", "opt_1": "Today", "act_req": "Action Required", "act_routes": "Active Routes", "comp": "Completed", "canc": "Cancelled", "tot_ord": "Total Orders", "inbox": "Inbox", "pend": "Pending", "prog": "In Progress", "done": "Done", "det_title": "Order Details", "det_sub": "👈 Select an order from the Inbox to view details and update status.", "btn_view": "View Order", "status_lbl": "Update Status", "btn_save": "Save Status", "msg_succ": "Status updated successfully!" }
}
t = translations.get(lang, translations["en"])

knop_tekst = f"<svg style='width:16px; height:16px; margin-right:8px; vertical-align:-2px; fill:currentColor;' viewBox='0 0 640 512'><path d='M224 256A128 128 0 1 0 224 0a128 128 0 1 0 0 256zm-45.7 48C79.8 304 0 383.8 0 482.3C0 498.7 13.3 512 29.7 512H322.8c-3.1-8.8-3.7-18.4-1.4-27.8l15-60.1c2.8-11.3 8.6-21.5 16.8-29.7l40.3-40.3c-32.4-31.6-78-50.1-126.5-50.1H178.3zm212.8-38.1l-40.3 40.3c-15.9 15.9-27.2 35.8-32.5 57.2l-15 60.1c-1.3 5.3-.2 10.9 3.1 15.3s8.5 7.1 14 7.1H592c5.5 0 10.7-2.7 14-7.1s4.4-10 3.1-15.3l-15-60.1c-5.3-21.4-16.6-41.3-32.5-57.2l-40.3-40.3c-23.4-23.4-60.6-23.4-84 0zM456 432c-13.3 0-24-10.7-24-24s10.7-24 24-24s24 10.7 24 24s-10.7 24-24 24z'/></svg>{st.session_state.company_name}"

dropdown_links = f'<a href="/Login?lang={lang}" target="_self">{t["menu_login"]}</a><a href="/Order?lang={lang}" target="_self">{t["menu_order"]}</a><a href="/Dashboard?lang={lang}" target="_self">{t["menu_dash"]}</a>'

st.markdown(f"""
<div class="navbar"><div class="nav-logo"><a href="/?lang={lang}" target="_self"><img src="https://cloud-1de12d.becdn.net/media/original/964295c9ae8e693f8bb4d6b70862c2be/logo-website-top-png-1-.webp"></a></div>
<div class="nav-links"><a href="/?lang={lang}" target="_self"><span>{t['nav_home']}</span></a><span>{t['nav_about']}</span><span>{t['nav_services']}</span><span>{t['nav_gallery']}</span><span>{t['nav_contact']}</span>
<div class="nav-text-dropdown"><button class="nav-text-dropbtn">{t['menu_title']}</button><div class="nav-text-dropdown-content">{dropdown_links}</div></div></div>
<div class="nav-cta"><div class="lang-dropdown"><button class="lang-dropbtn">{current_lang_display} ⌄</button><div class="lang-dropdown-content"><a href="?lang=en" target="_self">English</a><a href="?lang=no" target="_self">Norsk</a><a href="?lang=sv" target="_self">Svenska</a><a href="?lang=da" target="_self">Dansk</a></div></div>
<a href="/Login?lang={lang}" target="_self" class="cta-btn-outline">{knop_tekst}</a><a href="/?lang={lang}" target="_self" class="cta-btn-purple">{t['nav_contact_btn']}</a></div></div>
""", unsafe_allow_html=True)


# =========================================================================
# HOOFDTITEL VAN DE PAGINA
# =========================================================================
st.markdown("<h1 style='text-align: center; color: #b070c6; padding-bottom: 20px;'>Planner dashboard</h1>", unsafe_allow_html=True)

# =========================================================================
# DATA OPHALEN UIT SUPABASE
# =========================================================================
try:
    res = supabase.table("orders").select("*").order("id", desc=True).execute()
    all_orders = res.data
except Exception as e:
    st.error(f"Error fetching orders from database: {e}")
    all_orders = []

total_count = len(all_orders)
req_count = sum(1 for o in all_orders if str(o.get('status')) == 'New')
act_count = sum(1 for o in all_orders if str(o.get('status')) == 'In Progress')
comp_count = sum(1 for o in all_orders if str(o.get('status')) in ['Processed', 'Delivered'])
canc_count = sum(1 for o in all_orders if str(o.get('status')) == 'Cancelled')

# --- STATISTIEKEN EXPANDER ---
with st.expander(t['stat_title'], expanded=True):
    st.selectbox(t['filter_lbl'], [t['opt_30'], t['opt_7'], t['opt_1']], key="plan_filter")
    
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1: st.metric(f"🔴 {t['act_req']}", req_count)
    with m2: st.metric(f"🟡 {t['act_routes']}", act_count)
    with m3: st.metric(f"🟢 {t['comp']}", comp_count)
    with m4: st.metric(f"⚫ {t['canc']}", canc_count)
    with m5: st.metric(f"📋 {t['tot_ord']}", total_count)

st.write("")
st.write("")

# --- INBOX & DETAILS SECTIE ---
col_inbox, col_details = st.columns([1, 2], gap="large")

with col_inbox:
    st.markdown(f"<h2 style='margin-top:0;'>{t['inbox']}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 13px; color: #888;'>🔴 {t['pend']} &nbsp;&nbsp; 🟡 {t['prog']} &nbsp;&nbsp; 🟢 {t['done']} &nbsp;&nbsp; ⚫ {t['canc']}</p>", unsafe_allow_html=True)
    
    if len(all_orders) == 0:
        st.info("No orders found in the database.")
    else:
        for o in all_orders:
            stat = str(o.get('status', 'Unknown'))
            icon = "🔴" if stat == "New" else "🟡" if stat == "In Progress" else "🟢" if stat in ["Processed", "Delivered"] else "⚫"
            date_str = o.get('received_date', '')[:10]
            
            with st.container(border=True):
                st.markdown(f"{icon} **{o.get('company', 'Unknown')}**")
                st.caption(f"Order #{o['id']} | Received: {date_str}")
                
                if st.button(f"{t['btn_view']} #{o['id']}", key=f"view_{o['id']}", type="secondary", use_container_width=True):
                    st.session_state.selected_order_id = o['id']
                    st.rerun()

with col_details:
    st.markdown(f"<h2 style='margin-top:0;'>{t['det_title']}</h2>", unsafe_allow_html=True)
    st.write("---")
    
    if st.session_state.selected_order_id is None:
        st.info(t['det_sub'])
    else:
        selected_order = next((o for o in all_orders if o['id'] == st.session_state.selected_order_id), None)
        
        if selected_order:
            # --- ADRES VARIABELEN ---
            p_addr = selected_order.get('pickup_address', '-').strip()
            p_zip = selected_order.get('pickup_zip', '-').strip()
            p_city_display = selected_order.get('pickup_city', '-').strip()
            p_country = "Norway"
            
            d_addr = selected_order.get('delivery_address', '-').strip()
            d_zip = selected_order.get('delivery_zip', '-').strip()
            d_city_display = selected_order.get('delivery_city', '-').strip()
            d_country = "Norway"
            
            # --- FINANCIËLE BLOCK MET KLEUR LOGICA ---
            p_city = selected_order.get('pickup_city', 'Unknown')
            d_city = selected_order.get('delivery_city', 'Unknown')
            dist_km = get_route_distance(p_city, d_city)
            
            price = selected_order.get('price') or 0
            profit = selected_order.get('profit') or 0
            cost = price - profit
            
            margin = round((profit / price * 100), 1) if price > 0 else 0.0
            fuel_cost = int(dist_km * 6.5) if dist_km > 0 else int(cost * 0.4) 
            
            order_status = selected_order.get('status', 'New')
            if order_status == 'New':
                bg_color = "#15202b"; border_color = "#2196F3"; status_color = "#2196F3"
            elif order_status == 'In Progress':
                bg_color = "#2b2415"; border_color = "#FFC107"; status_color = "#FFC107"
            elif order_status in ['Processed', 'Delivered']:
                bg_color = "#152b1a"; border_color = "#4CAF50"; status_color = "#4CAF50"
            elif order_status == 'Cancelled':
                bg_color = "#2b1515"; border_color = "#F44336"; status_color = "#F44336"
            else:
                bg_color = "#1a1a2e"; border_color = "#b070c6"; status_color = "#b070c6"
            
            date_str = selected_order.get('received_date', '')[:10]
            
            st.markdown(f"""
            <div class="finance-card" style="background-color: {bg_color}; border-left: 4px solid {border_color};">
                <div class="finance-title">
                    Order #{selected_order['id']} — {date_str} <span style="color: {status_color}; font-size: 14px;">({order_status})</span>
                </div>
                <div class="finance-row">
                    🛣️ Route: <span class="finance-val" style="font-weight: 500;">{p_city} ➔ {d_city} &nbsp;|&nbsp; 📍 {dist_km} km</span>
                </div>
                <div class="finance-row" style="margin-top: 15px;">
                    ⛽ FUEL COST: <span class="finance-val">{fuel_cost:,.0f} NOK</span> &nbsp;&nbsp;|&nbsp;&nbsp; 
                    💰 Profit: <span class="finance-val">{profit:,.0f} NOK</span> &nbsp;&nbsp;|&nbsp;&nbsp; 
                    Margin: <span class="finance-val">{margin}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            c_info1, c_info2 = st.columns(2, gap="medium")
            
            with c_info1:
                with st.container(border=True):
                    st.markdown(f"<h4 style='margin-top:0px;'>🏢 {selected_order.get('company', '-')}</h4>", unsafe_allow_html=True)
                    reg_no = selected_order.get('reg_no') or '-'
                    st.write(f"**Registration No.:** {reg_no}")
                    st.write(f"**Contact:** {selected_order.get('contact_name', '-')}")
                    st.write(f"**Phone:** {selected_order.get('phone', '-')}")
                    st.write(f"**Email:** {selected_order.get('email', '-')}")
                
                with st.container(border=True):
                    st.markdown("<h4 style='margin-top:0px;'>🛣️ Adressen</h4>", unsafe_allow_html=True)

                    c_addr_left, c_addr_right = st.columns(2)
                    with c_addr_left:
                        st.markdown(f"<div style='color:#b070c6; font-size:14px; font-weight:bold; margin-bottom: 5px;'>FROM</div>", unsafe_allow_html=True)
                        st.markdown(f"<span style='color:#888; font-size:12px;'>Street:</span><br><b>{p_addr}</b>", unsafe_allow_html=True)
                        st.write("")
                        st.markdown(f"<span style='color:#888; font-size:12px;'>Zip Code & City:</span><br><b>{p_zip} {p_city_display}</b>", unsafe_allow_html=True)
                        st.write("")
                        st.markdown(f"<span style='color:#888; font-size:12px;'>Country:</span><br><b>{p_country}</b>", unsafe_allow_html=True)

                    with c_addr_right:
                        st.markdown(f"<div style='color:#b070c6; font-size:14px; font-weight:bold; margin-bottom: 5px;'>TO</div>", unsafe_allow_html=True)
                        st.markdown(f"<span style='color:#888; font-size:12px;'>Street:</span><br><b>{d_addr}</b>", unsafe_allow_html=True)
                        st.write("")
                        st.markdown(f"<span style='color:#888; font-size:12px;'>Zip Code & City:</span><br><b>{d_zip} {d_city_display}</b>", unsafe_allow_html=True)
                        st.write("")
                        st.markdown(f"<span style='color:#888; font-size:12px;'>Country:</span><br><b>{d_country}</b>", unsafe_allow_html=True)

                st.write("")
                if st.button("Edit Order", key=f"edit_addr_{selected_order['id']}", type="primary", use_container_width=True):
                    edit_order_modal(selected_order)

            with c_info2:
                with st.container(border=True):
                    st.markdown("<h4 style='margin-top:0px;'>📦 Freight Details</h4>", unsafe_allow_html=True)
                    types_str = selected_order.get('types', '')
                    if types_str:
                        st.write(f"**Types:** {types_str}")
                    info_notes = selected_order.get('info', '')
                    if info_notes:
                        st.markdown(f"<div style='background-color:#262626; padding:10px; border-radius:6px; font-size:13px; color:#ddd;'>{info_notes}</div>", unsafe_allow_html=True)
                    
                    admin_notes = selected_order.get('edit_reason', '')
                    if admin_notes:
                        customer_visible = selected_order.get('show_note_to_customer', False)
                        visibility_icon = "👁️ Visible to Customer" if customer_visible else "🔒 Internal Only"
                        
                        st.markdown(f"""
                        <div style='background-color: #2b1515; border-left: 4px solid #ff4b4b; padding: 14px 18px; border-radius: 6px; margin-top: 15px;'>
                            <div style='display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255, 75, 75, 0.2); padding-bottom: 8px; margin-bottom: 10px;'>
                                <span style='color: #ffcccc; font-size: 13px; font-weight: bold;'>⚠️ Admin Note</span>
                                <span style='font-size: 11px; color: #ffcccc; opacity: 0.8;'>{visibility_icon}</span>
                            </div>
                            <div style='color: #ffcccc; font-size: 14px; line-height: 1.5; white-space: pre-wrap; word-wrap: break-word;'>{admin_notes}</div>
                        </div>
                        """, unsafe_allow_html=True)

                with st.container(border=True):
                    st.markdown("<h4 style='margin-top:0px;'>🗺️ Route Map</h4>", unsafe_allow_html=True)
                    
                    p_coords = get_coordinates(p_addr, p_zip, p_city_display)
                    d_coords = get_coordinates(d_addr, d_zip, d_city_display)
                    
                    layers = []
                    if p_coords and d_coords:
                        _, route_geom = get_route_data(p_coords, d_coords) 
                        if route_geom:
                            layers.append(pdk.Layer(
                                "PathLayer", 
                                data=[{"path": route_geom}], 
                                get_path="path", 
                                get_color=[137, 75, 157, 255], 
                                width_scale=20, 
                                width_min_pixels=4, 
                                get_width=5
                            ))
                        else:
                            route_geom = [[p_coords[1], p_coords[0]], [d_coords[1], d_coords[0]]]
                            layers.append(pdk.Layer(
                                "PathLayer", 
                                data=[{"path": route_geom}], 
                                get_path="path", 
                                get_color=[137, 75, 157, 255], 
                                width_scale=20, 
                                width_min_pixels=4, 
                                get_width=5
                            ))
                        center_lat = (p_coords[0] + d_coords[0]) / 2
                        center_lon = (p_coords[1] + d_coords[1]) / 2
                        zoom = calculate_zoom(p_coords, d_coords)
                        pitch = 20
                    elif p_coords:
                        center_lat, center_lon, zoom, pitch = p_coords[0], p_coords[1], 11, 0
                    elif d_coords:
                        center_lat, center_lon, zoom, pitch = d_coords[0], d_coords[1], 11, 0
                    else:
                        center_lat, center_lon, zoom, pitch = 64.0, 10.0, 3.5, 0

                    points = []
                    if p_coords: points.append({"pos": [p_coords[1], p_coords[0]], "name": "Pickup", "color": [55, 30, 65, 255]})
                    if d_coords: points.append({"pos": [d_coords[1], d_coords[0]], "name": "Delivery", "color": [55, 30, 65, 255]})
                    
                    if points:
                        layers.append(pdk.Layer(
                            "ScatterplotLayer", 
                            data=points, 
                            get_position="pos", 
                            get_fill_color="color",
                            get_line_color=[255, 255, 255, 255],
                            stroked=True,
                            filled=True,
                            line_width_min_pixels=3,
                            get_radius=200, 
                            radius_min_pixels=6, 
                            radius_max_pixels=14
                        ))

                    st.pydeck_chart(pdk.Deck(
                        map_style="dark", 
                        layers=layers, 
                        initial_view_state=pdk.ViewState(latitude=center_lat, longitude=center_lon, zoom=zoom, pitch=pitch)
                    ), height=330)

            st.write("---")
            
            # =========================================================
            # OPTER API INTEGRATIE KNOPPEN (BOVENAAN)
            # =========================================================
            st.markdown("<h4 style='margin-bottom: 5px;'>Opter API Integration</h4>", unsafe_allow_html=True)
            st.markdown("<p style='color: #888; font-size: 13px; margin-bottom: 15px;'>Send or retrieve real-time data for this specific order via Opter.</p>", unsafe_allow_html=True)
            
            col_import, col_export = st.columns(2)
            
            with col_import:
                if st.button("Retrieve Latest Status from Opter", key=f"import_{selected_order['id']}", use_container_width=True):
                    with st.spinner("Fetching latest data from Opter..."):
                        time.sleep(1.5)
                    st.warning("Connection refused. Opter API integration is currently pending consultation.")
                    
            with col_export:
                if st.button("Send Order Details to Opter", key=f"export_{selected_order['id']}", use_container_width=True):
                    with st.spinner("Connecting to Opter API..."):
                        time.sleep(1.5)
                    st.info("Order details formatted for export. Waiting for Opter API credentials to complete the transfer.")
