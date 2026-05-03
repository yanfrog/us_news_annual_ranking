import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from time import sleep
import random
import fake_useragent as fu
import json
from urllib3.util import Retry, Timeout

from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType
from selenium.webdriver.remote.client_config import ClientConfig
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def _web_driver_setup(url):
    options = webdriver.ChromeOptions()
    options.browser_version = 'stable'
    # options.add_argument("--headless")                            # 不開起實體瀏覽器
    options.add_argument("--start-maximized")
    # options.add_argument("--incognito")
    # options.add_argument("--disable-popup-blocking")                # 禁止彈出窗口
    options.add_argument("--disable-notifications")                 # 禁止通知
    # options.add_experimental_option("detach", True)                 # 讓瀏覽器在程式結束後繼續運行
    options.add_experimental_option('excludeSwitches', ['disable-popup-blocking']) # 允許彈出窗口
    options.add_argument(f"--user-agent={fu.UserAgent().random}")
    # Local ChromeDriver path
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(1)
    print("Web driver initialized.")
    while True:        
        try:
            driver.get(url)
            print(f"Successfully navigated to {url}")
            break
        except Exception as e:
            print(f"Error navigating to {url}: {e}. Retrying...")
            sleep(3)
    print(f"Navigated to {url}")
    with open("cookies.json", "r") as f:
        cookies = json.load(f)
        for cookie in cookies:
            if cookie['sameSite'] not in ["strict", "lax", "none"]:
                if cookie['sameSite'] == 'unspecified':
                    cookie['sameSite'] = "None"
                elif cookie['sameSite'] == 'no_restriction':
                    cookie['sameSite'] = "None"
                cookie['sameSite'] = cookie['sameSite'].capitalize()
                driver.add_cookie(cookie)
    return driver



def get_school_urls():
    url = "https://www.usnews.com/education/best-global-universities/rankings"
    driver = _web_driver_setup(url)
    print("Web driver setup complete.")
    # 等待底部 Privacy Policy 加載完成
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "onetrust-pc-btn-handler"))
        )
    if driver.find_elements(By.ID, "onetrust-pc-btn-handler"):
        driver.find_element(By.ID, "onetrust-pc-btn-handler").click()
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".save-preference-btn-handler.onetrust-close-btn-handler"))
        )
    if driver.find_elements(By.CSS_SELECTOR, ".save-preference-btn-handler.onetrust-close-btn-handler"):
        driver.find_element(By.CSS_SELECTOR, ".save-preference-btn-handler.onetrust-close-btn-handler").click()
    # 關閉 Create Account 彈窗
    while True:
        try:
            create_acc = driver.find_element(By.CSS_SELECTOR, ".MuiModal-root")
            sleep(1)
            driver.execute_script("arguments[0].parentNode.removeChild(arguments[0]);", create_acc)
            print("Closed 'Create Account' window.")
            break
        except:
            continue
    '''
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".MuiButtonBase-root.MuiIconButton-root.MuiIconButton-sizeMedium.css-ub2qep"))
        )
    if driver.find_elements(By.CSS_SELECTOR, ".MuiButtonBase-root.MuiIconButton-root.MuiIconButton-sizeMedium.css-ub2qep"):
        driver.find_element(By.CSS_SELECTOR, ".MuiButtonBase-root.MuiIconButton-root.MuiIconButton-sizeMedium.css-ub2qep").click()
    '''
    '''
    # 縮小右下角 AI 聊天窗口
    ai_chat_expanded = "zls-sptwndw siqembed siqtrans zsiq-mobhgt zsiq-newtheme mobile-device siq_rht zsiq_size2 siqanim"
    ai_chat_expanded_css = ai_chat_expanded.replace(" ", ".")
    ai_chat_collapse = 'zls-sptwndw siqembed siqtrans zsiq-mobhgt zsiq-newtheme mobile-device siq_rht zsiq_size2'
    ai_chat_collapse_css = ai_chat_collapse.replace(" ", ".")
    chat_window = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, f".{ai_chat_expanded_css}"))
        )
    print("Minimizing AI chat window.")
    sleep(1)
    driver.execute_script("arguments[0].className = arguments[1];", chat_window, ai_chat_collapse)
    '''
    # 進入頁面後，持續滾動直到無法再加載更多內容
    while True:
        # 等待 Footer 加載完成
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".Footer__Wrapper-efmc92-0.XLfAG")))
        last_height = driver.execute_script("return document.body.scrollHeight")
        footer = driver.find_element(By.CSS_SELECTOR, ".Footer__Wrapper-efmc92-0.XLfAG")
        # 滾動到頁面底部以觸發加載更多內容
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        '''
        load_more = driver.find_elements(By.ID, "load-more-button")
        if load_more:
            load_more[0].click()
        '''
        try:
            # 等待 "Load More" 按鈕變為可點擊狀態
            load_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "load-more-button"))
            )
            # 使用 JavaScript 執行點擊，以避免被攔截
            driver.execute_script("arguments[0].click();", load_more_button)
            print("Clicked 'Load More' button.")

            # 等待新內容加載，直到頁面高度增加
            WebDriverWait(driver, 15).until(
                lambda d: d.execute_script("return document.body.scrollHeight") > last_height
            )
        except Exception as e:
            print(f"No more 'Load More' button or content failed to load. Exiting loop. Error: {e}")
            break  # 如果找不到按鈕或超時，則跳出迴圈
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".Footer__Wrapper-efmc92-0.XLfAG")))
        new_height = driver.execute_script("return document.body.scrollHeight")
        print(f"New page height after scrolling: {new_height}")
        if new_height == last_height:
            break
        last_height = new_height

    # 取得學校列表
    school_ol = driver.find_element(By.XPATH, '//*[@id="rankings"]/ol')
    schools_list = school_ol.find_elements(By.TAG_NAME, "li")
    print(f"Total schools found: {len(schools_list)}")
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
    return len(schools_list)




if __name__ == "__main__":
    num_schools = get_school_urls()
    print(f"Total number of schools found: {num_schools}")