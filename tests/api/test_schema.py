"""응답 구조와 데이터 형식"""
import re

import pytest

from tests.api.helpers import DATA, REQUIRED_ITEM_FIELDS

DATE = re.compile(r"^\d{8}$")


@pytest.fixture(scope="module")
def month_list(api, month_range):
    res = api.period(*month_range, rows=50)
    assert res.ok, res.summary()
    return res


@pytest.mark.smoke
def test_API_스키마_정상_001_필수_필드_포함(month_list):
    assert month_list.result_msg is not None, "header/resultMsg 없음"
    assert month_list.total_count is not None, "body/totalCount 없음"
    missing = {
        item.get("seq", "?"): [f for f in REQUIRED_ITEM_FIELDS if f not in item]
        for item in month_list.items
    }
    missing = {k: v for k, v in missing.items() if v}
    assert not missing, f"필수 필드가 빠진 항목: {missing}"


@pytest.mark.regression
def test_API_데이터_형식_001_날짜_8자리와_선후관계(month_list):
    bad = [
        i["seq"] for i in month_list.items
        if not (DATE.match(i.get("startDate", "")) and DATE.match(i.get("endDate", "")))
        or i.get("startDate", "") > i.get("endDate", "")
    ]
    assert not bad, f"날짜 형식 또는 시작일>종료일 오류 seq: {bad}"


@pytest.mark.regression
def test_API_데이터_형식_002_좌표가_국내_범위(month_list):
    (x_min, x_max), (y_min, y_max) = DATA["korea_bounds"]["gpsX"], DATA["korea_bounds"]["gpsY"]
    bad = []
    for i in month_list.items:
        if not i.get("gpsX") or not i.get("gpsY"):
            continue  # 좌표가 없는 항목은 제외
        x, y = float(i["gpsX"]), float(i["gpsY"])
        if not (x_min <= x <= x_max and y_min <= y <= y_max):
            bad.append((i["seq"], x, y))
    assert not bad, f"국내 범위를 벗어난 좌표: {bad}"
