"""
접속 확인 스크립트 — 테스트 전에 한 번 실행.
문화포털 화면과 Open API 에 이 환경에서 접속되는지 확인함.
(해외 서버에서 국내 공공 사이트 접속이 막히는 경우가 있어 먼저 확인)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import requests  # noqa: E402

from config import settings  # noqa: E402
from utils.api_client import CultureApiClient  # noqa: E402

ok = True

print("1) 문화포털 화면 접속 확인")
try:
    r = requests.get("https://www.culture.go.kr/", timeout=15)
    print(f"   HTTP {r.status_code} → {'정상' if r.status_code == 200 else '확인 필요'}")
    ok &= r.status_code == 200
except requests.RequestException as e:
    print(f"   접속 실패: {e}")
    ok = False

print("2) Open API 호출 확인 (period2)")
if not settings.SERVICE_KEY:
    print("   .env 에 SERVICE_KEY 가 없음 → .env 파일을 먼저 채우세요")
    ok = False
else:
    try:
        res = CultureApiClient().period("20190616", "20191231", rows=1)
        print(f"   {res.summary()}")
        if res.ok:
            print("   → 정상 (resultCode 00)")
        else:
            print("   → 실패. 승인 직후라면 몇 시간 뒤 다시 시도. resultCode 30이면 키 확인")
            ok = False
    except requests.RequestException as e:
        print(f"   접속 실패: {e}")
        ok = False

print("\n결과:", "모두 정상 — 테스트를 실행해도 됨" if ok else "위 메시지를 확인하세요")
sys.exit(0 if ok else 1)
