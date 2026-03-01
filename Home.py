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

# --- CSS STYLING & CLEANUP ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    /* VERWIJDER DE BOVENBALK EN HET >> ICOON */
    header[data-testid="stHeader"] { visibility: hidden; height: 0%; }
    [data-testid="stSidebar"] { display: none; }
    .block-container { padding-top: 2rem; }
    
    /* STYLING VOOR TITELS EN KNOPPEN */
    .main-title { color: #ffffff; font-weight: 700; font-size: 32px; text-align: center; margin-bottom: 5px; }
    .sub-title { color: #8b949e; text-align: center; font-size: 16px; margin-bottom: 30px; }
    .section-header { color: #894b9d; font-weight: bold; font-size: 18px; margin-top: 15px; margin-bottom: 10px; border-bottom: 1px solid #30363d; padding-bottom: 5px; }
    
    div.stButton > button { background-color: #894b9d; color: white; border-radius: 6px; font-weight: bold; padding: 10px; border: none;}
    div.stButton > button:hover { background-color: #723e83; color: white; }
    
    /* Verberg de standaard formulier-rand voor een schonere look */
    [data-testid="stForm"] { border: none; padding: 0; }
    </style>
""", unsafe_allow_html=True)

# --- CENTREREN VAN DE PAGINA ---
# We gebruiken [1, 2, 1] zodat het formulier in het midden staat en niet de hele breedte pakt
spacer_left, col_main, spacer_right = st.columns([1, 2.5, 1])

with col_main:
    # --- HEADER ---
    st.markdown('<div class="main-title">Dahle Transport - Booking Request</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Fill in the details below to request a transport quote directly into our system.</div>', unsafe_allow_html=True)

    # --- FORMULIER START ---
    with st.form("order_form", clear_on_submit=True):
        
        # 1. BEDRIJFSGEGEVENS
        st.markdown('<div class="section-header">🏢 Company Details</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            company_name = st.text_input("Company Name *")
            reg_no = st.text_input("Company Registration No. (optional)")
        with col2:
            address = st.text_input("Registered Address *")
            c_zip, c_city = st.columns([1, 2])
            with c_zip: postal = st.text_input("Postal Code *")
            with c_city: city = st.text_input("City *")

        # 2. ROUTE INFORMATIE
        st.markdown('<div class="section-header">📍 Route Information</div>', unsafe_allow_html=True)
        
        c_pickup, c_delivery = st.columns(2, gap="large")
        with c_pickup:
            st.markdown("**📤 Pickup Location**")
            p_address = st.text_input("Pickup Address", key="p_addr")
            cp1, cp2 = st.columns([1, 2])
            with cp1: p_zip = st.text_input("Zip Code", key="p_zip")
            with cp2: p_city = st.text_input("City", key="p_city")
            
        with c_delivery:
            st.markdown("**📥 Delivery Destination**")
            d_address = st.text_input("Delivery Address", key="d_addr")
            cd1, cd2 = st.columns([1, 2])
            with cd1: d_zip = st.text_input("Zip Code", key="d_zip")
            with cd2: d_city = st.text_input("City", key="d_city")

        # 3. CONTACTPERSOON
        st.markdown('<div class="section-header">👤 Contact Person</div>', unsafe_allow_html=True)
        c3, c4 = st.columns(2)
        with c3:
            contact_name = st.text_input("Full Name *")
            email = st.text_input("Email Address *")
        with c4:
            phone = st.text_input("Phone Number *")
            
        # 4. ZENDING DETAILS
        st.markdown('<div class="section-header">📦 Shipment Details</div>', unsafe_allow_html=True)
        shipment_type = st.multiselect("Requested Services", ["Freight", "Parcels", "Express", "Warehousing"])
        info = st.text_area("Additional Information (e.g. weight, dimensions, special instructions)")

        st.write("") # Extra witregel
        
        # SUBMIT KNOP
        submitted = st.form_submit_button("🚀 Submit Booking Request", use_container_width=True)

        if submitted:
            if not company_name or not contact_name or not email:
                st.error("⚠️ Please fill in all mandatory fields marked with (*).")
            else:
                order_data = {
                    "company": company_name,
                    "reg_no": reg_no,
                    "address": f"{address}, {postal} {city}",
                    "contact_name": contact_name,
                    "email": email,
                    "phone": phone,
                    "types": ", ".join(shipment_type),
                    "info": info,
                    "status": "New",
                    "received_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "pickup_address": p_address,
                    "pickup_zip": p_zip,
                    "pickup_city": p_city,
                    "delivery_address": d_address,
                    "delivery_zip": d_zip,
                    "delivery_city": d_city
                }
                try:
                    supabase.table("orders").insert(order_data).execute()
                    st.success("✅ Thank you! Your booking request has been sent to our planners.")
                except Exception as e:
                    st.error(f"Something went wrong: {e}")

# --- INTERNE NAVIGATIE VOOR DEMO (Onderaan gecentreerd) ---
st.write("")
st.write("")
st.markdown("---")
# Knoppen ook mooi in het midden zetten
spacer_nav1, col_nav1, col_nav2, spacer_nav2 = st.columns([2, 1.5, 1.5, 2])

with col_nav1:
    if st.button("🔐 Internal Planner", use_container_width=True):
        st.switch_page("pages/Planner.py")
with col_nav2:
    if st.button("🌍 CO₂ Dashboard", use_container_width=True):
        st.switch_page("pages/Dashboard.py")
