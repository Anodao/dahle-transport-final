import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Dahle Transport - Home",
    page_icon="🚚",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }
    
    /* Verberg sidebar en standaard header */
    [data-testid="collapsedControl"], [data-testid="stSidebar"], header[data-testid="stHeader"] { display: none !important; }
    
    .stApp { background-color: #f8f9fa !important; }
    .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: #111111 !important; }

    /* --- NAVBAR STYLE --- */
    .block-container { padding-top: 130px !important; }
    .navbar {
        position: fixed; top: 0; left: 0; width: 100%; height: 90px;
        background-color: #ffffff !important; z-index: 999; border-bottom: 1px solid #eaeaea; 
        display: grid; grid-template-columns: 1fr auto 1fr; align-items: center;
        padding: 0 40px; box-shadow: 0 2px 10px rgba(0,0,0,0.03);
    }
    .nav-logo img { height: 48px; width: auto; transition: transform 0.2s; }
    .nav-links { display: flex; gap: 28px; font-size: 15px; font-weight: 500; justify-content: center; }
    .nav-links a, .nav-links span { text-decoration: none; color: #111111 !important; cursor: pointer; }
    .nav-cta { display: flex; justify-content: flex-end; gap: 15px; }
    
    .cta-btn { background-color: #894b9d !important; color: white !important; padding: 10px 24px; border-radius: 50px; text-decoration: none !important; font-weight: 600; font-size: 13px; white-space: nowrap;}
    .cta-btn-outline { background-color: transparent !important; color: #894b9d !important; padding: 10px 20px; border-radius: 50px; text-decoration: none !important; font-weight: 600; font-size: 13px; border: 2px solid #894b9d; white-space: nowrap;}

    /* --- KINETIC ARCHITECT BUTTON STYLING (Aangepast naar Dahle Transport Paars) --- */
    
    /* Main Primary Button (De grote paarse knop met gradient) */
    div.stButton > button[kind="primary"] { 
        background: linear-gradient(135deg, #9d5bb3 0%, #894b9d 100%) !important; 
        color: white !important; 
        border: none !important; 
        border-radius: 6px !important; 
        padding: 16px 28px !important; 
        font-weight: 600 !important; 
        font-size: 15px !important;
        letter-spacing: 0.02em !important;
        text-transform: none !important;
        box-shadow: 0 4px 14px 0 rgba(137, 75, 157, 0.3) !important; /* Subtiele paarse schaduw */
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        width: 100% !important;
    }

    div.stButton > button[kind="primary"]:hover { 
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(137, 75, 157, 0.4) !important;
        filter: brightness(1.05) !important;
    }

    div.stButton > button[kind="primary"]:active {
        transform: translateY(0px) !important;
    }

    /* Secondary/Outline Style Buttons (Licht paars met donkere rand) */
    div.stButton > button[kind="secondary"] {
        background: rgba(137, 75, 157, 0.05) !important; 
        color: #894b9d !important; 
        padding: 14px 24px !important;
        border-radius: 6px !important; 
        font-weight: 600 !important; 
        font-size: 14px !important; 
        letter-spacing: 0.02em !important; 
        border: 1px solid rgba(137, 75, 157, 0.3) !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }

    div.stButton > button[kind="secondary"]:hover { 
        background: rgba(137, 75, 157, 0.15) !important; 
        border-color: #894b9d !important;
        color: #723e83 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(137, 75, 157, 0.15) !important;
    }
    
    /* Layout styling voor de inhoud */
    .hero-section { text-align: center; padding: 40px 0; }
    .hero-section h1 { font-size: 2.5rem; font-weight: 700; color: #894b9d !important; margin-bottom: 10px; }
    .hero-section p { font-size: 1.1rem; color: #666 !important; margin-bottom: 40px; }
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
            <a href="/Opter_Portal" target="_self" class="cta-btn-outline">OPTER LOGIN</a>
            <a href="/" target="_self" class="cta-btn">TA KONTAKT</a>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- HOMEPAGE INHOUD ---
st.markdown("""
<div class="hero-section">
    <h1>Welkom bij het Portaal</h1>
    <p>Kies hieronder de applicatie die je wilt openen om verder te gaan.</p>
</div>
""", unsafe_allow_html=True)

# Twee kolommen in het midden van het scherm voor de knoppen
c_left, c_right = st.columns(2, gap="large")

with c_left:
    # Dit wordt de donkerpaarse knop (door type="primary" te gebruiken)
    if st.button("Open Planner Inbox", type="primary"):
        st.switch_page("pages/Planner.py")

with c_right:
    # Dit wordt de lichtpaarse, doorzichtige knop (door type="secondary" te gebruiken)
    if st.button("Open Dashboard", type="secondary"):
        st.switch_page("pages/Dashboard.py")

st.markdown("<br><br><br><p style='text-align: center; color: #999; font-size: 12px;'>Dahle Transport Internal Tools © 2026</p>", unsafe_allow_html=True)
