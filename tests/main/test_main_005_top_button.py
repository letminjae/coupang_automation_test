# [TC-MAIN-005] 우측 하단 Top Button 동작 확인

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

# 랜덤 슬립
def sleep_moving(random_time = random.uniform(3,5)):
    time.sleep(random_time)

# 봇 감지 회피를 위한 의미없는 무빙
sleep_moving(random_time = random.uniform(1,3))
actions.move_by_offset(random.uniform(10, 100), random.uniform(10, 100)).perform()

# 스크롤을 랜덤하게 내리기
driver.execute_script(f"window.scrollTo(0, {random.uniform(800, 1200)})")
sleep_moving()
new_height = driver.execute_script("return document.body.scrollHeight")
driver.execute_script(f"window.scrollTo({new_height}, {new_height + random.uniform(800, 1200)})")

# Top Button 표시 확인한다.
top_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "goto-top__button")))

# Top Button을 클릭한다.
def human_like_click(element):
    actions.move_to_element(element).pause(random.uniform(0.2, 0.6)).click().perform()

human_like_click(top_button)

sleep_moving()

# 위쪽 상단까지 스크롤이 올라갔는지 확인
scroll_y = driver.execute_script("return window.scrollY")
assert scroll_y == 0, "Top Button 동작 실패"
print("Top button 정상 작동 확인 완료")

driver.quit()