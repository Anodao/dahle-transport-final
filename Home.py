import streamlit as st
from supabase import create_client
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Dahle Transport", page_icon="🚚", layout="wide")

# --- SUPABASE CONNECTIE ---
@st.cache_resource
def init_connection():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

supabase = init_connection()

# --- CSS STYLING ---
st.markdown("""
    <style>
    .header-text { color: #894b9d; font-weight: bold; font-size: 24px; margin-bottom: 20px; }
    .section-header { color: #894b9d; font-weight: bold; font-size: 18px; margin-top: 20px; margin-bottom: 10px; border-bottom: 1px solid #ddd; padding-bottom: 5px; }
    div.stButton > button { background-color: #894b9d; color: white; border-radius: 6px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
c1, c2 = st.columns([1, 4])
with c1:
    st.image("https://via.placeholder.com/150x80.png?text=LOGO", width=120) # Vervang met je eigen logo indien beschikbaar
with c2:
    st.title("Dahle Transport - Booking Request")
    st.write("Fill in the details below to request a transport quote directly into our system.")

st.markdown("---")

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

    # 2. ROUTE INFORMATIE (NIEUW!)
    st.markdown('<div class="section-header">📍 Route Information</div>', unsafe_allow_html=True)
    st.info("Please specify where the goods need to be picked up and delivered.")
    
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

    # SUBMIT KNOP
    submitted = st.form_submit_button("🚀 Submit Booking Request", use_container_width=True)

    if submitted:
        # Validatie: Check of verplichte velden zijn ingevuld
        if not company_name or not contact_name or not email:
            st.error("Please fill in all mandatory fields marked with (*).")
        else:
            # Data voorbereiden voor Supabase
            order_data = {
                "company": company_name,
                "reg_no": reg_no,
                "address": f"{address}, {postal} {city}", # We voegen dit samen voor het hoofd-adres
                "contact_name": contact_name,
                "email": email,
                "phone": phone,
                "types": ", ".join(shipment_type),
                "info": info,
                "status": "New",
                "received_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                # NIEUWE VELDEN OPSLAAN
                "pickup_address": p_address,
                "pickup_zip": p_zip,
                "pickup_city": p_city,
                "delivery_address": d_address,
                "delivery_zip": d_zip,
                "delivery_city": d_city
            }
            
            try:
                # Verstuur naar Supabase
                supabase.table("orders").insert(order_data).execute()
                st.success("✅ Thank you! Your booking request has been sent to our planners.")
            except Exception as e:
                st.error(f"Something went wrong: {e}")

# --- INTERNE NAVIGATIE VOOR DEMO ---
st.write("")
st.markdown("---")
c_link1, c_link2, c_link3, c_link4 = st.columns([1, 1.5, 1.5, 1])
with c_link1: pass 
with c_link2:
    if st.button("🔐 Internal Planner", use_container_width=True):
        st.switch_page("pages/Planner.py")
with c_link3:
    if st.button("🌍 CO₂ Dashboard", use_container_width=True):
        st.switch_page("pages/Dashboard.py")
with c_link4: pass
