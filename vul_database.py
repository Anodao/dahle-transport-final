import streamlit as st
from supabase import create_client

# Connectie maken
url = st.secrets["supabase"]["url"]
key = st.secrets["supabase"]["key"]
supabase = create_client(url, key)

dummy_orders = [
    {
        "company": "Rema 1000 Distribusjon",
        "reg_no": "987654321",
        "address": "Industriveien 2, 7080 Trondheim, Norway",
        "contact_name": "Ola Nordmann",
        "email": "ola.nordmann@rema.no",
        "phone": "+47 98765432",
        "types": "Cargo & Freight",
        "info": "--- Order Specifications ---\n🚛 Freight: 50 shipments/yr. Load: Pallet to Domestic.\n12 pallets with dry goods.",
        "status": "New",
        "received_date": "2026-02-25 08:30", # Paar dagen geleden
        "pickup_address": "Industriveien 2", "pickup_zip": "7080", "pickup_city": "Trondheim",
        "delivery_address": "Sentrumsveien 15", "delivery_zip": "7160", "delivery_city": "Bjugn"
    },
    {
        "company": "Byggmakker Oslo",
        "reg_no": "123456789",
        "address": "Ulvenveien 80, 0581 Oslo, Norway",
        "contact_name": "Kari Nilsen",
        "email": "kari@byggmakker.no",
        "phone": "+47 45678912",
        "types": "Cargo & Freight",
        "info": "--- Order Specifications ---\n🚛 Freight: One-time shipment. Load: Full Container to Domestic.\nBuilding materials, heavy load (approx. 18,000 kg).",
        "status": "New",
        "received_date": "2026-02-26 11:15",
        "pickup_address": "Ulvenveien 80", "pickup_zip": "0581", "pickup_city": "Oslo",
        "delivery_address": "Havneveien 10", "delivery_zip": "7010", "delivery_city": "Trondheim"
    },
    {
        "company": "Nordisk Finans AS",
        "reg_no": "888777666",
        "address": "Kongens gate 20, 7011 Trondheim, Norway",
        "contact_name": "Lars Bakken",
        "email": "lars@nordiskfinans.no",
        "phone": "+47 11223344",
        "types": "Parcels & Documents",
        "info": "--- Order Specifications ---\n📦 Parcels: 100 shipments (Weekly) to Pan-European.\nUrgent financial documents.",
        "status": "Processed", # Deze is al verwerkt!
        "received_date": "2026-02-27 14:00",
        "pickup_address": "Kongens gate 20", "pickup_zip": "7011", "pickup_city": "Trondheim",
        "delivery_address": "Sveavägen 44", "delivery_zip": "11134", "delivery_city": "Stockholm"
    },
    {
        "company": "Elektro Importøren",
        "reg_no": "555444333",
        "address": "Kabelgata 8, 0580 Oslo, Norway",
        "contact_name": "Silje Haugen",
        "email": "silje@elektro.no",
        "phone": "+47 99887766",
        "types": "Parcels & Documents, Cargo & Freight",
        "info": "--- Order Specifications ---\n📦 Parcels: Daily to Domestic.\n🚛 Freight: Monthly to Domestic.\nMixed electronics, fragile.",
        "status": "New",
        "received_date": "2026-02-28 09:45",
        "pickup_address": "Kabelgata 8", "pickup_zip": "0580", "pickup_city": "Oslo",
        "delivery_address": "Ladeveien 12", "delivery_zip": "7041", "delivery_city": "Trondheim"
    },
    {
        "company": "Trøndelag Fiskeeksport",
        "reg_no": "111222333",
        "address": "Kystveien 1, 7170 Åfjord, Norway",
        "contact_name": "Espen Lie",
        "email": "espen@trondelagfisk.no",
        "phone": "+47 44332211",
        "types": "Cargo & Freight",
        "info": "--- Order Specifications ---\n🚛 Freight: 200 shipments/yr. Load: Full Container to Pan-European.\nFresh salmon, requires cooling transport.",
        "status": "New",
        "received_date": "2026-03-01 10:20", # Vandaag
        "pickup_address": "Kystveien 1", "pickup_zip": "7170", "pickup_city": "Åfjord",
        "delivery_address": "Fisketorvet 2", "delivery_zip": "1561", "delivery_city": "Copenhagen"
    }
]

# Push alles naar de database
for order in dummy_orders:
    supabase.table("orders").insert(order).execute()

print("✅ 5 dummy orders succesvol toegevoegd aan de database!")
