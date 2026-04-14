import streamlit as st
import time
from datetime import datetime
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

import extra_streamlit_components as stx
from datetime import datetime, timedelta

# --- COOKIE MANAGER ---
cookie_manager = stx.CookieManager()

# --- INITIALIZE SESSION STATE ---
if 'user' not in st.session_state:
    # Check of er nog een actieve sessie in de 'achtergrond' leeft bij Supabase
    session = supabase.auth.get_session()
    if session:
        st.session_state.user = session.user
    else:
        st.session_state.user = None

# ANTI-DUBBELKLIK GEHEUGEN VOOR ORDERS
if 'last_order_signature' not in st.session_state:
    st.session_state.last_order_signature = None

# --- HERSTEL SESSIE UIT COOKIE (als nog niet ingelogd) ---
if st.session_state.user is None:
    access_token = cookie_manager.get("sb_access_token")
    refresh_token = cookie_manager.get("sb_refresh_token")
    
    if access_token and refresh_token:
        try:
            session = supabase.auth.set_session(access_token, refresh_token)
            st.session_state.user = session.user
        except Exception:
            cookie_manager.delete("sb_access_token")
            cookie_manager.delete("sb_refresh_token")

# --- CSS STYLING & NAVBAR (DARK MODE) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }
    
    /* Verberg standaard elementen */
    [data-testid="collapsedControl"], [data-testid="stSidebar"], header[data-testid="stHeader"] { display: none !important; }
    
    /* --- DARK THEME ACHTERGROND --- */
    .stApp { background-color: #111111 !important; }
    .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown li { color: #ffffff !important; }
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
    div[data-baseweb="input"] > div, div[data-baseweb="textarea"] { background-color: #333333 !important; border: 1px solid #444444 !important; border-radius: 6px !important; }
    div[data-baseweb="input"] input, div[data-baseweb="textarea"] textarea { color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; }
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
    contact_name = profile.get("contact_name", "")
    phone_nr = profile.get("phone", "")
    email_addr = st.session_state.user.email
    
    # Haal extra adres velden op (als ze nog niet bestaan, geeft hij een lege string terug)
    address = profile.get("address", "")
    zip_code = profile.get("zip_code", "")
    city = profile.get("city", "")
    country = profile.get("country", "")
    
    # --- DASHBOARD HEADER ---
    c_head1, c_head2 = st.columns([3, 1])
    with c_head1:
        st.markdown(f"<h2 style='color: #b070c6; margin-bottom: 0px;'>Welcome back, {company_name}!</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #888; font-size: 14px;'>Logged in as: {email_addr}</p>", unsafe_allow_html=True)
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
        
        try:
            orders_res = supabase.table("orders").select("*").eq("user_id", user_id).order("id", desc=True).execute()
            user_orders = orders_res.data
        except Exception as e:
            st.error("Could not fetch orders at this time.")
            user_orders = []

        if not user_orders:
            st.info("📊 You haven't placed any orders with this account yet. Go to 'New Order' to get started!")
        else:
            total_orders = len(user_orders)
            pending_orders = sum(1 for o in user_orders if o['status'] == 'New')
            processed_orders = sum(1 for o in user_orders if o['status'] in ['Processed', 'Delivered'])
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Total Shipments", total_orders)
            m2.metric("Pending Approval", pending_orders)
            m3.metric("Processed", processed_orders)
            
            st.write("---")
            
            for o in user_orders:
                # LOGICA VOOR DE JUISTE KLEUR BOLLETJES
                if o['status'] == 'New':
                    status_icon = "🔵"
                elif o['status'] == 'In Progress':
                    status_icon = "🟡"
                elif o['status'] in ['Processed', 'Delivered']:
                    status_icon = "🟢"
                elif o['status'] == 'Cancelled':
                    status_icon = "🔴"
                else:
                    status_icon = "⚪"

                with st.expander(f"{status_icon} Order #{o['id']} — {o.get('received_date', '')[:10]} (Status: {o['status']})"):
                    st.markdown("<br>", unsafe_allow_html=True)
                    c_det1, c_det2 = st.columns(2)
                    
                    # LOGICA VOOR STRAKKE ADRES WEERGAVE
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
                        
                    st.markdown("<br>", unsafe_allow_html=True)

    # --- TAB 2: NIEUWE ORDER (Snel Bestellen) ---
    with tab_new_order:
        st.markdown("### Quick Order Form")
        st.markdown(f"<p style='color:#aaaaaa;'>Book a new shipment. Your details (<b>{company_name}</b>) are automatically attached.</p>", unsafe_allow_html=True)
        
        with st.container(border=True):
            st.markdown("#### 1. What are you shipping?")
            
            c_ship1, c_ship2, c_ship3 = st.columns(3)
            with c_ship1: q_parcels = st.checkbox("Parcels & Documents", key="q_parcels")
            with c_ship2: q_freight = st.checkbox("Cargo & Freight", key="q_freight")
            with c_ship3: q_mail = st.checkbox("Mail & Marketing", key="q_mail")
            
            q_load_types = []
            if q_freight:
                st.markdown("<p style='color:#b070c6; font-size:14px; font-weight:600;'>Select Freight Options:</p>", unsafe_allow_html=True)
                fc1, fc2, fc3 = st.columns(3)
                with fc1: q_pal = st.checkbox("Pallet", key="q_pal")
                with fc2: q_full = st.checkbox("Full Container/Truck", key="q_full")
                with fc3: q_lc = st.checkbox("Loose Cargo", key="q_lc")
                if q_pal: q_load_types.append("Pallet")
                if q_full: q_load_types.append("Full Container")
                if q_lc: q_load_types.append("Loose Cargo")
            
            st.write("---")
            st.markdown("#### 2. Route Information")
            rc1, rc2 = st.columns(2, gap="large")
            with rc1:
                st.markdown("**📤 Pickup Location**")
                q_p_address = st.text_input("Address *", value=address, key="q_p_add")
                q_p_zip = st.text_input("Zip Code *", value=zip_code, key="q_p_zip")
                q_p_city = st.text_input("City *", value=city, key="q_p_city")
            with rc2:
                st.markdown("**📥 Delivery Destination**")
                q_d_address = st.text_input("Address *", key="q_d_add")
                q_d_zip = st.text_input("Zip Code *", key="q_d_zip")
                q_d_city = st.text_input("City *", key="q_d_city")
            
            st.write("---")
            st.markdown("#### 3. Order Specifications")
            q_info = st.text_area("Describe what you ship, approx. weight, special requirements, etc.", key="q_info")
            
            st.write("")
            if st.button("🚀 Submit Quick Order", type="primary", use_container_width=True):
                selected_types = []
                if q_parcels: selected_types.append("Parcels & Documents")
                if q_freight: selected_types.append("Cargo & Freight")
                if q_mail: selected_types.append("Mail & Direct Marketing")
                
                if not selected_types:
                    st.error("⚠️ Please select at least one shipment type.")
                elif not (q_p_address and q_p_zip and q_p_city and q_d_address and q_d_zip and q_d_city):
                    st.error("⚠️ Please fill in all the Route Information fields.")
                else:
                    compiled_info = q_info + "\n\n--- Quick Order Specs ---\n" if q_info else "--- Quick Order Specs ---\n"
                    if q_freight and q_load_types:
                        compiled_info += f"🚛 Freight Load: {', '.join(q_load_types)}\n"
                        
                    # LOGICA: UNIEKE STEMPEL MAKEN VOOR ANTI-DUBBELKLIK
                    current_signature = f"{q_p_address}-{q_d_address}-{compiled_info}"
                    
                    if st.session_state.last_order_signature == current_signature:
                        st.warning("⏳ Je hebt deze exacte order zojuist al verstuurd! We hebben hem in goede orde ontvangen.")
                    else:
                        db_order = {
                            "company": company_name,
                            "reg_no": "",  
                            "address": f"{q_p_address}, {q_p_zip} {q_p_city}",
                            "contact_name": contact_name,
                            "email": email_addr,
                            "phone": phone_nr,
                            "types": ", ".join(selected_types),
                            "info": compiled_info,
                            "status": "New",
                            "received_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "pickup_address": q_p_address,
                            "pickup_zip": q_p_zip,
                            "pickup_city": q_p_city,
                            "delivery_address": q_d_address,
                            "delivery_zip": q_d_zip,
                            "delivery_city": q_d_city,
                            "user_id": user_id 
                        }
                        
                        try:
                            supabase.table("orders").insert(db_order).execute()
                            st.session_state.last_order_signature = current_signature
                            st.success("🎉 Order submitted successfully! You can see it in your 'My Shipments' tab.")
                            # st.rerun() en st.balloons() zijn hier verwijderd zodat de melding blijft staan!
                        except Exception as e:
                            st.error(f"⚠️ Failed to send order. Error: {e}")

    # --- TAB 3: PROFIEL BEHEREN ---
    with tab_profile:
        st.markdown("### Manage Your Profile")
        st.markdown("<p style='color:#aaaaaa;'>Update your company and contact information here.</p>", unsafe_allow_html=True)
        
        with st.container(border=True):
            st.markdown("#### General Info")
            upd_company = st.text_input("Company Name", value=company_name, key="upd_comp")
            upd_contact = st.text_input("Contact Person", value=contact_name, key="upd_cont")
            upd_phone = st.text_input("Phone Number", value=phone_nr, key="upd_phone")
            
            # E-mail kan niet zomaar gewijzigd worden (zit vast aan Auth)
            st.text_input("Email Address (Login ID)", value=email_addr, disabled=True, key="upd_email")
            
            st.write("---")
            st.markdown("#### Address Details (Default Pickup)")
            st.markdown("<p style='color:#888; font-size:13px;'>We use this as your default pickup location to speed up your orders.</p>", unsafe_allow_html=True)
            
            upd_address = st.text_input("Street Address", value=address, key="upd_addr")
            col_zip, col_city = st.columns(2)
            with col_zip: upd_zip = st.text_input("Zip Code", value=zip_code, key="upd_zip")
            with col_city: upd_city = st.text_input("City", value=city, key="upd_city")
            upd_country = st.text_input("Country", value=country if country else "Norway", key="upd_country")
            
            st.write("")
            if st.button("💾 Save Changes", type="primary"):
                update_data = {
                    "company_name": upd_company,
                    "contact_name": upd_contact,
                    "phone": upd_phone,
                    "address": upd_address,
                    "zip_code": upd_zip,
                    "city": upd_city,
                    "country": upd_country
                }
                
                try:
                    # Update de profiles tabel met de nieuwe data, pas dit alleen toe op de ingelogde user
                    supabase.table("profiles").update(update_data).eq("id", user_id).execute()
                    st.success("✅ Profile updated successfully!")
                    time.sleep(1)
                    st.rerun() # Pagina herladen om nieuwe namen in de header te zetten
                except Exception as e:
                    st.error(f"⚠️ Could not update profile: {e}")
