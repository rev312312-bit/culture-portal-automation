"""
문화포털 Open API 클라이언트.

- 응답이 XML이라서 표준 라이브러리 ElementTree 로 읽음.
- 정상 응답(header/resultCode)과 게이트웨이 오류 응답(returnReasonCode 등)을
  같은 모양(ApiResponse)으로 돌려줘서 테스트에서 똑같이 다룰 수 있게 함.
- 호출 사이에 최소 간격을 둬서 운영 서버에 부담을 주지 않음.
"""
from __future__ import annotations

import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field

import requests

from config import settings

_last_call = 0.0

# 페이징 파라미터 이름 (2026-10-01 실측)
# 공식 사용가이드 예시는 cPage·rows 이지만 실제로는 무시되고,
# 응답 태그와 같은 PageNo·numOfrows(대소문자 구분)만 동작함 → 관찰사항 OBS-001
PAGE_PARAM = "PageNo"
ROWS_PARAM = "numOfrows"


def _throttle(interval: float) -> None:
    """직전 호출 뒤 interval 초가 지나기 전이면 기다림."""
    global _last_call
    wait = interval - (time.monotonic() - _last_call)
    if wait > 0:
        time.sleep(wait)
    _last_call = time.monotonic()


@dataclass
class ApiResponse:
    status_code: int
    text: str
    elapsed_ms: int
    result_code: str | None = None
    result_msg: str | None = None
    total_count: int | None = None
    page_no: int | None = None
    num_of_rows: int | None = None
    items: list[dict] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return self.status_code == 200 and self.result_code == "00"

    def summary(self) -> str:
        """실패 메시지에 붙일 한 줄 요약."""
        body = self.text.replace("\n", " ")[:200]
        return (
            f"HTTP {self.status_code} / resultCode={self.result_code} "
            f"/ msg={self.result_msg} / items={len(self.items)} "
            f"/ totalCount={self.total_count} / body={body}"
        )


def _find_text(root: ET.Element, *paths: str) -> str | None:
    for path in paths:
        node = root.find(path)
        if node is not None and node.text is not None:
            return node.text.strip()
    return None


def _to_int(value: str | None) -> int | None:
    try:
        return int(value) if value is not None else None
    except ValueError:
        return None


def parse_response(status_code: int, text: str, elapsed_ms: int = 0) -> ApiResponse:
    res = ApiResponse(status_code=status_code, text=text, elapsed_ms=elapsed_ms)
    try:
        root = ET.fromstring(text.encode("utf-8"))
    except ET.ParseError:
        # XML이 아닌 응답(예: 'Unauthorized' 같은 일반 문자열)
        return res

    res.result_code = _find_text(
        root, ".//header/resultCode", ".//resultCode", ".//returnReasonCode"
    )
    res.result_msg = _find_text(
        root, ".//header/resultMsg", ".//resultMsg", ".//returnAuthMsg", ".//errMsg"
    )
    res.total_count = _to_int(_find_text(root, ".//totalCount"))
    # 응답 태그 표기 주의: PageNo(대문자 P), numOfrows(소문자 r) — 관찰사항 OBS-001
    res.page_no = _to_int(_find_text(root, ".//PageNo", ".//pageNo"))
    res.num_of_rows = _to_int(_find_text(root, ".//numOfrows", ".//numOfRows"))
    res.items = [
        {child.tag: (child.text or "").strip() for child in item}
        for item in root.iter("item")
    ]
    return res


class CultureApiClient:
    def __init__(
        self,
        service_key: str | None = settings.SERVICE_KEY,
        base_url: str = settings.API_BASE_URL,
        interval: float = settings.API_CALL_INTERVAL,
        timeout: float = settings.API_TIMEOUT,
    ):
        self.service_key = service_key
        self.base_url = base_url.rstrip("/")
        self.interval = interval
        self.timeout = timeout
        self.session = requests.Session()

    def get(self, operation: str, *, include_key: bool = True, **params) -> ApiResponse:
        query = {k: v for k, v in params.items() if v is not None}
        if include_key and self.service_key is not None:
            query = {"serviceKey": self.service_key, **query}
        _throttle(self.interval)
        started = time.monotonic()
        r = self.session.get(f"{self.base_url}/{operation}", params=query, timeout=self.timeout)
        elapsed = int((time.monotonic() - started) * 1000)
        r.encoding = r.encoding or "utf-8"
        return parse_response(r.status_code, r.text, elapsed)

    # ── 오퍼레이션별 단축 메서드 ────────────────────────────────────────────
    def period(self, from_: str, to: str, page: int = 1, rows: int = 10, **extra) -> ApiResponse:
        """기간별 문화정보 목록 (from/to: YYYYMMDD)"""
        return self.get("period2", **{"from": from_, "to": to, PAGE_PARAM: page, ROWS_PARAM: rows, **extra})

    def area(self, area_value: str, from_: str, to: str, rows: int = 10, **extra) -> ApiResponse:
        """지역별 문화정보 목록 — 파라미터 이름은 settings.AREA_PARAM"""
        return self.get(
            "area2",
            **{settings.AREA_PARAM: area_value, "from": from_, "to": to, PAGE_PARAM: 1, ROWS_PARAM: rows, **extra},
        )

    def realm(self, realm_value: str, from_: str, to: str, rows: int = 10, **extra) -> ApiResponse:
        """분야별 문화정보 목록 — 파라미터 이름은 settings.REALM_PARAM"""
        return self.get(
            "realm2",
            **{settings.REALM_PARAM: realm_value, "from": from_, "to": to, PAGE_PARAM: 1, ROWS_PARAM: rows, **extra},
        )

    def detail(self, seq: str | int) -> ApiResponse:
        """문화정보 상세"""
        return self.get("detail2", seq=seq)

    def calendar(self, **params) -> ApiResponse:
        """문화캘린더 목록 — 파라미터는 미리보기 화면으로 확인 필요"""
        return self.get("livelihood2", **params)
