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

# --- CSS STYLING & NAVBAR (DARK MODE) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }
    
    /* Verberg standaard elementen */
    [data-testid="collapsedControl"], [data-testid="stSidebar"], header[data-testid="stHeader"] { display: none !important; }
    
    /* --- DARK THEME ACHTERGROND --- */
    .stApp { background-color: #111111 !important; }
    .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: #ffffff !important; }
    div[data-testid="stMetricValue"], div[data-testid="stMetricLabel"] { color: #ffffff !important; }

    /* --- NAVBAR (WIT MET ZWARTE TEKST) --- */
    .block-container { padding-top: 130px !important; max-width: 900px; }
    .navbar {
        position: fixed; top: 0; left: 0; width: 100%; height: 90px;
        background-color: #ffffff !important; z-index: 999; border-bottom: 1px solid #eaeaea; 
        display: grid; grid-template-columns: 1fr auto 1fr; align-items: center;
        padding: 0 40px; box-shadow: 0 2px 10px rgba(0,0,0,0.03);
    }
    .nav-logo img { height: 48px; width: auto; transition: transform 0.2s; }
    .nav-links { display: flex; gap: 28px; font-size: 15px; font-weight: 500; justify-content: center; }
    .nav-links a, .nav-links span { text-decoration: none; color: #111111 !important; cursor: pointer; transition: color 0.2s;}
    .nav-links span:hover { color: #894b9d !important; }
    .nav-cta { display: flex; justify-content: flex-end; gap: 15px; }
    .cta-btn { background-color: #894b9d !important; color: white !important; padding: 10px 24px; border-radius: 50px; text-decoration: none !important; font-weight: 600; font-size: 13px; white-space: nowrap;}
    .cta-btn-outline { background-color: transparent !important; color: #894b9d !important; padding: 10px 20px; border-radius: 50px; text-decoration: none !important; font-weight: 600; font-size: 13px; border: 2px solid #894b9d; white-space: nowrap;}

    /* --- FORM & CONTAINER STYLING VOOR DARK MODE --- */
    div[data-testid="stVerticalBlockBorderWrapper"] { background-color: #1e1e1e !important; border: 1px solid #333333 !important; border-radius: 12px !important; padding: 20px !important; }
    div[data-baseweb="input"] > div { background-color: #333333 !important; border: 1px solid #444444 !important; border-radius: 6px !important; }
    div[data-baseweb="input"] input { color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; }
    label[data-testid="stWidgetLabel"] p { color: #cccccc !important; font-weight: 600; font-size: 14px !important;}
    
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
        background: transparent !important; color: #e0c2ed !important; border: 2px solid #894b9d !important; border-radius: 6px !important; 
        padding: 14px 28px !important; font-weight: 600 !important; font-size: 15px !important;
        width: 100% !important; transition: all 0.3s ease !important;
    }
    div.stButton > button[kind="secondary"]:hover { background: #894b9d !important; color: white !important; transform: translateY(-2px) !important;}

    /* Tabs styling */
    button[data-baseweb="tab"] { background-color: transparent !important; color: #888888 !important; font-weight: 600; font-size: 16px;}
    button[data-baseweb="tab"][aria-selected="true"] { color: #b070c6 !important; border-bottom: 3px solid #b070c6 !important; }
    
    /* Expander styling */
    div[data-testid="stExpander"] { background-color: #262626 !important; border: 1px solid #444 !important; border-radius: 8px !important; }
    div[data-testid="stExpander"] p { color: #ffffff !important; }
    div[data-testid="stExpanderDetails"] { background-color: #1e1e1e !important; border-top: 1px solid #444 !important; }
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
    
    st.markdown("<h2 style='text-align: center; color: #b070c6;'>Customer Portal</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #aaaaaa; margin-bottom: 30px;'>Log in to manage your shipments and details.</p>", unsafe_allow_html=True)

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
    
    # --- DASHBOARD HEADER ---
    c_head1, c_head2 = st.columns([3, 1])
    with c_head1:
        st.markdown(f"<h2 style='color: #b070c6; margin-bottom: 0px;'>Welcome back, {company_name}!</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #888; font-size: 14px;'>Logged in as: {st.session_state.user.email}</p>", unsafe_allow_html=True)
    with c_head2:
        st.write("")
        if st.button("🚪 Log Out", type="secondary", use_container_width=True):
            supabase.auth.sign_out()
            st.session_state.user = None
            st.rerun()
            
    st.write("---")
    
    # --- DASHBOARD TABS ---
    tab_history, tab_new_order, tab_profile = st.tabs(["📦 My Shipments", "➕ New Order", "⚙️ Profile Settings"])

    # --- TAB 1: ORDER HISTORIE ---
    with tab_history:
        st.markdown("### Your Shipment History")
        
        # Haal ALLEEN de orders op van deze specifieke ingelogde gebruiker
        try:
            orders_res = supabase.table("orders").select("*").eq("user_id", user_id).order("id", desc=True).execute()
            user_orders = orders_res.data
        except Exception as e:
            st.error("Could not fetch orders at this time.")
            user_orders = []

        if not user_orders:
            st.info("📊 You haven't placed any orders with this account yet. Go to 'New Order' to get started!")
        else:
            # Genereer de metrics
            total_orders = len(user_orders)
            pending_orders = sum(1 for o in user_orders if o['status'] == 'New')
            processed_orders = sum(1 for o in user_orders if o['status'] == 'Processed')
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Total Shipments", total_orders)
            m2.metric("Pending Approval", pending_orders)
            m3.metric("Processed", processed_orders)
            
            st.write("---")
            
            # Laat de orders zien in inklapbare balken (Expanders)
            for o in user_orders:
                # Bepaal het icoon/kleur op basis van de status
                status_icon = "🔴" if o['status'] == 'New' else "🟢"
                
                with st.expander(f"{status_icon} Order #{o['id']} — {o.get('received_date', '')[:10]} (Status: {o['status']})"):
                    st.markdown("<br>", unsafe_allow_html=True)
                    c_det1, c_det2 = st.columns(2)
                    
                    with c_det1:
                        st.markdown("**📤 Pickup:**")
                        st.write(f"{o.get('pickup_address', '')}, {o.get('pickup_city', '')}")
                        st.write("")
                        st.markdown("**📥 Delivery:**")
                        st.write(f"{o.get('delivery_address', '')}, {o.get('delivery_city', '')}")
                        
                    with c_det2:
                        st.markdown("**🚛 Services Requested:**")
                        st.write(f"{o.get('types', '')}")
                        st.write("")
                        if o.get('info'):
                            st.markdown("**📝 Additional Info:**")
                            st.write(f"{o.get('info')}")
                    
                    st.markdown("<br>", unsafe_allow_html=True)

    # --- TAB 2: NIEUWE ORDER (Placeholder) ---
    with tab_new_order:
        st.markdown("### Quick Order Form")
        st.info("🚧 This feature is currently under construction. Soon you will be able to book shipments directly from here without filling in your company details again!")

    # --- TAB 3: PROFIEL (Placeholder) ---
    with tab_profile:
        st.markdown("### Manage Your Profile")
        st.info("🚧 Profile management will be available shortly.")
