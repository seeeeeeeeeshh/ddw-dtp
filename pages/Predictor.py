import streamlit as st
import pandas as pd
import math
from library import predict_food_waste, interpret_prediction, MEAN_WASTE

# Used for finding similar profiles
df = pd.read_excel("indicators.xlsx", sheet_name='CrossSection_2022_full')
df = df.loc[:, ["Country","GDP_per_capita_USD","HDI_value", "Urban_pop_pct", "LPI_score", "FoodWaste_HHS"]]
df = df.dropna()

def get_distance(row, predicted):
    return (row["FoodWaste_HHS"] - predicted) ** 2

st.set_page_config(page_title="Predictor", layout="wide")

st.header("Food Waste Predictor")
st.write("Enter a country's indicators on the left. The prediction appears on the right.")

# Two columns: inputs | result
left, right = st.columns([1, 1], gap="large")

with left:
    st.subheader("Country profile")
    gdp = st.number_input(
        "GDP per capita (US$)",
        min_value=300, max_value=125000, value=25000, step=500,
    )
    hdi = st.number_input(
        "Human Development Index (0-1)",
        min_value=0.35, max_value=0.97, value=0.80, step=0.01,
    )
    urban = st.number_input(
        "Urban population (%)",
        min_value=10, max_value=100, value=70, step=1,
    )
    lpi = st.number_input(
        "Logistics Performance Index (1-5)",
        min_value=1.5, max_value=4.5, value=3.0, step=0.1,
    )

with right:
    st.subheader("Result")
    prediction = predict_food_waste(gdp, hdi, urban, lpi)

    # prediction vs global average, shown as a delta
    st.metric(
        label="Predicted household waste (kg/capita/year)",
        value=f"{prediction:.1f}",
        delta=f"{prediction - MEAN_WASTE:+.1f} vs global average",
        delta_color="inverse",  # less waste = good = green
    )
    st.write(interpret_prediction(prediction))

    st.divider()
    st.caption(
        "The model's main finding: logistics quality (LPI) is the strongest "
        "predictor — lower LPI pushes waste up. National wealth barely matters."
    )

st.subheader("Countries with Similar HHW")

df["Distance"] = df.apply(get_distance, axis=1, args=(prediction,))
df = df.nsmallest(10, columns=["Distance"])
df = df.loc[:, ["Country","GDP_per_capita_USD","HDI_value", "Urban_pop_pct", "LPI_score", "FoodWaste_HHS"]]
df = df.sort_values(by="FoodWaste_HHS", ascending=False)
df = df.rename(columns={"GDP_per_capita_USD": "GDP per Capita",
                "HDI_value": "HDI Value",
                "Urban_pop_pct": "Urban Population Percentage",
                "LPI_score": "LPI Score",
                "FoodWaste_HHS": "Household Waste (kg/capita/year)"})
df = df.reset_index(drop = True)
st.write(df)