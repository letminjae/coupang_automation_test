# [TC-PDP-005] 상품 옵션 적용 확인

import pytest
from pages.product_detail_page import ProductDetailPage
from utils.config import Config

class TestProductOption:
    def test_product_option_application(self, driver):
        """
        상품 상세 페이지에서 옵션을 선택하고
        선택된 옵션의 텍스트가 올바르게 반영되는지 확인
        """
        
        # 테스트할 상품의 고유 URL (예: 아이폰 16 프로)
        product_url = Config.BASE_URL + "vp/products/8335434891"
        
        # ProductDetailPage 객체 생성 및 해당 상품 URL로 이동
        pdp = ProductDetailPage(driver)
        pdp.go_to_url(product_url)
        
        # 봇 감지 회피를 위한 초기 무빙
        pdp.move_mouse_randomly()

        # 1. 모든 옵션 피커 드롭다운 가져오기
        option_pickers = pdp.get_all_option_pickers()
        print(f"총 {len(option_pickers)}개의 옵션 드롭다운을 찾았습니다.")
        
        # 2. 각 옵션 피커에 대해 첫 번째 옵션 선택 및 확인
        for index, picker_element in enumerate(option_pickers):
            print(f"상품 {index+1}번 옵션 변경 테스트 진행 중...")
            
            # 옵션 선택 (첫 번째 옵션 클릭)
            selected_option_text = pdp.select_first_option_in_picker(picker_element)
            
            # 첫 번째 옵션의 내용이 상품에 반영되는지 확인
            current_picker_text = pdp.get_option_picker_text(picker_element)
            
            assert selected_option_text in current_picker_text, \
                f"상품 {index+1}번 옵션 반영 실패: 선택된 옵션 '{selected_option_text}', 현재 피커 텍스트 '{current_picker_text}'"
            print(f"상품 {index+1}번 옵션 변경 테스트 성공: '{selected_option_text}' 확인됨.")

        print("모든 상품 옵션 적용 확인 테스트 완료")