import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os

check_all_stores = False
sizes = [[185,16,14],[205,55,16],[225,50,16]]
data = pd.DataFrame(columns=["Site","Store", "Brand", "Pattern","Size","Type","Price"])
savefile = "scrapeddata.csv"

URL = "https://www.dexel.co.uk/tyres#tyres"
SITE = "dexel"
    
for size in sizes:
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)
    driver.get(URL)
    time.sleep(5)
    button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Search by Tyre Size.")))
    driver.execute_script("arguments[0].click();", button)
    time.sleep(3)

    tyre_inputs = ["width_list","profile_list","size_list"]
    error_occured = False
    for n , tyre_input in enumerate(tyre_inputs):
        try:
            element = driver.find_element(By.XPATH, f"//select[@class=\"{tyre_input}\"]")
            time.sleep(1)
            element.send_keys(str(size[n]))
            time.sleep(0.5)
            element.send_keys(Keys.TAB)
        except:
            print("Error with supplied data")
            driver.close()
            error_occured = True
            continue

    if error_occured:
        continue
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Search").click()
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    results = soup.body
    stores = results.find_all("div", class_="bookingLocator")
    
    names = []
    store_ids = []
    for i in stores:
        buttons = i.findAll("button", id=True)
        names.append(i.find("h3").get_text(strip=True))
        for button in buttons:
            store_ids.append(button['id'])

    for store, name in zip(store_ids,names):
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        button = wait.until(EC.element_to_be_clickable((By.ID, store)))
        driver.execute_script("arguments[0].click();", button)
        time.sleep(3)
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-add-tyre")))
        time.sleep(3)

        page = 1

        while True:
            time.sleep(1)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            products = soup.select("div.tkf-product")
            for product in products:
                img = product.find('div', class_="brand-logo-wrapper").find('img')
                text = product.find('p', class_="para-text").get_text(strip=True)
                BRAND = img.get('alt') if img and 'alt' in img.attrs else "Dexel - assumed as alt was missing"
                PATTERN = " ".join(text.split()[2:])
                SIZE = " ".join(text.split()[:2])
                TYRETYPE = []
                otherinfo = product.find('div', class_='tyre-icons')
                icons = otherinfo.find_all('i')
                for icon in icons:
                    TYRETYPE.append(icon.get('title'))
                PRICE = product.find("span", class_="price-number").get_text(strip=True)
                # ["Site", "Store", "Brand", "Pattern","Size","Type","Price"]
                newrow = {
                    "Site": SITE,
                    "Store":name,
                    "Brand": BRAND,
                    "Pattern": PATTERN,
                    "Size": SIZE,
                    "Type": TYRETYPE,
                    "Price": PRICE.replace("£",""),
                    }
                data.loc[len(data)] = newrow
                
            try:
                print(page)
                page+=1
                button = wait.until(EC.presence_of_element_located((By.LINK_TEXT, str(page))))
                driver.execute_script("arguments[0].click();", button)
                                
            except:
                print("final page reached")
                break
        if check_all_stores:
            time.sleep(5)
            button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-change-branch")))
            driver.execute_script("arguments[0].click();", button)
            time.sleep(3)
        else:
            break
    driver.close()

if not os.path.isfile(savefile):
    data.to_csv(savefile, index=False)
else:
    data.to_csv(savefile, mode='a', header=False, index=False)
            
driver.quit()
