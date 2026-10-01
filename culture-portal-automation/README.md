# 문화포털 자동화 테스트

운영 중인 [문화포털](https://www.culture.go.kr)을 대상으로 만든 Python 자동화 테스트입니다.
수동 테스트케이스(TC)를 BDD 시나리오로 옮기고, 그 시나리오가 실제로 실행되도록 Playwright·pytest-bdd로 구현했습니다.
화면 테스트와 함께 문화포털 Open API 테스트도 포함합니다.

| 구분 | 내용 |
|---|---|
| 대상 | 문화포털 실서버 (화면 + 한국문화정보원 Open API) |
| 언어·도구 | Python · Playwright · pytest · pytest-bdd · requests |
| 범위 | 즐겨요 문화정보 영역 (한눈에 보는 문화정보, 내 주변 문화콘텐츠, 문화캘린더) |
| 실행 | 로컬/Codespaces, GitHub Actions |

> 시나리오 출처: SW 테스팅 교육과정 팀 프로젝트에서 작성한 문화포털 수동 TC 중
> 본인 담당 영역인 '즐겨요 문화정보'를 중심으로 선정했습니다. (팀 산출물 기반)

## 수동 TC → BDD 시나리오 → 자동화 스크립트

```
팀 수동 TC (FN_INFO_001)
   └─ features/info_search.feature   @tc_FN_INFO_001  Scenario: UI-검색-필수값-001
        └─ tests/ui/test_info_search.py   단계(step) 구현
             └─ pages/info_search_page.py  화면 조작(Page Object)
```

- 시나리오마다 `@tc_<수동 TC ID>` 태그로 원본 TC를 연결합니다.
- 전체 추적표는 `docs/` 의 TC 엑셀(추적표 시트)에 있습니다.

### 이미 보고된 결함을 테스트로 고정하기

수동 테스트에서 찾은 결함은 `@defect_<결함 ID>` 태그를 붙여 자동화했습니다.

| 상태 | 결과 표시 | 의미 |
|---|---|---|
| 결함이 남아 있음 | `XFAIL` (예상된 실패) | 정상. CI 는 통과 |
| 결함이 고쳐짐 | `XPASS(strict)` → 실패 | 시나리오에서 결함 태그를 떼라는 신호 |
| 화면 요소를 못 찾음 등 | `FAILED` | 테스트 코드 점검 필요 |

`raises=AssertionError` 로 설정해, 기대결과 확인 단계의 실패만 결함으로 인정합니다.
로케이터 오류 같은 다른 실패가 결함으로 잘못 처리되지 않게 하기 위해서입니다.

## 폴더 구조

```
features/           BDD 시나리오 (.feature)
tests/ui/           시나리오 단계 구현 (pytest-bdd)
tests/api/          Open API 테스트 (pytest + requests)
pages/              화면별 Page Object — 로케이터를 한곳에 모음
utils/api_client.py API 호출·XML 해석·호출 간격 제어
config/settings.py  주소·파라미터 이름 등 설정 (비밀값은 .env)
data/               테스트 데이터 (분야 12개, 지역, 좌표 범위)
scripts/            설치·접속 확인 스크립트
```

## 실서버 운영 규칙

운영 중인 공공 서비스라서 아래 규칙을 지킵니다.

- **조회만 함:** 회원가입·댓글·신청처럼 데이터를 만드는 기능은 자동화하지 않음
- **robots.txt 준수:** 통합검색(`/portal/search`)은 대상에서 제외
- **호출 간격:** API 호출 사이 0.3초 이상 (초당 호출량 초과 오류 23 방지)
- **실행 빈도:** push 때는 smoke 만, 전체 실행은 수동으로만. 병렬 실행 안 함
- **데이터 변동 대응:** 결과 건수를 고정값으로 비교하지 않고, '선택한 조건과 결과가 일치하는지' 같은 규칙으로 검증
- **인증키 관리:** 코드에 넣지 않고 `.env`(로컬)와 GitHub Secrets(CI)로 관리. 활용기간 만료 시 오류 31

## 시작하기 (GitHub Codespaces)

1. 저장소에서 **Code → Codespaces → Create codespace on main**
2. 터미널에서 설치
   ```bash
   bash scripts/setup.sh
   ```
3. `.env` 파일을 열어 `SERVICE_KEY` 입력
4. 접속 확인
   ```bash
   python3 scripts/check_connection.py
   ```
5. 테스트 실행
   ```bash
   pytest -m api          # API 테스트만
   pytest -m smoke        # 핵심 흐름만
   pytest                 # 전체
   pytest -k 검색          # 이름에 '검색'이 들어간 테스트만
   ```
6. 결과: `reports/report.html` (실패한 화면 테스트는 `test-results/` 에 스크린샷·trace 저장)
   - trace 파일은 내려받아 [trace.playwright.dev](https://trace.playwright.dev) 에 끌어다 놓으면 단계별 화면을 볼 수 있음

## GitHub Actions

- `main` 에 push 하면 smoke 테스트 실행
- Actions 탭 → tests → Run workflow 에서 범위(smoke/all)와 브라우저(chromium/firefox/webkit) 선택
- 저장소 Settings → Secrets and variables → Actions 에 `SERVICE_KEY` 등록 필요

## 확인 필요 항목 (진행 중)

| 항목 | 위치 | 확인 방법 |
|---|---|---|
| 한눈에 보는 문화정보 목록 주소 | `config/settings.py` PAGES | 화면 주소창 |
| 문화캘린더 주소 | `config/settings.py` PAGES | 화면 주소창 |
| 화면 로케이터 | `pages/*.py` 각 클래스 상단 | 실패 시 trace 로 확인 후 수정 |
| area2·realm2 파라미터 이름 | `config/settings.py` | 공공데이터포털 미리보기 |
| 분야 코드 12개 | `data/test_data.json` | 공공데이터포털 미리보기 |
| livelihood2 파라미터 | `tests/api/test_calendar_api.py` | 공공데이터포털 미리보기 |
