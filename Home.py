import streamlit as st

# --- PAGE CONFIG ---
# Belangrijk: layout moet op 'wide' staan voor een full-screen website gevoel
st.set_page_config(page_title="Dahle Transport - Home", page_icon="🚚", layout="wide", initial_sidebar_state="collapsed")

# --- CSS STYLING, NAVBAR & HERO SECTION ---
st.markdown("""
    <style>
    /* Lettertypes inladen via Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Caveat:wght@700&display=swap'); /* Voor de handgeschreven titel */
    
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; margin: 0; padding: 0; }
    
    /* Streamlit's standaard marges en padding weghalen voor een full-screen ervaring */
    .stApp { background-color: #1e1e20 !important; }
    .block-container { padding: 0 !important; max-width: 100% !important; margin-top: 90px; }
    [data-testid="collapsedControl"], [data-testid="stSidebar"], header[data-testid="stHeader"] { display: none !important; }
    
    /* --- NAVBAR --- */
    .navbar { position: fixed; top: 0; left: 0; width: 100%; height: 90px; background-color: #ffffff !important; z-index: 999; display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; padding: 0 40px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
    .nav-logo a { display: inline-block; height: 48px; text-decoration: none; cursor: pointer; }
    .nav-logo img { height: 100%; width: auto; display: block; transition: transform 0.2s ease-in-out; }
    .nav-logo a:hover img { transform: scale(1.05); } 
    .nav-links { display: flex; gap: 28px; font-size: 15px; font-weight: 600; justify-content: center;}
    .nav-links a, .nav-links span { text-decoration: none; color: #111111 !important; cursor: pointer; transition: color 0.2s;}
    .nav-links span:hover { color: #894b9d !important; }
    .nav-cta { display: flex; justify-content: flex-end; gap: 15px; align-items: center; }
    .cta-btn-purple { background-color: #894b9d !important; color: white !important; padding: 10px 24px; border-radius: 50px; text-decoration: none !important; font-weight: 600; font-size: 13px; transition: background-color 0.2s;}
    .cta-btn-purple:hover { background-color: #723e83 !important; }
    .cta-btn-outline { background-color: transparent !important; color: #894b9d !important; padding: 10px 20px; border-radius: 50px; text-decoration: none !important; font-weight: 600; font-size: 13px; border: 2px solid #894b9d; }

    /* --- HERO SECTION (De gesplitste layout) --- */
    .hero-container {
        display: flex;
        flex-direction: row;
        width: 100%;
        min-height: calc(100vh - 90px); /* Schermhoogte minus de menubalk */
        background-color: #1a1c1e; /* Donkere achtergrondkleur links */
        overflow: hidden;
    }
    
    .hero-left {
        flex: 1;
        padding: 10% 5% 5% 15%; /* Schuift de tekst mooi naar het midden */
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: flex-start;
    }
    
    .hero-title {
        font-family: 'Caveat', cursive; /* Het handgeschreven lettertype */
        font-size: 80px;
        color: #ffffff;
        margin: 0 0 20px 0;
        letter-spacing: 2px;
        transform: rotate(-2deg); /* Geeft het een iets speelser effect, net als op de foto */
    }
    
    .hero-subtitle {
        font-size: 20px;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 40px;
    }
    
    .opening-box {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 25px 35px;
        width: 100%;
        max-width: 500px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin-bottom: 40px;
    }
    
    .opening-box p {
        color: #111111 !important;
        margin: 5px 0;
        font-size: 15px;
    }
    .opening-box strong { color: #111111; font-weight: 700; }
    .opening-box i { color: #666; font-size: 13px; }
    
    .circle-btn {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        border: 2px solid #ffffff;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-top: 20px;
        cursor: pointer;
        color: white;
        text-decoration: none;
        transition: 0.3s;
    }
    .circle-btn:hover { background-color: #ffffff; color: #1a1c1e; }
    
    /* --- RECHTERKANT (Foto met ronde vorm) --- */
    .hero-right {
        flex: 1.2;
        background-image: url('https://cloud-1de12d.becdn.net/media/iW=1200&iH=630/c9ca77aaff92037d097c5d1558e89fa1.jpg');
        background-size: cover;
        background-position: center left;
        /* Dit creëert de grote bolle ronding naar links */
        clip-path: ellipse(90% 100% at 100% 50%);
    }
    
    /* Zorg dat het op mobiel ook enigszins werkt door het onder elkaar te zetten */
    @media (max-width: 900px) {
        .hero-container { flex-direction: column; }
        .hero-right { min-height: 400px; clip-path: ellipse(100% 90% at 50% 100%); }
        .hero-left { padding: 10% 5%; align-items: center; text-align: center; }
        .hero-title { font-size: 60px; }
    }
    </style>
    
    <div class="navbar">
        <div class="nav-logo"><a href="/" target="_self"><img src="https://cloud-1de12d.becdn.net/media/original/964295c9ae8e693f8bb4d6b70862c2be/logo-website-top-png-1-.webp"></a></div>
        <div class="nav-links"><a href="/"><span>Hjem</span></a><span>Om oss</span><span>Tjenester</span><span>Galleri</span><span>Kontakt</span></div>
        <div class="nav-cta"><a href="/Order" target="_self" class="cta-btn-outline">BESTILL</a><a href="/" target="_self" class="cta-btn-purple">TA KONTAKT</a></div>
    </div>
    
    <div class="hero-container">
        <div class="hero-left">
            <h1 class="hero-title">D ÅRNE SÆ!</h1>
            <p class="hero-subtitle">Rask og sikker transport, uansett distanse.</p>
            
            <div class="opening-box">
                <p><strong>Åpningstider:</strong></p>
                <p>Mandag-fredag: 07:00-16:00</p>
                <p><i>Åpningstidene kan avvike ved spesielle høytider.</i></p>
            </div>
            
            <a href="#" class="cta-btn-purple" style="font-size: 16px; padding: 12px 30px;">TA KONTAKT</a>
            
            <a href="#more" class="circle-btn">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><polyline points="19 12 12 19 5 12"></polyline></svg>
            </a>
        </div>
        
        <div class="hero-right"></div>
    </div>
""", unsafe_allow_html=True)
