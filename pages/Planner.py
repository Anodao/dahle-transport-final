import streamlit as st
from supabase import create_client

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Dahle Transport - Planner",
    page_icon="🔒",
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
    st.error("⚠️ Database connection failed. Please check your connection.")

# --- CSS STYLING (SCHOON & STANDAARD) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    /* Verberg de standaard Streamlit header en zijbalk */
    header[data-testid="stHeader"] { display: none !important; }
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    
    /* Normale padding bovenaan, GEEN extra achtergrondkleuren */
    .block-container { padding-top: 2rem; max-width: 95%; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.title("🔒 Planner Dashboard")
st.caption("Internal Use Only")

# --- TOP NAVIGATION BUTTONS ---
c1, c2 = st.columns(2)
with c1:
    if st.button("🏠 ← Go Back to Website", use_container_width=True):
        st.switch_page("Home.py")
with c2:
    if st.button("🟢 Open CO₂ Dashboard →", use_container_width=True):
        st.switch_page("pages/Dashboard.py")

st.write("---")

# --- SESSION STATE VOOR GESELECTEERDE ORDER ---
if 'selected_order' not in st.session_state:
    st.session_state.selected_order = None

# --- DATA OPHALEN UIT SUPABASE ---
try:
    response = supabase.table("orders").select("*").order("id", desc=True).execute()
    orders = response.data
except Exception as e:
    st.error("Failed to fetch orders from the database.")
    orders = []

# --- LAYOUT: INBOX (LINKS) & DETAILS (RECHTS) ---
col_inbox, col_details = st.columns([1, 2], gap="large")

with col_inbox:
    st.subheader("📥 Inbox")
    if not orders:
        st.info("No orders found.")
    else:
        for o in orders:
            with st.container(border=True):
                # Bepaal het kleurtje voor de status
                status_icon = "🔴" if o['status'] == 'New' else "🟢"
                
                st.write(f"**{status_icon} {o['status']}** | {o.get('company', 'Unknown Company')}")
                st.write(f"*{o.get('types', 'No type specified')}*")
                st.write(f"Received: {o.get('received_date', 'Unknown date')}")
                
                # Knop om de order te openen
                if st.button(f"Open Order #{o['id']}", key=f"btn_open_{o['id']}", use_container_width=True):
                    st.session_state.selected_order = o
                    st.rerun()

with col_details:
    st.subheader("📋 Order Details")
    
    if st.session_state.selected_order is None:
        st.info("Click on an order in the inbox or history to view the full details here.")
    else:
        o = st.session_state.selected_order
        with st.container(border=True):
            st.write(f"### Order #{o['id']} - {o.get('company', '')}")
            st.write(f"**Status:** {o.get('status', '')}")
            st.write("---")
            
            # Klant & Contact info
            st.write("**👤 Contact Information**")
            st.write(f"**Name:** {o.get('contact_name', '')}")
            st.write(f"**Email:** {o.get('email', '')}")
            st.write(f"**Phone:** {o.get('phone', '')}")
            st.write(f"**Company Address:** {o.get('address', '')}")
            if o.get('reg_no'):
                st.write(f"**Reg No:** {o.get('reg_no', '')}")
                
            st.write("---")
            
            # Route Info (Nieuw toegevoegd!)
            col_p, col_d = st.columns(2)
            with col_p:
                st.write("**📤 Pickup Location**")
                st.write(f"{o.get('pickup_address', '')}")
                st.write(f"{o.get('pickup_zip', '')} {o.get('pickup_city', '')}")
            with col_d:
                st.write("**📥 Delivery Destination**")
                st.write(f"{o.get('delivery_address', '')}")
                st.write(f"{o.get('delivery_zip', '')} {o.get('delivery_city', '')}")
                
            st.write("---")
            
            # Specificaties & Info
            st.write("**📦 Order Specifications & Info**")
            # We gebruiken code-block/text voor nette formattering van de extra info
            st.text(o.get('info', 'No additional information provided.'))
            
            st.write("---")
            
            # Actie knop (Alleen als de order nog 'New' is)
            if o.get('status') == 'New':
                if st.button("✅ Process Order (Send to Opter TMS)", type="primary", use_container_width=True):
                    try:
                        # Update de status in Supabase
                        supabase.table("orders").update({"status": "Processed"}).eq("id", o['id']).execute()
                        
                        # Update de status in onze tijdelijke sessie zodat het scherm direct mee verandert
                        st.session_state.selected_order['status'] = 'Processed'
                        st.success("Order processed successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error("Failed to update the order status.")
