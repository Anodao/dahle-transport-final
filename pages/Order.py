import streamlit as st
import time
import requests
import pandas as pd
import pydeck as pdk
from datetime import datetime
from supabase import create_client
import extra_streamlit_components as stx

# --- PAGE CONFIG ---
st.set_page_config(page_title="Dahle Transport - Order", page_icon="🚚", layout="wide", initial_sidebar_state="collapsed")

# =========================================================
# 0. DIRECTE CSS INJECTIE 
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
* { font-family: 'Montserrat', sans-serif; }

/* FIX 1: ZIJBALK PIJLTJE ALTIJD ZICHTBAAR */
header[data-testid="stHeader"] { background-color: transparent !important; z-index: 1001 !important; }
footer { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
div[class^="viewerBadge"] { display: none !important; }
.block-container { padding-top: 110px; }

/* NAVBAR CSS */
.navbar { position: fixed; top: 0; left: 0; width: 100%; height: 90px; background-color: white; z-index: 999; border-bottom: 1px solid #eaeaea; display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; padding: 0 40px; box-shadow: 0 2px 10px rgba(0,0,0,0.03); }
.nav-logo { margin-left: 40px; display: flex; justify-content: flex-start; }
.nav-logo a { display: inline-block; height: 48px; text-decoration: none; cursor: pointer; }
.nav-logo img { height: 100%; width: auto; display: block; transition: transform 0.2s ease-in-out; }
.nav-logo a:hover img { transform: scale(1.05); } 
.nav-links { display: flex; gap: 28px; font-size: 15px; font-weight: 500; color: #000000; justify-content: center;}
.nav-links a { text-decoration: none; color: inherit; }
.nav-links span { cursor: pointer; transition: color 0.2s; }
.nav-links span:hover { color: #894b9d; }
.nav-cta { display: flex; justify-content: flex-end; gap: 15px; align-items: center; }
.cta-btn { background-color: #894b9d; color: white !important; padding: 10px 24px; border-radius: 50px; text-decoration: none !important; font-weight: 600; font-size: 13px; letter-spacing: 0.5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); cursor: pointer; transition: background-color 0.2s; white-space: nowrap; }
.cta-btn:hover { background-color: #723e83; }
.cta-btn-outline { background-color: transparent; color: #894b9d !important; padding: 10px 20px; border-radius: 50px; text-decoration: none !important; font-weight: 600; font-size: 13px; letter-spacing: 0.5px; border: 2px solid #894b9d; cursor: pointer; transition: all 0.2s; white-space: nowrap; }
.cta-btn-outline:hover { background-color: #894b9d; color: white !important; }

/* FIX 2: DROPDOWN MENU */
.lang-dropdown { position: relative; display: inline-block; margin-right: 10px; padding-bottom: 15px; margin-bottom: -15px; }
.lang-dropbtn { background-color: #f8f9fa; color: #111; font-weight: 600; font-size: 13px; border: 1px solid #eaeaea; border-radius: 20px; padding: 8px 16px; cursor: pointer; display: flex; align-items: center; gap: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.03); transition: all 0.2s ease; }
.lang-dropbtn:hover { background-color: #eaeaea; }
.lang-dropdown-content { display: none; position: absolute; background-color: #ffffff; min-width: 140px; box-shadow: 0px 8px 24px rgba(0,0,0,0.12); border-radius: 12px; border: 1px solid #eaeaea; z-index: 1000; top: 100%; right: 0; overflow: hidden; }
.lang-dropdown-content a { color: #111 !important; padding: 12px 16px; text-decoration: none; display: flex; align-items: center; gap: 10px; font-size: 14px; font-weight: 500; transition: background-color 0.2s; }
.lang-dropdown-content a:hover { background-color: #f4e9f7; color: #894b9d !important; }
.lang-dropdown:hover .lang-dropdown-content { display: block; }

/* STAPPEN FORMULIER CSS */
.step-wrapper { display: flex; justify-content: center; align-items: flex-start; margin-bottom: 30px; margin-top: 10px; gap: 15px; }
.step-item { display: flex; flex-direction: column; align-items: center; width: 80px; }
.step-circle { width: 40px; height: 40px; border-radius: 50%; border: 2px solid #555; display: flex; justify-content: center; align-items: center; font-weight: 700; font-size: 16px; color: #aaa; background-color: #262626; margin-bottom: 10px; z-index: 2; transition: 0.3s; }
.step-label { font-size: 13px; font-weight: 600; color: #888; text-align: center; }
.step-line { height: 2px; width: 60px; background-color: #444; margin-top: 20px; }
.step-item.active .step-circle { border-color: #ffffff; background-color: #ffffff; color: #000000; }
.step-item.active .step-label { color: #ffffff; }
.step-item.completed .step-circle { border-color: #894b9d; background-color: #894b9d; color: white; }
.step-item.completed .step-label { color: #894b9d; }
.line-completed { background-color: #894b9d; }

div.stButton > button[kind="primary"] { background: linear-gradient(135deg, #b070c6 0%, #894b9d 100%) !important; color: #ffffff !important; border: 2px solid transparent !important; border-radius: 6px !important; padding: 14px 28px !important; font-weight: 600 !important; font-size: 15px !important; box-shadow: 0 4px 14px 0 rgba(137, 75, 157, 0.4) !important; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important; width: 100% !important; white-space: nowrap !important; }
div.stButton > button[kind="primary"]:hover { background: #ffffff !important; color: #894b9d !important; border: 2px solid #894b9d !important; transform: translateY(-2px) !important; box-shadow: 0 8px 24px rgba(137, 75, 157, 0.6) !important; }
div.stButton > button[kind="secondary"] { background: transparent !important; color: #e0c2ed !important; padding: 14px 24px !important; border-radius: 6px !important; font-weight: 600 !important; font-size: 14px !important; border: 2px solid #894b9d !important; transition: all 0.3s ease !important; width: 100% !important; white-space: nowrap !important; }
div.stButton > button[kind="secondary"]:hover { background: #ffffff !important; border-color: #894b9d !important; color: #894b9d !important; transform: translateY(-2px) !important; box-shadow: 0 4px 12px rgba(137, 75, 157, 0.3) !important; }
div[data-baseweb="input"], div[data-baseweb="select"], div[data-baseweb="textarea"] { background-color: #333; border-radius: 8px; }
div[data-baseweb="input"] input, div[data-baseweb="textarea"] textarea { color: white; }
label { color: #ccc !important; font-weight: 600; font-size: 14px !important;}
div[data-baseweb="select"] div { color: white; background-color: #333;}
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
# 2. HET ORDER WOORDENBOEK
# =========================================================
translations = {
    "no": {
        "nav_home": "Hjem", "nav_about": "Om oss", "nav_services": "Tjenester", "nav_gallery": "Galleri", "nav_contact": "Kontakt", "nav_portal": "KUNDEPORTAL", "nav_contact_btn": "TA KONTAKT",
        "st1": "Forsendelse", "st2": "Detaljer", "st3": "Se over",
        "t_match": "Velg det du vanligvis sender for å finne riktig tjeneste.", "t_sub": "Velg minst ett alternativ for å fortsette",
        "b1_t": "Pakker & Dokumenter", "b1_s": "Typisk opptil 31.5kg", "b1_l1": "Lette til middels tunge sendinger", "b1_l2": "B2B/B2C", "b_com": "Vanlige sendinger:",
        "b2_t": "Gods & Frakt", "b2_s": "Typisk over 31.5kg+", "b2_l1": "Tyngre forsendelser (paller/containere)", "b2_l2": "B2B",
        "b3_t": "Post & Markedsføring", "b3_s": "Typisk opptil 2kg", "b3_l1": "Lette varer", "b3_l2": "Internasjonal post (brev, brosjyrer)",
        "err_sel": "❌ Vennligst velg minst ett alternativ.", "time_est": "⏱ Tar vanligvis under 5 minutter.", "btn_next": "Neste steg",
        "w_tot": "Totalvekt (kg)", "w_over": "Overdimensjonert / Uvanlig form", "l_type": "**Lasttype ***", "l_err": " 🚨 :red[(Velg minst én)]", "l_pal": "Pall", "l_full": "Full container/lastebil", "l_lc": "Stykkgods", "w_est": "Estimert totalvekt (kg)",
        "c_det": "🏢 Firma- & Kontaktdetaljer", "c_name": "Firmanavn *", "c_reg": "Foretaksregister (valgfritt)", "c_addr": "Firmaadresse *", "c_zip": "Postnummer *", "c_city": "By *", "c_ctry": "Land *",
        "c_fn": "Fornavn *", "c_ln": "Etternavn *", "c_em": "Jobb-e-post *", "c_ph": "Telefon *",
        "r_info": "📍 Ruteinformasjon", "r_pick": "📤 Hentested", "r_del": "📥 Leveringssted", "r_str": "Gateadresse *",
        "m_wait": "🗺️ Kartet vises når du skriver inn en adresse...", "a_info": "Tilleggsinformasjon (valgfritt)", "a_ph": "Beskriv hva du sender, ca. vekt, spesielle krav, etc.",
        "p_note": "Hvis du vil vite mer om hvordan vi bruker dataene dine, les vår personvernerklæring i bunnteksten.",
        "e_req": "⚠️ Vennligst fyll ut alle obligatoriske felt (*) før du fortsetter.", "e_em": "⚠️ Ugyldig e-postadresse.",
        "b_back": "← Gå tilbake", "b_cont": "Fortsett til neste steg →",
        "rev_t": "📝 Se over forespørselen din", "rev_s": "Vennligst sjekk at detaljene stemmer.", "rev_c": "🏢 Firma & Kontakt",
        "l_cn": "FIRMANAVN", "l_rn": "ORG.NR", "l_ad": "ADRESSE", "l_cp": "KONTAKTPERSON", "l_em": "E-POST", "l_ph": "TELEFON", "l_str": "GATEADRESSE", "l_zc": "POSTNR & BY",
        "rev_r": "📍 Rute", "rev_s": "📦 Forsendelse", "l_no": "NOTATER", "b_edit": "← Rediger detaljer", "b_send": "✅ BEKREFT & SEND",
        "db_err": "⚠️ Feil: Kunne ikke lagre i databasen.", "s_succ": "🎉 Din forespørsel er sendt!", "s_sub": "Vi tar kontakt snart.", "b_new": "← Start en ny forespørsel",
        "calc_t": "Estimert Kostnad", "c_base": "Grunngebyr", "c_hw": "Håndtering & Vekt", "c_tr": "Transport", "c_ww": "Internasjonal Flyfrakt", "c_src": "Søker adresse...", "c_aw": "Venter på rute...", "c_tot": "Total", "c_vat": "Ekskl. MVA (VAT)"
    },
    "en": {
        "nav_home": "Home", "nav_about": "About us", "nav_services": "Services", "nav_gallery": "Gallery", "nav_contact": "Contact", "nav_portal": "CUSTOMER PORTAL", "nav_contact_btn": "CONTACT US",
        "st1": "Shipment", "st2": "Details", "st3": "Review",
        "t_match": "To find your service match, select all that you ship.", "t_sub": "Select at least one option to continue",
        "b1_t": "Parcels & Documents", "b1_s": "Typically up to 31.5kg", "b1_l1": "Light to medium weight shipments", "b1_l2": "B2B/B2C", "b_com": "Commonly shipped:",
        "b2_t": "Cargo & Freight", "b2_s": "Typically over 31.5kg+", "b2_l1": "Heavier shipments (pallets/containers)", "b2_l2": "B2B",
        "b3_t": "Mail & Marketing", "b3_s": "Typically up to 2kg", "b3_l1": "Lightweight goods", "b3_l2": "International business mail",
        "err_sel": "❌ Please select at least one option.", "time_est": "⏱ Typically takes less than 5 minutes.", "btn_next": "Next Step",
        "w_tot": "Total Weight (kg)", "w_over": "Oversized / Irregular Shape", "l_type": "**Load Type ***", "l_err": " 🚨 :red[(Select at least one)]", "l_pal": "Pallet", "l_full": "Full Container/Truck", "l_lc": "Loose Cargo", "w_est": "Total Est. Weight (kg)",
        "c_det": "🏢 Company & Contact Details", "c_name": "Company Name *", "c_reg": "Registration No. (optional)", "c_addr": "Company Address *", "c_zip": "Zip Code *", "c_city": "City *", "c_ctry": "Country *",
        "c_fn": "First Name *", "c_ln": "Last Name *", "c_em": "Work Email *", "c_ph": "Phone *",
        "r_info": "📍 Route Information", "r_pick": "📤 Pickup Location", "r_del": "📥 Delivery Destination", "r_str": "Street Address *",
        "m_wait": "🗺️ Map will appear when you enter an address...", "a_info": "Additional Information (optional)", "a_ph": "Describe what you ship, approx. weight, etc.",
        "p_note": "To learn how we use your data, read our privacy notice in the footer.",
        "e_req": "⚠️ Please fill in all mandatory fields (*).", "e_em": "⚠️ Invalid email address.",
        "b_back": "← Go Back", "b_cont": "Continue to Review →",
        "rev_t": "📝 Review your request", "rev_s": "Please verify your details below.", "rev_c": "🏢 Company & Contact",
        "l_cn": "COMPANY NAME", "l_rn": "REG. NO", "l_ad": "ADDRESS", "l_cp": "CONTACT PERSON", "l_em": "EMAIL", "l_ph": "PHONE", "l_str": "STREET ADDRESS", "l_zc": "ZIP & CITY",
        "rev_r": "📍 Route", "rev_s": "📦 Shipment", "l_no": "NOTES", "b_edit": "← Edit Details", "b_send": "✅ CONFIRM & SEND",
        "db_err": "⚠️ Error: Failed to send to database.", "s_succ": "🎉 Request sent successfully!", "s_sub": "We will get in touch shortly.", "b_new": "← Start a New Request",
        "calc_t": "Estimated Cost", "c_base": "Base Fee", "c_hw": "Handling & Weight", "c_tr": "Transport", "c_ww": "Worldwide Air Freight", "c_src": "Searching address...", "c_aw": "Awaiting route...", "c_tot": "Total", "c_vat": "Excl. MVA (VAT)"
    },
    "sv": {
        "nav_home": "Hem", "nav_about": "Om oss", "nav_services": "Tjänster", "nav_gallery": "Galleri", "nav_contact": "Kontakt", "nav_portal": "KUNDPORTAL", "nav_contact_btn": "KONTAKTA OSS",
        "st1": "Försändelse", "st2": "Detaljer", "st3": "Granska",
        "t_match": "Välj vad du brukar skicka för att hitta rätt tjänst.", "t_sub": "Välj minst ett alternativ för att fortsätta",
        "b1_t": "Paket & Dokument", "b1_s": "Vanligtvis upp till 31.5kg", "b1_l1": "Lätta till medeltunga försändelser", "b1_l2": "B2B/B2C", "b_com": "Vanliga försändelser:",
        "b2_t": "Gods & Frakt", "b2_s": "Vanligtvis över 31.5kg+", "b2_l1": "Tyngre försändelser (pallar/containrar)", "b2_l2": "B2B",
        "b3_t": "Post & Marknadsföring", "b3_s": "Vanligtvis upp till 2kg", "b3_l1": "Lätta varer", "b3_l2": "Internationell företagspost",
        "err_sel": "❌ Vänligen välj minst ett alternativ.", "time_est": "⏱ Tar vanligtvis under 5 minuter.", "btn_next": "Nästa steg",
        "w_tot": "Totalvikt (kg)", "w_over": "Överdimensionerad / Ovanlig form", "l_type": "**Lasttyp ***", "l_err": " 🚨 :red[(Välj minst en)]", "l_pal": "Pall", "l_full": "Full container/lastbil", "l_lc": "Styckgods", "w_est": "Uppskattad totalvikt (kg)",
        "c_det": "🏢 Företags- & Kontaktdetaljer", "c_name": "Företagsnamn *", "c_reg": "Organisationsnummer (frivilligt)", "c_addr": "Företagsadress *", "c_zip": "Postnummer *", "c_city": "Stad *", "c_ctry": "Land *",
        "c_fn": "Förnamn *", "c_ln": "Efternamn *", "c_em": "Jobb-e-post *", "c_ph": "Telefon *",
        "r_info": "📍 Ruttinformation", "r_pick": "📤 Upphämtningsplats", "r_del": "📥 Leveransplats", "r_str": "Gatuadress *",
        "m_wait": "🗺️ Kartan visas när du skriver in en adress...", "a_info": "Ytterligare information (frivilligt)", "a_ph": "Beskriv vad du skickar, ca vikt etc.",
        "p_note": "För att läsa mer om hur vi hanterar din data, se vår integritetspolicy.",
        "e_req": "⚠️ Vänligen fyll i alla obligatoriska fält (*).", "e_em": "⚠️ Ogiltig e-postadress.",
        "b_back": "← Gå tillbaka", "b_cont": "Fortsätt till granskning →",
        "rev_t": "📝 Granska din förfrågan", "rev_s": "Vänligen kontrollera dina uppgifter.", "rev_c": "🏢 Företag & Kontakt",
        "l_cn": "FÖRETAGSNAMN", "l_rn": "ORG.NR", "l_ad": "ADRESS", "l_cp": "KONTAKTPERSON", "l_em": "E-POST", "l_ph": "TELEFON", "l_str": "GATUADRESS", "l_zc": "POSTNR & STAD",
        "rev_r": "📍 Rutt", "rev_s": "📦 Försändelse", "l_no": "ANTECKNINGAR", "b_edit": "← Redigera detaljer", "b_send": "✅ BEKRÄFTA & SKICKA",
        "db_err": "⚠️ Fel: Kunde inte spara i databasen.", "s_succ": "🎉 Din förfrågan har skickats!", "s_sub": "Vi återkommer inom kort.", "b_new": "← Starta en ny förfrågan",
        "calc_t": "Uppskattad Kostnad", "c_base": "Grundavgift", "c_hw": "Hantering & Vikt", "c_tr": "Transport", "c_ww": "Internationell Flygfrakt", "c_src": "Söker adress...", "c_aw": "Väntar på rutt...", "c_tot": "Totalt", "c_vat": "Exkl. Moms (VAT)"
    },
    "da": {
        "nav_home": "Hjem", "nav_about": "Om os", "nav_services": "Tjenester", "nav_gallery": "Galleri", "nav_contact": "Kontakt", "nav_portal": "KUNDEPORTAL", "nav_contact_btn": "KONTAKT OS",
        "st1": "Forsendelse", "st2": "Detaljer", "st3": "Gennemgå",
        "t_match": "Vælg det du normalt sender, for at finde den rette tjeneste.", "t_sub": "Vælg mindst én mulighed for at fortsætte",
        "b1_t": "Pakker & Dokumenter", "b1_s": "Typisk op til 31.5kg", "b1_l1": "Lette til mellemtunge forsendelser", "b1_l2": "B2B/B2C", "b_com": "Almindelige forsendelser:",
        "b2_t": "Gods & Fragt", "b2_s": "Typisk over 31.5kg+", "b2_l1": "Tungere forsendelser (pallar/containere)", "b2_l2": "B2B",
        "b3_t": "Post & Markedsføring", "b3_s": "Typisk op til 2kg", "b3_l1": "Lette varer", "b3_l2": "International erhvervspost",
        "err_sel": "❌ Vælg venligst mindst én mulighed.", "time_est": "⏱ Tager typisk under 5 minutter.", "btn_next": "Næste trin",
        "w_tot": "Totalvægt (kg)", "w_over": "Overdimensioneret / Usædvanlig form", "l_type": "**Lasttype ***", "l_err": " 🚨 :red[(Vælg mindst én)]", "l_pal": "Palle", "l_full": "Fuld container/lastbil", "l_lc": "Stykgods", "w_est": "Estimeret totalvægt (kg)",
        "c_det": "🏢 Firma- & Kontaktdetaljer", "c_name": "Firmanavn *", "c_reg": "CVR-nummer (valgfrit)", "c_addr": "Firmaadresse *", "c_zip": "Postnummer *", "c_city": "By *", "c_ctry": "Land *",
        "c_fn": "Fornavn *", "c_ln": "Efternavn *", "c_em": "Arbejds-e-mail *", "c_ph": "Telefon *",
        "r_info": "📍 Ruteinformation", "r_pick": "📤 Afhentningssted", "r_del": "📥 Leveringssted", "r_str": "Gadeadresse *",
        "m_wait": "🗺️ Kortet vises, når du indtaster en adresse...", "a_info": "Yderligere information (valgfrit)", "a_ph": "Beskriv hvad du sender, ca. vægt osv.",
        "p_note": "Læs vores privatlivspolitik i bunden for at se, hvordan vi bruger dine data.",
        "e_req": "⚠️ Udfyld venligst alle obligatoriske felter (*).", "e_em": "⚠️ Ugyldig e-mailadresse.",
        "b_back": "← Gå tilbage", "b_cont": "Fortsæt til gennemgang →",
        "rev_t": "📝 Gennemgå din anmodning", "rev_s": "Tjek venligst at dine oplysninger er korrekte.", "rev_c": "🏢 Firma & Kontakt",
        "l_cn": "FIRMANAVN", "l_rn": "CVR.NR", "l_ad": "ADRESSE", "l_cp": "KONTAKTPERSON", "l_em": "E-MAIL", "l_ph": "TELEFON", "l_str": "GADEADRESSE", "l_zc": "POSTNR & BY",
        "rev_r": "📍 Rute", "rev_s": "📦 Forsendelse", "l_no": "NOTER", "b_edit": "← Rediger detaljer", "b_send": "✅ BEKRÆFT & SEND",
        "db_err": "⚠️ Fejl: Kunne ikke gemme i databasen.", "s_succ": "🎉 Din anmodning er sendt!", "s_sub": "Vi vender tilbage snarest.", "b_new": "← Start en ny anmodning",
        "calc_t": "Estimeret Pris", "c_base": "Grundgebyr", "c_hw": "Håndtering & Vægt", "c_tr": "Transport", "c_ww": "International Luftfragt", "c_src": "Søger adresse...", "c_aw": "Afventer rute...", "c_tot": "Total", "c_vat": "Ekskl. Moms (VAT)"
    }
}
t = translations[lang]

# =========================================================
# 3. DATABASE & AUTHENTICATIE 
# =========================================================
def init_connection():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

if 'supabase_client' not in st.session_state:
    try: st.session_state.supabase_client = init_connection()
    except Exception as e: pass

supabase = st.session_state.supabase_client

if 'user' not in st.session_state:
    st.session_state.user = None

acc_token = cookie_manager.get('dahle_acc')
ref_token = cookie_manager.get('dahle_ref')

if st.session_state.get('user') is None and acc_token and ref_token:
    with st.spinner("Loading account... ⏳"):
        time.sleep(0.5)
        try:
            session = supabase.auth.set_session(acc_token, ref_token)
            st.session_state.user = session.user
        except Exception:
            pass

# FIX VOOR ATTRIBUTE ERROR:
current_user_id = st.session_state.user.id if st.session_state.get('user') else "guest"

if st.session_state.get('last_seen_user_id') != current_user_id:
    safe_profile = {}
    if current_user_id != "guest":
        try:
            prof_res = supabase.table("profiles").select("*").eq("id", current_user_id).execute()
            if prof_res.data:
                raw_prof = prof_res.data[0]
                name_parts = str(raw_prof.get('contact_name', '')).split(' ', 1)
                st.session_state.company_name = raw_prof.get("company_name", "")
                safe_profile = {
                    'comp_name': str(raw_prof.get('company_name') or ''), 'cont_fn': name_parts[0] if name_parts else '', 'cont_ln': name_parts[1] if len(name_parts) > 1 else '',
                    'cont_email': st.session_state.user.email, 'cont_phone': str(raw_prof.get('phone') or ''), 'comp_addr': str(raw_prof.get('address') or ''), 'comp_pc': str(raw_prof.get('zip_code') or ''),
                    'comp_city': str(raw_prof.get('city') or ''), 'p_addr': str(raw_prof.get('address') or ''), 'p_zip': str(raw_prof.get('zip_code') or ''), 'p_city': str(raw_prof.get('city') or ''),
                    'd_addr': str(raw_prof.get('del_address') or ''), 'd_zip': str(raw_prof.get('del_zip') or ''), 'd_city': str(raw_prof.get('del_city') or '')
                }
        except: pass
    st.session_state['user_db_profile'] = safe_profile
    st.session_state['last_seen_user_id'] = current_user_id

prof = st.session_state.get('user_db_profile', {})

if 'orders' not in st.session_state: st.session_state.orders = []
if 'step' not in st.session_state: st.session_state.step = 1
if 'selected_types' not in st.session_state: st.session_state.selected_types = []
if 'temp_order' not in st.session_state: st.session_state.temp_order = {}
if 'show_error' not in st.session_state: st.session_state.show_error = False
if 'is_submitted' not in st.session_state: st.session_state.is_submitted = False
if 'validate_step2' not in st.session_state: st.session_state.validate_step2 = False
if 'scroll_up' not in st.session_state: st.session_state.scroll_up = False

for k in ['chk_parcels', 'chk_freight', 'chk_mail']:
    if k not in st.session_state: st.session_state[k] = False

def reset_form_state():
    st.session_state.step = 1
    st.session_state.selected_types = [] 
    st.session_state.temp_order = {}
    st.session_state.show_error = False
    st.session_state.is_submitted = False
    st.session_state.validate_step2 = False
    st.session_state.scroll_up = False
    st.session_state['last_seen_user_id'] = None 
    for k in ['comp_name', 'comp_addr', 'comp_pc', 'comp_city', 'cont_fn', 'cont_ln', 'cont_email', 'cont_phone', 'p_addr', 'p_zip', 'p_city', 'd_addr', 'd_zip', 'd_city']:
        if k in st.session_state: del st.session_state[k]

if "reset" in st.query_params:
    reset_form_state()
    st.query_params.clear()
    st.rerun()

# =========================================================
# 4. NAVBAR (Met ?lang= parameter)
# =========================================================
if st.session_state.get('user') is not None and 'company_name' in st.session_state:
    icoon = "<svg style='width:16px; height:16px; margin-right:8px; vertical-align:-2px; fill:currentColor;' viewBox='0 0 640 512'><path d='M224 256A128 128 0 1 0 224 0a128 128 0 1 0 0 256zm-45.7 48C79.8 304 0 383.8 0 482.3C0 498.7 13.3 512 29.7 512H322.8c-3.1-8.8-3.7-18.4-1.4-27.8l15-60.1c2.8-11.3 8.6-21.5 16.8-29.7l40.3-40.3c-32.4-31.6-78-50.1-126.5-50.1H178.3zm212.8-38.1l-40.3 40.3c-15.9 15.9-27.2 35.8-32.5 57.2l-15 60.1c-1.3 5.3-.2 10.9 3.1 15.3s8.5 7.1 14 7.1H592c5.5 0 10.7-2.7 14-7.1s4.4-10 3.1-15.3l-15-60.1c-5.3-21.4-16.6-41.3-32.5-57.2l-40.3-40.3c-23.4-23.4-60.6-23.4-84 0zM456 432c-13.3 0-24-10.7-24-24s10.7-24 24-24s24 10.7 24 24s-10.7 24-24 24z'/></svg>"
    knop_tekst = f"{icoon}{st.session_state.company_name}"
else:
    knop_tekst = t['nav_portal']

html_navbar = f"""
<div class="navbar">
<div class="nav-logo"><a href="/?lang={lang}&reset=true" target="_self"><img src="https://cloud-1de12d.becdn.net/media/original/964295c9ae8e693f8bb4d6b70862c2be/logo-website-top-png-1-.webp"></a></div>
<div class="nav-links">
<a href="/?lang={lang}&reset=true" target="_self"><span>{t['nav_home']}</span></a>
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
<a href="/?lang={lang}&reset=true" target="_self" class="cta-btn">{t['nav_contact_btn']}</a>
</div>
</div>
"""
st.markdown(html_navbar, unsafe_allow_html=True)

# =========================================================
# ROUTING & PRIJS LOGICA
# =========================================================
@st.cache_data(ttl=3600, show_spinner=False)
def get_coordinates(address_string):
    if len(address_string) < 5: return None
    url = f"https://nominatim.openstreetmap.org/search?q={address_string}&format=json&limit=1"
    headers = {'User-Agent': 'DahleTransportApp/1.0'}
    try:
        resp = requests.get(url, headers=headers).json()
        if resp: return float(resp[0]['lat']), float(resp[0]['lon'])
    except: pass
    return None

@st.cache_data(ttl=3600, show_spinner=False)
def get_route_data(coord1, coord2):
    if not coord1 or not coord2: return None, None
    url = f"http://router.project-osrm.org/route/v1/driving/{coord1[1]},{coord1[0]};{coord2[1]},{coord2[0]}?overview=full&geometries=geojson"
    try:
        resp = requests.get(url).json()
        if resp.get("code") == "Ok":
            return resp["routes"][0]["distance"] / 1000.0, resp["routes"][0]["geometry"]["coordinates"]
    except: pass
    return None, None

def get_live_price():
    total_price = 0
    breakdown = [] 
    total_price += 49
    breakdown.append((t['c_base'], 49))

    weight_cost, total_weight = 0, 0
    
    if "Parcels & Documents" in st.session_state.selected_types:
        w_p = st.session_state.get('pd_weight', 1.0)
        total_weight += w_p
        weight_cost += (w_p * 8)
        if st.session_state.get('pd_oversized', False): weight_cost += 150 
            
    if "Cargo & Freight" in st.session_state.selected_types:
        w_f = st.session_state.get('cf_weight', 100)
        total_weight += w_f
        weight_cost += (w_f * 3) 
        if st.session_state.get('cf_pal', False): weight_cost += 250
        if st.session_state.get('cf_full', False): weight_cost += 2500
        if st.session_state.get('cf_lc', False): weight_cost += 100

    if "Mail & Direct Marketing" in st.session_state.selected_types:
        w_m = st.session_state.get('mdm_weight', 0.5)
        total_weight += w_m
        weight_cost += (w_m * 15)

    if weight_cost > 0:
        total_price += weight_cost
        breakdown.append((f"{t['c_hw']} ({total_weight}kg)", weight_cost))

    p_addr, p_city = str(st.session_state.get('p_addr') or '').strip(), str(st.session_state.get('p_city') or '').strip()
    d_addr, d_city = str(st.session_state.get('d_addr') or '').strip(), str(st.session_state.get('d_city') or '').strip()

    if len(p_addr) > 3 and len(p_city) > 2 and len(d_addr) > 3 and len(d_city) > 2:
        pick_coords = get_coordinates(f"{p_addr}, {st.session_state.get('p_zip', '')} {p_city}")
        del_coords = get_coordinates(f"{d_addr}, {st.session_state.get('d_zip', '')} {d_city}")
        
        if pick_coords and del_coords:
            dist_pick_del, _ = get_route_data(pick_coords, del_coords)
            if dist_pick_del is not None:
                transport_cost = dist_pick_del * 12 
                total_price += transport_cost
                breakdown.append((f"{t['c_tr']} ({dist_pick_del:.0f} km)", transport_cost))
                st.session_state.is_worldwide = False
            else:
                ww_cost = 2500 + (total_weight * 55)
                total_price += ww_cost
                breakdown.append((f"{t['c_ww']} ({total_weight}kg)", ww_cost))
                st.session_state.is_worldwide = True
        else: breakdown.append((t['c_src'], 0))
    elif st.session_state.step > 1: breakdown.append((t['c_aw'], 0))

    return total_price, breakdown

# =========================================================
# DE WEBSITE LOGICA
# =========================================================
s = st.session_state.step
def get_class(num): return "completed" if s > num else "active" if s == num else "inactive"
tracker_html = f"""<div class="step-wrapper"><div class="step-item {get_class(1)}"><div class="step-circle">1</div><div class="step-label">{t['st1']}</div></div><div class="step-line {"line-completed" if s > 1 else ""}"></div><div class="step-item {get_class(2)}"><div class="step-circle">2</div><div class="step-label">{t['st2']}</div></div><div class="step-line {"line-completed" if s > 2 else ""}"></div><div class="step-item {get_class(3)}"><div class="step-circle">3</div><div class="step-label">{t['st3']}</div></div></div>"""
st.markdown(tracker_html, unsafe_allow_html=True)
st.write("") 

if st.session_state.step == 1:
    col_spacer_L, col_main, col_spacer_R = st.columns([1, 6, 1])
    with col_main:
        dynamic_css = ""
        if st.session_state.get('chk_parcels'): dynamic_css += '''div[data-testid="stColumn"]:nth-child(1) div[data-testid="stVerticalBlockBorderWrapper"] { background-color: #ffffff !important; border: 2px solid #ffffff !important; transform: translateY(-5px); box-shadow: 0 10px 30px rgba(255,255,255,0.15) !important; } div[data-testid="stColumn"]:nth-child(1) div[data-testid="stVerticalBlockBorderWrapper"] * { color: #111111 !important; } div[data-testid="stColumn"]:nth-child(1) div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stCheckbox"] label span[role="checkbox"] { background-color: #894b9d !important; border-color: #894b9d !important; }'''
        if st.session_state.get('chk_freight'): dynamic_css += '''div[data-testid="stColumn"]:nth-child(2) div[data-testid="stVerticalBlockBorderWrapper"] { background-color: #ffffff !important; border: 2px solid #ffffff !important; transform: translateY(-5px); box-shadow: 0 10px 30px rgba(255,255,255,0.15) !important; } div[data-testid="stColumn"]:nth-child(2) div[data-testid="stVerticalBlockBorderWrapper"] * { color: #111111 !important; } div[data-testid="stColumn"]:nth-child(2) div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stCheckbox"] label span[role="checkbox"] { background-color: #894b9d !important; border-color: #894b9d !important; }'''
        if st.session_state.get('chk_mail'): dynamic_css += '''div[data-testid="stColumn"]:nth-child(3) div[data-testid="stVerticalBlockBorderWrapper"] { background-color: #ffffff !important; border: 2px solid #ffffff !important; transform: translateY(-5px); box-shadow: 0 10px 30px rgba(255,255,255,0.15) !important; } div[data-testid="stColumn"]:nth-child(3) div[data-testid="stVerticalBlockBorderWrapper"] * { color: #111111 !important; } div[data-testid="stColumn"]:nth-child(3) div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stCheckbox"] label span[role="checkbox"] { background-color: #894b9d !important; border-color: #894b9d !important; }'''
        if dynamic_css: st.markdown(f"<style>{dynamic_css}</style>", unsafe_allow_html=True)

        st.markdown(f"<h3 style='text-align: center; margin-bottom: 5px;'>{t['t_match']}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: #888; margin-bottom: 30px;'>{t['t_sub']}</p>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        with c1:
            with st.container(border=True):
                st.checkbox(t['b1_t'], key="chk_parcels")
                st.markdown(f"""<span style="display: inline-block; padding: 4px 12px; border: 1px solid #666; border-radius: 20px; font-size: 12px; color: #ccc; margin-bottom: 20px;">{t['b1_s']}</span><ul style="font-size: 14px; color: #bbb; line-height: 1.6; padding-left: 20px; margin-bottom: 30px; min-height: 80px;"><li>{t['b1_l1']}</li><li>{t['b1_l2']}</li></ul><div style="text-align: center; font-size: 12px; color: #aaa; border-top: 1px solid #444; padding-top: 20px; margin-top: 30px;">{t['b_com']}<div style="font-size: 32px; margin-top: 10px; display: flex; gap: 20px; justify-content: center;">✉️ 📦 📚</div></div>""", unsafe_allow_html=True)
        with c2:
            with st.container(border=True):
                st.checkbox(t['b2_t'], key="chk_freight")
                st.markdown(f"""<span style="display: inline-block; padding: 4px 12px; border: 1px solid #666; border-radius: 20px; font-size: 12px; color: #ccc; margin-bottom: 20px;">{t['b2_s']}</span><ul style="font-size: 14px; color: #bbb; line-height: 1.6; padding-left: 20px; margin-bottom: 30px; min-height: 80px;"><li>{t['b2_l1']}</li><li>{t['b2_l2']}</li></ul><div style="text-align: center; font-size: 12px; color: #aaa; border-top: 1px solid #444; padding-top: 20px; margin-top: 30px;">{t['b_com']}<div style="font-size: 32px; margin-top: 10px; display: flex; gap: 20px; justify-content: center;">🚛 🏗️</div></div>""", unsafe_allow_html=True)
        with c3:
            with st.container(border=True):
                st.checkbox(t['b3_t'], key="chk_mail")
                st.markdown(f"""<span style="display: inline-block; padding: 4px 12px; border: 1px solid #666; border-radius: 20px; font-size: 12px; color: #ccc; margin-bottom: 20px;">{t['b3_s']}</span><ul style="font-size: 14px; color: #bbb; line-height: 1.6; padding-left: 20px; margin-bottom: 30px; min-height: 80px;"><li>{t['b3_l1']}</li><li>{t['b3_l2']}</li></ul><div style="text-align: center; font-size: 12px; color: #aaa; border-top: 1px solid #444; padding-top: 20px; margin-top: 30px;">{t['b_com']}<div style="font-size: 32px; margin-top: 10px; display: flex; gap: 20px; justify-content: center;">📭 📄</div></div>""", unsafe_allow_html=True)

        if st.session_state.show_error: st.markdown(f"<p style='text-align: center; color: #ff4b4b; font-weight: bold; margin-top: 20px;'>{t['err_sel']}</p>", unsafe_allow_html=True)
        else: st.write("") 
            
        st.markdown(f"<p style='text-align: center; color: #888; font-size: 13px; margin-bottom: 15px;'>{t['time_est']}</p>", unsafe_allow_html=True)
        
        c_btn1, c_btn2, c_btn3 = st.columns([1, 2, 1])
        with c_btn2:
            if st.button(t['btn_next'], type="primary", use_container_width=True):
                selected = []
                if st.session_state.get('chk_parcels'): selected.append("Parcels & Documents")
                if st.session_state.get('chk_freight'): selected.append("Cargo & Freight")
                if st.session_state.get('chk_mail'): selected.append("Mail & Direct Marketing")
                if not selected:
                    st.session_state.show_error = True
                    st.rerun()
                else:
                    st.session_state.show_error = False
                    st.session_state.selected_types = selected
                    st.session_state.step = 2
                    st.rerun()

else:
    st.markdown("""<style> div[data-testid="column"]:nth-of-type(3), div[data-testid="stColumn"]:nth-of-type(3) { position: -webkit-sticky !important; position: sticky !important; top: 110px !important; align-self: flex-start !important; z-index: 100; } .step2-panel div[data-testid="stCheckbox"] { justify-content: flex-start; margin-bottom: 5px; position: static; height: auto;} .step2-panel div[data-testid="stCheckbox"] label { display: flex; width: auto; height: auto;} .step2-panel div[data-testid="stCheckbox"] label span[role="checkbox"] { position: static; transform: scale(1.0); margin-right: 10px; border-width: 1px;} .step2-panel div[data-testid="stCheckbox"] label p { display: block; font-size: 14px !important; } .step2-panel button[kind="tertiary"] { color: #888 !important; padding: 0px !important; min-height: 0px !important; margin-top: 15px !important; font-size: 16px !important; } .step2-panel button[kind="tertiary"]:hover { color: #ff4b4b !important; background-color: transparent !important; } .step2-panel div[role="radiogroup"] { gap: 0.5rem; } </style>""", unsafe_allow_html=True)
    st.markdown("<div id='error-top'></div>", unsafe_allow_html=True)
    if st.session_state.get('scroll_up', False):
        st.components.v1.html("""<script>const doc = window.parent.document; const el = doc.getElementById("error-top"); if(el) { el.scrollIntoView({behavior: "smooth"}); }</script>""", height=0)
        st.session_state.scroll_up = False 
    
    def req_lbl(key, base_text):
        if st.session_state.validate_step2 and not str(st.session_state.get(key) or "").strip(): return f"{base_text} 🚨 :red[(Required)]"
        return base_text
    def email_lbl():
        base = t['c_em']
        if st.session_state.validate_step2:
            val = str(st.session_state.get('cont_email') or "")
            if not val.strip() or "@" not in val: return f"{base} 🚨 :red[(Required)]"
        return base

    col_spacer_L, col_main, col_calc, col_spacer_R = st.columns([0.5, 6, 2.5, 0.5], gap="large")
    
    with col_main:
        if st.session_state.step == 2:
            st.markdown("<div class='step2-panel'>", unsafe_allow_html=True)
            if not st.session_state.selected_types: st.session_state.step = 1; st.rerun()

            cols = st.columns(len(st.session_state.selected_types))
            for i, sel in enumerate(st.session_state.selected_types[:]):
                with cols[i]:
                    with st.container(border=True):
                        c_title, c_close = st.columns([8, 1])
                        
                        disp_title = t['b1_t'] if sel=="Parcels & Documents" else t['b2_t'] if sel=="Cargo & Freight" else t['b3_t']
                        with c_title: st.markdown(f"#### {disp_title}")
                        with c_close:
                            if st.button("✖", key=f"btn_close_{sel}", type="tertiary"):
                                st.session_state.selected_types.remove(sel)
                                if sel == "Parcels & Documents": st.session_state.chk_parcels = False
                                if sel == "Cargo & Freight": st.session_state.chk_freight = False
                                if sel == "Mail & Direct Marketing": st.session_state.chk_mail = False
                                st.session_state.validate_step2 = False; st.rerun() 

                        if sel == "Parcels & Documents":
                            st.number_input(t['w_tot'], min_value=0.5, step=0.5, value=st.session_state.get('pd_weight', 1.0), key="pd_weight")
                            st.checkbox(t['w_over'], value=st.session_state.get('pd_oversized', False), key="pd_oversized")
                        elif sel == "Cargo & Freight":
                            cf_lbl = t['l_type']
                            if st.session_state.validate_step2 and not (st.session_state.get('cf_pal') or st.session_state.get('cf_full') or st.session_state.get('cf_lc')): cf_lbl += t['l_err']
                            st.markdown(cf_lbl)
                            st.checkbox(t['l_pal'], value=st.session_state.get('cf_pal', False), key="cf_pal")
                            st.checkbox(t['l_full'], value=st.session_state.get('cf_full', False), key="cf_full")
                            st.checkbox(t['l_lc'], value=st.session_state.get('cf_lc', False), key="cf_lc")
                            st.number_input(t['w_est'], min_value=50, step=50, value=st.session_state.get('cf_weight', 100), key="cf_weight")
                        elif sel == "Mail & Direct Marketing":
                            st.number_input(t['w_tot'], min_value=0.1, step=0.1, value=st.session_state.get('mdm_weight', 0.5), key="mdm_weight")
                            
            st.markdown("</div>", unsafe_allow_html=True)
            st.write("")
            
            with st.container(border=True):
                st.markdown(f"<h3 style='margin-top: 0px;'>{t['c_det']}</h3>", unsafe_allow_html=True)
                st.write("---")
                c_form_left, c_form_right = st.columns(2, gap="large")
                
                with c_form_left:
                    st.text_input(req_lbl("comp_name", t['c_name']), value=prof.get('comp_name', ''), key="comp_name", max_chars=100)
                    st.text_input(t['c_reg'], key="comp_reg", max_chars=50)
                    st.text_input(req_lbl("comp_addr", t['c_addr']), value=prof.get('comp_addr', ''), key="comp_addr", max_chars=150)
                    c_pc, c_city = st.columns(2)
                    with c_pc: st.text_input(req_lbl("comp_pc", t['c_zip']), value=prof.get('comp_pc', ''), key="comp_pc", max_chars=20)
                    with c_city: st.text_input(req_lbl("comp_city", t['c_city']), value=prof.get('comp_city', ''), key="comp_city", max_chars=100)
                    st.text_input(req_lbl("comp_country", t['c_ctry']), value="Norway", key="comp_country", max_chars=100)
    
                with c_form_right:
                    c_fn, c_ln = st.columns(2)
                    with c_fn: st.text_input(req_lbl("cont_fn", t['c_fn']), value=prof.get('cont_fn', ''), key="cont_fn", max_chars=50)
                    with c_ln: st.text_input(req_lbl("cont_ln", t['c_ln']), value=prof.get('cont_ln', ''), key="cont_ln", max_chars=50)
                    st.text_input(email_lbl(), value=prof.get('cont_email', ''), key="cont_email", max_chars=150)
                    
                    phone_lbl = t['c_ph']
                    if st.session_state.validate_step2 and not str(st.session_state.get('cont_phone') or '').strip(): phone_lbl += " 🚨 <span style='color:#ff4b4b;'>(Required)</span>"
                    st.markdown(f"<label style='font-size: 14px; font-weight: 600; color: #ccc;'>{phone_lbl}</label>", unsafe_allow_html=True)
                    c_code, c_phone = st.columns([1, 3])
                    with c_code: st.selectbox("Code", ["+47", "+46", "+45", "+31", "+44"], label_visibility="collapsed", key="cont_code")
                    with c_phone: st.text_input("Phone", value=prof.get('cont_phone', ''), label_visibility="collapsed", key="cont_phone", max_chars=20)
    
                st.write("")
                st.markdown(f"<h3 style='margin-top: 20px;'>{t['r_info']}</h3>", unsafe_allow_html=True)
                st.write("---")
                c_route_left, c_route_right = st.columns(2, gap="large")
                with c_route_left:
                    st.markdown(f"**{t['r_pick']}**")
                    st.text_input(req_lbl("p_addr", t['r_str']), value=prof.get('p_addr', ''), key="p_addr", max_chars=150)
                    c_p_zip, c_p_city = st.columns(2)
                    with c_p_zip: st.text_input(req_lbl("p_zip", t['c_zip']), value=prof.get('p_zip', ''), key="p_zip", max_chars=20)
                    with c_p_city: st.text_input(req_lbl("p_city", t['c_city']), value=prof.get('p_city', ''), key="p_city", max_chars=100)
                with c_route_right:
                    st.markdown(f"**{t['r_del']}**")
                    st.text_input(req_lbl("d_addr", t['r_str']), value=prof.get('d_addr', ''), key="d_addr", max_chars=150)
                    c_d_zip, c_d_city = st.columns(2)
                    with c_d_zip: st.text_input(req_lbl("d_zip", t['c_zip']), value=prof.get('d_zip', ''), key="d_zip", max_chars=20)
                    with c_d_city: st.text_input(req_lbl("d_city", t['c_city']), value=prof.get('d_city', ''), key="d_city", max_chars=100)
                    
                st.write("")
                
                # MAP
                p_addr_map = str(st.session_state.get('p_addr') or '').strip()
                p_city_map = str(st.session_state.get('p_city') or '').strip()
                d_addr_map = str(st.session_state.get('d_addr') or '').strip()
                d_city_map = str(st.session_state.get('d_city') or '').strip()
                p_coords = get_coordinates(f"{p_addr_map}, {st.session_state.get('p_zip', '')} {p_city_map}") if len(p_addr_map)>3 and len(p_city_map)>2 else None
                d_coords = get_coordinates(f"{d_addr_map}, {st.session_state.get('d_zip', '')} {d_city_map}") if len(d_addr_map)>3 and len(d_city_map)>2 else None
                
                if p_coords or d_coords:
                    layers, points = [], []
                    if p_coords: points.append({"pos": [p_coords[1], p_coords[0]], "name": "Pickup"})
                    if d_coords: points.append({"pos": [d_coords[1], d_coords[0]], "name": "Delivery"})
                    layers.append(pdk.Layer("ScatterplotLayer", data=points, get_position="pos", get_color=[137, 75, 157, 255], get_radius=1000, radius_min_pixels=6, radius_max_pixels=15))
                    
                    if p_coords and d_coords:
                        _, route_geom = get_route_data(p_coords, d_coords)
                        if route_geom:
                            layers.append(pdk.Layer("PathLayer", data=[{"path": route_geom}], get_path="path", get_color=[137, 75, 157, 200], width_scale=20, width_min_pixels=3, get_width=5))
                            pitch = 20 
                        else:
                            layers.append(pdk.Layer("ArcLayer", data=[{"source": [p_coords[1], p_coords[0]], "target": [d_coords[1], d_coords[0]]}], get_source_position="source", get_target_position="target", get_source_color=[137, 75, 157, 200], get_target_color=[137, 75, 157, 200], get_width=3, get_tilt=15))
                            pitch = 45
                        center_lat, center_lon, zoom = (p_coords[0]+d_coords[0])/2, (p_coords[1]+d_coords[1])/2, 3.5 
                    else:
                        center_lat, center_lon, zoom, pitch = p_coords[0] if p_coords else d_coords[0], p_coords[1] if p_coords else d_coords[1], 10, 0
                    st.pydeck_chart(pdk.Deck(layers=layers, initial_view_state=pdk.ViewState(latitude=center_lat, longitude=center_lon, zoom=zoom, pitch=pitch)))
                else: st.markdown(f"<div style='height: 250px; background-color: #1a1a1c; border: 1px solid #333; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #666; font-size: 13px;'>{t['m_wait']}</div>", unsafe_allow_html=True)
                
                st.write("---")
                st.text_area(t['a_info'], placeholder=t['a_ph'], max_chars=300, key="cont_info")

            st.write("")
            st.markdown(f"<p style='text-align: center; color: #888; font-size: 13px; margin-bottom: 30px;'>{t['p_note']}</p>", unsafe_allow_html=True)
            
            error_container = st.empty()
            missing_fields = False
            for rk in ['comp_name', 'comp_addr', 'comp_pc', 'comp_city', 'cont_fn', 'cont_ln', 'cont_email', 'cont_phone', 'comp_country', 'p_addr', 'p_zip', 'p_city', 'd_addr', 'd_zip', 'd_city']:
                if not str(st.session_state.get(rk) or '').strip(): missing_fields = True; break
            if "Cargo & Freight" in st.session_state.selected_types and not (st.session_state.get('cf_pal') or st.session_state.get('cf_full') or st.session_state.get('cf_lc')): missing_fields = True
            email_val = str(st.session_state.get('cont_email') or '').strip()
            invalid_email = bool(email_val and "@" not in email_val)

            if st.session_state.validate_step2:
                if missing_fields: error_container.error(t['e_req'])
                elif invalid_email: error_container.error(t['e_em'])

            c_back, c_next = st.columns([1, 4])
            if c_back.button(t['b_back'], type="secondary", use_container_width=True):
                st.session_state.step = 1; st.session_state.validate_step2 = False; st.rerun()
                
            if c_next.button(t['b_cont'], type="primary", use_container_width=True):
                st.session_state.validate_step2 = True 
                if missing_fields or invalid_email:
                    st.session_state.scroll_up = True; st.rerun()
                else:
                    st.session_state.validate_step2 = False; st.session_state.scroll_up = False
                    specs_list = []
                    is_ww = st.session_state.get('is_worldwide', False)
                    reg_txt = "Worldwide" if is_ww else "Domestic/European"
                    
                    if "Parcels & Documents" in st.session_state.selected_types:
                        sz = "Oversized" if st.session_state.get('pd_oversized') else "Standard"
                        specs_list.append(f"📦 {t['b1_t']}: {st.session_state.get('pd_weight', 1)}kg ({sz}) ➔ {reg_txt}")
                    if "Cargo & Freight" in st.session_state.selected_types:
                        loads = []
                        if st.session_state.get('cf_pal'): loads.append(t['l_pal'])
                        if st.session_state.get('cf_full'): loads.append(t['l_full'])
                        if st.session_state.get('cf_lc'): loads.append(t['l_lc'])
                        specs_list.append(f"🚛 {t['b2_t']}: {', '.join(loads)} | {st.session_state.get('cf_weight', 100)}kg ➔ {reg_txt}")
                    if "Mail & Direct Marketing" in st.session_state.selected_types:
                        specs_list.append(f"📭 {t['b3_t']}: {st.session_state.get('mdm_weight', 0.5)}kg ➔ {reg_txt}")
                    
                    db_info = "\n".join([s.replace("**", "") for s in specs_list])
                    if str(st.session_state.get('cont_info', '')).strip(): db_info += f"\n\nNotes: {str(st.session_state.get('cont_info')).strip()}"
                    
                    calc_price, calc_breakdown = get_live_price()
                    
                    st.session_state.temp_order = {
                        "company": st.session_state.get('comp_name', ''), "reg_no": st.session_state.get('comp_reg', ''),
                        "address": f"{st.session_state.get('comp_addr', '')}, {st.session_state.get('comp_pc', '')} {st.session_state.get('comp_city', '')}, {st.session_state.get('comp_country', '')}",
                        "contact_name": f"{st.session_state.get('cont_fn', '')} {st.session_state.get('cont_ln', '')}", "email": st.session_state.get('cont_email', ''), "phone": f"{st.session_state.get('cont_code', '')} {st.session_state.get('cont_phone', '')}",
                        "info_notes": str(st.session_state.get('cont_info', '')).strip(), "specs_list": specs_list, "db_info": db_info, "types": st.session_state.selected_types,
                        "pickup_address": st.session_state.get('p_addr', ''), "pickup_zip": st.session_state.get('p_zip', ''), "pickup_city": st.session_state.get('p_city', ''),
                        "delivery_address": st.session_state.get('d_addr', ''), "delivery_zip": st.session_state.get('d_zip', ''), "delivery_city": st.session_state.get('d_city', ''),
                        "price": calc_price, "price_breakdown": calc_breakdown
                    }
                    st.session_state.step = 3; st.rerun()

        elif st.session_state.step == 3:
            o = st.session_state.temp_order
            st.markdown(f"<h3 style='margin-top: 0px;'>{t['rev_t']}</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #888; font-size: 14px; margin-bottom: 20px;'>{t['rev_s']}</p>", unsafe_allow_html=True)
            
            with st.container(border=True):
                st.markdown(f"#### {t['rev_c']}")
                st.write("---")
                col_s1, col_s2 = st.columns(2)
                with col_s1:
                    st.markdown(f"<span style='color:#888; font-size:12px;'>{t['l_cn']}</span><br><b>{o['company']}</b>", unsafe_allow_html=True)
                    st.write("")
                    if o['reg_no']: st.markdown(f"<span style='color:#888; font-size:12px;'>{t['l_rn']}</span><br><b>{o['reg_no']}</b>", unsafe_allow_html=True)
                    st.write("")
                    st.markdown(f"<span style='color:#888; font-size:12px;'>{t['l_ad']}</span><br><b>{o['address']}</b>", unsafe_allow_html=True)
                with col_s2:
                    st.markdown(f"<span style='color:#888; font-size:12px;'>{t['l_cp']}</span><br><b>{o['contact_name']}</b>", unsafe_allow_html=True)
                    st.write("")
                    st.markdown(f"<span style='color:#888; font-size:12px;'>{t['l_em']}</span><br><b>{o['email']}</b>", unsafe_allow_html=True)
                    st.write("")
                    st.markdown(f"<span style='color:#888; font-size:12px;'>{t['l_ph']}</span><br><b>{o['phone']}</b>", unsafe_allow_html=True)
            
            with st.container(border=True):
                st.markdown(f"#### {t['rev_r']}")
                st.write("---")
                col_s3, col_s4 = st.columns(2)
                with col_s3:
                    st.markdown(f"<div style='color:#b070c6; font-size:14px; font-weight:bold; margin-bottom: 10px;'>{t['r_pick'].upper()}</div>", unsafe_allow_html=True)
                    st.markdown(f"<span style='color:#888; font-size:12px;'>{t['l_str']}</span><br><b>{o.get('pickup_address', '-')}</b>", unsafe_allow_html=True)
                    st.write("")
                    st.markdown(f"<span style='color:#888; font-size:12px;'>{t['l_zc']}</span><br><b>{o.get('pickup_zip', '-')} {o.get('pickup_city', '-')}</b>", unsafe_allow_html=True)
                with col_s4:
                    st.markdown(f"<div style='color:#b070c6; font-size:14px; font-weight:bold; margin-bottom: 10px;'>{t['r_del'].upper()}</div>", unsafe_allow_html=True)
                    st.markdown(f"<span style='color:#888; font-size:12px;'>{t['l_str']}</span><br><b>{o.get('delivery_address', '-')}</b>", unsafe_allow_html=True)
                    st.write("")
                    st.markdown(f"<span style='color:#888; font-size:12px;'>{t['l_zc']}</span><br><b>{o.get('delivery_zip', '-')} {o.get('delivery_city', '-')}</b>", unsafe_allow_html=True)
            
            with st.container(border=True):
                st.markdown(f"#### {t['rev_s']}")
                st.write("---")
                for spec in o['specs_list']: st.markdown(spec)
                if o['info_notes']:
                    st.write("")
                    st.markdown(f"<span style='color:#888; font-size:12px;'>{t['l_no']}</span>", unsafe_allow_html=True)
                    st.info(o['info_notes'])
            
            st.write("")
            if not st.session_state.is_submitted:
                c_b1, c_b2 = st.columns([1, 4])
                with c_b1:
                    if st.button(t['b_edit'], type="secondary", use_container_width=True): st.session_state.step = 2; st.rerun()
                with c_b2:
                    if st.button(t['b_send'], type="primary", use_container_width=True):
                        db_order = {
                            "company": o['company'], "reg_no": o['reg_no'], "address": o['address'], "contact_name": o['contact_name'], "email": o['email'], "phone": o['phone'],
                            "info": o['db_info'], "types": ", ".join(o['types']), "status": "New", "received_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "pickup_address": o.get('pickup_address', ''), "pickup_zip": o.get('pickup_zip', ''), "pickup_city": o.get('pickup_city', ''),
                            "delivery_address": o.get('delivery_address', ''), "delivery_zip": o.get('delivery_zip', ''), "delivery_city": o.get('delivery_city', ''),
                            "price": o.get('price', 0)
                        }
                        if st.session_state.get('user'): db_order["user_id"] = st.session_state.user.id
                        try:
                            supabase.table("orders").insert(db_order).execute()
                            st.balloons()
                            st.session_state.is_submitted = True
                            st.rerun()
                        except Exception as e: st.error(t['db_err'])
            else:
                st.success(t['s_succ']); st.info(t['s_sub'])
                if st.button(t['b_new'], type="primary", use_container_width=True): reset_form_state(); st.rerun()

    with col_calc:
        if st.session_state.step == 3: current_price, breakdown_lines = st.session_state.temp_order.get('price', 0), st.session_state.temp_order.get('price_breakdown', [])
        else: current_price, breakdown_lines = get_live_price()
        
        receipt_items_html = ""
        for name, price in breakdown_lines:
            receipt_items_html += f"""<div style="display: flex; justify-content: space-between; font-size: 13px; color: #bbb; margin-bottom: 8px;"><span>{name}</span><span>{price:,.0f}</span></div>"""
            
        receipt_html = f"""<div class="receipt-card" style="background: #1a1a1c; border: 1px solid #333; border-radius: 12px; padding: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.3);"><div style="color: #ffffff; font-size: 15px; font-weight: 600; text-transform: uppercase; letter-spacing: 1.5px; border-bottom: 1px solid #333; padding-bottom: 12px; margin-bottom: 20px;">{t['calc_t']}</div>{receipt_items_html}<div style="border-bottom: 1px dashed #444; margin: 15px 0;"></div><div style="display: flex; justify-content: space-between; align-items: center;"><span style="font-size: 14px; font-weight: 600; color: #fff;">{t['c_tot']}</span><span style="font-size: 26px; font-weight: 700; color: #b070c6;">{current_price:,.0f} <span style="font-size:16px;">NOK</span></span></div><div style="text-align: right; font-size: 11px; color: #666; margin-top: 2px;">{t['c_vat']}</div></div>"""
        st.markdown(receipt_html, unsafe_allow_html=True)
