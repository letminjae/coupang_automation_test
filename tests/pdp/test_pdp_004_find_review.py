# [TC-PDP-004] 리뷰 영역 확인

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
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

def human_like_click(element):
    actions.move_to_element(element).pause(random.uniform(0.2, 0.6)).click().perform()

last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    try:
        review_element = driver.find_element(By.XPATH,"//a[contains(text(), '상품평')]")
        print("리뷰 요소를 찾았습니다!")
        
        human_like_click(review_element)
        random_sleep()
        break

    except NoSuchElementException:
        print('요소를 못 찾아 스크롤 합니다.')

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        random_sleep()

        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            print("맨 아래까지 내렸지만 리뷰요소를 못 찾았어요")
            break
        last_height = new_height

review_header = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.review-header")))
assert review_header.is_displayed(), "상품평 로딩 실패"
print("상품평 화면 표시 성공")
driver.quit()