# Household Food Waste Predictor

A Streamlit web app that predicts a country's household food waste
(kg per capita per year) from four national indicators, using the
multiple linear regression model built in our Data Driven World project.

## What it does
Enter a country's GDP per capita, HDI, urban population %, and Logistics
Performance Index. The app returns the predicted household food waste and
compares it to the global average.

## Model
Multiple linear regression (built by hand in the DDW notebook, no scikit-learn).
The fitted coefficients are stored in `library.py`. Prediction:

    waste = 122.707 + 2.117*ln(GDP) - 39.140*HDI + 0.385*Urban% - 17.635*LPI

Target: household food waste (kg/capita/year), UNEP/FAO Food Waste Index.
Predictors: World Bank (GDP, urban %, LPI) and UNDP (HDI).

## File structure
- `Home.py` — landing page and summary of findings
- `pages/Predictor.py` — the interactive prediction tool
- `library.py` — model coefficients and prediction functions
- `Pipfile` / `Pipfile.lock` — dependencies (Streamlit)

## How to run
pipenv install
pipenv run streamlit run Home.py

Then open the local URL shown in the terminal.

## Note
The model is intentionally simple and moderately accurate (average error
~20 kg/capita). Its value is directional: it shows that logistics quality,
not national wealth, is the main predictor of household food waste.