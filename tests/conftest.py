"""
모든 테스트가 같이 쓰는 설정(fixture)과 BDD 태그 처리.
"""
from __future__ import annotations

import calendar
from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

from config import settings
from utils.api_client import CultureApiClient

KST = ZoneInfo("Asia/Seoul")


# ── BDD 태그 → pytest 마커 ──────────────────────────────────────────────────
def pytest_bdd_apply_tag(tag, function):
    """
    @tc_FN_INFO_001     → tc("FN_INFO_001") 마커 (추적성)
    @defect_INFO_DF_001 → known_defect 마커 + xfail(strict)
        결함이 남아 있으면 '예상된 실패(XFAIL)'로 통과 처리됨.
        결함이 고쳐지면 XPASS(strict) 로 실패가 떠서 시나리오를 갱신하라고 알려 줌.
        raises=AssertionError: 기대결과 확인(Then) 단계의 실패만 결함으로 인정하고,
        화면 요소를 못 찾는 등의 다른 오류는 진짜 실패로 보고함.
    """
    if tag.startswith("tc_"):
        pytest.mark.tc(tag[len("tc_"):])(function)
        return True
    if tag.startswith("defect_"):
        defect_id = tag[len("defect_"):]
        pytest.mark.known_defect(defect_id)(function)
        pytest.mark.xfail(
            reason=f"알려진 결함 {defect_id}", raises=AssertionError, strict=True
        )(function)
        return True
    return None  # smoke / regression 은 기본 처리(같은 이름의 마커)


def pytest_collection_modifyitems(items):
    """폴더 위치로 api / ui 마커를 자동으로 붙임 (-m api, -m ui 로 골라 실행)."""
    for item in items:
        path = str(item.path)
        if "/tests/api/" in path or "\\tests\\api\\" in path:
            item.add_marker(pytest.mark.api)
        elif "/tests/ui/" in path or "\\tests\\ui\\" in path:
            item.add_marker(pytest.mark.ui)


# ── Playwright 브라우저 설정 ────────────────────────────────────────────────
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "locale": "ko-KR",
        "timezone_id": "Asia/Seoul",
        "viewport": {"width": 1440, "height": 900},
    }


# ── API 공통 ────────────────────────────────────────────────────────────────
@pytest.fixture(scope="session")
def api() -> CultureApiClient:
    if not settings.SERVICE_KEY:
        pytest.skip(".env 파일(또는 GitHub Secrets)에 SERVICE_KEY 가 없어 API 테스트를 건너뜀")
    return CultureApiClient()


@pytest.fixture(scope="session")
def today() -> datetime:
    return datetime.now(KST)


@pytest.fixture(scope="session")
def month_range(today) -> tuple[str, str]:
    """이번 달 1일 ~ 말일 (YYYYMMDD, YYYYMMDD)"""
    last = calendar.monthrange(today.year, today.month)[1]
    return f"{today:%Y%m}01", f"{today:%Y%m}{last:02d}"


@pytest.fixture(scope="session")
def sample_item(api, month_range) -> dict:
    """이번 달 목록의 첫 항목 — 상세 조회 등 다른 테스트의 입력값으로 씀."""
    res = api.period(*month_range, rows=10)
    if not res.items:
        pytest.skip(f"이번 달 목록이 비어 있어 건너뜀: {res.summary()}")
    return res.items[0]
