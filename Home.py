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

# --- CSS STYLING (De Echte Dahle Look is terug) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }

    /* --- HEADER & SIDEBAR KNOP FIX --- */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    div[data-testid="stDecoration"] { display: none; }
    div[data-testid="stToolbar"] { display: none; }
    
    /* Maak het sidebar pijltje ZWART en goed zichtbaar */
    button[kind="header"] {
        color: #333 !important;
        margin-top: 5px; 
    }
    
    footer { visibility: hidden; }
    
    /* --- NAVBAR STYLING (Precies zoals eerst) --- */
    .block-container { padding-top: 150px; }

    .navbar {
        position: fixed; top: 0; left: 0; width: 100%; height: 110px;
        background-color: white; z-index: 999;
        border-bottom: 1px solid #eaeaea; 
        display: flex; align-items: center; justify-content: space-between;
        padding: 0 50px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03);
    }
    
    .logo-img { height: 60px; margin-left: 50px; } 
    
    /* De tekst linkjes */
    .nav-links { 
        font-size: 15px; 
        font-weight: 600; 
        color: #333; 
        display: flex; 
        gap: 30px; 
        margin-right: 40px;
        align-items: center;
    }
    
    .nav-links span { cursor: pointer; transition: 0.2s; }
    .nav-links span:hover { color: #9b59b6; }

    /* De paarse knop */
    .cta-btn { 
        background-color: #9b59b6; 
        color: white; 
        padding: 12px 28px; 
        border-radius: 25px; 
        text-decoration: none; 
        font-weight: bold; 
        font-size: 14px;
        box-shadow: 0 4px 6px rgba(155, 89, 182, 0.2);
    }

    /* --- CARDS --- */
    .option-card {
        background: #262626; border: 1px solid #444; border-radius: 12px;
        padding: 40px 20px; text-align: center; min-height: 280px;
        display: flex; flex-direction: column; justify-content: center;
    }
    .option-card:hover { border-color: #9b59b6; background: #2e2e2e; transform: translateY(-5px); transition: 0.3s;}
    
    /* --- BUTTONS --- */
    div.stButton > button { background: #9b59b6; color: white; border: none; border-radius: 30px; padding: 12px 28px; width: 100%; font-weight: bold;}
    div.stButton > button:hover { background: #af6bca; color: white; }
    
    /* FORMS */
    div[data-baseweb="input"] { background-color: #333; border-radius: 8px; }
    div[data-baseweb="input"] input { color: white; }
    label { color: #ccc !important; font-weight: 600; }
    </style>
    
    <div class="navbar">
        <img src="https://cloud-1de12d.becdn.net/media/original/964295c9ae8e693f8bb4d6b70862c2be/logo-website-top-png-1-.webp" class="logo-img">
        <div class="nav-links">
            <span>Home</span>
            <span>About Us</span>
            <span>Services</span>
            <span>Gallery</span>
            <span>Contact</span>
            <a class="cta-btn">CONTACT US</a>
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
            st.markdown('<div class="option-card"><h1>📦</h1><h3>Parcels & Docs</h3><p>Small boxes, envelopes, and urgent documents up to 30kg.</p></div>', unsafe_allow_html=True)
            if st.button("Select Parcels"):
                st.session_state.selected_type = "Parcels/Docs"
                st.session_state.step = 2
                st.rerun()
        with c2:
            st.markdown('<div class="option-card"><h1>🚛</h1><h3>Freight / Pallets</h3><p>Euro pallets, industrial goods, and bulk cargo over 30kg.</p></div>', unsafe_allow_html=True)
            if st.button("Select Freight"):
                st.session_state.selected_type = "Freight/Pallets"
                st.session_state.step = 2
                st.rerun()
        with c3:
            st.markdown('<div class="option-card"><h1>❄️</h1><h3>Special Transport</h3><p>Refrigerated, hazardous (ADR), or oversized loads.</p></div>', unsafe_allow_html=True)
            if st.button("Select Special"):
                st.session_state.selected_type = "Special Transport"
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
