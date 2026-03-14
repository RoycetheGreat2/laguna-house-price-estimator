import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

all_listings = []

for page in range(1, 41):
    url = f"https://www.lamudi.com.ph/laguna/house/buy/?page={page}"
    print(f"Scraping page {page}...")
    driver.get(url)
    time.sleep(4)

    cards = driver.find_elements(By.CLASS_NAME, "snippet")
    print(f"  Found {len(cards)} listings on page {page}")

    if len(cards) == 0:
        print("No more listings, stopping early.")
        break

    for card in cards:
        try:
            title = card.find_element(By.CLASS_NAME, "snippet__content__title").text.strip()
            location = card.find_element(By.CLASS_NAME, "snippet__content__location").text.strip()
            price = card.find_element(By.CLASS_NAME, "snippet__content__price").text.strip()

            props = card.find_element(By.CLASS_NAME, "snippet__content__properties").text.strip()
            lines = props.split("\n")
            bedrooms = lines[0] if len(lines) > 0 else None
            bathrooms = lines[1] if len(lines) > 1 else None
            floor_area = lines[2] if len(lines) > 2 else None
            amenity = lines[3] if len(lines) > 3 else None

            all_listings.append({
                "title": title,
                "price": price,
                "location": location,
                "bedrooms": bedrooms,
                "bathrooms": bathrooms,
                "floor_area": floor_area,
                "amenity": amenity
            })
        except:
            pass

driver.quit()

df = pd.DataFrame(all_listings)
df.to_csv("laguna_listings.csv", index=False)
print(f"\nDone! Scraped {len(df)} listings.")
print(df.head())