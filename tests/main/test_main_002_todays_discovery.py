# [TC-MAIN-002] "오늘의 발견" 이미지 및 리스트 표시 확인

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
wait = WebDriverWait(driver, 10)

#스크롤 내리기
driver.execute_script("window.scrollTo(0, 800)")
time.sleep(3)

# 오늘의 발견 section 확인
try:
    discovery_section = wait.until(EC.presence_of_element_located((By.ID, "todayDiscoveryUnit")))
    images = discovery_section.find_elements(By.CSS_SELECTOR, ".tti-image")

    # 이미지 표시 여부 확인
    loaded_images = [img for img in images if img.is_displayed() and img.get_attribute("src")]

    assert len(loaded_images) > 0, "오늘의 발견 이미지가 로드되지 않았습니다."
    print(f"로드된 오늘의 발견 이미지 수 : {len(loaded_images)}")
    print("오늘의 발견 이미지 및 리스트 정상 표시")

except Exception as E:
    print(f"오늘의 발견 영역을 찾을 수 없습니다. - {E}")

driver.quit()