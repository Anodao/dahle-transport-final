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

if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "My Shipments"

if 'user' not in st.session_state:
    st.session_state.user = None

# =========================================================
# DE MAGIC FIX: DATABASE VOLLEDIG INLOGGEN VIA COOKIES
# =========================================================
acc_token = cookie_manager.get('dahle_acc')
ref_token = cookie_manager.get('dahle_ref')

if st.session_state.user is None and acc_token and ref_token:
    try:
        # Dit logt niet alleen de UI in, maar ook de database uitsmijter!
        session = supabase.auth.set_session(acc_token, ref_token)
        st.session_state.user = session.user
    except Exception:
        pass


# --- CSS STYLING & NAVBAR ---
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
    .nav-logo img { height: 48px; width: auto; transition: transform 0.2s; }
    .nav-links { display: flex; gap: 28px; font-size: 15px; font-weight: 500; justify-content: center; }
    .nav-links a, .nav-links span { text-decoration: none; color: #111111 !important; cursor: pointer; transition: color 0.2s;}
    .nav-links span:hover { color: #894b9d !important; }
    .nav-cta { display: flex; justify-content: flex-end; gap: 15px; }
    .cta-btn { background-color: #894b9d !important; color: white !important; padding: 10px 24px; border-radius: 50px; text-decoration: none !important; font-weight: 600; font-size: 13px; white-space: nowrap;}
    .cta-btn-outline { background-color: transparent !important; color: #894b9d !important; padding: 10px 20px; border-radius: 50px; text-decoration: none !important; font-weight: 600; font-size: 13px; border: 2px solid #894b9d; white-space: nowrap;}
    div[data-testid="stVerticalBlockBorderWrapper"] { background-color: #1e1e1e !important; border: 1px solid #333333 !important; border-radius: 12px !important; padding: 20px !important; }
    div[data-baseweb="input"] > div, div[data-baseweb="textarea"] { background-color: #333333 !important; border: 1px solid #444444 !important; border-radius: 6px !important; }
    div[data-baseweb="input"] input, div[data-baseweb="textarea"] textarea { color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; }
    label[data-testid="stWidgetLabel"] p { color: #cccccc !important; font-weight: 600; font-size: 14px !important;}
    div.stButton > button[kind="primary"] { background: linear-gradient(135deg, #b070c6 0%, #894b9d 100%) !important; color: #ffffff !important; border: none !important; border-radius: 6px !important; padding: 14px 28px !important; font-weight: 600 !important; font-size: 15px !important; width: 100% !important; box-shadow: 0 4px 14px 0 rgba(137, 75, 157, 0.4) !important; transition: all 0.3s ease !important; }
    div.stButton > button[kind="primary"]:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 24px rgba(137, 75, 157, 0.6) !important; }
    div.stButton > button[kind="secondary"] { background: transparent !important; color: #e0c2ed !important; border: 2px solid #894b9d !important; border-radius: 6px !important; padding: 14px 28px !important; font-weight: 600 !important; font-size: 15px !important; width: 100% !important; transition: all 0.3s ease !important; }
    div.stButton > button[kind="secondary"]:hover { background: #894b9d !important; color: white !important; transform: translateY(-2px) !important;}
    div[data-testid="stExpander"] { background-color: #262626 !important; border: 1px solid #444 !important; border-radius: 8px !important; }
    div[data-testid="stExpander"] p { color: #ffffff !important; }
    div[data-testid="stExpanderDetails"] { background-color: #1e1e1e !important; border-top: 1px solid #444 !important; }
    </style>
    <div class="navbar">
        <div class="nav-logo"><a href="/" target="_self"><img src="https://cloud-1de12d.becdn.net/media/original/964295c9ae8e693f8bb4d6b70862c2be/logo-website-top-png-1-.webp"></a></div>
        <div class="nav-links"><a href="/"><span>Hjem</span></a><span>Om oss</span><span>Tjenester</span><span>Galleri</span><span>Kontakt</span></div>
        <div class="nav-cta"><a href="/Login" target="_self" class="cta-btn-outline">KUNDEPORTAL</a><a href="/" target="_self" class="cta-btn">TA KONTAKT</a></div>
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

        with tab_login:
            st.write("")
            with st.form("login_form", clear_on_submit=False):
                login_email = st.text_input("Email Address", key="log_email")
                login_pass = st.text_input("Password", type="password", key="log_pass")
                st.write("")
                submitted = st.form_submit_button("Log In", type="primary", use_container_width=True)
            
            status_bericht = st.empty()
            
            if submitted:
                if login_email and login_pass:
                    status_bericht.info("Bezig met inloggen... ⏳")
                    try:
                        auth_response = supabase.auth.sign_in_with_password({
                            "email": login_email,
                            "password": login_pass
                        })
                        st.session_state.user = auth_response.user
                        
                        # SLA BEIDE TOKENS OP VOOR DE DATABASE UITSMIJTER
                        cookie_manager.set('dahle_acc', auth_response.session.access_token, key="set_a")
                        cookie_manager.set('dahle_ref', auth_response.session.refresh_token, key="set_r")
                        
                        status_bericht.success("✅ Succesvol ingelogd! Je wordt doorgestuurd...")
                        time.sleep(1.5) 
                        st.rerun()
                    except Exception as e:
                        status_bericht.error("❌ Incorrect email or password.")
                else:
                    status_bericht.warning("⚠️ Please fill in both fields.")

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
                    with st.spinner("Account wordt aangemaakt... ⏳"):
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
                        except Exception as e:
                            st.error(f"❌ An error occurred or email already exists.")
                else:
                    st.warning("⚠️ Please fill in all mandatory fields (*).")

# =========================================================
# LOGIC: ALS DE GEBRUIKER SUCCESVOL IS INGELOGD
# =========================================================
else:
    user_id = st.session_state.user.id
    
    # 1. Haal het profiel op
    try:
        prof_res = supabase.table("profiles").select("*").eq("id", user_id).execute()
        profile = prof_res.data[0] if prof_res.data else {}
    except Exception as e:
        profile = {}

    company_name = profile.get("company_name", "Valued Customer")
    contact_name = profile.get("contact_name", "")
    phone_nr = profile.get("phone", "")
    email_addr = st.session_state.user.email
    
    address = profile.get("address", "")
    zip_code = profile.get("zip_code", "")
    city = profile.get("city", "")
    del_address = profile.get("del_address", "")
    del_zip = profile.get("del_zip", "")
    del_city = profile.get("del_city", "")

    # 2. Haal orders op
    try:
        orders_res = supabase.table("orders").select("*").eq("user_id", user_id).order("id", desc=True).execute()
        user_orders = orders_res.data
    except Exception as e:
        user_orders = []

    total_orders = len(user_orders)
    pending_orders = sum(1 for o in user_orders if o['status'] == 'New')
    processed_orders = sum(1 for o in user_orders if o['status'] in ['Processed', 'Delivered'])

    # --- DASHBOARD HEADER ---
    c_head1, c_head2 = st.columns([3, 1])
    with c_head1:
        st.markdown(f"<h2 style='color: #b070c6; margin-bottom: 0px;'>Welcome back, {company_name}!</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #888; font-size: 14px;'>Logged in as: {email_addr}</p>", unsafe_allow_html=True)
    with c_head2:
        st.write("")
        if st.button("🚪 Log Out", type="secondary", use_container_width=True):
            cookie_manager.delete('dahle_acc', key="del_a")
            cookie_manager.delete('dahle_ref', key="del_r")
            supabase.auth.sign_out()
            st.session_state.user = None
            st.rerun()
            
    st.write("---")
    
    # =========================================================
    # VASTE DASHBOARD TITEL & STATISTIEKEN 
    # =========================================================
    st.markdown("### 📦 Your Shipment History")
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Shipments", total_orders)
    m2.metric("Pending Approval", pending_orders)
    m3.metric("Processed", processed_orders)
    st.write("---")

    # =========================================================
    # MENU NAVIGATIE KNOPPEN 
    # =========================================================
    col_menu1, col_menu2, col_menu3 = st.columns(3)
    with col_menu1:
        if st.button("📦 My Shipments", type="primary" if st.session_state.active_tab == "My Shipments" else "secondary", use_container_width=True):
            st.session_state.active_tab = "My Shipments"
            st.rerun()
    with col_menu2:
        if st.button("➕ New Order", type="secondary", use_container_width=True):
            st.switch_page("pages/Order.py")
    with col_menu3:
        if st.button("⚙️ Profile Settings", type="primary" if st.session_state.active_tab == "Profile Settings" else "secondary", use_container_width=True):
            st.session_state.active_tab = "Profile Settings"
            st.rerun()
    st.write("") 

    # =========================================================
    # CONTENT 1: ORDER HISTORIE
    # =========================================================
    if st.session_state.active_tab == "My Shipments":
        if not user_orders:
            st.info("📊 You haven't placed any orders with this account yet. Go to 'New Order' to get started!")
        else:
            for o in user_orders:
                status_icon = "🔵" if o['status'] == 'New' else "🟡" if o['status'] == 'In Progress' else "🟢" if o['status'] in ['Processed', 'Delivered'] else "🔴"
                with st.expander(f"{status_icon} Order #{o['id']} — {o.get('received_date', '')[:10]} (Status: {o['status']})"):
                    st.markdown("<br>", unsafe_allow_html=True)
                    c_det1, c_det2 = st.columns(2)
                    with c_det1:
                        st.markdown("#### 📤 Pickup Location")
                        st.write(f"**Adres:** {o.get('pickup_address', '-')}")
                        st.write(f"**Postcode:** {o.get('pickup_zip', '-')}")
                        st.write(f"**Stad:** {o.get('pickup_city', '-')}")
                        st.write("")
                        st.markdown("#### 📥 Delivery Destination")
                        st.write(f"**Adres:** {o.get('delivery_address', '-')}")
                        st.write(f"**Postcode:** {o.get('delivery_zip', '-')}")
                        st.write(f"**Stad:** {o.get('delivery_city', '-')}")
                    with c_det2:
                        st.markdown("#### 🚛 Services Requested")
                        st.write(f"{o.get('types', '-')}")
                        st.write("")
                        st.markdown("#### 📝 Additional Info")
                        st.write(f"{o.get('info', '-')}")
                    
                    if o['status'] == 'New':
                        st.write("---")
                        c_space1, c_cancel, c_space2 = st.columns([1, 2, 1])
                        with c_cancel:
                            if st.button("❌ Cancel This Order", key=f"cancel_{o['id']}", type="secondary", use_container_width=True):
                                try:
                                    supabase.table("orders").update({"status": "Cancelled"}).eq("id", o['id']).execute()
                                    st.success("✅ Your order has been cancelled successfully.")
                                    time.sleep(1)
                                    st.rerun()
                                except Exception as e:
                                    st.error("⚠️ Failed to cancel order.")
                        
                    st.markdown("<br>", unsafe_allow_html=True)

    # =========================================================
    # CONTENT 3: PROFIEL BEHEREN
    # =========================================================
    elif st.session_state.active_tab == "Profile Settings":
        st.markdown("### ⚙️ Manage Your Profile")
        st.markdown("<p style='color:#aaaaaa;'>Update your company and contact information here.</p>", unsafe_allow_html=True)
        
        with st.container(border=True):
            st.markdown("#### General Info")
            upd_company = st.text_input("Company Name", value=company_name, key="upd_comp")
            upd_contact = st.text_input("Contact Person", value=contact_name, key="upd_cont")
            upd_phone = st.text_input("Phone Number", value=phone_nr, key="upd_phone")
            st.text_input("Email Address (Login ID)", value=email_addr, disabled=True, key="upd_email")
            
            st.write("---")
            st.markdown("#### Default Pickup Location 📤")
            st.markdown("<p style='color:#888; font-size:13px;'>We use this to speed up your orders.</p>", unsafe_allow_html=True)
            upd_address = st.text_input("Street Address", value=address, key="upd_addr")
            col_zip, col_city = st.columns(2)
            with col_zip: upd_zip = st.text_input("Zip Code", value=zip_code, key="upd_zip")
            with col_city: upd_city = st.text_input("City", value=city, key="upd_city")
            
            st.write("---")
            st.markdown("#### Default Delivery Destination 📥")
            st.markdown("<p style='color:#888; font-size:13px;'>We use this to speed up your orders.</p>", unsafe_allow_html=True)
            upd_del_address = st.text_input("Street Address", value=del_address, key="upd_del_addr")
            col_d_zip, col_d_city = st.columns(2)
            with col_d_zip: upd_del_zip = st.text_input("Zip Code", value=del_zip, key="upd_del_zip")
            with col_d_city: upd_del_city = st.text_input("City", value=del_city, key="upd_del_city")
            
            st.write("")
            if st.button("💾 Save Changes", type="primary"):
                update_data = {
                    "company_name": upd_company,
                    "contact_name": upd_contact,
                    "phone": upd_phone,
                    "address": upd_address,
                    "zip_code": upd_zip,
                    "city": upd_city,
                    "del_address": upd_del_address,
                    "del_zip": upd_del_zip,
                    "del_city": upd_del_city
                }
                
                with st.spinner("Profiel wordt bijgewerkt... ⏳"):
                    try:
                        supabase.table("profiles").update(update_data).eq("id", user_id).execute()
                        st.success("✅ Profile updated successfully!")
                        time.sleep(1.5)
                        st.rerun() 
                    except Exception as e:
                        st.error(f"⚠️ Could not update profile: {e}")
