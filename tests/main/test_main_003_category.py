# [TC-MAIN-003] 상단 카테고리 페이지 이동 동작 확인

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

driver.get("https://www.coupang.com/")
driver.implicitly_wait(5)

wait = WebDriverWait(driver, 10)
actions = ActionChains(driver)

# 자연스러운 Hover
def human_like_hover(element):
    actions.move_to_element(element).pause(random.uniform(0.4, 0.9)).perform()

# 자연스러운 클릭
def human_like_click(element):
    actions.move_to_element(element).pause(random.uniform(0.2, 0.6)).click().perform()

time.sleep(random.uniform(1,3))
actions.move_by_offset(100, 100).perform()

# Mouse Hover
category_menu = driver.find_element(By.CSS_SELECTOR, "#wa-category")
human_like_hover(category_menu)
time.sleep(random.uniform(0.8, 1.5))

appliance_digital = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "가전디지털")))
human_like_click(appliance_digital)

# 가전디지털 페이지로 이동했는지 확인
wait.until(EC.title_contains("가전디지털"))
assert "가전디지털" in driver.title, "가전디지털 페이지 이동 실패"
print("가전디지털 페이지 이동 성공")

driver.quit()