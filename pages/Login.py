import streamlit as st
import time
from datetime import datetime
from supabase import create_client
import extra_streamlit_components as stx

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Dahle Transport - Customer Portal",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- INIT COOKIE MANAGER ---
cookie_manager = stx.CookieManager()

# --- SUPABASE CONNECTIE ---
def init_connection():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

if 'supabase_client' not in st.session_state:
    try:
        st.session_state.supabase_client = init_connection()
    except Exception as e:
        st.error("⚠️ Database connection failed.")
        st.stop()

supabase = st.session_state.supabase_client

# --- INITIALIZE SESSION STATE ---
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "My Shipments"

if 'user' not in st.session_state:
    st.session_state.user = None

# --- HERSTEL SESSIE VIA COOKIES ---
saved_token = cookie_manager.get('dahle_token')

if st.session_state.user is None and saved_token:
    try:
        user_response = supabase.auth.get_user(saved_token)
        st.session_state.user = user_response.user
    except Exception:
        pass

# --- CSS STYLING (Hetzelfde gebleven) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }
    [data-testid="collapsedControl"], [data-testid="stSidebar"], header[data-testid="stHeader"] { display: none !important; }
    .stApp { background-color: #111111 !important; }
    .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown li { color: #ffffff !important; }
    div[data-testid="stMetricValue"], div[data-testid="stMetricLabel"] { color: #ffffff !important; }
    .block-container { padding-top: 130px !important; max-width: 900px; }
    .navbar {
        position: fixed; top: 0; left: 0; width: 100%; height: 90px;
        background-color: #ffffff !important; z-index: 999; border-bottom: 1px solid #eaeaea; 
        display: grid; grid-template-columns: 1fr auto 1fr; align-items: center;
        padding: 0 40px; box-shadow: 0 2px 10px rgba(0,0,0,0.03);
    }
    .nav-logo img { height: 48px; width: auto; }
    .nav-links { display: flex; gap: 28px; font-size: 15px; font-weight: 500; justify-content: center; }
    .nav-links a, .nav-links span { text-decoration: none; color: #111111 !important; }
    .nav-cta { display: flex; justify-content: flex-end; gap: 15px; }
    .cta-btn { background-color: #894b9d !important; color: white !important; padding: 10px 24px; border-radius: 50px; font-weight: 600; font-size: 13px; text-decoration: none;}
    .cta-btn-outline { background-color: transparent !important; color: #894b9d !important; padding: 10px 20px; border-radius: 50px; font-weight: 600; font-size: 13px; border: 2px solid #894b9d; text-decoration: none;}
    div[data-testid="stVerticalBlockBorderWrapper"] { background-color: #1e1e1e !important; border: 1px solid #333333 !important; border-radius: 12px !important; padding: 20px !important; }
    div[data-baseweb="input"] > div, div[data-baseweb="textarea"] { background-color: #333333 !important; border: 1px solid #444444 !important; }
    div[data-baseweb="input"] input, div[data-baseweb="textarea"] textarea { color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; }
    label[data-testid="stWidgetLabel"] p { color: #cccccc !important; font-weight: 600; }
    div.stButton > button[kind="primary"] { background: linear-gradient(135deg, #b070c6 0%, #894b9d 100%) !important; color: white !important; width: 100% !important; }
    div.stButton > button[kind="secondary"] { background: transparent !important; color: #e0c2ed !important; border: 2px solid #894b9d !important; width: 100% !important; }
    </style>
    <div class="navbar">
        <div class="nav-logo"><a href="/" target="_self"><img src="https://cloud-1de12d.becdn.net/media/original/964295c9ae8e693f8bb4d6b70862c2be/logo-website-top-png-1-.webp"></a></div>
        <div class="nav-links"><a href="/"><span>Hjem</span></a><span>Om oss</span><span>Tjenester</span><span>Galleri</span><span>Kontakt</span></div>
        <div class="nav-cta"><a href="/Login" target="_self" class="cta-btn-outline">KUNDEPORTAL</a><a href="/" target="_self" class="cta-btn">TA KONTAKT</a></div>
    </div>
""", unsafe_allow_html=True)

# --- LOGIN / DASHBOARD LOGIC ---
if st.session_state.user is None:
    st.markdown("<h2 style='text-align: center; color: #b070c6;'>Customer Portal</h2>", unsafe_allow_html=True)
    with st.container(border=True):
        tab_login, tab_register = st.tabs(["🔒 Log In", "📝 Create Account"])
        with tab_login:
            with st.form("login_form"):
                login_email = st.text_input("Email Address")
                login_pass = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Log In", type="primary")
            if submitted:
                try:
                    res = supabase.auth.sign_in_with_password({"email": login_email, "password": login_pass})
                    st.session_state.user = res.user
                    cookie_manager.set('dahle_token', res.session.access_token)
                    st.rerun()
                except:
                    st.error("❌ Login failed.")
        
        with tab_register:
            # (Registratie code blijft hetzelfde als voorheen)
            st.info("Vul alle velden in om een account aan te maken.")
            # ... (Rest van registratie formulier)

else:
    user_id = st.session_state.user.id
    email_addr = st.session_state.user.email

    # 1. Haal profiel op met extra check
    profile = {}
    try:
        prof_res = supabase.table("profiles").select("*").eq("id", user_id).execute()
        if prof_res.data:
            profile = prof_res.data[0]
        else:
            st.warning("⚠️ Geen profiel gevonden in de database. Vul je gegevens hieronder in en klik op 'Save' om je profiel aan te maken.")
    except Exception as e:
        st.error(f"Fout bij ophalen: {e}")

    # --- DASHBOARD HEADER ---
    st.markdown(f"## Welcome back!")
    if st.button("🚪 Log Out", type="secondary"):
        cookie_manager.delete('dahle_token')
        supabase.auth.sign_out()
        st.session_state.user = None
        st.rerun()

    # --- TABS ---
    t1, t2 = st.tabs(["📦 My Shipments", "⚙️ Profile Settings"])

    with t1:
        st.write("Jouw zendingen verschijnen hier.")

    with t2:
        st.markdown("### Profile Details")
        # We gebruiken .get() om te voorkomen dat de app crasht als data mist
        company = st.text_input("Company Name", value=profile.get("company_name", ""))
        contact = st.text_input("Contact Person", value=profile.get("contact_name", ""))
        phone = st.text_input("Phone Number", value=profile.get("phone", ""))
        
        st.write("---")
        st.markdown("#### Default Address")
        addr = st.text_input("Street Address", value=profile.get("address", ""))
        zip_c = st.text_input("Zip Code", value=profile.get("zip_code", ""))
        city = st.text_input("City", value=profile.get("city", ""))

        if st.button("💾 Save Profile Changes", type="primary"):
            # UPSERT: Dit is de fix. Het maakt de rij aan als deze niet bestaat.
            new_data = {
                "id": user_id, # ID moet mee voor upsert
                "company_name": company,
                "contact_name": contact,
                "phone": phone,
                "address": addr,
                "zip_code": zip_c,
                "city": city
            }
            try:
                with st.spinner("Opslaan..."):
                    supabase.table("profiles").upsert(new_data).execute()
                    st.success("✅ Profiel succesvol opgeslagen!")
                    time.sleep(1)
                    st.rerun()
            except Exception as e:
                st.error(f"Fout bij opslaan: {e}")
