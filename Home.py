import streamlit as st
import time
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Dahle Transport - Home",
    page_icon="🚚",
    layout="wide"
)

# --- SESSION STATE (De database die gedeeld wordt tussen pagina's) ---
if 'orders' not in st.session_state:
    st.session_state.orders = []
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'selected_type' not in st.session_state:
    st.session_state.selected_type = None
if 'temp_order' not in st.session_state:
    st.session_state.temp_order = {}

# --- CSS STYLING (Strakke website look) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }

    /* Verberg standaard elementen, MAAR LAAT DE SIDEBAR LEVEN */
    [data-testid="stToolbar"] { display: none; }
    [data-testid="stDecoration"] { display: none; }
    footer { visibility: hidden; }
    
    /* Ruimte voor de navbar */
    .block-container { padding-top: 140px; }

    /* NAVBAR */
    .navbar {
        position: fixed; top: 0; left: 0; width: 100%; height: 100px;
        background-color: white; z-index: 999;
        border-bottom: 1px solid #eee; display: flex; align-items: center; justify-content: space-between;
        padding: 0 40px;
    }
    .logo-img { height: 60px; margin-left: 50px; } /* Ruimte voor sidebar pijl */
    .nav-links { font-weight: 600; color: #333; gap: 30px; display: flex; margin-right: 40px;}
    .cta-btn { background: #9b59b6; color: white; padding: 10px 25px; border-radius: 20px; text-decoration: none; }

    /* CARDS */
    .option-card {
        background: #262626; border: 1px solid #444; border-radius: 10px;
        padding: 30px; text-align: center; min-height: 280px;
        display: flex; flex-direction: column; justify-content: center;
    }
    .option-card:hover { border-color: #9b59b6; background: #2e2e2e; transform: translateY(-5px); transition: 0.3s;}
    
    /* BUTTONS */
    div.stButton > button { background: #9b59b6; color: white; border: none; border-radius: 25px; padding: 10px 25px; width: 100%; font-weight: bold;}
    div.stButton > button:hover { background: #af6bca; color: white; }
    </style>
    
    <div class="navbar">
        <img src="https://cloud-1de12d.becdn.net/media/original/964295c9ae8e693f8bb4d6b70862c2be/logo-website-top-png-1-.webp" class="logo-img">
        <div class="nav-links">
            <span>Home</span><span>About</span><span>Services</span>
            <a class="cta-btn">CONTACT</a>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- DE WEBSITE LOGICA ---
st.markdown("<h2 style='text-align: center; margin-bottom: 40px;'>📦 Create new shipment</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # STAP 1: KEUZE
    if st.session_state.step == 1:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown('<div class="option-card"><h1>📦</h1><h3>Parcels</h3><p>Small boxes & docs</p></div>', unsafe_allow_html=True)
            if st.button("Select Parcels"):
                st.session_state.selected_type = "Parcels"
                st.session_state.step = 2
                st.rerun()
        with c2:
            st.markdown('<div class="option-card"><h1>🚛</h1><h3>Freight</h3><p>Pallets & Cargo</p></div>', unsafe_allow_html=True)
            if st.button("Select Freight"):
                st.session_state.selected_type = "Freight"
                st.session_state.step = 2
                st.rerun()
        with c3:
            st.markdown('<div class="option-card"><h1>❄️</h1><h3>Special</h3><p>Refrigerated/ADR</p></div>', unsafe_allow_html=True)
            if st.button("Select Special"):
                st.session_state.selected_type = "Special"
                st.session_state.step = 2
                st.rerun()

    # STAP 2: DETAILS
    elif st.session_state.step == 2:
        st.info(f"Shipping Type: {st.session_state.selected_type}")
        with st.form("shipment_form"):
            company = st.text_input("Company Name")
            email = st.text_input("Email")
            route = st.text_input("Route (e.g. Oslo -> Bergen)")
            weight = st.number_input("Weight (kg)", min_value=1)
            
            c_back, c_next = st.columns([1, 4])
            back = c_back.form_submit_button("← Back")
            submit = c_next.form_submit_button("Send Request")
            
            if back:
                st.session_state.step = 1
                st.rerun()
            
            if submit and company and email:
                new_order = {
                    "id": len(st.session_state.orders) + 1001,
                    "company": company,
                    "email": email,
                    "type": st.session_state.selected_type,
                    "route": route,
                    "weight": weight,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "status": "New"
                }
                st.session_state.orders.append(new_order)
                st.success("Order Sent!")
                time.sleep(1)
                st.session_state.step = 1
                st.rerun()

# Sidebar info
st.sidebar.info("👈 Gebruik dit menu om naar het **Planner Dashboard** te gaan.")