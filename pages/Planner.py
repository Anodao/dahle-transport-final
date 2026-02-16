import streamlit as st
import time

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Dahle Transport - Planner",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INITIALIZE STATE ---
# Voor de zekerheid checken of de orders bestaan, anders crasht de planner
if 'orders' not in st.session_state:
    st.session_state.orders = []
if 'selected_order' not in st.session_state:
    st.session_state.selected_order = None

# --- CSS STYLING VOOR DE PLANNER ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }
    
    /* Forceer de algemene tekstkleur naar donkergrijs/zwart, zodat het NOOIT wit-op-wit is */
    .stApp { background-color: #f4f6f9; }
    .block-container { padding-top: 2rem; }
    h1, h2, h3, h4, h5, h6 { color: #2c3e50 !important; }
    p, span, div { color: #34495e !important; }

    /* De donkerblauwe header banner bovenaan */
    .header-banner {
        background-color: #2c3e50;
        padding: 30px 40px;
        border-radius: 12px;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .header-banner h1 { color: #ffffff !important; margin: 0; font-weight: 700; letter-spacing: 0.5px;}
    .header-banner p { color: #bdc3c7 !important; margin: 5px 0 0 0; font-size: 14px;}

    /* Styling voor de lijst met orders links (Inbox) */
    .inbox-card {
        background-color: #ffffff;
        border: 1px solid #e0e6ed;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .inbox-title { color: #2c3e50 !important; font-weight: 700; font-size: 16px; margin: 0 0 8px 0; }
    .inbox-subtitle { color: #7f8c8d !important; font-size: 13px; margin: 0 0 8px 0; line-height: 1.4;}
    .inbox-date { color: #95a5a6 !important; font-size: 11px; margin: 0; }
    .status-new { color: #e74c3c !important; font-weight: 900; }
    
    /* Styling voor de order details rechts */
    .detail-box {
        background-color: #ffffff;
        border: 1px solid #e0e6ed;
        border-radius: 8px;
        padding: 30px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .detail-label { color: #95a5a6 !important; font-size: 11px; font-weight: 700; text-transform: uppercase; margin-bottom: 2px; letter-spacing: 0.5px;}
    .detail-value { color: #2c3e50 !important; font-size: 15px; font-weight: 500; margin-bottom: 20px;}
    .detail-header { border-bottom: 2px solid #f0f3f6; padding-bottom: 10px; margin-bottom: 20px; margin-top: 20px;}
    
    /* Terug knop naar home */
    .home-link { text-align: right; margin-bottom: 20px; }
    
    /* Streamlit Knoppen fix voor planner */
    div.stButton > button { background-color: #2c3e50 !important; color: white !important; border: none; font-weight: bold; border-radius: 6px;}
    div.stButton > button:hover { background-color: #1a252f !important; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER BANNER ---
st.markdown("""
    <div class="header-banner">
        <h1>🔒 Planner Dashboard</h1>
        <p>Internal Use Only</p>
    </div>
""", unsafe_allow_html=True)

# Link om makkelijk terug te navigeren naar de klant-website
st.markdown('<div class="home-link">', unsafe_allow_html=True)
st.page_link("Home.py", label="← Go Back to Customer Website", icon="🏠")
st.markdown('</div>', unsafe_allow_html=True)

# --- LAYOUT VERDELING ---
col_inbox, col_details = st.columns([1, 2], gap="large")

# =========================================================
# LINKER KOLOM: INBOX
# =========================================================
with col_inbox:
    st.markdown("### 📥 Inbox")
    st.write("") # Extra ruimte
    
    if not st.session_state.orders:
        st.info("No new requests at the moment. Waiting for customers...")
    else:
        # We draaien de lijst om zodat de nieuwste order bovenaan staat
        for o in reversed(st.session_state.orders): 
            with st.container():
                st.markdown(f"""
                    <div class="inbox-card">
                        <p class="inbox-title"><span class="status-new">🔴 New</span> &nbsp; {o.get('company', 'Unknown')}</p>
                        <p class="inbox-subtitle">{o.get('type', '')}</p>
                        <p class="inbox-date">Received: {o.get('date', '')}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                # Een Streamlit knop om de details te openen
                if st.button(f"Open Order #{o.get('id', '0000')}", key=f"btn_{o.get('id')}", use_container_width=True):
                    st.session_state.selected_order = o
                    st.rerun()

# =========================================================
# RECHTER KOLOM: ORDER DETAILS
# =========================================================
with col_details:
    st.markdown("### 📋 Order Details")
    st.write("")
    selected = st.session_state.selected_order
    
    if not selected:
        # Als er nog niets is aangeklikt
        st.markdown("""
            <div class="detail-box" style="text-align: center; padding: 60px; background-color: #f8f9fa;">
                <h2 style="color: #bdc3c7 !important;">No order selected</h2>
                <p style="color: #95a5a6 !important;">Click on an order in the inbox to view the full details here.</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        # Haal de data veilig op
        company = selected.get('company', 'N/A')
        reg_no = selected.get('reg_no', 'N/A')
        address = selected.get('address', 'N/A')
        contact_name = selected.get('contact_name', 'N/A')
        email = selected.get('email', 'N/A')
        phone = selected.get('phone', 'N/A')
        info = selected.get('info', 'None provided')
        s_type = selected.get('type', 'N/A')
        date = selected.get('date', 'N/A')
        order_id = selected.get('id', 'N/A')
        
        # Lege info netjes afvangen
        if not info.strip():
            info = "None provided."
        if not reg_no.strip():
            reg_no = "Not provided."

        st.markdown(f"""
            <div class="detail-box">
                <h2 style="margin-top:0;">Order #{order_id}</h2>
                <p style="color: #95a5a6 !important; font-size: 13px; margin-bottom: 25px;">Received on {date}</p>
                
                <h4 class="detail-header">🏢 Company Information</h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr;">
                    <div>
                        <p class="detail-label">Company Name</p>
                        <p class="detail-value">{company}</p>
                    </div>
                    <div>
                        <p class="detail-label">Registration No.</p>
                        <p class="detail-value">{reg_no}</p>
                    </div>
                </div>
                <p class="detail-label">Registered Address</p>
                <p class="detail-value">{address}</p>
                
                <h4 class="detail-header">👤 Contact Person</h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr;">
                    <div>
                        <p class="detail-label">Name</p>
                        <p class="detail-value">{contact_name}</p>
                    </div>
                    <div>
                        <p class="detail-label">Phone</p>
                        <p class="detail-value">{phone}</p>
                    </div>
                </div>
                <p class="detail-label">Email Address</p>
                <p class="detail-value"><a href="mailto:{email}" style="color: #2980b9;">{email}</a></p>
                
                <h4 class="detail-header">📦 Shipment Details</h4>
                <p class="detail-label">Requested Services</p>
                <p class="detail-value" style="font-weight: 700;">{s_type}</p>
                
                <p class="detail-label">Additional Instructions / Details</p>
                <p class="detail-value" style="background-color: #f4f6f9; padding: 15px; border-radius: 6px; font-size: 14px;">{info}</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        c_btn1, c_btn2, c_space = st.columns([2, 2, 3])
        with c_btn1:
            if st.button("✅ Mark as Processed", use_container_width=True):
                # Verwijdert de order uit het systeem voor de demo
                st.session_state.orders = [o for o in st.session_state.orders if o['id'] != order_id]
                st.session_state.selected_order = None
                st.success("Order has been successfully processed!")
                time.sleep(1.5)
                st.rerun()
        with c_btn2:
            # Optioneel verwijderen knopje
            if st.button("🗑️ Delete", type="secondary", use_container_width=True):
                st.session_state.orders = [o for o in st.session_state.orders if o['id'] != order_id]
                st.session_state.selected_order = None
                st.rerun()
