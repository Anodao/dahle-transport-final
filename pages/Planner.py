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

# --- CSS STYLING & NAVBAR HTML ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }

    /* Achtergrond wit, teksten zwart */
    .stApp { background-color: #ffffff !important; }
    h1, h2, h3, h4, h5, h6 { color: #111111 !important; }
    p, .stMarkdown, .stText, label { color: #111111 !important; } 

    /* Verberg standaard Streamlit elementen */
    header[data-testid="stHeader"] { visibility: hidden; display: none !important; }
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    footer { visibility: hidden; }

    /* --- NAVBAR STYLE --- */
    .navbar {
        position: fixed; top: 0; left: 0; width: 100%; height: 90px;
        background-color: #ffffff !important; z-index: 999; border-bottom: 1px solid #eaeaea; 
        display: grid; grid-template-columns: 1fr auto 1fr; align-items: center;
        padding: 0 40px; box-shadow: 0 2px 10px rgba(0,0,0,0.03);
    }
    .nav-logo img { height: 48px; width: auto; transition: transform 0.2s; }
    .nav-links { display: flex; gap: 28px; font-size: 15px; font-weight: 500; justify-content: center; }
    .nav-links a, .nav-links span { text-decoration: none; color: #111111 !important; cursor: pointer; }
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

    /* PAARS HEADER BLOK */
    .planner-banner {
        background-color: #894b9d !important; padding: 40px; border-radius: 12px; margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    .planner-banner h1, .planner-banner p { color: #ffffff !important; }
    
    /* INPUT VELDEN (Datumkiezer & Dropdown lichter maken) */
    div[data-baseweb="select"] > div, 
    div[data-baseweb="input"] > div, 
    div[data-baseweb="base-input"] {
        background-color: #f8f9fa !important; 
        border: 1px solid #ced4da !important; 
        color: #111111 !important;
    }
    input[type="text"], div[data-baseweb="select"] span { color: #111111 !important; }
    
    /* BOXJES & KNOPPEN */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff !important; border: 1px solid #e0e0e0 !important; border-radius: 8px !important;
    }
    div.stButton > button { background-color: #f0f2f6 !important; color: #111111 !important; border: 1px solid #dcdcdc !important; }
    div.stButton > button:hover { background-color: #e0e2e6 !important; }
    div.stButton > button[kind="primary"] { background-color: #894b9d !important; color: #ffffff !important; border: none !important; }
    div.stButton > button[kind="primary"]:hover { background-color: #723e83 !important; }
    
    /* Zorg dat tabbladen netjes zwart zijn */
    button[data-baseweb="tab"] p { color: #111111 !important; font-weight: 600; }
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

# --- DATA & LOGICA ---
if 'selected_order' not in st.session_state:
    st.session_state.selected_order = None

try:
    response = supabase.table("orders").select("*").order("id", desc=True).execute()
    orders = response.data
except:
    orders = []

# --- DATUM BEREKENINGEN ---
vandaag = datetime.now().date()
start_deze_week = vandaag - timedelta(days=vandaag.weekday())
eind_deze_week = start_deze_week + timedelta(days=6)

start_vorige_week = start_deze_week - timedelta(days=7)
eind_vorige_week = start_vorige_week + timedelta(days=6)

eerste_dag_deze_maand = vandaag.replace(day=1)
eind_vorige_maand = eerste_dag_deze_maand - timedelta(days=1)
start_vorige_maand = eind_vorige_maand.replace(day=1)

# --- LAYOUT ---
col_inbox, col_details = st.columns([1, 2], gap="large")

with col_inbox:
    st.subheader("📥 Inbox")
    
    # SNELLE FILTERS DROPDOWN
    filter_optie = st.selectbox("⏱️ Filter Periode", ["Alle orders", "Deze week", "Vorige week", "Vorige maand", "Aangepaste datum..."])
    
    # Bepaal de datum op basis van de keuze
    filter_dates = []
    if filter_optie == "Deze week":
        filter_dates = [start_deze_week, eind_deze_week]
    elif filter_optie == "Vorige week":
        filter_dates = [start_vorige_week, eind_vorige_week]
    elif filter_optie == "Vorige maand":
        filter_dates = [start_vorige_maand, eind_vorige_maand]
    elif filter_optie == "Aangepaste datum...":
        filter_dates = st.date_input("📅 Kies een periode of dag", value=[])

    st.write("") # Beetje ademruimte
    
    # TABBLADEN
    tab_new, tab_proc = st.tabs(["🔴 New Orders", "🟢 Processed Orders"])
    
    def render_order_list(status_filter):
        filtered_orders = [o for o in orders if o.get('status') == status_filter]
        
        if len(filter_dates) > 0:
            date_filtered = []
            for o in filtered_orders:
                try:
                    order_date = datetime.strptime(o['received_date'][:10], "%Y-%m-%d").date()
                    if len(filter_dates) == 2: 
                        if filter_dates[0] <= order_date <= filter_dates[1]:
                            date_filtered.append(o)
                    elif len(filter_dates) == 1: 
                        if order_date == filter_dates[0]:
                            date_filtered.append(o)
                except Exception:
                    date_filtered.append(o)
            filtered_orders = date_filtered
            
        if not filtered_orders:
            st.info(f"No {status_filter.lower()} orders found in this period.")
            
        for o in filtered_orders:
            with st.container(border=True):
                status_color = "#ff4b4b" if o['status'] == 'New' else "#28a745"
                st.markdown(f"<span style='color:{status_color}; font-weight:bold;'>● {o['status']}</span> | **{o['company']}**", unsafe_allow_html=True)
                st.write(f"*{o['types']}*")
                st.caption(f"Received: {o['received_date']}")
                
                if st.button(f"Open Order #{o['id']}", key=f"btn_{o['id']}", use_container_width=True):
                    st.session_state.selected_order = o
                    st.rerun()

    with tab_new:
        render_order_list("New")
    with tab_proc:
        render_order_list("Processed")

with col_details:
    st.subheader("📋 Order Details")
    if st.session_state.selected_order:
        o = st.session_state.selected_order
        with st.container(border=True):
            status_c = "🔴 New" if o['status'] == 'New' else "🟢 Processed"
            st.write(f"### Order #{o['id']} - {o['company']}")
            st.write(f"**Status:** {status_c}")
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
        st.info("Select an order from the inbox to view details.")

# --- NAVIGATIE KNOPPEN ONDERAAN ---
st.write("---")
st.write("")
c1, c2, spacer1, spacer2 = st.columns(4)
with c1:
    if st.button("🏠 ← Go Back to Website", use_container_width=True):
        st.switch_page("Home.py")
with c2:
    if st.button("🟢 Open CO₂ Dashboard →", use_container_width=True):
        st.switch_page("pages/Dashboard.py")
