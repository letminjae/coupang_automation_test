# [TC-MAIN-005] 우측 하단 Top Button 동작 확인

import pytest
from pages.main_page import MainPage

class TestMainTopButton:
    def test_top_button_functionality(self, driver):
        """
        쿠팡 메인 페이지의 'Top' 버튼이 올바르게 동작하여
        페이지 최상단으로 이동하는지 확인
        """
        main_page = MainPage(driver)
        
        # 봇 감지 회피를 위한 초기 무빙
        main_page.move_mouse_randomly() 

        # 1. 페이지를 랜덤하게 아래로 스크롤하여 Top 버튼 표시되게 하기
        main_page.scroll_down_randomly(min_px=800, max_px=1200) # 랜덤 스크롤
        
        # 2. Top 버튼 표시 확인
        assert main_page.is_top_button_displayed(), "Top 버튼이 표시되지 않거나 클릭할 수 없습니다."
        
        # 3. Top 버튼을 클릭
        main_page.click_top_button()
        
        # 4. 스크롤 위치 확인 (최상단으로 이동했는지)
        main_page.random_sleep(1, 2) 
        
        current_scroll_y = main_page.get_current_scroll_y()
        print(f"클릭 후 현재 스크롤 위치: {current_scroll_y}")

        assert current_scroll_y == 0, \
            f"Top 버튼 동작 실패: 페이지가 최상단으로 이동하지 않았습니다. 현재 스크롤 Y: {current_scroll_y}"
            
        print("Top button 정상 작동 확인 완료")