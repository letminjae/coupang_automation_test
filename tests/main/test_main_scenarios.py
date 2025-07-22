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
        driver.delete_all_cookies() # 테스트 후 쿠키 삭제로 상태 초기화
        print("브라우저 쿠키 삭제 완료.")
        
    def test_main_banner_auto_transition(self):
        """
        [TC-MAIN-001] 쿠팡 메인 페이지 배너 테스트
        배너가 정상적으로 표시되고, 올바르게 전환되는지 확인
        """
        print("\n--- 배너 캐러셀 테스트 시작 ---")
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
        print("'오늘의 발견' 이미지 및 리스트 표시 확인 테스트 시작")
        
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
        print("'가전디지털' 카테고리 이동 테스트 시작")
        
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
        print("'공지사항' 링크 클릭 및 페이지 이동 테스트 시작")
        
        # 1. 페이지 최하단으로 스크롤
        print("페이지 최하단으로 스크롤 중...")
        self.main_page.scroll_to_bottom()
        
        # 2. '공지사항' 링크 클릭
        self.main_page.click_footer_notice_link()
        
        # 3. 새로 열린 탭/창으로 전환 및 URL 검증
        # 공지사항 링크는 보통 새 탭/창으로 열리므로, 윈도우 핸들 전환 필요
        original_window_handle = self.main_page.switch_to_new_window()
        
        expected_url = "https://mc.coupang.com/ssr/desktop/contact/notice"
        print(f"현재 URL: {self.main_page.driver.current_url}, 예상 URL: {expected_url}")
        
        assert self.main_page.driver.current_url == expected_url, \
            f"공지사항 페이지로 이동 실패. 예상: {expected_url}, 실제: {self.main_page.driver.current_url}"
        print("공지사항 페이지로 이동 성공 확인")

        # 테스트 완료 후 원래 탭으로 돌아가기
        self.main_page.driver.close()
        self.main_page.switch_to_original_window(original_window_handle)
        print("공지사항 테스트 완료 및 메인 페이지로 복귀")