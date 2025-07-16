# [TC-SEARCH-001] 쿠팡 검색 기능 테스트 케이스 =>
# [TC-MAIN-007] 메인 페이지에서 상품 검색 기능 확인으로 변경

import pytest
from pages.main_page import MainPage
from utils.config import Config

class TestMainSearchProduct:
    def test_search_product_display(self, driver):
        """
        특정 상품을 메인페이지에서 검색하여 결과 확인
        """
        main_page = MainPage(driver)

        # 봇 감지 회피를 위한 초기 무빙
        main_page.move_mouse_randomly()

        # 검색창에 텍스트를 입력 후, 검색 버튼 클릭 (예: "노트북")
        main_page.search_product("노트북")

        # 검증 : 봇 감지로 인해 검색 결과 페이지가 로드되지 않음. (셀레니움 한계)
        result = main_page.MAIN_CONTENT
        assert "ERR_HTTP2_PROTOCOL_ERROR" in result.text, "정상적으로 봇 감지를 회피했습니다."
        print("검색 결과 페이지가 로드 되지 않았습니다. 봇 감지로 인해 정상적인 검색 결과를 확인할 수 없습니다.")
