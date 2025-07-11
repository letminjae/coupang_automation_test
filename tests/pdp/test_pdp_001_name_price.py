# [TC-PDP-001] 상풍 상세 페이지 상품명 및 가격 정상 표시 확인 테스트

import pytest
from pages.product_detail_page import ProductDetailPage
from utils.config import Config

class TestProductDetailPageBasicInfo:
    def test_product_name_and_price_display(self, driver):
        """
        특정 상품 상세 페이지에서 상품명과 가격이 정상적으로 표시되는지 확인
        """
        # 아이폰 16 프로 제품 URL
        product_url = Config.BASE_URL + "vp/products/8335434891"

        # driver 객체 생성 및 해당 제품 URL로 이동
        pdp = ProductDetailPage(driver)
        pdp.go_to_url(product_url)

        # 봇 감지 회피를 위한 초기 무빙
        pdp.move_mouse_randomly()

        # 1. 상품명 출력 확인
        assert pdp.is_product_name_displayed(), "상품명이 화면에 표시되지 않습니다."
        product_name_text = pdp.get_product_name()
        print(f"상품명 정상 출력 확인 - {product_name_text}")

        # 2. 가격 정보 출력 확인
        assert pdp.is_product_price_displayed(), "가격이 화면에 표시되지 않습니다."
        product_price_text = pdp.get_product_price()
        print(f"상품 가격 정상 출력 - {product_price_text}")

        print("상품명 및 가격 정상 표시 테스트 완료")