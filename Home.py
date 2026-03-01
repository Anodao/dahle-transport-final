import streamlit as st
from supabase import create_client
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Dahle Transport - Booking", page_icon="🚚", layout="wide")

# --- SUPABASE CONNECTIE ---
@st.cache_resource
def init_connection():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

try:
    supabase = init_connection()
except Exception:
    pass # Voorkomt foutmeldingen als secrets.toml nog niet perfect is

# --- SESSION STATE (Bewaar gegevens tussen stappen) ---
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

def reset_form():
    st.session_state.step = 1
    for key in st.session_state.fd.keys():
        st.session_state.fd[key] = [] if key == 'types' else ( 'Norway' if key == 'country' else '' )

# --- PAARSE KNOPPEN STYLING ---
st.markdown("""
    <style>
    div.stButton > button { background-color: #894b9d; color: white; border-radius: 6px; font-weight: bold; border: none; }
    div.stButton > button:hover { background-color: #723e83; }
    </style>
""", unsafe_allow_html=True)

fd = st.session_state.fd

# =========================================================
# HEADER & VOORTGANG (Zichtbaar op elke stap)
# =========================================================
st.title("Send us your contact information and we will get in touch.")
st.caption("All fields marked with an asterisk (*) are mandatory")

# Een simpele, betrouwbare ingebouwde progress bar van Streamlit in plaats van foutgevoelige HTML
st.progress(st.session_state.step / 3, text=f"Step {st.session_state.step} of 3")
st.write("---")

# =========================================================
# STAP 1: COMPANY DETAILS & CONTACT PERSON (Uit je screenshot)
# =========================================================
if st.session_state.step == 1:
    col_left, col_right = st.columns(2, gap="large")
    
    with col_left:
        st.subheader("🏢 Company Details")
        fd['company_name'] = st.text_input("Company Name *", value=fd['company_name'])
        fd['reg_no'] = st.text_input("Company Registration No. (optional)", value=fd['reg_no'])
        fd['address'] = st.text_input("Company Address *", value=fd['address'])
        c_zip, c_city = st.columns(2)
        with c_zip: fd['zip'] = st.text_input("Postal Code *", value=fd['zip'])
        with c_city: fd['city'] = st.text_input("City *", value=fd['city'])
        fd['country'] = st.text_input("Country *", value=fd['country'])

    with col_right:
        st.subheader("👤 Contact Person")
        c_fn, c_ln = st.columns(2)
        with c_fn: fd['first_name'] = st.text_input("First Name *", value=fd['first_name'])
        with c_ln: fd['last_name'] = st.text_input("Last Name *", value=fd['last_name'])
        fd['email'] = st.text_input("Work Email *", value=fd['email'], placeholder="example@email.no")
        fd['phone'] = st.text_input("Phone *", value=fd['phone'], placeholder="+47 123 456 789")
        fd['info'] = st.text_area("Additional Information (optional)", value=fd['info'], placeholder="Describe what you ship, approx. weight, any special requirements, etc.")

    st.write("<br>", unsafe_allow_html=True)
    _, col_btn = st.columns([4, 1])
    with col_btn:
        if st.button("Continue to Route ➔", use_container_width=True):
            st.session_state.step = 2
            st.rerun()

# =========================================================
# STAP 2: ROUTE INFORMATIE
# =========================================================
elif st.session_state.step == 2:
    st.subheader("📍 Route Information")
    st.info("Please specify where the goods need to be picked up and delivered.")
    
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
    st.subheader("📦 Requested Services")
    options = ["Freight", "Parcels", "Express", "Warehousing"]
    default_types = [t for t in fd['types'] if t in options]
    fd['types'] = st.multiselect("Select the services you need", options, default=default_types)

    st.write("<br>", unsafe_allow_html=True)
    c_btn1, _, c_btn2 = st.columns([1, 3, 1])
    with c_btn1:
        if st.button("⬅ Go Back", use_container_width=True):
            st.session_state.step = 1
            st.rerun()
    with c_btn2:
        if st.button("Continue to Review ➔", use_container_width=True):
            st.session_state.step = 3
            st.rerun()

# =========================================================
# STAP 3: REVIEW & SUBMIT
# =========================================================
elif st.session_state.step == 3:
    st.subheader("✅ Review & Confirm")
    
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
    c_btn1, _, c_btn2 = st.columns([1, 3, 1])
    with c_btn1:
        if st.button("⬅ Go Back", use_container_width=True):
            st.session_state.step = 2
            st.rerun()
    with c_btn2:
        if st.button("🚀 Submit Booking", use_container_width=True):
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
st.write("<br><br>", unsafe_allow_html=True)
st.markdown("---")
spacer_nav1, col_nav1, col_nav2, spacer_nav2 = st.columns([2, 1.5, 1.5, 2])
with col_nav1:
    if st.button("🔐 Internal Planner", use_container_width=True):
        st.switch_page("pages/Planner.py")
with col_nav2:
    if st.button("🌍 CO₂ Dashboard", use_container_width=True):
        st.switch_page("pages/Dashboard.py")
