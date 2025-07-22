import pytest
from pages.main_page import MainPage
from utils.config import config_instance as config

class TestMainScenarios:
    """
    쿠팡 메인 페이지의 다양한 기능에 대한 시나리오를 테스트합니다.
    (배너, 오늘의 발견 등)
    """
    
    @pytest.fixture(autouse=True)
    def setup_for_main_tests(self, driver):
        """
        각 메인 페이지 테스트가 시작되기 전에 메인 페이지로 이동합니다.
        """
        print("\n--- 메인 페이지 테스트 Setup ---")
        self.main_page = MainPage(driver) # 클래스 인스턴스 변수로 저장, 다른 테스트 함수에서 사용
        self.main_page.go_to_url(config.BASE_URL)
        self.main_page.move_mouse_randomly() # 봇 감지 회피
        
        yield  # 테스트 함수 실행
        
        # 각 테스트 후 필요한 정리 작업이 있다면 여기에 추가