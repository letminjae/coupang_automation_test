# Main page - Coupang 메인 페이지 요소와 메서드를 정리, 검색 기능 포함

from pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC
from utils.config import Config
from utils.locators import MainPageLocators
import time
import random

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
        
    def click_footer_notice_link(self):
        """
        메인 페이지 최하단 푸터의 '공지사항' 링크를 클릭
        클릭 후 새 탭/창으로 전환될 수 있으므로, 테스트에서 처리 필요.
        """
        self.click_element(MainPageLocators.NOTICE_LINK_FOOTER)
        
    def get_current_scroll_y(self):
        """현재 페이지의 Y축 스크롤 위치를 반환"""
        return self.driver.execute_script("return window.scrollY")

    def scroll_down_randomly(self, min_px=800, max_px=1200):
        """페이지를 랜덤한 픽셀만큼 아래로 스크롤"""
        scroll_amount = random.uniform(min_px, max_px)
        self.driver.execute_script(f"window.scrollTo(0, {scroll_amount})")
        self.random_sleep(3, 5) # 스크롤 후 대기

    def is_top_button_displayed(self):
        """Top 버튼이 화면에 표시되는지 확인"""
        # Top 버튼은 스크롤이 내려가야 나타나므로, element_to_be_clickable로 명시적 대기 필요
        return self.is_element_clickable(MainPageLocators.TOP_BUTTON, timeout=5) # 짧게 대기

    def click_top_button(self):
        """Top 버튼을 클릭"""
        self.click_element(MainPageLocators.TOP_BUTTON)
        
    def get_promotion_image_srcs(self):
        """
        '카테고리 광고상품' 섹션의 모든 이미지들의 src 속성을 반환
        """
        self.wait.until(EC.presence_of_all_elements_located(MainPageLocators.CATEGORY_PROMOTION_IMAGES))
        images = self.find_elements(MainPageLocators.CATEGORY_PROMOTION_IMAGES)
        # 이미지 요소의 'src' 속성을 가져와서 반환
        srcs = [img.get_attribute("src") for img in images if img.get_attribute("src")] # src가 없는 경우 제외
        return srcs

    def scroll_to_reveal_promotion_images(self, scroll_distance=2000, scroll_step=80, scroll_delay=0.15):
        """
        '카테고리 광고상품' 이미지가 로드될 때까지 페이지를 아래로 스크롤
        """
        print(f"이미지 로드를 위해 페이지 {scroll_distance}px 아래로 스크롤 중...")
        self.human_like_scroll_by(distance=scroll_distance, step=scroll_step, delay=scroll_delay)
        self.random_sleep(4, 5) # 충분히 대기하여 이미지가 로드될 시간을 줌
        
    def search_product(self, product_name, human_like=True):
        """
        메인 페이지에서 상품을 검색
        :param product_name: 검색할 상품 이름
        :param human_like: human_like 방식으로 입력할지 여부
        """
        # 검색창에 텍스트를 입력
        self.type_text(MainPageLocators.SEARCH_INPUT, product_name, human_like=human_like)
        self.random_sleep(1, 2)  # 입력 후 짧은 슬립
        # 검색 버튼 클릭
        self.click_element(MainPageLocators.SEARCH_BUTTON, human_like=human_like)