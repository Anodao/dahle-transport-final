import streamlit as st

st.set_page_config(page_title="Dahle Transport - Portal", page_icon="🚚", layout="wide", initial_sidebar_state="collapsed")

# --- CSS STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }
    
    [data-testid="collapsedControl"] { display: none !important; }
    [data-testid="stSidebar"] { display: none !important; }
    header[data-testid="stHeader"] { display: none !important; }
    
    .main-title { color: #ffffff; font-weight: 700; font-size: 36px; text-align: center; margin-top: 50px; margin-bottom: 10px; }
    .sub-title { color: #8b949e; text-align: center; font-size: 16px; margin-bottom: 50px; }
    
    /* Portal Cards Styling */
    .portal-card {
        background-color: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 40px; text-align: center; transition: 0.3s; height: 100%;
    }
    .portal-card:hover { border-color: #894b9d; transform: translateY(-5px); box-shadow: 0 10px 20px rgba(137, 75, 157, 0.1); }
    .card-icon { font-size: 50px; margin-bottom: 20px; }
    .card-title { color: white; font-size: 24px; font-weight: bold; margin-bottom: 15px; }
    .card-text { color: #8b949e; font-size: 14px; margin-bottom: 30px; line-height: 1.6; }
    
    div.stButton > button { background-color: #894b9d; color: white; border-radius: 6px; font-weight: bold; padding: 12px 24px; border: none; width: 100%; }
    div.stButton > button:hover { background-color: #723e83; }
    </style>
""", unsafe_allow_html=True)

# --- CONTENT ---
st.markdown('<div class="main-title">Welcome to Dahle Transport</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Please select your portal to continue</div>', unsafe_allow_html=True)

c_spacer1, c1, c2, c_spacer2 = st.columns([1, 3, 3, 1], gap="large")

with c1:
    st.markdown("""
        <div class="portal-card">
            <div class="card-icon">👋</div>
            <div class="card-title">New Customer</div>
            <div class="card-text">Looking for a reliable transport partner? Tell us about your shipment needs and request a quote. Our planners will get in touch.</div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Request a Quote", key="btn_new"):
        st.switch_page("pages/1_New_Request.py")

with c2:
    st.markdown("""
        <div class="portal-card">
            <div class="card-icon">🔐</div>
            <div class="card-title">Opter Client Portal</div>
            <div class="card-text">Existing customers can log in here. Book directly into our Opter TMS system via API for instant processing and tracking.</div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Log In & Book", key="btn_exist"):
        st.switch_page("pages/2_Opter_Portal.py")
