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

# Step 1 — collect all listing URLs first
print("Collecting listing URLs...")
urls = []

for page in range(1, 41):
    url = f"https://www.lamudi.com.ph/laguna/house/buy/?page={page}"
    driver.get(url)
    time.sleep(4)

    cards = driver.find_elements(By.CLASS_NAME, "snippet")
    if len(cards) == 0:
        print(f"Page {page} empty, stopping.")
        break

    for card in cards:
        try:
            link = card.find_element(By.TAG_NAME, "a").get_attribute("href")
            if link and "/property/" in link:
                urls.append(link)
        except:
            pass

    print(f"Page {page}: {len(urls)} URLs so far")

urls = list(set(urls))
print(f"\nTotal unique URLs: {len(urls)}")

# Step 2 — visit each listing and scrape details
print("\nScraping individual listings...")
all_listings = []

for i, url in enumerate(urls):
    try:
        driver.get(url)
        time.sleep(3)

        specs = driver.find_elements(By.CLASS_NAME, "spec")
        spec_data = {}
        for spec in specs:
            text = spec.text.strip()
            if ":" in text:
                key, value = text.split(":", 1)
                spec_data[key.strip()] = value.strip()

        try:
            price = driver.find_element(By.CLASS_NAME, "right-details").text.strip()
        except:
            price = None

        try:
            location = driver.find_element(By.CLASS_NAME, "left-details").text.strip()
        except:
            location = None

        all_listings.append({
            "url": url,
            "price": price,
            "location": location,
            "house_type": spec_data.get("House type"),
            "land_size": spec_data.get("Land size"),
            "usable_area": spec_data.get("Usable area"),
            "floors": spec_data.get("Property Floor"),
            "car_parks": spec_data.get("Car parks"),
        })

        if (i + 1) % 10 == 0:
            print(f"  Scraped {i + 1}/{len(urls)} listings...")

    except Exception as e:
        print(f"  Error on {url}: {e}")
        pass

driver.quit()

df = pd.DataFrame(all_listings)
df.to_csv("laguna_details.csv", index=False)
print(f"\nDone! Scraped {len(df)} listings with details.")
print(df.head())