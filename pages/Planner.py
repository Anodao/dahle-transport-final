import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(page_title="Internal Planner", page_icon="🔒", layout="wide")

# --- CSS (Simpelere look voor intern gebruik) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }
    [data-testid="stToolbar"] { display: none; }
    .stApp { background-color: #f0f2f6; }
    .header-bar { background: #2c3e50; padding: 20px; color: white; border-radius: 10px; margin-bottom: 20px;}
    </style>
""", unsafe_allow_html=True)

# --- LOGICA ---
st.markdown('<div class="header-bar"><h1>🔒 Planner Dashboard</h1><p>Internal Use Only</p></div>', unsafe_allow_html=True)

if 'orders' not in st.session_state or not st.session_state.orders:
    st.info("No active orders found. Go to the Home page to place an order.")
else:
    col_list, col_detail = st.columns([1, 2])
    
    with col_list:
        st.subheader("📥 Inbox")
        for order in reversed(st.session_state.orders):
            icon = "🔴" if order['status'] == "New" else "🟢"
            with st.container(border=True):
                st.write(f"**{icon} {order['company']}**")
                st.caption(f"{order['type']} | {order['date']}")
                if st.button(f"Open Order #{order['id']}", key=order['id']):
                    st.session_state.selected_order = order

    with col_detail:
        st.subheader("📋 Order Details")
        if 'selected_order' in st.session_state:
            o = st.session_state.selected_order
            with st.container(border=True):
                st.markdown(f"### Order #{o['id']}")
                st.markdown(f"**Customer:** {o['company']}")
                st.markdown(f"**Email:** {o['email']}")
                st.divider()
                st.markdown(f"**Route:** {o['route']}")
                st.markdown(f"**Weight:** {o['weight']} kg")
                st.markdown(f"**Type:** {o['type']}")
                
            c1, c2, c3 = st.columns(3)
            if c1.button("✅ Approve"):
                o['status'] = "Approved"
                st.success("Approved!")
                st.rerun()
            if c3.button("❌ Reject"):
                o['status'] = "Rejected"
                st.warning("Rejected")
                st.rerun()
