# [TC-LOGIN-003] 이메일 입력 없이 로그인 시도

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
import os
from dotenv import load_dotenv
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

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
password_input = driver.find_element(By.ID, "login-password-input")

password_input.send_keys(os.environ.get("COUPANG_PW"))

login_submit = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
login_submit.click()

time.sleep(1)

error_element = driver.find_element(By.CSS_SELECTOR, ".member__message-area.member__message-area--error._memberInputMessage.login-fail-web-log-error-msg")

assert "아이디(이메일)를 입력해주세요." in error_element.text  # 이메일 입력 필드에 대한 에러 메시지 확인

print("이메일 입력 제외 테스트 완료")
driver.quit()