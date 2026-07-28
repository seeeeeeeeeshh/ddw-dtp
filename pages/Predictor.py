import streamlit as st
from library import predict_food_waste, interpret_prediction

st.set_page_config(page_title="Predictor")

st.header("Predict Household Food Waste")
st.write("Enter a country's indicators below. The prediction updates automatically.")

# --- Inputs: sliders bounded to realistic ranges so values can't be invalid ---
gdp = st.slider(
    "GDP per capita (US$)",
    min_value=300, max_value=125000, value=25000, step=100,
    help="Gross domestic product per person, in current US dollars.",
)
hdi = st.slider(
    "Human Development Index (HDI)",
    min_value=0.35, max_value=0.97, value=0.80, step=0.01,
    help="UNDP development index, from 0 (low) to 1 (high).",
)
urban = st.slider(
    "Urban population (%)",
    min_value=10, max_value=100, value=70, step=1,
    help="Percentage of the population living in urban areas.",
)
lpi = st.slider(
    "Logistics Performance Index (LPI)",
    min_value=1.5, max_value=4.5, value=3.0, step=0.1,
    help="World Bank logistics quality score, 1 (poor) to 5 (excellent).",
)

# --- Prediction ---
prediction = predict_food_waste(gdp, hdi, urban, lpi)

st.subheader("Predicted household food waste")
st.metric(label="kg per capita per year", value=f"{prediction:.1f}")
st.write(interpret_prediction(prediction))

st.caption(
    "Tip: try lowering the LPI score — you'll see the prediction rise, "
    "reflecting the model's main finding that weaker logistics is linked "
    "to more household food waste."
)