import streamlit as st
import time
import requests
import pandas as pd
import pydeck as pdk
from datetime import datetime
from supabase import create_client
import extra_streamlit_components as stx
import math

# --- PAGE CONFIG ---
st.set_page_config(page_title="Dahle Transport - Order", layout="wide", initial_sidebar_state="collapsed")

# =========================================================
# 1. DIRECTE CSS INJECTIE (MOCKUP THEME)
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
* { font-family: 'Montserrat', sans-serif; }

/* VERBERG STREAMLIT BRANDING */
[data-testid="collapsedControl"], [data-testid="stSidebar"], header[data-testid="stHeader"] { display: none !important; }
footer { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
div[class^="viewerBadge"] { display: none !important; }
.block-container { padding-top: 100px; padding-left: 2rem; padding-right: 2rem; max-width: 100%; }

/* NAVBAR CSS */
.navbar { position: fixed; top: 0; left: 0; width: 100%; height: 90px; background-color: white; z-index: 999; border-bottom: 1px solid #eaeaea; display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; padding: 0 40px; box-shadow: 0 2px 10px rgba(0,0,0,0.03); }
.nav-logo { display: flex; justify-content: flex-start; margin-left: 20px; }
.nav-logo a { display: inline-block; height: 48px; text-decoration: none; cursor: pointer; }
.nav-logo img { height: 100%; width: auto; display: block; transition: transform 0.2s ease-in-out; }
.nav-logo a:hover img { transform: scale(1.05); } 

/* DE LINK TEKSTEN IN HET MIDDEN */
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

/* VERTICALE STAPPEN (MOCKUP STYLE) */
.v-steps-container { display: flex; flex-direction: column; gap: 15px; padding-top: 10px; }
.v-step { display: flex; align-items: center; gap: 12px; font-size: 14px; font-weight: 600; color: #555; transition: 0.3s; padding: 8px 12px; border-radius: 8px;}
.v-step.active { background-color: #3b2848; color: #e0c2ed; }
.v-step.completed { color: #888; }
.v-circle { width: 26px; height: 26px; border-radius: 50%; display: flex; justify-content: center; align-items: center; background-color: #222; font-size: 12px; font-weight: 700; border: 1px solid #444;}
.v-step.active .v-circle { background-color: #894b9d; color: #fff; border-color: #894b9d; }
.v-step.completed .v-circle { background-color: #333; color: #aaa; border-color: #555;}

/* FORMULIEREN & CONTAINERS */
div[data-testid="stVerticalBlockBorderWrapper"] { background-color: #161618 !important; border: 1px solid #2e2e30 !important; border-radius: 12px !important; padding: 15px !important; }
div[data-baseweb="input"] > div, div[data-baseweb="select"] > div, div[data-baseweb="textarea"] > div { background-color: #222224 !important; border: 1px solid #333 !important; border-radius: 8px !important; }
div[data-baseweb="input"] input, div[data-baseweb="textarea"] textarea, div[data-baseweb="select"] div { color: #fff !important; }
label { color: #aaa !important; font-weight: 500; font-size: 13px !important; }
h3, h4 { color: #fff !important; font-weight: 600 !important; margin-bottom: 5px !important;}

/* KNOPPEN STYLING */
div.stButton > button[kind="primary"] { background: #894b9d !important; color: #ffffff !important; border: none !important; border-radius: 6px !important; padding: 12px 24px !important; font-weight: 600 !important; font-size: 14px !important; box-shadow: 0 4px 14px 0 rgba(137, 75, 157, 0.4) !important; transition: all 0.2s ease !important; width: 100% !important; white-space: nowrap !important; }
div.stButton > button[kind="primary"]:hover { background: #9d56b5 !important; transform: translateY(-2px) !important; box-shadow: 0 8px 24px rgba(137, 75, 157, 0.6) !important; }
div.stButton > button[kind="secondary"] { background: transparent !important; color: #fff !important; padding: 12px 24px !important; border-radius: 6px !important; font-weight: 600 !important; font-size: 14px !important; border: 1px solid #555 !important; transition: all 0.2s ease !important; width: 100% !important; white-space: nowrap !important; }
div.stButton > button[kind="secondary"]:hover { background: #333 !important; border-color: #888 !important; color: #fff !important; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 2. INIT COOKIE MANAGER & STATE DEFAULTS
# =========================================================
cookie_manager = stx.CookieManager()

if 'cookie_retry' not in st.session_state:
    st.session_state.cookie_retry = True
    loading = st.empty()
    loading.markdown("<h3 style='text-align: center; color: #888; margin-top: 150px;'>Verifying credentials...</h3>", unsafe_allow_html=True)
    time.sleep(0.3)
    loading.empty()
    st.rerun()

# --- TAAL GEHEUGEN (COOKIE LOGICA) ---
saved_lang = cookie_manager.get('dahle_lang')

if "lang" in st.query_params:
    url_lang = st.query_params["lang"]
    if url_lang in ["no", "en", "sv", "da"]:
        if url_lang != saved_lang:
            cookie_manager.set("dahle_lang", url_lang, key="set_lang_safe")
        st.session_state.language = url_lang
elif saved_lang and saved_lang in ["no", "en", "sv", "da"]:
    st.session_state.language = saved_lang
elif 'language' not in st.session_state:
    st.session_state.language = "no"

lang = st.session_state.language 
lang_displays = { "no": "Norsk", "en": "English", "sv": "Svenska", "da": "Dansk" }
current_lang_display = lang_displays.get(lang, "Norsk")

default_keys = {
    'chk_parcels': False, 'chk_freight': False, 'chk_mail': False,
    'pd_weight': 0.0, 'pd_qty': 0, 'pd_oversized': False,
    'cf_pal': False, 'cf_pal_qty': 0, 'cf_pal_weight': 0.0,
    'cf_full': False, 'cf_full_qty': 0, 'cf_full_weight': 0.0,
    'cf_lc': False, 'cf_lc_qty': 0, 'cf_lc_weight': 0.0,
    'mdm_weight': 0.0, 'mdm_qty': 0,
    'req_sameday': False, 'req_ferry': False
}
for k, v in default_keys.items():
    if k not in st.session_state: st.session_state[k] = v

# =========================================================
# 3. HET ORDER WOORDENBOEK
# =========================================================
translations = {
    "no": {
        "nav_home": "Hjem", "nav_about": "Om oss", "nav_services": "Tjenester", "nav_gallery": "Galleri", "nav_contact": "Kontakt", 
        "menu_title": "Sider ⌄", "menu_dash": "Performance Dashboard", "menu_login": "Kundeportal", "menu_plan": "Intern Planner", "menu_order": "Ny bestilling",
        "nav_portal": "KUNDEPORTAL", "nav_contact_btn": "TA KONTAKT",
        "st1": "Velg Tjeneste", "st2": "Detaljer & Rute", "st3": "Se over", "st_title": "Bestillingssteg",
        "t_match": "Velg det du vanligvis sender for å finne riktig tjeneste.", "t_sub": "Velg minst ett alternativ for å fortsette",
        "b1_t": "Pakker & Dokumenter", "b1_s": "Typisk opptil 31.5kg", "b1_l1": "Lette til middels tunge sendinger", "b1_l2": "B2B/B2C", "b_com": "Vanlige sendinger:",
        "b2_t": "Gods & Frakt", "b2_s": "Typisk over 31.5kg+", "b2_l1": "Tyngre forsendelser (paller/containere)", "b2_l2": "B2B",
        "b3_t": "Post & Markedsføring", "b3_s": "Typisk opptil 2kg", "b3_l1": "Lette varer", "b3_l2": "Internasjonal post (brev, brosjyrer)",
        "err_sel": "❌ Vennligst velg minst ett alternativ.", "time_est": "Tar vanligvis under 5 minutter.", "btn_next": "Neste steg",
        "w_item": "Vekt per stk. (kg)", "w_over": "Overdimensjonert (Lengde > 3.5m)", "l_type": "Lasttype", "l_err": " 🚨 :red[(Velg minst én)]", "lbl_qty": "Antall", "lbl_wgt": "Totalvekt (kg)", "lbl_pcs": "stk", "l_pal": "Pall", "l_full": "Full container/lastebil", "l_lc": "Stykkgods", 
        "c_det": "Firma- & Kontaktdetaljer", "c_name": "Firmanavn *", "c_reg": "Foretaksregister (valgfritt)", "c_addr": "Firmaadresse *", "c_zip": "Postnr *", "c_city": "By *", "c_ctry": "Land *",
        "c_fn": "Fornavn *", "c_ln": "Etternavn *", "c_em": "Jobb-e-post *", "c_ph": "Telefon *",
        "r_info": "Ruteinformasjon", "r_pick": "Hentested (Fra)", "r_del": "Leveringssted (Til)", "r_str": "Gateadresse *",
        "delivery_opts": "Leveringsalternativer", "chk_same": "Express / Samme dag levering",
        "m_wait": "Skriv inn adresse for å beregne rute...", "a_info": "Tilleggsinformasjon (valgfritt)", 
        "a_ph": "F.eks spesielle krav ved levering...", 
        "e_req": "⚠️ Vennligst fyll ut alle obligatoriske felt (*) før du fortsetter.", "e_em": "⚠️ Ugyldig e-postadresse.",
        "e_wgt": "⚠️ Vennligst fyll inn vekt og antall (må være større enn 0).",
        "b_back": "Gå tilbake", "b_cont": "Fortsett til neste steg →",
        "rev_t": "Se over forespørselen", "rev_s": "Vennligst sjekk at detaljene stemmer.", "rev_c": "Firma & Kontakt",
        "l_cn": "FIRMANAVN", "l_rn": "ORG.NR", "l_ad": "ADRESSE", "l_cp": "KONTAKTPERSON", "l_em": "E-POST", "l_ph": "TELEFON", "l_str": "GATEADRESSE", "l_zc": "POSTNR & BY",
        "rev_r": "Rute", "rev_s_h": "Forsendelse", "l_no": "NOTATER", "b_edit": "Rediger detaljer", "b_send": "BEKREFT & SEND",
        "db_err": "⚠️ Feil: Kunne ikke lagre i databasen.", "s_succ": "Din forespørsel er sendt!", "s_sub": "Vi tar kontakt snart.", "b_new": "Start en ny forespørsel",
        "calc_t": "Estimert Kostnad", "c_tr": "Transport", "c_admin": "Administrasjon", "c_over": "Overdimensjonert (+25%)", "c_sameday": "Express levering", "c_ferry": "Bompenger", "c_tot": "Total", "c_vat": "Ekskl. MVA (VAT)",
        "w_reg": "Totalvekt", "qty_reg": "Registrert", "calc_note_pal": "Frakten er beregnet etter plass/antall.", "calc_note_we": "Frakten er beregnet etter totalvekt."
    },
    "en": {
        "nav_home": "Home", "nav_about": "About us", "nav_services": "Services", "nav_gallery": "Gallery", "nav_contact": "Contact", 
        "menu_title": "Pages ⌄", "menu_dash": "Performance Dashboard", "menu_login": "Customer Portal", "menu_plan": "Internal Planner", "menu_order": "New Order",
        "nav_portal": "CUSTOMER PORTAL", "nav_contact_btn": "CONTACT US",
        "st1": "Select Service", "st2": "Details & Route", "st3": "Review", "st_title": "Order Steps",
        "t_match": "To find your service match, select all that you ship.", "t_sub": "Select at least one option to continue",
        "b1_t": "Parcels & Documents", "b1_s": "Typically up to 31.5kg", "b1_l1": "Light to medium weight shipments", "b1_l2": "B2B/B2C", "b_com": "Commonly shipped:",
        "b2_t": "Cargo & Freight", "b2_s": "Typically over 31.5kg+", "b2_l1": "Heavier shipments (pallets/containers)", "b2_l2": "B2B",
        "b3_t": "Mail & Marketing", "b3_s": "Typically up to 2kg", "b3_l1": "Lightweight goods", "b3_l2": "International business mail",
        "err_sel": "❌ Please select at least one option.", "time_est": "Typically takes less than 5 minutes.", "btn_next": "Next Step",
        "w_item": "Weight per item (kg)", "w_over": "Oversized (Length > 3.5m)", "l_type": "Load Type", "l_err": " 🚨 :red[(Select at least one)]", "lbl_qty": "Quantity", "lbl_wgt": "Total weight (kg)", "lbl_pcs": "pcs", "l_pal": "Pallet", "l_full": "Full Container/Truck", "l_lc": "Loose Cargo", 
        "c_det": "Company & Contact Details", "c_name": "Company Name *", "c_reg": "Registration No. (optional)", "c_addr": "Company Address *", "c_zip": "Zip Code *", "c_city": "City *", "c_ctry": "Country *",
        "c_fn": "First Name *", "c_ln": "Last Name *", "c_em": "Work Email *", "c_ph": "Phone *",
        "r_info": "Route Information", "r_pick": "Pickup (From)", "r_del": "Delivery (To)", "r_str": "Street Address *",
        "delivery_opts": "Delivery Options", "chk_same": "Express / Same day delivery",
        "m_wait": "Enter address to map the route...", "a_info": "Additional Information (optional)", 
        "a_ph": "E.g. special requirements for delivery...", 
        "e_req": "⚠️ Please fill in all mandatory fields (*).", "e_em": "⚠️ Invalid email address.",
        "e_wgt": "⚠️ Please enter a valid weight and quantity (greater than 0).",
        "b_back": "Go Back", "b_cont": "Continue to Review →",
        "rev_t": "Review your request", "rev_s": "Please verify your details below.", "rev_c": "Company & Contact",
        "l_cn": "COMPANY NAME", "l_rn": "REG. NO", "l_ad": "ADDRESS", "l_cp": "CONTACT PERSON", "l_em": "EMAIL", "l_ph": "PHONE", "l_str": "STREET ADDRESS", "l_zc": "ZIP & CITY",
        "rev_r": "Route", "rev_s_h": "Shipment", "l_no": "NOTES", "b_edit": "Edit Details", "b_send": "CONFIRM & SEND",
        "db_err": "⚠️ Error: Failed to send to database.", "s_succ": "Request sent successfully!", "s_sub": "We will get in touch shortly.", "b_new": "Start a New Request",
        "calc_t": "Estimated Cost", "c_tr": "Freight", "c_admin": "Administration", "c_over": "Oversized (+25%)", "c_sameday": "Express Delivery", "c_ferry": "Toll", "c_tot": "Total", "c_vat": "Excl. MVA (VAT)",
        "w_reg": "Total weight", "qty_reg": "Registered", "calc_note_pal": "Freight is calculated by space/quantity.", "calc_note_we": "Freight is calculated by total weight."
    },
    "sv": {
        "nav_home": "Hem", "nav_about": "Om oss", "nav_services": "Tjänster", "nav_gallery": "Galleri", "nav_contact": "Kontakt", 
        "menu_title": "Sidor ⌄", "menu_dash": "Performance Dashboard", "menu_login": "Kundportal", "menu_plan": "Intern Planner", "menu_order": "Ny beställning",
        "nav_portal": "KUNDPORTAL", "nav_contact_btn": "KONTAKTA OSS",
        "st1": "Välj Tjänst", "st2": "Detaljer & Rutt", "st3": "Granska", "st_title": "Beställningssteg",
        "t_match": "Välj vad du brukar skicka för att hitta rätt tjänst.", "t_sub": "Välj minst ett alternativ för att fortsätta",
        "b1_t": "Paket & Dokument", "b1_s": "Vanligtvis upp till 31.5kg", "b1_l1": "Lätta till medeltunga försändelser", "b1_l2": "B2B/B2C", "b_com": "Vanliga försändelser:",
        "b2_t": "Gods & Frakt", "b2_s": "Vanligtvis över 31.5kg+", "b2_l1": "Tyngre försändelser (pallar/containrar)", "b2_l2": "B2B",
        "b3_t": "Post & Marknadsföring", "b3_s": "Vanligtvis upp till 2kg", "b3_l1": "Lätta varer", "b3_l2": "Internationell företagspost",
        "err_sel": "❌ Vänligen välj minst ett alternativ.", "time_est": "Tar vanligtvis under 5 minutter.", "btn_next": "Nästa steg",
        "w_item": "Vikt per styck (kg)", "w_over": "Överdimensionerad (Längd > 3.5m)", "l_type": "Lasttyp", "l_err": " 🚨 :red[(Välj minst en)]", "lbl_qty": "Antal", "lbl_wgt": "Totalvikt (kg)", "lbl_pcs": "st", "l_pal": "Pall", "l_full": "Full container/lastbil", "l_lc": "Styckgods", 
        "c_det": "Företags- & Kontaktdetaljer", "c_name": "Företagsnamn *", "c_reg": "Organisationsnummer (frivilligt)", "c_addr": "Företagsadress *", "c_zip": "Postnr *", "c_city": "Stad *", "c_ctry": "Land *",
        "c_fn": "Förnamn *", "c_ln": "Efternavn *", "c_em": "Jobb-e-post *", "c_ph": "Telefon *",
        "r_info": "Ruttinformation", "r_pick": "Upphämtning (Från)", "r_del": "Leveransplats (Till)", "r_str": "Gatuadress *",
        "delivery_opts": "Leveransalternativ", "chk_same": "Express / Samma dag leverans",
        "m_wait": "Ange adress för att beräkna rutten...", "a_info": "Ytterligare information (frivilligt)", 
        "a_ph": "T.ex. andra krav vid leverans...", 
        "e_req": "⚠️ Vänligen fyll i alla obligatoriska fält (*).", "e_em": "⚠️ Ogiltig e-postadress.",
        "e_wgt": "⚠️ Vänligen ange en giltig vikt och antal (större än 0).",
        "b_back": "Gå tillbaka", "b_cont": "Fortsätt till granskning →",
        "rev_t": "Granska din förfrågan", "rev_s": "Vänligen kontrollera dina uppgifter.", "rev_c": "Företag & Kontakt",
        "l_cn": "FÖRETAGSNAMN", "l_rn": "ORG.NR", "l_ad": "ADRESS", "l_cp": "KONTAKTPERSON", "l_em": "E-POST", "l_ph": "TELEFON", "l_str": "GATUADRESS", "l_zc": "POSTNR & STAD",
        "rev_r": "Rutt", "rev_s_h": "Försändelse", "l_no": "ANTECKNINGAR", "b_edit": "Redigera detaljer", "b_send": "BEKRÄFTA & SKICKA",
        "db_err": "⚠️ Fel: Kunde inte spara i databasen.", "s_succ": "Din förfrågan har skickats!", "s_sub": "Vi återkommer inom kort.", "b_new": "Starta en ny förfrågan",
        "calc_t": "Uppskattad Kostnad", "c_tr": "Transport", "c_admin": "Administration", "c_over": "Överdimensionerad (+25%)", "c_sameday": "Expressleverans", "c_ferry": "Vägavgift", "c_tot": "Totalt", "c_vat": "Exkl. Moms (VAT)",
        "w_reg": "Totalvikt", "qty_reg": "Registrerad", "calc_note_pal": "Frakten beräknas efter antal/plats.", "calc_note_we": "Frakten beräknas efter totalvikt."
    },
    "da": {
        "nav_home": "Hjem", "nav_about": "Om os", "nav_services": "Tjenester", "nav_gallery": "Galleri", "nav_contact": "Kontakt", 
        "menu_title": "Sider ⌄", "menu_dash": "Performance Dashboard", "menu_login": "Kundeportal", "menu_plan": "Intern Planner", "menu_order": "Ny bestilling",
        "nav_portal": "KUNDEPORTAL", "nav_contact_btn": "KONTAKT OS",
        "st1": "Vælg Tjeneste", "st2": "Detaljer & Rute", "st3": "Gennemgå", "st_title": "Bestillingsstrin",
        "t_match": "Vælg det du normalt sender, for at finde den rette tjeneste.", "t_sub": "Vælg mindst én mulighed for at fortsætte",
        "b1_t": "Pakker & Dokumenter", "b1_s": "Typisk op til 31.5kg", "b1_l1": "Lette til mellemtunge forsendelser", "b1_l2": "B2B/B2C", "b_com": "Almindelige forsendelser:",
        "b2_t": "Gods & Fragt", "b2_s": "Typisk over 31.5kg+", "b2_l1": "Tungere forsendelser (pallar/containere)", "b2_l2": "B2B",
        "b3_t": "Post & Markedsføring", "b3_s": "Typisk op til 2kg", "b3_l1": "Lette varer", "b3_l2": "International erhvervspost",
        "err_sel": "❌ Vælg venligst mindst én mulighed.", "time_est": "Tager typisk under 5 minutter.", "btn_next": "Næste trin",
        "w_item": "Vægt pr. stk. (kg)", "w_over": "Overdimensioneret (Længde > 3.5m)", "l_type": "Lasttype", "l_err": " 🚨 :red[(Vælg mindst én)]", "lbl_qty": "Antal", "lbl_wgt": "Totalvægt (kg)", "lbl_pcs": "stk", "l_pal": "Palle", "l_full": "Fuld container/lastbil", "l_lc": "Stykgods", 
        "c_det": "Firma- & Kontaktdetaljer", "c_name": "Firmanavn *", "c_reg": "CVR-nummer (valgfrit)", "c_addr": "Firmaadresse *", "c_zip": "Postnr *", "c_city": "By *", "c_ctry": "Land *",
        "c_fn": "Fornavn *", "c_ln": "Efternavn *", "c_em": "Arbejds-e-mail *", "c_ph": "Telefon *",
        "r_info": "Ruteinformation", "r_pick": "Afhentning (Fra)", "r_del": "Levering (Til)", "r_str": "Gadeadresse *",
        "delivery_opts": "Leveringsmuligheder", "chk_same": "Express / Samme dag levering",
        "m_wait": "Indtast adresse for at beregne rute...", "a_info": "Yderligere information (valgfrit)", 
        "a_ph": "F.eks. specielle krav ved levering...", 
        "e_req": "⚠️ Udfyld venligst alle obligatoriske felter (*).", "e_em": "⚠️ Ugyldig e-mailadresse.",
        "e_wgt": "⚠️ Indtast venligst en gyldig vægt og mængde (større end 0).",
        "b_back": "Gå tilbage", "b_cont": "Fortsæt til gennemgang →",
        "rev_t": "Gennemgå din anmodning", "rev_s": "Tjek venligst at dine oplysninger er korrekte.", "rev_c": "Firma & Kontakt",
        "l_cn": "FIRMANAVN", "l_rn": "CVR.NR", "l_ad": "ADRESS", "l_cp": "KONTAKTPERSON", "l_em": "E-MAIL", "l_ph": "TELEFON", "l_str": "GADEADRESSE", "l_zc": "POSTNR & BY",
        "rev_r": "Rute", "rev_s_h": "Forsendelse", "l_no": "NOTER", "b_edit": "Rediger detaljer", "b_send": "BEKRÄFT & SEND",
        "db_err": "⚠️ Fejl ved lagring i databasen.", "s_succ": "Din anmodning er sendt!", "s_sub": "Vi vender tilbage snarest.", "b_new": "Start en ny anmodning",
        "calc_t": "Estimeret Pris", "c_tr": "Transport", "c_admin": "Administration", "c_over": "Overdimensioneret (+25%)", "c_sameday": "Express levering", "c_ferry": "Bompenge", "c_tot": "Total", "c_vat": "Ekskl. Moms (VAT)",
        "w_reg": "Totalvægt", "qty_reg": "Registreret", "calc_note_pal": "Fragten er beregnet efter plads/antal.", "calc_note_we": "Fragten er beregnet efter totalvægt."
    }
}
t = translations[lang]

# =========================================================
# 4. DATABASE & AUTHENTICATIE
# =========================================================
def init_connection():
    return create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])

if 'supabase_client' not in st.session_state:
    try: st.session_state.supabase_client = init_connection()
    except Exception: pass
supabase = st.session_state.supabase_client

if 'user' not in st.session_state: st.session_state.user = None
if 'role' not in st.session_state: st.session_state.role = "guest"
acc_token, ref_token = cookie_manager.get('dahle_acc'), cookie_manager.get('dahle_ref')

if st.session_state.get('user') is None and acc_token and ref_token:
    try: st.session_state.user = supabase.auth.set_session(acc_token, ref_token).user
    except Exception: pass

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
                st.session_state.role = str(raw_prof.get("roles", "customer")).strip().lower()
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
is_employee = st.session_state.get('role') in ['admin', 'employee']

if 'orders' not in st.session_state: st.session_state.orders = []
if 'step' not in st.session_state: st.session_state.step = 1
if 'selected_types' not in st.session_state: st.session_state.selected_types = []
if 'temp_order' not in st.session_state: st.session_state.temp_order = {}
if 'show_error' not in st.session_state: st.session_state.show_error = False
if 'is_submitted' not in st.session_state: st.session_state.is_submitted = False
if 'validate_step2' not in st.session_state: st.session_state.validate_step2 = False
if 'scroll_up' not in st.session_state: st.session_state.scroll_up = False

def reset_form_state():
    st.session_state.step = 1; st.session_state.selected_types = []; st.session_state.temp_order = {}
    st.session_state.show_error = False; st.session_state.is_submitted = False; st.session_state.validate_step2 = False; st.session_state.scroll_up = False
    st.session_state['last_seen_user_id'] = None 
    for k in ['comp_name', 'comp_addr', 'comp_pc', 'comp_city', 'cont_fn', 'cont_ln', 'cont_email', 'cont_phone', 'p_addr', 'p_zip', 'p_city', 'd_addr', 'd_zip', 'd_city']:
        if k in st.session_state: del st.session_state[k]

if "reset" in st.query_params:
    reset_form_state()
    st.query_params.clear()
    st.rerun()

# =========================================================
# 5. NAVBAR SAMENSTELLEN 
# =========================================================
if st.session_state.get('user') is not None and 'company_name' in st.session_state:
    icoon = "<svg style='width:16px; height:16px; margin-right:8px; vertical-align:-2px; fill:currentColor;' viewBox='0 0 640 512'><path d='M224 256A128 128 0 1 0 224 0a128 128 0 1 0 0 256zm-45.7 48C79.8 304 0 383.8 0 482.3C0 498.7 13.3 512 29.7 512H322.8c-3.1-8.8-3.7-18.4-1.4-27.8l15-60.1c2.8-11.3 8.6-21.5 16.8-29.7l40.3-40.3c-32.4-31.6-78-50.1-126.5-50.1H178.3zm212.8-38.1l-40.3 40.3c-15.9 15.9-27.2 35.8-32.5 57.2l-15 60.1c-1.3 5.3-.2 10.9 3.1 15.3s8.5 7.1 14 7.1H592c5.5 0 10.7-2.7 14-7.1s4.4-10 3.1-15.3l-15-60.1c-5.3-21.4-16.6-41.3-32.5-57.2l-40.3-40.3c-23.4-23.4-60.6-23.4-84 0zM456 432c-13.3 0-24-10.7-24-24s10.7-24 24-24s24 10.7 24 24s-10.7 24-24 24z'/></svg>"
    knop_tekst = f"{icoon}{st.session_state.company_name}"
else:
    knop_tekst = t['nav_portal']

dropdown_links = f'<a href="/Login?lang={lang}" target="_self">{t["menu_login"]}</a>'
if is_employee:
    dropdown_links += f'<a href="/Dashboard?lang={lang}" target="_self">{t["menu_dash"]}</a><a href="/Planner?lang={lang}" target="_self">{t["menu_plan"]}</a>'

html_navbar = f"""
<div class="navbar"><div class="nav-logo"><a href="/?lang={lang}&reset=true" target="_self"><img src="https://cloud-1de12d.becdn.net/media/original/964295c9ae8e693f8bb4d6b70862c2be/logo-website-top-png-1-.webp"></a></div>
<div class="nav-links"><a href="/?lang={lang}&reset=true" target="_self"><span>{t['nav_home']}</span></a><span>{t['nav_about']}</span><span>{t['nav_services']}</span><span>{t['nav_gallery']}</span><span>{t['nav_contact']}</span>
<div class="nav-text-dropdown"><button class="nav-text-dropbtn">{t['menu_title']}</button><div class="nav-text-dropdown-content">{dropdown_links}</div></div></div>
<div class="nav-cta"><div class="lang-dropdown"><button class="lang-dropbtn">{current_lang_display} ⌄</button><div class="lang-dropdown-content"><a href="?lang=en" target="_self">English</a><a href="?lang=no" target="_self">Norsk</a><a href="?lang=sv" target="_self">Svenska</a><a href="?lang=da" target="_self">Dansk</a></div></div>
<a href="/Login?lang={lang}" target="_self" class="cta-btn-outline">{knop_tekst}</a><a href="/?lang={lang}&reset=true" target="_self" class="cta-btn-purple">{t['nav_contact_btn']}</a></div></div>
"""
st.markdown(html_navbar, unsafe_allow_html=True)

# =========================================================
# ROUTING, KAART & DAHLE PRIJS LOGICA
# =========================================================
@st.cache_data(ttl=3600, show_spinner=False)
def get_coordinates(street, zip_code, city):
    if len(city) < 2: return None
    headers = {'User-Agent': 'DahleTransportMap/17.0'}
    url = "https://nominatim.openstreetmap.org/search"
    queries = [f"{street}, {zip_code} {city}, Norway", f"{street}, {city}, Norway", f"{zip_code} {city}, Norway", f"{city}, Norway", f"{street}, {city}", f"{city}"]
    for q in queries:
        try:
            r = requests.get(url, params={'q': q, 'format': 'json', 'limit': 1}, headers=headers, timeout=2).json()
            if r: return float(r[0]['lat']), float(r[0]['lon'])
        except: continue
    return None

@st.cache_data(ttl=3600, show_spinner=False)
def get_route_data(coord1, coord2):
    if not coord1 or not coord2: return None, None
    url = f"https://router.project-osrm.org/route/v1/driving/{coord1[1]},{coord1[0]};{coord2[1]},{coord2[0]}?overview=full&geometries=geojson"
    try:
        resp = requests.get(url, timeout=3).json()
        if resp.get("code") == "Ok": return resp["routes"][0]["distance"] / 1000.0, resp["routes"][0]["geometry"]["coordinates"]
    except: pass
    return None, None

def calculate_zoom(coord1, coord2):
    if not coord1 or not coord2: return 4.0
    lat_diff = abs(coord1[0] - coord2[0])
    lon_diff = abs(coord1[1] - coord2[1])
    max_diff = max(lat_diff, lon_diff)
    
    if max_diff < 0.02: return 13.5
    if max_diff < 0.1:  return 11.0
    if max_diff < 0.5:  return 9.0
    if max_diff < 2.0:  return 7.5
    if max_diff < 5.0:  return 6.0
    return 4.5 

@st.cache_data(show_spinner=False)
def determine_zone(p_city, d_city):
    cities = (str(p_city).lower() + " " + str(d_city).lower())
    if any(c in cities for c in ['roan', 'osen', 'bessaker', 'refsnes', 'stokkøy', 'stokkoy', 'linesøya', 'linesoya']): return 3
    if any(c in cities for c in ['bjugn', 'brekstad', 'vallersund', 'lysøysund', 'lysoysund', 'åfjord', 'afjord']): return 2
    if any(c in cities for c in ['stadsbygd', 'rissa', 'hasselvika', 'fevåg', 'fevag', 'husbysjøen', 'husbysjoen', 'råkvåg', 'rakvag', 'leksvik', 'trondheim']): return 1
    return 4 

def check_if_ferry_needed(p_city, d_city):
    p = str(p_city).lower().strip()
    d = str(d_city).lower().strip()
    fosen_dests = ['roan', 'osen', 'bessaker', 'refsnes', 'stokkøy', 'stokkoy', 'linesøya', 'linesoya', 'bjugn', 'brekstad', 'vallersund', 'lysøysund', 'lysoysund', 'åfjord', 'afjord', 'stadsbygd', 'rissa', 'hasselvika', 'fevåg', 'fevag', 'husbysjøen', 'husbysjoen', 'råkvåg', 'rakvag', 'leksvik']
    if ('trondheim' in p and any(c in d for c in fosen_dests)) or ('trondheim' in d and any(c in p for c in fosen_dests)): return True
    return False

def get_live_price():
    total_weight = 0
    oversized = False
    reg_items = []
    
    if "Parcels & Documents" in st.session_state.selected_types:
        q = min(st.session_state.get('pd_qty', 0), 10000)
        w = min(st.session_state.get('pd_weight', 0.0), 35.0)
        if q > 0 and w > 0:
            total_weight += (w * q)
            reg_items.append(f"{q}x {t['b1_t']} ({w:g} kg)")
            if st.session_state.get('pd_oversized', False): oversized = True
        
    cargo_units = 0
    if "Cargo & Freight" in st.session_state.selected_types:
        if st.session_state.get('cf_pal'):
            pq = min(st.session_state.get('cf_pal_qty', 0), 33)
            pw = min(st.session_state.get('cf_pal_weight', 0.0), 1200.0)
            if pq > 0 and pw > 0:
                cargo_units += pq
                total_weight += pw
                reg_items.append(f"{pq}x {t['l_pal']} ({pw:g} kg)")
        if st.session_state.get('cf_full'):
            fq = min(st.session_state.get('cf_full_qty', 0), 10)
            fw = min(st.session_state.get('cf_full_weight', 0.0), 25000.0)
            if fq > 0 and fw > 0:
                cargo_units += fq * 33 
                total_weight += fw
                reg_items.append(f"{fq}x {t['l_full']} ({fw:g} kg)")
        if st.session_state.get('cf_lc'):
            lq = min(st.session_state.get('cf_lc_qty', 0), 1000)
            lw = min(st.session_state.get('cf_lc_weight', 0.0), 25000.0)
            if lq > 0 and lw > 0:
                cargo_units += lq
                total_weight += lw
                reg_items.append(f"{lq}x {t['l_lc']} ({lw:g} kg)")
            
    if "Mail & Direct Marketing" in st.session_state.selected_types:
        q = min(st.session_state.get('mdm_qty', 0), 100000)
        w = min(st.session_state.get('mdm_weight', 0.0), 2.0)
        if q > 0 and w > 0:
            total_weight += (w * q)
            reg_items.append(f"{q}x {t['b3_t']} ({w:g} kg)")

    if total_weight <= 0 and cargo_units <= 0:
        return 0, 0, 0, [(t['c_tr'], 0)], ""

    zone = determine_zone(st.session_state.get('p_city', ''), st.session_state.get('d_city', ''))
    
    prices = {
        1: [(24, 342), (49, 456), (99, 570), (149, 682), (199, 791), (399, 918), (599, 1225), (799, 1377), (999, 1530)],
        2: [(24, 362), (49, 478), (99, 588), (149, 716), (199, 825), (399, 963), (599, 1283), (799, 1443), (999, 1605)],
        3: [(24, 395), (49, 526), (99, 676), (149, 768), (199, 868), (399, 1058), (599, 1411), (799, 1587), (999, 1766)],
        4: [(24, 275), (49, 364), (99, 457), (149, 580), (199, 641), (399, 734), (599, 979), (799, 1100), (999, 1225)]
    }
    
    weight_cost = 0
    tier_lbl = ""
    if total_weight > 999:
        extra_weight = total_weight - 999
        steps = int((extra_weight - 0.001) / 100) + 1
        weight_cost = prices[zone][-1][1] + (steps * 100)
        tier_lbl = "> 999 kg"
    else:
        for max_w, price in prices[zone]:
            if total_weight <= max_w:
                weight_cost = price
                if max_w == 24: tier_lbl = "0-24 kg"
                elif max_w == 49: tier_lbl = "25-49 kg"
                elif max_w == 99: tier_lbl = "50-99 kg"
                elif max_w == 149: tier_lbl = "100-149 kg"
                elif max_w == 199: tier_lbl = "150-199 kg"
                elif max_w == 399: tier_lbl = "200-399 kg"
                elif max_w == 599: tier_lbl = "400-599 kg"
                elif max_w == 799: tier_lbl = "600-799 kg"
                elif max_w == 999: tier_lbl = "800-999 kg"
                break
        if weight_cost == 0: weight_cost = prices[zone][-1][1]; tier_lbl = "800-999 kg"

    space_cost = 0
    pallet_prices = {1: 700, 2: 750, 3: 800, 4: 600}
    if cargo_units > 0: space_cost = pallet_prices[zone] * cargo_units

    if space_cost > weight_cost:
        base_cost = space_cost
        lbl = f"{t['c_tr']} ({cargo_units} {t['lbl_pcs']})"
        calc_note = t['calc_note_pal']
    else:
        base_cost = weight_cost
        tier_lbl = "> 999 kg" if total_weight > 999 else f"{total_weight:g} kg"
        lbl = f"{t['c_tr']} ({tier_lbl})"
        calc_note = t['calc_note_we']

    cost = base_cost + 50 
    breakdown_lines = [(lbl, base_cost)]
    
    if reg_items:
        breakdown_lines.append((f"<span style='display:block; font-size:12px; color:#aaa; padding-left:10px; margin-top:-4px;'>↳ {t['qty_reg']}:</span>", ""))
        for item in reg_items: breakdown_lines.append((f"<span style='display:block; font-size:12px; color:#888; padding-left:25px; margin-top:-6px;'>• {item}</span>", ""))
            
    breakdown_lines.append((f"<span style='display:block; font-size:12px; color:#aaa; padding-left:10px; margin-top:-4px;'>↳ {t['w_reg']}: {total_weight:g} kg</span>", ""))
    breakdown_lines.append((t['c_admin'], 50))
    
    if oversized:
        surcharge = cost * 0.25
        cost += surcharge
        breakdown_lines.append((t['c_over'], surcharge))
    if st.session_state.get('req_sameday'):
        cost += 250
        breakdown_lines.append((t['c_sameday'], 250))
    if check_if_ferry_needed(st.session_state.get('p_city', ''), st.session_state.get('d_city', '')):
        cost += 250
        breakdown_lines.append((t['c_ferry'], 250))
        
    final_price = cost * 1.10
    profit = final_price - cost
    
    return final_price, cost, profit, breakdown_lines, calc_note

# =========================================================
# DE WEBSITE LOGICA (MOCKUP STIJL)
# =========================================================
s = st.session_state.step
def v_class(num): return "completed" if s > num else "active" if s == num else ""

if st.session_state.step == 1:
    c_spacer1, c_main, c_spacer2 = st.columns([2, 8, 2])
    with c_main:
        dynamic_css = ""
        if st.session_state.get('chk_parcels'): dynamic_css += '''div[data-testid="stColumn"]:nth-child(1) div[data-testid="stVerticalBlockBorderWrapper"] { background-color: #ffffff !important; border: 2px solid #ffffff !important; transform: translateY(-5px); box-shadow: 0 10px 30px rgba(255,255,255,0.15) !important; } div[data-testid="stColumn"]:nth-child(1) div[data-testid="stVerticalBlockBorderWrapper"] * { color: #111111 !important; } div[data-testid="stColumn"]:nth-child(1) div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stCheckbox"] label span[role="checkbox"] { background-color: #894b9d !important; border-color: #894b9d !important; }'''
        if st.session_state.get('chk_freight'): dynamic_css += '''div[data-testid="stColumn"]:nth-child(2) div[data-testid="stVerticalBlockBorderWrapper"] { background-color: #ffffff !important; border: 2px solid #ffffff !important; transform: translateY(-5px); box-shadow: 0 10px 30px rgba(255,255,255,0.15) !important; } div[data-testid="stColumn"]:nth-child(2) div[data-testid="stVerticalBlockBorderWrapper"] * { color: #111111 !important; } div[data-testid="stColumn"]:nth-child(2) div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stCheckbox"] label span[role="checkbox"] { background-color: #894b9d !important; border-color: #894b9d !important; }'''
        if st.session_state.get('chk_mail'): dynamic_css += '''div[data-testid="stColumn"]:nth-child(3) div[data-testid="stVerticalBlockBorderWrapper"] { background-color: #ffffff !important; border: 2px solid #ffffff !important; transform: translateY(-5px); box-shadow: 0 10px 30px rgba(255,255,255,0.15) !important; } div[data-testid="stColumn"]:nth-child(3) div[data-testid="stVerticalBlockBorderWrapper"] * { color: #111111 !important; } div[data-testid="stColumn"]:nth-child(3) div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stCheckbox"] label span[role="checkbox"] { background-color: #894b9d !important; border-color: #894b9d !important; }'''
        if dynamic_css: st.markdown(f"<style>{dynamic_css}</style>", unsafe_allow_html=True)

        st.markdown(f"<h3 style='text-align: center; margin-bottom: 5px; margin-top: 40px;'>{t['t_match']}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: #888; margin-bottom: 40px;'>{t['t_sub']}</p>", unsafe_allow_html=True)
        
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
            
        c_b1, c_b2, c_b3 = st.columns([1, 2, 1])
        with c_b2:
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
    # --- DE MOCKUP LAYOUT VOOR STAP 2 & 3 ---
    st.markdown("<div id='error-top'></div>", unsafe_allow_html=True)
    if st.session_state.get('scroll_up', False):
        st.components.v1.html("""<script>const doc = window.parent.document; const el = doc.getElementById("error-top"); if(el) { el.scrollIntoView({behavior: "smooth"}); }</script>""", height=0)
        st.session_state.scroll_up = False 
    
    def req_lbl(key, base_text):
        if st.session_state.validate_step2 and not str(st.session_state.get(key) or "").strip(): return f"{base_text} 🚨 :red[(Required)]"
        return base_text
        
    def wgt_lbl(key, base_text):
        if st.session_state.validate_step2 and float(st.session_state.get(key) or 0) <= 0: return f"{base_text} 🚨 <span style='color:#ff4b4b;'>(> 0)</span>"
        return base_text
        
    def email_lbl():
        base = t['c_em']
        if st.session_state.validate_step2:
            val = str(st.session_state.get('cont_email') or "")
            if not val.strip() or "@" not in val: return f"{base} 🚨 :red[(Required)]"
        return base

    col_steps, col_forms, col_map, col_receipt = st.columns([1.5, 3.5, 5, 2], gap="large")
    
    with col_steps:
        st.markdown(f"""
        <div class="v-steps-container">
            <h4 style="color: #fff; margin-bottom: 20px; font-size: 16px;">{t['st_title']}</h4>
            <div class="v-step {v_class(1)}"><div class="v-circle">1</div><div class="v-label">{t['st1']}</div></div>
            <div class="v-step {v_class(2)}"><div class="v-circle">2</div><div class="v-label">{t['st2']}</div></div>
            <div class="v-step {v_class(3)}"><div class="v-circle">3</div><div class="v-label">{t['st3']}</div></div>
        </div>
        """, unsafe_allow_html=True)

    if st.session_state.step == 2:
        with col_forms:
            if not st.session_state.selected_types: st.session_state.step = 1; st.rerun()

            with st.container(border=True):
                st.markdown(f"#### {t['r_info']}")
                c_p_zip, c_p_city = st.columns([1, 2])
                with c_p_zip: st.text_input(req_lbl("p_zip", "Pickup Zip"), value=prof.get('p_zip', ''), key="p_zip", max_chars=20)
                with c_p_city: st.text_input(req_lbl("p_city", "Pickup City"), value=prof.get('p_city', ''), key="p_city", max_chars=100)
                st.text_input(req_lbl("p_addr", "Pickup Address"), value=prof.get('p_addr', ''), key="p_addr", max_chars=150)
                
                st.write("")
                c_d_zip, c_d_city = st.columns([1, 2])
                with c_d_zip: st.text_input(req_lbl("d_zip", "Delivery Zip"), value=prof.get('d_zip', ''), key="d_zip", max_chars=20)
                with c_d_city: st.text_input(req_lbl("d_city", "Delivery City"), value=prof.get('d_city', ''), key="d_city", max_chars=100)
                st.text_input(req_lbl("d_addr", "Delivery Address"), value=prof.get('d_addr', ''), key="d_addr", max_chars=150)
                
            for sel in st.session_state.selected_types:
                with st.container(border=True):
                    disp_title = t['b1_t'] if sel=="Parcels & Documents" else t['b2_t'] if sel=="Cargo & Freight" else t['b3_t']
                    st.markdown(f"#### Load Details ({disp_title})")
                    if sel == "Parcels & Documents":
                        c_p1, c_p2 = st.columns(2)
                        with c_p1: st.number_input(wgt_lbl('pd_qty', t['lbl_qty']), min_value=0, max_value=10000, key="pd_qty")
                        with c_p2: st.number_input(wgt_lbl('pd_weight', t['lbl_wgt']), min_value=0.0, max_value=35.0, step=0.5, key="pd_weight")
                        st.checkbox(t['w_over'], key="pd_oversized")
                    elif sel == "Cargo & Freight":
                        cf_lbl = t['l_type']
                        if st.session_state.validate_step2 and not (st.session_state.get('cf_pal') or st.session_state.get('cf_full') or st.session_state.get('cf_lc')): cf_lbl += t['l_err']
                        st.markdown(f"<div style='font-size:13px; font-weight:600; color:#aaa; margin-bottom:5px;'>{cf_lbl}</div>", unsafe_allow_html=True)
                        st.checkbox(t['l_pal'], key="cf_pal")
                        if st.session_state.get('cf_pal'):
                            c_pf1, c_pf2 = st.columns(2)
                            with c_pf1: st.number_input(t['lbl_qty'], min_value=0, max_value=33, key="cf_pal_qty", label_visibility="collapsed")
                            with c_pf2: st.number_input(t['lbl_wgt'], min_value=0.0, max_value=1200.0, step=10.0, key="cf_pal_weight", label_visibility="collapsed")
                        st.checkbox(t['l_full'], key="cf_full")
                        if st.session_state.get('cf_full'):
                            c_ff1, c_ff2 = st.columns(2)
                            with c_ff1: st.number_input(t['lbl_qty'], min_value=0, max_value=10, key="cf_full_qty", label_visibility="collapsed")
                            with c_ff2: st.number_input(t['lbl_wgt'], min_value=0.0, max_value=25000.0, step=100.0, key="cf_full_weight", label_visibility="collapsed")
                        st.checkbox(t['l_lc'], key="cf_lc")
                        if st.session_state.get('cf_lc'):
                            c_lf1, c_lf2 = st.columns(2)
                            with c_lf1: st.number_input(t['lbl_qty'], min_value=0, max_value=1000, key="cf_lc_qty", label_visibility="collapsed")
                            with c_lf2: st.number_input(t['lbl_wgt'], min_value=0.0, max_value=25000.0, step=10.0, key="cf_lc_weight", label_visibility="collapsed")
                    elif sel == "Mail & Direct Marketing":
                        c_m1, c_m2 = st.columns(2)
                        with c_m1: st.number_input(wgt_lbl('mdm_qty', t['lbl_qty']), min_value=0, max_value=100000, key="mdm_qty")
                        with c_m2: st.number_input(wgt_lbl('mdm_weight', t['lbl_wgt']), min_value=0.0, max_value=2.0, step=0.1, key="mdm_weight")

            with st.container(border=True):
                st.markdown(f"#### {t['c_det']}")
                c_fn, c_ln = st.columns(2)
                with c_fn: st.text_input(req_lbl("comp_name", "Company"), value=prof.get('comp_name', ''), key="comp_name", max_chars=100)
                with c_ln: st.text_input(email_lbl(), value=prof.get('cont_email', ''), key="cont_email", max_chars=150)
                
            with st.container(border=True):
                st.markdown("#### Options & Info")
                st.checkbox(t['chk_same'], key="req_sameday")
                st.text_area("Additional Information (optional)", placeholder=t['a_ph'], max_chars=300, key="cont_info", height=80)

        with col_map:
            # MAP LOGICA MET HOLLOW CIRCLES
            p_addr_map = str(st.session_state.get('p_addr') or '').strip()
            p_zip_map = str(st.session_state.get('p_zip') or '').strip()
            p_city_map = str(st.session_state.get('p_city') or '').strip()
            
            d_addr_map = str(st.session_state.get('d_addr') or '').strip()
            d_zip_map = str(st.session_state.get('d_zip') or '').strip()
            d_city_map = str(st.session_state.get('d_city') or '').strip()
            
            p_coords = get_coordinates(p_addr_map, p_zip_map, p_city_map)
            d_coords = get_coordinates(d_addr_map, d_zip_map, d_city_map)
            
            layers = []
            
            if p_coords and d_coords:
                _, route_geom = get_route_data(p_coords, d_coords) 
                # 1. TEKEN EERST DE LIJN (zodat hij onder de stippen ligt)
                if route_geom:
                    layers.append(pdk.Layer("PathLayer", data=[{"path": route_geom}], get_path="path", get_color=[137, 75, 157, 255], width_scale=20, width_min_pixels=3, get_width=5))
                else:
                    route_geom = [[p_coords[1], p_coords[0]], [d_coords[1], d_coords[0]]]
                    layers.append(pdk.Layer("PathLayer", data=[{"path": route_geom}], get_path="path", get_color=[137, 75, 157, 255], width_scale=20, width_min_pixels=3, get_width=5))
                center_lat = (p_coords[0] + d_coords[0]) / 2
                center_lon = (p_coords[1] + d_coords[1]) / 2
                zoom = calculate_zoom(p_coords, d_coords)
            elif p_coords:
                center_lat, center_lon, zoom = p_coords[0], p_coords[1], 11
            elif d_coords:
                center_lat, center_lon, zoom = d_coords[0], d_coords[1], 11
            else:
                center_lat, center_lon, zoom = 64.0, 10.0, 3.5

            # 2. TEKEN DAN DE STIPPEN (met hollow/donkere kern look)
            points = []
            if p_coords: points.append({"pos": [p_coords[1], p_coords[0]], "name": "Pickup"})
            if d_coords: points.append({"pos": [d_coords[1], d_coords[0]], "name": "Delivery"})
            
            if points:
                layers.append(pdk.Layer(
                    "ScatterplotLayer", 
                    data=points, 
                    get_position="pos", 
                    get_fill_color=[26, 26, 28, 255], # Donkere kaartkleur als kern
                    get_line_color=[137, 75, 157, 255], # Paarse rand
                    stroked=True,
                    filled=True,
                    line_width_min_pixels=4,
                    get_radius=300, 
                    radius_min_pixels=8, 
                    radius_max_pixels=15
                ))
                
                # 3. TEKEN DE LABELS ALS LAATSTE (zwevend boven de stip)
                layers.append(pdk.Layer(
                    "TextLayer",
                    data=points,
                    get_position="pos",
                    get_text="name",
                    get_color=[255, 255, 255, 255],
                    get_size=13,
                    get_alignment_baseline="'bottom'",
                    get_pixel_offset=[0, -20]
                ))

            st.pydeck_chart(pdk.Deck(map_style="dark", layers=layers, initial_view_state=pdk.ViewState(latitude=center_lat, longitude=center_lon, zoom=zoom, pitch=0)), height=600)

        with col_receipt:
            current_price, _, _, breakdown_lines, _ = get_live_price()
            receipt_items_html = ""
            for name, price in breakdown_lines:
                if price == "": receipt_items_html += f"""<div style="display: flex; justify-content: space-between; margin-bottom: 2px;"><span>{name}</span><span></span></div>"""
                else: receipt_items_html += f"""<div style="display: flex; justify-content: space-between; font-size: 13px; color: #bbb; margin-bottom: 8px; margin-top: 6px;"><span>{name}</span><span>${price:,.2f}</span></div>"""
                
            receipt_html = f"""<div style="background: #1a1a1c; border: 1px solid #333; border-radius: 12px; padding: 24px;"><div style="color: #ffffff; font-size: 16px; font-weight: 600; margin-bottom: 20px;">Estimated Cost</div>{receipt_items_html}<div style="border-bottom: 1px dashed #444; margin: 15px 0;"></div><div style="display: flex; justify-content: space-between; align-items: center;"><span style="font-size: 14px; font-weight: 600; color: #fff;">Total</span><span style="font-size: 20px; font-weight: 700; color: #fff;">${current_price:,.2f}</span></div><div style="text-align: right; font-size: 11px; color: #666; margin-top: 2px;">Excl. MVA (VAT)</div></div>"""
            st.markdown(receipt_html, unsafe_allow_html=True)
            
            error_container = st.empty()
            
            # --- Validatie Logica ---
            missing_fields = False
            invalid_wgt = False
            for rk in ['comp_name', 'cont_email', 'p_zip', 'p_city', 'p_addr', 'd_zip', 'd_city', 'd_addr']:
                if not str(st.session_state.get(rk) or '').strip(): missing_fields = True; break
            if "Parcels & Documents" in st.session_state.selected_types:
                if st.session_state.get('pd_qty', 0) <= 0 or st.session_state.get('pd_weight', 0.0) <= 0: invalid_wgt = True
            if "Cargo & Freight" in st.session_state.selected_types:
                has_cf = False
                if st.session_state.get('cf_pal'):
                    has_cf = True
                    if st.session_state.get('cf_pal_qty', 0) <= 0 or st.session_state.get('cf_pal_weight', 0.0) <= 0: invalid_wgt = True
                if st.session_state.get('cf_full'):
                    has_cf = True
                    if st.session_state.get('cf_full_qty', 0) <= 0 or st.session_state.get('cf_full_weight', 0.0) <= 0: invalid_wgt = True
                if st.session_state.get('cf_lc'):
                    has_cf = True
                    if st.session_state.get('cf_lc_qty', 0) <= 0 or st.session_state.get('cf_lc_weight', 0.0) <= 0: invalid_wgt = True
                if not has_cf: missing_fields = True
            if "Mail & Direct Marketing" in st.session_state.selected_types:
                if st.session_state.get('mdm_qty', 0) <= 0 or st.session_state.get('mdm_weight', 0.0) <= 0: invalid_wgt = True

            email_val = str(st.session_state.get('cont_email') or '').strip()
            invalid_email = bool(email_val and "@" not in email_val)

            if st.session_state.validate_step2:
                if missing_fields: error_container.error(t['e_req'])
                elif invalid_email: error_container.error(t['e_em'])
                elif invalid_wgt: error_container.error(t['e_wgt'])
                
            st.write("")
            c_b1, c_b2 = st.columns([1, 1.5])
            with c_b1:
                if st.button("Go Back", type="secondary"): st.session_state.step = 1; st.session_state.validate_step2 = False; st.rerun()
            with c_b2:
                if st.button("Continue to Review →", type="primary"):
                    st.session_state.validate_step2 = True 
                    if missing_fields or invalid_email or invalid_wgt:
                        st.session_state.scroll_up = True; st.rerun()
                    else:
                        st.session_state.validate_step2 = False; st.session_state.scroll_up = False
                        specs_list = []
                        if "Parcels & Documents" in st.session_state.selected_types:
                            sz = "Oversized" if st.session_state.get('pd_oversized') else "Standard"
                            specs_list.append(f"📦 {st.session_state.get('pd_qty', 1)}x {t['b1_t']} ({st.session_state.get('pd_weight', 1)}kg) - {sz}")
                        if "Cargo & Freight" in st.session_state.selected_types:
                            loads = []
                            if st.session_state.get('cf_pal'): loads.append(f"{st.session_state.get('cf_pal_qty', 1)}x Pallet ({st.session_state.get('cf_pal_weight', 0.0)}kg)")
                            if st.session_state.get('cf_full'): loads.append(f"{st.session_state.get('cf_full_qty', 1)}x Container ({st.session_state.get('cf_full_weight', 0.0)}kg)")
                            if st.session_state.get('cf_lc'): loads.append(f"{st.session_state.get('cf_lc_qty', 1)}x Cargo ({st.session_state.get('cf_lc_weight', 0.0)}kg)")
                            specs_list.append(f"🚛 {t['b2_t']}: {', '.join(loads)}")
                        if "Mail & Direct Marketing" in st.session_state.selected_types:
                            specs_list.append(f"📭 {st.session_state.get('mdm_qty', 1)}x {t['b3_t']} ({st.session_state.get('mdm_weight', 0.5)}kg)")
                        
                        db_info = "\n".join([s.replace("**", "") for s in specs_list])
                        if str(st.session_state.get('cont_info', '')).strip(): db_info += f"\n\nNotes: {str(st.session_state.get('cont_info')).strip()}"
                        
                        calc_price, calc_cost, calc_profit, calc_breakdown, calc_note = get_live_price()
                        
                        st.session_state.temp_order = {
                            "company": st.session_state.get('comp_name', ''), "reg_no": "",
                            "address": "", "contact_name": "", "email": st.session_state.get('cont_email', ''), "phone": "",
                            "info_notes": str(st.session_state.get('cont_info', '')).strip(), "specs_list": specs_list, "db_info": db_info, "types": st.session_state.selected_types,
                            "pickup_address": st.session_state.get('p_addr', ''), "pickup_zip": st.session_state.get('p_zip', ''), "pickup_city": st.session_state.get('p_city', ''),
                            "delivery_address": st.session_state.get('d_addr', ''), "delivery_zip": st.session_state.get('d_zip', ''), "delivery_city": st.session_state.get('d_city', ''),
                            "price": calc_price, "profit": calc_profit, "price_breakdown": calc_breakdown, "calc_note": calc_note
                        }
                        st.session_state.step = 3; st.rerun()

    if st.session_state.step == 3:
        o = st.session_state.temp_order
        with col_forms:
            st.markdown(f"<h3 style='margin-top: 0px;'>{t['rev_t']}</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #888; font-size: 14px; margin-bottom: 20px;'>{t['rev_s']}</p>", unsafe_allow_html=True)
            
            with st.container(border=True):
                st.markdown(f"#### {t['rev_c']}")
                col_s1, col_s2 = st.columns(2)
                with col_s1:
                    st.markdown(f"<span style='color:#888; font-size:12px;'>{t['l_cn']}</span><br><b>{o['company']}</b>", unsafe_allow_html=True)
                with col_s2:
                    st.markdown(f"<span style='color:#888; font-size:12px;'>{t['l_em']}</span><br><b>{o['email']}</b>", unsafe_allow_html=True)
            
            with st.container(border=True):
                st.markdown(f"#### {t['rev_r']}")
                col_s3, col_s4 = st.columns(2)
                with col_s3:
                    st.markdown(f"<div style='color:#b070c6; font-size:14px; font-weight:bold; margin-bottom: 10px;'>PICKUP</div>", unsafe_allow_html=True)
                    st.write(f"{o.get('pickup_address', '-')}\n{o.get('pickup_zip', '-')} {o.get('pickup_city', '-')}")
                with col_s4:
                    st.markdown(f"<div style='color:#b070c6; font-size:14px; font-weight:bold; margin-bottom: 10px;'>DELIVERY</div>", unsafe_allow_html=True)
                    st.write(f"{o.get('delivery_address', '-')}\n{o.get('delivery_zip', '-')} {o.get('delivery_city', '-')}")
            
            with st.container(border=True):
                st.markdown(f"#### Shipment")
                for spec in o['specs_list']: st.markdown(spec)
                if o['info_notes']:
                    st.write("")
                    st.info(o['info_notes'])

        with col_map:
            if not st.session_state.is_submitted:
                st.markdown("<div style='height:300px'></div>", unsafe_allow_html=True)
                c_b1, c_b2 = st.columns([1, 1])
                with c_b1:
                    if st.button("Edit Details", type="secondary", use_container_width=True): st.session_state.step = 2; st.rerun()
                with c_b2:
                    if st.button("CONFIRM & SEND", type="primary", use_container_width=True):
                        db_order = {
                            "company": o['company'], "reg_no": o['reg_no'], "address": o['address'], "contact_name": o['contact_name'], "email": o['email'], "phone": o['phone'],
                            "info": o['db_info'], "types": ", ".join(o['types']), "status": "New", "received_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "pickup_address": o.get('pickup_address', ''), "pickup_zip": o.get('pickup_zip', ''), "pickup_city": o.get('pickup_city', ''),
                            "delivery_address": o.get('delivery_address', ''), "delivery_zip": o.get('delivery_zip', ''), "delivery_city": o.get('delivery_city', ''),
                            "price": o.get('price', 0), "profit": o.get('profit', 0)
                        }
                        if st.session_state.get('user'): db_order["user_id"] = st.session_state.user.id
                        try:
                            supabase.table("orders").insert(db_order).execute()
                            st.balloons()
                            st.session_state.is_submitted = True
                            st.rerun()
                        except Exception as e: st.error(f"{t['db_err']} Details: {e}")
            else:
                st.success(t['s_succ']); st.info(t['s_sub'])
                if st.button(t['b_new'], type="primary", use_container_width=True): reset_form_state(); st.rerun()
