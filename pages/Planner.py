import streamlit as st
import time
from datetime import datetime, timedelta
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

# --- CSS (ALLEEN LAYOUT, GEEN KLEUREN GEFORCEERD) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }

/* Verberg overbodige Streamlit zijbalk/header */
[data-testid="collapsedControl"], [data-testid="stSidebar"], header[data-testid="stHeader"] { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
footer { display: none !important; }
div[class^="viewerBadge"] { display: none !important; }

/* Custom Navbar bovenaan */
.block-container { padding-top: 120px !important; }
.navbar { 
    position: fixed; top: 0; left: 0; width: 100%; height: 90px; 
    background-color: #ffffff !important; border-bottom: 1px solid #eaeaea !important; 
    z-index: 999; display: flex; justify-content: space-between; align-items: center; padding: 0 40px; 
}
.nav-logo img { height: 48px; width: auto; }
.nav-links a { text-decoration: none; font-weight: bold; margin: 0 15px; color: #111111 !important; }
.cta-btn-outline { border: 2px solid #894b9d !important; color: #894b9d !important; border-radius: 50px; padding: 10px 20px; text-decoration: none; font-weight: bold; }
</style>

<div class="navbar">
    <div class="nav-logo"><a href="/" target="_self"><img src="https://cloud-1de12d.becdn.net/media/original/964295c9ae8e693f8bb4d6b70862c2be/logo-website-top-png-1-.webp"></a></div>
    <div class="nav-links">
        <a href="/" target="_self">Hjem</a>
        <a href="/" target="_self">Om oss</a>
        <a href="/" target="_self">Tjenester</a>
        <a href="/" target="_self">Galleri</a>
        <a href="/" target="_self">Kontakt</a>
    </div>
    <div><a href="/" target="_self" class="cta-btn-outline">← BACK TO HOME</a></div>
</div>
""", unsafe_allow_html=True)

# --- DATA OPHALEN ---
def fetch_all_orders():
    try:
        res = supabase.table("orders").select("*").order("id", desc=True).execute()
        return res.data
    except: 
        return []

all_orders = fetch_all_orders()

# =========================================================
# KPI DASHBOARD (Inklapbaar, met Datumfilter en 5 kolommen)
# =========================================================
with st.expander("📊 Bekijk Statistieken & KPI's", expanded=True):
    
    # --- Datum Filter UI (Nu met 'Show All' optie) ---
    col_filter, _ = st.columns([1, 2])
    with col_filter:
        filter_optie = st.selectbox("📅 Filter periode:", ["Laatste 30 dagen", "Alle orders", "Aangepaste datum..."])
        
        start_date = None
        end_date = None
        
        if filter_optie == "Laatste 30 dagen":
            start_date = datetime.now().date() - timedelta(days=30)
            end_date = datetime.now().date()
        elif filter_optie == "Aangepaste datum...":
            default_start = datetime.now().date() - timedelta(days=30)
            date_range = st.date_input("Kies datum:", value=(default_start, datetime.now().date()))
            if isinstance(date_range, tuple) and len(date_range) == 2:
                start_date, end_date = date_range

    # --- Data Filter Logica ---
    filtered_orders = all_orders
    
    # Als start_date en end_date zijn ingevuld (dus NIET bij 'Alle orders'), dan filteren we:
    if start_date and end_date:
        temp_orders = []
        for o in all_orders:
            raw_date = o.get('received_date')
            if raw_date:
                try:
                    # Zet de datum string om naar een echt datum object
                    order_date = datetime.strptime(raw_date[:10], "%Y-%m-%d").date()
                    if start_date <= order_date <= end_date:
                        temp_orders.append(o)
                except ValueError:
                    pass # Negeer orders met een foute datum
        filtered_orders = temp_orders

    # --- Berekeningen toepassen op de gefilterde data ---
    count_pending = sum(1 for o in filtered_orders if o['status'] == 'New')
    count_progress = sum(1 for o in filtered_orders if o['status'] == 'In Progress')
    count_done = sum(1 for o in filtered_orders if o['status'] in ['Processed', 'Delivered'])
    count_cancelled = sum(1 for o in filtered_orders if o['status'] == 'Cancelled')
    total_orders = len(filtered_orders)

    # --- Strakke 5-koloms weergave ---
    m1, m2, m3, m4, m5 = st.columns(5)
    
    with m1:
        with st.container(border=True):
            st.markdown("<div style='font-size: 14px; color: #ccc;'>🔴 Action Required</div>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='margin: 0; padding-top: 5px;'>{count_pending}</h2>", unsafe_allow_html=True)
    with m2:
        with st.container(border=True):
            st.markdown("<div style='font-size: 14px; color: #ccc;'>🟡 Active Routes</div>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='margin: 0; padding-top: 5px;'>{count_progress}</h2>", unsafe_allow_html=True)
    with m3:
        with st.container(border=True):
            st.markdown("<div style='font-size: 14px; color: #ccc;'>🟢 Completed</div>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='margin: 0; padding-top: 5px;'>{count_done}</h2>", unsafe_allow_html=True)
    with m4:
        with st.container(border=True):
            st.markdown("<div style='font-size: 14px; color: #ccc;'>⚫ Cancelled</div>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='margin: 0; padding-top: 5px;'>{count_cancelled}</h2>", unsafe_allow_html=True)
    with m5:
        with st.container(border=True):
            st.markdown("<div style='font-size: 14px; color: #ccc;'>📋 Total Orders</div>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='margin: 0; padding-top: 5px;'>{total_orders}</h2>", unsafe_allow_html=True)

st.write("---")

# =========================================================
# LAYOUT (2 KOLOMMEN)
# =========================================================
col_list, col_details = st.columns([1, 2], gap="large")

with col_list:
    st.markdown("<h2>Inbox</h2>", unsafe_allow_html=True)
    
    tab_new, tab_prog, tab_done, tab_fail = st.tabs(["🔴 Pending", "🟡 In Progress", "🟢 Done", "❌ Cancelled"])
    
    with tab_new:
        pending = [o for o in all_orders if o['status'] == 'New']
        if not pending: st.info("No pending orders.")
        for o in pending:
            with st.container(border=True):
                st.markdown(f"**🔴 {o['company']}**")
                st.caption(f"Order #{o['id']} | Received: {o.get('received_date', '')[:10]}")
                if st.button(f"View #{o['id']}", key=f"p_{o['id']}", use_container_width=True):
                    st.session_state.selected_order_id = o['id']
                    st.rerun()

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

    with tab_fail:
        failed = [o for o in all_orders if o['status'] == 'Cancelled']
        if not failed: st.info("No cancelled orders.")
        for o in failed:
            with st.container(border=True):
                st.markdown(f"**❌ {o['company']}**")
                proc_date = o.get('processed_date')
                display_date = proc_date[:10] if proc_date else o.get('received_date', '')[:10]
                st.caption(f"Order #{o['id']} | Niet gelukt | Datum: {display_date}")
                if st.button(f"View #{o['id']}", key=f"f_{o['id']}", use_container_width=True):
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
                r1, r2 = st.columns(2)
                with r1:
                    st.markdown("#### 📤 Pickup Details")
                    st.markdown(f"**Address:** {order.get('pickup_address', '-')}")
                    st.markdown(f"**Zip Code:** {order.get('pickup_zip', '-')}")
                    st.markdown(f"**City:** {order.get('pickup_city', '-')}")
                with r2:
                    st.markdown("#### 📥 Delivery Details")
                    st.markdown(f"**Address:** {order.get('delivery_address', '-')}")
                    st.markdown(f"**Zip Code:** {order.get('delivery_zip', '-')}")
                    st.markdown(f"**City:** {order.get('delivery_city', '-')}")
            
            with st.container(border=True):
                st.markdown("#### 📞 Contact Information")
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.markdown("**Contact Person**")
                    st.write(order.get('contact_name', '-'))
                with c2:
                    st.markdown("**Phone**")
                    st.write(order.get('phone', '-'))
                with c3:
                    st.markdown("**Email**")
                    st.write(order.get('email', '-'))

            with st.container(border=True):
                st.markdown("#### 📝 Specifications & Internal Notes")
                st.markdown(f"**Requested Services:** {order.get('types', '-')}")
                if order.get('info'):
                    st.info(order['info'])
                
                st.write("---")
                st.markdown("**Internal Dispatch Notes (Hidden from customer):**")
                current_notes = order.get('internal_notes', '')
                new_notes = st.text_area("Typ hier je eigen notities...", value=current_notes if current_notes else "", height=100, label_visibility="collapsed")
            
            st.write("")
            
            st.markdown("#### Control Panel")
            status_list = ["New", "In Progress", "Processed", "Delivered", "Cancelled"]
            try:
                current_idx = status_list.index(order['status'])
            except:
                current_idx = 0
                
            new_status = st.selectbox("Update Order Status", options=status_list, index=current_idx)
            
            if st.button("💾 Save Updates", type="primary", use_container_width=True):
                update_data = {
                    "status": new_status,
                    "processed_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "internal_notes": new_notes
                }
                supabase.table("orders").update(update_data).eq("id", order['id']).execute()
                st.success("✅ Updates saved successfully!")
                time.sleep(1)
                st.rerun()
    else:
        st.info("👈 Select an order from the Inbox to view details and update its status.")
