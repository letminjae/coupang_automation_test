# [TC-PDP-002] 메인 이미지 정상 출력 및 이미지 변경 확인

import pytest
from pages.product_detail_page import ProductDetailPage
from utils.config import Config

class TestProductImageDisplay:
    def test_main_image_and_thumbnail_hover(self, driver):
        """
        상품 상세 페이지에서 메인 이미지가 정상적으로 표시되고,
        썸네일에 마우스를 올렸을 때 메인 이미지가 올바르게 변경되는지 확인
        """
        
        # 테스트할 상품의 고유 URL (예: 아이폰 16 프로)
        product_url = Config.BASE_URL + "vp/products/8335434891"
        
        # ProductDetailPage 객체 생성 및 해당 상품 URL로 이동
        pdp = ProductDetailPage(driver)
        pdp.go_to_url(product_url)
        
        # 봇 감지 회피를 위한 초기 무빙
        pdp.move_mouse_randomly()

        # 1. 메인 이미지 표시되는지 확인
        assert pdp.is_main_image_displayed(), "메인 이미지가 화면에 표시되지 않습니다."
        print("메인 이미지 정상 표시 확인.")

        # 2. 썸네일 이미지에 마우스 오버 시 메인 이미지가 변경되는지 확인
        thumbnail_images = pdp.get_all_thumbnail_images()

        for index, thumbnail in enumerate(thumbnail_images):
            # 썸네일에 마우스 올리고, 비교를 위한 썸네일 src 가져오기
            processed_thumbnail_src = pdp.hover_on_thumbnail_and_get_src(thumbnail)
            
            # 현재 메인 이미지의 src 가져오기
            current_main_src = pdp.get_main_image_src()

            print(f"[{index+1}번] 썸네일 이미지 (사이즈 조정): {processed_thumbnail_src}")
            print(f"[{index+1}번] 메인 이미지: {current_main_src}")

            # 검증: 썸네일 src가 메인 이미지 src에 포함되는지 확인
            assert processed_thumbnail_src in current_main_src, \
                f'메인 이미지와 썸네일 이미지가 일치하지 않습니다. 썸네일: {processed_thumbnail_src}, 메인: {current_main_src}'

        print("모든 썸네일 호버 시 메인 이미지로 정상 표시 확인 완료")