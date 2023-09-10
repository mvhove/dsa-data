import csv
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType
import pandas as pd
from selenium.webdriver.common.by import By
import json
import random
import os

# maeve andersen
# 27 august 2023
# scrapes from dsa website to a csv current zip codes associated with a chapter
# cuz this is for some reason (???) the best way to determine constituency

# if you don't know exactly what this is doing and the consequences, you
# should really not be using this script! there is an inherent risk of
# overloading the API. do not adjust any sleep settings except to increase
# them! i have intentionally not included the proxy list, consider it a 
# really basic "means test" of sorts for my conscience to ensure no one is
# running this out of the box.

# this will take several days to scrape depending on RNG, i suggest running it
# on an always-up server or VM.

def get_random_proxy(proxy_list):
    return random.choice(proxy_list)

def scrape_zip_code(zip_code, driver, proxy):
    proxy_url = f"http://{proxy['host']}:{proxy['port']}"
    webdriver.DesiredCapabilities.CHROME['proxy'] = {
        "httpProxy": proxy_url,
        "ftpProxy": proxy_url,
        "sslProxy": proxy_url,
        "proxyType": "MANUAL",
    }
    print(proxy_url)
    # this sucks but prevents overload
    rand = random.randint(2, 5)
    print("waiting " + str(rand))
    time.sleep(rand)
    url = f"view-source:https://chapters.dsausa.org/api/search?zip={zip_code}"
    driver.get(url)
    content = driver.page_source

    # ensure no server error
    i = 0
    while ("Internal Server Error" in driver.page_source) or ("Rate limit exceeded" in driver.page_source) or ("502: Bad gateway" in driver.page_source):
        rand = random.randint(2, 5)
        i += rand
        print("stalled for " + str(i))
        time.sleep(rand)
        proxy = get_random_proxy(proxy_list)
        proxy_url = f"http://{proxy['host']}:{proxy['port']}"
        webdriver.DesiredCapabilities.CHROME['proxy'] = {
            "httpProxy": proxy_url,
            "ftpProxy": proxy_url,
            "sslProxy": proxy_url,
            "proxyType": "MANUAL",
        }
        print(proxy_url)
        driver.get(url)
        content = driver.page_source
        if i > 600:
            print("timed out!")
            driver.quit()
            print("scraped and written!")
            exit()
    
    content = driver.find_element(By.CLASS_NAME, "line-content").text

    try:
        data = json.loads(content)
        chapter_name = data.get("data", {}).get("chapter", "Chapter not found.")
    except json.JSONDecodeError:
        chapter_name = "Chapter not found."

    return zip_code, chapter_name

# load proxies
proxy_list = []
os.chdir(os.path.dirname(os.path.abspath(__file__)))
with open("proxy_list.csv", "r", encoding="utf-8") as proxy_csv:
    reader = csv.DictReader(proxy_csv)
    for row in reader:
        proxy_list.append(row)

# my laziness knows no bounds
zip_codes = [ str(i).zfill(5) for i in range(00501, 99951) ]

# webdriver
driver = webdriver.Chrome()

# create the .csv
with open("chapter_zips.csv", "w", newline="") as csvfile:
    fieldnames = ["zip", "chapter"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()

    for zip_code in zip_codes:
        print(zip_code)
        proxy = get_random_proxy(proxy_list)
        zip_code, chapter_name = scrape_zip_code(zip_code, driver, proxy)
        if chapter_name != "Chapter not found.":
            writer.writerow({"zip": zip_code, "chapter": chapter_name})
            print(chapter_name)
        else:
            print("not written!")

driver.quit()

print("scraped and written!")