import streamlit as st
import time
import requests
import datetime
from supabase import create_client
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
        "menu_title": "Sider ⌄", "menu_dash": "Performance Dashboard", "menu_plan": "Intern Planner", "nav_portal": "KUNDEPORTAL", "nav_contact_btn": "TA KONTAKT",
        "menu_order": "Ny bestilling", "menu_login": "Kundeportal",
        "t_title": "Spesialforespørsel", 
        "t_sub": "Gjør en forespørsel, så kommer vi tilbake til deg så fort som mulig.",
        "lbl_name": "Navn / Firma *", "lbl_email": "E-postadresse *", "lbl_code": "Kode", "lbl_phone": "Telefonnummer",
        "lbl_from": "Fra (Hentested)", "lbl_to": "Til (Leveringssted)", 
        "lbl_start": "Startdato", "lbl_end": "Sluttdato",
        "lbl_specs": "Hva gjelder det? (Beskriv ditt behov) *",
        "btn_send": "Send Forespørsel", "msg_succ": "Takk! Forespørselen din er sendt. Vi tar kontakt snart.", "msg_err": "Vennligst fyll ut alle obligatoriske felt (*).",
        "email_greeting": "Hei", "email_req_title": "Din forespørsel:", "email_date": "Dato", "email_details": "Detaljer", 
        "email_footer": "Med vennlig hilsen,", "email_disclaimer": "Dette er en automatisk e-post. Vennligst ikke svar på denne.", "no_phone": "Ikke angitt"
    },
    "en": {
        "nav_home": "Home", "nav_about": "About us", "nav_services": "Services", "nav_gallery": "Gallery", "nav_contact": "Contact", 
        "menu_title": "Pages ⌄", "menu_dash": "Performance Dashboard", "menu_plan": "Internal Planner", "nav_portal": "CUSTOMER PORTAL", "nav_contact_btn": "CONTACT US",
        "menu_order": "New Order", "menu_login": "Customer Portal",
        "t_title": "Special Request", 
        "t_sub": "Make a request and we will get back to you as soon as possible.",
        "lbl_name": "Name / Company *", "lbl_email": "Email Address *", "lbl_code": "Code", "lbl_phone": "Phone Number",
        "lbl_from": "From (Pickup)", "lbl_to": "To (Delivery)", 
        "lbl_start": "Start Date", "lbl_end": "End Date",
        "lbl_specs": "What do you need? (Describe your request) *",
        "btn_send": "Send Request", "msg_succ": "Thank you! Your request has been sent. We will contact you shortly.", "msg_err": "Please fill in all mandatory fields (*).",
        "email_greeting": "Hi", "email_req_title": "Your request:", "email_date": "Date", "email_details": "Details", 
        "email_footer": "Kind regards,", "email_disclaimer": "This is an automated email. Please do not reply.", "no_phone": "Not provided"
    },
    "sv": {
        "nav_home": "Hem", "nav_about": "Om oss", "nav_services": "Tjänster", "nav_gallery": "Galleri", "nav_contact": "Kontakt", 
        "menu_title": "Sidor ⌄", "menu_dash": "Performance Dashboard", "menu_plan": "Intern Planner", "nav_portal": "KUNDPORTAL", "nav_contact_btn": "KONTAKTA OSS",
        "menu_order": "Ny beställning", "menu_login": "Kundportal",
        "t_title": "Specialförfrågan", 
        "t_sub": "Gör en förfrågan, så återkommer vi till dig så snart som möjligt.",
        "lbl_name": "Namn / Företag *", "lbl_email": "E-postadress *", "lbl_code": "Kod", "lbl_phone": "Telefonnummer",
        "lbl_from": "Från (Upphämtning)", "lbl_to": "Till (Leverans)", 
        "lbl_start": "Startdatum", "lbl_end": "Slutdatum",
        "lbl_specs": "Vad gäller det? (Beskriv ditt behov) *",
        "btn_send": "Skicka Förfrågan", "msg_succ": "Tack! Din förfrågan har skickats. Vi återkommer snart.", "msg_err": "Vänligen fyll i alla obligatoriska fält (*).",
        "email_greeting": "Hej", "email_req_title": "Din förfrågan:", "email_date": "Datum", "email_details": "Detaljer", 
        "email_footer": "Med vänliga hälsningar,", "email_disclaimer": "Detta är ett automatiskt e-postmeddelande. Vänligen svara inte.", "no_phone": "Ej angivet"
    },
    "da": {
        "nav_home": "Hjem", "nav_about": "Om os", "nav_services": "Tjenester", "nav_gallery": "Galleri", "nav_contact": "Kontakt", 
        "menu_title": "Sider ⌄", "menu_dash": "Performance Dashboard", "menu_plan": "Intern Planner", "nav_portal": "KUNDEPORTAL", "nav_contact_btn": "KONTAKT OS",
        "menu_order": "Ny bestilling", "menu_login": "Kundeportal",
        "t_title": "Specialforespørgsel", 
        "t_sub": "Lav en forespørgsel, så vender vi tilbage til dig hurtigst muligt.",
        "lbl_name": "Navn / Firma *", "lbl_email": "E-mailadresse *", "lbl_code": "Kode", "lbl_phone": "Telefonnummer",
        "lbl_from": "Fra (Afhentning)", "lbl_to": "Til (Levering)", 
        "lbl_start": "Startdato", "lbl_end": "Slutdato",
        "lbl_specs": "Hvad drejer det sig om? (Beskriv dit behov) *",
        "btn_send": "Send Forespørgsel", "msg_succ": "Tak! Din forespørgsel er sendt. Vi vender tilbage snarest.", "msg_err": "Udfyld venligst alle obligatoriske felter (*).",
        "email_greeting": "Hej", "email_req_title": "Din forespørgsel:", "email_date": "Dato", "email_details": "Detaljer", 
        "email_footer": "Med venlig hilsen,", "email_disclaimer": "Dette er en automatisk e-mail. Besvar venligst ikke denne.", "no_phone": "Ikke angivet"
    }
}
t = translations.get(lang, translations["en"])

# =========================================================
# 4. DATABASE & AUTH (TO PREVENT LOGGING OUT)
# =========================================================
def init_connection():
    return create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])

if 'supabase_client' not in st.session_state:
    try: st.session_state.supabase_client = init_connection()
    except Exception: pass
supabase = st.session_state.supabase_client

if 'user' not in st.session_state: st.session_state.user = None
if 'role' not in st.session_state: st.session_state.role = "guest"

acc_token = cookie_manager.get('dahle_acc')
ref_token = cookie_manager.get('dahle_ref')

# Check cookies to maintain session
if st.session_state.get('user') is None and acc_token and ref_token:
    try:
        session = supabase.auth.set_session(acc_token, ref_token)
        st.session_state.user = session.user
    except Exception: pass

# Get user details for Navbar and Pre-filling
if st.session_state.get('user'):
    try:
        prof_res = supabase.table("profiles").select("*").eq("id", st.session_state.user.id).execute()
        if prof_res.data:
            st.session_state.company_name = prof_res.data[0].get("company_name", "")
            st.session_state.role = str(prof_res.data[0].get("roles", "customer")).strip().lower()
    except Exception: st.session_state.role = "customer"

is_employee = st.session_state.get('role') in ['admin', 'employee']

# Pre-fill data if logged in
default_name = st.session_state.get('company_name', '')
default_email = st.session_state.user.email if st.session_state.get('user') else ''


# =========================================================
# 5. NAVBAR
# =========================================================
if st.session_state.get('user') is not None and 'company_name' in st.session_state:
    icoon = "<svg style='width:16px; height:16px; margin-right:8px; vertical-align:-2px; fill:currentColor;' viewBox='0 0 640 512'><path d='M224 256A128 128 0 1 0 224 0a128 128 0 1 0 0 256zm-45.7 48C79.8 304 0 383.8 0 482.3C0 498.7 13.3 512 29.7 512H322.8c-3.1-8.8-3.7-18.4-1.4-27.8l15-60.1c2.8-11.3 8.6-21.5 16.8-29.7l40.3-40.3c-32.4-31.6-78-50.1-126.5-50.1H178.3zm212.8-38.1l-40.3 40.3c-15.9 15.9-27.2 35.8-32.5 57.2l-15 60.1c-1.3 5.3-.2 10.9 3.1 15.3s8.5 7.1 14 7.1H592c5.5 0 10.7-2.7 14-7.1s4.4-10 3.1-15.3l-15-60.1c-5.3-21.4-16.6-41.3-32.5-57.2l-40.3-40.3c-23.4-23.4-60.6-23.4-84 0zM456 432c-13.3 0-24-10.7-24-24s10.7-24 24-24s24 10.7 24 24s-10.7 24-24 24z'/></svg>"
    knop_tekst = f"{icoon}{st.session_state.company_name}"
else:
    knop_tekst = t['nav_portal']

dropdown_links = f'<a href="/Login?lang={lang}" target="_self">{t["menu_login"]}</a><a href="/Order?lang={lang}" target="_self">{t["menu_order"]}</a>'
if is_employee: dropdown_links += f'<a href="/Dashboard?lang={lang}" target="_self">{t["menu_dash"]}</a><a href="/Planner?lang={lang}" target="_self">{t["menu_plan"]}</a>'

html_navbar = f"""
<div class="navbar"><div class="nav-logo"><a href="/?lang={lang}" target="_self"><img src="https://cloud-1de12d.becdn.net/media/original/964295c9ae8e693f8bb4d6b70862c2be/logo-website-top-png-1-.webp"></a></div>
<div class="nav-links"><a href="/?lang={lang}" target="_self"><span>{t['nav_home']}</span></a><span>{t['nav_about']}</span><span>{t['nav_services']}</span><span>{t['nav_gallery']}</span><span>{t['nav_contact']}</span>
<div class="nav-text-dropdown"><button class="nav-text-dropbtn">{t['menu_title']}</button><div class="nav-text-dropdown-content">{dropdown_links}</div></div></div>
<div class="nav-cta"><div class="lang-dropdown"><button class="lang-dropbtn">{current_lang_display} ⌄</button><div class="lang-dropdown-content"><a href="?lang=en" target="_self">English</a><a href="?lang=no" target="_self">Norsk</a><a href="?lang=sv" target="_self">Svenska</a><a href="?lang=da" target="_self">Dansk</a></div></div>
<a href="/Login?lang={lang}" target="_self" class="cta-btn-outline">{knop_tekst}</a><a href="/?lang={lang}" target="_self" class="cta-btn-purple">{t['nav_contact_btn']}</a></div></div>
"""
st.markdown(html_navbar, unsafe_allow_html=True)

# =========================================================
# 6. PAGINA INHOUD
# =========================================================
st.markdown(f"<h2 style='text-align: center; color: #b070c6;'>{t['t_title']}</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #aaaaaa; margin-bottom: 30px;'>{t['t_sub']}</p>", unsafe_allow_html=True)

with st.container(border=True):
    # RIJ 1
    c1, c2, c3, c4 = st.columns([3, 3, 1.5, 3])
    with c1: 
        req_name = st.text_input(t['lbl_name'], value=default_name)
    with c2: 
        req_email = st.text_input(t['lbl_email'], value=default_email)
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
                
                # Combineer telefoonnummer. Als er geen nummer is ingevuld, pakt hij de vertaling "Ikke angitt" / "Not provided"
                full_phone = f"{req_phone_code} {req_phone_num.strip()}" if req_phone_num.strip() else t['no_phone']
                
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
                
                # Volledig Vertaalde HTML e-mail voor de klant
                customer_html = f"""
                <html>
                <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #333; line-height: 1.6;">
                    <div style="max-width: 600px; margin: 0 auto; border: 1px solid #eaeaea; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                        <div style="background: linear-gradient(135deg, #b070c6 0%, #894b9d 100%); padding: 25px; text-align: center;">
                            <h2 style="color: white; margin: 0; font-size: 24px;">Dahle Transport</h2>
                        </div>
                        <div style="padding: 30px; background-color: #ffffff;">
                            <h3 style="color: #111; margin-top: 0;">{t['email_greeting']} {req_name}!</h3>
                            <p>{t['msg_succ']}</p>
                            
                            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; border-left: 4px solid #894b9d; margin: 20px 0;">
                                <h4 style="margin-top: 0; margin-bottom: 15px; color: #894b9d;">{t['email_req_title']}</h4>
                                <p style="margin: 0 0 10px 0;"><b>📞 {t['lbl_phone']}:</b> {full_phone}</p>
                                <p style="margin: 0 0 10px 0;"><b>📍 {t['lbl_from']}:</b> {req_from}</p>
                                <p style="margin: 0 0 10px 0;"><b>🏁 {t['lbl_to']}:</b> {req_to}</p>
                                <p style="margin: 0 0 10px 0;"><b>📅 {t['email_date']}:</b> {req_start} - {req_end}</p>
                                <p style="margin: 0;"><b>📝 {t['email_details']}:</b><br>{req_specs}</p>
                            </div>
                            
                            <p>{t['email_footer']}<br><b>Team Dahle Transport</b></p>
                            
                            <hr style="border: none; border-top: 1px solid #eee; margin: 25px 0;">
                            <p style="font-size: 11px; color: #888; text-align: center;">{t['email_disclaimer']}</p>
                        </div>
                    </div>
                </body>
                </html>
                """
                
                requests.post("https://api.resend.com/emails", json={
                    "from": "Dahle Transport <info@dahletransport.nl>",
                    "to": [req_email],
                    "subject": subject_t.get(lang, subject_t["en"]),
                    "html": customer_html
                }, headers=headers)
                
                st.success(t['msg_succ'])
            except Exception as e:
                st.error(f"Fout bij verzenden: {str(e)}")
        else:
            st.warning(t['msg_err'])
