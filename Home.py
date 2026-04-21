import streamlit as st
from supabase import create_client
import extra_streamlit_components as stx

# --- PAGE CONFIG ---
st.set_page_config(page_title="Dahle Transport - Home", page_icon="🚚", layout="wide", initial_sidebar_state="collapsed")

# =========================================================
# 1. DATABASE & COOKIE CHECKER (MET LAAD-CIRKEL)
# =========================================================
# Dit voorkomt de NameError!
cookie_manager = stx.CookieManager()

def init_connection():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

if 'supabase_client' not in st.session_state:
    try:
        st.session_state.supabase_client = init_connection()
    except:
        pass

supabase = st.session_state.supabase_client

if 'user' not in st.session_state:
    st.session_state.user = None

# Lees de cookies uit je browser
acc_token = cookie_manager.get('dahle_acc')
ref_token = cookie_manager.get('dahle_ref')

# Als je nog niet in het geheugen zit, maar wel een cookie hebt: Inloggen!
if st.session_state.user is None and acc_token and ref_token:
    # HIER IS DE LAAD-CIRKEL TOEGEVOEGD:
    with st.spinner("Laster inn konto... ⏳"): 
        try:
            session = supabase.auth.set_session(acc_token, ref_token)
            st.session_state.user = session.user
            
            # Omdat we op Home zijn, trekken we ook even je bedrijfsnaam uit Supabase
            prof_res = supabase.table("profiles").select("company_name").eq("id", session.user.id).execute()
            if prof_res.data:
                st.session_state.company_name = prof_res.data[0]["company_name"]
        except Exception:
            pass

# =========================================================
# 2. BEPAAL DE TEKST VOOR DE NAVBAR (MET ICOONTJE)
# =========================================================
if st.session_state.user is not None and 'company_name' in st.session_state:
    # Dit is de wiskundige code (SVG) voor exact dat poppetje met het slotje!
    icoon = "<svg style='width:16px; height:16px; margin-right:8px; vertical-align:-2px; fill:currentColor;' viewBox='0 0 640 512'><path d='M224 256A128 128 0 1 0 224 0a128 128 0 1 0 0 256zm-45.7 48C79.8 304 0 383.8 0 482.3C0 498.7 13.3 512 29.7 512H322.8c-3.1-8.8-3.7-18.4-1.4-27.8l15-60.1c2.8-11.3 8.6-21.5 16.8-29.7l40.3-40.3c-32.4-31.6-78-50.1-126.5-50.1H178.3zm212.8-38.1l-40.3 40.3c-15.9 15.9-27.2 35.8-32.5 57.2l-15 60.1c-1.3 5.3-.2 10.9 3.1 15.3s8.5 7.1 14 7.1H592c5.5 0 10.7-2.7 14-7.1s4.4-10 3.1-15.3l-15-60.1c-5.3-21.4-16.6-41.3-32.5-57.2l-40.3-40.3c-23.4-23.4-60.6-23.4-84 0zM456 432c-13.3 0-24-10.7-24-24s10.7-24 24-24s24 10.7 24 24s-10.7 24-24 24z'/></svg>"
    
    # Plak het icoon en de bedrijfsnaam aan elkaar
    knop_tekst = f"{icoon}{st.session_state.company_name}"
else:
    knop_tekst = "KUNDEPORTAL"


# =========================================================
# 3. CSS STYLING & HTML (Jouw eigen design)
# =========================================================
html_code = """<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Caveat:wght@700&display=swap');
html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; margin: 0; padding: 0; }
.stApp { background-color: #1e1e20 !important; }
.block-container { padding: 0 !important; max-width: 100% !important; margin-top: 90px; }

/* VERBERG STREAMLIT BRANDING (Inclusief de kat en het bootje!) */
[data-testid="collapsedControl"], [data-testid="stSidebar"], header[data-testid="stHeader"] { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
footer { display: none !important; }
div[class^="viewerBadge"] { display: none !important; }
#viewerBadge_container__1jcJt { display: none !important; }

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
.cta-btn-outline { background-color: transparent !important; color: #894b9d !important; padding: 10px 20px; border-radius: 50px; text-decoration: none !important; font-weight: 600; font-size: 13px; border: 2px solid #894b9d; max-width: 250px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;}

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

<div class="navbar">
<div class="nav-logo"><a href="/" target="_self"><img src="https://cloud-1de12d.becdn.net/media/original/964295c9ae8e693f8bb4d6b70862c2be/logo-website-top-png-1-.webp"></a></div>
<div class="nav-links"><a href="/" target="_self"><span>Hjem</span></a><span>Om oss</span><span>Tjenester</span><span>Galleri</span><span>Kontakt</span></div>
<div class="nav-cta"><a href="/Login" target="_self" class="cta-btn-outline">KUNDEPORTAL</a><a href="/" target="_self" class="cta-btn-purple">TA KONTAKT</a></div>
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

<div style="display: flex; gap: 15px;">
<a href="/Order" target="_self" class="cta-btn-purple" style="font-size: 16px; padding: 12px 30px;">BESTILL</a>
<a href="#" target="_self" class="cta-btn-purple" style="font-size: 16px; padding: 12px 30px;">TA KONTAKT</a>
</div>

<a href="#more" class="circle-btn">
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><polyline points="19 12 12 19 5 12"></polyline></svg>
</a>
</div>
<div class="hero-right"></div>
</div>"""

# =========================================================
# 4. TEKEN DE PAGINA MET DE JUISTE KNOP
# =========================================================
aangepaste_html = html_code.replace(">KUNDEPORTAL<", f">{knop_tekst}<")
st.markdown(aangepaste_html, unsafe_allow_html=True)
