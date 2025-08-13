# Pytest Fixture 정의
# 테스트 실행 환경 설정 로직 관리

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import random
from utils.config import Config

# 1. 모든 테스트를 위한 기본 드라이버 (session 스코프)
# 봇 감지에 덜 민감한 테스트들은 이 드라이버를 사용합니다.
@pytest.fixture(scope="session")
def driver():
    """
    Selenium WebDriver 인스턴스를 초기화하고 테스트 완료 후 종료합니다.
    제공된 스크립트의 Chrome 옵션 및 사용자 에이전트 설정을 포함합니다.
    """
    print("\n--- 기본 웹드라이버 세션 시작 ---")
    chrome_options = Options()
    
    # 모든 테스트가 공유할 안정적인 User-Agent로 고정
    # 모바일 UA가 안정적이므로 아래 UA를 기본으로 사용
    stable_ua = "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36"
    chrome_options.add_argument(f"user-agent={stable_ua}")
    print(f"기본 Driver 사용 UA: {stable_ua}")
    
    # Jenkins 환경의 언어 설정과 일치시키거나, 일반적인 브라우저 설정을 사용 - 봇처럼 안보이도록 설정
    chrome_options.add_argument("Accept-Language=ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7")
    
    # Chrome 옵션 추가 - 자동화 감지 회피 및 성능 최적화
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument('--disable-gpu') # GPU 사용 중지
    chrome_options.add_argument('--disable-extensions') # 브라우저 확장 프로그램 사용 중지
    chrome_options.add_argument('--proxy-server="direct://"') # 프록시 사용 안 함
    chrome_options.add_argument('--proxy-bypass-list=*')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Implicit Wait는 여기에서 한 번만 설정합니다.
    driver.implicitly_wait(Config.IMPLICIT_WAIT_TIME)

    yield driver # driver() 를 테스트 함수들에게 제공하고, 테스트 함수 실행이 다 끝난 후에 정리 작업을 수행합니다.
    # 모든 테스트가 완료된 후, 드라이버 종료를 수행합니다.
    driver.quit()
    
# 2. PDP 테스트를 위한 전용 드라이버 (function 스코프)
# 봇 감지에 취약한 PDP 테스트는 이 드라이버를 사용
@pytest.fixture(scope="function")
def pdp_driver():
    """
    PDP 테스트를 위한 Selenium WebDriver 인스턴스를 테스트마다 초기화하고 종료
    각 PDP 테스트가 독립적으로 실행
    """
    print("\n--- PDP 테스트용 웹드라이버 세션 시작 ---")
    chrome_options = Options()
    
    # 랜덤한 모바일 User-Agent 설정
    user_agent = random.choice(Config.USER_AGENTS)
    chrome_options.add_argument(f"user-agent={user_agent}")
    print(f"PDP Driver 사용 UA: {user_agent}")
    
    # Jenkins 환경의 언어 설정과 일치시키거나, 일반적인 브라우저 설정을 사용 - 봇처럼 안보이도록 설정
    chrome_options.add_argument("Accept-Language=ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7")
    
    # Chrome 옵션 추가 - 자동화 감지 회피 및 성능 최적화
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument('--disable-gpu') # GPU 사용 중지
    chrome_options.add_argument('--disable-extensions') # 브라우저 확장 프로그램 사용 중지
    chrome_options.add_argument('--proxy-server="direct://"') # 프록시 사용 안 함
    chrome_options.add_argument('--proxy-bypass-list=*')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Implicit Wait는 여기에서 한 번만 설정합니다.
    driver.implicitly_wait(Config.IMPLICIT_WAIT_TIME)

    yield driver # driver() 를 테스트 함수들에게 제공하고, 테스트 함수 실행이 다 끝난 후에 정리 작업을 수행합니다.
    # 모든 테스트가 완료된 후, 드라이버 종료를 수행합니다.
    driver.quit()