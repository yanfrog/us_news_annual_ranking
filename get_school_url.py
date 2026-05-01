import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from time import sleep
import random
import fake_useragent as fu

from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

def _web_driver_setup():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")                          # 不開起實體瀏覽器
    options.add_argument("--start-maximized")
    options.add_argument("--incognito")
    options.add_argument("--disable-popup-blocking")    
    options.add_argument("--disable-notifications")
    options.add_argument(f"user-agent={fu.UserAgent().random}")
    driver = webdriver.Chrome(options = options)
    return driver



def get_school_urls():
    url = "https://www.usnews.com/education/best-global-universities/rankings"
    driver = _web_driver_setup()
    driver.get(url)
    sleep(5)
    while True:
        # 向下滾動一段距離以觸發動態加載
        ActionChains(driver).send_keys_to_element(driver.find_element(By.TAG_NAME, "body"), Keys.PAGE_DOWN).perform()
        sleep(2)
        school_ol = driver.find_element(By.XPATH, '//*[@id="rankings"]/ol')
        schools_list = school_ol.find_elements(By.TAG_NAME, "li")
        for school_li in schools_list:
            print(f'School: {school_li.find_element(By.TAG_NAME, "h2").text}')
            print(f'URL: {school_li.find_element(By.TAG_NAME, "a").get_attribute("href")}\n')
        driver.quit()







if __name__ == "__main__":
    get_school_urls()