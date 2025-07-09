# Main page - Coupang 메인 페이지 요소와 메서드를 정리, 검색 기능 포함

from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utils.config import Config
import time

# Main Page 전용 로케이터
class MainPageLocators:
    LOGIN_BUTTON = (By.CSS_SELECTOR, "a[title='로그인']")
    MY_COUPANG_LINK = (By.ID, "wa-mycoupang-link")
    MAIN_TODAY_BANNERS = (By.CSS_SELECTOR, ".main-today__bg") # 모든 배너 요소
    DISCOVERY_SECTION = (By.ID, "todayDiscoveryUnit") # 오늘의 발견 섹션
    DISCOVERY_SECTION_IMAGES = (By.CSS_SELECTOR, ".tti-image") # 오늘의 발견 이미지들
    CATEGORY_MENU = (By.ID, "wa-category") # 상단 카테고리 메뉴
    APPLIANCE_DIGITAL_CATEGORY = (By.LINK_TEXT, "가전디지털") # 가전디지털 카테고리 링크

# Main Page 전용 메서드
class MainPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.go_to_url(Config.BASE_URL) # 생성 시, 기본 URL 이동

    def click_login_button(self):
        """메인 페이지에서 로그인 버튼 클릭"""
        self.click_element(MainPageLocators.LOGIN_BUTTON)

    def is_my_coupang_link_displayed(self):
        """로그인 성공 후, '마이쿠팡' 링크가 보이는지 확인"""
        return self.is_element_displayed(MainPageLocators.MY_COUPANG_LINK)
    
    def get_my_coupang_link_text(self):
        """'마이쿠팡' 링크의 텍스트를 반환"""
        return self.get_element_text(MainPageLocators.MY_COUPANG_LINK)
    
    def get_visible_banner_index(self):
        """
        현재 화면에 보이는 배너의 인덱스를 반환
        배너 요소가 완전히 로딩될 때까지 대기
        """
        self.wait.until(EC.presence_of_all_elements_located(MainPageLocators.MAIN_TODAY_BANNERS))
        banners = self.find_elements(MainPageLocators.MAIN_TODAY_BANNERS)
        for idx, banner in enumerate(banners):
            try:
                if banner.is_displayed():
                    return idx
            except Exception as E:
                print("배너 요소 미확인.. 재시도")
                continue
        return -1
    
    def wait_for_banner_transition(self, initial_index, timeout=10):
        """
        배너가 초기 인덱스에서 다음 인덱스로 전환될 때까지 대기
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            current_index = self.get_visible_banner_index()
            if current_index != -1 and current_index != initial_index:
                return current_index
            self.random_sleep(0.5, 1)
        return initial_index
    
    def scroll_to_discovery_section(self):
        """
        '오늘의 발견' 섹션으로 스크롤
        """
        discovery_section = self.wait.until(EC.presence_of_element_located(MainPageLocators.DISCOVERY_SECTION))
        self.scroll_to_element(discovery_section)
        
    def get_discovery_images(self):
        """
        '오늘의 발견' 섹션의 모든 이미지 요소를 반환
        """
        images = self.find_elements(MainPageLocators.DISCOVERY_SECTION_IMAGES)
        visible_valid_images = [
            img for img in images 
            if img.is_displayed() and img.get_attribute("src") # src 속성도 확인하여 유효성 높임
        ]
        return visible_valid_images
        
    def hover_category_menu(self):
        """
        상단 카테고리 메뉴에 마우스 오버
        """
        self.human_like_hover(MainPageLocators.CATEGORY_MENU)
        
    def click_appliance_digital_category(self):
        """
        '가전디지털' 카테고리 클릭 후 이동 확인
        """
        self.click_element(MainPageLocators.APPLIANCE_DIGITAL_CATEGORY, human_like=True)
        self.random_sleep(1, 2)  # 클릭 후 짧은 슬립