import streamlit as st
import time
from datetime import datetime
from supabase import create_client

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Dahle Transport - Planner",
    page_icon="📋",
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
    st.error("⚠️ Database connection failed.")
    st.stop()

# --- PERSISTENT SESSION CHECK ---
if 'user' not in st.session_state:
    try:
        session = supabase.auth.get_session()
        if session:
            st.session_state.user = session.user
        else:
            st.session_state.user = None
    except:
        st.session_state.user = None

if 'selected_order_id' not in st.session_state:
    st.session_state.selected_order_id = None

# --- CSS STYLING & NAVBAR (CRISP LIGHT MODE) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }
    
    [data-testid="collapsedControl"], [data-testid="stSidebar"], header[data-testid="stHeader"] { display: none !important; }
    
    /* --- LIGHT THEME ACHTERGROND --- */
    .stApp { background-color: #f4f6f8 !important; }
    
    /* Forceer alle algemene tekst naar donkergrijs/zwart */
    .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown li, .stMarkdown span { color: #111111 !important; }
    div[data-testid="caption"] { color: #666666 !important; }

    /* NAVBAR */
    .block-container { padding-top: 130px !important; }
    .navbar {
        position: fixed; top: 0; left: 0; width: 100%; height: 90px;
        background-color: #ffffff !important; z-index: 999; border-bottom: 1px solid #eaeaea; 
        display: grid; grid-template-columns: 1fr auto 1fr; align-items: center;
        padding: 0 40px; box-shadow: 0 2px 10px rgba(0,0,0,0.03);
    }
    .nav-logo img { height: 48px; width: auto; }
    .nav-links { display: flex; gap: 28px; font-size: 15px; font-weight: 500; justify-content: center; }
    .nav-links a, .nav-links span { text-decoration: none; color: #111111 !important; cursor: pointer; transition: color 0.2s;}
    .nav-links span:hover { color: #894b9d !important; }
    .nav-cta { display: flex; justify-content: flex-end; }
    .cta-btn-outline { background-color: transparent !important; color: #894b9d !important; padding: 10px 20px; border-radius: 50px; text-decoration: none !important; font-weight: 600; font-size: 13px; border: 2px solid #894b9d; white-space: nowrap;}

    /* CONTAINERS (Witte kaarten met lichte schaduw) */
    div[data-testid="stVerticalBlockBorderWrapper"] { 
        background-color: #ffffff !important; 
        border: 1px solid #d1d5db !important; 
        border-radius: 8px !important; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.03) !important;
    }
    
    /* FIX VOOR KPI METRICS TEKST (Geforceerd Zwart) */
    div[data-testid="stMetricValue"] > div { color: #894b9d !important; font-weight: 700 !important; font-size: 32px !important;}
    div[data-testid="stMetricLabel"] * { color: #111111 !important; font-weight: 600 !important; font-size: 14px !important; visibility: visible !important;}
    
    /* FIX VOOR DROPDOWNS EN INPUTS (Geforceerd Zwart) */
    div[data-baseweb="select"] { background-color: #ffffff !important; }
    div[data-baseweb="select"] * { color: #111111 !important; }
    
    /* BUTTONS */
    div.stButton > button[kind="primary"] { 
        background: linear-gradient(135deg, #b070c6 0%, #894b9d 100%) !important; color: #ffffff !important; border: none !important; border-radius: 6px !important; padding: 10px 24px !important; font-weight: 600 !important; width: 100% !important; transition: all 0.3s ease !important;
    }
    div.stButton > button[kind="primary"] * { color: #ffffff !important; }
    div.stButton > button[kind="primary"]:hover { transform: translateY(-2px) !important; box-shadow: 0 6px 16px rgba(137, 75, 157, 0.3) !important; }
    
    div.stButton > button[kind="secondary"] { 
        background: #ffffff !important; color: #333333 !important; border: 1px solid #d1d5db !important; border-radius: 6px !important; padding: 10px 24px !important; font-weight: 600 !important; width: 100% !important; transition: all 0.2s ease !important;
    }
    div.stButton > button[kind="secondary"] * { color: #333333 !important; }
    div.stButton > button[kind="secondary"]:hover { border-color: #894b9d !important; color: #894b9d !important;}

    /* TABS FIX */
    button[data-baseweb="tab"] p { color: #666666 !important; font-weight: 600; font-size: 15px;}
    button[data-baseweb="tab"][aria-selected="true"] p { color: #b070c6 !important; }
    button[data-baseweb="tab"] { background-color: transparent !important; }
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
            <a href="/" target="_self" class="cta-btn-outline">← BACK TO HOME</a>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- DATA OPHALEN ---
def fetch_all_orders():
    try:
        res = supabase.table("orders").select("*").order("id", desc=True).execute()
        return res.data
    except: return []

all_orders = fetch_all_orders()

# =========================================================
# KPI DASHBOARD
# =========================================================
count_pending = sum(1 for o in all_orders if o['status'] == 'New')
count_progress = sum(1 for o in all_orders if o['status'] == 'In Progress')
count_done = sum(1 for o in all_orders if o['status'] in ['Processed', 'Delivered'])
total_orders = len(all_orders)

m1, m2, m3, m4 = st.columns(4)
with m1:
    with st.container(border=True):
        st.metric("🔴 Action Required (New)", count_pending)
with m2:
    with st.container(border=True):
        st.metric("🟡 Active Routes", count_progress)
with m3:
    with st.container(border=True):
        st.metric("🟢 Completed", count_done)
with m4:
    with st.container(border=True):
        st.metric("📋 Total All-Time", total_orders)

st.write("---")

# =========================================================
# LAYOUT (2 KOLOMMEN)
# =========================================================
col_list, col_details = st.columns([1, 2], gap="large")

with col_list:
    st.markdown("<h2 style='color: #b070c6;'>Inbox</h2>", unsafe_allow_html=True)
    
    tab_new, tab_prog, tab_done = st.tabs(["🔴 Pending", "🟡 In Progress", "🟢 Done"])
    
    # --- 1. PENDING (Status: New) ---
    with tab_new:
        pending = [o for o in all_orders if o['status'] == 'New']
        if not pending: st.info("No pending orders.")
        for o in pending:
            with st.container(border=True):
                st.markdown(f"**{o['company']}**")
                st.caption(f"Order #{o['id']} | Received: {o.get('received_date', '')[:10]}")
                if st.button(f"View #{o['id']}", key=f"p_{o['id']}", use_container_width=True):
                    st.session_state.selected_order_id = o['id']
                    st.rerun()

    # --- 2. IN PROGRESS (Status: In Progress) ---
    with tab_prog:
        inprogress = [o for o in all_orders if o['status'] == 'In Progress']
        if not inprogress: st.info("Nothing in progress.")
        for o in inprogress:
            with st.container(border=True):
                st.markdown(f"**🟡 {o['company']}**")
                st.caption(f"Order #{o['id']} | Received: {o.get('received_date', '')[:10]}")
                if st.button(f"View #{o['id']}", key=f"prog_{o['id']}", use_container_width=True):
                    st.session_state.selected_order_id = o['id']
                    st.rerun()

    # --- 3. DONE (Status: Processed / Delivered) ---
    with tab_done:
        done = [o for o in all_orders if o['status'] in ['Processed', 'Delivered']]
        if not done: st.info("No completed orders.")
        for o in done:
            with st.container(border=True):
                st.markdown(f"**🟢 {o['company']}**")
                proc_date = o.get('processed_date')
                display_date = proc_date[:10] if proc_date else o.get('received_date', '')[:10]
                st.caption(f"Order #{o['id']} | Afgerond | Datum: {display_date}")
                if st.button(f"View #{o['id']}", key=f"d_{o['id']}", use_container_width=True):
                    st.session_state.selected_order_id = o['id']
                    st.rerun()

with col_details:
    st.markdown("<h2>Order Details</h2>", unsafe_allow_html=True)
    st.write("---")
    
    if st.session_state.selected_order_id:
        order = next((o for o in all_orders if o['id'] == st.session_state.selected_order_id), None)
        if order:
            st.markdown(f"### Order #{order['id']} - {order['company']}")
            
            with st.container(border=True):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**📤 Pickup**")
                    st.write(f"{order['pickup_address']}\n{order['pickup_zip']} {order['pickup_city']}")
                with c2:
                    st.markdown("**📥 Delivery**")
                    st.write(f"{order['delivery_address']}\n{order['delivery_zip']} {order['delivery_city']}")
            
            st.write("")
            
            # --- STATUS UPDATE ---
            st.markdown("#### Update Status")
            status_list = ["New", "In Progress", "Processed", "Delivered"]
            try:
                current_idx = status_list.index(order['status'])
            except:
                current_idx = 0
                
            new_status = st.selectbox("Status", options=status_list, index=current_idx)
            
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.button("💾 Save Status", type="primary", use_container_width=True):
                    update_data = {
                        "status": new_status,
                        "processed_date": datetime.now().strftime("%Y-%m-%d %H:%M")
                    }
                    supabase.table("orders").update(update_data).eq("id", order['id']).execute()
                    st.success(f"Status updated to {new_status}")
                    time.sleep(1)
                    st.rerun()
            with col_b2:
                if st.button("🗑️ Delete", use_container_width=True):
                    supabase.table("orders").delete().eq("id", order['id']).execute()
                    st.session_state.selected_order_id = None
                    st.rerun()
    else:
        st.info("Select an order to view details.")
