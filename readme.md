## Coupang UI Automation Test
#### `SDET로써 성장을 위한 대형사이트 기반 UI 자동화 테스트 프레임워크`

이 프로젝트는 쿠팡 웹사이트의 핵심 기능에 대한 자동화 테스트 프레임워크를 구축하여 **테스트 코드의 품질과 지속적인 통합(CI) 역량**을 높이고자 제작하였습니다.

단순히 테스트 스크립트를 작성하는 것을 넘어, 실제 현업에서 발생하는 다양한 문제들을 해결하며 프레임워크를 고도화하는 과정을 담았습니다.

***

### 1. 기술 스택 및 환경
이 프로젝트는 자동화 테스트 엔지니어로서 요구되는 다양한 기술 스택을 활용하여 구축되었습니다.

-   **언어 및 도구:** Python, Pytest, Selenium, webdriver-manager
-   **CI/CD:** Jenkins
-   **협업 및 버전 관리:** Git
-   **OS환경:** macOS

***

### 2. 프로젝트 설계와 특징
이 프레임워크는 유지보수성과 신뢰성을 최우선으로 고려하여 설계했습니다.

-   **Page Object Model (POM) 도입:** 웹 페이지의 UI 요소와 상호작용 로직을 `pages` 폴더 내의 별도 클래스로 분리했습니다. `BasePage`를 통해 공통 기능을 추상화하고, `Utils/locators.py`에서 모든 로케이터를 중앙 관리하여 코드의 재사용성과 유지보수성을 극대화했습니다.
-   **봇 감지 회피 전략:** 쿠팡의 강력한 봇 감지 시스템에 대응하기 위해 다양한 기법을 적용했습니다.
    1.  **데스크톱 / 모바일 User-Agent 분리하여 활용:** 데스크톱 UA와 모바일 UA를 분리하여 봇 감지에 둔감한 부분은 데스크톱, 민감한 부분은 모바일 UA로 분리해서 테스트를 진행했습니다.
    2.  **`WebDriver` 세션 관리:** 봇 감지에 취약한 Main, PDP 테스트를 `function` 스코프의 전용 드라이버(`mobile_driver`)를 사용하고, 로그인 테스트는 `session` 스코프의 `driver`를 공유하여 효율성과 신뢰성을 동시에 잡았습니다.
-   **테스트 복원력 확보:** `go_to_url()` 메서드에 재시도(Retry) 로직을 추가하여, 일시적인 네트워크 오류나 서버 문제에 대한 테스트의 복원력을 높였습니다.

***

### 3. 프로젝트 실행

이 프로젝트는 `pytest`와 `Jenkins`를 통해 실행할 수 있습니다.

-   **로컬 환경에서 Pytest 실행**
    1.  `pip install -r requirements.txt`
    2.  `pytest -s -v`
-   **Jenkins CI/CD를 통한 실행**
    1.  Jenkins Job 설정
    2.  `Build Steps`에서 Pytest 명령어 실행
        `pytest -s -v --html=report.html --self-contained-html tests/login/ tests/main/ tests/pdp/`

***

### 4. 주요 트러블슈팅 사례
프로젝트 진행 중 어려움을 겪었던 사례들을 해결한 부분입니다.

1. TimeoutException - 슬래시('/') 하나가 일으킨 문제
    * 문제: `driver.get("https://www.coupang.com")`을 실행, `EC.url_to_be("https://www.coupang.com")` 조건에서 TimeoutException 발생.

    * 원인: WebDriver는 https://www.coupang.com에 접근하면 자동으로 https://www.coupang.com/로 URL을 변경했습니다. EC.url_to_be()는 URL이 정확히 일치하는지(==)를 검사하기 때문에, 슬래시 하나의 차이로 불일치하여 TimeoutException이 발생했습니다.

    * 해결: BASE_URL 변수를 "https://www.coupang.com/"와 같이 끝에 슬래시를 명시적으로 포함하도록 수정하여, WebDriver의 동작과 기대결과를 일치시킴.

2. TypeError: find_element에 WebElement 전달 오류
    * 문제: `find_element(*locator)` 메서드에 WebElement 객체를 전달하여 TypeError가 발생. 해당 오류는 '리뷰 영역 확인'(TC-PDP-004) 및 '상품 옵션 적용'(TC-PDP-005) 테스트에서 반복적 발생.

    * 원인: WebElement 객체는 이미 요소를 찾은 상태이므로, 다시 find_element()를 호출할 필요가 없습니다. 하지만 메서드 내에서 WebElement를 로케이터처럼 사용하면서 오류가 발생했습니다.

    * 해결: click_element() 메서드를 로케이터를 받는 역할로, human_like_click() 메서드를 WebElement 객체를 받는 역할로 명확하게 분리.

3. **봇 감지 시스템에 의한 WebDriver 세션 종료 (Hard)**
    * 문제: `go_to_url()` 메서드 실행 시 `invalid session id: session deleted as the browser has closed the connection `오류 발생.

    * 원인: 쿠팡의 강력한 봇 감지 시스템이 WebDriver를 감지하고 브라우저 프로세스를 강제로 종료한 것이 가장 유력한 원인인 듯 합니다. 이는 단순한 네트워크 오류가 아닌 자동화 도구를 감지하고 프레임워크 자체에 대한 강력한 차단이라고 판단했습니다.

    * 해결 : 3가지의 방법
      - User-Agent 변경: 모바일 User Agent는 상대적으로 데스크톱 User Agent 보다 마우스 감지가 덜하고, 감지가 느슨하여 봇 감지가 민감한 검색 또는 카테고리 부분은 모바일 UA로 변경하여 테스트를 수행했습니다.

      - chrome_options 추가: ---disable-gpu, ---no-sandbox 등 봇 감지 회피에 도움이 되는 다양한 옵션을 conftest.py에 추가하여 브라우저의 `자동화 흔적`을 최소화했습니다.

      - 사람처럼 행동하는 메서드 : human_like_click, ~scroll, ~hover 등, 봇처럼 휙휙 움직이는게 아닌 사람처럼 움직이는 듯한 동작 메서드를 추가하여 실제 사람이 웹사이트를 움직이는 듯하게 테스트를 수행했습니다.

***

### 5. 프로젝트 회고

이 프로젝트를 진행하면서 자동화 테스트의 본질에 대해 깊이 고민할 수 있었습니다. 단순히 테스트 코드를 작성하는 것을 넘어, 아래와 같은 경험들을 얻었습니다.


-   **추상화(Abstraction)와 재사용성(Reusability)의 가치:**
    복잡한 WebDriver 코드를 BasePage와 MainPage의 메서드로 추상화하여, 테스트 코드를 마치 사용자의 행동 시나리오처럼 읽히게 했습니다. 이러한 높은 수준의 추상화 덕분에 테스트 코드의 가독성이 향상되었고, 여러 테스트 파일에서 click_element(), go_to_url()과 같은 코드를 반복적으로 재사용할 수 있었습니다. 이는 자동화 테스트의 생산성을 극대화하는 중요한 경험이었습니다.

-   **'될 때도 있고 안 될 때도 있는' 테스트의 문제점 파악:**
    테스트가 때로 에러가 나거나 실패할 때, 원인은 코드의 버그뿐만 아니라 **외부 환경(네트워크 상황, 봇 감지, 브라우저 버전 등)** 에 있을 수 있다는 것을 깨달았습니다. 이를 막기 위해, retry같은 테스트 복원력 확보 또는 촘촘한 실패 관련 로그를 작성하여 출력함으로써 빠르게 외부환경 문제점을 파악할 수 있었습니다.

-   **복잡한 문제 해결 과정의 중요성:**
    `TimeoutException`, `AttributeError`, `ERR_HTTP2_PROTOCOL_ERROR` 등 수많은 오류에 직면했습니다. 이 과정에서 단순히 오류를 우회하는 것이 아닌, `WebDriver` 세션 로그, `curl` 명령어, `selenium-wire` 같은 도구를 활용하여 문제의 근본 원인을 파고드는 디버깅 능력을 키울 수 있었습니다.

-   **CI/CD 환경에서의 테스트 운영 능력:**
    Jenkins를 통해 테스트를 CI/CD 파이프라인에 통합하면서, 테스트 환경 설정, Credential 관리, HTML 보고서 게시 등 CI/CD 환경에서 테스트를 운영하는 능력을 능숙하게 다룰 수 있게 되었습니다. 테스트 코딩을 넘어, CI/CD 시스템과 연동하여 테스트를 안정적으로 실행하는 중요한 경험을 얻었습니다.