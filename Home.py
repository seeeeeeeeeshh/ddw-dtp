import streamlit as st

st.set_page_config(page_title="Home")

st.header("Household Food Waste Predictor")

st.write(
    "This app predicts a country's **household food waste** "
    "(kg per capita per year) from four national indicators, using the "
    "multiple linear regression model built in our DDW project (Task 3)."
)

st.write(
    "Use the **Predictor** page (left sidebar) to enter a country's "
    "indicators and see the predicted waste."
)

st.subheader("What the model found")
st.write(
    "- National **wealth (GDP) does not predict** how much a household wastes.\n"
    "- **Logistics quality (LPI)** is the strongest predictor — better "
    "logistics is linked to *less* household waste.\n"
    "- This suggests food waste is **not** simply a rich-country problem, "
    "and that supply-chain improvements matter more than income."
)

st.caption(
    "Note: the model is intentionally simple and only moderately accurate "
    "(average error ~20 kg/capita). It is a directional guide, not a precise forecast."
)