import streamlit as st
import pandas as pd
import numpy as np
import joblib

model = joblib.load("model_final.pkl")
feature_cols = joblib.load("features_final.pkl")

# Clean city mapping
city_mapping = {
    "4C Biñan": "Biñan",
    "Binan": "Biñan",
    "Binan City": "Biñan",
    "Binan Laguna\nProject unit Verdana Homes - Laguna\nLIIP Avenue": "Biñan",
    "Biñan\nLIIP Avenue": "Biñan",
    "Biñan City": "Biñan",
    "Calamba City": "Calamba",
    "Cabuyao City": "Cabuyao",
    "Canlubang": "Calamba",
    "Nuvali": "Calamba",
    "Nuvali Calamba": "Calamba",
    "Calamba Laguna\nProject unit Laguna Hills Subdivision\nSummerville": "Calamba",
    "Laguna\nProject unit Verdana Homes - Laguna\nLIIP Avenue": "Biñan",
    "Mamplasan": "Biñan",
    "Mamplasan\nProject unit Verdana Homes - Laguna\nLIIP Avenue": "Biñan",
    "Santa Rosa City": "Santa Rosa",
    "Sta. Rosa": "Santa Rosa",
    "Sta.Rosa": "Santa Rosa",
    "Laguna near Enchanted Kingdom\nSanta Rosa": "Santa Rosa",
    "Eton City": "Santa Rosa",
    "Greenfield City": "Biñan",
    "Paseo": "Santa Rosa",
    "Residential Park": "Santa Rosa",
    "Ayala Greenfield Estates": "Calamba",
    "Laguna for Sale\nLos Baños": "Los Baños",
}

raw_cities = [c.replace("city_", "") for c in feature_cols if c.startswith("city_")]

valid_cities = ["Alaminos", "Bay", "Biñan", "Cabuyao", "Calamba", "Calauan",
                "Los Baños", "Lumban", "Majayjay", "Pagsanjan", "Pila",
                "San Pablo", "San Pedro", "Santa Cruz", "Santa Maria", "Santa Rosa"]

st.set_page_config(page_title="Laguna House Price Estimator", page_icon="🏠")
st.title("🏠 Laguna House Price Estimator")
st.write("Estimate the price of a house in Laguna based on its features.")
st.caption("Model trained on 713 real Lamudi listings | Accuracy: 87.2% (R² = 0.872)")

st.sidebar.header("Property Details")
usable_area = st.sidebar.slider("Usable Area (sqm)", 20, 1000, 120)
land_size = st.sidebar.slider("Land Size (sqm)", 20, 2000, 150)
car_parks = st.sidebar.slider("Car Parks", 0, 8, 1)
city = st.sidebar.selectbox("City", valid_cities)
house_type = st.sidebar.selectbox("House Type", ["House", "Townhouse", "Villas"])
is_nuvali = st.sidebar.checkbox("Inside Nuvali / Ayala / Premium Subdivision")

input_data = {col: 0 for col in feature_cols}
input_data["usable_area"] = usable_area
input_data["land_size"] = land_size
input_data["car_parks"] = car_parks
input_data["area_ratio"] = usable_area / land_size
input_data["price_potential"] = land_size * usable_area
input_data["is_nuvali"] = int(is_nuvali)
input_data["is_premium_city"] = int(city in ["Santa Rosa", "San Pedro", "Biñan"])

# Map clean city to raw feature columns
for raw_city in raw_cities:
    mapped = city_mapping.get(raw_city, raw_city)
    if mapped == city and f"city_{raw_city}" in input_data:
        input_data[f"city_{raw_city}"] = 1

if f"house_type_{house_type}" in input_data:
    input_data[f"house_type_{house_type}"] = 1

input_df = pd.DataFrame([input_data])

if st.sidebar.button("Estimate Price"):
    log_price = model.predict(input_df)[0]
    price = np.exp(log_price)
    low = price * 0.85
    high = price * 1.15

    st.success(f"### Estimated Price: ₱{price:,.0f}")
    st.info(f"Likely range: ₱{low:,.0f} — ₱{high:,.0f}")

    st.subheader("Property Summary")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Usable Area", f"{usable_area} sqm")
    col2.metric("Land Size", f"{land_size} sqm")
    col3.metric("Car Parks", car_parks)
    col4.metric("City", city)

    price_per_sqm = price / land_size
    st.metric("Price per sqm", f"₱{price_per_sqm:,.0f}")

    st.caption("Based on 713 scraped Lamudi listings from Laguna. Actual prices may vary.")