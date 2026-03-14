import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

df = pd.read_csv("laguna_details_clean.csv")

# Extract city and house type
df["city"] = df["location"].str.extract(r",\s*([^,]+),\s*Laguna")
df["house_type"] = df["house_type"].fillna("House")

# Fill missing
df["car_parks"] = df["car_parks"].fillna(0)

# Engineer features
df["area_ratio"] = df["usable_area"] / df["land_size"]
df["price_potential"] = df["land_size"] * df["usable_area"]
df["is_nuvali"] = df["location"].str.contains("Nuvali|Mirala|Avida|Mondia|Ayala Greenfield", case=False, na=False).astype(int)
df["is_premium_city"] = df["city"].isin(["Santa Rosa", "San Pedro", "Biñan"]).astype(int)

# One-hot encode
df = pd.get_dummies(df, columns=["city", "house_type"])

feature_cols = (
    ["usable_area", "land_size", "car_parks", "area_ratio",
     "price_potential", "is_nuvali", "is_premium_city"]
    + [col for col in df.columns if col.startswith("city_")]
    + [col for col in df.columns if col.startswith("house_type_")]
)

X = df[feature_cols]
y = np.log(df["price"])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Training on {len(X_train)} rows, testing on {len(X_test)} rows")
print(f"Total features: {len(feature_cols)}")

def evaluate(name, y_test, y_pred):
    actual = np.exp(y_test)
    predicted = np.exp(y_pred)
    print(f"\n{name}:")
    print(f"  MAE:  ₱{mean_absolute_error(actual, predicted):,.0f}")
    print(f"  R2:   {r2_score(actual, predicted):.3f}")

rf = RandomForestRegressor(n_estimators=200, random_state=42)
rf.fit(X_train, y_train)
evaluate("Random Forest", y_test, rf.predict(X_test))

joblib.dump(rf, "model_final.pkl")
joblib.dump(feature_cols, "features_final.pkl")
print("\nFinal model saved!")