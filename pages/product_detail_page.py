# Product Detail Page - Coupang 상품 상세 페이지 요소와 메서드를 정리

from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utils.config import Config

# PDP 전용 로케이터
class ProductDetailPageLocators:
    PRODUCT_TITLE = (By.CSS_SELECTOR, ".product-title span") # 상품명
    PRODUCT_PRICE = (By.CLASS_NAME, "price-amount") # 가격
    MAIN_PRODUCT_IMAGE = (By.CSS_SELECTOR, "img[alt='Product image']") # 메인 상품 이미지
    THUMBNAIL_IMAGES = (By.CSS_SELECTOR, "ul.twc-w-\\[70px\\] li") # 썸네일 이미지 목록 (li 태그)
    ROCKET_BADGE = (By.CSS_SELECTOR, "div.price-badge img") # 로켓 배송 뱃지

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
        img_tag = thumbnail_element.find_element(By.TAG_NAME, "img")
        thumbnail_src = img_tag.get_attribute("src")
        
        # 메인 이미지 src와 비교할 수 있도록 썸네일 src의 사이즈를 조정
        processed_thumbnail_src = thumbnail_src.replace("48x48ex", "492x492ex") 

        # 썸네일에 마우스를 호버링
        self.actions.move_to_element(thumbnail_element).perform()
        self.random_sleep(0.5, 1.0) # 호버 후 잠시 대기

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