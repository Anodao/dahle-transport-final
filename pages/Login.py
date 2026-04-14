import streamlit as st
from supabase import create_client

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Dahle Transport - Customer Portal",
    page_icon="🔐",
    layout="centered",
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
    st.error("⚠️ Database connection failed.")
    st.stop()

# --- INITIALIZE SESSION STATE ---
if 'user' not in st.session_state:
    st.session_state.user = None

# --- CSS STYLING & NAVBAR ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }
    
    [data-testid="collapsedControl"], [data-testid="stSidebar"], header[data-testid="stHeader"] { display: none !important; }
    .stApp { background-color: #f8f9fa !important; }
    .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: #111111 !important; }

    /* --- NAVBAR --- */
    .block-container { padding-top: 130px !important; max-width: 800px; }
    .navbar {
        position: fixed; top: 0; left: 0; width: 100%; height: 90px;
        background-color: #ffffff !important; z-index: 999; border-bottom: 1px solid #eaeaea; 
        display: grid; grid-template-columns: 1fr auto 1fr; align-items: center;
        padding: 0 40px; box-shadow: 0 2px 10px rgba(0,0,0,0.03);
    }
    .nav-logo img { height: 48px; width: auto; transition: transform 0.2s; }
    .nav-links { display: flex; gap: 28px; font-size: 15px; font-weight: 500; justify-content: center; }
    .nav-links a { text-decoration: none; color: #111111 !important; cursor: pointer; }
    .nav-cta { display: flex; justify-content: flex-end; gap: 15px; }
    
    .cta-btn { background-color: #894b9d !important; color: white !important; padding: 10px 24px; border-radius: 50px; text-decoration: none !important; font-weight: 600; font-size: 13px; white-space: nowrap;}
    .cta-btn-outline { background-color: transparent !important; color: #894b9d !important; padding: 10px 20px; border-radius: 50px; text-decoration: none !important; font-weight: 600; font-size: 13px; border: 2px solid #894b9d; white-space: nowrap;}

    /* --- FORM & BUTTON STYLING (GEFIXT VOOR LIGHT MODE) --- */
    div[data-baseweb="input"] > div { background-color: #ffffff !important; border: 1px solid #d1d5db !important; border-radius: 6px !important; }
    div[data-baseweb="input"] input { color: #111111 !important; -webkit-text-fill-color: #111111 !important; }
    label[data-testid="stWidgetLabel"] p { color: #333333 !important; font-weight: 600; font-size: 14px !important;}
    
    /* Primary Button */
    div.stButton > button[kind="primary"] { 
        background: linear-gradient(135deg, #b070c6 0%, #894b9d 100%) !important; 
        color: #ffffff !important; border: none !important; border-radius: 6px !important; 
        padding: 14px 28px !important; font-weight: 600 !important; font-size: 15px !important;
        width: 100% !important; box-shadow: 0 4px 14px 0 rgba(137, 75, 157, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button[kind="primary"]:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 24px rgba(137, 75, 157, 0.6) !important; }
    
    /* Secondary Button */
    div.stButton > button[kind="secondary"] { 
        background: transparent !important; color: #894b9d !important; border: 2px solid #894b9d !important; border-radius: 6px !important; 
        padding: 14px 28px !important; font-weight: 600 !important; font-size: 15px !important;
        width: 100% !important; transition: all 0.3s ease !important;
    }
    div.stButton > button[kind="secondary"]:hover { background: #894b9d !important; color: white !important; }

    /* Tabs styling */
    button[data-baseweb="tab"] { background-color: transparent !important; color: #666 !important; font-weight: 600; font-size: 16px;}
    button[data-baseweb="tab"][aria-selected="true"] { color: #894b9d !important; border-bottom: 3px solid #894b9d !important; }
    </style>

    <div class="navbar">
        <div class="nav-logo">
            <a href="/" target="_self"><img src="https://cloud-1de12d.becdn.net/media/original/964295c9ae8e693f8bb4d6b70862c2be/logo-website-top-png-1-.webp"></a>
        </div>
        <div class="nav-links">
            <a href="/"><span>Hjem</span></a>
            <span>Om oss</span><span>Tjenester</span><span>Galleri</span><span>Kontakt</span>
        </div>
        <div class="nav-cta">
            <a href="/Login" target="_self" class="cta-btn-outline">KUNDEPORTAL</a>
            <a href="/" target="_self" class="cta-btn">TA KONTAKT</a>
        </div>
    </div>
""", unsafe_allow_html=True)

# =========================================================
# LOGIC: ALS DE GEBRUIKER NIET IS INGELOGD
# =========================================================
if st.session_state.user is None:
    
    st.markdown("<h2 style='text-align: center; color: #894b9d;'>Customer Portal</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666; margin-bottom: 30px;'>Log in to manage your shipments and details.</p>", unsafe_allow_html=True)

    with st.container(border=True):
        tab_login, tab_register = st.tabs(["🔒 Log In", "📝 Create Account"])

        # --- TAB 1: INLOGGEN ---
        with tab_login:
            st.write("")
            login_email = st.text_input("Email Address", key="log_email")
            login_pass = st.text_input("Password", type="password", key="log_pass")
            
            st.write("")
            if st.button("Log In", type="primary", use_container_width=True):
                if login_email and login_pass:
                    try:
                        auth_response = supabase.auth.sign_in_with_password({
                            "email": login_email,
                            "password": login_pass
                        })
                        st.session_state.user = auth_response.user
                        st.rerun()
                    except Exception as e:
                        st.error("❌ Incorrect email or password. Please try again.")
                else:
                    st.warning("⚠️ Please fill in both fields.")

        # --- TAB 2: ACCOUNT AANMAKEN ---
        with tab_register:
            st.write("")
            reg_company = st.text_input("Company Name *", key="reg_comp")
            
            c_fn, c_ln = st.columns(2)
            with c_fn: reg_fname = st.text_input("First Name *", key="reg_fn")
            with c_ln: reg_lname = st.text_input("Last Name *", key="reg_ln")
            
            reg_phone = st.text_input("Phone Number", key="reg_phone")
            st.write("---")
            reg_email = st.text_input("Email Address (This will be your login) *", key="reg_email")
            reg_pass = st.text_input("Choose a Password *", type="password", key="reg_pass")
            
            st.write("")
            if st.button("Create Account", type="primary", use_container_width=True):
                if reg_email and reg_pass and reg_company and reg_fname and reg_lname:
                    try:
                        auth_res = supabase.auth.sign_up({
                            "email": reg_email,
                            "password": reg_pass
                        })
                        
                        new_user_id = auth_res.user.id
                        full_name = f"{reg_fname} {reg_lname}"
                        
                        profile_data = {
                            "id": new_user_id,
                            "company_name": reg_company,
                            "contact_name": full_name,
                            "phone": reg_phone
                        }
                        supabase.table("profiles").insert(profile_data).execute()
                        
                        st.success("✅ Account created successfully! You can now log in via the 'Log In' tab.")
                        st.balloons()
                    except Exception as e:
                        if "already registered" in str(e).lower():
                            st.error("⚠️ This email address is already registered.")
                        else:
                            st.error(f"❌ An error occurred: {e}")
                else:
                    st.warning("⚠️ Please fill in all mandatory fields (*).")

# =========================================================
# LOGIC: ALS DE GEBRUIKER SUCCESVOL IS INGELOGD
# =========================================================
else:
    user_id = st.session_state.user.id
    try:
        prof_res = supabase.table("profiles").select("*").eq("id", user_id).execute()
        profile = prof_res.data[0] if prof_res.data else {}
    except:
        profile = {}

    company_name = profile.get("company_name", "Valued Customer")
    
    st.markdown(f"<h2 style='color: #894b9d;'>Welcome back, {company_name}!</h2>", unsafe_allow_html=True)
    st.write(f"Logged in as: {st.session_state.user.email}")
    
    st.write("---")
    st.info("🚧 Welcome to your dashboard! Here you will soon be able to see your active orders, past shipments, and update your company details.")
    
    st.write("")
    if st.button("🚪 Log Out", type="secondary"):
        supabase.auth.sign_out()
        st.session_state.user = None
        st.rerun()
