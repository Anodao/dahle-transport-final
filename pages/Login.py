import streamlit as st
import time
from datetime import datetime, timedelta
from supabase import create_client
import extra_streamlit_components as stx

# --- PAGE CONFIG ---
st.set_page_config(page_title="Dahle Transport - Customer Portal", layout="centered", initial_sidebar_state="collapsed")

# =========================================================
# 1. DIRECTE CSS INJECTIE 
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; margin: 0; padding: 0; }
.stApp { background-color: #111111 !important; }
.block-container { padding-top: 130px !important; max-width: 900px; }
.stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown li { color: #ffffff !important; }
div[data-testid="stMetricValue"], div[data-testid="stMetricLabel"] { color: #ffffff !important; }

/* VERBERG STREAMLIT BRANDING VOLLEDIG */
[data-testid="collapsedControl"], [data-testid="stSidebar"], header[data-testid="stHeader"] { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
footer { display: none !important; }
div[class^="viewerBadge"] { display: none !important; }

/* NAVBAR CSS */
.navbar { position: fixed; top: 0; left: 0; width: 100%; height: 90px; background-color: #ffffff !important; z-index: 999; display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; padding: 0 40px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
.nav-logo { display: flex; justify-content: flex-start; margin-left: 20px; }
.nav-logo a { display: inline-block; height: 48px; text-decoration: none; cursor: pointer; }
.nav-logo img { height: 100%; width: auto; display: block; transition: transform 0.2s ease-in-out; }
.nav-logo a:hover img { transform: scale(1.05); } 

/* DE LINK TEKSTEN IN HET MIDDEN */
.nav-links { display: flex; gap: 28px; font-size: 15px; font-weight: 600; justify-content: center; align-items: center;}
.nav-links a, .nav-links span { text-decoration: none; color: #111111 !important; cursor: pointer; transition: color 0.2s;}
.nav-links span:hover { color: #894b9d !important; }

/* HET TEKST-DROPDOWN MENU NAAST 'CONTACT' */
.nav-text-dropdown { position: relative; display: inline-block; cursor: pointer; padding-bottom: 20px; margin-bottom: -20px; }
.nav-text-dropbtn { background: transparent; border: none; font-size: 15px; font-weight: 600; color: #111111 !important; cursor: pointer; padding: 0; font-family: inherit; transition: color 0.2s; display: flex; align-items: center; gap: 4px; }
.nav-text-dropdown:hover .nav-text-dropbtn { color: #894b9d !important; }
.nav-text-dropdown::after { content: ''; position: absolute; top: 100%; left: 0; width: 100%; height: 30px; background: transparent; display: none; }
.nav-text-dropdown:hover::after { display: block; }
.nav-text-dropdown-content { display: none; position: absolute; top: calc(100% + 10px); left: 50%; transform: translateX(-50%); background-color: #ffffff; min-width: 180px; box-shadow: 0px 8px 24px rgba(0,0,0,0.12); border-radius: 12px; border: 1px solid #eaeaea; z-index: 1000; overflow: hidden; }
.nav-text-dropdown-content a { color: #111111 !important; padding: 12px 16px; text-decoration: none; display: block; font-size: 14px; font-weight: 500; text-align: left; transition: background-color 0.2s; border-bottom: none !important; }
.nav-text-dropdown-content a:hover { background-color: #f4e9f7; color: #894b9d !important; }
.nav-text-dropdown:hover .nav-text-dropdown-content { display: block; }

/* DE KNOPPEN RECHTS */
.nav-cta { display: flex; justify-content: flex-end; gap: 15px; align-items: center; }
.cta-btn-purple { background-color: #894b9d !important; color: white !important; padding: 10px 24px; border-radius: 50px; text-decoration: none !important; font-weight: 600; font-size: 13px; transition: background-color 0.2s; white-space: nowrap;}
.cta-btn-purple:hover { background-color: #723e83 !important; }
.cta-btn-outline { background-color: transparent !important; color: #894b9d !important; padding: 10px 20px; border-radius: 50px; text-decoration: none !important; font-weight: 600; font-size: 13px; border: 2px solid #894b9d; max-width: 250px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;}
.cta-btn-outline:hover { background-color: #f4e9f7 !important; }

/* TAAL DROPDOWN */
.lang-dropdown { position: relative; display: inline-block; margin-right: 10px; }
.lang-dropbtn { background-color: #f8f9fa; color: #111; font-weight: 600; font-size: 13px; border: 1px solid #eaeaea; border-radius: 20px; padding: 8px 16px; cursor: pointer; display: flex; align-items: center; gap: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.03); transition: all 0.2s ease; }
.lang-dropbtn:hover { background-color: #eaeaea; }
.lang-dropdown::after { content: ''; position: absolute; top: 100%; right: 0; width: 140px; height: 30px; background: transparent; display: none; z-index: 999; }
.lang-dropdown:hover::after { display: block; }
.lang-dropdown-content { display: none; position: absolute; background-color: #ffffff; min-width: 140px; box-shadow: 0px 8px 24px rgba(0,0,0,0.12); border-radius: 12px; border: 1px solid #eaeaea; z-index: 1000; top: calc(100% + 10px); right: 0; margin-top: 0; overflow: hidden; }
.lang-dropdown-content a { color: #111 !important; padding: 12px 16px; text-decoration: none; display: flex; align-items: center; gap: 10px; font-size: 14px; font-weight: 500; transition: background-color 0.2s; }
.lang-dropdown-content a:hover { background-color: #f4e9f7; color: #894b9d !important; }
.lang-dropdown:hover .lang-dropdown-content { display: block; }

/* STREAMLIT ELEMENTEN STYLING */
div[data-testid="stVerticalBlockBorderWrapper"] { background-color: #1e1e1e !important; border: 1px solid #333333 !important; border-radius: 12px !important; padding: 20px !important; }
div[data-baseweb="input"] > div, div[data-baseweb="textarea"] { background-color: #333333 !important; border: 1px solid #444444 !important; border-radius: 6px !important; }
div[data-baseweb="input"] input, div[data-baseweb="textarea"] textarea { color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; }
label[data-testid="stWidgetLabel"] p { color: #cccccc !important; font-weight: 600; font-size: 14px !important;}
div.stButton > button[kind="primary"] { background: linear-gradient(135deg, #b070c6 0%, #894b9d 100%) !important; color: #ffffff !important; border: none !important; border-radius: 6px !important; padding: 14px 28px !important; font-weight: 600 !important; font-size: 15px !important; width: 100% !important; box-shadow: 0 4px 14px 0 rgba(137, 75, 157, 0.4) !important; transition: all 0.3s ease !important; }
div.stButton > button[kind="primary"]:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 24px rgba(137, 75, 157, 0.6) !important; }
div.stButton > button[kind="secondary"] { background: transparent !important; color: #e0c2ed !important; border: 2px solid #894b9d !important; border-radius: 6px !important; padding: 14px 28px !important; font-weight: 600 !important; font-size: 15px !important; width: 100% !important; transition: all 0.3s ease !important; }
div.stButton > button[kind="secondary"]:hover { background: #894b9d !important; color: white !important; transform: translateY(-2px) !important;}
div[data-testid="stExpander"] { background-color: #262626 !important; border: 1px solid #444 !important; border-radius: 8px !important; }
div[data-testid="stExpander"] p { color: #ffffff !important; }
div[data-testid="stExpanderDetails"] { background-color: #1e1e1e !important; border-top: 1px solid #444 !important; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 2. INIT COOKIE MANAGER & WACHTRUIMTE 
# =========================================================
cookie_manager = stx.CookieManager()

if 'cookie_retry' not in st.session_state:
    st.session_state.cookie_retry = True
    loading = st.empty()
    loading.markdown("<h3 style='text-align: center; color: #888; margin-top: 150px;'>Verifying credentials... ⏳</h3>", unsafe_allow_html=True)
    time.sleep(0.3) 
    loading.empty()
    st.rerun() 

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
        "portal_title": "Kundeportal", "portal_sub": "Logg inn for å administrere dine sendinger og detaljer.",
        "tab_login": "Logg inn", "tab_reg": "Opprett konto",
        "lbl_email": "E-postadresse", "lbl_pass": "Passord", "btn_login": "Logg inn",
        "msg_logging_in": "Logger inn...", "msg_login_succ": "Vellykket innlogging! Videresender...", "msg_login_fail": "Feil e-post eller passord.", "msg_fill_both": "Vennligst fyll ut begge feltene.",
        "lbl_comp": "Firmanavn *", "lbl_fn": "Fornavn *", "lbl_ln": "Etternavn *", "lbl_phone": "Telefonnummer", "lbl_email_reg": "E-post (Dette blir din innlogging) *", "lbl_pass_reg": "Velg passord *", "btn_reg": "Opprett konto",
        "msg_creating": "Oppretter konto...", "msg_reg_succ": "Konto opprettet! Du kan nå logge inn via 'Logg inn'-fanen.", "msg_reg_fail": "En feil oppstod.", "msg_fill_req": "Vennligst fyll ut alle obligatoriske felt (*).",
        "welcome": "Velkommen tilbake", "logged_in_as": "Logget inn som", "btn_logout": "Logg ut",
        "hist_title": "Din sendingshistorik", "tot_ship": "Totale sendinger", "pend_appr": "Venter på godkjenning", "processed": "Behandlet",
        "tab_myship": "Mine sendinger", "tab_neworder": "Ny bestilling", "tab_prof": "Profilinnstillinger",
        "no_orders": "Du har ikke lagt inn noen bestillinger ennå. Gå til 'Ny bestilling' for å starte!",
        "status": "Status", "pickup": "Hentested", "delivery": "Leveringssted", "addr": "Adresse", "zip": "Postnr", "city": "By",
        "track_trace": "Sporing (Track & Trace)", "track_pending": "Venter på tildeling...",
        "services": "Forespurte tjenester", "add_info": "Tilleggsinfo", "btn_cancel": "Avbryt denne bestillingen",
        "prof_title": "Administrer profilen din", "prof_sub": "Oppdater firma- og kontaktinformasjon her.",
        "gen_info": "Generell info", "cont_pers": "Kontaktperson", "email_id": "E-postadresse (Innloggings-ID)",
        "bill_t": "Faktureringsdetaljer", "bill_same": "Bruk firma og adresse fra Generell Info", "b_comp": "Fakturamottaker (Firma)", "b_em": "Faktura E-post", "r_name": "Kontaktperson (Navn/Firma)", "r_ph": "Telefon",
        "def_pickup": "Standard hentested", "def_del": "Standard leveringssted", "speed_up": "Vi bruker dette for å gjøre bestillingen raskere.",
        "street": "Gateadresse", "btn_save": "Lagre endringer", "msg_saving": "Oppdaterer profil...", "msg_save_succ": "Profil oppdatert!", "msg_save_fail": "Klarte ikke å oppdatere profil:",
        "msg_cancel_succ": "Bestillingen ble kansellert.",
        "msg_cancel_fail": "Kunne ikke kansellere bestillingen.",
        "msg_planner": "Melding fra Dahle Transport:",
        "btn_seen": "Marker som lest (Fjern varsel)",
        "new_upd": "✨ NY OPPDATERING"
    },
    "en": {
        "nav_home": "Home", "nav_about": "About us", "nav_services": "Services", "nav_gallery": "Gallery", "nav_contact": "Contact", 
        "menu_title": "Pages ⌄", "menu_dash": "Performance Dashboard", "menu_plan": "Internal Planner", "nav_portal": "CUSTOMER PORTAL", "nav_contact_btn": "CONTACT US",
        "menu_order": "New Order", "menu_login": "Customer Portal",
        "portal_title": "Customer Portal", "portal_sub": "Log in to manage your shipments and details.",
        "tab_login": "Log In", "tab_reg": "Create Account",
        "lbl_email": "Email Address", "lbl_pass": "Password", "btn_login": "Log In",
        "msg_logging_in": "Logging in...", "msg_login_succ": "Successfully logged in! Redirecting...", "msg_login_fail": "Incorrect email or password.", "msg_fill_both": "Please fill in both fields.",
        "lbl_comp": "Company Name *", "lbl_fn": "First Name *", "lbl_ln": "Last Name *", "lbl_phone": "Phone Number", "lbl_email_reg": "Email Address (This will be your login) *", "lbl_pass_reg": "Choose a Password *", "btn_reg": "Create Account",
        "msg_creating": "Creating account...", "msg_reg_succ": "Account created successfully! You can now log in via the 'Log In' tab.", "msg_reg_fail": "An error occurred.", "msg_fill_req": "Please fill in all mandatory fields (*).",
        "welcome": "Welcome back", "logged_in_as": "Logged in as", "btn_logout": "Log Out",
        "hist_title": "Your Shipment History", "tot_ship": "Total Shipments", "pend_appr": "Pending Approval", "processed": "Processed",
        "tab_myship": "My Shipments", "tab_neworder": "New Order", "tab_prof": "Profile Settings",
        "no_orders": "You haven't placed any orders with this account yet. Go to 'New Order' to get started!",
        "status": "Status", "pickup": "Pickup Location", "delivery": "Delivery Destination", "addr": "Address", "zip": "Zip Code", "city": "City",
        "track_trace": "Track & Trace", "track_pending": "Pending assignment...",
        "services": "Services Requested", "add_info": "Additional Info", "btn_cancel": "Cancel This Order",
        "prof_title": "Manage Your Profile", "prof_sub": "Update your company and contact information here.",
        "gen_info": "General Info", "cont_pers": "Contact Person", "email_id": "Email Address (Login ID)",
        "bill_t": "Billing Details", "bill_same": "Use Company and Address from General Info", "b_comp": "Billing Company", "b_em": "Billing Email", "r_name": "Contact Name/Company", "r_ph": "Phone Number",
        "def_pickup": "Default Pickup Location", "def_del": "Default Delivery Destination", "speed_up": "We use this to speed up your orders.",
        "street": "Street Address", "btn_save": "Save Changes", "msg_saving": "Updating profile...", "msg_save_succ": "Profile updated successfully!", "msg_save_fail": "Could not update profile:",
        "msg_cancel_succ": "Order successfully cancelled.",
        "msg_cancel_fail": "Could not cancel the order.",
        "msg_planner": "Message from Dahle Transport:",
        "btn_seen": "Mark as seen (Clear alert)",
        "new_upd": "✨ NEW UPDATE"
    },
    "sv": {
        "nav_home": "Hem", "nav_about": "Om oss", "nav_services": "Tjänster", "nav_gallery": "Galleri", "nav_contact": "Kontakt", 
        "menu_title": "Sidor ⌄", "menu_dash": "Performance Dashboard", "menu_plan": "Intern Planner", "nav_portal": "KUNDPORTAL", "nav_contact_btn": "KONTAKTA OSS",
        "menu_order": "Ny beställning", "menu_login": "Kundportal",
        "portal_title": "Kundportal", "portal_sub": "Logga in för att hantera dina försändelser och uppgifter.",
        "tab_login": "Logga in", "tab_reg": "Skapa konto",
        "lbl_email": "E-postadress", "lbl_pass": "Lösenord", "btn_login": "Logga in",
        "msg_logging_in": "Loggar in...", "msg_login_succ": "Inloggad! Omdirigerar...", "msg_login_fail": "Fel e-post eller lösenord.", "msg_fill_both": "Vänligen fyll i båda fälten.",
        "lbl_comp": "Företagsnamn *", "lbl_fn": "Förnamn *", "lbl_ln": "Efternavn *", "lbl_phone": "Telefonnummer", "lbl_email_reg": "E-post (Detta blir din inloggning) *", "lbl_pass_reg": "Välj lösenord *", "btn_reg": "Skapa konto",
        "msg_creating": "Skapar konto...", "msg_reg_succ": "Konto skapat! Du kan nu logga in via 'Logga in'-fliken.", "msg_reg_fail": "Ett fel uppstod.", "msg_fill_req": "Vänligen fyll i alla obligatoriska fält (*).",
        "welcome": "Välkommen tillbaka", "logged_in_as": "Inloggad som", "btn_logout": "Logga ut",
        "hist_title": "Din sändningshistorik", "tot_ship": "Totala försändelser", "pend_appr": "Väntar på godkännande", "processed": "Behandlad",
        "tab_myship": "Mina försändelser", "tab_neworder": "Ny beställning", "tab_prof": "Profilinställningar",
        "no_orders": "Du har inte lagt några beställningar ännu. Gå till 'Ny beställning' för att börja!",
        "status": "Status", "pickup": "Upphämtningsplats", "delivery": "Leveransplats", "addr": "Adress", "zip": "Postnr", "city": "Stad",
        "track_trace": "Spårning (Track & Trace)", "track_pending": "Väntar på tilldelning...",
        "services": "Begärda tjänster", "add_info": "Ytterligare info", "btn_cancel": "Avbryt denna beställning",
        "prof_title": "Hantera din profil", "prof_sub": "Uppdatera dina företags- och kontaktuppgifter här.",
        "gen_info": "Allmän info", "cont_pers": "Kontaktperson", "email_id": "E-postadress (Inloggnings-ID)",
        "bill_t": "Faktureringsuppgifter", "bill_same": "Använd företag och adress från Allmän Info", "b_comp": "Fakturamottagare (Företag)", "b_em": "Faktura E-post", "r_name": "Kontaktperson (Namn/Företag)", "r_ph": "Telefon",
        "def_pickup": "Standard upphämtningsplats", "def_del": "Standard leveransplats", "speed_up": "Vi använder detta för att påskynda din beställning.",
        "street": "Gatuadress", "btn_save": "Spara ändringar", "msg_saving": "Uppdaterar profil...", "msg_save_succ": "Profil uppdaterad!", "msg_save_fail": "Kunde inte uppdatera profil:",
        "msg_cancel_succ": "Beställningen har avbrutits.",
        "msg_cancel_fail": "Kunde inte avbryta beställningen.",
        "msg_planner": "Meddelande från Dahle Transport:",
        "btn_seen": "Markera som läst (Ta bort avisering)",
        "new_upd": "✨ NY UPPDATERING"
    },
    "da": {
        "nav_home": "Hjem", "nav_about": "Om os", "nav_services": "Tjenester", "nav_gallery": "Galleri", "nav_contact": "Kontakt", 
        "menu_title": "Sider ⌄", "menu_dash": "Performance Dashboard", "menu_plan": "Intern Planner", "nav_portal": "KUNDEPORTAL", "nav_contact_btn": "KONTAKT OS",
        "menu_order": "Ny bestilling", "menu_login": "Kundeportal",
        "portal_title": "Kundeportal", "portal_sub": "Log ind for at administrere dine forsendelser og oplysninger.",
        "tab_login": "Log ind", "tab_reg": "Opret konto",
        "lbl_email": "E-mailadresse", "lbl_pass": "Adgangskode", "btn_login": "Log ind",
        "msg_logging_in": "Logger ind...", "msg_login_succ": "Login succesfuldt! Omdirigerer...", "msg_login_fail": "Forkert e-mail eller adgangskode.", "msg_fill_both": "Udfyld venligst begge felter.",
        "lbl_comp": "Firmanavn *", "lbl_fn": "Fornavn *", "lbl_ln": "Efternavn *", "lbl_phone": "Telefonnummer", "lbl_email_reg": "E-mail (Dette bliver dit login) *", "lbl_pass_reg": "Vælg adgangskode *", "btn_reg": "Opret konto",
        "msg_creating": "Opretter konto...", "msg_reg_succ": "Konto oprettet! Du kan nu logge ind via 'Log ind'-fanen.", "msg_reg_fail": "Der opstod en fejl.", "msg_fill_req": "Udfyld venligst alle obligatoriske felter (*).",
        "welcome": "Velkommen tilbage", "logged_in_as": "Logget ind som", "btn_logout": "Log ud",
        "hist_title": "Din forsendelseshistorik", "tot_ship": "Samlede forsendelser", "pend_appr": "Afventer godkendelse", "processed": "Behandlet",
        "tab_myship": "Mine forsendelser", "tab_neworder": "Ny bestilling", "tab_prof": "Profilindstillinger",
        "no_orders": "Du har endnu ikke foretaget nogen bestillinger. Gå til 'Ny bestilling' for at starte!",
        "status": "Status", "pickup": "Afhentningssted", "delivery": "Leveringssted", "addr": "Adresse", "zip": "Postnr", "city": "By",
        "track_trace": "Sporing (Track & Trace)", "track_pending": "Afventer tildeling...",
        "services": "Anmodede tjenester", "add_info": "Yderligere info", "btn_cancel": "Annuller denne bestilling",
        "prof_title": "Administrer din profil", "prof_sub": "Opdater dine firma- og kontaktoplysninger her.",
        "gen_info": "Generel info", "cont_pers": "Kontaktperson", "email_id": "E-mailadresse (Login-ID)",
        "bill_t": "Faktureringsoplysninger", "bill_same": "Brug firma og adresse fra Generel Info", "b_comp": "Fakturamodtager (Firma)", "b_em": "Faktura E-mail", "r_name": "Kontaktperson (Navn/Firma)", "r_ph": "Telefon",
        "def_pickup": "Standard afhentningssted", "def_del": "Standard leveringssted", "speed_up": "Vi bruger dette til at fremskynde din bestilling.",
        "street": "Gadeadresse", "btn_save": "Gem ændringer", "msg_saving": "Opdaterer profil...", "msg_save_succ": "Profil opdateret!", "msg_save_fail": "Kunne ikke opdatere profil:",
        "msg_cancel_succ": "Bestillingen blev annulleret.",
        "msg_cancel_fail": "Kunne ikke annullere bestillingen.",
        "msg_planner": "Besked fra Dahle Transport:",
        "btn_seen": "Marker som læst (Fjern advarsel)",
        "new_upd": "✨ NY OPDATERING"
    }
}
t = translations.get(lang, translations["en"])

# =========================================================
# 4. DATABASE & AUTH
# =========================================================
def init_connection():
    return create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])

if 'supabase_client' not in st.session_state:
    try: st.session_state.supabase_client = init_connection()
    except Exception: pass
supabase = st.session_state.supabase_client

if 'active_tab' not in st.session_state: st.session_state.active_tab = "My Shipments"
if 'user' not in st.session_state: st.session_state.user = None
if 'role' not in st.session_state: st.session_state.role = "guest"

acc_token = cookie_manager.get('dahle_acc')
ref_token = cookie_manager.get('dahle_ref')

if st.session_state.get('user') is None and acc_token and ref_token:
    try:
        session = supabase.auth.set_session(acc_token, ref_token)
        st.session_state.user = session.user
    except Exception: pass

if st.session_state.get('user'):
    try:
        prof_res = supabase.table("profiles").select("*").eq("id", st.session_state.user.id).execute()
        if prof_res.data:
            st.session_state.company_name = prof_res.data[0].get("company_name", "")
            st.session_state.role = str(prof_res.data[0].get("roles", "customer")).strip().lower()
    except Exception: st.session_state.role = "customer"

is_employee = st.session_state.get('role') in ['admin', 'employee']

# =========================================================
# 5. NAVBAR
# =========================================================
if st.session_state.get('user') is not None and 'company_name' in st.session_state:
    icoon = "<svg style='width:16px; height:16px; margin-right:8px; vertical-align:-2px; fill:currentColor;' viewBox='0 0 640 512'><path d='M224 256A128 128 0 1 0 224 0a128 128 0 1 0 0 256zm-45.7 48C79.8 304 0 383.8 0 482.3C0 498.7 13.3 512 29.7 512H322.8c-3.1-8.8-3.7-18.4-1.4-27.8l15-60.1c2.8-11.3 8.6-21.5 16.8-29.7l40.3-40.3c-32.4-31.6-78-50.1-126.5-50.1H178.3zm212.8-38.1l-40.3 40.3c-15.9 15.9-27.2 35.8-32.5 57.2l-15 60.1c-1.3 5.3-.2 10.9 3.1 15.3s8.5 7.1 14 7.1H592c5.5 0 10.7-2.7 14-7.1s4.4-10 3.1-15.3l-15-60.1c-5.3-21.4-16.6-41.3-32.5-57.2l-40.3-40.3c-23.4-23.4-60.6-23.4-84 0zM456 432c-13.3 0-24-10.7-24-24s10.7-24 24-24s24 10.7 24 24s-10.7 24-24 24z'/></svg>"
    knop_tekst = f"{icoon}{st.session_state.company_name}"
else:
    knop_tekst = t['nav_portal']

dropdown_links = f'<a href="/Order?lang={lang}" target="_self">{t["menu_order"]}</a>'
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
# LOGICA: NIET INGELOGD
# =========================================================
if st.session_state.get('user') is None:
    st.markdown(f"<h2 style='text-align: center; color: #b070c6;'>{t['portal_title']}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #aaaaaa; margin-bottom: 30px;'>{t['portal_sub']}</p>", unsafe_allow_html=True)

    with st.container(border=True):
        tab_login, tab_register = st.tabs([t['tab_login'], t['tab_reg']])
        with tab_login:
            st.write("")
            with st.form("login_form", clear_on_submit=False):
                login_email = st.text_input(t['lbl_email'], key="log_email")
                login_pass = st.text_input(t['lbl_pass'], type="password", key="log_pass")
                st.write("")
                submitted = st.form_submit_button(t['btn_login'], type="primary", use_container_width=True)
            
            status_bericht = st.empty()
            if submitted:
                if login_email and login_pass:
                    with st.spinner(t['msg_logging_in']):
                        try:
                            auth_response = supabase.auth.sign_in_with_password({"email": login_email, "password": login_pass})
                            st.session_state.user = auth_response.user
                            expire_time = datetime.now() + timedelta(days=1)
                            cookie_manager.set('dahle_acc', auth_response.session.access_token, expires_at=expire_time, key="set_a")
                            cookie_manager.set('dahle_ref', auth_response.session.refresh_token, expires_at=expire_time, key="set_r")
                            status_bericht.success(t['msg_login_succ'])
                            time.sleep(1.5); st.rerun()
                        except: status_bericht.error(t['msg_login_fail'])
                else: status_bericht.warning(t['msg_fill_both'])

        with tab_register:
            st.write("")
            reg_company = st.text_input(t['lbl_comp'], key="reg_comp")
            c_fn, c_ln = st.columns(2)
            with c_fn: reg_fname = st.text_input(t['lbl_fn'], key="reg_fn")
            with c_ln: reg_lname = st.text_input(t['lbl_ln'], key="reg_ln")
            reg_phone = st.text_input(t['lbl_phone'], key="reg_phone")
            st.write("---")
            reg_email = st.text_input(t['lbl_email_reg'], key="reg_email")
            reg_pass = st.text_input(t['lbl_pass_reg'], type="password", key="reg_pass")
            
            st.write("")
            if st.button(t['btn_reg'], type="primary", use_container_width=True):
                if reg_email and reg_pass and reg_company and reg_fname and reg_lname:
                    with st.spinner(t['msg_creating']):
                        try:
                            auth_res = supabase.auth.sign_up({"email": reg_email, "password": reg_pass})
                            profile_data = {
                                "id": auth_res.user.id, "company_name": reg_company,
                                "contact_name": f"{reg_fname} {reg_lname}", "phone": reg_phone, "roles": "customer"
                            }
                            supabase.table("profiles").insert(profile_data).execute()
                            st.success(t['msg_reg_succ'])
                        except: st.error(t['msg_reg_fail'])
                else: st.warning(t['msg_fill_req'])

# =========================================================
# LOGICA: INGELOGD
# =========================================================
else:
    user_id = st.session_state.user.id
    try:
        prof_res = supabase.table("profiles").select("*").eq("id", user_id).execute()
        profile = prof_res.data[0] if prof_res.data else {}
        st.session_state.company_name = profile.get("company_name", "Valued Customer")
    except: profile = {}

    company_name = profile.get("company_name", "Valued Customer")
    contact_name = profile.get("contact_name", "")
    phone_nr = profile.get("phone", "")
    email_addr = st.session_state.user.email

    try: user_orders = supabase.table("orders").select("*").eq("user_id", user_id).order("id", desc=True).execute().data
    except: user_orders = []

    c_head1, c_head2 = st.columns([3, 1])
    with c_head1:
        st.markdown(f"<h2 style='color: #b070c6; margin-bottom: 0px;'>{t['welcome']}, {company_name}!</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #888; font-size: 14px;'>{t['logged_in_as']}: {email_addr}</p>", unsafe_allow_html=True)
    with c_head2:
        st.write("")
        if st.button(t['btn_logout'], type="secondary", use_container_width=True):
            cookie_manager.delete('dahle_acc', key="del_a"); cookie_manager.delete('dahle_ref', key="del_r")
            supabase.auth.sign_out()
            st.session_state.user = None
            if 'company_name' in st.session_state: del st.session_state['company_name']
            if 'role' in st.session_state: del st.session_state['role']
            st.rerun()
            
    st.write("---")
    
    st.markdown(f"### {t['hist_title']}")
    m1, m2, m3 = st.columns(3)
    m1.metric(t['tot_ship'], len(user_orders))
    m2.metric(t['pend_appr'], sum(1 for o in user_orders if o['status'] == 'New'))
    m3.metric(t['processed'], sum(1 for o in user_orders if o['status'] in ['Processed', 'Delivered']))
    st.write("---")

    col_menu1, col_menu2, col_menu3 = st.columns(3)
    with col_menu1:
        if st.button(t['tab_myship'], type="primary" if st.session_state.active_tab == "My Shipments" else "secondary", use_container_width=True): st.session_state.active_tab = "My Shipments"; st.rerun()
    with col_menu2:
        if st.button(t['tab_neworder'], type="secondary", use_container_width=True): st.switch_page("pages/Order.py")
    with col_menu3:
        if st.button(t['tab_prof'], type="primary" if st.session_state.active_tab == "Profile Settings" else "secondary", use_container_width=True): st.session_state.active_tab = "Profile Settings"; st.rerun()
    st.write("") 

    if st.session_state.active_tab == "My Shipments":
        if not user_orders: st.info(t['no_orders'])
        else:
            for o in user_orders:
                status_icon = "🔵" if o['status'] == 'New' else "🟡" if o['status'] == 'In Progress' else "🟢" if o['status'] in ['Processed', 'Delivered'] else "🔴"
                
                # NIEUW: Check of er een ongelezen update is
                unread = o.get('has_unread_update', False)
                update_badge = f" &nbsp; {t['new_upd']}" if unread else ""
                
                with st.expander(f"{status_icon} Order #{o['id']} — {o.get('received_date', '')[:10]} ({t['status']}: {o['status']}){update_badge}"):
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # NIEUW: Toon bericht van de planner als dit is aangevinkt
                    if o.get('show_note_to_customer') and o.get('edit_reason'):
                        st.markdown(f"""
                        <div style='background-color: #2b1515; border-left: 4px solid #ff4b4b; padding: 12px 16px; border-radius: 6px; margin-bottom: 20px;'>
                            <span style='color: #ffcccc; font-size: 14px;'><b>⚠️ {t['msg_planner']}</b><br>{o['edit_reason']}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # NIEUW: Knop om de highlight/melding weg te klikken
                    if unread:
                        c_read_btn, _ = st.columns([1, 2])
                        with c_read_btn:
                            if st.button(t['btn_seen'], key=f"read_{o['id']}", type="secondary", use_container_width=True):
                                try:
                                    supabase.table("orders").update({"has_unread_update": False}).eq("id", o['id']).execute()
                                    st.rerun()
                                except Exception as e:
                                    pass
                        st.write("---")

                    c_det1, c_det2 = st.columns(2)
                    with c_det1:
                        st.markdown(f"#### {t['pickup']}")
                        st.write(f"**{t['addr']}:** {o.get('pickup_address', '-')}")
                        st.write(f"**{t['zip']}:** {o.get('pickup_zip', '-')}")
                        st.write(f"**{t['city']}:** {o.get('pickup_city', '-')}")
                        st.write("")
                        st.markdown(f"#### {t['delivery']}")
                        st.write(f"**{t['addr']}:** {o.get('delivery_address', '-')}")
                        st.write(f"**{t['zip']}:** {o.get('delivery_zip', '-')}")
                        st.write(f"**{t['city']}:** {o.get('delivery_city', '-')}")
                        
                    with c_det2:
                        tracking_code = o.get('tracking_code')
                        st.markdown(f"#### 📦 {t['track_trace']}")
                        if tracking_code and str(tracking_code).strip():
                            st.markdown(f"<div style='background-color: #262626; padding: 10px 14px; border-radius: 6px; border-left: 4px solid #b070c6; margin-bottom: 20px;'><span style='color: #bbb; font-size: 13px;'>Code: </span><span style='color: #fff; font-size: 15px; font-weight: bold;'>{tracking_code}</span></div>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<div style='background-color: #1e1e1e; padding: 10px 14px; border-radius: 6px; border-left: 4px solid #555; margin-bottom: 20px;'><span style='color: #888; font-size: 13px; font-style: italic;'>{t['track_pending']}</span></div>", unsafe_allow_html=True)
                        
                        st.markdown(f"#### {t['services']}")
                        st.write(f"{o.get('types', '-')}")
                        st.write("")
                        st.markdown(f"#### {t['add_info']}")
                        st.write(f"{o.get('info', '-')}")
                    
                    if o['status'] == 'New':
                        st.write("---")
                        c_space1, c_cancel, c_space2 = st.columns([1, 2, 1])
                        with c_cancel:
                            if st.button(t['btn_cancel'], key=f"cancel_{o['id']}", type="secondary", use_container_width=True):
                                try: 
                                    supabase.table("orders").update({"status": "Cancelled"}).eq("id", o['id']).execute()
                                    st.success(t['msg_cancel_succ'])
                                    time.sleep(1)
                                    st.rerun()
                                except Exception as e: 
                                    st.error(f"{t['msg_cancel_fail']} Details: {str(e)}")
                        
                    st.markdown("<br>", unsafe_allow_html=True)

    elif st.session_state.active_tab == "Profile Settings":
        st.markdown(f"### {t['prof_title']}")
        st.markdown(f"<p style='color:#aaaaaa;'>{t['prof_sub']}</p>", unsafe_allow_html=True)
        
        with st.container(border=True):
            st.markdown(f"#### {t['gen_info']}")
            upd_company = st.text_input(t['lbl_comp'].replace(" *", ""), value=company_name, key="upd_comp")
            upd_contact = st.text_input(t['cont_pers'], value=contact_name, key="upd_cont")
            upd_phone = st.text_input(t['lbl_phone'], value=phone_nr, key="upd_phone")
            st.text_input(t['email_id'], value=email_addr, disabled=True, key="upd_email")
            
            upd_main_addr = st.text_input(t['street'], value=profile.get("address", ""), key="upd_main_addr")
            c_mz, c_mc = st.columns(2)
            with c_mz: upd_main_zip = st.text_input(t['zip'], value=profile.get("zip_code", ""), key="upd_main_zip")
            with c_mc: upd_main_city = st.text_input(t['city'], value=profile.get("city", ""), key="upd_main_city")
            
            st.write("---")
            st.markdown(f"#### {t['bill_t']}")
            
            heeft_afwijkende_billing = bool(profile.get("billing_company") and profile.get("billing_company") != company_name)
            same_billing_prof = st.checkbox(t.get('bill_same'), value=not heeft_afwijkende_billing, key="prof_same_bill")
            
            c_b1, c_b2 = st.columns(2)
            with c_b1:
                if same_billing_prof:
                    upd_b_comp = st.text_input(t['b_comp'], value=upd_company, disabled=True, key="upd_b_comp_dis")
                    upd_b_email = st.text_input(t['b_em'], value=email_addr, disabled=True, key="upd_b_email_dis")
                else:
                    upd_b_comp = st.text_input(t['b_comp'], value=profile.get("billing_company", ""), key="upd_b_comp")
                    upd_b_email = st.text_input(t['b_em'], value=profile.get("billing_email", ""), key="upd_b_email")
                    
            with c_b2:
                if same_billing_prof:
                    upd_b_addr = st.text_input(t['street'], value=upd_main_addr, disabled=True, key="upd_b_addr_dis")
                    c_bz, c_bc = st.columns(2)
                    with c_bz: upd_b_zip = st.text_input(t['zip'], value=upd_main_zip, disabled=True, key="upd_b_zip_dis")
                    with c_bc: upd_b_city = st.text_input(t['city'], value=upd_main_city, disabled=True, key="upd_b_city_dis")
                else:
                    upd_b_addr = st.text_input(t['street'], value=profile.get("billing_address", ""), key="upd_b_addr")
                    c_bz, c_bc = st.columns(2)
                    with c_bz: upd_b_zip = st.text_input(t['zip'], value=profile.get("billing_zip", ""), key="upd_b_zip")
                    with c_bc: upd_b_city = st.text_input(t['city'], value=profile.get("billing_city", ""), key="upd_b_city")
            
            st.write("---")
            st.markdown(f"#### {t['def_pickup']}")
            st.markdown(f"<p style='color:#888; font-size:13px;'>{t['speed_up']}</p>", unsafe_allow_html=True)
            c_pn, c_pp = st.columns(2)
            with c_pn: upd_p_name = st.text_input(t['r_name'] + " (Pickup)", value=profile.get("pickup_name", ""), key="upd_p_name")
            with c_pp: upd_p_phone = st.text_input(t['r_ph'] + " (Pickup)", value=profile.get("pickup_phone", ""), key="upd_p_phone")
            upd_address = st.text_input(t['street'] + " ", value=profile.get("pickup_address", ""), key="upd_addr")
            col_zip, col_city = st.columns(2)
            with col_zip: upd_zip = st.text_input(t['zip'] + " ", value=profile.get("pickup_zip", ""), key="upd_zip")
            with col_city: upd_city = st.text_input(t['city'] + " ", value=profile.get("pickup_city", ""), key="upd_city")
            
            st.write("---")
            st.markdown(f"#### {t['def_del']}")
            st.markdown(f"<p style='color:#888; font-size:13px;'>{t['speed_up']}</p>", unsafe_allow_html=True)
            c_dn, c_dp = st.columns(2)
            with c_dn: upd_d_name = st.text_input(t['r_name'] + " (Delivery)", value=profile.get("delivery_name", ""), key="upd_d_name")
            with c_dp: upd_d_phone = st.text_input(t['r_ph'] + " (Delivery)", value=profile.get("delivery_phone", ""), key="upd_d_phone")
            upd_del_address = st.text_input(t['street'] + "  ", value=profile.get("del_address", ""), key="upd_del_addr")
            col_d_zip, col_d_city = st.columns(2)
            with col_d_zip: upd_del_zip = st.text_input(t['zip'] + "  ", value=profile.get("del_zip", ""), key="upd_del_zip")
            with col_d_city: upd_del_city = st.text_input(t['city'] + "  ", value=profile.get("del_city", ""), key="upd_del_city")
            
            st.write("")
            if st.button(t['btn_save'], type="primary"):
                update_data = {
                    "company_name": upd_company,
                    "contact_name": upd_contact,
                    "phone": upd_phone,
                    
                    "address": upd_main_addr,
                    "zip_code": upd_main_zip,
                    "city": upd_main_city,
                    
                    "billing_company": upd_b_comp,
                    "billing_email": upd_b_email,
                    "billing_address": upd_b_addr,
                    "billing_zip": upd_b_zip,
                    "billing_city": upd_b_city,

                    "pickup_name": upd_p_name,
                    "pickup_phone": upd_p_phone,
                    "pickup_address": upd_address,
                    "pickup_zip": upd_zip,
                    "pickup_city": upd_city,
                    
                    "delivery_name": upd_d_name,
                    "delivery_phone": upd_d_phone,
                    "del_address": upd_del_address,
                    "del_zip": upd_del_zip,
                    "del_city": upd_del_city
                }
                with st.spinner(t['msg_saving']):
                    try:
                        supabase.table("profiles").update(update_data).eq("id", user_id).execute()
                        st.success(t['msg_save_succ'])
                        st.session_state.company_name = upd_company
                        time.sleep(1.5); st.rerun() 
                    except Exception as e:
                        st.error(f"{t['msg_save_fail']} {e}")
