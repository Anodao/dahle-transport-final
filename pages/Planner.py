import streamlit as st
import time
from datetime import datetime
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
    st.error("⚠️ Database connection failed. Please check your secrets.toml file.")
    st.stop()

# --- INITIALIZE STATE ---
if 'selected_order' not in st.session_state:
    st.session_state.selected_order = None
if 'view_status' not in st.session_state:
    st.session_state.view_status = 'New'

# --- HAAL DATA OP BASIS VAN STATUS ---
try:
    resp = supabase.table("orders").select("*").eq("status", st.session_state.view_status).order("id", desc=True).execute()
    orders = resp.data
except Exception as e:
    st.error(f"Error fetching data: {e}")
    orders = []

# Update geselecteerde order indien nodig
if st.session_state.selected_order:
    curr_id = st.session_state.selected_order['id']
    st.session_state.selected_order = next((o for o in orders if o['id'] == curr_id), st.session_state.selected_order)

# --- POP-UP WAARSCHUWING VOOR VERWIJDEREN ---
@st.dialog("Confirm Deletion")
def confirm_delete_dialog(order_id):
    st.write(f"Are you sure you want to permanently delete **Order #{order_id}**?")
    st.caption("This action cannot be undone.")
    
    st.write("") 
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Cancel", type="secondary", use_container_width=True):
            st.rerun()
    with c2:
        if st.button("Yes, Delete", use_container_width=True):
            supabase.table("orders").delete().eq("id", order_id).execute()
            st.session_state.selected_order = None
            st.rerun()

# --- CSS STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }
    
    [data-testid="collapsedControl"], [data-testid="stSidebar"], header[data-testid="stHeader"] { display: none !important; }
    
    .stApp { background-color: #f8f9fa !important; }
    .block-container { padding-top: 2rem; }

    .header-banner {
        background-color: #894b9d;
        padding: 30px 40px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .header-banner h1 { color: #ffffff !important; margin: 0; font-weight: 700; }
    .header-banner p { color: #e0d0e6 !important; margin: 5px 0 0 0; font-size: 14px;}

    .inbox-card {
        background-color: #ffffff !important;
        border: 1px solid #e0e6ed !important;
        border-radius: 8px !important;
        padding: 20px !important;
        margin-bottom: 5px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
    }
    .selected-card {
        border: 2px solid #894b9d !important;
        background-color: #faf5fc !important; 
        transform: translateX(8px); 
    }

    .inbox-title { color: #333333 !important; font-weight: 700; font-size: 16px; margin: 0 0 8px 0; }
    .inbox-subtitle { color: #666666 !important; font-size: 13px; margin: 0 0 8px 0; }
    .inbox-date { color: #888888 !important; font-size: 11px; margin: 0; }
    .status-new { color: #e74c3c !important; font-weight: 900; }
    .status-done { color: #27ae60 !important; font-weight: 900; }
    
    .detail-label { color: #888888 !important; font-size: 12px; font-weight: 700; text-transform: uppercase; margin-bottom: 0px !important; }
    .detail-value { color: #333333 !important; font-size: 16px; font-weight: 500; margin-top: 2px !important; margin-bottom: 15px !important;}
    
    div.stButton > button { background-color: #894b9d !important; color: white !important; border: none; font-weight: bold; border-radius: 6px;}
    div.stButton > button:hover { background-color: #723e83 !important; }
    div.stButton > button[kind="secondary"] { background-color: #e0e6ed !important; color: #333 !important;}
    </style>
""", unsafe_allow_html=True)

# --- HEADER BANNER ---
st.markdown("""
<div class="header-banner">
    <h1>Planner Dashboard</h1>
    <p>Internal Use Only</p>
</div>
""", unsafe_allow_html=True)

# --- NAVIGATIE KNOPPEN ---
c_nav1, c_nav2 = st.columns([1, 1])
with c_nav1:
    if st.button("Go Back to Website", type="secondary", use_container_width=True):
        st.switch_page("Home.py")
with c_nav2:
    if st.button("Open Dashboard", use_container_width=True):
        st.switch_page("pages/Dashboard.py")

st.write("")

# --- LAYOUT VERDELING ---
col_inbox, col_details = st.columns([1, 2], gap="large")

# =========================================================
# LINKER KOLOM: INBOX
# =========================================================
with col_inbox:
    st.markdown("<h3 style='color:#333333; margin-bottom: 15px;'>Inbox</h3>", unsafe_allow_html=True)

    # 1. Knoppen voor status (Not Ready / Ready)
    c_btn_new, c_btn_proc = st.columns(2)
    with c_btn_new:
        if st.button("Not Ready", use_container_width=True, 
                     type="primary" if st.session_state.view_status == 'New' else "secondary"):
            st.session_state.view_status = 'New'
            st.session_state.selected_order = None
            st.rerun()
    with c_btn_proc:
        if st.button("Ready", use_container_width=True, 
                     type="primary" if st.session_state.view_status == 'Processed' else "secondary"):
            st.session_state.view_status = 'Processed'
            st.session_state.selected_order = None
            st.rerun()
            
    # 2. De datumbalk
    date_range = st.date_input("Filter by Date Range", value=[], label_visibility="collapsed")
    st.write("---")

    # 3. De Lijst
    if not orders:
        st.info(f"No {st.session_state.view_status.lower()} orders found.")
    else:
        for o in orders: 
            # Datum filter toepassen
            show_order = True
            if len(date_range) == 2:
                o_date = datetime.strptime(o['received_date'][:10], "%Y-%m-%d").date()
                if not (date_range[0] <= o_date <= date_range[1]):
                    show_order = False
            
            if show_order:
                is_selected = "selected-card" if st.session_state.selected_order and o['id'] == st.session_state.selected_order['id'] else ""
                status_label = "New" if o['status'] == 'New' else "Done"
                status_class = "status-new" if o['status'] == 'New' else "status-done"
                
                st.markdown(f"""
                <div class="inbox-card {is_selected}">
                    <p class="inbox-title"><span class="{status_class}">{status_label}</span> &nbsp; {o.get('company', 'Unknown')}</p>
                    <p class="inbox-subtitle">{o.get('types', '')}</p>
                    <p class="inbox-date">Received: {o.get('received_date', '')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Open Order #{o['id']}", key=f"btn_{o['id']}", use_container_width=True):
                    st.session_state.selected_order = o
                    st.rerun()
                st.write("")

# =========================================================
# RECHTER KOLOM: ORDER DETAILS 
# =========================================================
with col_details:
    st.markdown("<h3 style='color:#333333; margin-bottom: 15px;'>Order Details</h3>", unsafe_allow_html=True)
    
    selected = st.session_state.selected_order
    if not selected:
        st.info("Select an order from the inbox to view details.")
    else:
        with st.container(border=True):
            st.markdown(f"## Order #{selected['id']}")
            st.markdown(f"<p style='color: #888; font-size: 13px;'>Received on {selected['received_date']}</p>", unsafe_allow_html=True)
            
            st.markdown("<h4 style='color: #894b9d; border-bottom: 2px solid #f0f3f6;'>Company Information</h4>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            c1.markdown(f"<p class='detail-label'>Company</p><p class='detail-value'>{selected['company']}</p>", unsafe_allow_html=True)
            c2.markdown(f"<p class='detail-label'>Reg No</p><p class='detail-value'>{selected.get('reg_no') or 'N/A'}</p>", unsafe_allow_html=True)
            
            st.markdown("<h4 style='color: #894b9d; border-bottom: 2px solid #f0f3f6;'>Contact Person</h4>", unsafe_allow_html=True)
            c3, c4 = st.columns(2)
            c3.markdown(f"<p class='detail-label'>Name</p><p class='detail-value'>{selected['contact_name']}</p>", unsafe_allow_html=True)
            c4.markdown(f"<p class='detail-label'>Phone</p><p class='detail-value'>{selected['phone']}</p>", unsafe_allow_html=True)
            
            st.markdown("<h4 style='color: #894b9d; border-bottom: 2px solid #f0f3f6;'>Shipment</h4>", unsafe_allow_html=True)
            st.markdown(f"<p class='detail-label'>Services</p><p class='detail-value'>{selected['types']}</p>", unsafe_allow_html=True)
            st.info(selected.get('info') or "No additional instructions.")
            
            st.write("---")
            c_btn1, c_btn2, _ = st.columns([2, 2, 3])
            
            if selected['status'] == 'New':
                with c_btn1:
                    if st.button("Mark as Processed", use_container_width=True):
                        now = datetime.now().strftime("%Y-%m-%d %H:%M")
                        supabase.table("orders").update({"status": "Processed", "processed_at": now}).eq("id", selected['id']).execute()
                        st.session_state.selected_order = None 
                        st.success("Order processed!")
                        time.sleep(1)
                        st.rerun()
                with c_btn2:
                    if st.button("Delete Request", type="secondary", use_container_width=True):
                        confirm_delete_dialog(selected['id'])
            else:
                with c_btn1:
                    if st.button("Delete from History", type="secondary", use_container_width=True):
                        confirm_delete_dialog(selected['id'])
