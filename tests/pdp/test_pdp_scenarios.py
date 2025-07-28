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
        
    def test_main_image_and_thumbnail_hover(self):
        """
        [TC-PDP-002] 상품 상세 페이지에서 메인 이미지가 정상적으로 표시되고,
        썸네일에 마우스를 올렸을 때 메인 이미지가 올바르게 변경되는지 확인
        """
        print("\n[TC-PDP-002] 메인 이미지 정상 출력 및 이미지 변경 확인 테스트 시작")
        
        # 1. 메인 이미지 표시되는지 확인
        assert self.pdp_page.is_main_image_displayed(), "메인 이미지가 화면에 표시되지 않습니다."
        print("메인 이미지 정상 표시 확인")

        # 2. 썸네일 이미지에 마우스 오버 시 메인 이미지가 변경되는지 확인
        thumbnail_images = self.pdp_page.get_all_thumbnail_images()

        for index, thumbnail in enumerate(thumbnail_images):
            # 썸네일에 마우스 올리고, 비교를 위한 썸네일 src 가져오기
            processed_thumbnail_src = self.pdp_page.hover_on_thumbnail_and_get_src(thumbnail)
            
            # 현재 메인 이미지의 src 가져오기
            current_main_src = self.pdp_page.get_main_image_src()

            print(f"[{index+1}번] 썸네일 이미지 (사이즈 조정): {processed_thumbnail_src}")
            print(f"[{index+1}번] 메인 이미지: {current_main_src}")

            assert processed_thumbnail_src in current_main_src, \
                f'메인 이미지와 썸네일 이미지가 일치하지 않습니다. 썸네일: {processed_thumbnail_src}, 메인: {current_main_src}'

        print("모든 썸네일 호버 시 메인 이미지로 정상 표시 확인 완료")
        
    def test_rocket_badge_display(self):
        """
        [TC-PDP-003] 상품 상세 페이지에서 로켓배송 뱃지가 정상적으로 표시되는지 확인
        """
        print("\n[TC-PDP-003] 로켓배송 정보 영역 확인 테스트 시작")
        
        # 1. 로켓배송 뱃지 표시 확인
        assert self.pdp_page.is_rocket_badge_displayed(), "로켓배송 뱃지가 화면에 표시되지 않습니다."
        
        # (선택 사항) 뱃지의 alt 텍스트 등 추가 정보 확인
        badge_alt_text = self.pdp_page.get_rocket_badge_alt_text()
        print(f"로켓배송 뱃지 정상 표시 확인 (alt: '{badge_alt_text}')")
        
        # 만약 로켓배송이 아닌 상품도 테스트해야 한다면, 별도의 테스트 케이스 또는 parametrize를 사용 필요
        print("로켓배송 정보 영역 확인 테스트 완료")
        
    def test_review_section_display(self):
        """
        [TC-PDP-004] 상품 상세 페이지에서 '상품평' 링크를 찾아 클릭하고,
        리뷰 영역이 정상적으로 표시되는지 확인
        """
        print("\n[TC-PDP-004] 리뷰 영역 확인 테스트 시작")
        
        # 1. '상품평' 링크를 찾고 클릭 (필요시 스크롤 수행)
        link_clicked = self.pdp_page.find_and_click_review_link()
        
        assert link_clicked, "상품평 링크를 찾거나 클릭하는 데 실패했습니다."
        print("상품평 링크 클릭 성공")

        # 2. 리뷰 헤더가 표시되는지 확인 (리뷰 영역 로딩 확인)
        assert self.pdp_page.is_review_header_displayed(), "상품평 영역의 헤더가 표시되지 않습니다. 리뷰 로딩 실패."
        
        print("상품평 화면 표시 성공 확인 완료")