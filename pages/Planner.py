import streamlit as st
import time
from datetime import datetime, timedelta
from supabase import create_client

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
    st.error("Database connection failed.")
    st.stop()

# --- INITIALIZE STATE ---
if 'selected_order' not in st.session_state:
    st.session_state.selected_order = None
if 'view_status' not in st.session_state:
    st.session_state.view_status = 'New'

# --- POP-UP VOOR VERWIJDEREN ---
@st.dialog("Confirm Deletion")
def confirm_delete_dialog(order_id):
    st.write(f"Are you sure you want to permanently delete **Order #{order_id}**?")
    st.write("")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Cancel", use_container_width=True):
            st.rerun()
    with c2:
        if st.button("Delete", type="primary", use_container_width=True):
            supabase.table("orders").delete().eq("id", order_id).execute()
            st.session_state.selected_order = None
            st.rerun()

# --- CSS STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }
    
    [data-testid="collapsedControl"], [data-testid="stSidebar"], header[data-testid="stHeader"] { display: none !important; }
    
    .stApp { background-color: #ffffff !important; }
    .block-container { padding-top: 2rem; }

    /* Header Banner */
    .header-banner {
        background-color: #894b9d;
        padding: 25px 35px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .header-banner h1 { color: #ffffff !important; margin: 0; font-size: 28px; }
    .header-banner p { color: #f0f0f0 !important; margin: 0; font-size: 14px; opacity: 0.8; }

    /* Inbox Kaarten */
    .order-card {
        background-color: #fcfcfc;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 10px;
    }
    .selected-card {
        border: 2px solid #894b9d !important;
        background-color: #faf5fc !important;
    }

    /* Knoppen Styling */
    div.stButton > button { border-radius: 6px; font-weight: 600; }
    
    /* Toggle buttons bovenaan inbox */
    .st-emotion-cache-12w0qpk { gap: 0.5rem; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
<div class="header-banner">
    <h1>Planner Dashboard</h1>
    <p>Internal Use Only</p>
</div>
""", unsafe_allow_html=True)

# --- DATA OPHALEN ---
try:
    # Haal orders op basis van de gekozen status
    resp = supabase.table("orders").select("*").eq("status", st.session_state.view_status).order("id", desc=True).execute()
    orders = resp.data
except:
    orders = []

# --- LAYOUT ---
col_inbox, col_details = st.columns([1, 2], gap="large")

# =========================================================
# INBOX KOLOM
# =========================================================
with col_inbox:
    st.subheader("Inbox")
    
    # 1. STATUS SELECTIE (Twee knoppen naast elkaar)
    c_btn_new, c_btn_proc = st.columns(2)
    with c_btn_new:
        if st.button("Not Ready", use_container_width=True, 
                     type="primary" if st.session_state.view_status == 'New' else "secondary"):
            st.session_state.view_status = 'New'
            st.rerun()
    with c_btn_proc:
        if st.button("Ready", use_container_width=True, 
                     type="primary" if st.session_state.view_status == 'Processed' else "secondary"):
            st.session_state.view_status = 'Processed'
            st.rerun()
            
    # 2. DATUM FILTER BALK
    date_range = st.date_input("Filter by Date Range", value=[], label_visibility="collapsed")
    
    st.write("---")

    # 3. ORDER LIJST
    if not orders:
        st.info("No orders found for this selection.")
    else:
        for o in orders:
            # Filter op datum indien geselecteerd
            show_order = True
            if len(date_range) == 2:
                o_date = datetime.strptime(o['received_date'][:10], "%Y-%m-%d").date()
                if not (date_range[0] <= o_date <= date_range[1]):
                    show_order = False
            
            if show_order:
                is_selected = "selected-card" if st.session_state.selected_order and st.session_state.selected_order['id'] == o['id'] else ""
                
                with st.container(border=True):
                    st.markdown(f"**{o.get('company', 'Unknown')}**")
                    st.caption(f"Received: {o.get('received_date', '')}")
                    
                    if st.button(f"Open Order #{o['id']}", key=f"btn_{o['id']}", use_container_width=True):
                        st.session_state.selected_order = o
                        st.rerun()

# =========================================================
# DETAILS KOLOM
# =========================================================
with col_details:
    st.subheader("Order Details")
    
    selected = st.session_state.selected_order
    if not selected:
        st.info("Select an order from the inbox to view the details.")
    else:
        with st.container(border=True):
            st.markdown(f"## Order #{selected['id']}")
            st.write(f"**Status:** {'Not Ready' if selected['status'] == 'New' else 'Ready'}")
            st.write("---")
            
            # Klant details
            st.markdown("#### Company Information")
            c1, c2 = st.columns(2)
            c1.markdown(f"**Name:**\n{selected['company']}")
            c2.markdown(f"**Address:**\n{selected['address']}")
            
            st.write("")
            st.markdown("#### Contact Person")
            c3, c4 = st.columns(2)
            c3.markdown(f"**Name:**\n{selected['contact_name']}")
            c4.markdown(f"**Phone:**\n{selected['phone']}")
            st.markdown(f"**Email:** {selected['email']}")
            
            st.write("")
            st.markdown("#### Shipment")
            st.markdown(f"**Type:** {selected['types']}")
            st.info(selected['info'] if selected['info'] else "No additional instructions.")
            
            st.write("---")
            
            # Actie knoppen
            ca, cb = st.columns(2)
            if selected['status'] == 'New':
                if ca.button("Mark as Ready", use_container_width=True):
                    now = datetime.now().strftime("%Y-%m-%d %H:%M")
                    supabase.table("orders").update({"status": "Processed", "processed_at": now}).eq("id", selected['id']).execute()
                    st.session_state.selected_order = None
                    st.rerun()
            
            if cb.button("Delete Request", type="secondary", use_container_width=True):
                confirm_delete_dialog(selected['id'])

# --- NAVIGATIE ONDERAAN ---
st.write("")
st.write("---")
_, c_nav1, c_nav2 = st.columns([2, 1, 1])
with c_nav1:
    if st.button("Go Back to Website", use_container_width=True):
        st.switch_page("Home.py")
with c_nav2:
    if st.button("Open Dashboard", use_container_width=True):
        st.switch_page("pages/Dashboard.py")
