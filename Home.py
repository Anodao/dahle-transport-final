import streamlit as st
from supabase import create_client
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Dahle Transport - Booking", page_icon="🚚", layout="wide", initial_sidebar_state="collapsed")

# --- SUPABASE CONNECTIE ---
@st.cache_resource
def init_connection():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

supabase = init_connection()

# --- SESSION STATE INITIALIZATION ---
if 'step' not in st.session_state:
    st.session_state.step = 1

if 'fd' not in st.session_state:
    st.session_state.fd = {
        'company_name': '', 'reg_no': '', 'address': '', 'zip': '', 'city': '', 'country': 'Norway',
        'first_name': '', 'last_name': '', 'email': '', 'phone': '', 'info': '',
        'p_address': '', 'p_zip': '', 'p_city': '',
        'd_address': '', 'd_zip': '', 'd_city': '',
        'types': []
    }

def next_step(): st.session_state.step += 1
def prev_step(): st.session_state.step -= 1
def reset_form():
    st.session_state.step = 1
    for key in st.session_state.fd.keys():
        st.session_state.fd[key] = [] if key == 'types' else ( 'Norway' if key == 'country' else '' )

# --- CSS STYLING (Jouw originele donkere thema + Cirkels) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    header[data-testid="stHeader"] { visibility: hidden; height: 0%; }
    [data-testid="stSidebar"] { display: none; }
    .block-container { padding-top: 2rem; max-width: 1200px; }
    
    .main-title { color: #ffffff; font-weight: 700; font-size: 28px; text-align: center; margin-bottom: 10px; }
    .sub-title { color: #8b949e; text-align: center; font-size: 14px; margin-bottom: 30px; }
    .section-header { color: #ffffff; font-weight: 700; font-size: 22px; margin-bottom: 15px; }
    
    /* 3 CIRCLES STEPPER CSS */
    .stepper-wrapper { display: flex; justify-content: center; align-items: center; margin-bottom: 40px; }
    .step-circle { width: 40px; height: 40px; border-radius: 50%; background-color: #30363d; color: #8b949e; display: flex; justify-content: center; align-items: center; font-weight: bold; font-size: 18px; z-index: 2; transition: 0.3s; }
    .step-circle.active { background-color: #894b9d; color: white; box-shadow: 0 0 10px rgba(137, 75, 157, 0.5); }
    .step-line { height: 4px; width: 120px; background-color: #30363d; margin: 0 -5px; z-index: 1; transition: 0.3s; }
    .step-line.active { background-color: #894b9d; }
    
    /* Knoppen (Dahle Paars) */
    div.stButton > button { background-color: #894b9d; color: white; border-radius: 6px; font-weight: bold; border: none; padding: 0.5rem 1rem;}
    div.stButton > button:hover { background-color: #723e83; }
    </style>
""", unsafe_allow_html=True)

fd = st.session_state.fd

# --- LOGO & HEADER ---
col_logo, col_title, col_empty = st.columns([1, 4, 1])
with col_logo:
    # Vervang dit door de link naar jouw echte logo!
    st.image("https://via.placeholder.com/150x80.png?text=LOGO", width=120) 
with col_title:
    st.markdown('<div class="main-title">Send us your contact information and we will get in touch.</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">All fields marked with an asterisk (*) are mandatory</div>', unsafe_allow_html=True)

# --- 3 CIRCLES PROGRESS BAR ---
step1_class = "active"
step2_class = "active" if st.session_state.step >= 2 else ""
line1_class = "active" if st.session_state.step >= 2 else ""
step3_class = "active" if st.session_state.step >= 3 else ""
line2_class = "active" if st.session_state.step >= 3 else ""

st.markdown(f"""
    <div class="stepper-wrapper">
        <div class="step-circle {step1_class}">1</div>
        <div class="step-line {line1_class}"></div>
        <div class="step-circle {step2_class}">2</div>
        <div class="step-line {line2_class}"></div>
        <div class="step-circle {step3_class}">3</div>
    </div>
""", unsafe_allow_html=True)

# =========================================================
# STAP 1: JOUW ORIGINELE LAYOUT (COMPANY & CONTACT)
# =========================================================
if st.session_state.step == 1:
    col_left, col_right = st.columns(2, gap="large")
    
    with col_left:
        st.markdown('<div class="section-header">Company Details</div>', unsafe_allow_html=True)
        fd['company_name'] = st.text_input("Company Name *", value=fd['company_name'])
        fd['reg_no'] = st.text_input("Company Registration No. (optional)", value=fd['reg_no'])
        fd['address'] = st.text_input("Company Address *", value=fd['address'])
        c_zip, c_city = st.columns(2)
        with c_zip: fd['zip'] = st.text_input("Postal Code *", value=fd['zip'])
        with c_city: fd['city'] = st.text_input("City *", value=fd['city'])
        fd['country'] = st.text_input("Country *", value=fd['country'])

    with col_right:
        st.markdown('<div class="section-header">Contact Person</div>', unsafe_allow_html=True)
        c_fn, c_ln = st.columns(2)
        with c_fn: fd['first_name'] = st.text_input("First Name *", value=fd['first_name'])
        with c_ln: fd['last_name'] = st.text_input("Last Name *", value=fd['last_name'])
        fd['email'] = st.text_input("Work Email *", value=fd['email'])
        fd['phone'] = st.text_input("Phone *", value=fd['phone'])
        fd['info'] = st.text_area("Additional Information (optional)", value=fd['info'], placeholder="Describe what you ship, approx. weight, any special requirements, etc.")

    st.write("<br>", unsafe_allow_html=True)
    c_btn1, c_btn2, _ = st.columns([1, 1, 4])
    with c_btn2:
        if st.button("Continue to Route ➔", use_container_width=True):
            next_step()
            st.rerun()

# =========================================================
# STAP 2: DE NIEUWE ROUTE INFORMATIE
# =========================================================
elif st.session_state.step == 2:
    st.markdown('<div class="section-header" style="text-align: center;">Route Information</div>', unsafe_allow_html=True)
    
    c_pick, c_del = st.columns(2, gap="large")
    with c_pick:
        st.markdown("**📤 Pickup Location**")
        fd['p_address'] = st.text_input("Pickup Address *", value=fd['p_address'])
        col_pz, col_pc = st.columns(2)
        with col_pz: fd['p_zip'] = st.text_input("Zip Code *", value=fd['p_zip'])
        with col_pc: fd['p_city'] = st.text_input("City *", value=fd['p_city'])
        
    with c_del:
        st.markdown("**📥 Delivery Destination**")
        fd['d_address'] = st.text_input("Delivery Address *", value=fd['d_address'])
        col_dz, col_dc = st.columns(2)
        with col_dz: fd['d_zip'] = st.text_input("Zip Code *", value=fd['d_zip'])
        with col_dc: fd['d_city'] = st.text_input("City *", value=fd['d_city'])

    st.write("---")
    st.markdown("**📦 Requested Services**")
    options = ["Freight", "Parcels", "Express", "Warehousing"]
    default_types = [t for t in fd['types'] if t in options]
    fd['types'] = st.multiselect("Select the services you need", options, default=default_types)

    st.write("<br>", unsafe_allow_html=True)
    c_btn1, c_btn2, _ = st.columns([1, 1, 4])
    with c_btn1:
        st.button("⬅ Go Back", on_click=prev_step, use_container_width=True)
    with c_btn2:
        if st.button("Continue to Review ➔", use_container_width=True):
            next_step()
            st.rerun()

# =========================================================
# STAP 3: REVIEW & SUBMIT
# =========================================================
elif st.session_state.step == 3:
    st.markdown('<div class="section-header" style="text-align: center;">Review & Confirm</div>', unsafe_allow_html=True)
    
    with st.container(border=True):
        c_rev1, c_rev2 = st.columns(2)
        with c_rev1:
            st.markdown(f"**🏢 Company:** {fd['company_name']}")
            st.markdown(f"**👤 Contact:** {fd['first_name']} {fd['last_name']} ({fd['email']})")
            st.markdown(f"**📦 Services:** {', '.join(fd['types']) if fd['types'] else 'Not specified'}")
        with c_rev2:
            st.markdown(f"**📤 From:** {fd['p_address']}, {fd['p_city']}")
            st.markdown(f"**📥 To:** {fd['d_address']}, {fd['d_city']}")
            st.markdown(f"**ℹ️ Info:** {fd['info']}")

    st.write("<br>", unsafe_allow_html=True)
    c_btn1, c_btn2, _ = st.columns([1, 1, 4])
    with c_btn1:
        st.button("⬅ Go Back", on_click=prev_step, use_container_width=True)
    with c_btn2:
        if st.button("🚀 Submit Booking", use_container_width=True):
            # Bereid de data voor Supabase voor
            order_data = {
                "company": fd['company_name'],
                "reg_no": fd['reg_no'],
                "address": f"{fd['address']}, {fd['zip']} {fd['city']}, {fd['country']}",
                "contact_name": f"{fd['first_name']} {fd['last_name']}",
                "email": fd['email'],
                "phone": fd['phone'],
                "types": ", ".join(fd['types']),
                "info": fd['info'],
                "status": "New",
                "received_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "pickup_address": fd['p_address'],
                "pickup_zip": fd['p_zip'],
                "pickup_city": fd['p_city'],
                "delivery_address": fd['d_address'],
                "delivery_zip": fd['d_zip'],
                "delivery_city": fd['d_city']
            }
            try:
                supabase.table("orders").insert(order_data).execute()
                st.success("🎉 Request successfully submitted!")
                reset_form()
            except Exception as e:
                st.error(f"Something went wrong: {e}")

# --- DEMO NAVIGATIE ONDERAAN ---
st.write("<br><br><br>", unsafe_allow_html=True)
st.markdown("---")
spacer_nav1, col_nav1, col_nav2, spacer_nav2 = st.columns([2, 1.5, 1.5, 2])
with col_nav1:
    if st.button("🔐 Internal Planner", use_container_width=True):
        st.switch_page("pages/Planner.py")
with col_nav2:
    if st.button("🌍 CO₂ Dashboard", use_container_width=True):
        st.switch_page("pages/Dashboard.py")
