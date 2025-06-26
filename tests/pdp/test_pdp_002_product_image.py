# [TC-PDP-002] 메인 이미지 정상 출력 및 이미지 변경 확인

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

# 메인 이미지 표시되는지 확인
main_image = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "img[alt='Product image']")))
assert main_image.is_displayed(), "메인 이미지 표시되지 않음"

# hover 시 메인 이미지가 변경되는지 확인
thumbnail_images = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.twc-w-[70px] li")))

for index, thumbnail in enumerate(thumbnail_images):
    img_tag = thumbnail.find_element(By.TAG_NAME, "img")
    thumbnail_src = img_tag.get_attribute("src").replace("48x48ex", "492x492ex") # main_image와 같게 사이즈 조정

    actions.move_to_element(thumbnail).perform()
    random_sleep()

    current_main_src = main_image.get_attribute("src")

    print(f"[{index+1}번] 썸네일 이미지(사이즈 조정) : {thumbnail_src}")
    print(f"[{index+1}번] 메인 이미지 : {current_main_src}")

    assert thumbnail_src in current_main_src, '메인 이미지와 썸네일 이미지가 같지 않음'

print("모든 썸네일 hover 시, 메인 이미지로 정상 표시")

driver.quit()