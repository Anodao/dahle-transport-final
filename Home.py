import streamlit as st
import time
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Dahle Transport - Home",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- SESSION STATE ---
if 'orders' not in st.session_state:
    st.session_state.orders = []
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'selected_type' not in st.session_state:
    st.session_state.selected_type = None
if 'temp_order' not in st.session_state:
    st.session_state.temp_order = {}

# --- CSS STYLING (Schone Look) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }

    /* --- DE STANDAARD BALK WEGHALEN --- */
    
    /* 1. Maak de header transparant (zodat je onze witte balk ziet) */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    
    /* 2. Verberg de regenbooglijn en de toolbar rechts */
    div[data-testid="stDecoration"] { display: none; }
    div[data-testid="stToolbar"] { display: none; }
    
    /* 3. Maak het menu-knopje (pijltje) ZWART zodat je hem ziet op wit */
    button[kind="header"] {
        color: #333 !important; 
    }
    
    /* Verberg footer */
    footer { visibility: hidden; }
    
    /* --- EIGEN NAVBAR --- */
    
    /* Content naar beneden duwen zodat het niet achter de balk zit */
    .block-container { padding-top: 140px; }

    .navbar {
        position: fixed; 
        top: 0; 
        left: 0; 
        width: 100%; 
        height: 100px;
        background-color: white; 
        z-index: 999; /* Net onder de header knop */
        border-bottom: 1px solid #eee; 
        display: flex; 
        align-items: center; 
        justify-content: space-between;
        padding: 0 40px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    /* Logo iets naar rechts schuiven voor de menu knop */
    .logo-img { height: 60px; margin-left: 50px; } 
    
    .nav-links { font-weight: 600; color: #333; gap: 30px; display: flex; margin-right: 40px;}
    .cta-btn { background: #9b59b6; color: white; padding: 10px 25px; border-radius: 20px; text-decoration: none; font-weight: bold;}

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
    
    /* FORMS */
    div[data-baseweb="input"] { background-color: #333; border-radius: 8px; }
    div[data-baseweb="input"] input { color: white; }
    label { color: #ccc !important; font-weight: 600; }
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
        st.write("Select the type of goods you want to ship:")
        st.write("")
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
            c_form1, c_form2 = st.columns(2)
            with c_form1:
                company = st.text_input("Company Name")
                email = st.text_input("Email")
            with c_form2:
                route = st.text_input("Route (e.g. Oslo -> Bergen)")
                weight = st.number_input("Weight (kg)", min_value=1)
            
            st.markdown("---")
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
st.sidebar.markdown("### ⚙️ Menu")
st.sidebar.info("Schakel hierboven tussen **Home** (Klant) en **Planner** (Intern).")
