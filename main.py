
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np
import time
from has_numbers import has_numbers
from selenium.webdriver.chrome.service import Service
s = r"C:/Users/Zacha/PycharmProjects/ScrapingBNA2/chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options,executable_path=s)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
print(driver.execute_script("return navigator.userAgent;"))
url_main='https://www.britishnewspaperarchive.co.uk/search/results/1918-01-01/1918-12-31?basicsearch=%2bminer%20%2binjured&freesearch=miner%20injured&retrievecountrycounts=false'
driver.get(url_main)
time.sleep(10)
try:
    driver.find_element_by_id('onetrust-accept-btn-handler').click()
except:
    pass

time.sleep(2)
driver.execute_script("window.scrollTo(0, 2000)")
#Counties and Places finder
modals = driver.find_elements(By.CLASS_NAME,'list-group-item btn btn-default btn-sm')

for elem in modals:
    elem_title=elem.getattribute('title')
    if 'Counties' in elem_title:
        county_modal=elem
    if 'Place' in elem_title:
        place_modal=elem

county_modal.click()
time.sleep(2)

nav_buttons=driver.find_elements_by_class_name('paginator')
modal_buttons=[]
for button in nav_buttons:
    try:
        button_type=button.getattribute('data-target')
        modal_buttons.append(button)
    except:
        continue
time.sleep(2)
text_list=[]
while (True):
    try:
        list_items = driver.find_elements_by_class_name('list-group-item')
        for item in list_items:
            item_title = item.get_attribute('title')
            if has_numbers(item_title)==True:
                text_list.append(item_title)
        modal_buttons[-1].click()
    except:
        break

county_list=[]
country_list=[]
number_reports=[]
for text in text_list:
    step1=text.split(", ")
    county_list.append(step1[0])
    step2=step1[1].split(" (")
    country_list.append(step2[0])
    number_report=[int(s) for s in step2[1].split() if s.isdigit()]
    number_reports.append(number_report)


df = pd.DataFrame()
df['County'] = county_list
df['Country']= country_list
df['Number_Reports'] = number_reports

# Converting to excel
df.to_excel('miner_injured.xlsx', index = False)




