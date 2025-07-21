import pytest
from pages.main_page import MainPage
from pages.login_page import LoginPage
from utils.config import config_instance as config

class TestLoginScenarios:
    """
    쿠팡 로그인 기능에 대한 다양한 시나리오를 테스트합니다.
    (성공 로그인, 잘못된 ID/PW, ID/PW 미입력 등)
    """
    
    # 각 테스트 함수 실행 전에 공통적으로 로그인 페이지로 이동하는 fixture
    # autouse=True를 사용하면 이 클래스 내의 모든 테스트 함수에 자동으로 적용
    @pytest.fixture(autouse=True)
    def setup_for_login_tests(self, driver):
        """
        각 로그인 테스트가 시작되기 전에 메인 페이지로 이동 후 로그인 페이지로 진입합니다.
        """
        print("\n--- 로그인 테스트 Setup ---")
        main_page = MainPage(driver)
        main_page.go_to_url(config.BASE_URL) # 기본 URL로 이동
        main_page.move_mouse_randomly() # 봇 감지 회피
        
        # 메인 페이지에서 로그인 버튼 클릭하여 로그인 페이지로 진입
        main_page.click_login_button()
        
        # 로그인 페이지 객체 생성
        login_page_instance = LoginPage(driver)
        
        yield # 여기서 테스트 함수가 실행된다.
        
        # 각 테스트 후 필요한 정리 작업이 있다면 여기에 추가 (예: 로그아웃, 쿠키 삭제 등)
        # 현재는 driver.quit()은 conftest.py의 session scope fixture에서 처리
        
    def test_successful_login(self, driver):
        """
        [TC-LOGIN-001] 쿠팡 로그인 성공 테스트 케이스
        메인 페이지에서 로그인 버튼 클릭 -> 로그인 페이지에서 ID/PW 입력 -> 로그인 버튼 클릭 -> 마이쿠팡 링크 확인
        """
        print("LOGIN 001 테스트: 유효한 정보로 로그인 시도")
        # 로그인 정보 입력 및 로그인 시도
        id = config.COUPANG_ID
        pw = config.COUPANG_PW
        
        login_page = LoginPage(driver)
        login_page.login(id, pw)
        
        # 로그인 성공 확인
        main_page = MainPage(driver)
        assert main_page.is_my_coupang_link_displayed(), "로그인 성공 후 '마이쿠팡' 링크가 표시되지 않습니다."
        assert main_page.get_my_coupang_link_text() == "마이쿠팡", "'마이쿠팡' 링크 텍스트가 올바르지 않습니다."
        
        print("로그인 성공 테스트 완료: 마이쿠팡 링크 확인")