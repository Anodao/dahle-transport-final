import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client
import extra_streamlit_components as stx
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="Dahle Transport - Planner", page_icon="📅", layout="wide", initial_sidebar_state="collapsed")

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

/* DE LINK TEKSTEN IN HET MIDDEN */
.nav-links { display: flex; gap: 28px; font-size: 15px; font-weight: 600; justify-content: center; align-items: center;}
.nav-links a, .nav-links span { text-decoration: none; color: #111111 !important; cursor: pointer; transition: color 0.2s;}
.nav-links span:hover { color: #894b9d !important; }

/* HET TEKST-DROPDOWN MENU NAAST 'CONTACT' */
.nav-text-dropdown { position: relative; display: inline-block; cursor: pointer; padding-bottom: 20px; margin-bottom: -20px; }
.nav-text-dropbtn { background: transparent; border: none; font-size: 15px; font-weight: 600; color: #111111 !important; cursor: pointer; padding: 0; font-family: inherit; transition: color 0.2s; display: flex; align-items: center; gap: 4px; }
.nav-text-dropdown:hover .nav-text-dropbtn { color: #894b9d !important; }
.nav-text-dropdown::after { content: ''; position: absolute; top: 100%; left: 0; width: 100%; height: 20px; background: transparent; display: none; }
.nav-text-dropdown:hover::after { display: block; }
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
.lang-dropdown { position: relative; display: inline-block; margin-right: 10px; }
.lang-dropbtn { background-color: #f8f9fa; color: #111; font-weight: 600; font-size: 13px; border: 1px solid #eaeaea; border-radius: 20px; padding: 8px 16px; cursor: pointer; display: flex; align-items: center; gap: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.03); transition: all 0.2s ease; }
.lang-dropbtn:hover { background-color: #eaeaea; }
.lang-dropdown::after { content: ''; position: absolute; top: 100%; right: 0; width: 140px; height: 20px; background: transparent; display: none; z-index: 999; }
.lang-dropdown:hover::after { display: block; }
.lang-dropdown-content { display: none; position: absolute; background-color: #ffffff; min-width: 140px; box-shadow: 0px 8px 24px rgba(0,0,0,0.12); border-radius: 12px; border: 1px solid #eaeaea; z-index: 1000; top: calc(100% + 5px); right: 0; margin-top: 0; overflow: hidden; }
.lang-dropdown-content a { color: #111 !important; padding: 12px 16px; text-decoration: none; display: flex; align-items: center; gap: 10px; font-size: 14px; font-weight: 500; transition: background-color 0.2s; }
.lang-dropdown-content a:hover { background-color: #f4e9f7; color: #894b9d !important; }
.lang-dropdown:hover .lang-dropdown-content { display: block; }

/* Dashboard elementen styling */
div[data-baseweb="select"] > div, div[data-baseweb="base-input"] { background-color: #212529 !important; border: 1px solid #333333 !important; border-radius: 6px !important; }
.stSelectbox div[data-baseweb="select"] span, .stSelectbox div[data-baseweb="select"] div, .stDateInput input { color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; }
label[data-testid="stWidgetLabel"] p { color: #ffffff !important; font-weight: 600; font-size: 14px; }
div[data-testid="stVerticalBlockBorderWrapper"] { background-color: #1a1a1a !important; border: 1px solid #333333 !important; border-radius: 10px !important; padding: 15px !important; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 2. INIT COOKIE MANAGER & TAAL LOGICA
# =========================================================
cookie_manager = stx.CookieManager()

if 'language' not in st.session_state:
    st.session_state.language = "no"

if "lang" in st.query_params:
    url_lang = st.query_params["lang"]
    if url_lang in ["no", "en", "sv", "da"]:
        st.session_state.language = url_lang
        cookie_manager.set("dahle_lang", url_lang, key="set_lang_safe")

lang = st.session_state.language 
lang_displays = { "no": "🇳🇴 Norsk", "en": "🇬🇧 English", "sv": "🇸🇪 Svenska", "da": "🇩🇰 Dansk" }
current_lang_display = lang_displays.get(lang, "🇳🇴 Norsk")

# =========================================================
# 3. WOORDENBOEK
# =========================================================
translations = {
    "no": { 
        "nav_home": "Hjem", "nav_about": "Om oss", "nav_services": "Tjenester", "nav_gallery": "Galleri", "nav_contact": "Kontakt", 
        "menu_title": "Sider ⌄", "menu_dash": "CO2 Dashboard", "menu_login": "Kundeportal", "menu_order": "Ny bestilling",
        "nav_portal": "KUNDEPORTAL", "nav_contact_btn": "TA KONTAKT"
    },
    "en": { 
        "nav_home": "Home", "nav_about": "About us", "nav_services": "Services", "nav_gallery": "Gallery", "nav_contact": "Contact", 
        "menu_title": "Pages ⌄", "menu_dash": "CO2 Dashboard", "menu_login": "Customer Portal", "menu_order": "New Order",
        "nav_portal": "CUSTOMER PORTAL", "nav_contact_btn": "CONTACT US"
    },
    "sv": { 
        "nav_home": "Hem", "nav_about": "Om oss", "nav_services": "Tjänster", "nav_gallery": "Galleri", "nav_contact": "Kontakt", 
        "menu_title": "Sidor ⌄", "menu_dash": "CO2 Dashboard", "menu_login": "Kundportal", "menu_order": "Ny beställning",
        "nav_portal": "KUNDPORTAL", "nav_contact_btn": "KONTAKTA OSS"
    },
    "da": { 
        "nav_home": "Hjem", "nav_about": "Om os", "nav_services": "Tjenester", "nav_gallery": "Galleri", "nav_contact": "Kontakt", 
        "menu_title": "Sider ⌄", "menu_dash": "CO2 Dashboard", "menu_login": "Kundeportal", "menu_order": "Ny bestilling",
        "nav_portal": "KUNDEPORTAL", "nav_contact_btn": "KONTAKT OS"
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
# 5. NAVBAR SAMENSTELLEN (Zonder 'Planner' in de dropdown)
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
<a href="/Login?lang={lang}" target="_self">🔐 {t['menu_login']}</a>
<a href="/Order?lang={lang}" target="_self">📦 {t['menu_order']}</a>
<a href="/Dashboard?lang={lang}" target="_self">📈 {t['menu_dash']}</a>
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

    # --- Strakke 5-koloms weergave ---
    m1, m2, m3, m4, m5 = st.columns(5)
    
    with m1:
        with st.container(border=True):
            st.markdown("<div style='font-size: 14px; color: #ccc;'>🔴 Action Required</div>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='margin: 0; padding-top: 5px;'>{count_pending}</h2>", unsafe_allow_html=True)
    with m2:
        with st.container(border=True):
            st.markdown("<div style='font-size: 14px; color: #ccc;'>🟡 Active Routes</div>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='margin: 0; padding-top: 5px;'>{count_progress}</h2>", unsafe_allow_html=True)
    with m3:
        with st.container(border=True):
            st.markdown("<div style='font-size: 14px; color: #ccc;'>🟢 Completed</div>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='margin: 0; padding-top: 5px;'>{count_done}</h2>", unsafe_allow_html=True)
    with m4:
        with st.container(border=True):
            st.markdown("<div style='font-size: 14px; color: #ccc;'>⚫ Cancelled</div>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='margin: 0; padding-top: 5px;'>{count_cancelled}</h2>", unsafe_allow_html=True)
    with m5:
        with st.container(border=True):
            st.markdown("<div style='font-size: 14px; color: #ccc;'>📋 Total Orders</div>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='margin: 0; padding-top: 5px;'>{total_orders}</h2>", unsafe_allow_html=True)

st.write("---")

# =========================================================
# LAYOUT (2 KOLOMMEN)
# =========================================================
col_list, col_details = st.columns([1, 2], gap="large")

with col_list:
    st.markdown("<h2>Inbox</h2>", unsafe_allow_html=True)
    
    tab_new, tab_prog, tab_done, tab_fail = st.tabs(["🔴 Pending", "🟡 In Progress", "🟢 Done", "❌ Cancelled"])
    
    with tab_new:
        pending = [o for o in all_orders if o['status'] == 'New']
        if not pending: st.info("No pending orders.")
        for o in pending:
            with st.container(border=True):
                st.markdown(f"**🔴 {o['company']}**")
                st.caption(f"Order #{o['id']} | Received: {o.get('received_date', '')[:10]}")
                if st.button(f"View #{o['id']}", key=f"p_{o['id']}", use_container_width=True):
                    st.session_state.selected_order_id = o['id']
                    st.rerun()

    with tab_prog:
        inprogress = [o for o in all_orders if o['status'] == 'In Progress']
        if not inprogress: st.info("Nothing in progress.")
        for o in inprogress:
            with st.container(border=True):
                st.markdown(f"**🟡 {o['company']}**")
                st.caption(f"Order #{o['id']} | Received: {o.get('received_date', '')[:10]}")
                if st.button(f"View #{o['id']}", key=f"prog_{o['id']}", use_container_width=True):
                    st.session_state.selected_order_id = o['id']
                    st.rerun()

    with tab_done:
        done = [o for o in all_orders if o['status'] in ['Processed', 'Delivered']]
        if not done: st.info("No completed orders.")
        for o in done:
            with st.container(border=True):
                st.markdown(f"**🟢 {o['company']}**")
                proc_date = o.get('processed_date')
                display_date = proc_date[:10] if proc_date else o.get('received_date', '')[:10]
                st.caption(f"Order #{o['id']} | Afgerond | Datum: {display_date}")
                if st.button(f"View #{o['id']}", key=f"d_{o['id']}", use_container_width=True):
                    st.session_state.selected_order_id = o['id']
                    st.rerun()

    with tab_fail:
        failed = [o for o in all_orders if o['status'] == 'Cancelled']
        if not failed: st.info("No cancelled orders.")
        for o in failed:
            with st.container(border=True):
                st.markdown(f"**❌ {o['company']}**")
                proc_date = o.get('processed_date')
                display_date = proc_date[:10] if proc_date else o.get('received_date', '')[:10]
                st.caption(f"Order #{o['id']} | Niet gelukt | Datum: {display_date}")
                if st.button(f"View #{o['id']}", key=f"f_{o['id']}", use_container_width=True):
                    st.session_state.selected_order_id = o['id']
                    st.rerun()

with col_details:
    st.markdown("<h2>Order Details</h2>", unsafe_allow_html=True)
    st.write("---")
    
    if st.session_state.selected_order_id:
        order = next((o for o in all_orders if o['id'] == st.session_state.selected_order_id), None)
        if order:
            st.markdown(f"### Order #{order['id']} - {order['company']}")
            
            with st.container(border=True):
                r1, r2 = st.columns(2)
                with r1:
                    st.markdown("#### 📤 Pickup Details")
                    st.markdown(f"**Address:** {order.get('pickup_address', '-')}")
                    st.markdown(f"**Zip Code:** {order.get('pickup_zip', '-')}")
                    st.markdown(f"**City:** {order.get('pickup_city', '-')}")
                with r2:
                    st.markdown("#### 📥 Delivery Details")
                    st.markdown(f"**Address:** {order.get('delivery_address', '-')}")
                    st.markdown(f"**Zip Code:** {order.get('delivery_zip', '-')}")
                    st.markdown(f"**City:** {order.get('delivery_city', '-')}")
            
            with st.container(border=True):
                st.markdown("#### 📞 Contact Information")
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.markdown("**Contact Person**")
                    st.write(order.get('contact_name', '-'))
                with c2:
                    st.markdown("**Phone**")
                    st.write(order.get('phone', '-'))
                with c3:
                    st.markdown("**Email**")
                    st.write(order.get('email', '-'))

            with st.container(border=True):
                st.markdown("#### 📝 Specifications & Internal Notes")
                st.markdown(f"**Requested Services:** {order.get('types', '-')}")
                if order.get('info'):
                    st.info(order['info'])
                
                st.write("---")
                st.markdown("**Internal Dispatch Notes (Hidden from customer):**")
                current_notes = order.get('internal_notes', '')
                new_notes = st.text_area("Typ hier je eigen notities...", value=current_notes if current_notes else "", height=100, label_visibility="collapsed")
            
            st.write("")
            
            st.markdown("#### Control Panel")
            status_list = ["New", "In Progress", "Processed", "Delivered", "Cancelled"]
            try:
                current_idx = status_list.index(order['status'])
            except:
                current_idx = 0
                
            new_status = st.selectbox("Update Order Status", options=status_list, index=current_idx)
            
            if st.button("💾 Save Updates", type="primary", use_container_width=True):
                update_data = {
                    "status": new_status,
                    "processed_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "internal_notes": new_notes
                }
                supabase.table("orders").update(update_data).eq("id", order['id']).execute()
                st.success("✅ Updates saved successfully!")
                time.sleep(1)
                st.rerun()
    else:
        st.info("👈 Select an order from the Inbox to view details and update its status.")
