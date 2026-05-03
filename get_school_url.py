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
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def _web_driver_setup():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")                            # 不開起實體瀏覽器
    options.add_argument("--start-maximized")
    options.add_argument("--incognito")
    options.add_argument("--disable-popup-blocking")                # 禁止彈出窗口
    options.add_argument("--disable-notifications")                 # 禁止通知
    options.add_experimental_option("detach", True)                 # 讓瀏覽器在程式結束後繼續運行
    options.add_argument(f"user-agent={fu.UserAgent().random}")
    driver = webdriver.Chrome(options = options)
    ac = ActionChains(driver)
    return driver, ac



def get_school_urls():
    url = "https://www.usnews.com/education/best-global-universities/rankings"
    driver, ac = _web_driver_setup()
    driver.get(url)
    sleep(30)  # 等待頁面加載完成
    # 取消登入彈窗
    signin = driver.find_elements(By.CSS_SELECTOR, ".MuiButtonBase-root.MuiIconButton-root.MuiIconButton-sizeMedium.css-ub2qep")
    if signin:
        signin[0].click()
    # 右下角聊天
    chat = driver.find_elements(By.CSS_SELECTOR, ".win_close.sqico-larrow")
    if chat:
        chat[0].click()
    # 
    last_height = driver.execute_script("return document.body.scrollHeight")
    print(last_height)
    while True:
        footer = driver.find_element(By.CSS_SELECTOR, ".Footer__Wrapper-efmc92-0.XLfAG")
        driver.execute_script("arguments[0].scrollIntoView();", footer)
        # driver.execute_script("window.scrollBy(0, 10000);")
        sleep (random.uniform(2, 4))  # 等待頁面加載完成
        '''
        load_more = driver.find_elements(By.CSS_SELECTOR, ".button__ButtonStyled-sc-1vhaw8r-1.bGXiGV.pager__ButtonStyled-sc-1i8e93j-1.dypUdv.type-secondary.size-large")
        if load_more and load_more[0].is_displayed():
            load_more[0].click()
        retry_button = driver.find_elements(By.CSS_SELECTOR, ".message-box__Action-sc-7sukoj-2.iZynkP")
        if retry_button:
            retry_button[0].click()
            continue
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # sleep(random.uniform(2, 4))
        '''
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # 取得學校列表
    school_ol = driver.find_element(By.XPATH, '//*[@id="rankings"]/ol')
    schools_list = school_ol.find_elements(By.TAG_NAME, "li")
    for school_li in schools_list:
        # 過濾掉廣告或非學校的元素
        if school_li.find_elements(By.TAG_NAME, 'aside'):
            continue
        # 提取學校名稱和URL
        tag_a = school_li.find_elements(By.CSS_SELECTOR, '.Anchor-byh49a-0.DetailCardGlobalUniversities__StyledAnchor-sc-1v60hm5-5.gzdPVF.bFdMFJ')
        if not tag_a:
            continue
        school_name = tag_a[0].text
        school_url = tag_a[0].get_attribute('href')
        print(f'School: {school_name}')
        print(f'URL: {school_url}\n')




if __name__ == "__main__":
    get_school_urls()