# [TC-MAIN-006] "카테고리 광고상품" Lazy Loading 처리 확인

import pytest
from pages.main_page import MainPage

class TestMainPromotionLazyLoading:
    def test_promotion_lazy_loading(self, driver):
        """
        쿠팡 메인 페이지의 '카테고리 광고상품' 섹션 이미지가
        스크롤에 의해 레이지 로딩되는지 확인
        """
        main_page = MainPage(driver)
        
        # 봇 감지 회피를 위한 초기 무빙
        main_page.move_mouse_randomly() 

        # 1. 스크롤 이전에 이미지 src 속성 확인
        srcs_before_scroll = main_page.get_promotion_image_srcs()
        print(f"스크롤 이전 src 속성 (처음 3개): {srcs_before_scroll[:3]}")

        # 2. '카테고리 광고상품' 이미지가 나타날 때까지 아래로 스크롤
        main_page.scroll_to_reveal_promotion_images(scroll_distance=2000, scroll_step=80, scroll_delay=0.15)
        
        # 3. 스크롤 이후 다시 src 속성 확인 (lazy loading 여부)
        srcs_after_scroll = main_page.get_promotion_image_srcs()
        print(f"스크롤 이후 src 속성 (처음 3개): {srcs_after_scroll[:3]}")

        # 4. 검증: 스크롤 이후 이미지 src 목록의 길이가 스크롤 이전보다 길어졌는지 확인
        assert len(srcs_after_scroll) > len(srcs_before_scroll), "Lazy loading이 정상 작동하지 않았습니다."
        
        print("Lazy loading 정상 작동 확인 완료")