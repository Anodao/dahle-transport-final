import streamlit as st
from supabase import create_client
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Dahle Transport - Booking", 
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

supabase = init_connection()

# --- SESSION STATE INITIALIZATION (Bewaar data tussen de stappen) ---
if 'step' not in st.session_state:
    st.session_state.step = 1

# We slaan alle ingevulde formulier data hier op:
if 'fd' not in st.session_state:
    st.session_state.fd = {
        'company_name': '', 'reg_no': '', 'address': '', 'zip': '', 'city': '',
        'contact_name': '', 'email': '', 'phone': '',
        'p_address': '', 'p_zip': '', 'p_city': '',
        'd_address': '', 'd_zip': '', 'd_city': '',
        'types': [], 'info': ''
    }

def next_step(): st.session_state.step += 1
def prev_step(): st.session_state.step -= 1
def reset_form():
    st.session_state.step = 1
    for key in st.session_state.fd.keys():
        st.session_state.fd[key] = [] if key == 'types' else ''

# --- CSS STYLING & CLEANUP ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    /* VERWIJDER DE BOVENBALK EN HET >> ICOON */
    header[data-testid="stHeader"] { visibility: hidden; height: 0%; }
    [data-testid="stSidebar"] { display: none; }
    
    /* Zorg dat de breedte mooi behapbaar blijft en niet 100% uitsmeert */
    .block-container { padding-top: 2rem; max-width: 1100px; }
    
    .main-title { color: #ffffff; font-weight: 700; font-size: 32px; text-align: center; margin-bottom: 5px; }
    .sub-title { color: #8b949e; text-align: center; font-size: 16px; margin-bottom: 30px; }
    .step-header { color: #894b9d; font-weight: bold; font-size: 20px; border-bottom: 2px solid #30363d; padding-bottom: 8px; margin-bottom: 20px; margin-top: 10px;}
    
    /* Knop Styling */
    div.stButton > button { background-color: #894b9d; color: white; border-radius: 6px; font-weight: bold; border: none; padding: 0.5rem 1rem; transition: 0.2s;}
    div.stButton > button:hover { background-color: #723e83; transform: translateY(-2px); }
    div.stButton > button[kind="secondary"] { background-color: #30363d; color: #c9d1d9; }
    div.stButton > button[kind="secondary"]:hover { background-color: #484f58; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER & PROGRESS BAR ---
st.markdown('<div class="main-title">Dahle Transport - Booking Request</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Follow the 3 steps below to request a transport quote directly into our system.</div>', unsafe_allow_html=True)

st.progress(st.session_state.step / 3)
st.markdown(f"<p style='text-align: right; color: #8b949e; font-size: 14px;'>Step {st.session_state.step} of 3</p>", unsafe_allow_html=True)

# Koppel de formulier variabelen aan een kortere naam voor het gemak
fd = st.session_state.fd

# =========================================================
# STAP 1: COMPANY & CONTACT
# =========================================================
if st.session_state.step == 1:
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown('<div class="step-header">🏢 Company Details</div>', unsafe_allow_html=True)
        fd['company_name'] = st.text_input("Company Name *", value=fd['company_name'])
        fd['reg_no'] = st.text_input("Company Registration No. (optional)", value=fd['reg_no'])
        fd['address'] = st.text_input("Company Address *", value=fd['address'])
        col_z, col_c = st.columns(2)
        with col_z: fd['zip'] = st.text_input("Postal Code *", value=fd['zip'])
        with col_c: fd['city'] = st.text_input("City *", value=fd['city'])
        
    with c2:
        st.markdown('<div class="step-header">👤 Contact Person</div>', unsafe_allow_html=True)
        fd['contact_name'] = st.text_input("Full Name *", value=fd['contact_name'])
        fd['email'] = st.text_input("Work Email *", value=fd['email'])
        fd['phone'] = st.text_input("Phone Number *", value=fd['phone'])
        
    st.write("---")
    _, col_btn = st.columns([4, 1])
    with col_btn:
        if st.button("Continue to Route ➔", use_container_width=True):
            if not fd['company_name'] or not fd['email'] or not fd['contact_name']:
                st.error("⚠️ Please fill in all mandatory fields (*).")
            else:
                next_step()
                st.rerun()

# =========================================================
# STAP 2: ROUTE & SHIPMENT (DE NIEUWE VELDEN)
# =========================================================
elif st.session_state.step == 2:
    st.markdown('<div class="step-header">📍 Route Information</div>', unsafe_allow_html=True)
    c_pick, c_del = st.columns(2, gap="large")
    with c_pick:
        st.markdown("**📤 Pickup Location**")
        fd['p_address'] = st.text_input("Pickup Address", value=fd['p_address'])
        col_pz, col_pc = st.columns(2)
        with col_pz: fd['p_zip'] = st.text_input("Pickup Zip", value=fd['p_zip'])
        with col_pc: fd['p_city'] = st.text_input("Pickup City", value=fd['p_city'])
        
    with c_del:
        st.markdown("**📥 Delivery Destination**")
        fd['d_address'] = st.text_input("Delivery Address", value=fd['d_address'])
        col_dz, col_dc = st.columns(2)
        with col_dz: fd['d_zip'] = st.text_input("Delivery Zip", value=fd['d_zip'])
        with col_dc: fd['d_city'] = st.text_input("Delivery City", value=fd['d_city'])
        
    st.markdown('<div class="step-header">📦 Shipment Details</div>', unsafe_allow_html=True)
    options = ["Freight", "Parcels", "Express", "Warehousing"]
    default_types = [t for t in fd['types'] if t in options]
    fd['types'] = st.multiselect("Requested Services", options, default=default_types)
    fd['info'] = st.text_area("Additional Information (optional)", value=fd['info'], placeholder="Describe what you ship, approx. weight, special requirements, etc.")

    st.write("---")
    col_back, _, col_next = st.columns([1, 3, 1])
    with col_back:
        st.button("⬅ Go Back", on_click=prev_step, type="secondary", use_container_width=True)
    with col_next:
        if st.button("Continue to Review ➔", use_container_width=True):
            next_step()
            st.rerun()

# =========================================================
# STAP 3: REVIEW & SUBMIT
# =========================================================
elif st.session_state.step == 3:
    st.markdown('<div class="step-header">✅ Review & Confirm</div>', unsafe_allow_html=True)
    st.info("Please review your details below. If everything is correct, click Submit to send your request.")
    
    with st.container(border=True):
        c_rev1, c_rev2 = st.columns(2)
        with c_rev1:
            st.markdown(f"**🏢 Company:** {fd['company_name']}")
            st.markdown(f"**👤 Contact:** {fd['contact_name']} ({fd['email']})")
            st.markdown(f"**📦 Services:** {', '.join(fd['types']) if fd['types'] else 'Not specified'}")
        with c_rev2:
            st.markdown(f"**📤 From:** {fd['p_address']}, {fd['p_city']}")
            st.markdown(f"**📥 To:** {fd['d_address']}, {fd['d_city']}")
            st.markdown(f"**ℹ️ Info:** {fd['info']}")

    st.write("---")
    col_back, _, col_sub = st.columns([1, 3, 1])
    with col_back:
        st.button("⬅ Go Back", on_click=prev_step, type="secondary", use_container_width=True)
    with col_sub:
        if st.button("🚀 Submit Booking", use_container_width=True):
            order_data = {
                "company": fd['company_name'],
                "reg_no": fd['reg_no'],
                "address": f"{fd['address']}, {fd['zip']} {fd['city']}",
                "contact_name": fd['contact_name'],
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

# --- INTERNE NAVIGATIE KAN GECOMBINEERD ONDERAAN ---
st.write("<br><br>", unsafe_allow_html=True)
st.markdown("---")
spacer_nav1, col_nav1, col_nav2, spacer_nav2 = st.columns([2, 1.5, 1.5, 2])
with col_nav1:
    if st.button("🔐 Internal Planner", type="secondary", use_container_width=True):
        st.switch_page("pages/Planner.py")
with col_nav2:
    if st.button("🌍 CO₂ Dashboard", type="secondary", use_container_width=True):
        st.switch_page("pages/Dashboard.py")
