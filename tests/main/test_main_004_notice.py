# [TC-MAIN-004] 최하단 Footer 공지사항 클릭 및 페이지 이동 확인

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

# 자연스러운 클릭
def human_like_click(element):
    actions.move_to_element(element).pause(random.uniform(0.2, 0.6)).click().perform()

time.sleep(random.uniform(1,3))
actions.move_by_offset(100, 100).perform()

# 스크롤 최하단까지 내리기
def scroll_to_bottom(pause_time=random.uniform(1, 3)):
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        # 스크롤 가장 아래로 내리기
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause_time)

        # 새로운 높이 측정
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  # 더 이상 로딩된 컨텐츠가 없을 경우 종료
        last_height = new_height

scroll_to_bottom()

notice = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='https://mc.coupang.com/ssr/desktop/contact/notice']")))
human_like_click(notice)

assert driver.current_url == "https://mc.coupang.com/ssr/desktop/contact/notice", "공지사항 이동 실패"
print("공지사항 페이지로 이동 성공")

driver.quit()