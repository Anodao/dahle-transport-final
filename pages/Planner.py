import streamlit as st
from supabase import create_client
from datetime import datetime, timedelta

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Dahle Transport - Planner",
    page_icon="🔒",
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
    st.error("⚠️ Database connection failed.")

# --- CSS STYLING (Lichtgrijs met Witte Kaarten) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }

    /* Achtergrond lichtgrijs voor contrast met witte kaarten */
    .stApp { background-color: #f3f4f6 !important; }
    h1, h2, h3, h4, h5, h6, p, label { color: #111827 !important; }

    /* Verberg standaard Streamlit elementen */
    header[data-testid="stHeader"] { visibility: hidden; display: none !important; }
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    footer { visibility: hidden; }

    /* --- NAVBAR STYLE --- */
    .navbar {
        position: fixed; top: 0; left: 0; width: 100%; height: 90px;
        background-color: #ffffff !important; z-index: 999; border-bottom: 1px solid #e5e7eb; 
        display: grid; grid-template-columns: 1fr auto 1fr; align-items: center;
        padding: 0 40px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .nav-logo img { height: 48px; width: auto; }
    .nav-links { display: flex; gap: 28px; font-size: 15px; font-weight: 500; justify-content: center; }
    .nav-links a { text-decoration: none; color: #374151 !important; }
    .nav-cta { display: flex; justify-content: flex-end; gap: 15px; }
    
    .cta-btn { 
        background-color: #894b9d !important; color: white !important; padding: 10px 24px; border-radius: 50px; 
        text-decoration: none !important; font-weight: 600; font-size: 13px; white-space: nowrap;
    }
    .cta-btn-outline {
        background-color: transparent !important; color: #894b9d !important; padding: 10px 20px; border-radius: 50px; 
        text-decoration: none !important; font-weight: 600; font-size: 13px; border: 2px solid #894b9d; white-space: nowrap;
    }

    .block-container { padding-top: 110px !important; max-width: 95%; }
    
    /* INPUT VELDEN */
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
        background-color: #ffffff !important; border: 1px solid #d1d5db !important; border-radius: 6px !important;
    }

    /* --- DE WITTE KAARTEN (De rand die je wilde) --- */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff !important; 
        border: 1px solid #e5e7eb !important; 
        border-radius: 12px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
        padding: 25px !important;
        margin-bottom: 20px !important;
    }
    
    /* TABBLADEN */
    div[data-baseweb="tab-list"] { gap: 10px; border-bottom: 1px solid #e5e7eb; }
    button[data-baseweb="tab"] {
        background-color: transparent !important; border: none !important; padding: 10px 20px !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        border-bottom: 3px solid #894b9d !important;
    }
    div[data-baseweb="tab-highlight"] { display: none !important; }

    /* ORDER SPECIFICATIE BLOK FIX */
    .order-info-box {
        background-color: #f9fafb; border: 1px solid #e5e7eb; padding: 20px; 
        border-radius: 8px; color: #1f2937; font-family: 'Courier New', Courier, monospace;
        line-height: 1.6; font-size: 14px; margin-top: 15px;
    }
    </style>
    
    <div class="navbar">
        <div class="nav-logo"><a href="/"><img src="https://cloud-1de12d.becdn.net/media/original/964295c9ae8e693f8bb4d6b70862c2be/logo-website-top-png-1-.webp"></a></div>
        <div class="nav-links"><a href="/"><span>Hjem</span></a><span>Om oss</span><span>Tjenester</span><span>Galleri</span><span>Kontakt</span></div>
        <div class="nav-cta">
            <a href="/Opter_Portal" class="cta-btn-outline">OPTER LOGIN</a>
            <a href="/" class="cta-btn">TA KONTAKT</a>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- DATA ---
if 'selected_order' not in st.session_state: st.session_state.selected_order = None

try:
    response = supabase.table("orders").select("*").order("id", desc=True).execute()
    orders = response.data
except: orders = []

# --- LAYOUT ---
col_inbox, col_details = st.columns([1, 2], gap="large")

with col_inbox:
    with st.container(border=True):
        st.subheader("Inbox")
        filter_optie = st.selectbox("Filter Periode", ["Alle orders", "Deze week", "Vorige week"])
        
        tab_new, tab_proc = st.tabs(["🔴 New", "🟢 Processed"])
        
        def show_list(stat):
            filtered = [o for o in orders if o.get('status') == stat]
            for o in filtered:
                with st.container(border=True):
                    st.markdown(f"**{o['company']}**")
                    st.caption(f"ID: #{o['id']} | {o['received_date']}")
                    if st.button(f"View Order Details", key=f"v_{o['id']}", use_container_width=True):
                        st.session_state.selected_order = o
                        st.rerun()
        
        with tab_new: show_list("New")
        with tab_proc: show_list("Processed")

with col_details:
    with st.container(border=True):
        st.subheader("Order Details")
        if st.session_state.selected_order:
            o = st.session_state.selected_order
            st.write(f"### Order #{o['id']} - {o['company']}")
            
            c1, c2 = st.columns(2)
            with c1:
                st.write("**Contact Info**")
                st.write(f"Name: {o['contact_name']}\n\nEmail: {o['email']}\n\nPhone: {o['phone']}")
            with c2:
                st.write("**Route**")
                st.write(f"Pickup: {o['pickup_address']}\n\nDelivery: {o['delivery_address']}")
            
            # --- DE VEILIGE TEKST FIX ---
            st.write("---")
            st.write("**Specifications**")
            clean_info = str(o['info']).replace("</div>", "").replace("<div>", "")
            st.markdown(f'<div class="order-info-box">{clean_info}</div>', unsafe_allow_html=True)
            
            if o['status'] == 'New':
                st.write("")
                if st.button("✅ PROCESS AND SEND TO OPTER TMS", type="primary", use_container_width=True):
                    supabase.table("orders").update({"status": "Processed"}).eq("id", o['id']).execute()
                    st.session_state.selected_order['status'] = 'Processed'
                    st.rerun()
        else:
            st.info("Select an order to view details.")

# --- FOOTER BUTTONS RECHTS ---
st.write("")
_, c_nav1, c_nav2 = st.columns([2, 1, 1])
with c_nav1:
    if st.button("🏠 Home", use_container_width=True): st.switch_page("Home.py")
with c_nav2:
    if st.button("🟢 Dashboard", use_container_width=True): st.switch_page("pages/Dashboard.py")
