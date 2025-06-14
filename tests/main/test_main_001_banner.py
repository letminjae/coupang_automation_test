# [TC-MAIN-001] 쿠팡 메인 페이지 배너 테스트

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
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

driver.get("https://www.coupang.com/")
driver.implicitly_wait(5)

# 배너 이미지들
banners = driver.find_elements(By.CSS_SELECTOR, ".main-today__bg")

# 현재 보여지는 배너 찾기
def get_visible_banner_index():
    for idx, banner in enumerate(banners):
        if banner.is_displayed():
            return idx
    return -1

# 슬라이드 자동 전환 확인
first_index = get_visible_banner_index()
print("첫 배너 인덱스:", first_index)

time.sleep(3)  # 슬라이드 자동 전환 대기

second_index = get_visible_banner_index()
print("다음 배너 인덱스:", second_index)

assert first_index != second_index, "배너가 자동으로 전환되지 않았습니다."
driver.quit()