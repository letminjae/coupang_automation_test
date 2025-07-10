# [TC-MAIN-004] 최하단 Footer 공지사항 클릭 및 페이지 이동 확인

import pytest
from pages.main_page import MainPage

class TestMainNotice:
    def test_footer_notice_link_navigation(self, driver):
        """
        쿠팡 메인 페이지 최하단 푸터의 '공지사항' 링크를 클릭하여
        해당 페이지로 올바르게 이동하는지 확인 테스트
        """
        main_page = MainPage(driver)
        
        # 봇 감지 회피를 위한 초기 무빙
        main_page.move_mouse_randomly() 

        # 1. 페이지 최하단으로 스크롤
        print("페이지 최하단으로 스크롤 중...")
        main_page.scroll_to_bottom() # BasePage의 scroll_to_bottom 메서드 사용
        
        # 2. '공지사항' 링크 클릭
        main_page.click_footer_notice_link()
        
        # 3. 새로 열린 탭/창으로 전환 및 URL 검증
        # 공지사항 링크는 보통 새 탭/창으로 열리므로, 윈도우 핸들 전환 필요
        original_window_handle = main_page.switch_to_new_window()
        
        expected_url = "https://mc.coupang.com/ssr/desktop/contact/notice"
        print(f"현재 URL: {driver.current_url}, 예상 URL: {expected_url}")
        
        assert driver.current_url == expected_url, \
            f"공지사항 페이지로 이동 실패. 예상: {expected_url}, 실제: {driver.current_url}"
        print("공지사항 페이지로 이동 성공 확인")

        # 테스트 완료 후 원래 탭으로 돌아가기
        driver.close() # 현재(공지사항) 탭 닫기
        main_page.switch_to_original_window(original_window_handle) # 원래(메인 페이지) 탭으로 전환
        
        print("테스트 완료 및 원래 페이지로 복귀.")