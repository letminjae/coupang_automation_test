# Pytest Fixture 정의
# 테스트 실행 환경 설정 로직 관리

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import random
from utils.config import Config

@pytest.fixture(scope="session") # 세션 범위(제일 큰 범위)로 설정하여 *모든 테스트*에서 동일한 드라이버 인스턴스를 사용
def driver():
    """
    Selenium WebDriver 인스턴스를 초기화하고 테스트 완료 후 종료합니다.
    제공된 스크립트의 Chrome 옵션 및 사용자 에이전트 설정을 포함합니다.
    """
    chrome_options = Options()
    # 봇 감지 회피를 위한 사용자 에이전트 설정
    ua = random.choice(Config.USER_AGENTS)
    chrome_options.add_argument(f"user-agent={ua}")
    
    # Chrome 옵션 추가 - 자동화 감지 회피 및 성능 최적화
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--log-level=3")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Implicit Wait는 여기에서 한 번만 설정합니다.
    driver.implicitly_wait(Config.IMPLICIT_WAIT_TIME) 

    yield driver # driver() 를 테스트 함수들에게 제공하고, 테스트 함수 실행이 다 끝난 후에 정리 작업을 수행합니다.
    # 모든 테스트가 완료된 후, 드라이버 종료를 수행합니다.
    driver.quit()