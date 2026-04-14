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

# --- THEMA WISSELAAR (Light/Dark Mode Knop) ---
if 'theme' not in st.session_state:
    st.session_state.theme = "dark" # Standaard begint hij in donker

# Functie om thema te wisselen
def toggle_theme():
    if st.session_state.theme == "dark":
        st.session_state.theme = "light"
    else:
        st.session_state.theme = "dark"

# --- CSS STYLING GEBASEERD OP THEMA ---
if st.session_state.theme == "light":
    theme_css = """
    <style>
    /* LICHTE MODUS: Witte achtergrond, donkere letters */
    .stApp { background-color: #f4f6f8 !important; }
    .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown li, .stMarkdown span { color: #111111 !important; }
    div[data-testid="stVerticalBlockBorderWrapper"] { background-color: #ffffff !important; border: 1px solid #d1d5db !important; }
    div[data-testid="stMetricValue"] > div { color: #894b9d !important; }
    div[data-testid="stMetricLabel"] > div > p { color: #333333 !important; }
    div[data-baseweb="select"] > div, div[data-baseweb="textarea"] > div { background-color: #ffffff !important; }
    div[data-baseweb="select"] span, div[data-baseweb="textarea"] textarea { color: #111111 !important; }
    button[data-baseweb="tab"] p { color: #666666 !important; }
    </style>
    """
else:
    theme_css = """
    <style>
    /* DONKERE MODUS: Zwarte achtergrond, lichte letters */
    .stApp { background-color: #111111 !important; }
    .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown li, .stMarkdown span { color: #ffffff !important; }
    div[data-testid="stVerticalBlockBorderWrapper"] { background-color: #1e1e1e !important; border: 1px solid #333333 !important; }
    div[data-testid="stMetricValue"] > div { color: #b070c6 !important; }
    div[data-testid="stMetricLabel"] > div > p { color: #cccccc !important; }
    div[data-baseweb="select"] > div, div[data-baseweb="textarea"] > div { background-color: #333333 !important; border-color: #444 !important;}
    div[data-baseweb="select"] span, div[data-baseweb="textarea"] textarea { color: #ffffff !important; }
    button[data-baseweb="tab"] p { color: #aaaaaa !important; }
    </style>
    """

# Algemene styling (Menubalk, Knopjes, Lettertype) die voor beide thema's geldt
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
html, body, [class*="css"] {{ font-family: 'Montserrat', sans-serif; }}
[data-testid="collapsedControl"], [data-testid="stSidebar"], header[data-testid="stHeader"] {{ display: none !important; }}

/* NAVBAR (Altijd Wit) */
.block-container {{ padding-top: 130px !important; }}
.navbar {{ position: fixed; top: 0; left: 0; width: 100%; height: 90px; background-color: #ffffff !important; z-index: 999; border-bottom: 1px solid #eaeaea; display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; padding: 0 40px; box-shadow: 0 2px 10px rgba(0,0,0,0.03); }}
.nav-logo img {{ height: 48px; width: auto; }}
.nav-links {{ display: flex; gap: 28px; font-size: 15px; font-weight: 500; justify-content: center; }}
.nav-links a, .nav-links span {{ text-decoration: none; color: #111111 !important; }}
.nav-cta {{ display: flex; justify-content: flex-end; }}
.cta-btn-outline {{ background-color: transparent !important; color: #894b9d !important; padding: 10px 20px; border-radius: 50px; text-decoration: none !important; font-weight: 600; font-size: 13px; border: 2px solid #894b9d; }}

/* ALGEMENE BUTTONS */
div.stButton > button[kind="primary"] {{ background: linear-gradient(135deg, #b070c6 0%, #894b9d 100%) !important; color: #ffffff !important; border: none !important; border-radius: 6px !important; padding: 10px 24px !important; font-weight: 600 !important; width: 100% !important; }}
div.stButton > button[kind="primary"] p {{ color: #ffffff !important; }}
</style>
{theme_css}
""", unsafe_allow_html=True)

# --- NAVBAR ---
st.markdown("""
<div class="navbar">
    <div class="nav-logo"><a href="/" target="_self"><img src="https://cloud-1de12d.becdn.net/media/original/964295c9ae8e693f8bb4d6b70862c2be/logo-website-top-png-1-.webp"></a></div>
    <div class="nav-links">
        <a href="/"><span>Hjem</span></a>
        <span>Om oss</span><span>Tjenester</span><span>Galleri</span><span>Kontakt</span>
    </div>
    <div class="nav-cta"><a href="/" target="_self" class="cta-btn-outline">← BACK TO HOME</a></div>
</div>
""", unsafe_allow_html=True)

# --- THEMA KNOP (Rechtsboven onder de navbar) ---
c_title, c_toggle = st.columns([5, 1])
with c_title:
    pass # Ruimte voor titel als we die willen
with c_toggle:
    btn_text = "🌙 Dark Mode" if st.session_state.theme == "light" else "☀️ Light Mode"
    if st.button(btn_text, use_container_width=True):
        toggle_theme()
        st.rerun()

st.write("---")

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
        st.metric("🔴 Action Required", count_pending)
with m2:
    with st.container(border=True):
        st.metric("🟡 Active Routes", count_progress)
with m3:
    with st.container(border=True):
        st.metric("🟢 Completed", count_done)
with m4:
    with st.container(border=True):
        st.metric("📋 Total Orders", total_orders)

st.write("---")

# =========================================================
# LAYOUT (2 KOLOMMEN)
# =========================================================
col_list, col_details = st.columns([1, 2], gap="large")

with col_list:
    st.markdown("<h2 style='color: #b070c6; margin-bottom: 5px;'>Inbox</h2>", unsafe_allow_html=True)
    
    tab_new, tab_prog, tab_done = st.tabs(["🔴 Pending", "🟡 In Progress", "🟢 Done"])
    
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

with col_details:
    st.markdown("<h2 style='margin-bottom: 5px;'>Order Details</h2>", unsafe_allow_html=True)
    st.write("---")
    
    if st.session_state.selected_order_id:
        order = next((o for o in all_orders if o['id'] == st.session_state.selected_order_id), None)
        if order:
            st.markdown(f"### Order #{order['id']} - {order['company']}")
            
            # --- ROUTE INFO (Opgeschoonde Layout) ---
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
            status_list = ["New", "In Progress", "Processed", "Delivered"]
            try:
                current_idx = status_list.index(order['status'])
            except:
                current_idx = 0
                
            new_status = st.selectbox("Update Order Status", options=status_list, index=current_idx)
            
            col_b1, col_b2 = st.columns(2)
            with col_b1:
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
            with col_b2:
                if st.button("🗑️ Delete Order", use_container_width=True):
                    supabase.table("orders").delete().eq("id", order['id']).execute()
                    st.session_state.selected_order_id = None
                    st.rerun()
    else:
        st.info("👈 Select an order from the Inbox to view details and update its status.")
