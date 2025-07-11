# Product Detail Page - Coupang 상품 상세 페이지 요소와 메서드를 정리

from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utils.config import Config

# PDP 전용 로케이터
class ProductDetailPageLocators:
    PRODUCT_TITLE = (By.CSS_SELECTOR, ".product-title span") # 상품명
    PRODUCT_PRICE = (By.CLASS_NAME, "price-amount") # 가격

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