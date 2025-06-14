# 쿠팡 웹사이트 자동화 테스트

## E2E 자동화 테스트 실패 과정 및 분석

본 프로젝트는 `pytest`와 `Selenium`을 활용하여 쿠팡 웹사이트의 검색부터 결제까지의 E2E 자동화 테스트를 구현하는 것을 목표로 했습니다. 그러나, 강력한 봇 감지 시스템으로 인해 `ERR_HTTP2_PROTOCOL_ERROR`가 발생하여 테스트가 실패하였고, 이에 대한 원인 분석 및 후속 조치를 정리합니다.

---

## 1. 문제 발생 과정: 검색 테스트 코드 작성 중 ERR_HTTP2_PROTOCOL_ERROR 발생

- **초기 테스트 목표**: 사용자가 쿠팡 메인 페이지에 접속 → 검색어 입력 → 검색 결과 페이지 정상 로드 여부 검증
- **로그인 자동화 성공**
- **검색 시도 코드**:
  ```python
  search_input.send_keys("노트북")
  search_button.click()
  ```
- **결과**: 검색 결과 페이지 대신 다음과 같은 오류 발생
  ```
  이 웹페이지를 사용할 수 없음 - ERR_HTTP2_PROTOCOL_ERROR
  ```

---

## 2. 실패 원인 분석: 쿠팡의 고도화된 봇 감지 시스템

수동으로 검색했을 때는 문제가 없었기 때문에, Selenium을 통한 자동화 접근이 감지되어 차단된 것으로 판단했습니다. 쿠팡은 다음과 같은 봇 감지 메커니즘을 활용하는 것으로 보입니다:

### 주요 감지 요소

- **브라우저 지문 분석**
  - `navigator.webdriver`
  - `User-Agent`, 해상도, WebGL, `window.chrome` 등
- **행동 패턴 분석**
  - 클릭/입력 속도, 마우스 이동, 스크롤 등
- **IP 및 요청 빈도**
  - 짧은 시간 내 반복 요청 감지
- **HTTP 헤더 분석**
  - 일반 브라우저와 다른 `User-Agent`, `Accept-Language` 등
- **프로토콜 차단**
  - HTTP/2 연결을 서버에서 강제로 끊으며 발생하는 `ERR_HTTP2_PROTOCOL_ERROR`

---

## 3. 문제 해결 시도: 스텔스 기능 + 인간 행동 시뮬레이션

### 기술적 우회 시도 목록

- `selenium-stealth` 라이브러리 적용
  - `navigator.webdriver = false`
  - WebGL, vendor 정보 등 위장

- **Chrome Options 조정**
  ```python
  options.add_argument("--start-maximized")
  options.add_argument("user-agent=...")
  options.add_experimental_option("excludeSwitches", ["enable-automation"])
  options.add_experimental_option("useAutomationExtension", False)
  options.add_argument("--disable-blink-features=AutomationControlled")
  ```

- **인간적인 행동 시뮬레이션**
  - `random.uniform()`으로 불규칙한 `sleep`
  - `ActionChains`로 자연스러운 마우스 이동 및 클릭
  - `send_keys`에 타이핑 딜레이 추가

### 문제 해결 시도 결과

- 로그인 테스트에서는 **일부 성공**
- 그러나 검색 테스트에서는 여전히 `ERR_HTTP2_PROTOCOL_ERROR` 발생 → **차단 유지**

---

## 4. 후속 조치 및 결론

### 결론

- 지속적인 우회 시도는 학습 효율을 낮추고 프로젝트 목적과 멀어짐
- 쿠팡의 감지 시스템은 매우 강력하여 상용 봇도 뚫기 어려움
- **검색 기능 테스트 코드는 유지**하되, 실패는 **예상된 결과**로 간주함

### 향후 계획

- **쿠팡 외 봇감지가 약한 해외사이트**로 E2E 테스트 대상을 변경
- **쿠팡에서 봇 감지를 하지않는 페이지 이동 및 상세페이지 테스트만 진행**