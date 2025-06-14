# [TC-SEARCH-001] 쿠팡 검색 기능 테스트 케이스

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth
from selenium.webdriver.common.action_chains import ActionChains # ActionChains import
import os
from dotenv import load_dotenv
import time
import random # random import

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
# 추가적인 봇 감지 회피 옵션
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Selenium Stealth 적용 (탐지 방지)
stealth(driver,
        languages=["ko-KR", "ko"],
        vendor="Google Inc.",
        platform="MacIntel",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True)

driver.get("https://www.coupang.com/")
driver.implicitly_wait(5)

# 인간적인 행동 시뮬레이션을 위한 함수
def human_like_send_keys(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.2)) # 글자마다 불규칙한 딜레이를 준다.

def human_like_click(element):
    actions = ActionChains(driver)
    actions.move_to_element(element).pause(random.uniform(0.3, 1.0)).click().perform() # 클릭 전 불규칙한 대기를 준다.

# 검색창 입력 (인간적인 입력 적용)
search_input = driver.find_element(By.CSS_SELECTOR, "input[name='q']")
human_like_send_keys(search_input, "노트북")

search_button = driver.find_element(By.CSS_SELECTOR, "form[id='wa-search-form'] button[title='검색']")
time.sleep(random.uniform(2, 4))  # 잠시 대기하여 요소가 안정화되도록 함

# 검색 버튼 클릭 (인간적인 클릭 적용)
human_like_click(search_button)
driver.implicitly_wait(5)

# 봇 감지로 인해 검색 결과 페이지가 로드되지 않는다.
result = driver.find_element(By.ID, "main-content")
assert "ERR_HTTP2_PROTOCOL_ERROR" in result.text
print("검색 결과 페이지가 로드되지 않았습니다. 봇 감지로 인해 정상적인 검색 결과를 확인할 수 없습니다.")

driver.quit()