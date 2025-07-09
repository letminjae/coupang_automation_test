# [TC-MAIN-001] 쿠팡 메인 페이지 배너 자동 전환 테스트

import pytest
from pages.main_page import MainPage

class TestMainBanner:
    def test_main_page_banner_auto_transition(self, driver):
        """
        쿠팡 메인 페이지 배너 자동 전환 기능 테스트
        """
        # MainPage 객체 생성 및 기본 URL로 이동
        main_page = MainPage(driver)
       
        # 봇 감지 회피를 위한 초기 무빙
        main_page.move_mouse_randomly()

        # 1. 초기 보이는 배너 인덱스 확인
        initial_banner_index = main_page.get_visible_banner_index()
        print(f"초기 배너 인덱스: {initial_banner_index}")
       
        # 2. 배너가 전환될 때까지 기다림 (자동 전환 대기)
        transitioned_banner_index = main_page.wait_for_banner_transition(initial_banner_index, timeout=5)
       
        print(f"전환 후 배너 인덱스: {transitioned_banner_index}")

        # 3. 검증: 초기 배너 인덱스와 전환 후 배너 인덱스가 다른지 확인
        assert initial_banner_index != -1, "초기 배너를 찾을 수 없습니다."
        assert transitioned_banner_index != -1, "전환 후 배너를 찾을 수 없습니다."
        assert initial_banner_index != transitioned_banner_index, \
            f"배너가 자동으로 전환되지 않았습니다. 초기: {initial_banner_index}, 전환 후: {transitioned_banner_index}"
       
        print("배너 자동 전환 테스트 완료")