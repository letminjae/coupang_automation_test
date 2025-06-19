# [TC-MAIN-001] 쿠팡 메인 페이지 배너 테스트

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option("detach", True)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://www.coupang.com/")
driver.implicitly_wait(5)

# 현재 보여지는 배너 찾기
def get_visible_banner_index():
    banners = driver.find_elements(By.CSS_SELECTOR, ".main-today__bg")
    for idx, banner in enumerate(banners):
        try:
            if banner.is_displayed():
                return idx
        except Exception as e:
            print(f"배너 {idx} 확인 중 예외 발생 : {e}")
    return -1

# 슬라이드 자동 전환 확인
first_index = get_visible_banner_index()
print("첫 배너 인덱스:", first_index)

time.sleep(3)  # 슬라이드 자동 전환 대기

second_index = get_visible_banner_index()
print("다음 배너 인덱스:", second_index)

assert first_index != second_index, "배너가 자동으로 전환되지 않았습니다."
driver.quit()
