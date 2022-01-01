
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np
import os
import time
from has_numbers import has_numbers
from selenium.webdriver.chrome.service import Service

def getListItems(popup_modal):
    text_list = []
    list_items = popup_modal.find_elements(By.CLASS_NAME, 'list-group-item')
    for item in list_items:
        item_title = item.text
        if has_numbers(item_title):
            text_list.append(item_title)
    return text_list

if __name__ == "__main__":
    s = os.path.dirname(os.path.abspath(__file__))+"/chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options,executable_path=s)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
    print(driver.execute_script("return navigator.userAgent;"))
    url_main='https://www.britishnewspaperarchive.co.uk/search/results/1918-01-01/1918-12-31?basicsearch=%2bminer%20%2binjured&freesearch=miner%20injured&retrievecountrycounts=false'
    driver.get(url_main)
    time.sleep(5)
    try:
        driver.find_element(By.ID, 'onetrust-accept-btn-handler').click()
    except:
        pass

    time.sleep(2)
    driver.execute_script("window.scrollTo(0, 2000)")
    #Counties and Places finder

    modals = driver.find_elements(By.CLASS_NAME, 'list-group-item.btn.btn-default.btn-sm')

    for elem in modals:
        elem_title = elem.get_attribute('title')
        if 'Counties' in elem_title:
            county_modal = elem
        if 'Place' in elem_title:
            place_modal = elem

    place_modal.click()
    time.sleep(2)

    # Get modal class
    popup_modal = driver.find_element(By.CLASS_NAME, 'ui-dialog-content.ui-widget-content')
    text_list=[]

    # Begin gathering data
    nav_buttons = popup_modal.find_element(By.CLASS_NAME, 'pagination.pagination-lg')
    modal_buttons = nav_buttons.find_elements(By.TAG_NAME, 'li')
    last_button = modal_buttons[-1].find_element(By.TAG_NAME, 'a')
    text_list += getListItems(popup_modal)
    while not has_numbers(last_button.text):
        last_button.click()
        time.sleep(3)
        nav_buttons = popup_modal.find_element(By.CLASS_NAME, 'pagination.pagination-lg')
        modal_buttons = nav_buttons.find_elements(By.TAG_NAME, 'li')
        last_button = modal_buttons[-1].find_element(By.TAG_NAME, 'a')
        text_list += getListItems(popup_modal)

    df = {'Place':[], 'County':[], 'Country':[], 'Number_Reports':[]}
    for text in text_list:
        step1=text.split(", ")
        df['Place'].append(step1[0])
        df['County'].append(step1[1])
        step2 = step1[2].split(' ')
        df['Country'].append(step2[0])
        df['Number_Reports'].append(int(''.join([s for s in step2[-1] if s.isdigit()])))

    # Converting to excel
    df = pd.DataFrame(df)
    df.to_csv('miner_injured.csv', index = False)




