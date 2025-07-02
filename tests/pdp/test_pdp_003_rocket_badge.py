# [TC-PDP-003] 로켓배송 정보 영역 확인

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
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
actions = ActionChains(driver)

# 랜덤 슬립
def random_sleep(random_time = random.uniform(1,3)):
    time.sleep(random_time)

# 봇 감지 회피를 위한 의미없는 무빙
random_sleep()
actions.move_by_offset(random.uniform(10, 100), random.uniform(10, 100)).perform()

# 배송방식 (로켓배송/판매자배송) 상품페이지에 표시되는지 확인
rocket_badge = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.price-badge img")))
assert rocket_badge.is_displayed(), "로켓 배송 뱃지 미표시"

driver.quit()