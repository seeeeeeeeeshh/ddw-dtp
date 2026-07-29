import streamlit as st
import pandas as pd
import math
from library import predict_food_waste, interpret_prediction, MEAN_WASTE

# Used for finding similar profiles
df = pd.read_excel("indicators.xlsx", sheet_name='CrossSection_2022_full')
df = df.loc[:, ["Country","GDP_per_capita_USD","HDI_value", "Urban_pop_pct", "LPI_score", "FoodWaste_HHS"]]
df = df.dropna()
df["LN_GDP"] = df["GDP_per_capita_USD"].apply(math.log)
df_features = df.loc[:, ["LN_GDP", "HDI_value", "Urban_pop_pct", "LPI_score"]]

means = df_features.mean(axis=0)
stds = df_features.std(axis=0)

def get_normal_z(val, mean, std):
    result = (val - mean) / std
    return result

def get_cost(row, normal_ln_gdp, normal_hdi, normal_urban, normal_lpi):
    cost_gdp = (row["Normal_LN_GDP"] - normal_ln_gdp) ** 2
    cost_hdi = (row["Normal_HDI"] - normal_hdi) ** 2
    cost_urban = (row["Normal_Urban"] - normal_urban) ** 2
    cost_lpi = (row["Normal_LPI"] - normal_lpi) ** 2

    return (cost_gdp + cost_hdi + cost_urban + cost_lpi) ** 0.5

df["Normal_LN_GDP"] = get_normal_z(df["LN_GDP"], means.iloc[0], stds.iloc[0])
df["Normal_HDI"] = get_normal_z(df["HDI_value"], means.iloc[1], stds.iloc[1])
df["Normal_Urban"] =  get_normal_z(df["Urban_pop_pct"], means.iloc[2], stds.iloc[2])
df["Normal_LPI"] = get_normal_z(df["LPI_score"], means.iloc[3], stds.iloc[3])

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

st.subheader("Similar Profiles")
st.write("The following countries are the most similar to the inputted country profile (not including HHW). Very similar profiles are ranked higher.")

ln_gdp = math.log(gdp)
normal_ln_gdp = get_normal_z(ln_gdp, means.iloc[0], stds.iloc[0])
normal_hdi = get_normal_z(hdi, means.iloc[1], stds.iloc[1])
normal_urban =  get_normal_z(urban, means.iloc[2], stds.iloc[2])
normal_lpi = get_normal_z(lpi, means.iloc[3], stds.iloc[3])

df["Cost"] = df.apply(get_cost, axis=1, args=(normal_ln_gdp, normal_hdi, normal_urban, normal_lpi))

df = df.nsmallest(5, columns=["Cost"])
df = df.loc[:, ["Country","GDP_per_capita_USD","HDI_value", "Urban_pop_pct", "LPI_score", "FoodWaste_HHS"]]
df = df.rename(columns={"GDP_per_capita_USD": "GDP per Capita (US$)",
                "HDI_value": "HDI",
                "Urban_pop_pct": "Urban Population Percentage",
                "LPI_score": "LPI",
                "FoodWaste_HHS": "Household Waste (kg/capita/year)"})
df = df.reset_index(drop = True)
st.dataframe(df.style.format({
    "GDP per Capita (US$)": "{:.2f}",
    "HDI": "{:.3f}",
    "Urban Population Percentage": "{:.2f}",
    "LPI": "{:.1f}",
    "Household Waste (kg/capita/year)": "{:.2f}"
    }))