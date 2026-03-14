import pandas as pd
import numpy as np
import re

df = pd.read_csv("laguna_details.csv")
print(f"Before cleaning: {len(df)} rows")

# Clean price - extract first ₱ amount only
def extract_price(text):
    if pd.isna(text):
        return None
    match = re.search(r'₱\s*([\d,]+)', str(text))
    if match:
        return match.group(1).replace(",", "")
    return None

df["price"] = df["price"].apply(extract_price)
df["price"] = pd.to_numeric(df["price"], errors="coerce")

# Clean land_size
df["land_size"] = df["land_size"].str.replace("sqm", "").str.strip()
df["land_size"] = pd.to_numeric(df["land_size"], errors="coerce")

# Clean usable_area
df["usable_area"] = df["usable_area"].str.replace("sqm", "").str.strip()
df["usable_area"] = pd.to_numeric(df["usable_area"], errors="coerce")

# Clean floors
df["floors"] = pd.to_numeric(df["floors"], errors="coerce")

# Clean car_parks
df["car_parks"] = pd.to_numeric(df["car_parks"], errors="coerce")

# Extract city from location
df["city"] = df["location"].str.extract(r",\s*([^,]+),\s*Laguna")

# Remove duplicates
df = df.drop_duplicates(subset=["url"])
print(f"After removing duplicates: {len(df)} rows")

# Drop rows missing critical fields
df = df.dropna(subset=["price", "land_size", "usable_area", "city"])
print(f"After dropping missing values: {len(df)} rows")

# Remove outliers
df = df[df["price"] > 500000]
df = df[df["price"] < 200000000]
df = df[df["land_size"] <= 2000]
df = df[df["usable_area"] <= 1000]
print(f"After removing outliers: {len(df)} rows")

print("\nData summary:")
print(df[["price", "land_size", "usable_area", "car_parks"]].describe())


df.to_csv("laguna_details_clean.csv", index=False)
print("\nSaved to laguna_details_clean.csv!")