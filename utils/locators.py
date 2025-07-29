# 유지보수성을 극대화 하기 위해 locator를 별도의 파일로 분리합니다.

from selenium.webdriver.common.by import By

class LoginPageLocators:
    # 로그인 페이지의 웹 UI 요소들을 정의합니다.
    EMAIL_INPUT = (By.ID, "login-email-input")
    PASSWORD_INPUT = (By.ID, "login-password-input")
    LOGIN_SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    
    # 로그인 실패 시 표시되는 에러 메시지 로케이터
    LOGIN_ERROR_MESSAGE = (By.CSS_SELECTOR, "div.login__error-msg") # 일반적인 로그인 실패 메시지
    LOGIN_INPUT_ERROR_MESSAGE = (By.CSS_SELECTOR, ".member__message-area.member__message-area--error._memberInputMessage.login-fail-web-log-error-msg") # ID/PW 입력 필드 하단
    LOGIN_PASSWORD_ERROR_MESSAGE = (By.CSS_SELECTOR, ".member__message-area.member__message-area--error._loginPasswordError.login-fail-web-log-error-msg") # 비밀번호 입력 필드 하단
    LOGIN_PASSWORD_COMMON_ERROR_MESSAGE = (By.CSS_SELECTOR, ".member__message-area.member__message-area--error._loginCommonError.login-fail-web-log-error-msg") # 비밀번호 관련 공통 에러