import streamlit as st
import time
import requests
import datetime
import extra_streamlit_components as stx

# --- PAGE CONFIG ---
st.set_page_config(page_title="Dahle Transport - Special Request", layout="centered", initial_sidebar_state="collapsed")

# =========================================================
# 1. DIRECTE CSS INJECTIE 
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
* { font-family: 'Montserrat', sans-serif; }

/* VERBERG STREAMLIT BRANDING */
[data-testid="collapsedControl"], [data-testid="stSidebar"], header[data-testid="stHeader"], footer, [data-testid="stToolbar"] { display: none !important; }

/* HIER IS DE BOX BREDER GEMAAKT (950px in plaats van 800px) */
.block-container { padding-top: 110px; max-width: 950px; }

/* NAVBAR CSS */
.navbar { position: fixed; top: 0; left: 0; width: 100%; height: 90px; background-color: white; z-index: 999; border-bottom: 1px solid #eaeaea; display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; padding: 0 40px; box-shadow: 0 2px 10px rgba(0,0,0,0.03); }
.nav-logo { display: flex; justify-content: flex-start; margin-left: 20px; }
.nav-logo a { display: inline-block; height: 48px; text-decoration: none; cursor: pointer; }
.nav-logo img { height: 100%; width: auto; display: block; transition: transform 0.2s ease-in-out; }
.nav-logo a:hover img { transform: scale(1.05); } 
.nav-links { display: flex; gap: 28px; font-size: 15px; font-weight: 600; justify-content: center; align-items: center;}
.nav-links a, .nav-links span { text-decoration: none; color: #111111 !important; cursor: pointer; transition: color 0.2s;}
.nav-links span:hover { color: #894b9d !important; }
.nav-text-dropdown { position: relative; display: inline-block; cursor: pointer; padding-bottom: 20px; margin-bottom: -20px; }
.nav-text-dropbtn { background: transparent; border: none; font-size: 15px; font-weight: 600; color: #111111 !important; cursor: pointer; padding: 0; font-family: inherit; transition: color 0.2s; display: flex; align-items: center; gap: 4px; }
.nav-text-dropdown:hover .nav-text-dropbtn { color: #894b9d !important; }
.nav-text-dropdown::after { content: ''; position: absolute; top: 100%; left: 0; width: 100%; height: 30px; background: transparent; display: none; }
.nav-text-dropdown:hover::after { display: block; }
.nav-text-dropdown-content { display: none; position: absolute; top: calc(100% + 10px); left: 50%; transform: translateX(-50%); background-color: #ffffff; min-width: 180px; box-shadow: 0px 8px 24px rgba(0,0,0,0.12); border-radius: 12px; border: 1px solid #eaeaea; z-index: 1000; overflow: hidden; }
.nav-text-dropdown-content a { color: #111111 !important; padding: 12px 16px; text-decoration: none; display: block; font-size: 14px; font-weight: 500; text-align: left; transition: background-color 0.2s; border-bottom: none !important; }
.nav-text-dropdown-content a:hover { background-color: #f4e9f7; color: #894b9d !important; }
.nav-text-dropdown:hover .nav-text-dropdown-content { display: block; }
.nav-cta { display: flex; justify-content: flex-end; gap: 15px; align-items: center; }
.cta-btn-purple { background-color: #894b9d !important; color: white !important; padding: 10px 24px; border-radius: 50px; text-decoration: none !important; font-weight: 600; font-size: 13px; transition: background-color 0.2s; white-space: nowrap;}
.cta-btn-purple:hover { background-color: #723e83 !important; }
.cta-btn-outline { background-color: transparent !important; color: #894b9d !important; padding: 10px 20px; border-radius: 50px; text-decoration: none !important; font-weight: 600; font-size: 13px; border: 2px solid #894b9d; max-width: 250px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;}
.cta-btn-outline:hover { background-color: #f4e9f7 !important; }
.lang-dropdown { position: relative; display: inline-block; margin-right: 10px; }
.lang-dropbtn { background-color: #f8f9fa; color: #111; font-weight: 600; font-size: 13px; border: 1px solid #eaeaea; border-radius: 20px; padding: 8px 16px; cursor: pointer; display: flex; align-items: center; gap: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.03); transition: all 0.2s ease; }
.lang-dropbtn:hover { background-color: #eaeaea; }
.lang-dropdown::after { content: ''; position: absolute; top: 100%; right: 0; width: 140px; height: 30px; background: transparent; display: none; z-index: 999; }
.lang-dropdown:hover::after { display: block; }
.lang-dropdown-content { display: none; position: absolute; background-color: #ffffff; min-width: 140px; box-shadow: 0px 8px 24px rgba(0,0,0,0.12); border-radius: 12px; border: 1px solid #eaeaea; z-index: 1000; top: calc(100% + 10px); right: 0; margin-top: 0; overflow: hidden; }
.lang-dropdown-content a { color: #111 !important; padding: 12px 16px; text-decoration: none; display: flex; align-items: center; gap: 10px; font-size: 14px; font-weight: 500; transition: background-color 0.2s; }
.lang-dropdown-content a:hover { background-color: #f4e9f7; color: #894b9d !important; }
.lang-dropdown:hover .lang-dropdown-content { display: block; }

/* FORMULIER STYLING */
div.stButton > button[kind="primary"] { background: linear-gradient(135deg, #b070c6 0%, #894b9d 100%) !important; color: #ffffff !important; border: 2px solid transparent !important; border-radius: 6px !important; padding: 14px 28px !important; font-weight: 600 !important; font-size: 15px !important; box-shadow: 0 4px 14px 0 rgba(137, 75, 157, 0.4) !important; transition: all 0.3s ease !important; width: 100% !important; margin-top: 10px !important;}
div.stButton > button[kind="primary"]:hover { background: #ffffff !important; color: #894b9d !important; border: 2px solid #894b9d !important; transform: translateY(-2px) !important; box-shadow: 0 8px 24px rgba(137, 75, 157, 0.6) !important; }

/* INPUTS & SELECTBOX DONKER MAKEN */
div[data-baseweb="input"] > div, div[data-baseweb="textarea"], div[data-baseweb="select"] > div { background-color: #262626 !important; border-radius: 8px !important; border: 1px solid #444 !important; }
div[data-baseweb="input"] input, div[data-baseweb="textarea"] textarea, div[data-baseweb="select"] div { color: white !important; }
label { color: #ccc !important; font-weight: 600; font-size: 14px !important;}
div[data-testid="stVerticalBlockBorderWrapper"] { background-color: #1a1a1c !important; border: 1px solid #333 !important; border-radius: 12px !important; padding: 25px !important; box-shadow: 0 10px 30px rgba(0,0,0,0.3) !important;}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 2. INIT COOKIE MANAGER & TAAL 
# =========================================================
cookie_manager = stx.CookieManager()
saved_lang = cookie_manager.get('dahle_lang')

if "lang" in st.query_params:
    url_lang = st.query_params["lang"]
    if url_lang in ["no", "en", "sv", "da"]:
        if url_lang != saved_lang: cookie_manager.set("dahle_lang", url_lang, key="set_lang_safe")
        st.session_state.language = url_lang
elif saved_lang and saved_lang in ["no", "en", "sv", "da"]:
    st.session_state.language = saved_lang
elif 'language' not in st.session_state:
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
        "menu_title": "Sider ⌄", "menu_login": "Kundeportal", "menu_order": "Ny bestilling", "nav_portal": "KUNDEPORTAL", "nav_contact_btn": "TA KONTAKT",
        "t_title": "Spesialforespørsel & Utleie", 
        "t_sub": "Gjør en forespørsel, så kommer vi tilbake til deg så fort som mulig.",
        "lbl_name": "Navn / Firma *", "lbl_email": "E-postadresse *", "lbl_code": "Kode", "lbl_phone": "Telefonnummer",
        "lbl_from": "Fra (Hentested)", "lbl_to": "Til (Leveringssted)", 
        "lbl_start": "Startdato", "lbl_end": "Sluttdato",
        "lbl_specs": "Hva gjelder det? (F.eks. leie av varebil i 3 dager, flytting, etc.) *",
        "btn_send": "Send Forespørsel", "msg_succ": "Takk! Forespørselen din er sendt. Vi tar kontakt snart.", "msg_err": "Vennligst fyll out alle obligatoriske felt (*)."
    },
    "en": {
        "nav_home": "Home", "nav_about": "About us", "nav_services": "Services", "nav_gallery": "Gallery", "nav_contact": "Contact", 
        "menu_title": "Pages ⌄", "menu_login": "Customer Portal", "menu_order": "New Order", "nav_portal": "CUSTOMER PORTAL", "nav_contact_btn": "CONTACT US",
        "t_title": "Special Request & Rentals", 
        "t_sub": "Make a request and we will get back to you as soon as possible.",
        "lbl_name": "Name / Company *", "lbl_email": "Email Address *", "lbl_code": "Code", "lbl_phone": "Phone Number",
        "lbl_from": "From (Pickup)", "lbl_to": "To (Delivery)", 
        "lbl_start": "Start Date", "lbl_end": "End Date",
        "lbl_specs": "What do you need? (Describe your request) *",
        "btn_send": "Send Request", "msg_succ": "Thank you! Your request has been sent. We will contact you shortly.", "msg_err": "Please fill in all mandatory fields (*)."
    },
    "sv": {
        "nav_home": "Hem", "nav_about": "Om oss", "nav_services": "Tjänster", "nav_gallery": "Galleri", "nav_contact": "Kontakt", 
        "menu_title": "Sidor ⌄", "menu_login": "Kundportal", "menu_order": "Ny beställning", "nav_portal": "KUNDPORTAL", "nav_contact_btn": "KONTAKTA OSS",
        "t_title": "Specialförfrågan & Uthyrning", 
        "t_sub": "Gör en förfrågan, så återkommer vi till dig så snart som möjligt.",
        "lbl_name": "Namn / Företag *", "lbl_email": "E-postadress *", "lbl_code": "Kod", "lbl_phone": "Telefonnummer",
        "lbl_from": "Från (Upphämtning)", "lbl_to": "Till (Leverans)", 
        "lbl_start": "Startdatum", "lbl_end": "Slutdatum",
        "lbl_specs": "Vad gäller det? (Beskriv ditt behov) *",
        "btn_send": "Skicka Förfrågan", "msg_succ": "Tack! Din förfrågan har skickats. Vi återkommer snart.", "msg_err": "Vänligen fyll i alla obligatoriska fält (*)."
    },
    "da": {
        "nav_home": "Hjem", "nav_about": "Om os", "nav_services": "Tjenester", "nav_gallery": "Galleri", "nav_contact": "Kontakt", 
        "menu_title": "Sider ⌄", "menu_login": "Kundeportal", "menu_order": "Ny bestilling", "nav_portal": "KUNDEPORTAL", "nav_contact_btn": "KONTAKT OS",
        "t_title": "Specialforespørgsel & Udlejning", 
        "t_sub": "Lav en forespørgsel, så vender vi tilbage til dig hurtigst muligt.",
        "lbl_name": "Navn / Firma *", "lbl_email": "E-mailadresse *", "lbl_code": "Kode", "lbl_phone": "Telefonnummer",
        "lbl_from": "Fra (Afhentning)", "lbl_to": "Til (Levering)", 
        "lbl_start": "Startdato", "lbl_end": "Slutdato",
        "lbl_specs": "Hvad drejer det sig om? (Beskriv dit behov) *",
        "btn_send": "Send Forespørgsel", "msg_succ": "Tak! Din forespørgsel er sendt. Vi vender tilbage snarest.", "msg_err": "Udfyld venligst alle obligatoriske felter (*)."
    }
}
t = translations.get(lang, translations["en"])

# =========================================================
# 4. NAVBAR
# =========================================================
dropdown_links = f'<a href="/Login?lang={lang}" target="_self">{t["menu_login"]}</a><a href="/Order?lang={lang}" target="_self">{t["menu_order"]}</a>'
html_navbar = f"""
<div class="navbar"><div class="nav-logo"><a href="/?lang={lang}" target="_self"><img src="https://cloud-1de12d.becdn.net/media/original/964295c9ae8e693f8bb4d6b70862c2be/logo-website-top-png-1-.webp"></a></div>
<div class="nav-links"><a href="/?lang={lang}" target="_self"><span>{t['nav_home']}</span></a><span>{t['nav_about']}</span><span>{t['nav_services']}</span><span>{t['nav_gallery']}</span><span>{t['nav_contact']}</span>
<div class="nav-text-dropdown"><button class="nav-text-dropbtn">{t['menu_title']}</button><div class="nav-text-dropdown-content">{dropdown_links}</div></div></div>
<div class="nav-cta"><div class="lang-dropdown"><button class="lang-dropbtn">{current_lang_display} ⌄</button><div class="lang-dropdown-content"><a href="?lang=en" target="_self">English</a><a href="?lang=no" target="_self">Norsk</a><a href="?lang=sv" target="_self">Svenska</a><a href="?lang=da" target="_self">Dansk</a></div></div>
<a href="/Login?lang={lang}" target="_self" class="cta-btn-outline">{t['nav_portal']}</a><a href="/?lang={lang}" target="_self" class="cta-btn-purple">{t['nav_contact_btn']}</a></div></div>
"""
st.markdown(html_navbar, unsafe_allow_html=True)

# =========================================================
# 5. PAGINA INHOUD
# =========================================================
st.markdown(f"<h2 style='text-align: center; color: #b070c6;'>{t['t_title']}</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #aaaaaa; margin-bottom: 30px;'>{t['t_sub']}</p>", unsafe_allow_html=True)

with st.container(border=True):
    # RIJ 1: De kolomverhoudingen zijn geüpdatet zodat 'Code' meer ademruimte heeft.
    c1, c2, c3, c4 = st.columns([3, 3, 1.5, 3])
    with c1: 
        req_name = st.text_input(t['lbl_name'])
    with c2: 
        req_email = st.text_input(t['lbl_email'])
    with c3: 
        req_phone_code = st.selectbox(t['lbl_code'], ["+47", "+46", "+45", "+31", "+44"])
    with c4: 
        req_phone_num = st.text_input(t['lbl_phone'])
    
    st.write("")
    
    # RIJ 2: Locaties
    c5, c6 = st.columns(2)
    with c5: 
        req_from = st.text_input(t['lbl_from'])
    with c6: 
        req_to = st.text_input(t['lbl_to'])
    
    st.write("")
    
    # RIJ 3: Kalender
    c7, c8 = st.columns(2)
    with c7: 
        req_start = st.date_input(t['lbl_start'], value=None)
    with c8: 
        req_end = st.date_input(t['lbl_end'], value=None)
    
    st.write("")
    
    # RIJ 4: Tekstvak
    req_specs = st.text_area(t['lbl_specs'], height=120)
    
    st.write("")
    if st.button(t['btn_send'], type="primary", use_container_width=True):
        if req_name and req_email and req_specs:
            try:
                api_key = st.secrets["resend"]["api_key"]
                
                # Combineer telefoonnummer
                full_phone = f"{req_phone_code} {req_phone_num.strip()}" if req_phone_num.strip() else "Ikke angitt"
                
                # E-mail naar Dahle Transport (Jullie ontvangen deze)
                internal_html = f"""
                <h3>Ny Spesialforespørsel / Leieforespørsel!</h3>
                <p><b>Navn/Firma:</b> {req_name}</p>
                <p><b>E-post:</b> {req_email}</p>
                <p><b>Telefon:</b> {full_phone}</p>
                <p><b>Rute / Sted:</b> Fra {req_from} til {req_to}</p>
                <p><b>Periode:</b> {req_start} - {req_end}</p>
                <p><b>Spesifikasjoner / Behov:</b><br>{req_specs}</p>
                """
                
                headers = { "Authorization": f"Bearer {api_key}", "Content-Type": "application/json" }
                
                # Stuur mail naar kantoor
                requests.post("https://api.resend.com/emails", json={
                    "from": "Dahle System <info@dahletransport.nl>", 
                    "to": ["info@dahletransport.nl"], # Verander dit naar jullie eigen inbox!
                    "subject": f"Ny forespørsel: {req_name}",
                    "html": internal_html
                }, headers=headers)
                
                # Bevestiging naar de klant
                subject_t = {
                    "no": "Vi har mottatt din forespørsel",
                    "en": "We received your request",
                    "sv": "Vi har tagit emot din förfrågan",
                    "da": "Vi har modtaget din forespørgsel"
                }
                
                customer_html = f"""
                <p>Hei {req_name},</p>
                <p>{t['msg_succ']}</p>
                <p>Mvh,<br>Dahle Transport</p>
                """
                
                requests.post("https://api.resend.com/emails", json={
                    "from": "Dahle Transport <info@dahletransport.nl>",
                    "to": [req_email],
                    "subject": subject_t.get(lang, subject_t["en"]),
                    "html": customer_html
                }, headers=headers)
                
                st.success(t['msg_succ'])
                st.balloons()
            except Exception as e:
                st.error(f"Fout bij verzenden: {str(e)}")
        else:
            st.warning(t['msg_err'])
