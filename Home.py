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
    st.session_state.chk_parcels = False
    st.session_state.chk_freight = False
    st.session_state.chk_mail = False
    st.session_state.show_error = False
    st.query_params.clear()

# --- SESSION STATE ---
if 'orders' not in st.session_state: st.session_state.orders = []
if 'step' not in st.session_state: st.session_state.step = 1
if 'selected_types' not in st.session_state: st.session_state.selected_types = []
if 'temp_order' not in st.session_state: st.session_state.temp_order = {}
if 'chk_parcels' not in st.session_state: st.session_state.chk_parcels = False
if 'chk_freight' not in st.session_state: st.session_state.chk_freight = False
if 'chk_mail' not in st.session_state: st.session_state.chk_mail = False
if 'show_error' not in st.session_state: st.session_state.show_error = False

# --- CSS STYLING GLOBAL ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }

    /* --- HEADER & SIDEBAR FIX --- */
    header[data-testid="stHeader"] { background: transparent !important; pointer-events: none !important; }
    div[data-testid="stDecoration"] { display: none; }
    div[data-testid="stToolbar"] { display: none; }
    button[kind="header"] { color: #000 !important; margin-top: 5px; pointer-events: auto !important; }
    footer { visibility: hidden; }
    
    /* --- NAVBAR --- */
    .block-container { padding-top: 110px; }
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

    /* --- STEP TRACKER --- */
    .step-wrapper { display: flex; justify-content: center; align-items: flex-start; margin-bottom: 30px; margin-top: 10px; gap: 15px; }
    .step-item { display: flex; flex-direction: column; align-items: center; width: 80px; }
    .step-circle {
        width: 40px; height: 40px; border-radius: 50%; border: 2px solid #555; display: flex; justify-content: center; align-items: center;
        font-weight: 700; font-size: 16px; color: #aaa; background-color: #262626; margin-bottom: 10px; z-index: 2; transition: 0.3s;
    }
    .step-label { font-size: 13px; font-weight: 600; color: #888; text-align: center; }
    .step-line { height: 2px; width: 60px; background-color: #444; margin-top: 20px; }
    .step-item.active .step-circle { border-color: #ffffff; background-color: #ffffff; color: #000000; }
    .step-item.active .step-label { color: #ffffff; }
    .step-item.completed .step-circle { border-color: #894b9d; background-color: #894b9d; color: white; }
    .step-item.completed .step-label { color: #894b9d; }
    .line-completed { background-color: #894b9d; }

    /* --- ALGEMENE FORMS & BUTTONS --- */
    div.stButton > button[kind="primary"], div.stButton > button[kind="secondary"] { 
        background: #894b9d !important; color: white !important; border: none; border-radius: 6px; 
        padding: 10px 28px; width: 100%; font-weight: bold;
    }
    div.stButton > button[kind="primary"]:hover, div.stButton > button[kind="secondary"]:hover { 
        background: #723e83 !important; color: white !important; 
    }
    div[data-baseweb="input"] { background-color: #333; border-radius: 8px; }
    div[data-baseweb="input"] input { color: white; }
    label { color: #ccc !important; font-weight: 600; }
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

    # =========================================================
    # STAP 1: KEUZE (VOLLEDIG KLIKBARE KAARTEN)
    # =========================================================
    if st.session_state.step == 1:
        
        # CSS speciaal voor de kaarten in Stap 1
        st.markdown("""
        <style>
        /* 1. De boxen opmaken als echte kaarten */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            position: relative !important;
            border-radius: 12px !important;
            transition: all 0.3s ease !important;
            background-color: #262626 !important;
            border: 2px solid #444 !important;
            padding: 25px !important; /* Iets meer padding voor een luchtiger gevoel */
            height: 100%;
        }
        
        /* 2. Hover effect (kaart komt iets omhoog) */
        div[data-testid="stVerticalBlockBorderWrapper"]:hover {
            border-color: #894b9d !important;
            background-color: #2e2e2e !important;
            transform: translateY(-5px);
        }
        
        /* 3. Als het vinkje aan staat, licht de héle box paars op! */
        div[data-testid="stVerticalBlockBorderWrapper"]:has(input[type="checkbox"]:checked) {
            border-color: #894b9d !important;
            background-color: #2e2e2e !important;
        }
        
        /* 4. MAGIC TRICK: Maak de héle box klikbaar */
        div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stCheckbox"] label::after {
            content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%; cursor: pointer; z-index: 10;
        }
        
        /* 5. Maak het vinkje zelf groot en stijl het als de titel van de kaart */
        div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stCheckbox"] {
            margin-bottom: 5px; padding-top: 0px;
        }
        div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stCheckbox"] label span[role="checkbox"] {
            transform: scale(1.6); margin-right: 15px; border-color: #888;
        }
        div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stCheckbox"] label p {
            font-size: 20px !important; font-weight: 700 !important; color: white !important;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown("<h3 style='text-align: center; margin-bottom: 5px;'>To find your service match, select all that you ship on a regular basis.</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #888; margin-bottom: 30px;'>Select at least one option to continue</p>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        
        # KAART 1: Parcels (GEÜPDATETE FOOTER)
        with c1:
            with st.container(border=True):
                st.checkbox("Parcels & Documents", key="chk_parcels")
                st.markdown("""
                    <span style="display: inline-block; padding: 4px 12px; border: 1px solid #666; border-radius: 20px; font-size: 12px; color: #ccc; margin-bottom: 20px;">Typically up to 31.5kg</span>
                    <ul style="font-size: 14px; color: #bbb; line-height: 1.6; padding-left: 20px; margin-bottom: 30px; min-height: 80px;">
                        <li>Light to medium weight shipments</li>
                        <li>B2B/B2C</li>
                    </ul>
                    <div style="text-align: center; font-size: 12px; color: #aaa; border-top: 1px solid #444; padding-top: 20px; margin-top: 30px;">
                        Commonly shipped items:
                        <div style="font-size: 32px; margin-top: 10px; display: flex; gap: 20px; justify-content: center;">✉️ 📦 📚</div>
                    </div>
                """, unsafe_allow_html=True)

        # KAART 2: Freight (GEÜPDATETE FOOTER)
        with c2:
            with st.container(border=True):
                st.checkbox("Cargo & Freight", key="chk_freight")
                st.markdown("""
                    <span style="display: inline-block; padding: 4px 12px; border: 1px solid #666; border-radius: 20px; font-size: 12px; color: #ccc; margin-bottom: 20px;">Typically over 31.5kg+</span>
                    <ul style="font-size: 14px; color: #bbb; line-height: 1.6; padding-left: 20px; margin-bottom: 30px; min-height: 80px;">
                        <li>Heavier shipments using pallets or containers</li>
                        <li>B2B</li>
                    </ul>
                    <div style="text-align: center; font-size: 12px; color: #aaa; border-top: 1px solid #444; padding-top: 20px; margin-top: 30px;">
                        Commonly shipped items:
                        <div style="font-size: 32px; margin-top: 10px; display: flex; gap: 20px; justify-content: center;">🚛 🏗️</div>
                    </div>
                """, unsafe_allow_html=True)

        # KAART 3: Mail (GEÜPDATETE FOOTER)
        with c3:
            with st.container(border=True):
                st.checkbox("Mail & Marketing", key="chk_mail")
                st.markdown("""
                    <span style="display: inline-block; padding: 4px 12px; border: 1px solid #666; border-radius: 20px; font-size: 12px; color: #ccc; margin-bottom: 20px;">Typically up to 2kg</span>
                    <ul style="font-size: 14px; color: #bbb; line-height: 1.6; padding-left: 20px; margin-bottom: 30px; min-height: 80px;">
                        <li>Lightweight goods</li>
                        <li>International business mail (letters, brochures, books)</li>
                    </ul>
                    <div style="text-align: center; font-size: 12px; color: #aaa; border-top: 1px solid #444; padding-top: 20px; margin-top: 30px;">
                        Commonly shipped items:
                        <div style="font-size: 32px; margin-top: 10px; display: flex; gap: 20px; justify-content: center;">📭 📄</div>
                    </div>
                """, unsafe_allow_html=True)

        # --- FOUTMELDING & KNOP ---
        if st.session_state.show_error:
            st.markdown("<p style='text-align: center; color: #ff4b4b; font-weight: bold; margin-top: 20px;'>❌ Please select at least one option.</p>", unsafe_allow_html=True)
        else:
            st.write("") 
            
        st.markdown("<p style='text-align: center; color: #888; font-size: 13px; margin-bottom: 15px;'>⏱ Typically takes less than 5 minutes.</p>", unsafe_allow_html=True)
        
        c_btn1, c_btn2, c_btn3 = st.columns([1, 2, 1])
        with c_btn2:
            if st.button("Next Step", use_container_width=True):
                selected = []
                if st.session_state.chk_parcels: selected.append("Parcels & Documents")
                if st.session_state.chk_freight: selected.append("Cargo & Freight")
                if st.session_state.chk_mail: selected.append("Mail & Direct Marketing")
                
                if len(selected) == 0:
                    st.session_state.show_error = True
                    st.rerun()
                else:
                    st.session_state.show_error = False
                    st.session_state.selected_types = selected
                    st.session_state.step = 2
                    st.rerun()

    # =========================================================
    # STAP 2: DYNAMISCHE DETAILS
    # =========================================================
    elif st.session_state.step == 2:
        
        # CSS voor Stap 2
        st.markdown("""
        <style>
        .step2-panel div[data-testid="stCheckbox"] { justify-content: flex-start; margin-bottom: 5px; position: static; height: auto;}
        .step2-panel div[data-testid="stCheckbox"] label { display: flex; width: auto; height: auto;}
        .step2-panel div[data-testid="stCheckbox"] label span[role="checkbox"] { position: static; transform: scale(1.0); margin-right: 10px; border-width: 1px;}
        .step2-panel div[data-testid="stCheckbox"] label p { display: block; font-size: 14px !important; }

        /* STYLING VOOR DE 'X' KNOPJES IN STAP 2 */
        .step2-panel button[kind="tertiary"] {
            color: #888 !important; padding: 0px !important; min-height: 0px !important;
            margin-top: 15px !important; font-size: 16px !important;
        }
        .step2-panel button[kind="tertiary"]:hover { color: #ff4b4b !important; background-color: transparent !important; }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='step2-panel'>", unsafe_allow_html=True)
        
        if not st.session_state.selected_types:
             st.session_state.step = 1
             st.rerun()

        aantal_geselecteerd = len(st.session_state.selected_types)
        cols = st.columns(aantal_geselecteerd)
        
        for i, sel in enumerate(st.session_state.selected_types[:]):
            with cols[i]:
                with st.container(border=True):
                    # --- DE 'X' KNOP LOGICA ---
                    c_title, c_close = st.columns([8, 1])
                    with c_title:
                         st.markdown(f"#### {sel}")
                    with c_close:
                        if st.button("✖", key=f"btn_close_{sel}", help=f"Remove {sel}", type="tertiary"):
                            st.session_state.selected_types.remove(sel)
                            if sel == "Parcels & Documents": st.session_state.chk_parcels = False
                            if sel == "Cargo & Freight": st.session_state.chk_freight = False
                            if sel == "Mail & Direct Marketing": st.session_state.chk_mail = False
                            st.rerun() 

                    # --- DE VELDEN ---
                    if sel == "Parcels & Documents":
                        st.text_input("Average Number of Shipments *", key="pd_avg")
                        st.radio("Shipping frequency *", ["Daily", "Weekly", "Monthly"], horizontal=True, key="pd_freq")
                        st.markdown("**Where do you ship? ***")
                        st.checkbox("Domestic", key="pd_dom")
                        st.checkbox("Pan-European", key="pd_pan")
                        st.checkbox("Worldwide", key="pd_world")
                        
                    elif sel == "Cargo & Freight":
                        st.radio("Shipping Type *", ["One-off", "Recurring Shipment"], horizontal=True, key="cf_type")
                        st.markdown("**Load Type ***")
                        st.checkbox("Pallet", key="cf_pal")
                        st.checkbox("Full Container/Truck Load", key="cf_full")
                        st.checkbox("Loose Cargo", key="cf_lc")
                        st.text_input("Avg. Shipments per Year *", key="cf_avg")
                        st.markdown("**Where do you ship? ***")
                        st.checkbox("Domestic", key="cf_dom")
                        st.checkbox("Pan-European", key="cf_pan")
                        st.checkbox("Worldwide", key="cf_world")
                        
                    elif sel == "Mail & Direct Marketing":
                        st.text_input("Average Number of Shipments *", key="mdm_avg")
                        st.radio("Shipping frequency *", ["Daily", "Weekly", "Monthly"], horizontal=True, key="mdm_freq")
                        st.markdown("**Where do you ship? ***")
                        st.checkbox("Pan-European", key="mdm_pan")
                        st.checkbox("Worldwide", key="mdm_world")
                        st.caption("International shipments only.")
                        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### General Contact Details")
        c_form1, c_form2 = st.columns(2)
        with c_form1:
            company = st.text_input("Company Name *", key="company_name")
            email = st.text_input("Email *", key="email_address")
        with c_form2:
            route = st.text_input("Route (e.g. Oslo -> Bergen) *", key="route_info")
            weight = st.number_input("Total Est. Weight (kg)", min_value=1, key="weight_info")
        
        st.markdown("---")
        c_back, c_next = st.columns([1, 4])
        
        if c_back.button("← Back"):
            st.session_state.step = 1
            st.rerun()
            
        if c_next.button("Continue to Review →"):
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

    # =========================================================
    # STAP 3: REVIEW
    # =========================================================
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
                # Volledige reset na succes
                st.session_state.step = 1
                st.session_state.selected_types = []
                st.session_state.chk_parcels = False
                st.session_state.chk_freight = False
                st.session_state.chk_mail = False
                st.rerun()

    # =========================================================
    # DE DEMO KNOP NAAR DE PLANNER
    # =========================================================
    st.write("")
    st.write("")
    st.markdown("---")
    st.page_link("pages/Planner.py", label="🔒 Open Internal Planner System", icon="⚙️")
