# [TC-SEARCH-001] 쿠팡 검색 기능 테스트 케이스

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth
import os
from dotenv import load_dotenv

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option("detach", True)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Selenium Stealth 적용 (탐지 방지)
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True)

driver.get("https://www.coupang.com/")
driver.implicitly_wait(5)

login_button = driver.find_element(By.CSS_SELECTOR, "a[title='로그인']")
login_button.click()

load_dotenv() # .env 파일 로드

id_input = driver.find_element(By.ID, "login-email-input")
password_input = driver.find_element(By.ID, "login-password-input")

id_input.send_keys(os.environ.get("COUPANG_ID"))
password_input.send_keys(os.environ.get("COUPANG_PW"))

login_submit = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
login_submit.click()
driver.implicitly_wait(5)