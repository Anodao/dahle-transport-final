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
    st.error("⚠️ Database verbinding mislukt.")
    st.stop()

# --- INITIALIZE STATE ---
if 'selected_order' not in st.session_state:
    st.session_state.selected_order = None
if 'view_status' not in st.session_state:
    st.session_state.view_status = 'New'

# --- DATA OPHALEN ---
try:
    resp = supabase.table("orders").select("*").order("id", desc=True).execute()
    all_orders = resp.data
except Exception as e:
    st.error(f"Fout bij ophalen data: {e}")
    all_orders = []

# --- POP-UP VERWIJDEREN ---
@st.dialog("Confirm Deletion")
def confirm_delete_dialog(order_id):
    st.write(f"Weet je zeker dat je **Order #{order_id}** wilt verwijderen?")
    st.write("") 
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Annuleren", type="secondary", use_container_width=True):
            st.rerun()
    with c2:
        if st.button("Verwijderen", use_container_width=True):
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

    /* Header Banner */
    .header-banner {
        background-color: #894b9d;
        padding: 30px 40px;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    .header-banner h1 { color: #ffffff !important; margin: 0; font-weight: 700; }
    .header-banner p { color: #e0d0e6 !important; margin: 5px 0 0 0; font-size: 14px;}

    /* INPUT VELDEN (Dropdown & Datumkiezer) */
    div[data-baseweb="select"] > div, div[data-baseweb="base-input"] {
        background-color: #ffffff !important;
        border: 1px solid #d1d5db !important;
        border-radius: 6px !important;
    }
    input { color: #111111 !important; }
    
    /* Zorg dat de label tekst boven de datumkiezer zwart is */
    label[data-testid="stWidgetLabel"] { color: #333333 !important; font-weight: 600; font-size: 13px; }

    /* Inbox Kaarten */
    .inbox-card {
        background-color: #ffffff !important;
        border: 1px solid #e0e6ed !important;
        border-radius: 8px !important;
        padding: 20px !important;
        margin-bottom: 0px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
    }
    .selected-card {
        border: 2px solid #894b9d !important;
        background-color: #faf5fc !important; 
    }

    .status-new { color: #e74c3c !important; font-weight: 900; }
    .status-done { color: #27ae60 !important; font-weight: 900; }
    
    div.stButton > button { background-color: #894b9d !important; color: white !important; border: none; font-weight: bold; border-radius: 6px;}
    div.stButton > button:hover { background-color: #723e83 !important; }
    div.stButton > button[kind="secondary"] { background-color: #e0e6ed !important; color: #333 !important;}
    </style>
""", unsafe_allow_html=True)

# --- HEADER BANNER ---
st.markdown("""<div class="header-banner"><h1>Planner Dashboard</h1><p>Internal Use Only</p></div>""", unsafe_allow_html=True)

# --- DATUM LOGICA ---
today = datetime.now().date()
start_of_week = today - timedelta(days=today.weekday())
start_of_last_week = start_of_week - timedelta(days=7)

# --- LAYOUT ---
col_inbox, col_details = st.columns([1, 2], gap="large")

# =========================================================
# LINKER KOLOM: INBOX
# =========================================================
with col_inbox:
    st.markdown("<h3 style='color:#333333; margin-bottom: 10px;'>Inbox</h3>", unsafe_allow_html=True)

    # 1. Status knoppen
    c_btn_new, c_btn_proc = st.columns(2)
    with c_btn_new:
        if st.button("Not Ready", use_container_width=True, type="primary" if st.session_state.view_status == 'New' else "secondary"):
            st.session_state.view_status = 'New'
            st.rerun()
    with c_btn_proc:
        if st.button("Ready", use_container_width=True, type="primary" if st.session_state.view_status == 'Processed' else "secondary"):
            st.session_state.view_status = 'Processed'
            st.rerun()
            
    # 2. Dropdown Filter
    filter_optie = st.selectbox("Filter", ["Alle orders", "Vandaag", "Deze week", "Vorige week", "Aangepaste datum..."], label_visibility="collapsed")
    
    # 3. Toon Datumkiezer ALLEEN bij "Aangepaste datum..."
    custom_dates = []
    if filter_optie == "Aangepaste datum...":
        # Hier is de label_visibility='collapsed' weggehaald zodat de tekst zichtbaar is!
        custom_dates = st.date_input("Kies een specifieke dag of een periode (klik begin- en einddatum):", value=[])
    else:
        st.write("") # Extra lege regel als de kalender er niet is voor een gelijke opmaak

    # Filteren van de data
    filtered_orders = [o for o in all_orders if o['status'] == st.session_state.view_status]
    final_list = []

    for o in filtered_orders:
        try:
            order_date = datetime.strptime(o['received_date'][:10], "%Y-%m-%d").date()
            if filter_optie == "Alle orders":
                final_list.append(o)
            elif filter_optie == "Vandaag" and order_date == today:
                final_list.append(o)
            elif filter_optie == "Deze week" and order_date >= start_of_week:
                final_list.append(o)
            elif filter_optie == "Vorige week" and start_of_last_week <= order_date < start_of_week:
                final_list.append(o)
            elif filter_optie == "Aangepaste datum..." and len(custom_dates) > 0:
                if len(custom_dates) == 2: # Periode geselecteerd
                    if custom_dates[0] <= order_date <= custom_dates[1]: final_list.append(o)
                else: # Eén specifieke dag geselecteerd
                    if order_date == custom_dates[0]: final_list.append(o)
        except:
            if filter_optie == "Alle orders": final_list.append(o)

    # 4. Weergave lijst
    if not final_list:
        st.info("Geen orders gevonden in deze periode.")
    else:
        for o in final_list:
            is_active = "selected-card" if st.session_state.selected_order and o['id'] == st.session_state.selected_order['id'] else ""
            status_label = "New" if o['status'] == 'New' else "Done"
            status_class = "status-new" if o['status'] == 'New' else "status-done"
            
            st.markdown(f"""
            <div class="inbox-card {is_active}">
                <p style="margin:0; font-weight:700; color:#333;"><span class="{status_class}">{status_label}</span> &nbsp; {o.get('company', 'Unknown')}</p>
                <p style="margin:5px 0; font-size:13px; color:#666;">{o.get('types', '')}</p>
                <p style="margin:0; font-size:11px; color:#999;">Ontvangen: {o.get('received_date', '')}</p>
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
    st.markdown("<h3 style='color:#333333; margin-bottom: 10px;'>Order Details</h3>", unsafe_allow_html=True)
    selected = st.session_state.selected_order
    if not selected:
        st.info("Selecteer een order uit de inbox.")
    else:
        with st.container(border=True):
            st.markdown(f"## Order #{selected['id']}")
            st.markdown(f"**Bedrijf:** {selected['company']}")
            st.markdown(f"**Contact:** {selected['contact_name']} ({selected['phone']})")
            st.markdown(f"**Route:** {selected['pickup_address']} ➔ {selected['delivery_address']}")
            st.info(selected.get('info') or "Geen extra info.")
            
            st.write("---")
            c_btn1, c_btn2, _ = st.columns([2, 2, 3])
            
            if selected['status'] == 'New':
                with c_btn1:
                    if st.button("Verwerk Order", use_container_width=True):
                        now = datetime.now().strftime("%Y-%m-%d %H:%M")
                        supabase.table("orders").update({"status": "Processed", "processed_at": now}).eq("id", selected['id']).execute()
                        st.session_state.selected_order = None 
                        st.rerun()
                with c_btn2:
                    if st.button("Verwijder Request", type="secondary", use_container_width=True):
                        confirm_delete_dialog(selected['id'])
            else:
                with c_btn1:
                    if st.button("Verwijder uit Historie", type="secondary", use_container_width=True):
                        confirm_delete_dialog(selected['id'])

# --- NAVIGATIE ---
st.write("---")
_, c_nav1, c_nav2 = st.columns([2, 1, 1])
with c_nav1:
    if st.button("Terug naar Website", type="secondary", use_container_width=True): st.switch_page("Home.py")
with c_nav2:
    if st.button("Open Dashboard", use_container_width=True): st.switch_page("pages/Dashboard.py")
