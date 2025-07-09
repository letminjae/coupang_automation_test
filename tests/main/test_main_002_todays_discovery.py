# [TC-MAIN-002] "오늘의 발견" 이미지 및 리스트 표시 확인

import pytest
from pages.main_page import MainPage

class TestTodaysDiscovery:
    def test_todays_discovery_images_displayed(self, driver):
        """
        쿠팡 메인 페이지 '오늘의 발견' 섹션의 이미지 및 리스트 표시 확인
        """
        # MainPage 객체 생성 및 기본 URL로 이동
        main_page = MainPage(driver)
        
        # 봇 감지 회피를 위한 초기 무빙
        main_page.move_mouse_randomly()

        # 스크롤 내리기
        main_page.scroll_to_discovery_section()
        
        # '오늘의 발견' 섹션의 이미지 요소 로드 확인
        loaded_images = main_page.get_discovery_images()
        
        assert len(loaded_images) > 0, "오늘의 발견 이미지가 로드되지 않았습니다."
        print(f"로드된 오늘의 발견 이미지 수 : {len(loaded_images)}")
        print("오늘의 발견 이미지 및 리스트 정상 표시")