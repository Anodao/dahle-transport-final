import streamlit as st
import requests
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="Dahle Transport - Plaats Order", page_icon="📦", layout="centered", initial_sidebar_state="collapsed")

# --- CSS STYLING & NAVBAR ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }
    .stApp { background-color: #111111 !important; }
    .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown li { color: #ffffff !important; }
    [data-testid="collapsedControl"], [data-testid="stSidebar"], header[data-testid="stHeader"] { display: none !important; }
    
    .block-container { padding-top: 110px; max-width: 800px; } 
    .navbar { position: fixed; top: 0; left: 0; width: 100%; height: 90px; background-color: #ffffff !important; z-index: 999; border-bottom: 1px solid #eaeaea; display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; padding: 0 40px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
    .nav-logo a { display: inline-block; height: 48px; text-decoration: none; cursor: pointer; }
    .nav-logo img { height: 100%; width: auto; display: block; transition: transform 0.2s ease-in-out; }
    .nav-logo a:hover img { transform: scale(1.05); } 
    .nav-links { display: flex; gap: 28px; font-size: 15px; font-weight: 500; justify-content: center;}
    .nav-links a, .nav-links span { text-decoration: none; color: #111111 !important; cursor: pointer; transition: color 0.2s;}
    .nav-links span:hover { color: #894b9d !important; }
    .nav-cta { display: flex; justify-content: flex-end; gap: 15px; align-items: center; }
    .cta-btn { background-color: #894b9d !important; color: white !important; padding: 10px 24px; border-radius: 50px; text-decoration: none !important; font-weight: 600; font-size: 13px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); white-space: nowrap;}
    
    div[data-baseweb="select"] > div, div[data-baseweb="base-input"] { background-color: #212529 !important; border: 1px solid #333333 !important; border-radius: 6px !important; }
    .stSelectbox div[data-baseweb="select"] span, .stSelectbox div[data-baseweb="select"] div, .stTextInput input, .stNumberInput input { color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; }
    div[data-testid="stVerticalBlockBorderWrapper"] { background-color: #1a1a1a; border: 1px solid #333333; border-radius: 10px; padding: 15px; }
    
    /* Stepper Styling */
    .step-indicator { display: flex; justify-content: space-between; align-items: center; margin-bottom: 40px; position: relative; }
    .step-indicator::before { content: ''; position: absolute; top: 50%; left: 0; right: 0; height: 2px; background-color: #333; z-index: 1; }
    .step { width: 40px; height: 40px; border-radius: 50%; background-color: #212529; color: #888; display: flex; align-items: center; justify-content: center; font-weight: bold; position: relative; z-index: 2; border: 2px solid #333; }
    .step.active { background-color: #894b9d; color: white; border-color: #894b9d; }
    </style>
    
    <div class="navbar">
        <div class="nav-logo"><a href="/" target="_self"><img src="https://cloud-1de12d.becdn.net/media/original/964295c9ae8e693f8bb4d6b70862c2be/logo-website-top-png-1-.webp"></a></div>
        <div class="nav-links"><a href="/"><span>Hjem</span></a><span>Om oss</span><span>Tjenester</span><span>Galleri</span><span>Kontakt</span></div>
        <div class="nav-cta"><a href="/Login" target="_self" style="color: #894b9d; font-weight:600; text-decoration:none;">KUNDEPORTAL</a><a href="/" target="_self" class="cta-btn">TA KONTAKT</a></div>
    </div>
""", unsafe_allow_html=True)

# --- API FUNCTIE VOOR AFSTAND ---
@st.cache_data(ttl=86400)
def get_route_distance(city1, city2):
    headers = {'User-Agent': 'DahleTransportApp/1.0'}
    try:
        res1 = requests.get(f"https://nominatim.openstreetmap.org/search?q={city1},Norway&format=json&limit=1", headers=headers).json()
        if not res1: return None
        lat1, lon1 = res1[0]['lat'], res1[0]['lon']
        time.sleep(0.5)
        res2 = requests.get(f"https://nominatim.openstreetmap.org/search?q={city2},Norway&format=json&limit=1", headers=headers).json()
        if not res2: return None
        lat2, lon2 = res2[0]['lat'], res2[0]['lon']
        route_url = f"http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=false"
        route_res = requests.get(route_url).json()
        if route_res.get('code') == 'Ok':
            return route_res['routes'][0]['distance'] / 1000.0 
    except Exception as e:
        pass
    return None

# --- GEHEUGEN INSTELLEN (SESSION STATE) ---
if 'step' not in st.session_state:
    st.session_state.step = 1

# --- VISUELE STAPPEN BALK ---
s1 = "active" if st.session_state.step >= 1 else ""
s2 = "active" if st.session_state.step >= 2 else ""
s3 = "active" if st.session_state.step == 3 else ""

st.markdown(f"""
<div class="step-indicator">
    <div class="step {s1}">1</div>
    <div class="step {s2}">2</div>
    <div class="step {s3}">3</div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# STAP 1: WAT WIL JE VERSTUREN?
# ==========================================
if st.session_state.step == 1:
    st.markdown("<h2 style='text-align: center; margin-bottom: 30px;'>Kies uw type zending</h2>", unsafe_allow_html=True)
    
    shape = st.radio("Selecteer een optie:", ["Parcels & Documents (tot 31.5kg)", "Cargo & Freight (Pallets/Containers)", "Afwijkend/Speciaal"], label_visibility="collapsed")
    weight = st.number_input("Geschat gewicht per stuk (kg)", min_value=0.5, value=10.0, step=0.5)
    quantity = st.number_input("Aantal items", min_value=1, value=1, step=1)
    
    st.write("")
    if st.button("Next Step ➔", type="primary", use_container_width=True):
        st.session_state.shape = shape
        st.session_state.weight = weight
        st.session_state.quantity = quantity
        st.session_state.step = 2
        st.rerun()

# ==========================================
# STAP 2: WAAR MOET HET HEEN?
# ==========================================
elif st.session_state.step == 2:
    st.markdown("<h2 style='text-align: center; margin-bottom: 30px;'>Route Informatie</h2>", unsafe_allow_html=True)
    
    pickup = st.text_input("📍 Afhaaladres (Stad in Noorwegen, bijv. Oslo)")
    delivery = st.text_input("🏁 Verzendadres (Stad in Noorwegen, bijv. Bergen)")
    
    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🡄 Back"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("Review Order ➔", type="primary", use_container_width=True):
            if not pickup or not delivery:
                st.warning("Vul a.u.b. beide steden in.")
            else:
                st.session_state.pickup = pickup
                st.session_state.delivery = delivery
                st.session_state.step = 3
                st.rerun()

# ==========================================
# STAP 3: REVIEW & CALCULATE (Checkout)
# ==========================================
elif st.session_state.step == 3:
    st.markdown("<h2 style='text-align: center; margin-bottom: 30px;'>Review & Estimate</h2>", unsafe_allow_html=True)
    
    with st.spinner("Berekent de beste route en prijs via satelliet..."):
        afstand_km = get_route_distance(st.session_state.pickup, st.session_state.delivery)
        
    if afstand_km is None:
        st.error("Route kon niet berekend worden. Controleer of de steden correct gespeld zijn.")
        if st.button("🡄 Terug om aan te passen"):
            st.session_state.step = 2
            st.rerun()
    else:
        # BEREKENING (Pas aan naar jouw echte prijzen!)
        base_fee = 350.0 
        km_cost = afstand_km * 12.5 
        weight_cost = (st.session_state.weight * st.session_state.quantity) * 5.0 
        
        shape_surcharge = 0.0
        if "Cargo" in st.session_state.shape: shape_surcharge = 400.0 * st.session_state.quantity
        elif "Afwijkend" in st.session_state.shape: shape_surcharge = 750.0 * st.session_state.quantity
            
        total_price = base_fee + km_cost + weight_cost + shape_surcharge
        
        with st.container(border=True):
            st.markdown(f"**Route:** {st.session_state.pickup.title()} ➔ {st.session_state.delivery.title()} ({afstand_km:.1f} km)")
            st.markdown(f"**Zending:** {st.session_state.quantity}x {st.session_state.shape.split('(')[0]}")
            st.write("---")
            st.markdown(f"<h2 style='text-align: center; color: #894b9d;'>Estimate: {total_price:,.0f} NOK</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #888; font-size: 12px;'>Exclusief BTW.</p>", unsafe_allow_html=True)
        
        st.write("")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🡄 Edit Details"):
                st.session_state.step = 2
                st.rerun()
        with c2:
            if st.button("✅ Confirm Order", type="primary", use_container_width=True):
                st.success("🎉 Order succesvol geplaatst! Wij nemen spoedig contact met u op.")
                # Hier later code toevoegen om op te slaan in de database!
                st.balloons()
