import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(page_title="Dahle Transport - Home", page_icon="🚚", layout="centered", initial_sidebar_state="collapsed")

# --- CSS STYLING & NAVBAR ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }
    .stApp { background-color: #111111 !important; }
    .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown li { color: #ffffff !important; }
    [data-testid="collapsedControl"], [data-testid="stSidebar"], header[data-testid="stHeader"] { display: none !important; }
    
    .block-container { padding-top: 110px; }
    .navbar { position: fixed; top: 0; left: 0; width: 100%; height: 90px; background-color: #ffffff !important; z-index: 999; border-bottom: 1px solid #eaeaea; display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; padding: 0 40px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
    .nav-logo a { display: inline-block; height: 48px; text-decoration: none; cursor: pointer; }
    .nav-logo img { height: 100%; width: auto; display: block; transition: transform 0.2s ease-in-out; }
    .nav-logo a:hover img { transform: scale(1.05); } 
    .nav-links { display: flex; gap: 28px; font-size: 15px; font-weight: 500; justify-content: center;}
    .nav-links a, .nav-links span { text-decoration: none; color: #111111 !important; cursor: pointer; transition: color 0.2s;}
    .nav-links span:hover { color: #894b9d !important; }
    .nav-cta { display: flex; justify-content: flex-end; gap: 15px; align-items: center; }
    .cta-btn { background-color: #894b9d !important; color: white !important; padding: 10px 24px; border-radius: 50px; text-decoration: none !important; font-weight: 600; font-size: 13px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); white-space: nowrap;}
    .cta-btn-outline { background-color: transparent !important; color: #894b9d !important; padding: 10px 20px; border-radius: 50px; text-decoration: none !important; font-weight: 600; font-size: 13px; border: 2px solid #894b9d; white-space: nowrap;}
    </style>
    
    <div class="navbar">
        <div class="nav-logo"><a href="/" target="_self"><img src="https://cloud-1de12d.becdn.net/media/original/964295c9ae8e693f8bb4d6b70862c2be/logo-website-top-png-1-.webp"></a></div>
        <div class="nav-links"><a href="/"><span>Hjem</span></a><span>Om oss</span><span>Tjenester</span><span>Galleri</span><span>Kontakt</span></div>
        <div class="nav-cta"><a href="/Login" target="_self" class="cta-btn-outline">KUNDEPORTAL</a><a href="/Order" target="_self" class="cta-btn">BESTILL TRANSPORT</a></div>
    </div>
""", unsafe_allow_html=True)

# --- WELKOMST SCHERM ---
st.write("")
st.write("")
st.markdown("<h1 style='text-align: center; font-size: 42px;'>Velkommen til Dahle Transport</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888; font-size: 18px;'>Rask, pålitelig og bærekraftig transport i hele Norge.</p>", unsafe_allow_html=True)
st.write("---")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.info("Klaar om iets te verzenden? Gebruik de knop **'BESTILL TRANSPORT'** rechtsbovenin om direct uw route en prijs te berekenen.")
