import streamlit as st
from supabase import create_client
import extra_streamlit_components as stx
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="Dahle Transport - Home", page_icon="🚚", layout="wide", initial_sidebar_state="collapsed")

# =========================================================
# 1. DIRECTE CSS INJECTIE (Schoon & Gebruiksvriendelijk)
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Caveat:wght@700&display=swap');

html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; margin: 0; padding: 0; }
.stApp { background-color: #1e1e20 !important; }
.block-container { padding: 0 !important; max-width: 100% !important; margin-top: 90px; }

/* VERBERG STREAMLIT BRANDING VOLLEDIG */
[data-testid="collapsedControl"], [data-testid="stSidebar"], header[data-testid="stHeader"] { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
footer { display: none !important; }
div[class^="viewerBadge"] { display: none !important; }

/* NAVBAR CSS */
.navbar { 
    position: fixed; top: 0; left: 0; width: 100%; height: 90px; 
    background-color: #ffffff !important; z-index: 999; 
    display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; 
    padding: 0 40px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); 
}

.nav-logo { display: flex; justify-content: flex-start; margin-left: 20px; }
.nav-logo a { display: inline-block; height: 48px; text-decoration: none; cursor: pointer; }
.nav-logo img { height: 100%; width: auto; display: block; transition: transform 0.2s ease-in-out; }
.nav-logo a:hover img { transform: scale(1.05); } 

.nav-links { display: flex; gap: 28px; font-size: 15px; font-weight: 600; justify-content: center; align-items: center;}
.nav-links a, .nav-links span { text-decoration: none; color: #111111 !important; cursor: pointer; transition: color 0.2s;}
.nav-links span:hover { color: #894b9d !important; }

.nav-cta { display: flex; justify-content: flex-end; gap: 15px; align-items: center; }
.cta-btn-purple { 
    background-color: #894b9d !important; color: white !important; 
    padding: 10px 24px; border-radius: 50px; text-decoration: none !important; 
    font-weight: 600; font-size: 13px; transition: background-color 0.2s; white-space: nowrap;
}
.cta-btn-purple:hover { background-color: #723e83 !important; }

/* DROPDOWN STYLING (Voor Taal en Navigatie) */
.custom-dropdown { position: relative; display: inline-block; }
.custom-dropbtn { 
    background-color: #f8f9fa; color: #111; font-weight: 600; font-size: 13px; 
    border: 1px solid #eaeaea; border-radius: 20px; padding: 8px 16px; 
    cursor: pointer; display: flex; align-items: center; gap: 6px; 
    box-shadow: 0 2px 5px rgba(0,0,0,0.03); transition: all 0.2s ease; 
}
.custom-dropbtn:hover { background-color: #eaeaea; }

/* De 'Outline' variant voor de menu knop */
.btn-outline { 
    background-color: transparent !important; border: 2px solid #894b9d !important; 
    color: #894b9d !important; 
}

.custom-dropdown-content { 
    display: none; position: absolute; background-color: #ffffff; 
    min-width: 180px; box-shadow: 0px 8px 24px rgba(0,0,0,0.12); 
    border-radius: 12px; border: 1px solid #eaeaea; z-index: 1000; 
    top: 40px; right: 0; overflow: hidden; 
}

/* Onzichtbare brug om menu open te houden */
.custom-dropdown::after { content: ''; position: absolute; top: 100%; left: 0; width: 100%; height: 15px; background: transparent; }

.custom-dropdown:hover .custom-dropdown-content { display: block; }

.custom-dropdown-content a { 
    color: #111 !important; padding: 12px 16px; text-decoration: none; 
    display: flex; align-items: center; gap: 10px; font-size: 14px; 
    font-weight: 500; transition: background-color 0.2s; 
}
.custom-dropdown-content a:hover { background-color: #f4e9f7; color: #894b9d !important; }

/* HERO SECTION */
.hero-container { display: flex; flex-direction: row; width: 100%; min-height: calc(100vh - 90px); background-color: #1a1c1e; overflow: hidden; }
.hero-left { flex: 1; padding: 10% 5% 5% 15%; display: flex; flex-direction: column; justify-content: center; align-items: flex-start; }
.hero-title { font-family: 'Caveat', cursive; font-size: 80px; color: #ffffff; margin: 0 0 20px 0; letter-spacing: 2px; transform: rotate(-2deg); }
.hero-subtitle { font-size: 20px; font-weight: 600; color: #ffffff; margin-bottom: 40px; }
.opening-box { background-color: #ffffff; border-radius: 8px; padding: 25px 35px; width: 100%; max-width: 500px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); margin-bottom: 40px; }
.opening-box p { color: #111111 !important; margin: 5px 0; font-size: 15px; }
.circle-btn { width: 50px; height: 50px; border-radius: 50%; border: 2px solid #ffffff; display: flex; align-items: center; justify-content: center; margin-top: 20px; cursor: pointer; color: white; text-decoration: none; transition: 0.3s; }
.hero-right { flex: 1.2; background-image: url('https://cloud-1de12d.becdn.net/media/iW=1200&iH=630/c9ca77aaff92037d097c5d1558e89fa1.jpg'); background-size: cover; background-position: center left; clip-path: ellipse(90% 100% at 100% 50%); }

@media (max-width: 900px) { .hero-container { flex-direction: column; } .hero-right { min-height: 400px; } .hero-left { padding: 10% 5%; align-items: center; text-align: center; } }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 2. TAAL LOGICA
# =========================================================
if 'language' not in st.session_state:
    st.session_state.language = "no"

if "lang" in st.query_params:
    url_lang = st.query_params["lang"]
    if url_lang in ["no", "en", "sv", "da"]:
        st.session_state.language = url_lang

lang = st.session_state.language
lang_displays = { "no": "🇳🇴 Norsk", "en": "🇬🇧 English", "sv": "🇸🇪 Svenska", "da": "🇩🇰 Dansk" }
current_lang_display = lang_displays.get(lang, "🇳🇴 Norsk")

# =========================================================
# 3. WOORDENBOEK
# =========================================================
translations = {
    "no": { 
        "nav_home": "Hjem", "nav_about": "Om oss", "nav_services": "Tjenester", "nav_gallery": "Galleri", "nav_contact": "Kontakt", 
        "menu_title": "Navigasjon ⌄", "menu_login": "Kundeportal", "menu_order": "Ny bestilling", "menu_dash": "CO2 Dashboard", "menu_plan": "Intern Planner",
        "nav_contact_btn": "TA KONTAKT", "hero_title": "D ÅRNE SÆ!", "hero_subtitle": "Rask og sikker transport, uansett distanse.", 
        "open_title": "Åpningstider:", "open_days": "Mandag-fredag: 07:00-16:00", "open_note": "Åpningstidene kan avvike ved spesielle høytider.", "btn_order": "BESTILL" 
    },
    "en": { 
        "nav_home": "Home", "nav_about": "About us", "nav_services": "Services", "nav_gallery": "Gallery", "nav_contact": "Contact", 
        "menu_title": "Navigation ⌄", "menu_login": "Customer Portal", "menu_order": "New Order", "menu_dash": "CO2 Dashboard", "menu_plan": "Internal Planner",
        "nav_contact_btn": "CONTACT US", "hero_title": "WE'VE GOT IT!", "hero_subtitle": "Fast and secure transport, regardless of distance.", 
        "open_title": "Opening Hours:", "open_days": "Monday-Friday: 07:00-16:00", "open_note": "Opening hours may vary during public holidays.", "btn_order": "ORDER NOW" 
    },
    "sv": { 
        "nav_home": "Hem", "nav_about": "Om oss", "nav_services": "Tjänster", "nav_gallery": "Galleri", "nav_contact": "Kontakt", 
        "menu_title": "Navigering ⌄", "menu_login": "Kundportal", "menu_order": "Ny beställning", "menu_dash": "CO2 Dashboard", "menu_plan": "Intern Planner",
        "nav_contact_btn": "KONTAKTA OSS", "hero_title": "VI LÖSER DET!", "hero_subtitle": "Snabb och säker transport, oavsett avstånd.", 
        "open_title": "Öppettider:", "open_days": "Måndag-fredag: 07:00-16:00", "open_note": "Öppettiderna kan variera under helgdagar.", "btn_order": "BESTÄLL" 
    },
    "da": { 
        "nav_home": "Hjem", "nav_about": "Om os", "nav_services": "Tjenester", "nav_gallery": "Galleri", "nav_contact": "Kontakt", 
        "menu_title": "Navigering ⌄", "menu_login": "Kundeportal", "menu_order": "Ny bestilling", "menu_dash": "CO2 Dashboard", "menu_plan": "Intern Planner",
        "nav_contact_btn": "KONTAKT OS", "hero_title": "VI KLARER DEN!", "hero_subtitle": "Hurtig og sikker transport, uanset afstand.", 
        "open_title": "Åbningstider:", "open_days": "Mandag-fredag: 07:00-16:00", "open_note": "Åbningstiderne kan afvige på helligdage.", "btn_order": "BESTIL" 
    }
}
t = translations[lang]

# =========================================================
# 4. NAVBAR SAMENSTELLEN
# =========================================================
html_navbar = f"""
<div class="navbar">
    <div class="nav-logo">
        <a href="/?lang={lang}" target="_self">
            <img src="https://cloud-1de12d.becdn.net/media/original/964295c9ae8e693f8bb4d6b70862c2be/logo-website-top-png-1-.webp">
        </a>
    </div>
    
    <div class="nav-links">
        <a href="/?lang={lang}" target="_self"><span>{t['nav_home']}</span></a>
        <span>{t['nav_about']}</span>
        <span>{t['nav_services']}</span>
        <span>{t['nav_gallery']}</span>
        <span>{t['nav_contact']}</span>
    </div>
    
    <div class="nav-cta">
        <div class="custom-dropdown">
            <button class="custom-dropbtn">{current_lang_display} ⌄</button>
            <div class="custom-dropdown-content">
                <a href="?lang=en" target="_self">🇬🇧 English</a>
                <a href="?lang=no" target="_self">🇳🇴 Norsk</a>
                <a href="?lang=sv" target="_self">🇸🇪 Svenska</a>
                <a href="?lang=da" target="_self">🇩🇰 Dansk</a>
            </div>
        </div>

        <div class="custom-dropdown">
            <button class="custom-dropbtn btn-outline">{t['menu_title']}</button>
            <div class="custom-dropdown-content">
                <a href="/Login?lang={lang}" target="_self">🔐 {t['menu_login']}</a>
                <a href="/Order?lang={lang}" target="_self">📦 {t['menu_order']}</a>
                <a href="/Dashboard?lang={lang}" target="_self">🌱 {t['menu_dash']}</a>
                <a href="/Planner?lang={lang}" target="_self">📅 {t['menu_plan']}</a>
            </div>
        </div>

        <a href="/?lang={lang}" target="_self" class="cta-btn-purple">{t['nav_contact_btn']}</a>
    </div>
</div>
"""
st.markdown(html_navbar, unsafe_allow_html=True)

# =========================================================
# 5. HERO SECTION
# =========================================================
st.markdown(f"""
<div class="hero-container">
    <div class="hero-left">
        <h1 class="hero-title">{t['hero_title']}</h1>
        <p class="hero-subtitle">{t['hero_subtitle']}</p>
        <div class="opening-box">
            <p><strong>{t['open_title']}</strong></p>
            <p>{t['open_days']}</p>
            <p><i>{t['open_note']}</i></p>
        </div>
        <div style="display: flex; gap: 15px;">
            <a href="/Order?lang={lang}" target="_self" class="cta-btn-purple" style="font-size: 16px; padding: 12px 30px;">{t['btn_order']}</a>
            <a href="#" target="_self" class="cta-btn-purple" style="font-size: 16px; padding: 12px 30px; background-color: transparent !important; border: 2px solid white !important;">{t['nav_contact_btn']}</a>
        </div>
        <a href="#more" class="circle-btn">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><polyline points="19 12 12 19 5 12"></polyline></svg>
        </a>
    </div>
    <div class="hero-right"></div>
</div>
""", unsafe_allow_html=True)
