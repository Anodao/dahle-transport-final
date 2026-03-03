import streamlit as st
from supabase import create_client

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

# --- CSS STYLING & NAVBAR HTML ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }

    /* Verberg standaard Streamlit elementen */
    header[data-testid="stHeader"] { visibility: hidden; display: none !important; }
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    footer { visibility: hidden; }

    /* --- NAVBAR STYLE --- */
    .navbar {
        position: fixed; top: 0; left: 0; width: 100%; height: 90px;
        background-color: white; z-index: 999; border-bottom: 1px solid #eaeaea; 
        display: grid; grid-template-columns: 1fr auto 1fr; align-items: center;
        padding: 0 40px; box-shadow: 0 2px 10px rgba(0,0,0,0.03);
    }
    .nav-logo img { height: 48px; width: auto; transition: transform 0.2s; }
    .nav-links { display: flex; gap: 28px; font-size: 15px; font-weight: 500; color: #000; justify-content: center; }
    .nav-links a { text-decoration: none; color: inherit; }
    .nav-cta { display: flex; justify-content: flex-end; gap: 15px; }
    
    .cta-btn { 
        background-color: #894b9d; color: white !important; padding: 10px 24px; border-radius: 50px; 
        text-decoration: none !important; font-weight: 600; font-size: 13px; white-space: nowrap;
    }
    .cta-btn-outline {
        background-color: transparent; color: #894b9d !important; padding: 10px 20px; border-radius: 50px; 
        text-decoration: none !important; font-weight: 600; font-size: 13px; border: 2px solid #894b9d; white-space: nowrap;
    }

    /* Ruimte maken voor de navbar */
    .block-container { padding-top: 110px !important; max-width: 95%; }

    /* Paars Header Blok Styling */
    .planner-banner {
        background-color: #894b9d; padding: 40px; border-radius: 12px; color: white; margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    </style>

    <div class="navbar">
        <div class="nav-logo">
            <a href="/" target="_self"><img src="https://cloud-1de12d.becdn.net/media/original/964295c9ae8e693f8bb4d6b70862c2be/logo-website-top-png-1-.webp"></a>
        </div>
        <div class="nav-links">
            <a href="/"><span>Hjem</span></a>
            <span>Om oss</span><span>Tjenester</span><span>Galleri</span><span>Kontakt</span>
        </div>
        <div class="nav-cta">
            <a href="/Opter_Portal" target="_self" class="cta-btn-outline">OPTER LOGIN</a>
            <a href="/" target="_self" class="cta-btn">TA KONTAKT</a>
        </div>
    </div>

    <div class="planner-banner">
        <h1 style="margin: 0; font-size: 42px;">🔒 Planner Dashboard</h1>
        <p style="margin: 0; opacity: 0.8; font-size: 16px;">Internal Use Only</p>
    </div>
""", unsafe_allow_html=True)

# --- NAVIGATIE KNOPPEN ---
c1, c2 = st.columns(2)
with c1:
    if st.button("🏠 ← Go Back to Website", use_container_width=True):
        st.switch_page("Home.py")
with c2:
    if st.button("🟢 Open CO₂ Dashboard →", use_container_width=True):
        st.switch_page("pages/Dashboard.py")

st.write("")

# --- DATA & LOGICA ---
if 'selected_order' not in st.session_state:
    st.session_state.selected_order = None

try:
    response = supabase.table("orders").select("*").order("id", desc=True).execute()
    orders = response.data
except:
    orders = []

col_inbox, col_details = st.columns([1, 2], gap="large")

with col_inbox:
    st.subheader("📥 Inbox")
    for o in orders:
        with st.container(border=True):
            status_color = "#ff4b4b" if o['status'] == 'New' else "#28a745"
            st.markdown(f"<span style='color:{status_color}; font-weight:bold;'>● {o['status']}</span> | {o['company']}", unsafe_allow_html=True)
            st.write(f"*{o['types']}*")
            st.caption(f"Received: {o['received_date']}")
            if st.button(f"Open Order #{o['id']}", key=f"btn_{o['id']}", use_container_width=True):
                st.session_state.selected_order = o
                st.rerun()

with col_details:
    st.subheader("📋 Order Details")
    if st.session_state.selected_order:
        o = st.session_state.selected_order
        with st.container(border=True):
            st.write(f"### Order #{o['id']} - {o['company']}")
            st.write("---")
            st.write(f"**Contact:** {o['contact_name']} | {o['email']} | {o['phone']}")
            st.write(f"**Pickup:** {o['pickup_address']}, {o['pickup_zip']} {o['pickup_city']}")
            st.write(f"**Delivery:** {o['delivery_address']}, {o['delivery_zip']} {o['delivery_city']}")
            st.write("---")
            st.text(o['info'])
            if o['status'] == 'New':
                if st.button("✅ Process Order", type="primary", use_container_width=True):
                    supabase.table("orders").update({"status": "Processed"}).eq("id", o['id']).execute()
                    st.session_state.selected_order['status'] = 'Processed'
                    st.rerun()
    else:
        st.info("Select an order to view details.")
