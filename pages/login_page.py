# Login Page - Coupang 로그인 페이지 요소와 메서드를 정리

from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from utils.config import Config
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Login Page 전용 로케이터
class LoginPageLocators:
    EMAIL_INPUT = (By.ID, "login-email-input")
    PASSWORD_INPUT = (By.ID, "login-password-input")
    LOGIN_SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    
    # 로그인 실패 시 표시되는 에러 메시지 로케이터
    LOGIN_ERROR_MESSAGE = (By.CSS_SELECTOR, "div.login__error-msg") # 일반적인 로그인 실패 메시지
    LOGIN_INPUT_ERROR_MESSAGE = (By.CSS_SELECTOR, ".member__message-area.member__message-area--error._memberInputMessage.login-fail-web-log-error-msg") # ID/PW 입력 필드 하단
    LOGIN_PASSWORD_ERROR_MESSAGE = (By.CSS_SELECTOR, ".member__message-area.member__message-area--error._loginPasswordError.login-fail-web-log-error-msg") # 비밀번호 입력 필드 하단
    LOGIN_PASSWORD_COMMON_ERROR_MESSAGE = (By.CSS_SELECTOR, ".member__message-area.member__message-area--error._loginCommonError.login-fail-web-log-error-msg") # 비밀번호 관련 공통 에러

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
    
    def get_error_message(self, timeout=5):
        """
        로그인 실패 시 표시되는 다양한 유형의 에러 메시지 중 하나를 반환
        정의된 여러 에러 메시지 로케이터를 순회하며 가장 먼저 표시되는 메시지를 반환
        """
        # 메시지를 확인할 로케이터들의 리스트
        error_locators_to_check = [
            LoginPageLocators.LOGIN_ERROR_MESSAGE,
            LoginPageLocators.LOGIN_INPUT_ERROR_MESSAGE,
            LoginPageLocators.LOGIN_PASSWORD_ERROR_MESSAGE,
            LoginPageLocators.LOGIN_PASSWORD_COMMON_ERROR_MESSAGE,
        ]

        for locator in error_locators_to_check:
            try:
                # 각 로케이터에 대해 요소가 보일 때까지 짧게 대기
                error_element = self.wait.until(EC.visibility_of_element_located(locator))
                if error_element.is_displayed():
                    return error_element.text
            except TimeoutException:
                # 해당 로케이터로 메시지를 찾지 못하면 다음 로케이터 시도
                continue
            except Exception as e:
                # 다른 예외 발생 시 로깅 (선택 사항)
                print(f"예외발생 에러 체킹 {locator}: {e}")
                continue
        
        # 모든 로케이터를 시도했지만 메시지를 찾지 못한 경우
        print("로그인 에러 메시지를 찾지 못했습니다.")
        return None

    def is_error_message_displayed(self, timeout=5):
        """
        로그인 실패 시 에러 메시지 중 하나라도 표시되는지 확인
        """
        # get_error_message() 내부 로직을 재활용하여 메시지가 존재하면 True 반환
        return bool(self.get_error_message(timeout=timeout))