import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import os

check_all_stores = False
sizes = [[185,16,14],[205,55,16],[225,50,16]]
data = pd.DataFrame(columns=["Site","Store", "Brand", "Pattern","Size","Type","Price"])
savefile = "scrapeddata.csv"

URL = "https://www.national.co.uk/tyres-search/"#205-55-16 example on how sizes are used
SITE = "www.national.co.uk"

for size in sizes:
    URL_with_size = URL + "-".join([str(i) for i in size])
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(URL_with_size)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    products = soup.select("div[id^=PageContent_ucTyreResults_rptTyres_divTyre_]")
    for product in products:
        img = product.find('div', class_="details").find('img')
        text = [p.get_text(strip=True) for p in product.find('div', class_="details").find_all('p')]       
        BRAND = img.get('alt') if img and 'alt' in img.attrs else "no alt specified"
        PATTERN = text[0]
        SIZE = text[1]
        PRICE = product.find('span', class_="red text-24").find('strong').get_text(strip=True)
        TYPE = product["data-tyre-season"]
        
        # ["Site", "Store", "Brand", "Pattern","Size","Type","Price"]
        newrow = {
            "Site": SITE,
            "Store": "N/A",
            "Brand": BRAND,
            "Pattern": PATTERN,
            "Size": SIZE,
            "Type": TYPE,
            "Price": PRICE.replace("£",""),
            }
        data.loc[len(data)] = newrow

if not os.path.isfile(savefile):
    data.to_csv(savefile, index=False)
else:
    data.to_csv(savefile, mode='a', header=False, index=False)

driver.quit()
