# [TC-LOGIN-001] 쿠팡 로그인 성공 테스트 케이스

import pytest
from pages.main_page import MainPage
from pages.login_page import LoginPage
from utils.config import config_instance as config

class TestLogin001Success:
    def test_successful_login_to_coupang(self, driver):
        """
        메인 페이지에서 로그인 버튼 클릭 -> 로그인 페이지에서 ID/PW 입력 -> 로그인 버튼 클릭 -> 마이쿠팡 링크 확인
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
        pw = config.COUPANG_PW

        login_page.login(id, pw)
        
        # 5. 로그인 성공 확인
        # 로그인 후 다시 메인 페이지의 상태를 확인합니다.
        # 명시적 대기를 통해 요소가 나타날 때까지 기다립니다.
        assert main_page.is_my_coupang_link_displayed(), "로그인 성공 후 '마이쿠팡' 링크가 표시되지 않습니다."
        assert main_page.get_my_coupang_link_text() == "마이쿠팡", "'마이쿠팡' 링크 텍스트가 올바르지 않습니다."
        
        print("로그인 성공 테스트 완료: 마이쿠팡 링크 확인")