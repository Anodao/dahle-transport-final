import streamlit as st
import time
from datetime import datetime
from supabase import create_client
import extra_streamlit_components as stx
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- PAGE CONFIG ---
st.set_page_config(page_title="Dahle Transport - New Order", layout="centered", initial_sidebar_state="collapsed")

# =========================================================
# 1. EMAIL FUNCTIE (OUTLOOK / OFFICE 365)
# =========================================================
def stuur_bevestigings_email(naar_email, order_data, order_id):
    try:
        # Haalt gegevens veilig uit .streamlit/secrets.toml
        zender_email = st.secrets["email"]["address"]
        zender_wachtwoord = st.secrets["email"]["password"]

        msg = MIMEMultipart()
        msg['From'] = f"Dahle Transport <{zender_email}>"
        msg['To'] = naar_email
        msg['Subject'] = f"Ordre Godkjent / Order Confirmation #{order_id}"

        # HTML Email Template
        html_body = f"""
        <html>
        <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #333; line-height: 1.6;">
            <div style="max-width: 600px; margin: 0 auto; border: 1px solid #eaeaea; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                <div style="background: linear-gradient(135deg, #b070c6 0%, #894b9d 100%); padding: 25px; text-align: center;">
                    <h2 style="color: white; margin: 0; font-size: 24px;">Dahle Transport</h2>
                </div>
                <div style="padding: 30px; background-color: #ffffff;">
                    <h3 style="color: #111; margin-top: 0;">Hei {order_data.get('contact_name', 'Kunde')}!</h3>
                    <p>Takk for din bestilling. Vi har mottatt din transportforespørsel og vil behandle den så snart som mulig.</p>
                    
                    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #894b9d; margin: 20px 0;">
                        <p style="margin: 0 0 10px 0;"><b>📦 Order ID:</b> #{order_id}</p>
                        <p style="margin: 0 0 10px 0;"><b>📍 Fra:</b> {order_data.get('pickup_city', 'Ikke angitt')} ({order_data.get('pickup_zip', '')})</p>
                        <p style="margin: 0;"><b>🏁 Til:</b> {order_data.get('delivery_city', 'Ikke angitt')} ({order_data.get('delivery_zip', '')})</p>
                    </div>
                    
                    <p>Du kan følge statusen på forsendelsen din i <a href="https://din-app-url.streamlit.app/Login" style="color: #894b9d; text-decoration: none; font-weight: bold;">Kundeportalen</a>.</p>
                    <p>Med vennlig hilsen,<br><b>Team Dahle Transport</b></p>
                    
                    <hr style="border: none; border-top: 1px solid #eee; margin: 25px 0;">
                    <p style="font-size: 11px; color: #888; text-align: center;">Dette er en automatisk e-post. Vennligst ikke svar på denne.</p>
                </div>
            </div>
        </body>
        </html>
        """
        msg.attach(MIMEText(html_body, 'html'))

        # Outlook SMTP Configuratie
        server = smtplib.SMTP('smtp.office365.com', 587)
        server.starttls()
        server.login(zender_email, zender_wachtwoord)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Fout bij versturen email: {e}")
        return False


# =========================================================
# 2. DIRECTE CSS INJECTIE 
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; margin: 0; padding: 0; }
.stApp { background-color: #111111 !important; }
.block-container { padding-top: 130px !important; max-width: 900px; }
.stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown li { color: #ffffff !important; }
[data-testid="collapsedControl"], [data-testid="stSidebar"], header[data-testid="stHeader"] { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
footer { display: none !important; }
div[class^="viewerBadge"] { display: none !important; }

/* NAVBAR CSS */
.navbar { position: fixed; top: 0; left: 0; width: 100%; height: 90px; background-color: #ffffff !important; z-index: 999; display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; padding: 0 40px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
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

/* STREAMLIT FORMULIER STYLING */
div[data-testid="stVerticalBlockBorderWrapper"] { background-color: #1e1e1e !important; border: 1px solid #333333 !important; border-radius: 12px !important; padding: 25px !important; }
div[data-baseweb="input"] > div, div[data-baseweb="textarea"], div[data-baseweb="select"] > div { background-color: #333333 !important; border: 1px solid #444444 !important; border-radius: 6px !important; }
div[data-baseweb="input"] input, div[data-baseweb="textarea"] textarea, div[data-baseweb="select"] span { color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; }
label[data-testid="stWidgetLabel"] p { color: #cccccc !important; font-weight: 600; font-size: 14px !important;}
div.stButton > button[kind="primary"] { background: linear-gradient(135deg, #b070c6 0%, #894b9d 100%) !important; color: #ffffff !important; border: none !important; border-radius: 6px !important; padding: 14px 28px !important; font-weight: 600 !important; font-size: 15px !important; width: 100% !important; box-shadow: 0 4px 14px 0 rgba(137, 75, 157, 0.4) !important; transition: all 0.3s ease !important; }
div.stButton > button[kind="primary"]:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 24px rgba(137, 75, 157, 0.6) !important; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. DATABASE & COOKIE MANAGER INIT
# =========================================================
cookie_manager = stx.CookieManager()

@st.cache_resource
def init_connection():
    return create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])

supabase = init_connection()

if 'user' not in st.session_state: st.session_state.user = None
if 'role' not in st.session_state: st.session_state.role = "guest"
if 'company_name' not in st.session_state: st.session_state.company_name = ""
if 'is_submitted' not in st.session_state: st.session_state.is_submitted = False

acc_token = cookie_manager.get('dahle_acc')
ref_token = cookie_manager.get('dahle_ref')

if st.session_state.get('user') is None and acc_token and ref_token:
    try: 
        st.session_state.user = supabase.auth.set_session(acc_token, ref_token).user
    except: pass

# Haal profiel data op als ingelogd
profile = {}
if st.session_state.get('user'):
    try:
        prof_res = supabase.table("profiles").select("*").eq("id", st.session_state.user.id).execute()
        if prof_res.data:
            profile = prof_res.data[0]
            st.session_state.company_name = profile.get("company_name", "")
            st.session_state.role = str(profile.get("roles", "customer")).strip().lower()
    except: pass

is_employee = st.session_state.get('role') in ['admin', 'employee']

# =========================================================
# 4. TAAL LOGICA & NAVBAR
# =========================================================
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

translations = {
    "no": { "nav_home": "Hjem", "nav_about": "Om oss", "nav_services": "Tjenester", "nav_gallery": "Galleri", "nav_contact": "Kontakt", "menu_title": "Sider ⌄", "menu_dash": "Performance Dashboard", "menu_plan": "Intern Planner", "nav_portal": "KUNDEPORTAL", "nav_contact_btn": "TA KONTAKT", "menu_order": "Ny bestilling", "menu_login": "Kundeportal", "order_title": "Ny Bestilling", "order_sub": "Fyll ut skjemaet nedenfor for å bestille transport.", "step1": "Firma & Kontakt", "step2": "Hentested", "step3": "Leveringssted", "step4": "Frakt & Tjenester", "comp": "Firmanavn *", "reg": "Org. nummer", "name": "Kontaktperson *", "phone": "Telefon *", "email": "E-post *", "addr": "Adresse *", "zip": "Postnummer *", "city": "By *", "type": "Type gods", "info": "Tilleggsinformasjon / Merknader", "submit": "BEKREFT & SEND BESTILLING", "success": "Takk! Bestillingen er mottatt og bekreftelse er sendt på e-post.", "new_order_btn": "Lag en ny bestilling", "err_fill": "Vennligst fyll ut alle obligatoriske felt (*)." },
    "en": { "nav_home": "Home", "nav_about": "About us", "nav_services": "Services", "nav_gallery": "Gallery", "nav_contact": "Contact", "menu_title": "Pages ⌄", "menu_dash": "Performance Dashboard", "menu_plan": "Internal Planner", "nav_portal": "CUSTOMER PORTAL", "nav_contact_btn": "CONTACT US", "menu_order": "New Order", "menu_login": "Customer Portal", "order_title": "New Order", "order_sub": "Fill out the form below to request transport.", "step1": "Company & Contact", "step2": "Pickup Location", "step3": "Delivery Destination", "step4": "Freight & Services", "comp": "Company Name *", "reg": "Registration No.", "name": "Contact Person *", "phone": "Phone *", "email": "Email *", "addr": "Address *", "zip": "Zip Code *", "city": "City *", "type": "Freight Type", "info": "Additional Info / Notes", "submit": "CONFIRM & SUBMIT ORDER", "success": "Thank you! Your order has been received and a confirmation email has been sent.", "new_order_btn": "Place another order", "err_fill": "Please fill in all mandatory fields (*)." }
}
t = translations.get(lang, translations["en"]) # Fallback to EN if language not mapped fully

if st.session_state.get('user') is not None and 'company_name' in st.session_state:
    icoon = "<svg style='width:16px; height:16px; margin-right:8px; vertical-align:-2px; fill:currentColor;' viewBox='0 0 640 512'><path d='M224 256A128 128 0 1 0 224 0a128 128 0 1 0 0 256zm-45.7 48C79.8 304 0 383.8 0 482.3C0 498.7 13.3 512 29.7 512H322.8c-3.1-8.8-3.7-18.4-1.4-27.8l15-60.1c2.8-11.3 8.6-21.5 16.8-29.7l40.3-40.3c-32.4-31.6-78-50.1-126.5-50.1H178.3zm212.8-38.1l-40.3 40.3c-15.9 15.9-27.2 35.8-32.5 57.2l-15 60.1c-1.3 5.3-.2 10.9 3.1 15.3s8.5 7.1 14 7.1H592c5.5 0 10.7-2.7 14-7.1s4.4-10 3.1-15.3l-15-60.1c-5.3-21.4-16.6-41.3-32.5-57.2l-40.3-40.3c-23.4-23.4-60.6-23.4-84 0zM456 432c-13.3 0-24-10.7-24-24s10.7-24 24-24s24 10.7 24 24s-10.7 24-24 24z'/></svg>"
    knop_tekst = f"{icoon}{st.session_state.company_name}"
else:
    knop_tekst = t['nav_portal']

dropdown_links = f'<a href="/Login?lang={lang}" target="_self">{t["menu_login"]}</a>'
if is_employee:
    dropdown_links += f'<a href="/Dashboard?lang={lang}" target="_self">{t["menu_dash"]}</a><a href="/Planner?lang={lang}" target="_self">{t["menu_plan"]}</a>'

html_navbar = f"""
<div class="navbar"><div class="nav-logo"><a href="/?lang={lang}" target="_self"><img src="https://cloud-1de12d.becdn.net/media/original/964295c9ae8e693f8bb4d6b70862c2be/logo-website-top-png-1-.webp"></a></div>
<div class="nav-links"><a href="/?lang={lang}" target="_self"><span>{t['nav_home']}</span></a><span>{t['nav_about']}</span><span>{t['nav_services']}</span><span>{t['nav_gallery']}</span><span>{t['nav_contact']}</span>
<div class="nav-text-dropdown"><button class="nav-text-dropbtn">{t['menu_title']}</button><div class="nav-text-dropdown-content">{dropdown_links}</div></div></div>
<div class="nav-cta"><div class="lang-dropdown"><button class="lang-dropbtn">{lang_displays.get(lang, 'Norsk')} ⌄</button><div class="lang-dropdown-content"><a href="?lang=en" target="_self">English</a><a href="?lang=no" target="_self">Norsk</a><a href="?lang=sv" target="_self">Svenska</a><a href="?lang=da" target="_self">Dansk</a></div></div>
<a href="/Login?lang={lang}" target="_self" class="cta-btn-outline">{knop_tekst}</a><a href="/?lang={lang}" target="_self" class="cta-btn-purple">{t['nav_contact_btn']}</a></div></div>
"""
st.markdown(html_navbar, unsafe_allow_html=True)


# =========================================================
# 5. ORDER FORMULIER LOGICA
# =========================================================
st.markdown(f"<h1 style='text-align: center; color: #b070c6;'>{t['order_title']}</h1>", unsafe_allow_html=True)

if st.session_state.is_submitted:
    st.success(t['success'])
    st.write("")
    if st.button(t['new_order_btn'], type="primary"):
        st.session_state.is_submitted = False
        st.rerun()
else:
    st.markdown(f"<p style='text-align: center; color: #aaaaaa; margin-bottom: 40px;'>{t['order_sub']}</p>", unsafe_allow_html=True)
    
    with st.container(border=True):
        st.markdown(f"<h3 style='margin-top:0;'>1. {t['step1']}</h3>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: 
            val_comp = profile.get("company_name", "") if profile else ""
            comp = st.text_input(t['comp'], value=val_comp)
        with c2: 
            reg = st.text_input(t['reg'])
        
        c3, c4, c5 = st.columns([2, 1.5, 2])
        with c3:
            val_contact = profile.get("contact_name", "") if profile else ""
            contact = st.text_input(t['name'], value=val_contact)
        with c4:
            val_phone = profile.get("phone", "") if profile else ""
            phone = st.text_input(t['phone'], value=val_phone)
        with c5:
            val_email = st.session_state.user.email if st.session_state.get('user') else ""
            email = st.text_input(t['email'], value=val_email)

    st.write("")

    col_addr1, col_addr2 = st.columns(2)
    with col_addr1:
        with st.container(border=True):
            st.markdown(f"<h3 style='margin-top:0;'>2. {t['step2']}</h3>", unsafe_allow_html=True)
            p_addr = st.text_input(t['addr'], value=profile.get("address", "") if profile else "", key="p_addr")
            c_pz, c_pc = st.columns([1, 2])
            with c_pz: p_zip = st.text_input(t['zip'], value=profile.get("zip_code", "") if profile else "", key="p_zip")
            with c_pc: p_city = st.text_input(t['city'], value=profile.get("city", "") if profile else "", key="p_city")

    with col_addr2:
        with st.container(border=True):
            st.markdown(f"<h3 style='margin-top:0;'>3. {t['step3']}</h3>", unsafe_allow_html=True)
            d_addr = st.text_input(t['addr'], value=profile.get("del_address", "") if profile else "", key="d_addr")
            c_dz, c_dc = st.columns([1, 2])
            with c_dz: d_zip = st.text_input(t['zip'], value=profile.get("del_zip", "") if profile else "", key="d_zip")
            with c_dc: d_city = st.text_input(t['city'], value=profile.get("del_city", "") if profile else "", key="d_city")

    st.write("")

    with st.container(border=True):
        st.markdown(f"<h3 style='margin-top:0;'>4. {t['step4']}</h3>", unsafe_allow_html=True)
        type_options = ["Cargo & Freight", "Container Transport", "Temperature Controlled", "Express Delivery"]
        f_type = st.selectbox(t['type'], type_options)
        f_info = st.text_area(t['info'], placeholder="E f.eks. '2x Pallet (70.0kg)' eller spesielle instruksjoner...")

    st.write("")
    
    # SUBMIT KNOP & DATABASE/EMAIL LOGICA
    if st.button(t['submit'], type="primary"):
        # Basis validatie
        if not all([comp, contact, phone, email, p_addr, p_zip, p_city, d_addr, d_zip, d_city]):
            st.error(t['err_fill'])
        else:
            with st.spinner("Lagrer bestilling..."):
                try:
                    # 1. Opbouwen van het database record
                    db_order = {
                        "company": comp,
                        "reg_no": reg,
                        "contact_name": contact,
                        "phone": phone,
                        "email": email,
                        "pickup_address": p_addr,
                        "pickup_zip": p_zip,
                        "pickup_city": p_city,
                        "delivery_address": d_addr,
                        "delivery_zip": d_zip,
                        "delivery_city": d_city,
                        "types": f_type,
                        "info": f_info,
                        "status": "New"
                    }
                    
                    # Koppel aan account indien ingelogd
                    if st.session_state.get('user'):
                        db_order["user_id"] = st.session_state.user.id

                    # 2. Opslaan in Supabase en ID terughalen
                    res = supabase.table("orders").insert(db_order).execute()
                    nieuw_order_id = res.data[0]['id'] if res.data else "Ukjent"

                    # 3. VERSTUUR DE BEVESTIGINGSMAIL VIA OUTLOOK
                    stuur_bevestigings_email(email, db_order, nieuw_order_id)

                    # 4. Succes weergave
                    st.balloons()
                    st.session_state.is_submitted = True
                    st.rerun()

                except Exception as e:
                    st.error(f"Det oppstod en feil: {e}")
