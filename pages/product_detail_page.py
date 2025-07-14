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