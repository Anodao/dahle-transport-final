import streamlit as st
import time
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Dahle Transport - Home",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- SESSION STATE ---
if 'orders' not in st.session_state:
    st.session_state.orders = []
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'selected_type' not in st.session_state:
    st.session_state.selected_type = None
if 'temp_order' not in st.session_state:
    st.session_state.temp_order = {}

# --- CSS STYLING (Schone Look) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }

    /* --- DE STANDAARD BALK WEGHALEN --- */
    
    /* 1. Maak de header transparant (zodat je onze witte balk ziet) */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    
    /* 2. Verberg de regenbooglijn en de toolbar rechts */
    div[data-testid="stDecoration"] { display: none; }
    div[data-testid="stToolbar"] { display: none; }
    
    /* 3. Maak het menu-knopje (pijltje) ZWART zodat je hem ziet op wit */
    button[kind="header"] {
        color: #333 !important; 
    }
    
    /* Verberg footer */
    footer { visibility: hidden; }
    
    /* --- EIGEN NAVBAR --- */
    
    /* Content naar beneden duwen zodat het niet achter de balk zit */
    .block-container { padding-top: 140px; }

    .navbar {
        position: fixed; 
        top: 0; 
        left: 0; 
        width: 100%; 
        height: 100px;
        background-color: white; 
        z-index: 999; /* Net onder de header knop */
        border-bottom: 1px solid #eee; 
        display: flex; 
        align-items: center; 
        justify-content: space-between;
        padding: 0
