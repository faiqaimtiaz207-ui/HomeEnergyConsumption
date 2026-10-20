
import pickle
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Smart Home Energy AI",
    page_icon="🏡",
    layout="wide"
)

# Load the trained model
@st.cache_resource
def load_model():
    with open("energy_model.pkl", "rb") as file:
        return pickle.load(file)

model = load_model()

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0b1220, #122b35);
    color: #f1f5f9;
}
.block-container {
    max-width: 1200px;
    padding-top: 2rem;
}
.hero {
    background: linear-gradient(120deg, #0f766e, #164e63);
    padding: 28px;
    border-radius: 20px;
    margin-bottom: 25px;
}
.hero h1 {
    color: white;
    font-size: 36px;
}
.hero p {
    color: #d1fae5;
}
.metric-card {
    background: #172b3a;
    border: 1px solid #28505a;
    padding: 22px;
    border-radius: 16px;
    text-align: center;
}
div.stButton > button {
    background: #14b8a6;
    color: #062c2b;
    border-radius: 10px;
    border: none;
    width: 100%;
    font-weight: bold;
    padding: 12px;
}
div.stButton > button:hover {
    background: #5eead4;
    color: #062c2b;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>🏡 Smart Home Energy AI</h1>
    <p>Predict appliance energy consumption using environmental
    conditions and smart-home sensor readings.</p>
</div>
""", unsafe_allow_html=True)

st.subheader("🌡️ Configure your home environment")
st.caption("Enter sensor readings to estimate appliance energy consumption.")

# Input order must match the 25 training features
feature_names = [
    "lights", "T1", "RH_1", "T2", "RH_2",
    "T3", "RH_3", "T4", "RH_4", "T5", "RH_5",
    "T6", "RH_6", "T7", "RH_7", "T8", "RH_8",
    "T9", "RH_9", "T_out", "Press_mm_hg",
    "RH_out", "Windspeed", "Visibility", "Tdewpoint"
]

defaults = {
    "lights": 0, "T1": 21.7, "RH_1": 40.3,
    "T2": 20.3, "RH_2": 40.4, "T3": 22.3,
    "RH_3": 39.2, "T4": 20.9, "RH_4": 39.0,
    "T5": 19.6, "RH_5": 50.0, "T6": 7.4,
    "RH_6": 50.0, "T7": 20.3, "RH_7": 35.0,
    "T8": 22.0, "RH_8": 42.0, "T9": 19.5,
    "RH_9": 41.6, "T_out": 7.4, "Press_mm_hg": 755.5,
    "RH_out": 79.8, "Windspeed": 4.0,
    "Visibility": 38.3, "Tdewpoint": 3.8
}

labels = {
    "lights": "Lights energy (Wh)",
    "T1": "Kitchen temperature (°C)",
    "RH_1": "Kitchen humidity (%)",
    "T2": "Living room temperature (°C)",
    "RH_2": "Living room humidity (%)",
    "T3": "Laundry temperature (°C)",
    "RH_3": "Laundry humidity (%)",
    "T4": "Office temperature (°C)",
    "RH_4": "Office humidity (%)",
    "T5": "Bathroom temperature (°C)",
    "RH_5": "Bathroom humidity (%)",
    "T6": "Outside building temperature (°C)",
    "RH_6": "Outside building humidity (%)",
    "T7": "Ironing room temperature (°C)",
    "RH_7": "Ironing room humidity (%)",
    "T8": "Teenager room temperature (°C)",
    "RH_8": "Teenager room humidity (%)",
    "T9": "Parents' room temperature (°C)",
    "RH_9": "Parents' room humidity (%)",
    "T_out": "Outdoor temperature (°C)",
    "Press_mm_hg": "Atmospheric pressure (mm Hg)",
    "RH_out": "Outdoor humidity (%)",
    "Windspeed": "Wind speed (m/s)",
    "Visibility": "Visibility (km)",
    "Tdewpoint": "Dew point (°C)"
}

with st.form("prediction_form"):
    st.subheader("🏠 Indoor Conditions")
    col1, col2 = st.columns(2)

    values = defaults.copy()

    with col1:
        values["lights"] = st.number_input(
            "Lights Energy (Wh)", min_value=0,
            max_value=100, value=0
        )
        values["T1"] = st.number_input(
            "Kitchen Temperature (°C)", value=21.7
        )
        values["RH_1"] = st.number_input(
            "Kitchen Humidity (%)", value=40.3
        )
        values["T2"] = st.number_input(
            "Living Room Temperature (°C)", value=20.3
        )

    with col2:
        values["RH_2"] = st.number_input(
            "Living Room Humidity (%)", value=40.4
        )
        values["T_out"] = st.number_input(
            "Outdoor Temperature (°C)", value=7.4
        )
        values["RH_out"] = st.number_input(
            "Outdoor Humidity (%)", value=79.8
        )
        values["Windspeed"] = st.number_input(
            "Wind Speed (m/s)", value=4.0
        )

    submitted = st.form_submit_button(
        "⚡ Predict Energy Consumption"
    )

if submitted:
    input_df = pd.DataFrame(
        [[values[name] for name in feature_names]],
        columns=feature_names
    )

    prediction = max(0, float(model.predict(input_df)[0]))

    st.markdown("---")
    st.subheader("📊 Prediction Result")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Predicted Energy Consumption", f"{prediction:.2f} Wh")

    with col2:
        st.metric("Model", "Ridge Regression")
        st.caption("10-fold cross-validation RMSE: 93.69 Wh")

    st.info(
        "This is an estimate based on the dataset, not a live "
        "measurement of your home."
    )
