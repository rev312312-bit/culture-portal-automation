"""
프로젝트 설정 모음.

- 인증키 같은 비밀값은 코드에 쓰지 않고 .env 파일(내 컴퓨터/Codespaces)과
  GitHub Secrets(CI)에서 읽어 옴.
- '확인 필요'라고 표시된 값은 실제 화면·미리보기로 한 번 확인한 뒤 고치면 됨.
"""
import os

from dotenv import load_dotenv

load_dotenv()

# ── 문화포털 Open API (한국문화정보원_한눈에보는문화정보조회서비스) ──────────────
SERVICE_KEY = os.getenv("SERVICE_KEY", "").strip()
API_BASE_URL = os.getenv("API_BASE_URL", "https://apis.data.go.kr/B553457/cultureinfo")
API_TIMEOUT = float(os.getenv("API_TIMEOUT", "15"))

# 실서버 배려: 호출 사이 최소 간격(초). 초당 호출량 초과(에러코드 23) 방지.
API_CALL_INTERVAL = float(os.getenv("API_CALL_INTERVAL", "0.3"))

# area2 / realm2 요청 파라미터 이름 — 확인 필요
# 공공데이터포털 활용신청 상세 > 미리보기(열기) 화면의 파라미터 이름으로 바꿀 것
AREA_PARAM = os.getenv("AREA_PARAM", "sido")
REALM_PARAM = os.getenv("REALM_PARAM", "realmCode")

# ── 문화포털 화면 ─────────────────────────────────────────────────────────────
# pytest.ini 의 base_url(https://www.culture.go.kr) 뒤에 붙는 경로
PAGES = {
    "main": "/",
    # 확인 필요: 즐겨요 문화정보 > 한눈에 보는 문화정보 '목록' 화면 주소창 경로
    "info_list": os.getenv(
        "PAGE_INFO_LIST", "/portal/cltInfo/oneCltInfo/list.do?menuNo=200010"
    ),
    # 상세 화면 (pblprfrSn 값이 API의 seq와 같은지는 2주 차에 확인)
    "info_detail": "/portal/cltInfo/oneCltInfo/oneCltInfoView.do?menuNo=200010&pblprfrSn={seq}",
    "nearby": "/portal/cltInfo/locCltEvt/list.do?menuNo=200168",
    # 확인 필요: 즐겨요 문화정보 > 문화캘린더 화면 주소창 경로
    "calendar": os.getenv("PAGE_CALENDAR", "/calendar/view.do"),
}

# ── Restful-Booker (2주 차 CRUD 보완용 공개 연습 API) ─────────────────────────
BOOKER_URL = os.getenv("BOOKER_URL", "https://restful-booker.herokuapp.com")
BOOKER_USER = os.getenv("BOOKER_USER", "admin")
BOOKER_PASSWORD = os.getenv("BOOKER_PASSWORD", "password123")
