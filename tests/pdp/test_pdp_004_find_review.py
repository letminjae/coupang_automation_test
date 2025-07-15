# [TC-PDP-004] 리뷰 영역 확인

import pytest
from pages.product_detail_page import ProductDetailPage
from utils.config import Config

class TestProductReviewArea:
    def test_review_section_display(self, driver):
        """
        상품 상세 페이지에서 '상품평' 링크를 찾아 클릭하고,
        리뷰 영역이 정상적으로 표시되는지 확인
        """
        
        # 테스트할 상품의 고유 URL (예: 아이폰 16 프로)
        product_url = Config.BASE_URL + "vp/products/8335434891"
        
        # ProductDetailPage 객체 생성 및 해당 상품 URL로 이동
        pdp = ProductDetailPage(driver)
        pdp.go_to_url(product_url)
        
        # 봇 감지 회피를 위한 초기 무빙
        pdp.move_mouse_randomly()
        
        # 1. '상품평' 링크를 찾고 클릭 (필요시 스크롤 수행)
        link_clicked = pdp.find_and_click_review_link()
        
        # 링크 클릭 성공 여부 확인
        assert link_clicked, "상품평 링크를 찾거나 클릭하는 데 실패했습니다."
        
        # 2. 리뷰 헤더가 표시되는지 확인 (리뷰 영역 로딩 확인)
        assert pdp.is_review_header_displayed(), "상품평 영역의 헤더가 표시되지 않습니다. 리뷰 로딩 실패."
        print("상품평 화면 표시 성공 확인 완료")