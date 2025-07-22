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
