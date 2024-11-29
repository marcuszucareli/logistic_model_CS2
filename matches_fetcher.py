"""
This file was used to fetch all the matches from the ESL Pro League Season 20.

The links to the matches will be used to extract the data we will work on.
"""

import time
import random
import pandas as pd
import undetected_chromedriver as uc

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome()

url = 'https://www.hltv.org/results?startDate=2024-01-01&endDate=2024-12-31&content=stats&event=7441'

driver.get(url)
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, f"//div[@data-zonedgrouping-entry-unix='1725369904000']")))
hrefs = driver.find_elements(By.CSS_SELECTOR, 'div.result-con a')

driver.quit()

df = pd.DataFrame(hrefs, columns=['links'])
df.to_csv('matches.csv', index=False)

driver = uc.Chrome()
stats_url = []
for url in hrefs:

    driver.get(url)

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, f"div.small-padding.stats-detailed-stats a")))

    element = driver.find_element(By.CSS_SELECTOR, 'div.small-padding.stats-detailed-stats a')

    stats_url.append(element.get_attribute('href'))
    
    time.sleep(random.randint(1, 8))
    
driver.quit()

df = pd.DataFrame(stats_url, columns=['links'])
df.to_csv('matches_stats.csv', index=False)

