# Product Detail Page - Coupang 상품 상세 페이지 요소와 메서드를 정리

from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utils.locators import ProductDetailPageLocators
from selenium.common.exceptions import TimeoutException

class ProductDetailPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
    
    def get_product_name(self):
        """
        상품 상세 페이지의 상품명 반환
        """
        return self.get_element_text(ProductDetailPageLocators.PRODUCT_TITLE)
    
    def get_product_price(self):
        """
        상품 상세 페이지의 가격 반환
        """
        return self.get_element_text(ProductDetailPageLocators.PRODUCT_PRICE)
    
    def is_product_name_displayed(self):
        """
        상품명이 화면에 표시되는지 확인
        """
        return self.is_element_displayed(ProductDetailPageLocators.PRODUCT_TITLE)
    
    def is_product_price_displayed(self):
        """
        상품 가격이 화면에 표시되는지 확인
        """
        return self.is_element_displayed(ProductDetailPageLocators.PRODUCT_PRICE)
    
    def is_main_image_displayed(self):
        """
        메인 상품 이미지가 화면에 표시되는지 확인
        """
        return self.is_element_displayed(ProductDetailPageLocators.MAIN_PRODUCT_IMAGE)

    def get_main_image_src(self):
        """
        현재 메인 상품 이미지의 src 속성을 반환
        """
        main_image = self.find_element(ProductDetailPageLocators.MAIN_PRODUCT_IMAGE)
        return main_image.get_attribute("src")

    def get_all_thumbnail_images(self):
        """
        모든 썸네일 이미지 WebElement들을 반환
        """
        return self.find_elements(ProductDetailPageLocators.THUMBNAIL_IMAGES)

    def hover_on_thumbnail_and_get_src(self, thumbnail_element):
        """
        주어진 썸네일 요소에 마우스를 올리고,
        해당 썸네일의 원본 이미지 src를 반환
        """
        # 현재 메인 이미지의 src를 저장
        original_main_src = self.get_main_image_src()
        
        # 썸네일 요소 내의 img 태그를 찾아 src 속성 가져오기
        img_tag = thumbnail_element.find_element(By.TAG_NAME, "img")
        thumbnail_src = img_tag.get_attribute("src")
        
        # 메인 이미지 src와 비교할 수 있도록 썸네일 src의 사이즈를 조정
        processed_thumbnail_src = thumbnail_src.replace("48x48ex", "492x492ex") 
        
        # 썸네일에 마우스를 호버링
        self.action.move_to_element(thumbnail_element).perform()
        self.random_sleep(3, 4) # 호버 후 잠시 대기
        
        return processed_thumbnail_src
    
    def is_rocket_badge_displayed(self):
        """
        로켓배송 뱃지가 화면에 표시되는지 확인
        """
        try:
            self.wait.until(EC.visibility_of_element_located(ProductDetailPageLocators.ROCKET_BADGE))
            return True
        except:
            return False
            
    def get_rocket_badge_alt_text(self):
        """
        로켓배송 뱃지의 alt 텍스트를 반환 (이미지 뱃지일 경우)
        """
        rocket_badge_element = self.find_element(ProductDetailPageLocators.ROCKET_BADGE)
        return rocket_badge_element.get_attribute("alt")

    # [TC-PDP-005] 옵션 관련 메서드
    _OPTION_PICKER_SELECT = (By.CSS_SELECTOR, "div.option-picker-select") # 옵션 선택 드롭다운
    _OPTION_LIST_FIRST_CHILD = (By.CSS_SELECTOR, "ul.custom-scrollbar > li:first-child") # 옵션 목록의 첫 번째 항목

    def get_all_option_pickers(self):
        """
        모든 옵션 선택 드롭다운 요소를 반환
        """
        return self.find_elements(self._OPTION_PICKER_SELECT)

    def select_first_option_in_picker(self, picker_element):
        """
        주어진 옵션 선택 드롭다운에서 첫 번째 옵션을 선택하고,
        선택된 옵션의 텍스트를 반환
        """
        self.human_like_click(picker_element)
        
        first_option_li = self.find_element(self._OPTION_LIST_FIRST_CHILD)
        selected_option_text = self.get_element_text(first_option_li)
        
        self.human_like_click(first_option_li)
        return selected_option_text

    def get_option_picker_text(self, picker_element):
        """
        주어진 옵션 선택 드롭다운의 현재 선택된 옵션 텍스트를 반환
        """
        return picker_element.text
    
    def find_and_click_review_link(self, max_scroll_attempts=5):
        """
        '상품평' 링크를 찾을 때까지 페이지를 스크롤하고 클릭
        """
        attempt = 0 # 스크롤 시도 횟수
        while attempt < max_scroll_attempts:
            try:
                # 리뷰 링크가 클릭 가능한 상태가 될 때까지 대기
                review_link = self.wait.until(EC.element_to_be_clickable(ProductDetailPageLocators.REVIEW_LINK))
                print("리뷰 링크를 찾았습니다. 클릭합니다.")
                self.human_like_click(review_link)
                return True # 클릭 성공
            except TimeoutException:
                # 요소를 못 찾았을 경우, 스크롤을 시도
                print(f"리뷰 링크를 찾지 못했습니다 (시도 {attempt+1}/{max_scroll_attempts}). 페이지를 스크롤합니다.")
                # BasePage의 scroll_to_bottom을 사용하여 조금씩 스크롤
                # 전체를 다 내리지 않고 필요한 만큼만 내릴 수 있도록 조정 가능
                self.driver.execute_script("window.scrollBy(0, window.innerHeight);") # 한 화면 높이만큼 스크롤
                self.random_sleep(1, 2) # 스크롤 후 대기
                attempt += 1
                
        print("최대 스크롤 시도 횟수에 도달했지만 리뷰 링크를 찾지 못했습니다.")
        return False # 클릭 실패

    def is_review_header_displayed(self):
        """
        리뷰 섹션의 헤더가 화면에 표시되는지 확인
        """
        try:
            # 리뷰 헤더가 가시적인 상태가 될 때까지 기다립니다.
            self.wait.until(EC.visibility_of_element_located(ProductDetailPageLocators.REVIEW_HEADER))
            return True
        except TimeoutException:
            return False
        
    def get_all_option_pickers(self):
        """모든 옵션 선택 드롭다운 요소를 반환"""
        return self.find_elements(ProductDetailPageLocators.OPTION_PICKER_SELECT)

    def select_first_option_in_picker(self, picker_element):
        """
        주어진 옵션 피커 드롭다운을 클릭하고,
        첫 번째 옵션을 선택한 후, 선택된 옵션의 텍스트를 반환
        """
        self.human_like_click(picker_element) # BasePage의 human_like_click 사용
        
        first_option_li = self.wait.until(EC.visibility_of_element_located(ProductDetailPageLocators.OPTION_LIST_FIRST_CHILD))
        selected_option_text = self.get_element_text(first_option_li) # 텍스트 미리 저장
        
        self.human_like_click(first_option_li)
        return selected_option_text

    def get_option_picker_text(self, picker_element):
        """옵션 피커 드롭다운에 현재 표시된 텍스트를 반환"""
        return picker_element.text