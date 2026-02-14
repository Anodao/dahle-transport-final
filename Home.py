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

# --- CSS STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }

    /* --- HEADER & SIDEBAR KNOP FIX --- */
    header[data-testid="stHeader"] { background: transparent !important; }
    div[data-testid="stDecoration"] { display: none; }
    div[data-testid="stToolbar"] { display: none; }
    
    /* Maak het sidebar pijltje ZWART en goed zichtbaar */
    button[kind="header"] { color: #000 !important; margin-top: 5px; }
    footer { visibility: hidden; }
    
    /* --- NAVBAR STYLING (EXACT ZOALS DE FOTO) --- */
    .block-container { padding-top: 150px; }

    .navbar {
        position: fixed; top: 0; left: 0; width: 100%; height: 110px;
        background-color: white; z-index: 999;
        border-bottom: 1px solid #eaeaea; 
        display: flex; align-items: center; justify-content: space-between;
        padding: 0 40px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03);
    }
    
    /* Verdeel de navbar in 3 gelijke blokken voor perfecte centrering */
    .nav-logo {
        flex: 1;
        display: flex;
        justify-content: flex-start;
        padding-left: 50px; /* Ruimte voor de Streamlit sidebar knop */
    }
    .nav-logo img { height: 60px; } 
    
    .nav-links { 
        flex: 2; /* Neemt de middelste ruimte in */
        display: flex; 
        justify-content: center; /* Forceert de tekst naar het midden */
        gap: 35px; 
        font-size: 16px; 
        font-weight: 700; /* Iets dikker (bold), zoals op de foto */
        color: #000; 
    }
    .nav-links span { cursor: pointer; transition: 0.2s; }
    .nav-links span:hover { color: #9b59b6; }

    .nav-cta {
        flex: 1;
        display: flex;
        justify-content: flex-end; /* Forceert de knop helemaal naar rechts */
    }
    .cta-btn { 
        background-color: #8c4b99; /* De paarse kleur van Dahle */
        color: white; 
        padding: 14px 30px; 
        border-radius: 30px; 
        text-decoration: none; 
        font-weight: bold; 
        font-size: 14px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        cursor: pointer;
        transition: 0.2s;
    }
    .cta-btn:hover { background-color: #7a3c87; }

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
        <div class="nav-logo">
            <img src="https://cloud-1de12d.becdn.net/media/original/964295c9ae8e693f8bb4d6b70862c2be/logo-website-top-png-1-.webp" alt="Dahle Transport Logo">
        </div>
        <div class="nav-links">
            <span>Hjem</span>
            <span>Om oss</span>
            <span>Tjenester</span>
            <span>Galleri</span>
            <span>Kontakt</span>
        </div>
        <div class="nav-cta">
            <a class="cta-btn">TA KONTAKT</a>
        </div>
    </div>
""", unsafe_allow_html=True)


# =========================================================
# DE WEBSITE LOGICA
# =========================================================

col_spacer_L, col_main, col_spacer_R = st.columns([1, 3, 1])

with col_main:
    st.markdown("<h2 style='text-align: center; margin-bottom: 40px;'>📦 Create new shipment</h2>", unsafe_allow_html=True)

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
