import streamlit as st
import time

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Dahle Transport - Planner",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- INITIALIZE STATE ---
if 'orders' not in st.session_state:
    st.session_state.orders = []
if 'selected_order' not in st.session_state:
    st.session_state.selected_order = None

# --- CSS STYLING VOOR DE PLANNER ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }
    
    /* Verberg de sidebar en knoppen volledig */
    [data-testid="collapsedControl"] { display: none !important; }
    [data-testid="stSidebar"] { display: none !important; }
    header[data-testid="stHeader"] { display: none !important; }
    
    /* Algemene achtergrond voor de planner */
    .stApp { background-color: #f8f9fa !important; }
    .block-container { padding-top: 2rem; }

    /* De donkerpaarse Dahle Transport header banner bovenaan */
    .header-banner {
        background-color: #894b9d; /* DAHLE PAARS */
        padding: 30px 40px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .header-banner h1 { color: #ffffff !important; margin: 0; font-weight: 700; letter-spacing: 0.5px;}
    .header-banner p { color: #e0d0e6 !important; margin: 5px 0 0 0; font-size: 14px;}

    /* Styling voor de lijst met orders links (Inbox) */
    .inbox-card {
        background-color: #ffffff !important;
        border: 1px solid #e0e6ed !important;
        border-radius: 8px !important;
        padding: 20px !important;
        margin-bottom: 15px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
    }
    .inbox-title { color: #333333 !important; font-weight: 700; font-size: 16px; margin: 0 0 8px 0; }
    .inbox-subtitle { color: #666666 !important; font-size: 13px; margin: 0 0 8px 0; line-height: 1.4;}
    .inbox-date { color: #888888 !important; font-size: 11px; margin: 0; }
    .status-new { color: #e74c3c !important; font-weight: 900; }
    
    /* Custom styling voor de details in de box rechts */
    .detail-label { color: #888888 !important; font-size: 12px; font-weight: 700; text-transform: uppercase; margin-bottom: 0px !important; letter-spacing: 0.5px;}
    .detail-value { color: #333333 !important; font-size: 16px; font-weight: 500; margin-top: 2px !important; margin-bottom: 15px !important;}
    
    /* Container voor de 'Go Back' knop */
    .home-btn-container { margin-bottom: 30px; }
    
    /* Streamlit Knoppen fix voor planner (Dahle Paars) */
    div.stButton > button { background-color: #894b9d !important; color: white !important; border: none; font-weight: bold; border-radius: 6px;}
    div.stButton > button:hover { background-color: #723e83 !important; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER BANNER ---
st.markdown("""
<div class="header-banner">
    <h1>🔒 Planner Dashboard</h1>
    <p>Internal Use Only</p>
</div>
""", unsafe_allow_html=True)

# --- ECHTE KNOP NAAR HOME ---
st.markdown('<div class="home-btn-container">', unsafe_allow_html=True)
if st.button("🏠 ← Go Back to Customer Website"):
    st.switch_page("Home.py")
st.markdown('</div>', unsafe_allow_html=True)

# --- LAYOUT VERDELING ---
col_inbox, col_details = st.columns([1, 2], gap="large")

# =========================================================
# LINKER KOLOM: INBOX
# =========================================================
with col_inbox:
    st.markdown("<h3 style='color:#333333;'>📥 Inbox</h3>", unsafe_allow_html=True)
    st.write("") 
    
    if not st.session_state.orders:
        st.info("No new requests at the moment. Waiting for customers...")
    else:
        for o in reversed(st.session_state.orders): 
            st.markdown(f"""
                <div class="inbox-card">
                    <p class="inbox-title"><span class="status-new">🔴 New</span> &nbsp; {o.get('company', 'Unknown')}</p>
                    <p class="inbox-subtitle">{o.get('type', '')}</p>
                    <p class="inbox-date">Received: {o.get('date', '')}</p>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Open Order #{o.get('id', '0000')}", key=f"btn_{o.get('id')}", use_container_width=True):
                st.session_state.selected_order = o
                st.rerun()

# =========================================================
# RECHTER KOLOM: ORDER DETAILS (NU VOLLEDIG STREAMLIT NATIVE)
# =========================================================
with col_details:
    st.markdown("<h3 style='color:#333333;'>📋 Order Details</h3>", unsafe_allow_html=True)
    
    selected = st.session_state.selected_order
    
    if not selected:
        st.info("Click on an order in the inbox to view the full details here.")
    else:
        # Haal de data veilig op
        company = selected.get('company', 'N/A')
        reg_no = selected.get('reg_no', '')
        if not reg_no.strip(): reg_no = "Not provided"
        address = selected.get('address', 'N/A')
        contact_name = selected.get('contact_name', 'N/A')
        email = selected.get('email', 'N/A')
        phone = selected.get('phone', 'N/A')
        info = selected.get('info', '')
        if not info.strip(): info = "None provided."
        s_type = selected.get('type', 'N/A')
        date = selected.get('date', 'N/A')
        order_id = selected.get('id', 'N/A')

        # We bouwen het nu netjes op met standaard Streamlit containers en kolommen
        with st.container(border=True):
            st.subheader(f"Order #{order_id}")
            st.caption(f"Received on {date}")
            st.write("") # Beetje ruimte
            
            # --- COMPANY INFO ---
            st.markdown("<h4 style='color: #894b9d; border-bottom: 2px solid #f0f3f6; padding-bottom: 5px;'>🏢 Company Information</h4>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"<p class='detail-label'>Company Name</p><p class='detail-value'>{company}</p>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"<p class='detail-label'>Registration No.</p><p class='detail-value'>{reg_no}</p>", unsafe_allow_html=True)
            
            st.markdown(f"<p class='detail-label'>Registered Address</p><p class='detail-value'>{address}</p>", unsafe_allow_html=True)
            
            # --- CONTACT PERSON ---
            st.write("")
            st.markdown("<h4 style='color: #894b9d; border-bottom: 2px solid #f0f3f6; padding-bottom: 5px;'>👤 Contact Person</h4>", unsafe_allow_html=True)
            c3, c4 = st.columns(2)
            with c3:
                st.markdown(f"<p class='detail-label'>Name</p><p class='detail-value'>{contact_name}</p>", unsafe_allow_html=True)
            with c4:
                st.markdown(f"<p class='detail-label'>Phone</p><p class='detail-value'>{phone}</p>", unsafe_allow_html=True)
            
            st.markdown(f"<p class='detail-label'>Email Address</p><p class='detail-value'><a href='mailto:{email}' style='color: #894b9d;'>{email}</a></p>", unsafe_allow_html=True)
            
            # --- SHIPMENT DETAILS ---
            st.write("")
            st.markdown("<h4 style='color: #894b9d; border-bottom: 2px solid #f0f3f6; padding-bottom: 5px;'>📦 Shipment Details</h4>", unsafe_allow_html=True)
            st.markdown(f"<p class='detail-label'>Requested Services</p><p class='detail-value' style='font-weight: 700;'>{s_type}</p>", unsafe_allow_html=True)
            
            st.markdown("<p class='detail-label'>Additional Instructions / Details</p>", unsafe_allow_html=True)
            # Dit zet de tekst in een mooi lichtblauw/grijs informatie blokje, altijd leesbaar!
            st.info(info)
            
            st.write("---")
            
            # Knoppen onderaan
            c_btn1, c_btn2, _ = st.columns([2, 2, 3])
            with c_btn1:
                if st.button("✅ Mark as Processed", use_container_width=True):
                    st.session_state.orders = [o for o in st.session_state.orders if o['id'] != order_id]
                    st.session_state.selected_order = None
                    st.success("Order has been successfully processed!")
                    time.sleep(1.5)
                    st.rerun()
            with c_btn2:
                if st.button("🗑️ Delete", type="secondary", use_container_width=True):
                    st.session_state.orders = [o for o in st.session_state.orders if o['id'] != order_id]
                    st.session_state.selected_order = None
                    st.rerun()
