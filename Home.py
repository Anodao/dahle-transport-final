import streamlit as st
from supabase import create_client
import extra_streamlit_components as stx
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="Dahle Transport - Home", page_icon="🚚", layout="wide", initial_sidebar_state="collapsed")

# =========================================================
# 0. DIRECTE CSS INJECTIE 
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Caveat:wght@700&display=swap');
html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; margin: 0; padding: 0; }
.stApp { background-color: #1e1e20 !important; }
.block-container { padding: 0 !important; max-width: 100% !important; margin-top: 90px; }

/* FIX 1: ZIJBALK PIJLTJE ALTIJD ZICHTBAAR */
header[data-testid="stHeader"] { background-color: transparent !important; z-index: 1001 !important; }
[data-testid="stToolbar"] { display: none !important; }
footer { display: none !important; }
div[class^="viewerBadge"] { display: none !important; }

/* NAVBAR CSS */
.navbar { position: fixed; top: 0; left: 0; width: 100%; height: 90px; background-color: #ffffff !important; z-index: 999; display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; padding: 0 40px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
.nav-logo { margin-left: 40px; display: flex; justify-content: flex-start; }
.nav-logo a { display: inline-block; height: 48px; text-decoration: none; cursor: pointer; }
.nav-logo img { height: 100%; width: auto; display: block; transition: transform 0.2s ease-in-out; }
.nav-logo a:hover img { transform: scale(1.05); } 
.nav-links { display: flex; gap: 28px; font-size: 15px; font-weight: 600; justify-content: center; align-items: center;}
.nav-links a, .nav-links span { text-decoration: none; color: #111111 !important; cursor: pointer; transition: color 0.2s;}
.nav-links span:hover { color: #894b9d !important; }
.nav-cta { display: flex; justify-content: flex-end; gap: 15px; align-items: center; }
.cta-btn-purple { background-color: #894b9d !important; color: white !important; padding: 10px 24px; border-radius: 50px; text-decoration: none !important; font-weight: 600; font-size: 13px; transition: background-color 0.2s; white-space: nowrap;}
.cta-btn-purple:hover { background-color: #723e83 !important; }
.cta-btn-outline { background-color: transparent !important; color: #894b9d !important; padding: 10px 20px; border-radius: 50px; text-decoration: none !important; font-weight: 600; font-size: 13px; border: 2px solid #894b9d; max-width: 250px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;}

/* FIX 2: DROPDOWN MENU */
.lang-dropdown { position: relative; display: inline-block; margin-right: 10px; padding-bottom: 15px; margin-bottom: -15px; }
.lang-dropbtn { background-color: #f8f9fa; color: #111; font-weight: 600; font-size: 13px; border: 1px solid #eaeaea; border-radius: 20px; padding: 8px 16px; cursor: pointer; display: flex; align-items: center; gap: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.03); transition: all 0.2s ease; }
.lang-dropbtn:hover { background-color: #eaeaea; }
.lang-dropdown-content { display: none; position: absolute; background-color: #ffffff; min-width: 140px; box-shadow: 0px 8px 24px rgba(0,0,0,0.12); border-radius: 12px; border: 1px solid #eaeaea; z-index: 1000; top: 100%; right: 0; overflow: hidden; }
.lang-dropdown-content a { color: #111 !important; padding: 12px 16px; text-decoration: none; display: flex; align-items: center; gap: 10px; font-size: 14px; font-weight: 500; transition: background-color 0.2s; }
.lang-dropdown-content a:hover { background-color: #f4e9f7; color: #894b9d !important; }
.lang-dropdown:hover .lang-dropdown-content { display: block; }

.hero-container { display: flex; flex-direction: row; width: 100%; min-height: calc(100vh - 90px); background-color: #1a1c1e; overflow: hidden; }
.hero-left { flex: 1; padding: 10% 5% 5% 15%; display: flex; flex-direction: column; justify-content: center; align-items: flex-start; }
.hero-title { font-family: 'Caveat', cursive; font-size: 80px; color: #ffffff; margin: 0 0 20px 0; letter-spacing: 2px; transform: rotate(-2deg); }
.hero-subtitle { font-size: 20px; font-weight: 600; color: #ffffff; margin-bottom: 40px; }
.opening-box { background-color: #ffffff; border-radius: 8px; padding: 25px 35px; width: 100%; max-width: 500px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); margin-bottom: 40px; }
.opening-box p { color: #111111 !important; margin: 5px 0; font-size: 15px; }
.opening-box strong { color: #111111; font-weight: 700; }
.opening-box i { color: #666; font-size: 13px; }
.circle-btn { width: 50px; height: 50px; border-radius: 50%; border: 2px solid #ffffff; display: flex; align-items: center; justify-content: center; margin-top: 20px; cursor: pointer; color: white; text-decoration: none; transition: 0.3s; }
.circle-btn:hover { background-color: #ffffff; color: #1a1c1e; }
.hero-right { flex: 1.2; background-image: url('https://cloud-1de12d.becdn.net/media/iW=1200&iH=630/c9ca77aaff92037d097c5d1558e89fa1.jpg'); background-size: cover; background-position: center left; clip-path: ellipse(90% 100% at 100% 50%); }

@media (max-width: 900px) { .hero-container { flex-direction: column; } .hero-right { min-height: 400px; clip-path: ellipse(100% 90% at 50% 100%); } .hero-left { padding: 10% 5%; align-items: center; text-align: center; } .hero-title { font-size: 60px; } }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 1. INIT COOKIE MANAGER & TAAL LOGICA
# =========================================================
cookie_manager = stx.CookieManager()

saved_lang = cookie_manager.get('dahle_lang')
if 'language' not in st.session_state:
    st.session_state.language = saved_lang if saved_lang else "no"

if "lang" in st.query_params:
    gekozen_taal = st.query_params["lang"]
    if gekozen_taal in ["no", "en", "sv", "da"]:
        st.session_state.language = gekozen_taal
        cookie_manager.set("dahle_lang", gekozen_taal, key="set_lang_safe")
    st.query_params.clear()
    st.rerun()

lang = st.session_state.language
lang_displays = { "no": "🇳🇴 Norsk", "en": "🇬🇧 English", "sv": "🇸🇪 Svenska", "da": "🇩🇰 Dansk" }
current_lang_display = lang_displays.get(lang, "🇳🇴 Norsk")

# =========================================================
# 2. DATABASE & AUTHENTICATIE
# =========================================================
def init_connection():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

if 'supabase_client' not in st.session_state:
    try: st.session_state.supabase_client = init_connection()
    except: pass

supabase = st.session_state.supabase_client

if 'user' not in st.session_state:
    st.session_state.user = None

acc_token = cookie_manager.get('dahle_acc')
ref_token = cookie_manager.get('dahle_ref')

if st.session_state.get('user') is None and acc_token and ref_token:
    loading_text = "Laster inn konto... ⏳" if lang == "no" else "Loading account... ⏳"
    with st.spinner(loading_text): 
        time.sleep(0.5) 
        try:
            session = supabase.auth.set_session(acc_token, ref_token)
            st.session_state.user = session.user
            prof_res = supabase.table("profiles").select("company_name").eq("id", session.user.id).execute()
            if prof_res.data: st.session_state.company_name = prof_res.data[0]["company_name"]
        except Exception: pass

# =========================================================
# 3. HET WOORDENBOEK
# =========================================================
translations = {
    "no": { "nav_home": "Hjem", "nav_about": "Om oss", "nav_services": "Tjenester", "nav_gallery": "Galleri", "nav_contact": "Kontakt", "nav_portal": "KUNDEPORTAL", "nav_contact_btn": "TA KONTAKT", "hero_title": "D ÅRNE SÆ!", "hero_subtitle": "Rask og sikker transport, uansett distanse.", "open_title": "Åpningstider:", "open_days": "Mandag-fredag: 07:00-16:00", "open_note": "Åpningstidene kan avvike ved spesielle høytider.", "btn_order": "BESTILL" },
    "en": { "nav_home": "Home", "nav_about": "About us", "nav_services": "Services", "nav_gallery": "Gallery", "nav_contact": "Contact", "nav_portal": "CUSTOMER PORTAL", "nav_contact_btn": "CONTACT US", "hero_title": "WE'VE GOT IT!", "hero_subtitle": "Fast and secure transport, regardless of distance.", "open_title": "Opening Hours:", "open_days": "Monday-Friday: 07:00-16:00", "open_note": "Opening hours may vary during public holidays.", "btn_order": "ORDER NOW" },
    "sv": { "nav_home": "Hem", "nav_about": "Om oss", "nav_services": "Tjänster", "nav_gallery": "Galleri", "nav_contact": "Kontakt", "nav_portal": "KUNDPORTAL", "nav_contact_btn": "KONTAKTA OSS", "hero_title": "VI LÖSER DET!", "hero_subtitle": "Snabb och säker transport, oavsett avstånd.", "open_title": "Öppettider:", "open_days": "Måndag-fredag: 07:00-16:00", "open_note": "Öppettiderna kan variera under helgdagar.", "btn_order": "BESTÄLL" },
    "da": { "nav_home": "Hjem", "nav_about": "Om os", "nav_services": "Tjenester", "nav_gallery": "Galleri", "nav_contact": "Kontakt", "nav_portal": "KUNDEPORTAL", "nav_contact_btn": "KONTAKT OS", "hero_title": "VI KLARER DEN!", "hero_subtitle": "Hurtig og sikker transport, uanset afstand.", "open_title": "Åbningstider:", "open_days": "Mandag-fredag: 07:00-16:00", "open_note": "Åbningstiderne kan afvige på helligdage.", "btn_order": "BESTIL" }
}

t = translations.get(lang, translations["no"])

if st.session_state.get('user') is not None and 'company_name' in st.session_state:
    icoon = "<svg style='width:16px; height:16px; margin-right:8px; vertical-align:-2px; fill:currentColor;' viewBox='0 0 640 512'><path d='M224 256A128 128 0 1 0 224 0a128 128 0 1 0 0 256zm-45.7 48C79.8 304 0 383.8 0 482.3C0 498.7 13.3 512 29.7 512H322.8c-3.1-8.8-3.7-18.4-1.4-27.8l15-60.1c2.8-11.3 8.6-21.5 16.8-29.7l40.3-40.3c-32.4-31.6-78-50.1-126.5-50.1H178.3zm212.8-38.1l-40.3 40.3c-15.9 15.9-27.2 35.8-32.5 57.2l-15 60.1c-1.3 5.3-.2 10.9 3.1 15.3s8.5 7.1 14 7.1H592c5.5 0 10.7-2.7 14-7.1s4.4-10 3.1-15.3l-15-60.1c-5.3-21.4-16.6-41.3-32.5-57.2l-40.3-40.3c-23.4-23.4-60.6-23.4-84 0zM456 432c-13.3 0-24-10.7-24-24s10.7-24 24-24s24 10.7 24 24s-10.7 24-24 24z'/></svg>"
    knop_tekst = f"{icoon}{st.session_state.company_name}"
else:
    knop_tekst = t['nav_portal']

# =========================================================
# 5. DYNAMISCHE HTML 
# =========================================================
html_code = f"""
<div class="navbar">
<div class="nav-logo"><a href="/?lang={lang}" target="_self"><img src="https://cloud-1de12d.becdn.net/media/original/964295c9ae8e693f8bb4d6b70862c2be/logo-website-top-png-1-.webp"></a></div>
<div class="nav-links">
<a href="/?lang={lang}" target="_self"><span>{t['nav_home']}</span></a>
<span>{t['nav_about']}</span>
<span>{t['nav_services']}</span>
<span>{t['nav_gallery']}</span>
<span>{t['nav_contact']}</span>
</div>
<div class="nav-cta">
<div class="lang-dropdown">
<button class="lang-dropbtn">{current_lang_display} ⌄</button>
<div class="lang-dropdown-content">
<a href="?lang=en" target="_self">🇬🇧 English</a>
<a href="?lang=no" target="_self">🇳🇴 Norsk</a>
<a href="?lang=sv" target="_self">🇸🇪 Svenska</a>
<a href="?lang=da" target="_self">🇩🇰 Dansk</a>
</div>
</div>
<a href="/Login?lang={lang}" target="_self" class="cta-btn-outline">{knop_tekst}</a>
<a href="/?lang={lang}" target="_self" class="cta-btn-purple">{t['nav_contact_btn']}</a>
</div>
</div>

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
<a href="/?lang={lang}" target="_self" class="cta-btn-purple" style="font-size: 16px; padding: 12px 30px;">{t['nav_contact_btn']}</a>
</div>
<a href="#more" class="circle-btn">
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><polyline points="19 12 12 19 5 12"></polyline></svg>
</a>
</div>
<div class="hero-right"></div>
</div>
"""
st.markdown(html_code, unsafe_allow_html=True)
