# [TC-MAIN-006] "카테고리 광고상품" Lazy Loading 처리 확인

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
import time

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

# 봇 감지로 Lazy loading 불가하기에, 회피 옵션 설정
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://www.coupang.com/")
driver.implicitly_wait(5)
wait = WebDriverWait(driver, 10)

def human_like_scroll(driver, distance, step, delay):
    current_scroll = 0
    while current_scroll < distance:
        driver.execute_script(f"window.scrollBy(0, {step});")
        current_scroll += step
        time.sleep(delay)

# DOM에 있는 카테고리 광고상품 이미지 요소
placeholder_images = driver.find_elements(By.CSS_SELECTOR, "#categoryBest_food img")
srcs_before = [img.get_attribute("src") for img in placeholder_images]

print(f"스크롤 이전 src 속성 : {srcs_before[:3]}") # 요소가 없기에 빈 array가 출력된다.

# 카테고리 광고상품 이미지 나타날 때 까지 아래로 스크롤
human_like_scroll(driver, distance=2000, step=80, delay=0.15)
time.sleep(4)

# 다시 src 속성 확인 (lazy loading)
placeholder_images_after = driver.find_elements(By.CSS_SELECTOR, "#categoryBest_food img")
srcs_after = [img.get_attribute("src") for img in placeholder_images_after]

print(f"스크롤 이후 src 속성 : {srcs_after[:3]}") # 일부만 예시로 출력

# before after 비교
assert len(srcs_after) > len(srcs_before), "lazy loading 실패"
print("Lazy loading 정상 작동 확인")