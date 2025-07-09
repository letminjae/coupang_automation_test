# [TC-MAIN-003] 상단 카테고리 페이지 이동 동작 확인

import pytest
from pages.main_page import MainPage

class TestMainCategory:
    def test_category_navigation(self, driver):
        """
        쿠팡 메인 페이지 카테고리 메뉴에서 '가전디지털' 카테고리로 이동하는 동작 확인
        """
        
        # MainPage 객체 생성 및 기본 URL로 이동
        main_page = MainPage(driver)
        
        # 봇 감지 회피를 위한 초기 무빙
        main_page.move_mouse_randomly()
        
        # '가전디지털' 카테고리로 Hover 후 클릭
        main_page.hover_category_menu()
        main_page.click_appliance_digital_category()

        # # 가전디지털 페이지로 이동했는지 확인
        assert "가전디지털" in driver.title, "가전디지털 페이지 이동 실패"
        print("가전디지털 페이지 이동 성공")