# [TC-PDP-001] 상품 상세 페이지 상품명 및 가격 정상 표시 확인 테스트코드 추가

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.117 Safari/537.36"
]
ua = random.choice(user_agents)

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument(f"user-agent={ua}")
chrome_options.add_argument("--log-level=3")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://www.coupang.com/vp/products/8335434891") # 아이폰 16 프로
driver.implicitly_wait(5)

wait = WebDriverWait(driver,10)

# 상품명 정상 출력 확인
product_name = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,".product-title span")))
assert product_name.is_displayed(), "상품명이 출력되지 않습니다."
print(f"상품명 정상 출력 확인 - {product_name.text}")

# 가격정보 정상 표시 확인
price = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"price-amount")))
assert price.is_displayed(), "가격이 출력되지 않습니다."
print(f"상품가격 정상 출력 - {price.text}")

driver.quit()