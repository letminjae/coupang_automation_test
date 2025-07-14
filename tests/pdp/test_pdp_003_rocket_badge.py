# [TC-PDP-003] 로켓배송 정보 영역 확인

import pytest
from pages.product_detail_page import ProductDetailPage
from utils.config import Config

class TestProductRocketBadge:
    def test_rocket_badge_display(self, driver):
        """
        상품 상세 페이지에서 로켓배송 뱃지가 정상적으로 표시되는지 확인
        """
        
        # 테스트할 상품의 고유 URL (예: 아이폰 16 프로)
        product_url = Config.BASE_URL + "vp/products/8335434891"
        
        # ProductDetailPage 객체 생성 및 해당 상품 URL로 이동
        pdp = ProductDetailPage(driver)
        pdp.go_to_url(product_url)
        
        # 봇 감지 회피를 위한 초기 무빙
        pdp.move_mouse_randomly()

        # 1. 로켓배송 뱃지 표시 확인
        assert pdp.is_rocket_badge_displayed(), "로켓배송 뱃지가 화면에 표시되지 않습니다."
        
        # 뱃지의 alt 텍스트 등 추가 정보 확인
        badge_alt_text = pdp.get_rocket_badge_alt_text()
        print(f"로켓배송 뱃지 정상 표시 확인 (alt: '{badge_alt_text}')")
        
        # 만약 로켓배송이 아닌 상품도 테스트해야 한다면, 별도의 테스트 케이스 또는 parametrize를 사용 필요.
        
        print("로켓배송 정보 영역 확인 테스트 완료")