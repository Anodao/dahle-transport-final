import streamlit as st
from datetime import datetime
import time

st.set_page_config(page_title="Opter Client Portal", page_icon="🔐", layout="centered")

# --- CSS STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }
    [data-testid="collapsedControl"] { display: none !important; }
    [data-testid="stSidebar"] { display: none !important; }
    header[data-testid="stHeader"] { display: none !important; }
    
    .opter-header { text-align: center; margin-bottom: 30px; }
    .opter-logo { color: #894b9d; font-size: 40px; font-weight: 800; letter-spacing: 2px; }
    div.stButton > button { background-color: #894b9d; color: white; font-weight: bold; width: 100%; border-radius: 6px; border: none; }
    div.stButton > button:hover { background-color: #723e83; }
    </style>
""", unsafe_allow_html=True)

# Simpele login state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

st.markdown('<div class="opter-header"><span class="opter-logo">OPTER</span><br><span style="color:#888;">Direct API Integration Portal</span></div>', unsafe_allow_html=True)

if not st.session_state.logged_in:
    # --- LOGIN SCHERM ---
    with st.container(border=True):
        st.subheader("Client Login")
        st.info("Demo: Je kunt hier met elk wachtwoord inloggen.")
        client_id = st.text_input("Client ID / API Key", value="DAHLE-API-992")
        password = st.text_input("Password", type="password")
        
        if st.button("Secure Login ➔"):
            if client_id and password:
                with st.spinner("Authenticating with Opter API..."):
                    time.sleep(1.5) # Simuleer laadtijd
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Please enter credentials.")
                
    if st.button("← Back to Home", type="secondary"):
        st.switch_page("Home.py")

else:
    # --- DIRECT BOOKING FORMULIER (Als je bent ingelogd) ---
    st.success("✅ Authenticated. Connected to Opter TMS.")
    st.write("Welcome back, **Client #992**. Fast-track your order below. Data is pushed directly via API.")
    
    with st.form("api_booking_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            ref_no = st.text_input("Your Reference Number *")
            p_zip = st.text_input("Pickup Zip Code *")
        with col2:
            service = st.selectbox("Service Level", ["Standard Freight", "Express 24h", "Cold Chain"])
            d_zip = st.text_input("Delivery Zip Code *")
            
        weight = st.number_input("Total Weight (kg) *", min_value=1, value=150)
        
        submitted = st.form_submit_button("🚀 PUSH TO OPTER", use_container_width=True)
        
        if submitted:
            if not ref_no or not p_zip or not d_zip:
                st.error("Please fill in all mandatory fields.")
            else:
                # Hier bouw je in theorie de API POST request!
                st.info("📡 Transmitting JSON payload to Opter Endpoint...")
                time.sleep(1.5)
                st.success(f"🎉 Success! Order {ref_no} injected into Opter. Tracking ID: OP-{datetime.now().strftime('%M%S%f')}")
                
    if st.button("Log Out"):
        st.session_state.logged_in = False
        st.rerun()
