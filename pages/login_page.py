# Login Page - Coupang 로그인 페이지 요소와 메서드를 정리

from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from utils.config import Config

# Login Page 전용 로케이터
class LoginPageLocators:
    EMAIL_INPUT = (By.ID, "login-email-input")
    PASSWORD_INPUT = (By.ID, "login-password-input")
    LOGIN_SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    LOGIN_ERROR_MESSAGE = (By.CSS_SELECTOR, "div.login__error-msg")
    LOGIN_INPUT_ERROR_MESSAGE = (By.CSS_SELECTOR, ".member__message-area.member__message-area--error._memberInputMessage.login-fail-web-log-error-msg")
    LOGIN_PASSWORD_ERROR_MESSAGE = (By.CSS_SELECTOR, ".member__message-area.member__message-area--error._loginPasswordError.login-fail-web-log-error-msg")

# Login Page 전용 메서드
class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def enter_credentials(self, email, password):
        """이메일과 비밀번호를 입력"""
        self.type_text(LoginPageLocators.EMAIL_INPUT, email)
        self.type_text(LoginPageLocators.PASSWORD_INPUT, password)
        self.move_mouse_randomly()
    
    def click_login_submit_button(self):
        """로그인 제출 버튼을 클릭"""
        self.click_element(LoginPageLocators.LOGIN_SUBMIT_BUTTON)
        
    def login(self, email, password):
        """로그인 절차 수행"""
        self.enter_credentials(email, password)
        self.click_login_submit_button()
    
    def get_error_message(self):
        """로그인 실패 시, 표시되는 에러메시지 텍스트 반환"""
        return self.get_element_text(LoginPageLocators.LOGIN_ERROR_MESSAGE)
    
    def is_error_message_displayed(self):
        """로그인 에러 메시지가 표시되는지 확인"""
        return self.is_element_displayed(LoginPageLocators.LOGIN_ERROR_MESSAGE)
    
    def get_input_error_message(self):
        """입력 필드 에러 메시지 텍스트 반환"""
        return self.get_element_text(LoginPageLocators.LOGIN_INPUT_ERROR_MESSAGE)
    
    def is_input_error_message_displayed(self):
        """입력 필드 에러 메시지가 표시되는지 확인"""
        return self.is_element_displayed(LoginPageLocators.LOGIN_INPUT_ERROR_MESSAGE)
    
    def get_password_error_message(self):
        """비밀번호 입력 필드 에러 메시지 텍스트 반환"""
        return self.get_element_text(LoginPageLocators.LOGIN_PASSWORD_ERROR_MESSAGE)
    
    def is_password_error_message_displayed(self):
        """비밀번호 입력 필드 에러 메시지가 표시되는지 확인"""
        return self.is_element_displayed(LoginPageLocators.LOGIN_PASSWORD_ERROR_MESSAGE)