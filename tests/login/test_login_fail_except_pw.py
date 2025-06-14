# [TC-LOGIN-004] 비밀번호 입력 없이 로그인 시도

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
import os
from dotenv import load_dotenv
import time

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

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

login_button = driver.find_element(By.CLASS_NAME, "login")
login_button.click()

load_dotenv() # .env 파일 로드
id_input = driver.find_element(By.ID, "login-email-input")

id_input.send_keys(os.environ.get("COUPANG_ID"))

login_submit = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
login_submit.click()

time.sleep(1)

error_element = driver.find_element(By.CSS_SELECTOR, ".member__message-area.member__message-area--error._loginPasswordError.login-fail-web-log-error-msg")

assert "비밀번호를 입력해주세요." in error_element.text  # 비밀번호 입력 필드에 대한 에러 메시지 확인

print("비밀번호 입력 제외 테스트 완료")
driver.quit()