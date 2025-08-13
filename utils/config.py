# Webdriver 환경 설정 - 프로젝트 전체의 설정값, 상수, 환경 변수

from dotenv import load_dotenv, find_dotenv
import os

class Config:
    BASE_URL = "https://www.coupang.com"
    IMPLICIT_WAIT_TIME = 5 # driver.implicitly_wait()에 사용
    EXPLICIT_WAIT_TIME = 10 # WebDriverWait에 사용

    # User Agent 데이터 관련 (모바일 User-Agent만 사용)
    USER_AGENTS = [
        # Mobile User-Agents (Android Chrome)
        "Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; Samsung SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36",
    ]

    def __init__(self):
        # 1. Jenkins 환경 변수를 먼저 가져오기
        self.COUPANG_ID = os.environ.get("COUPANG_ID")
        self.COUPANG_PW = os.environ.get("COUPANG_PW")

        # 2. Jenkins 환경 변수가 없는 경우에만, .env 파일을 로드
        # 로컬 개발 환경용
        if self.COUPANG_ID is None or self.COUPANG_PW is None:
            dotenv_path = os.path.join(os.getcwd(), '.env')
            if os.path.exists(dotenv_path):
                load_dotenv(dotenv_path=dotenv_path, override=True, verbose=True) # override=True는 기존 환경변수 덮어쓰기
                self.COUPANG_ID = os.environ.get("COUPANG_ID")
                self.COUPANG_PW = os.environ.get("COUPANG_PW")
            else:
                print(f"env 파일을 찾을 수 없습니다. - {dotenv_path}. 환경 변수를 설정해주세요")

        # 디버깅을 위한 최종 값 확인 (나중에 삭제)
        if self.COUPANG_ID is None:
            print("쿠팡 아이디가 None입니다. 환경 변수를 확인해주세요.")
        if self.COUPANG_PW is None:
            print("쿠팡 비밀번호가 None입니다. 환경 변수를 확인해주세요.")

# Config 인스턴스 생성
config_instance = Config()