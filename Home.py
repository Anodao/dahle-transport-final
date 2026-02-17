import streamlit as st
import time
from datetime import datetime
from supabase import create_client, Client

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Dahle Transport - Home",
    page_icon="🚚",
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
    st.error("⚠️ Database connection failed. Please check the Secrets settings in your Streamlit Cloud dashboard.")

# --- LOGO RESET TRUCJE ---
if "reset" in st.query_params:
    st.session_state.step = 1
    st.session_state.selected_types = [] 
    st.session_state.temp_order = {}
    st.session_state.chk_parcels = False
    st.session_state.chk_freight = False
    st.session_state.chk_mail = False
    st.session_state.show_error = False
    st.session_state.is_submitted = False
    st.session_state.validate_step2 = False
    st.session_state.scroll_up = False
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
if 'order_counter' not in st.session_state: st.session_state.order_counter = 1000
if 'is_submitted' not in st.session_state: st.session_state.is_submitted = False
if 'validate_step2' not in st.session_state: st.session_state.validate_step2 = False
if 'scroll_up' not in st.session_state: st.session_state.scroll_up = False

# --- CSS STYLING GLOBAL & NAVBAR HTML ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }

    /* --- HEADER & SIDEBAR FIX --- */
    [data-testid="collapsedControl"] { display: none !important; }
    [data-testid="stSidebar"] { display: none !important; }
    header[data-testid="stHeader"] { background: transparent !important; pointer-events: none !important; display: none !important;}
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
    div[data-baseweb="input"], div[data-baseweb="select"], div[data-baseweb="textarea"] { background-color: #333; border-radius: 8px; }
    div[data-baseweb="input"] input, div[data-baseweb="textarea"] textarea { color: white; }
    label { color: #ccc !important; font-weight: 600; font-size: 14px !important;}
    
    /* Dropdown text kleur fix */
    div[data-baseweb="select"] div { color: white; background-color: #333;}
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
    # STAP 1: KEUZE 
    # =========================================================
    if st.session_state.step == 1:
        st.markdown("""
        <style>
        div[data-testid="stVerticalBlockBorderWrapper"] {
            position: relative !important; border-radius: 12px !important; transition: all 0.3s ease !important;
            background-color: #262626 !important; border: 2px solid #444 !important; padding: 25px !important; height: 100%;
        }
        div[data-testid="stVerticalBlockBorderWrapper"]:hover {
            border-color: #894b9d !important; background-color: #2e2e2e !important; transform: translateY(-5px);
        }
        div[data-testid="stVerticalBlockBorderWrapper"]:has(input[type="checkbox"]:checked) {
            border-color: #894b9d !important; background-color: #2e2e2e !important;
        }
        div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stCheckbox"] label::after {
            content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%; cursor: pointer; z-index: 10;
        }
        div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stCheckbox"] { margin-bottom: 5px; padding-top: 0px; }
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
        
        with c1:
            with st.container(border=True):
                st.checkbox("Parcels & Documents", key="chk_parcels")
                st.markdown("""
                    <span style="display: inline-block; padding: 4px 12px; border: 1px solid #666; border-radius: 20px; font-size: 12px; color: #ccc; margin-bottom: 20px;">Typically up to 31.5kg</span>
                    <ul style="font-size: 14px; color: #bbb; line-height: 1.6; padding-left: 20px; margin-bottom: 30px; min-height: 80px;">
                        <li>Light to medium weight shipments</li><li>B2B/B2C</li>
                    </ul>
                    <div style="text-align: center; font-size: 12px; color: #aaa; border-top: 1px solid #444; padding-top: 20px; margin-top: 30px;">
                        Commonly shipped items:
                        <div style="font-size: 32px; margin-top: 10px; display: flex; gap: 20px; justify-content: center;">✉️ 📦 📚</div>
                    </div>
                """, unsafe_allow_html=True)

        with c2:
            with st.container(border=True):
                st.checkbox("Cargo & Freight", key="chk_freight")
                st.markdown("""
                    <span style="display: inline-block; padding: 4px 12px; border: 1px solid #666; border-radius: 20px; font-size: 12px; color: #ccc; margin-bottom: 20px;">Typically over 31.5kg+</span>
                    <ul style="font-size: 14px; color: #bbb; line-height: 1.6; padding-left: 20px; margin-bottom: 30px; min-height: 80px;">
                        <li>Heavier shipments using pallets or containers</li><li>B2B</li>
                    </ul>
                    <div style="text-align: center; font-size: 12px; color: #aaa; border-top: 1px solid #444; padding-top: 20px; margin-top: 30px;">
                        Commonly shipped items:
                        <div style="font-size: 32px; margin-top: 10px; display: flex; gap: 20px; justify-content: center;">🚛 🏗️</div>
                    </div>
                """, unsafe_allow_html=True)

        with c3:
            with st.container(border=True):
                st.checkbox("Mail & Marketing", key="chk_mail")
                st.markdown("""
                    <span style="display: inline-block; padding: 4px 12px; border: 1px solid #666; border-radius: 20px; font-size: 12px; color: #ccc; margin-bottom: 20px;">Typically up to 2kg</span>
                    <ul style="font-size: 14px; color: #bbb; line-height: 1.6; padding-left: 20px; margin-bottom: 30px; min-height: 80px;">
                        <li>Lightweight goods</li><li>International business mail (letters, brochures, books)</li>
                    </ul>
                    <div style="text-align: center; font-size: 12px; color: #aaa; border-top: 1px solid #444; padding-top: 20px; margin-top: 30px;">
                        Commonly shipped items:
                        <div style="font-size: 32px; margin-top: 10px; display: flex; gap: 20px; justify-content: center;">📭 📄</div>
                    </div>
                """, unsafe_allow_html=True)

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
    # STAP 2: DYNAMISCHE DETAILS + CONTACT FORMULIER
    # =========================================================
    elif st.session_state.step == 2:
        
        # --- VERBORGEN ANKER OM NAARTOE TE SCROLLEN ---
        st.markdown("<div id='error-top'></div>", unsafe_allow_html=True)
        
        # --- JAVASCRIPT VOOR AUTO-SCROLL (VOERT UIT ALS SCROLL_UP TRUE IS) ---
        if st.session_state.get('scroll_up', False):
            st.components.v1.html(
                """
                <script>
                    const doc = window.parent.document;
                    const el = doc.getElementById("error-top");
                    if(el) {
                        el.scrollIntoView({behavior: "smooth"});
                    }
                </script>
                """, height=0
            )
            st.session_state.scroll_up = False # Reset direct na het scrollen
            
        st.markdown("""
        <style>
        .step2-panel div[data-testid="stCheckbox"] { justify-content: flex-start; margin-bottom: 5px; position: static; height: auto;}
        .step2-panel div[data-testid="stCheckbox"] label { display: flex; width: auto; height: auto;}
        .step2-panel div[data-testid="stCheckbox"] label span[role="checkbox"] { position: static; transform: scale(1.0); margin-right: 10px; border-width: 1px;}
        .step2-panel div[data-testid="stCheckbox"] label p { display: block; font-size: 14px !important; }
        .step2-panel button[kind="tertiary"] { color: #888 !important; padding: 0px !important; min-height: 0px !important; margin-top: 15px !important; font-size: 16px !important; }
        .step2-panel button[kind="tertiary"]:hover { color: #ff4b4b !important; background-color: transparent !important; }
        .step2-panel div[role="radiogroup"] { gap: 0.5rem; }
        </style>
        """, unsafe_allow_html=True)
        
        # --- HIGHLIGHT FUNCTIES ---
        def req_lbl(key, base_text):
            if st.session_state.get('validate_step2', False):
                val = st.session_state.get(key, "")
                if not val or not str(val).strip():
                    return f"{base_text} 🚨 :red[(Required)]"
            return base_text

        def email_lbl():
            base = "Work Email *"
            if st.session_state.get('validate_step2', False):
                val = st.session_state.get('cont_email', "")
                if not val or not str(val).strip():
                    return f"{base} 🚨 :red[(Required)]"
                elif "@" not in str(val):
                    return f"{base} 🚨 :red[(Missing '@')]"
            return base

        st.markdown("<div class='step2-panel'>", unsafe_allow_html=True)
        
        if not st.session_state.selected_types:
             st.session_state.step = 1
             st.rerun()

        aantal_geselecteerd = len(st.session_state.selected_types)
        cols = st.columns(aantal_geselecteerd)
        
        pd_avg_val = ""
        cf_avg_val = ""
        cf_pal_val = False
        cf_full_val = False
        cf_lc_val = False
        mdm_avg_val = ""
        
        for i, sel in enumerate(st.session_state.selected_types[:]):
            with cols[i]:
                with st.container(border=True):
                    c_title, c_close = st.columns([8, 1])
                    with c_title: st.markdown(f"#### {sel}")
                    with c_close:
                        if st.button("✖", key=f"btn_close_{sel}", help=f"Remove {sel}", type="tertiary"):
                            st.session_state.selected_types.remove(sel)
                            if sel == "Parcels & Documents": st.session_state.chk_parcels = False
                            if sel == "Cargo & Freight": st.session_state.chk_freight = False
                            if sel == "Mail & Direct Marketing": st.session_state.chk_mail = False
                            st.session_state.validate_step2 = False
                            st.rerun() 

                    if sel == "Parcels & Documents":
                        pd_avg_val = st.text_input(req_lbl("pd_avg", "Average Number of Shipments *"), key="pd_avg", max_chars=50)
                        st.radio("Shipping frequency *", ["One-time shipment", "Daily", "Weekly", "Monthly"], horizontal=True, key="pd_freq")
                        st.radio("**Where do you ship? *** (Select one)", 
                                 options=["Domestic", "Pan-European", "Worldwide"], 
                                 captions=["within the country", "within the continent", "beyond the continent"],
                                 key="pd_ship_where")
                        
                    elif sel == "Cargo & Freight":
                        st.radio("Shipping Type *", ["One-time shipment", "Recurring Shipment"], horizontal=True, key="cf_type")
                        
                        cf_lbl = "**Load Type ***"
                        if st.session_state.get('validate_step2', False) and not (st.session_state.get('cf_pal') or st.session_state.get('cf_full') or st.session_state.get('cf_lc')):
                            cf_lbl += " 🚨 :red[(Select at least one)]"
                        st.markdown(cf_lbl)
                        
                        cf_pal_val = st.checkbox("Pallet", key="cf_pal")
                        cf_full_val = st.checkbox("Full Container/Truck Load", key="cf_full")
                        cf_lc_val = st.checkbox("Loose Cargo", key="cf_lc")
                        
                        cf_avg_val = st.text_input(req_lbl("cf_avg", "Avg. Shipments per Year *"), key="cf_avg", max_chars=50)
                        st.radio("**Where do you ship? *** (Select one)", 
                                 options=["Domestic", "Pan-European", "Worldwide"], 
                                 captions=["within the country", "within the continent", "beyond the continent"],
                                 key="cf_ship_where")
                        
                    elif sel == "Mail & Direct Marketing":
                        mdm_avg_val = st.text_input(req_lbl("mdm_avg", "Average Number of Shipments *"), key="mdm_avg", max_chars=50)
                        st.radio("Shipping frequency *", ["One-time shipment", "Daily", "Weekly", "Monthly"], horizontal=True, key="mdm_freq")
                        st.radio("**Where do you ship? *** (Select one)", 
                                 options=["Pan-European", "Worldwide"], 
                                 captions=["within the continent", "beyond the continent"],
                                 key="mdm_ship_where")
                        st.caption("Our business accounts for Mail & Direct Marketing currently service international shipments only.")
                        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        st.markdown("<h3 style='text-align: center; margin-bottom: 5px;'>Send us your contact information and we will get in touch.</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #888; font-size: 14px; margin-bottom: 40px;'>All fields marked with an asterisk (*) are mandatory</p>", unsafe_allow_html=True)
        
        c_form_left, c_form_right = st.columns(2, gap="large")
        
        with c_form_left:
            st.markdown("#### Company Details")
            company_name = st.text_input(req_lbl("comp_name", "Company Name *"), key="comp_name", max_chars=100)
            company_reg = st.text_input("Company Registration No. (optional)", key="comp_reg", max_chars=50)
            company_address = st.text_input(req_lbl("comp_addr", "Company Address *"), key="comp_addr", max_chars=150)
            c_pc, c_city = st.columns(2)
            with c_pc: postal_code = st.text_input(req_lbl("comp_pc", "Postal Code *"), key="comp_pc", max_chars=20)
            with c_city: city = st.text_input(req_lbl("comp_city", "City *"), key="comp_city", max_chars=100)
            country = st.text_input(req_lbl("comp_country", "Country *"), value="Norway", key="comp_country", max_chars=100)

        with c_form_right:
            st.markdown("#### Contact Person")
            c_fn, c_ln = st.columns(2)
            with c_fn: first_name = st.text_input(req_lbl("cont_fn", "First Name *"), key="cont_fn", max_chars=50)
            with c_ln: last_name = st.text_input(req_lbl("cont_ln", "Last Name *"), key="cont_ln", max_chars=50)
            
            work_email = st.text_input(email_lbl(), placeholder="example@email.no", key="cont_email", max_chars=150)
            
            phone_lbl = "Phone *"
            if st.session_state.get('validate_step2', False) and not st.session_state.get('cont_phone', '').strip():
                phone_lbl += " 🚨 <span style='color:#ff4b4b;'>(Required)</span>"
            st.markdown(f"<label style='font-size: 14px; font-weight: 600; color: #ccc;'>{phone_lbl}</label>", unsafe_allow_html=True)
            
            c_code, c_phone = st.columns([1, 3])
            with c_code: 
                phone_code = st.selectbox("Code", ["+47", "+46", "+45", "+31", "+44"], label_visibility="collapsed", key="cont_code")
            with c_phone: 
                phone = st.text_input("Phone", placeholder="e.g. 123 456 789", label_visibility="collapsed", key="cont_phone", max_chars=20)
            
            additional_info = st.text_area("Additional Information (optional)", placeholder="Describe what you ship, approx. weight, any special requirements, etc.", max_chars=300, key="cont_info")

        st.write("")
        st.markdown("<p style='text-align: center; color: #888; font-size: 13px; margin-bottom: 30px;'>If you would like to learn more about how Dahle Transport uses your personal data, please read our privacy notice which you can find in the footer.</p>", unsafe_allow_html=True)
        
        error_container = st.empty()
        missing_fields = False
        
        if not company_name.strip() or not company_address.strip() or not postal_code.strip() or not city.strip() or not first_name.strip() or not last_name.strip() or not work_email.strip() or not phone.strip() or not country.strip():
            missing_fields = True
            
        if "Parcels & Documents" in st.session_state.selected_types and not pd_avg_val.strip():
            missing_fields = True
        
        if "Cargo & Freight" in st.session_state.selected_types:
            if not cf_avg_val.strip() or not (cf_pal_val or cf_full_val or cf_lc_val):
                missing_fields = True
                
        if "Mail & Direct Marketing" in st.session_state.selected_types and not mdm_avg_val.strip():
            missing_fields = True

        invalid_email = bool(work_email.strip() and "@" not in work_email)

        if st.session_state.get('validate_step2', False):
            if missing_fields:
                error_container.error("⚠️ Please fill in all highlighted mandatory fields (*) before continuing.")
            elif invalid_email:
                error_container.error("⚠️ Please enter a valid email address containing an '@' symbol.")

        c_back, c_next = st.columns([1, 4])
        if c_back.button("← Go Back"):
            st.session_state.step = 1
            st.session_state.validate_step2 = False 
            st.rerun()
            
        if c_next.button("Continue to Review →"):
            st.session_state.validate_step2 = True 
            
            if missing_fields or invalid_email:
                # --- HIER WORDT DE SCROLL TRIGGER GEZET ALS DE VALIDATIE FAALT ---
                st.session_state.scroll_up = True
                st.rerun()
            else:
                st.session_state.validate_step2 = False 
                st.session_state.scroll_up = False
                
                compiled_info = additional_info + "\n\n--- Order Specifications ---\n" if additional_info else "--- Order Specifications ---\n"
                
                if "Parcels & Documents" in st.session_state.selected_types:
                    compiled_info += f"📦 Parcels: {pd_avg_val} shipments ({st.session_state.pd_freq}) to {st.session_state.pd_ship_where}.\n"
                
                if "Cargo & Freight" in st.session_state.selected_types:
                    loads = []
                    if cf_pal_val: loads.append("Pallet")
                    if cf_full_val: loads.append("Full Container")
                    if cf_lc_val: loads.append("Loose Cargo")
                    compiled_info += f"🚛 Freight: {st.session_state.cf_type}, {cf_avg_val} shipments/yr. Load: {', '.join(loads)} to {st.session_state.cf_ship_where}.\n"
                
                if "Mail & Direct Marketing" in st.session_state.selected_types:
                    compiled_info += f"📭 Mail: {mdm_avg_val} shipments ({st.session_state.mdm_freq}) to {st.session_state.mdm_ship_where}.\n"
                
                st.session_state.temp_order = {
                    "company": company_name, 
                    "reg_no": company_reg,
                    "address": f"{company_address}, {postal_code} {city}, {country}",
                    "contact_name": f"{first_name} {last_name}",
                    "email": work_email,
                    "phone": f"{phone_code} {phone}",
                    "info": compiled_info,
                    "types": st.session_state.selected_types
                }
                st.session_state.step = 3
                st.rerun()

    # =========================================================
    # STAP 3: REVIEW (OPSLAAN IN SUPABASE!)
    # =========================================================
    elif st.session_state.step == 3:
        o = st.session_state.temp_order
        with st.container(border=True):
            st.markdown("#### Review your request")
            st.markdown("---")
            
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                st.write(f"**Company Name:** {o['company']}")
                if o['reg_no']: st.write(f"**Registration No:** {o['reg_no']}")
                st.write(f"**Address:** {o['address']}")
                st.write("")
                st.write(f"**Selected Services:**")
                for s_type in o['types']:
                    st.write(f"- {s_type}")
                    
            with col_s2:
                st.write(f"**Contact Person:** {o['contact_name']}")
                st.write(f"**Email:** {o['email']}")
                st.write(f"**Phone:** {o['phone']}")
                if o['info'] and o['info'] != "--- Order Specifications ---\n":
                    st.write("")
                    st.write(f"**Additional Information & Specifications:**")
                    st.write(f"_{o['info']}_")
        
        st.write("")
        
        if not st.session_state.is_submitted:
            c_b1, c_b2 = st.columns([1, 4])
            with c_b1:
                if st.button("← Edit Details"):
                    st.session_state.step = 2
                    st.rerun()
            with c_b2:
                if st.button("✅ CONFIRM & SEND REQUEST"):
                    
                    db_order = {
                        "company": o['company'],
                        "reg_no": o['reg_no'],
                        "address": o['address'],
                        "contact_name": o['contact_name'],
                        "email": o['email'],
                        "phone": o['phone'],
                        "info": o['info'],
                        "types": ", ".join(o['types']),
                        "status": "New",
                        "received_date": datetime.now().strftime("%Y-%m-%d %H:%M")
                    }
                    
                    try:
                        supabase.table("orders").insert(db_order).execute()
                        st.balloons()
                        st.session_state.is_submitted = True
                        st.rerun()
                    except Exception as e:
                        st.error("⚠️ Failed to send order to the database. Please try again later.")
                        
        else:
            st.success("🎉 Your transport request has been sent successfully! We will get in touch shortly.")
            st.info("You can review your submitted details above.")
            
            if st.button("← Start a New Request"):
                st.session_state.step = 1
                st.session_state.is_submitted = False
                st.session_state.validate_step2 = False
                st.session_state.scroll_up = False
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
