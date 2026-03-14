# Laguna House Price Estimator

A machine learning web app that predicts house prices in Laguna, Philippines using real listing data scraped from Lamudi.

## Live Demo
[Try the app here] https://laguna-house-price-estimator-jwbceu9ag6tqhlmxyzuvfc.streamlit.app/

## What I Built
- **Web scraper** using Selenium to collect 1,200+ real property listings from Lamudi.com.ph
- **Data cleaning pipeline** to handle missing values, outliers, and feature engineering
- **ML model** trained on 713 cleaned listings with 87.2% accuracy (R² = 0.872)
- **Streamlit web app** for interactive price estimation

## Tech Stack
- Python, Selenium, BeautifulSoup
- Pandas, Scikit-learn, XGBoost
- Streamlit

## Model Features
- Usable area (sqm)
- Land size (sqm)
- Car parks
- City (18 Laguna cities)
- House type
- Premium subdivision flag (Nuvali, Ayala, etc.)

## How to Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Results
| Model | R² | MAE |
|---|---|---|
| Linear Regression | -5.136 | ₱13,358,746 |
| XGBoost | 0.855 | ₱3,959,831 |
| **Final (Random Forest)** | **0.872** | **₱3,750,787** |

## Dataset
Scraped from Lamudi.com.ph — 1,200 raw listings cleaned down to 713 quality rows covering Calamba, Santa Rosa, Biñan, San Pedro, Cabuyao and 13 other Laguna cities.
