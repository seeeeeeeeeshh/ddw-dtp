"""
library.py
Shared model logic for the Food Waste predictor app.

The model is a multiple linear regression trained in the DDW notebook
(Task 3). Because the fitted model is just an intercept plus four
coefficients, we store those numbers directly here rather than reloading
or retraining anything. This keeps the web app instant and dependency-free.

Model target : household food waste (kg per capita per year)
Predictors   : ln(GDP per capita USD), HDI, urban population %, LPI score
"""

import math

# --- Fitted coefficients from the DDW training set (raw, un-standardised) ---
# These match the notebook and the MU Excel workbook exactly.
INTERCEPT   = 122.707
COEF_LN_GDP = 2.117
COEF_HDI    = -39.140
COEF_URBAN  = 0.385
COEF_LPI    = -17.635

# Reference point for interpreting a prediction (training-set mean target).
MEAN_WASTE = 83.85


def predict_food_waste(gdp_per_capita, hdi, urban_pct, lpi):
    """Predict per-capita household food waste (kg/person/year).

    Args:
        gdp_per_capita (float): GDP per capita in current US$ (raw, not logged).
        hdi (float): Human Development Index, 0-1.
        urban_pct (float): Urban population as a percentage, 0-100.
        lpi (float): Logistics Performance Index, 1-5.

    Returns:
        float: predicted household food waste in kg per capita per year.
    """
    ln_gdp = math.log(gdp_per_capita)
    prediction = (
        INTERCEPT
        + COEF_LN_GDP * ln_gdp
        + COEF_HDI * hdi
        + COEF_URBAN * urban_pct
        + COEF_LPI * lpi
    )
    return prediction


def interpret_prediction(prediction):
    """Return a short plain-language reading of a prediction.

    Compares the predicted value against the global training-set mean so
    the user gets insight, not just a number.

    Args:
        prediction (float): predicted kg per capita per year.

    Returns:
        str: a one-sentence interpretation.
    """
    diff = prediction - MEAN_WASTE
    if diff > 5:
        return (f"That is about {diff:.0f} kg **above** the global average "
                f"(~{MEAN_WASTE:.0f} kg) — relatively high household waste.")
    elif diff < -5:
        return (f"That is about {abs(diff):.0f} kg **below** the global average "
                f"(~{MEAN_WASTE:.0f} kg) — relatively low household waste.")
    else:
        return (f"That is close to the global average "
                f"(~{MEAN_WASTE:.0f} kg per capita).")