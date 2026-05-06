import streamlit as st
import extra_streamlit_components as stx
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="Dahle Transport - Hjem", layout="wide", initial_sidebar_state="collapsed")

# =========================================================
# 1. DIRECTE CSS INJECTIE (Design & Layout)
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }
.stApp { background-color: #111111 !important; }

/* VERBERG STREAMLIT BRANDING */
[data-testid="collapsedControl"], [data-testid="stSidebar"], header[data-testid="stHeader"] { display: none !important; }
footer { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
div[class^="viewerBadge"] { display: none !important; }
.block-container { padding: 0 !important; }

/* NAVBAR CSS */
.navbar { position: fixed; top: 0; left: 0; width: 100%; height: 90px; background-color: #ffffff !important; z-index: 999; display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; padding: 0 40px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
.nav-logo { display: flex; justify-content: flex-start; margin-left: 20px; }
.nav-logo a { display: inline-block; height: 48px; text-decoration: none; }
.nav-logo img { height: 100%; width: auto; display: block; transition: transform 0.2s ease; }
.nav-logo a:hover img { transform: scale(1.05); } 

.nav-links { display: flex; gap: 28px; font-size: 15px; font-weight: 600; justify-content: center; align-items: center;}
.nav-links a, .nav-links span { text-decoration: none; color: #111111 !important; cursor: pointer; transition: color 0.2s;}
.nav-links span:hover { color: #894b9d !important; }

/* DROPDOWN MENU */
.nav-text-dropdown { position: relative; display: inline-block; cursor: pointer; padding-bottom: 20px; margin-bottom: -20px; }
.nav-text-dropbtn { background: transparent; border: none; font-size: 15px; font-weight: 600; color: #111111 !important; cursor: pointer; padding: 0; font-family: inherit; display: flex; align-items: center; gap: 4px; }
.nav-text-dropdown:hover .nav-text-dropbtn { color: #894b9d !important; }
.nav-text-dropdown-content { display: none; position: absolute; top: calc(100% + 10px); left: 50%; transform: translateX(-50%); background-color: #ffffff; min-width: 180px; box-shadow: 0px 8px 24px rgba(0,0,0,0.12); border-radius: 12px; border: 1px solid #eaeaea; z-index: 1000; overflow: hidden; }
.nav-text-dropdown-content a { color: #111111 !important; padding: 12px 16px; text-decoration: none; display: block; font-size: 14px; font-weight: 500; text-align: left; transition: background-color 0.2s; border-bottom: none !important; }
.nav-text-dropdown-content a:hover { background-color: #f4e9f7; color: #894b9d !important; }
.nav-text-dropdown:hover .nav-text-dropdown-content { display: block; }

.nav-cta { display: flex; justify-content: flex-end; gap: 15px; align-items: center; }
.cta-btn-purple { background-color: #894b9d !important; color: white !important; padding: 12px 28px; border-radius: 50px; text-decoration: none !important; font-weight: 600; font-size: 13px; transition: 0.2s; white-space: nowrap;}
.cta-btn-purple:hover { background-color: #723e83 !important; transform: translateY(-2px); }
.cta-btn-outline { background-color: transparent !important; color: #894b9d !important; padding: 10px 20px; border-radius: 50px; text-decoration: none !important; font-weight: 600; font-size: 13px; border: 2px solid #894b9d; transition: 0.2s; white-space: nowrap;}
.cta-btn-outline:hover { background-color: #f4e9f7 !important; }

/* HERO SECTION */
.hero-section { position: relative; width: 100%; height: 100vh; min-height: 700px; background-color: #111; overflow: hidden; display: flex; align-items: center; }
.hero-content { position: relative; z-index: 10; width: 50%; padding-left: 10%; }
.hero-title { font-size: 72px; font-weight: 800; color: white; margin-bottom: 10px; line-height: 1.1; letter-spacing: -2px; }
.hero-subtitle { font-size: 18px; color: #cccccc; margin-bottom: 40px; font-weight: 500; }

/* OPENING HOURS BOX */
.opening-box { background: white; padding: 25px; border-radius: 12px; width: 350px; margin-bottom: 40px; color: #111; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
.opening-box h4 { margin: 0 0 10px 0; font-size: 15px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: #894b9d; }
.opening-box p { margin: 0; font-size: 15px; font-weight: 600; }
.opening-box small { color: #666; font-size: 12px; font-style: italic; }

/* HERO IMAGE (Mooie curve zoals in screenshot) */
.hero-image-container { position: absolute; top: 0; right: 0; width: 60%; height: 100%; background: url('https://cloud-1de12d.becdn.net/media/original/eb55018659f77f59796e6d1e49b814a0/scania-dahle-transport-fosen-trondheim-v-re-tjenester-1.webp') center/cover no-view; clip-path: polygon(25% 0%, 100% 0%, 100% 100%, 0% 100%); z-index: 5; }

/* TAAL DROPDOWN */
.lang-dropdown { position: relative; display: inline-block; margin-right: 10px; }
.lang-dropbtn { background-color: #f8f9fa; color: #111; font-weight: 600; font-size: 13px; border: 1px solid #eaeaea; border-radius: 20px; padding: 8px 16px; cursor: pointer; display: flex; align-items: center; gap: 6px; }
.lang-dropdown-content { display: none; position: absolute; background-color: #ffffff; min-width: 140px; box-shadow: 0px 8px 24px rgba(0,0,0,0.12); border-radius: 12px; z-index: 1000; top: calc(100% + 10px); right: 0; overflow: hidden; }
.lang-dropdown-content a { color: #111 !important; padding: 12px 16px; text-decoration: none; display: flex; align-items: center; gap: 10px; font-size: 14px; font-weight: 500; }
.lang-dropdown-content a:hover { background-color: #f4e9f7; color: #894b9d !important; }
.lang-dropdown:hover .lang-dropdown-content { display: block; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 2. COOKIE MANAGER & TAAL
# =========================================================
cookie_manager = stx.CookieManager()

# Kleine hack om cookies direct te laden
if 'cookie_retry' not in st.session_state:
    st.session_state.cookie_retry = True
    time.sleep(0.1)
    st.rerun()

saved_lang = cookie_manager.get('dahle_lang')

# Check of taal in URL staat (?lang=en)
if "lang" in st.query_params:
    url_lang = st.query_params["lang"]
    if url_lang in ["no", "en", "sv", "da"]:
        if url_lang != saved_lang:
            cookie_manager.set("dahle_lang", url_lang, key="set_lang_safe")
        st.session_state.language = url_lang
elif saved_lang and saved_lang in ["no", "en", "sv", "da"]:
    st.session_state.language = saved_lang
else:
    st.session_state.language = "no"

lang = st.session_state.language
lang_displays = { "no": "Norsk", "en": "English", "sv": "Svenska", "da": "Dansk" }
current_lang_display = lang_displays.get(lang, "Norsk")

# =========================================================
# 3. WOORDENBOEK
# =========================================================
translations = {
    "no": {
        "nav_home": "Hjem", "nav_about": "Om oss", "nav_services": "Tjenester", "nav_gallery": "Galleri", "nav_contact": "Kontakt", 
        "menu_title": "Sider ⌄", "menu_order": "Ny bestilling", "menu_request": "Kundehenvendelse", "menu_login": "Kundeportal",
        "nav_portal": "KUNDEPORTAL", "nav_contact_btn": "TA KONTAKT",
        "hero_t": "D ÅRNE SÆ!", "hero_s": "Rask og sikker transport, uansett distanse.",
        "open_t": "Åpningstider:", "open_d": "Mandag-fredag: 07:00-16:00", "open_note": "Åpningstidene kan avvike ved spesielle høytider.",
        "btn_order": "BESTILL", "btn_request": "FORESPØRSEL", "btn_contact": "TA KONTAKT"
    },
    "en": {
        "nav_home": "Home", "nav_about": "About us", "nav_services": "Services", "nav_gallery": "Gallery", "nav_contact": "Contact", 
        "menu_title": "Pages ⌄", "menu_order": "New Order", "menu_request": "Quick Request", "menu_login": "Customer Portal",
        "nav_portal": "CUSTOMER PORTAL", "nav_contact_btn": "CONTACT US",
        "hero_t": "IT'S COVERED!", "hero_s": "Fast and secure transport, regardless of distance.",
        "open_t": "Opening Hours:", "open_d": "Monday-Friday: 07:00-16:00", "open_note": "Hours may differ during public holidays.",
        "btn_order": "ORDER NOW", "btn_request": "REQUEST QUOTE", "btn_contact": "CONTACT US"
    }
}
t = translations.get(lang, translations["en"])

# =========================================================
# 4. NAVBAR SAMENSTELLEN
# =========================================================
# Dropdown links
dropdown_links = f"""
<a href="/Order?lang={lang}" target="_self">{t['menu_order']}</a>
<a href="/Request?lang={lang}" target="_self">{t['menu_request']}</a>
<a href="/Login?lang={lang}" target="_self">{t['menu_login']}</a>
"""

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
        <div class="nav-text-dropdown">
            <button class="nav-text-dropbtn">{t['menu_title']}</button>
            <div class="nav-text-dropdown-content">{dropdown_links}</div>
        </div>
    </div>
    <div class="nav-cta">
        <div class="lang-dropdown">
            <button class="lang-dropbtn">{current_lang_display} ⌄</button>
            <div class="lang-dropdown-content">
                <a href="?lang=en" target="_self">English</a>
                <a href="?lang=no" target="_self">Norsk</a>
                <a href="?lang=sv" target="_self">Svenska</a>
                <a href="?lang=da" target="_self">Dansk</a>
            </div>
        </div>
        <a href="/Login?lang={lang}" target="_self" class="cta-btn-outline">{t['nav_portal']}</a>
        <a href="/?lang={lang}" target="_self" class="cta-btn-purple">{t['nav_contact_btn']}</a>
    </div>
</div>
"""
st.markdown(html_navbar, unsafe_allow_html=True)

# =========================================================
# 5. HERO SECTION
# =========================================================
html_hero = f"""
<div class="hero-section">
    <div class="hero-content">
        <h1 class="hero-title">{t['hero_t']}</h1>
        <p class="hero-subtitle">{t['hero_s']}</p>
        
        <div class="opening-box">
            <h4>{t['open_t']}</h4>
            <p>{t['open_d']}</p>
            <small>{t['open_note']}</small>
        </div>
        
        <div style="display: flex; gap: 15px;">
            <a href="/Order?lang={lang}" target="_self" class="cta-btn-purple" style="padding: 18px 45px; font-size: 15px;">{t['btn_order']}</a>
            <a href="/Request?lang={lang}" target="_self" class="cta-btn-outline" style="padding: 18px 35px; font-size: 15px; border-width: 2px;">{t['btn_request']}</a>
            <a href="/?lang={lang}" target="_self" class="cta-btn-purple" style="padding: 18px 35px; font-size: 15px; background: transparent !important; border: 2px solid white !important;">{t['btn_contact']}</a>
        </div>
    </div>
    <div class="hero-image-container"></div>
</div>
"""
st.markdown(html_hero, unsafe_allow_html=True)

# Verberg de standaard Streamlit "pijltjes" en menu's die soms nog zichtbaar zijn
st.markdown("<script>window.parent.document.querySelector('section[data-testid=\"stSidebar\"]').remove();</script>", unsafe_allow_html=True)
