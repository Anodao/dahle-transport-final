import streamlit as st
from datetime import datetime
import time

st.set_page_config(page_title="Opter Client Portal", page_icon="🔐", layout="centered")

# --- CSS STYLING GLOBAL & NAVBAR HTML ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }

    /* --- HEADER & SIDEBAR FIX --- */
    [data-testid="collapsedControl"] { display: none !important; }
    [data-testid="stSidebar"] { display: none !important; }
    header[data-testid="stHeader"] { background: transparent !important; pointer-events: none !important; display: none !important;}
    
    /* --- NAVBAR --- */
    .block-container { padding-top: 110px; }
    .navbar {
        position: fixed; top: 0; left: 0; width: 100%; height: 90px;
        background-color: white; z-index: 999; border-bottom: 1px solid #eaeaea; 
        display: grid; grid-template-columns: 1fr auto 1fr; align-items: center;
        padding: 0 40px; box-shadow: 0 2px 10px rgba(0,0,0,0.03);
    }
    .nav-logo { display: flex; justify-content: flex-start; }
    .nav-logo a { display: inline-block; height: 48px; text-decoration: none; cursor: pointer; }
    .nav-logo img { height: 100%; width: auto; display: block; transition: transform 0.2s ease-in-out; }
    .nav-logo a:hover img { transform: scale(1.05); } 
    .nav-links { display: flex; gap: 28px; font-size: 15px; font-weight: 500; color: #000000; justify-content: center;}
    .nav-links a { text-decoration: none; color: inherit; }
    .nav-links span { cursor: pointer; transition: color 0.2s; }
    .nav-links span:hover { color: #894b9d; }
    .nav-cta { display: flex; justify-content: flex-end; gap: 15px; align-items: center; }
    
    /* Knoppen styling */
    .cta-btn { 
        background-color: #894b9d; color: white !important; padding: 10px 24px;
        border-radius: 50px; text-decoration: none !important; font-weight: 600; 
        font-size: 13px; letter-spacing: 0.5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        cursor: pointer; transition: background-color 0.2s; white-space: nowrap;
    }
    .cta-btn:hover { background-color: #723e83; }

    .cta-btn-outline {
        background-color: transparent; color: #894b9d !important; padding: 10px 20px;
        border-radius: 50px; text-decoration: none !important; font-weight: 600; 
        font-size: 13px; letter-spacing: 0.5px; border: 2px solid #894b9d;
        cursor: pointer; transition: all 0.2s; white-space: nowrap;
    }
    .cta-btn-outline:hover { background-color: #894b9d; color: white !important; }
    </style>
    
    <div class="navbar">
        <div class="nav-logo">
            <a href="/" target="_self" title="Go back to Home">
                <img src="https://cloud-1de12d.becdn.net/media/original/964295c9ae8e693f8bb4d6b70862c2be/logo-website-top-png-1-.webp" alt="Dahle Transport Logo">
            </a>
        </div>
        <div class="nav-links">
            <a href="/"><span>Hjem</span></a>
            <span>Om oss</span><span>Tjenester</span><span>Galleri</span><span>Kontakt</span>
        </div>
        <div class="nav-cta">
            <a href="/Opter_Portal" target="_self" class="cta-btn-outline">OPTER LOGIN</a>
            <a href="/" target="_self" class="cta-btn">TA KONTAKT</a>
        </div>
    </div>
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
