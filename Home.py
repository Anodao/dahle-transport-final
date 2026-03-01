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

try:
    supabase = init_connection()
except Exception:
    pass

# --- CSS STYLING (Jouw originele opmaak) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    /* Verberg de sidebar */
    [data-testid="collapsedControl"] { display: none; }
    [data-testid="stSidebar"] { display: none; }
    
    /* Titels */
    .main-header { text-align: center; color: white; font-size: 28px; font-weight: 700; margin-top: 20px; margin-bottom: 5px;}
    .sub-header { text-align: center; color: #8b949e; font-size: 14px; margin-bottom: 40px;}
    
    /* Knoppen (Dahle Paars) */
    div.stButton > button, div[data-testid="stFormSubmitButton"] > button { 
        background-color: #894b9d; 
        color: white; 
        border-radius: 6px; 
        font-weight: bold; 
        border: none; 
        padding: 0.5rem 1rem;
    }
    div.stButton > button:hover, div[data-testid="stFormSubmitButton"] > button:hover { 
        background-color: #723e83; 
        color: white;
    }
    
    .privacy-text { text-align: center; color: #8b949e; font-size: 13px; margin-top: 40px; margin-bottom: 20px;}
    </style>
""", unsafe_allow_html=True)

# --- HEADER TITELS ---
st.markdown('<div class="main-header">Send us your contact information and we will get in touch.</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">All fields marked with an asterisk (*) are mandatory</div>', unsafe_allow_html=True)

# --- JOUW ORIGINELE FORMULIER ---
with st.form("booking_form", clear_on_submit=True):
    col_left, col_right = st.columns(2, gap="large")
    
    with col_left:
        st.subheader("Company Details")
        company_name = st.text_input("Company Name *")
        reg_no = st.text_input("Company Registration No. (optional)")
        address = st.text_input("Company Address *")
        
        c_zip, c_city = st.columns(2)
        with c_zip: 
            postal = st.text_input("Postal Code *")
        with c_city: 
            city = st.text_input("City *")
            
        country = st.text_input("Country *", value="Norway")

    with col_right:
        st.subheader("Contact Person")
        c_fn, c_ln = st.columns(2)
        with c_fn: 
            first_name = st.text_input("First Name *")
        with c_ln: 
            last_name = st.text_input("Last Name *")
            
        email = st.text_input("Work Email *", placeholder="example@email.no")
        phone = st.text_input("Phone *", placeholder="+47 123 456 789")
        
        info = st.text_area("Additional Information (optional)", placeholder="Describe what you ship, approx. weight, any special requirements, etc.")

    # Privacy tekstje onderaan
    st.markdown('<div class="privacy-text">If you would like to learn more about how Dahle Transport uses your personal data, please read our privacy notice which you can find in the footer.</div>', unsafe_allow_html=True)

    # --- KNOPPEN (Go Back & Continue) ---
    c_btn1, c_space, c_btn3 = st.columns([1, 4, 1.5])
    with c_btn1:
        st.form_submit_button("← Go Back", use_container_width=True)
    with c_btn3:
        submitted = st.form_submit_button("Continue to Review →", use_container_width=True)

    # --- SUPABASE OPSLAAN ---
    if submitted:
        if not company_name or not first_name or not last_name or not email:
            st.error("Please fill in all mandatory fields (*).")
        else:
            order_data = {
                "company": company_name,
                "reg_no": reg_no,
                "address": f"{address}, {postal} {city}, {country}",
                "contact_name": f"{first_name} {last_name}",
                "email": email,
                "phone": phone,
                "types": "Standard Delivery",
                "info": info,
                "status": "New",
                "received_date": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            try:
                supabase.table("orders").insert(order_data).execute()
                st.success("🎉 Request successfully submitted! Your data has been sent to our planners.")
            except Exception as e:
                st.error(f"Something went wrong while saving: {e}")

# --- DEMO KNOPPEN NAAR DE PLANNER & DASHBOARD (Gecentreerd) ---
st.write("<br><br>", unsafe_allow_html=True)
st.markdown("---")
spacer_nav1, col_nav1, col_nav2, spacer_nav2 = st.columns([2, 1.5, 1.5, 2])
with col_nav1:
    if st.button("🔐 Open Internal Planner System", use_container_width=True):
        st.switch_page("pages/Planner.py")
with col_nav2:
    if st.button("🌍 Open CO₂ Dashboard", use_container_width=True):
        st.switch_page("pages/Dashboard.py")
