import pytest
from pages.main_page import MainPage
from utils.config import config_instance as config

class TestMainScenarios:
    """
    쿠팡 메인 페이지의 다양한 기능에 대한 시나리오를 테스트합니다.
    (배너, 오늘의 발견 등)
    """
    
    @pytest.fixture(autouse=True)
    def setup_for_main_tests(self, driver):
        """
        각 메인 페이지 테스트가 시작되기 전에 메인 페이지로 이동합니다.
        """
        print("\n--- 메인 페이지 테스트 Setup ---")
        self.main_page = MainPage(driver) # 클래스 인스턴스 변수로 저장, 다른 테스트 함수에서 사용
        self.main_page.go_to_url(config.BASE_URL)
        self.main_page.move_mouse_randomly() # 봇 감지 회피
        
        yield  # 테스트 함수 실행
        
        # 각 테스트 후 필요한 정리 작업이 있다면 여기에 추가
        # main 페이지에서 빈번하게 쿠키를 삭제하는 것은 리소스 낭비, 주석처리
        # driver.delete_all_cookies() # 테스트 후 쿠키 삭제로 상태 초기화
        # print("브라우저 쿠키 삭제 완료.")
        
    def test_main_banner_auto_transition(self):
        """
        [TC-MAIN-001] 쿠팡 메인 페이지 배너 테스트
        배너가 정상적으로 표시되고, 올바르게 전환되는지 확인
        """
        print("\n--- [TC-MAIN-001] 배너 캐러셀 테스트 시작 ---")
        # 1. 초기 보이는 배너 인덱스 확인
        initial_banner_index = self.main_page.get_visible_banner_index()
        print(f"초기 배너 인덱스: {initial_banner_index}")
        
        # 2. 배너가 전환될 때까지 기다림 (자동 전환 대기)
        transitioned_banner_index = self.main_page.wait_for_banner_transition(initial_banner_index, timeout=5) # 5초 내에 배너 전환 확인
        
        print(f"전환 후 배너 인덱스: {transitioned_banner_index}")

        # 3. 검증: 초기 배너 인덱스와 전환 후 배너 인덱스가 다른지 확인
        assert initial_banner_index != -1, "초기 배너를 찾을 수 없습니다."
        assert transitioned_banner_index != -1, "전환 후 배너를 찾을 수 없습니다."
        assert initial_banner_index != transitioned_banner_index, \
            f"배너가 자동으로 전환되지 않았습니다. 초기: {initial_banner_index}, 전환 후: {transitioned_banner_index}"
        
        print("배너 자동 전환 테스트 완료")
        
    def test_todays_discovery_images_and_list_displayed(self):
        """
        [TC-MAIN-002] 쿠팡 메인 페이지 '오늘의 발견' 섹션의 이미지 및 리스트 표시 확인
        """
        print("\n--- [TC-MAIN-002] '오늘의 발견' 이미지 및 리스트 표시 확인 테스트 시작")
        
        # 1. '오늘의 발견' 섹션으로 스크롤 내리기
        print("'오늘의 발견' 섹션으로 스크롤 중...")
        self.main_page.scroll_to_discovery_section()
        
        # 2. '오늘의 발견' 섹션의 이미지 요소 로드 확인
        print("'오늘의 발견' 섹션 이미지 로딩 중...")
        loaded_images = self.main_page.get_discovery_images()
        
        # 3. 검증: 로드된 이미지 수가 0보다 큰지 확인
        assert len(loaded_images) > 0, "'오늘의 발견' 섹션의 이미지가 로드되지 않았습니다."
        print(f"로드된 '오늘의 발견' 이미지 수: {len(loaded_images)}")
        print("오늘의 발견 이미지 및 리스트 정상 표시 확인 완료!")
        
    def test_category_navigation(self):
        """
        [TC-MAIN-003] 쿠팡 메인 페이지 카테고리 메뉴에서 '가전디지털' 카테고리로 이동하는 동작 확인
        """
        print("\n--- [TC-MAIN-003] '가전디지털' 카테고리 이동 테스트 시작")
        
        # 1. '가전디지털' 카테고리로 Hover 후 클릭
        self.main_page.hover_category_menu()
        self.main_page.click_appliance_digital_category()

        # 2. 가전디지털 페이지로 이동했는지 확인
        assert "가전디지털" in self.main_page.driver.title, "가전디지털 페이지 이동 실패"
        print("가전디지털 페이지 이동 성공")
        
    def test_footer_notice_link_navigation(self):
        """
        [TC-MAIN-004] 쿠팡 메인 페이지 최하단 푸터의 '공지사항' 링크 클릭 및 페이지 이동 확인
        """
        print("\n--- [TC-MAIN-004] '공지사항' 링크 클릭 및 페이지 이동 테스트 시작")
        
        # 1. 페이지 최하단으로 스크롤
        print("페이지 최하단으로 스크롤 중...")
        self.main_page.scroll_to_bottom()
        
        # 2. '공지사항' 링크 클릭 전, 현재 URL을 저장
        original_url = self.main_page.driver.current_url
        print(f"링크 클릭 전 URL: {original_url}")
        
        # 3. '공지사항' 링크 클릭
        self.main_page.click_footer_notice_link()
        print(f'공지사항 링크 클릭 후 URL: {self.main_page.driver.current_url}')
        
        # 4. URL이 바뀌었는지 확인
        expected_url = "https://mc.coupang.com/ssr/desktop/contact/notice"
        assert self.main_page.driver.current_url == expected_url, \
            f"공지사항 페이지로 이동 실패. 예상: {expected_url}, 실제: {self.main_page.driver.current_url}"
        print("공지사항 페이지로 이동 성공 확인")

        print("공지사항 테스트 완료")
        
    def test_top_button_functionality(self):
        """
        [TC-MAIN-005] 쿠팡 메인 페이지의 'Top' 버튼이 올바르게 동작하여
        페이지 최상단으로 이동하는지 확인
        """
        print("\n--- [TC-MAIN-005] Top 버튼 동작 테스트 시작")
        
        # 1. 페이지를 랜덤하게 아래로 스크롤하여 Top 버튼 표시되게 하기
        self.main_page.scroll_down_randomly(min_px=1600, max_px=2000) # 랜덤 스크롤
        
        # 2. Top 버튼 표시 확인
        assert self.main_page.is_top_button_displayed(), "Top 버튼이 표시되지 않거나 클릭할 수 없습니다."
        
        # 3. Top 버튼 클릭
        self.main_page.click_top_button()
        self.main_page.random_sleep(1, 2) # 잠시 대기 
        
        current_scroll_y = self.main_page.get_current_scroll_y()
        print(f"클릭 후 현재 스크롤 위치: {current_scroll_y}")

        # 4. 검증 : 스크롤 위치 확인 (최상단으로 이동했는지)
        assert current_scroll_y == 0, \
            f"Top 버튼 동작 실패: 페이지가 최상단으로 이동하지 않았습니다. 현재 스크롤 Y: {current_scroll_y}"
            
        print("Top button 정상 작동 확인 완료")
        
    def test_promotion_lazy_loading(self):
        """
        [TC-MAIN-006] 쿠팡 메인 페이지 '카테고리 광고상품' 섹션의 이미지가
        스크롤에 의해 레이지 로딩되는지 확인
        """
        print("\n--- [TC-MAIN-006] '카테고리 광고상품' Lazy Loading 테스트 시작")
        
        # 1. 스크롤 이전에 이미지 src 속성을 먼저 확인
        srcs_before_scroll = self.main_page.get_promotion_image_srcs()
        print(f"스크롤 이전 src 속성 (처음 3개): {srcs_before_scroll[:3]}") # 사실 상 렌더링전이라 srcs_before_scroll는 빈 리스트일 가능성이 높음
        
        # 2. '카테고리 광고상품' 이미지가 나타날 때까지 아래로 스크롤
        self.main_page.scroll_to_reveal_promotion_images(scroll_distance=2000, scroll_step=80, scroll_delay=0.15)
        
        # 3. 스크롤 이후 다시 src 속성 확인 (lazy loading 여부)
        srcs_after_scroll = self.main_page.get_promotion_image_srcs()
        print(f"스크롤 이후 src 속성 (처음 3개): {srcs_after_scroll[:3]}")
        
        # 4. 검증: 스크롤 이후 이미지 src 목록의 길이가 스크롤 이전보다 길어졌는지 확인
        assert len(srcs_after_scroll) > len(srcs_before_scroll), "Lazy loading이 정상 작동하지 않았습니다."
        
        print("Lazy loading 정상 작동 확인 완료")
        
    def test_search_product_display(self):
        """
        [TC-MAIN-007] 메인 페이지에서 상품 검색 기능 확인
        상품 검색 시, 봇 감지로 인해 검색 결과 페이지가 로드되지 않는지 확인
        """
        print("\n--- [TC-MAIN-007] 상품 검색 기능 테스트 시작")
        
        # 1. 검색창에 텍스트를 입력 후, 검색 버튼 클릭 (예: "노트북")
        self.main_page.search_product("노트북")
        
        # 2. 검증 : 봇 감지로 인해 검색 결과 페이지가 로드되지 않음. (셀레니움 한계)
        result = self.main_page.get_search_result_content()
        assert "ERR_HTTP2_PROTOCOL_ERROR" in result.text, "정상적으로 봇 감지를 회피했습니다."
        
        print("검색 결과 페이지가 로드 되지 않았습니다. 봇 감지로 인해 정상적인 검색 결과를 확인할 수 없습니다.")