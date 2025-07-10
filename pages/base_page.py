# Base Page - Webdriver와 Page에서의 공통적인 사용 메서드를 정리

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
from utils.config import Config
from selenium.webdriver.remote.webelement import WebElement # WebElement 타입 임포트

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
        
    def human_like_hover(self, locator, human_like=True):
        """
        특정 로케이터의 웹 요소에 인간처럼 마우스 오버
        human_like=True : 인간처럼 마우스 오버하는 동작을 시뮬레이션
        """
        element = self.find_element(locator)
        if human_like:
            self.action.move_to_element(element).pause(random.uniform(0.4, 0.9)).perform()
        else:
            self.action.move_to_element(element).perform()
        self.random_sleep(0.5, 1.5) # 오버 후 짧은 슬립
    
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
    
    def scroll_to_element(self, locator_or_element):
        """
        주어진 로케이터(tuple) 또는 WebElement 객체로 스크롤
        """
        if isinstance(locator_or_element, WebElement): # 이미 WebElement 객체인 경우
            element = locator_or_element
        else: # 로케이터 튜플인 경우 (By.ID, "...")
            element = self.find_element(locator_or_element) # find_element를 사용하여 요소를 찾음
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        self.random_sleep(0.5, 1.5)
        
    def scroll_to_bottom(self, pause_time=None):
        """
        페이지의 최하단까지 스크롤하기
        새로운 컨텐츠가 로드될 때까지 대기
        """
        if pause_time is None:
            pause_time = random.uniform(1, 3) # 기본 랜덤 대기 시간

        last_height = self.driver.execute_script("return document.body.scrollHeight")
       
        while True:
            # 스크롤 가장 아래로 내리기
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.random_sleep(pause_time, pause_time) # 지정된 시간 동안 대기

            # 새로운 높이 측정
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break  # 더 이상 로딩된 컨텐츠가 없을 경우 종료
            last_height = new_height
        self.random_sleep(1, 2) # 스크롤 완료 후 마지막 대기
    
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
    
    def switch_to_new_window(self):
        """새로 열린 윈도우(탭)로 전환"""
        self.wait.until(EC.number_of_windows_to_be(2)) # 새 창이 뜰 때까지 기다림
        original_window = self.driver.current_window_handle
        for window_handle in self.driver.window_handles:
            if window_handle != original_window:
                self.driver.switch_to.window(window_handle)
                break
        self.random_sleep(1, 2) # 전환 후 대기
        return original_window # 이전 윈도우 핸들을 반환하여 필요시 다시 전환 가능
    
    def switch_to_original_window(self, original_window_handle):
        """원래 윈도우(탭)로 다시 전환"""
        self.driver.switch_to.window(original_window_handle)
        self.random_sleep(1, 2) # 전환 후 대기