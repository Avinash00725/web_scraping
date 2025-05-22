import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")

service = Service('/usr/bin/chromedriver')
driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get('https://www.olx.in/items/q-car-cover')
    wait = WebDriverWait(driver, 30) 
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3) 

    listings = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-aut-id="itemBox3"]')))

    print(f"Found {len(listings)} listings")

    results = []
    for listing in listings:
        try:
            title = listing.find_element(By.CSS_SELECTOR, '[data-aut-id="itemTitle"]').text
        except:
            title = "N/A"

        try:
            cost = listing.find_element(By.CSS_SELECTOR, '[data-aut-id="itemPrice"]').text
        except:
            cost = "N/A"

        results.append({
            "title": title,
            "cost": cost
        })
    with open('car_cover_listings.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print("Scraping completed. Results saved to 'car_cover_listings.json'.")

except Exception as e:
    print(f"An error occurred: {e}")
    with open("page_source.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)

finally:
    driver.quit()