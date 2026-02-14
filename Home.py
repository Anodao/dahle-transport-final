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

# --- LOGO RESET TRUCJE ---
if "reset" in st.query_params:
    st.session_state.step = 1
    st.session_state.selected_types = [] 
    st.session_state.temp_order = {}
    st.query_params.clear()

# --- SESSION STATE ---
if 'orders' not in st.session_state:
    st.session_state.orders = []
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'selected_types' not in st.session_state:
    st.session_state.selected_types = []
if 'temp_order' not in st.session_state:
    st.session_state.temp_order = {}

# --- CSS STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }

    /* --- HEADER & SIDEBAR KNOP FIX --- */
    header[data-testid="stHeader"] { background: transparent !important; pointer-events: none !important; }
    div[data-testid="stDecoration"] { display: none; }
    div[data-testid="stToolbar"] { display: none; }
    button[kind="header"] { color: #000 !important; margin-top: 5px; pointer-events: auto !important; }
    footer { visibility: hidden; }
    
    /* --- NAVBAR STYLING --- */
    .block-container { padding-top: 130px; }

    .navbar {
        position: fixed; top: 0; left: 0; width: 100%; height: 90px;
        background-color: white; z-index: 999; border-bottom: 1px solid #eaeaea; 
        display: grid; grid-template-columns: 1fr auto 1fr; align-items: center;
        padding: 0 40px; box-shadow: 0 2px 10px rgba(0,0,0,0.03);
    }
    .nav-logo { display: flex; justify-content: flex-start; padding-left: 40px; }
    .nav-logo a { display: inline-block; height: 48px; text-decoration: none; cursor: pointer; }
    .nav-logo img { height: 100%; width: auto; display: block; transition: transform 0.2s ease-in-out; }
    .nav-logo a:hover img { transform: scale(1.05); } 
    .nav-links { display: flex; gap: 28px; font-size: 15px; font-weight: 500; color: #000000; }
    .nav-links span { cursor: pointer; transition: color 0.2s; }
    .nav-links span:hover { color: #894b9d; }
    .nav-cta { display: flex; justify-content: flex-end; }
    .cta-btn { 
        background-color: #894b9d; color: white !important; padding: 10px 24px;
        border-radius: 50px; text-decoration: none !important; font-weight: 600; 
        font-size: 13px; letter-spacing: 0.5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        cursor: pointer; transition: background-color 0.2s;
    }
    .cta-btn:hover { background-color: #723e83; }

    /* --- STEP TRACKER STYLING --- */
    .step-wrapper { display: flex; justify-content: center; align-items: flex-start; margin-bottom: 40px; margin-top: 10px; gap: 15px; }
    .step-item { display: flex; flex-direction: column; align-items: center; width: 80px; }
    .step-circle {
        width: 40px; height: 40px; border-radius: 50%; border: 2px solid #555;
        display: flex; justify-content: center; align-items: center;
        font-weight: 700; font-size: 16px; color: #aaa; background-color: #262626;
        margin-bottom: 10px; z-index: 2; transition: 0.3s;
    }
    .step-label { font-size: 13px; font-weight: 600; color: #888; text-align: center; }
    .step-line { height: 2px; width: 60px; background-color: #444; margin-top: 20px; }
    .step-item.active .step-circle { border-color: #ffffff; background-color: #ffffff; color: #000000; }
    .step-item.active .step-label { color: #ffffff; }
    .step-item.completed .step-circle { border-color: #894b9d; background-color: #894b9d; color: white; }
    .step-item.completed .step-label { color: #894b9d; }
    .line-completed { background-color: #894b9d; }

    /* --- CARDS --- */
    .option-card {
        background: #262626; border: 1px solid #444; border-radius: 12px;
        padding: 40px 20px; text-align: center; min-height: 250px;
        display: flex; flex-direction: column; justify-content: center;
        margin-bottom: 15px; 
    }
    .option-card:hover { border-color: #894b9d; background: #2e2e2e; transition: 0.3s;}
    
    /* --- BUTTONS & FORMS --- */
    div.stButton > button { background: #894b9d; color: white; border: none; border-radius: 30px; padding: 12px 28px; width: 100%; font-weight: bold;}
    div.stButton > button:hover { background: #723e83; color: white; }
    div[data-testid="stCheckbox"] { display: flex; justify-content: center; margin-bottom: 20px;}
    div[data-baseweb="input"] { background-color: #333; border-radius: 8px; }
    div[data-baseweb="input"] input { color: white; }
    label { color: #ccc !important; font-weight: 600; }
    
    /* Zorg dat de radio buttons (toggles) en sub-checkboxes in stap 2 links uitlijnen */
    .step2-panel div[data-testid="stCheckbox"] { justify-content: flex-start; margin-bottom: 5px;}
    </style>
    
    <div class="navbar">
        <div class="nav-logo">
            <a href="?reset=true" target="_self" title="Go back to Step 1">
                <img src="https://cloud-1de12d.becdn.net/media/original/964295c9ae8e693f8bb4d6b70862c2be/logo-website-top-png-1-.webp" alt="Dahle Transport Logo">
            </a>
        </div>
        <div class="nav-links">
            <span>Home</span><span>About Us</span><span>Services</span><span>Gallery</span><span>Contact</span>
        </div>
        <div class="nav-cta">
            <a class="cta-btn">CONTACT US</a>
        </div>
    </div>
""", unsafe_allow_html=True)

# =========================================================
# DE WEBSITE LOGICA
# =========================================================

col_spacer_L, col_main, col_spacer_R = st.columns([1, 6, 1])

with col_main:
    
    # --- DYNAMISCHE STEP TRACKER ---
    s = st.session_state.step
    def get_class(step_num):
        if s > step_num: return "completed"
        elif s == step_num: return "active"
        return "inactive"
        
    line_1 = "line-completed" if s > 1 else ""
    line_2 = "line-completed" if s > 2 else ""

    tracker_html = f"""
    <div class="step-wrapper">
        <div class="step-item {get_class(1)}">
            <div class="step-circle">1</div><div class="step-label">Shipment</div>
        </div>
        <div class="step-line {line_1}"></div>
        <div class="step-item {get_class(2)}">
            <div class="step-circle">2</div><div class="step-label">Details</div>
        </div>
        <div class="step-line {line_2}"></div>
        <div class="step-item {get_class(3)}">
            <div class="step-circle">3</div><div class="step-label">Review</div>
        </div>
    </div>
    """
    st.markdown(tracker_html, unsafe_allow_html=True)

    # --- STAP 1: KEUZE ---
    if st.session_state.step == 1:
        st.markdown("<h3 style='text-align: center; margin-bottom: 5px;'>To find your service match, select all that you ship on a regular basis.</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #888; margin-bottom: 40px;'>Select at least one option to continue</p>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown('<div class="option-card"><h1>📦</h1><h3>Parcels & Documents</h3><p>Light to medium weight shipments (B2B/B2C)</p></div>', unsafe_allow_html=True)
            check_parcels = st.checkbox("Select Parcels & Documents")
        with c2:
            st.markdown('<div class="option-card"><h1>🚛</h1><h3>Cargo & Freight</h3><p>Heavier shipments using pallets or containers (B2B)</p></div>', unsafe_allow_html=True)
            check_freight = st.checkbox("Select Cargo & Freight")
        with c3:
            st.markdown('<div class="option-card"><h1>✉️</h1><h3>Mail & Direct Marketing</h3><p>Lightweight goods & international business mail</p></div>', unsafe_allow_html=True)
            check_mail = st.checkbox("Select Mail & Marketing")

        st.markdown("---")
        
        c_btn1, c_btn2, c_btn3 = st.columns([1, 2, 1])
        with c_btn2:
            if st.button("Next Step", use_container_width=True):
                selected = []
                if check_parcels: selected.append("Parcels & Documents")
                if check_freight: selected.append("Cargo & Freight")
                if check_mail: selected.append("Mail & Direct Marketing")
                
                if len(selected) == 0:
                    st.error("❌ Please select at least one option.")
                else:
                    st.session_state.selected_types = selected
                    st.session_state.step = 2
                    st.rerun()

    # --- STAP 2: DYNAMISCHE DETAILS (ZOALS DE FOTO) ---
    elif st.session_state.step == 2:
        with st.form("shipment_form"):
            st.markdown("<div class='step2-panel'>", unsafe_allow_html=True)
            
            # Maak dynamisch het aantal kolommen aan op basis van de selectie!
            aantal_geselecteerd = len(st.session_state.selected_types)
            cols = st.columns(aantal_geselecteerd)
            
            # Vul elke kolom met de specifieke vragen voor dat type
            for i, sel in enumerate(st.session_state.selected_types):
                with cols[i]:
                    with st.container(border=True):
                        if sel == "Parcels & Documents":
                            st.markdown("#### 📦 Parcels & Documents")
                            st.text_input("Average Number of Shipments *", key="pd_avg")
                            st.radio("Shipping frequency *", ["Daily", "Weekly", "Monthly"], horizontal=True, key="pd_freq")
                            st.markdown("**Where do you ship? ***")
                            st.checkbox("Domestic (within the country)", key="pd_dom")
                            st.checkbox("Pan-European (within the continent)", key="pd_pan")
                            st.checkbox("Worldwide (beyond the continent)", key="pd_world")
                            
                        elif sel == "Cargo & Freight":
                            st.markdown("#### 🚛 Cargo & Freight")
                            st.radio("Shipping Type *", ["One-off", "Recurring Shipment"], horizontal=True, key="cf_type")
                            st.markdown("**Load Type ***")
                            st.checkbox("Pallet", key="cf_pal")
                            st.checkbox("Full Container/Truck Load", key="cf_full")
                            st.checkbox("Loose Cargo", key="cf_lc")
                            st.text_input("Average Number of Shipments per Year *", key="cf_avg")
                            st.markdown("**Where do you ship? ***")
                            st.checkbox("Domestic", key="cf_dom")
                            st.checkbox("Pan-European", key="cf_pan")
                            st.checkbox("Worldwide", key="cf_world")
                            
                        elif sel == "Mail & Direct Marketing":
                            st.markdown("#### ✉️ Mail & Direct Marketing")
                            st.text_input("Average Number of Shipments *", key="mdm_avg")
                            st.radio("Shipping frequency *", ["Daily", "Weekly", "Monthly"], horizontal=True, key="mdm_freq")
                            st.markdown("**Where do you ship? ***")
                            st.checkbox("Pan-European", key="mdm_pan")
                            st.checkbox("Worldwide", key="mdm_world")
                            st.caption("Our business accounts for Mail & Direct Marketing currently service international shipments only.")
                            
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("### General Contact Details")
            c_form1, c_form2 = st.columns(2)
            with c_form1:
                company = st.text_input("Company Name *")
                email = st.text_input("Email *")
            with c_form2:
                route = st.text_input("Route (e.g. Oslo -> Bergen) *")
                weight = st.number_input("Total Est. Weight (kg)", min_value=1)
            
            st.markdown("---")
            c_back, c_next = st.columns([1, 4])
            back = c_back.form_submit_button("← Back")
            submit = c_next.form_submit_button("Continue to Review →")
            
            if back:
                st.session_state.step = 1
                st.rerun()
            
            if submit:
                if not company or not email or not route:
                    st.error("⚠️ Please fill in all General Contact Details before continuing.")
                else:
                    st.session_state.temp_order = {
                        "company": company, "email": email,
                        "route": route, "weight": weight, 
                        "types": st.session_state.selected_types
                    }
                    st.session_state.step = 3
                    st.rerun()

    # --- STAP 3: REVIEW ---
    elif st.session_state.step == 3:
        o = st.session_state.temp_order
        with st.container(border=True):
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                st.write(f"**Customer:** {o['company']}")
                st.write(f"**Email:** {o['email']}")
                st.write(f"**Shipment Types:** {', '.join(o['types'])}")
            with col_s2:
                st.write(f"**Route:** {o['route']}")
                st.write(f"**Total Weight:** {o['weight']} kg")
        
        st.write("")
        c_b1, c_b2 = st.columns([1, 4])
        with c_b1:
            if st.button("← Edit"):
                st.session_state.step = 2
                st.rerun()
        with c_b2:
            if st.button("✅ CONFIRM & SEND REQUEST"):
                new_order = o.copy()
                new_order['id'] = len(st.session_state.orders) + 1001
                new_order['date'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                new_order['status'] = "New"
                new_order['type'] = ", ".join(o['types']) 
                
                st.session_state.orders.append(new_order)
                st.balloons()
                st.success("Your transport request has been sent successfully!")
                time.sleep(2.5)
                st.session_state.step = 1
                st.session_state.selected_types = []
                st.rerun()

    # =========================================================
    # DE DEMO KNOP NAAR DE PLANNER
    # =========================================================
    st.write("")
    st.write("")
    st.markdown("---")
    
    st.page_link("pages/Planner.py", label="🔒 Open Internal Planner System", icon="⚙️")
