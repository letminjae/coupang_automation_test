# [TC-PDP-005] 상품 옵션 적용 확인

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

# 옵션 드롭다운 확인
option_pickers = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.option-picker-select")))

def human_like_click(element):
    actions.move_to_element(element).pause(random.uniform(0.2, 0.6)).click().perform()

# 옵션 선택
for index, option in enumerate(option_pickers):
    human_like_click(option)
    random_sleep()

    first_li = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"ul.custom-scrollbar > li:first-child")))
    human_like_click(first_li)
    random_sleep()
    
    # 첫번째 옵션의 내용이 상품에 반영되는지 확인
    assert first_li.text in option.text, "옵션 반영 실패"
    print(f"상품 {index+1}번 옵션 변경 테스트 성공")

driver.quit()