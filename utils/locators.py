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
    
class MainPageLocators:
    # 메인 페이지의 웹 UI 요소들을 정의합니다.
    LOGIN_BUTTON = (By.CSS_SELECTOR, "a[title='로그인']")
    MY_COUPANG_LINK = (By.ID, "wa-mycoupang-link")
    MAIN_TODAY_BANNERS = (By.CSS_SELECTOR, ".main-today__bg") # 모든 배너 요소
    DISCOVERY_SECTION = (By.ID, "todayDiscoveryUnit") # 오늘의 발견 섹션
    DISCOVERY_SECTION_IMAGES = (By.CSS_SELECTOR, ".tti-image") # 오늘의 발견 이미지들
    CATEGORY_MENU = (By.ID, "wa-category") # 상단 카테고리 메뉴
    APPLIANCE_DIGITAL_CATEGORY = (By.LINK_TEXT, "가전디지털") # 가전디지털 카테고리 링크
    NOTICE_LINK_FOOTER = (By.CSS_SELECTOR, "a[href='https://mc.coupang.com/ssr/desktop/contact/notice']") # 하단 공지사항 링크
    TOP_BUTTON = (By.CLASS_NAME, "goto-top__button") # 우측 하단 Top Button
    CATEGORY_PROMOTION_IMAGES = (By.CSS_SELECTOR, "#categoryBest_food img") # 카테고리 프로모션 이미지들
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[name='q']") # 검색창
    SEARCH_BUTTON = (By.CSS_SELECTOR, "form[id='wa-search-form'] button[title='검색']") # 검색버튼
    SEARCH_RESULT = (By.ID, "main-content") # 검색 결과 창 콘텐츠
    ERROR_MAIN_CONTENT = (By.ID, "main-content") # 에러 발생 시 메인 콘텐츠 영역
    
class ProductDetailPageLocators:
    PRODUCT_TITLE = (By.CSS_SELECTOR, ".product-title span") # 상품명
    PRODUCT_PRICE = (By.CLASS_NAME, "price-amount") # 가격
    MAIN_PRODUCT_IMAGE = (By.CSS_SELECTOR, "img[alt='Product image']") # 메인 상품 이미지
    THUMBNAIL_IMAGES = (By.CSS_SELECTOR, "ul.twc-w-\\[70px\\] li") # 썸네일 이미지 목록 (li 태그)
    ROCKET_BADGE = (By.CSS_SELECTOR, "div.price-badge img") # 로켓 배송 뱃지
    REVIEW_LINK = (By.XPATH, "//a[contains(text(), '상품평')]") # '상품평' 텍스트를 포함하는 링크
    REVIEW_HEADER = (By.CSS_SELECTOR, "div.review-header") # 리뷰 섹션의 헤더
    OPTION_PICKER_SELECT = (By.CSS_SELECTOR, "div.option-picker-select") # 옵션 선택 드롭다운
    OPTION_LIST_FIRST_CHILD = (By.CSS_SELECTOR, "ul.custom-scrollbar > li:first-child") # 옵션 목록의 첫 번째 항목
    
class CommonLocators:
    POPUP_CLOSE_BUTTON_1 = (By.CLASS_NAME, "close-banner-icon-button") # 1번 팝업 닫기 버튼
    POPUP_CLOSE_BUTTON_2 = (By.ID, "bottomSheetBudgeCloseButton") # 2번 팝업 닫기 버튼