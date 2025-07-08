# Base Page - Webdriver와 Page에서의 공통적인 사용 메서드를 정리

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
from utils.config import Config

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        # 명시적 대기 객체 초기화 (Config에서 설정 시간 가져옴)
        self.wait = WebDriverWait(self.driver, Config.EXPLICIT_WAIT_TIME)
        # 액션 체인 객체 초기화
        self.action = ActionChains(self.driver)

    def go_to_url(self, url):
        """주어진 URL로 이동"""
        self.driver.get(url)
        self.random_sleep() # 페이지 로딩 후 랜덤 딜레이
        
    def random_sleep(self, min_time=1, max_time=3):
        """랜덤 시간 동안 슬립"""
        time.sleep(random.uniform(min_time, max_time))
        
    def find_element(self, locator, timeout=None):
        """
        특정 로케이터를 사용하여 웹 요소를 찾고, 요소가 나타날 때까지 대기
        """
        if timeout:
            wait = WebDriverWait(self.driver, timeout)
            return wait.until(EC.presence_of_element_located(locator))
        return self.wait.until(EC.presence_of_element_located(locator))
    
    def find_elements(self, locator, timeout=None):
        """
        특정 로케이터를 사용하여 웹 요소들을 찾고, 요소들이 나타날 때까지 대기
        """
        if timeout:
            wait = WebDriverWait(self.driver, timeout)
            return wait.until(EC.presence_of_all_elements_located(locator))
        return self.wait.until(EC.presence_of_all_elements_located(locator))
    
    def click_element(self, locator, human_like=True):
        """
        특정 로케이터를 사용하여 웹 요소를 클릭
        human_like=True : 인간처럼 클릭하는 동작을 시뮬레이션
        """
        element = self.find_element(locator)
        if human_like:
            self.action.move_to_element(element).pause(random.uniform(0.2, 0.6)).click().perform()
        else:
            element.click()
        self.random_sleep(0.5, 1.5) # 클릭 후 짧은 슬립
    
    def move_mouse_randomly(self, min_offset=10, max_offset=100):
        """
        봇 감지 회피를 위해 마우스를 랜덤으로 움직임.
        """
        self.action.move_by_offset(random.uniform(min_offset, max_offset),
                                    random.uniform(min_offset, max_offset)).perform()
        self.random_sleep(0.5, 1.5) # 무빙 후 짧은 슬립
        
    def type_text(self, locator, text, human_like=True):
        """
        특정 로케이터를 사용하여 텍스트 입력
        human_like=True : 인간처럼 타이핑하는 동작을 시뮬레이션
        """
        element = self.find_element(locator)
        element.clear()
        if human_like: # 인간처럼 타이핑
            for char in text:
                element.send_keys(char)
                self.random_sleep(0.05, 0.15)
        else: # 한 번에 입력
            element.send_keys(text)
        self.random_sleep(0.5, 1.5) # 입력 후 짧은 슬립
    
    def scroll_to_element(self, locator):
        """
        특정 로케이터의 요소로 스크롤
        """
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        self.random_sleep(0.5, 1.5)
    
    def get_element_text(self, locator):
        """특정 로케이터의 웹 요소 텍스트를 리턴"""
        return self.find_element(locator).text

    def is_element_displayed(self, locator):
        """특정 로케이터의 웹 요소가 화면에 표시되는지 확인"""
        try:
            return self.find_element(locator).is_displayed()
        except:
            return False
    
    def is_element_clickable(self, locator, timeout=None):
        """특정 로케이터의 웹 요소가 클릭 가능한 상태인지 확인"""
        try:
            if timeout:
                wait = WebDriverWait(self.driver, timeout)
                wait.until(EC.element_to_be_clickable(locator))
            else:
                self.wait.until(EC.element_to_be_clickable(locator))
            return True
        except:
            return False
    
    def get_page_title(self):
        """현재 페이지의 타이틀을 리턴"""
        return self.driver.title

    def get_current_url(self):
        """현재 페이지의 URL을 리턴"""
        return self.driver.current_url