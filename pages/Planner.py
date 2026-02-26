import streamlit as st
import time
from datetime import datetime
from supabase import create_client, Client

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Dahle Transport - Planner",
    page_icon="⚙️",
    layout="wide",
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
    st.error("⚠️ Database connection failed. Please check your secrets.toml file.")
    st.stop()

# --- HAAL DATA LIVE OP UIT DATABASE ---
try:
    active_resp = supabase.table("orders").select("*").eq("status", "New").order("id", desc=True).execute()
    active_orders = active_resp.data
    
    processed_resp = supabase.table("orders").select("*").eq("status", "Processed").order("processed_at", desc=True).execute()
    processed_orders = processed_resp.data
except Exception as e:
    st.error(f"Error fetching data: {e}")
    active_orders = []
    processed_orders = []

# --- INITIALIZE STATE VOOR GESELECTEERDE ORDER ---
if 'selected_order' not in st.session_state:
    st.session_state.selected_order = None

# Zorg dat de openstaande order geüpdatet blijft als de database verandert
if st.session_state.selected_order:
    curr_id = st.session_state.selected_order['id']
    # Zoek hem op in de net opgehaalde data
    found = next((o for o in active_orders + processed_orders if o['id'] == curr_id), None)
    st.session_state.selected_order = found

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

    /* --- INBOX KAARTEN STYLING --- */
    .inbox-card {
        background-color: #ffffff !important;
        border: 1px solid #e0e6ed !important;
        border-radius: 8px !important;
        padding: 20px !important;
        margin-bottom: 5px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
        transition: all 0.2s ease-in-out;
    }
    .processed-card {
        background-color: #f8f9fa !important;
        border: 1px dashed #bdc3c7 !important;
        border-radius: 8px !important;
        padding: 20px !important;
        margin-bottom: 5px !important;
        transition: all 0.2s ease-in-out;
    }

    /* --- HIGHLIGHT EFFECT VOOR GESELECTEERDE ORDER --- */
    .selected-card {
        border: 2px solid #894b9d !important;
        background-color: #faf5fc !important; 
        box-shadow: 0 6px 12px rgba(137, 75, 157, 0.15) !important;
        transform: translateX(8px); 
    }

    .inbox-title { color: #333333 !important; font-weight: 700; font-size: 16px; margin: 0 0 8px 0; }
    .inbox-subtitle { color: #666666 !important; font-size: 13px; margin: 0 0 8px 0; line-height: 1.4;}
    .inbox-date { color: #888888 !important; font-size: 11px; margin: 0; }
    .status-new { color: #e74c3c !important; font-weight: 900; }
    .status-done { color: #27ae60 !important; font-weight: 900; }
    
    /* Custom styling voor de details in de box rechts */
    .detail-label { color: #888888 !important; font-size: 12px; font-weight: 700; text-transform: uppercase; margin-bottom: 0px !important; letter-spacing: 0.5px;}
    .detail-value { color: #333333 !important; font-size: 16px; font-weight: 500; margin-top: 2px !important; margin-bottom: 15px !important;}
    
    /* Container voor de 'Go Back' knop */
    .home-btn-container { margin-bottom: 30px; }
    .card-spacer { margin-bottom: 20px; }
    
    /* Streamlit Knoppen fix voor planner (Dahle Paars) */
    div.stButton > button { background-color: #894b9d !important; color: white !important; border: none; font-weight: bold; border-radius: 6px;}
    div.stButton > button:hover { background-color: #723e83 !important; }
    
    /* Secundaire knop (voor "Delete" of "Go Back") */
    div.stButton > button[kind="secondary"] { background-color: #e0e6ed !important; color: #333 !important;}
    div.stButton > button[kind="secondary"]:hover { background-color: #bdc3c7 !important; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER BANNER ---
st.markdown("""
<div class="header-banner">
    <h1>🔒 Planner Dashboard</h1>
    <p>Internal Use Only</p>
</div>
""", unsafe_allow_html=True)

# --- NAVIGATIE KNOPPEN ---
st.markdown('<div class="home-btn-container">', unsafe_allow_html=True)
c_nav1, c_nav2 = st.columns([1, 1])

with c_nav1:
    if st.button("🏠 ← Go Back to Website", type="secondary", use_container_width=True):
        st.switch_page("Home.py")

with c_nav2:
    if st.button("🌍 Open CO₂ Dashboard →", use_container_width=True):
        st.switch_page("pages/Dashboard.py")
        
st.markdown('</div>', unsafe_allow_html=True)

# --- LAYOUT VERDELING ---
col_inbox, col_details = st.columns([1, 2], gap="large")

selected_id = st.session_state.selected_order.get('id') if st.session_state.selected_order else None

# =========================================================
# LINKER KOLOM: INBOX & GESCHIEDENIS
# =========================================================
with col_inbox:
    # --- 1. ACTIEVE ORDERS ---
    st.markdown("<h3 style='color:#333333; margin-bottom: 15px;'>📥 Inbox</h3>", unsafe_allow_html=True)
    
    if not active_orders:
        st.info("No new requests at the moment. Waiting for customers...")
    else:
        for o in active_orders: 
            is_active = "selected-card" if o.get('id') == selected_id else ""
            
            st.markdown(f"""
<div class="inbox-card {is_active}">
    <p class="inbox-title"><span class="status-new">🔴 New</span> &nbsp; {o.get('company', 'Unknown')}</p>
    <p class="inbox-subtitle">{o.get('types', '')}</p>
    <p class="inbox-date">Received: {o.get('received_date', '')}</p>
</div>
""", unsafe_allow_html=True)
            
            btn_txt = f"👁️ Viewing Order #{o.get('id')}" if o.get('id') == selected_id else f"Open Order #{o.get('id')}"
            
            if st.button(btn_txt, key=f"btn_{o.get('id')}", use_container_width=True):
                st.session_state.selected_order = o
                st.rerun()
            st.markdown('<div class="card-spacer"></div>', unsafe_allow_html=True)

    # --- 2. VERWERKTE ORDERS (GESCHIEDENIS) ---
    st.markdown("<br><h3 style='color:#333333; margin-bottom: 15px; border-top: 2px solid #e0e6ed; padding-top: 15px;'>✅ Processed History</h3>", unsafe_allow_html=True)
    
    if not processed_orders:
        st.write("<p style='color:#888888; font-size: 14px;'>No orders have been processed yet.</p>", unsafe_allow_html=True)
    else:
        for po in processed_orders:
            is_active = "selected-card" if po.get('id') == selected_id else ""
            
            st.markdown(f"""
<div class="processed-card {is_active}">
    <p class="inbox-title" style="color: #888 !important;"><span class="status-done">✅ Done</span> &nbsp; {po.get('company', 'Unknown')}</p>
    <p class="inbox-subtitle" style="color: #999 !important;">{po.get('types', '')}</p>
    <p class="inbox-date">Processed on: {po.get('processed_at', '')}</p>
</div>
""", unsafe_allow_html=True)
            
            btn_txt = f"👁️ Viewing Order #{po.get('id')}" if po.get('id') == selected_id else f"View Order #{po.get('id')}"
            
            if st.button(btn_txt, key=f"btn_hist_{po.get('id')}", type="secondary", use_container_width=True):
                st.session_state.selected_order = po
                st.rerun()
            st.markdown('<div class="card-spacer"></div>', unsafe_allow_html=True)

# =========================================================
# RECHTER KOLOM: ORDER DETAILS 
# =========================================================
with col_details:
    st.markdown("<h3 style='color:#333333; margin-bottom: 15px;'>📋 Order Details</h3>", unsafe_allow_html=True)
    
    selected = st.session_state.selected_order
    
    if not selected:
        st.info("Click on an order in the inbox or history to view the full details here.")
    else:
        company = selected.get('company', 'N/A')
        reg_no = selected.get('reg_no', '')
        if not reg_no or not reg_no.strip(): reg_no = "Not provided"
        address = selected.get('address', 'N/A')
        contact_name = selected.get('contact_name', 'N/A')
        email = selected.get('email', 'N/A')
        phone = selected.get('phone', 'N/A')
        info = selected.get('info', '')
        if not info or not info.strip(): info = "None provided."
        s_type = selected.get('types', 'N/A')
        date = selected.get('received_date', 'N/A')
        order_id = selected.get('id', 'N/A')
        status = selected.get('status', 'New')

        with st.container(border=True):
            if status == 'Processed':
                st.markdown(f"<span style='background-color: #27ae60; color: white; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: bold;'>✅ Processed on {selected.get('processed_at', '')}</span>", unsafe_allow_html=True)
            else:
                st.markdown("<span style='background-color: #e74c3c; color: white; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: bold;'>🔴 Action Required</span>", unsafe_allow_html=True)
                
            st.markdown(f"<h2 style='color: #2c3e50; margin-top: 15px; margin-bottom: 0px;'>Order #{order_id}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #888888; font-size: 13px; margin-bottom: 25px;'>Received on {date}</p>", unsafe_allow_html=True)
            
            st.markdown("<h4 style='color: #894b9d; border-bottom: 2px solid #f0f3f6; padding-bottom: 5px;'>🏢 Company Information</h4>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"<p class='detail-label'>Company Name</p><p class='detail-value'>{company}</p>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"<p class='detail-label'>Registration No.</p><p class='detail-value'>{reg_no}</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='detail-label'>Registered Address</p><p class='detail-value'>{address}</p>", unsafe_allow_html=True)
            
            st.write("")
            st.markdown("<h4 style='color: #894b9d; border-bottom: 2px solid #f0f3f6; padding-bottom: 5px;'>👤 Contact Person</h4>", unsafe_allow_html=True)
            c3, c4 = st.columns(2)
            with c3:
                st.markdown(f"<p class='detail-label'>Name</p><p class='detail-value'>{contact_name}</p>", unsafe_allow_html=True)
            with c4:
                st.markdown(f"<p class='detail-label'>Phone</p><p class='detail-value'>{phone}</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='detail-label'>Email Address</p><p class='detail-value'><a href='mailto:{email}' style='color: #894b9d;'>{email}</a></p>", unsafe_allow_html=True)
            
            st.write("")
            st.markdown("<h4 style='color: #894b9d; border-bottom: 2px solid #f0f3f6; padding-bottom: 5px;'>📦 Shipment Details</h4>", unsafe_allow_html=True)
            st.markdown(f"<p class='detail-label'>Requested Services</p><p class='detail-value' style='font-weight: 700;'>{s_type}</p>", unsafe_allow_html=True)
            st.markdown("<p class='detail-label'>Additional Instructions / Details</p>", unsafe_allow_html=True)
            st.info(info)
            
            st.write("---")
            
            c_btn1, c_btn2, _ = st.columns([2, 2, 3])
            
            if status != 'Processed':
                with c_btn1:
                    if st.button("✅ Mark as Processed", use_container_width=True):
                        # --- UPDATE IN DATABASE ---
                        now = datetime.now().strftime("%Y-%m-%d %H:%M")
                        supabase.table("orders").update({"status": "Processed", "processed_at": now}).eq("id", order_id).execute()
                        st.session_state.selected_order = None 
                        st.success("Order has been successfully processed!")
                        time.sleep(1.5)
                        st.rerun()
                with c_btn2:
                    if st.button("🗑️ Delete Request", type="secondary", use_container_width=True):
                        # --- VERWIJDER UIT DATABASE ---
                        supabase.table("orders").delete().eq("id", order_id).execute()
                        st.session_state.selected_order = None
                        st.rerun()
            else:
                with c_btn1:
                    if st.button("🗑️ Delete from History", type="secondary", use_container_width=True):
                        # --- VERWIJDER UIT DATABASE ---
                        supabase.table("orders").delete().eq("id", order_id).execute()
                        st.session_state.selected_order = None
                        st.rerun()
