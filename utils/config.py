# Webdriver 환경 설정 - 프로젝트 전체의 설정값, 상수, 환경 변수

import random
from dotenv import load_dotenv
import os

class Config:
  BASE_URL = "https://www.coupang.com"
  IMPLICIT_WAIT_TIME = 5 # driver.implicitly_wait()에 사용
  EXPLICIT_WAIT_TIME = 10 # WebDriverWait에 사용

  # User Agent 데이터 관련
  USER_AGENTS = [
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
      "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.117 Safari/537.36"
  ]

  def __init__(self):
      load_dotenv()
      self.COUPANG_ID = os.environ.get("COUPANG_ID")
      self.COUPANG_PW = os.environ.get("COUPANG_PW")

# Config 인스턴스 생성
config_instance = Config()
