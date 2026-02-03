import streamlit as st
import numpy as np
import joblib

# ------------------ Page Config ------------------
st.set_page_config(
    page_title="AQI Prediction App",
    page_icon="🌫️",
    layout="wide"
)

# ------------------ Title ------------------
st.title("🌍 Air Quality Index (AQI) Predictor")
st.caption("Predict air quality based on environmental parameters")

st.divider()

# ------------------ Load Model ------------------
model = joblib.load("LR_AQI_Prediction.joblib")

# ------------------ Sidebar Inputs ------------------
st.sidebar.header("⚙️ Input Parameters")

pm25 = st.sidebar.slider("PM2.5", 0.0, 500.0, 50.0)
pm10 = st.sidebar.slider("PM10", 0.0, 500.0, 80.0)
no2 = st.sidebar.slider("NO₂", 0.0, 300.0, 40.0)
so2 = st.sidebar.slider("SO₂", 0.0, 300.0, 20.0)
co = st.sidebar.slider("CO", 0.0, 10.0, 1.0)
temperature = st.sidebar.slider("🌡️ Temperature (°C)", -30.0, 50.0, 25.0)
humidity = st.sidebar.slider("💧 Humidity (%)", 0.0, 100.0, 50.0)

# ------------------ Input Array ------------------
input_data = np.array([[pm25, pm10, no2, so2, co, temperature, humidity]])

# ------------------ AQI Category Logic ------------------
def aqi_category(aqi):
    if aqi <= 50:
        return "🟢 Good"
    elif aqi <= 100:
        return "🟡 Moderate"
    elif aqi <= 150:
        return "🟠 Unhealthy (Sensitive)"
    elif aqi <= 200:
        return "🔴 Unhealthy"
    elif aqi <= 300:
        return "🟣 Very Unhealthy"
    else:
        return "⚫ Hazardous"

# ------------------ Layout Columns ------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("PM2.5", pm25)

with col2:
    st.metric("PM10", pm10)

with col3:
    st.metric("NO₂", no2)

st.divider()

# ------------------ Prediction ------------------
if st.button("🔮 Predict AQI", use_container_width=True):

    with st.spinner("Predicting AQI..."):
        prediction = model.predict(input_data)[0]

    st.subheader("📊 Prediction Result")

    colA, colB = st.columns(2)

    with colA:
        st.metric(
            label="AQI Value",
            value=f"{prediction:.2f}"
        )

    with colB:
        st.metric(
            label="AQI Category",
            value=aqi_category(prediction)
        )

    st.success("Prediction completed successfully!")

# ------------------ Info Section ------------------
with st.expander("ℹ️ What does AQI mean?"):
    st.markdown("""
    - 🟢 **0–50:** Good  
    - 🟡 **51–100:** Moderate  
    - 🟠 **101–150:** Unhealthy for Sensitive Groups  
    - 🔴 **151–200:** Unhealthy  
    - 🟣 **201–300:** Very Unhealthy  
    - ⚫ **301+:** Hazardous  
    """)