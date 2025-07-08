# [TC-LOGIN-004] 비밀번호 입력 없이 로그인 시도

import pytest
from pages.main_page import MainPage
from pages.login_page import LoginPage
from utils.config import config_instance as config

class TestLogin004EmptyPassword:
    def test_empty_password_login_to_coupang(self, driver):
        """
        메인 페이지에서 로그인 버튼 클릭 -> 로그인 페이지에서 빈 비밀번호 입력 (ID는 올바르게 입력) -> 로그인 버튼 클릭 -> 에러메시지 확인
        """
        # 1. 메인 페이지 객체 생성 및 기본 URL 이동
        main_page = MainPage(driver)
        
        # 봇 감지 회피를 위한 초기 무빙
        main_page.move_mouse_randomly()

        # 2. 메인 페이지에서 로그인 버튼 클릭
        main_page.click_login_button()
        
        # 3. 로그인 페이지 객체 생성
        login_page = LoginPage(driver)
        
        # 4. 로그인 정보 입력 및 로그인 시도
        id = config.COUPANG_ID
        pw = ""  # 빈 비밀번호 입력

        login_page.login(id, pw)
        
        # 5. 에러 메시지 확인
        assert login_page.is_password_error_message_displayed, "입력 필드 에러 메시지가 표시되지 않았습니다."
        error_message = login_page.get_password_error_message()
        assert "비밀번호를 입력해주세요." in error_message, f"예상 에러 메시지와 다릅니다: {error_message}"
        
        print("비밀번호 입력 제외 테스트 완료")