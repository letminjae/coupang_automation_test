# Main page - Coupang 메인 페이지 요소와 메서드를 정리, 검색 기능 포함

from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from utils.config import Config

# Main Page 전용 로케이터
class MainPageLocators:
    LOGIN_BUTTON = (By.CSS_SELECTOR, "a[title='로그인]")
    MY_COUPANG_LINK = (By.ID, "wa-mycoupang-link")

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