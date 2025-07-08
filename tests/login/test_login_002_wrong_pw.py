# [TC-LOGIN-002] 쿠팡 로그인 실패 테스트 케이스

import pytest
from pages.main_page import MainPage
from pages.login_page import LoginPage
from utils.config import config_instance as config

class TestLogin002WrongPW:
    def test_fail_login_to_coupang_with_PW(self, driver):
        """
        메인 페이지에서 로그인 버튼 클릭 -> 로그인 페이지에서 잘못된 비밀번호 입력 -> 로그인 버튼 클릭 -> 메인페이지로 돌아가지 않음
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
        pw = "123456" # 잘못된 비밀번호 입력

        login_page.login(id, pw)
        
        # 5. 로그인 실패 확인
        assert driver.current_url != "https://www.coupang.com/", "로그인이 실패하여야하나, 성공했습니다." # 로그인 실패 시 URL이 변경되지 않아야 함
        
        print("로그인 실패 테스트 완료")