import pytest
from pages.product_detail_page import ProductDetailPage
from utils.config import config_instance as config

class TestPDPScenarios:
    """
    쿠팡 상품 상세 페이지(PDP)의 다양한 기능에 대한 시나리오를 테스트
    (상품명/가격, 이미지, 로켓배송 뱃지, 리뷰 영역, 상품 옵션 등)
    """
    
    @pytest.fixture(autouse=True)
    def setup_for_pdp_tests(self, driver):
        """
        각 PDP 테스트가 시작되기 전에 상품 상세 페이지로 이동합니다.
        """
        print("\n--- PDP 페이지 테스트 Setup ---")
        self.pdp_page = ProductDetailPage(driver) # 클래스 인스턴스 변수로 저장, 다른 테스트 함수에서 사용
        
        # 테스트할 상품의 고유 URL (예: 아이폰 16 프로)
        # 동일한 상품에 대한 여러 테스트이므로, fixture에서 한 번만 URL을 설정
        self.product_url = config.BASE_URL + "vp/products/8335434891" # 사용할 상품 URL
        
        self.pdp_page.go_to_url(self.product_url)
        self.pdp_page.move_mouse_randomly() # 봇 감지 회피
        
        yield # 테스트 함수 실행

        # 각 테스트 후 필요한 정리 작업이 있다면 여기에 추가
        driver.delete_all_cookies() # 테스트 후 쿠키 삭제로 상태 초기화
        print("브라우저 쿠키 삭제 완료.")
        
    def test_product_name_and_price_display(self):
        """
        [TC-PDP-001] 특정 상품 상세 페이지에서 상품명과 가격이 정상적으로 표시되는지 확인
        """
        print("\n[TC-PDP-001] 상품명 및 가격 정상 표시 확인 테스트 시작")
        
        # 1. 상품명 정상 출력 확인
        assert self.pdp_page.is_product_name_displayed(), "상품명이 화면에 표시되지 않습니다."
        product_name_text = self.pdp_page.get_product_name()
        print(f"상품명 정상 출력 확인 - {product_name_text}")

        # 2. 가격정보 정상 표시 확인
        assert self.pdp_page.is_product_price_displayed(), "가격이 화면에 표시되지 않습니다."
        product_price_text = self.pdp_page.get_product_price()
        print(f"상품가격 정상 출력 - {product_price_text}")
        
        print("상품명 및 가격 정상 표시 테스트 완료")