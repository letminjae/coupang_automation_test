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
        print("--- 로그인 테스트 완료 후 쿠키 삭제 ---")
        # 현재 브라우저의 모든 쿠키를 삭제하여 로그인 상태 등 세션 정보를 초기화
        driver.delete_all_cookies()
        print("브라우저 쿠키 삭제 완료.")

        
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
        
    # 잘못된 비밀번호, 잘못된 ID, 비밀번호 미입력 등 다양한 로그인 실패 시나리오를 테스트 (parametrize 사용)
    @pytest.mark.parametrize("email, password, expected_error_message", [
        (config.COUPANG_ID, "wrong123456", "이메일 또는 비밀번호가 올바르지 않습니다. 다시 확인해주세요."), # TC-LOGIN-002: 잘못된 비밀번호
        ("", config.COUPANG_PW, "아이디(이메일)를 입력해주세요."),  # TC-LOGIN-003: 이메일 미입력
        (config.COUPANG_ID, "", "비밀번호를 입력해주세요."),  # TC-LOGIN-004: 비밀번호 미입력
        ("zzzz.1234", config.COUPANG_PW, "아이디는 이메일 형식으로 입력해주세요."), # TC-LOGIN-005: 잘못된 이메일 형식
    ])
    def test_invalid_login_scenarios(self, driver, email, password, expected_error_message):
        """
        [TC-LOGIN-002 ~ TC-LOGIN-005] 쿠팡 로그인 실패 테스트 케이스
        잘못된 비밀번호, 이메일 미입력, 비밀번호 미입력, 잘못된 이메일 형식 등 다양한 시나리오를 테스트
        """
        print("LOGIN 002 ~ 005 테스트: 잘못된 정보로 로그인 시도")
        
        # 로그인 페이지 객체 생성
        login_page = LoginPage(driver)
        
        # 로그인 시도
        login_page.login(email, password)
        
        # 오류 메시지 확인
        assert login_page.is_error_message_displayed(), "오류 메시지가 표시되지 않습니다."
        
        # 실제 오류 메시지와 예상 메시지 비교
        actual_error_message = login_page.get_error_message()
        assert actual_error_message == expected_error_message, f"예상 오류 메시지: '{
            expected_error_message}', 실제 오류 메시지: '{actual_error_message}'"
        
        print(f"로그인 실패 테스트 완료: {actual_error_message} 오류 메시지 확인")