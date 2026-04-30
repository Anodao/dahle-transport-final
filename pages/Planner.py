import streamlit as st
from supabase import create_client
import extra_streamlit_components as stx
import time

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
div[data-baseweb="select"] > div, div[data-baseweb="base-input"] { background-color: #1e1e1e !important; border: 1px solid #333333 !important; border-radius: 6px !important; }
.stSelectbox div[data-baseweb="select"] span, .stSelectbox div[data-baseweb="select"] div, .stDateInput input { color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; }
label[data-testid="stWidgetLabel"] p { color: #ffffff !important; font-weight: 600; font-size: 14px; }
div[data-testid="stVerticalBlockBorderWrapper"] { background-color: #1a1a1a !important; border: 1px solid #333333 !important; border-radius: 10px !important; padding: 15px !important; }
div[data-testid="stMetric"] { background-color: #161616 !important; border: 1px solid #333 !important; padding: 15px !important; border-radius: 8px !important; }
div[data-testid="stMetricValue"] { font-size: 36px !important; font-weight: 700 !important; }
/* KNOPPEN STYLING */
div.stButton > button[kind="primary"] { background: linear-gradient(135deg, #b070c6 0%, #894b9d 100%) !important; color: #ffffff !important; border: 2px solid transparent !important; border-radius: 6px !important; padding: 10px 24px !important; font-weight: 600 !important; font-size: 14px !important; width: 100% !important; transition: all 0.3s ease !important; }
div.stButton > button[kind="primary"]:hover { background: #ffffff !important; color: #894b9d !important; border: 2px solid #894b9d !important; }
div.stButton > button[kind="secondary"] { background: transparent !important; color: #e0c2ed !important; border: 1px solid #894b9d !important; border-radius: 6px !important; padding: 8px 16px !important; font-weight: 600 !important; font-size: 13px !important; width: 100% !important; transition: all 0.3s ease !important; }
div.stButton > button[kind="secondary"]:hover { background: #894b9d !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 2. INIT COOKIE MANAGER & ROBUUSTE AUTH VERIFICATIE
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

# --- DE SLIMME UITSMIJTER (Verhelpt de flash) ---
if not is_employee:
    # We geven de cookies nu MEER tijd (maximaal ~2.5 sec) om veilig binnen te komen.
    if 'auth_denied_wait' not in st.session_state:
        st.session_state.auth_denied_wait = 0
    
    if st.session_state.auth_denied_wait < 3:  # 3 pogingen
        st.session_state.auth_denied_wait += 1
        st.markdown("<div style='text-align: center; margin-top: 150px; color: #888;'><h3>Verifying permissions...</h3></div>", unsafe_allow_html=True)
        time.sleep(0.6) # Iets langer wachten per poging
        st.rerun()

    # Is hij na alle 3 pogingen nóg geen medewerker? Dán pas de rode melding tonen.
    html_navbar_empty = f"""<div class="navbar"><div class="nav-logo"><a href="/?lang=no"><img src="https://cloud-1de12d.becdn.net/media/original/964295c9ae8e693f8bb4d6b70862c2be/logo-website-top-png-1-.webp"></a></div></div>"""
    st.markdown(html_navbar_empty, unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: center; margin-top: 120px;'><h1 style='color:#ff4b4b;'>Access Denied</h1><p style='color:#aaa; font-size: 18px;'>You do not have permission to view the internal dashboard.</p></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,1,1])
    with c2: 
        st.markdown(f'<a href="/" target="_self" style="display: block; text-align: center; background-color: transparent; color: #894b9d; padding: 10px 20px; border-radius: 50px; text-decoration: none; font-weight: 600; border: 2px solid #894b9d;">← Back to Home</a>', unsafe_allow_html=True)
    st.stop()


# =========================================================
# 3. TAAL LOGICA MET COOKIES
# =========================================================
saved_lang = cookie_manager.get('dahle_lang')

if "lang" in st.query_params:
    url_lang = st.query_params["lang"]
    if url_lang in ["no", "en", "sv", "da"]:
        if url_lang != saved_lang:
            cookie_manager.set("dahle_lang", url_lang, key="set_lang_safe")
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
    "en": { "nav_home": "Home", "nav_about": "About us", "nav_services": "Services", "nav_gallery": "Gallery", "nav_contact": "Contact", "menu_title": "Pages ⌄", "menu_dash": "Performance Dashboard", "menu_login": "Customer Portal", "menu_order": "New Order", "nav_portal": "CUSTOMER PORTAL", "nav_contact_btn": "CONTACT US", "stat_title": "📊 Statistics & KPIs", "filter_lbl": "Filter period:", "opt_30": "Last 30 days", "opt_7": "Last 7 days", "opt_1": "Today", "act_req": "Action Required", "act_routes": "Active Routes", "comp": "Completed", "canc": "Cancelled", "tot_ord": "Total Orders", "inbox": "Inbox", "pend": "Pending", "prog": "In Progress", "done": "Done", "det_title": "Order Details", "det_sub": "👈 Select an order from the Inbox to view details and update status.", "btn_view": "View Order", "status_lbl": "Update Status", "btn_save": "Save Status", "msg_succ": "Status updated successfully!" },
    "sv": { "nav_home": "Hem", "nav_about": "Om oss", "nav_services": "Tjänster", "nav_gallery": "Galleri", "nav_contact": "Kontakt", "menu_title": "Sidor ⌄", "menu_dash": "Performance Dashboard", "menu_login": "Kundportal", "menu_order": "Ny beställning", "nav_portal": "KUNDPORTAL", "nav_contact_btn": "KONTAKTA OSS", "stat_title": "📊 Statistik och KPI:er", "filter_lbl": "Filterperiod:", "opt_30": "Senaste 30 dagarna", "opt_7": "Senaste 7 dagarna", "opt_1": "Idag", "act_req": "Åtgärd krävs", "act_routes": "Aktiva rutter", "comp": "Slutförd", "canc": "Avbruten", "tot_ord": "Totala ordrar", "inbox": "Inkorg", "pend": "Väntar", "prog": "Pågår", "done": "Klar", "det_title": "Orderdetaljer", "det_sub": "👈 Välj en order från inkorgen för att se detaljer och uppdatera status.", "btn_view": "Visa Order", "status_lbl": "Uppdatera Status", "btn_save": "Spara Status", "msg_succ": "Status uppdaterad!" },
    "da": { "nav_home": "Hjem", "nav_about": "Om os", "nav_services": "Tjenester", "nav_gallery": "Galleri", "nav_contact": "Kontakt", "menu_title": "Sider ⌄", "menu_dash": "Performance Dashboard", "menu_login": "Kundeportal", "menu_order": "Ny bestilling", "nav_portal": "KUNDEPORTAL", "nav_contact_btn": "KONTAKT OS", "stat_title": "📊 Statistik og KPI'er", "filter_lbl": "Filterperiode:", "opt_30": "Seneste 30 dage", "opt_7": "Seneste 7 dage", "opt_1": "I dag", "act_req": "Handling påkrævet", "act_routes": "Aktive ruter", "comp": "Gennemført", "canc": "Annulleret", "tot_ord": "Samlede ordrer", "inbox": "Indbakke", "pend": "Afventer", "prog": "I gang", "done": "Færdig", "det_title": "Ordredetaljer", "det_sub": "👈 Vælg en ordre fra indbakken for at se detaljer og opdatere status.", "btn_view": "Vis Ordre", "status_lbl": "Opdater Status", "btn_save": "Gem Status", "msg_succ": "Status opdateret!" }
}
t = translations.get(lang, translations["no"])

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
    
    # Loop door alle échte orders uit de database
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
                
                # Als op de knop wordt geklikt, slaan we het ID op in de sessie en herladen we de pagina
                if st.button(f"{t['btn_view']} #{o['id']}", key=f"view_{o['id']}", type="secondary", use_container_width=True):
                    st.session_state.selected_order_id = o['id']
                    st.rerun()

with col_details:
    st.markdown(f"<h2 style='margin-top:0;'>{t['det_title']}</h2>", unsafe_allow_html=True)
    st.write("---")
    
    if st.session_state.selected_order_id is None:
        st.info(t['det_sub'])
    else:
        # Zoek de specifieke order in de lijst
        selected_order = next((o for o in all_orders if o['id'] == st.session_state.selected_order_id), None)
        
        if selected_order:
            c_info1, c_info2 = st.columns(2)
            
            with c_info1:
                st.markdown(f"#### 🏢 {selected_order.get('company', '-')}")
                st.write(f"**Contact:** {selected_order.get('contact_name', '-')} ({selected_order.get('phone', '-')})")
                st.write(f"**Email:** {selected_order.get('email', '-')}")
                
                st.write("")
                st.markdown("#### 🛣️ Route")
                st.write(f"**From:** {selected_order.get('pickup_city', '-')} ({selected_order.get('pickup_zip', '-')})")
                st.write(f"**To:** {selected_order.get('delivery_city', '-')} ({selected_order.get('delivery_zip', '-')})")

            with c_info2:
                st.markdown("#### 📦 Freight Details")
                types_str = selected_order.get('types', '')
                if types_str:
                    st.write(f"**Types:** {types_str}")
                info_notes = selected_order.get('info', '')
                if info_notes:
                    st.markdown(f"<div style='background-color:#262626; padding:10px; border-radius:6px; font-size:13px; color:#ddd;'>{info_notes}</div>", unsafe_allow_html=True)
                
                st.write("")
                st.markdown("#### 💰 Financials")
                st.write(f"**Est. Cost / Revenue:** {selected_order.get('price', 0):,.0f} NOK")
                profit = selected_order.get('profit', 0)
                color = "green" if profit > 0 else "red"
                st.write(f"**Est. Profit:** <span style='color:{color}; font-weight:bold;'>{profit:,.0f} NOK</span>", unsafe_allow_html=True)

            st.write("---")
            
            # --- STATUS UPDATE MODULE ---
            st.markdown(f"#### {t['status_lbl']}")
            current_status = selected_order.get('status', 'New')
            status_options = ["New", "In Progress", "Processed", "Delivered", "Cancelled"]
            
            # Zorg dat de huidige status geselecteerd is
            idx = status_options.index(current_status) if current_status in status_options else 0
            
            c_stat1, c_stat2 = st.columns([2, 1])
            with c_stat1:
                new_status = st.selectbox("Select new status:", status_options, index=idx, label_visibility="collapsed")
            with c_stat2:
                if st.button(t['btn_save'], type="primary", use_container_width=True):
                    try:
                        # Update de database met de nieuwe status
                        supabase.table("orders").update({"status": new_status}).eq("id", selected_order['id']).execute()
                        st.success(t['msg_succ'])
                        time.sleep(1)
                        st.rerun() # Herlaad om wijzigingen te zien
                    except Exception as e:
                        st.error(f"Failed to update status: {e}")
