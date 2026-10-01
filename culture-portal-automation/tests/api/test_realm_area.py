"""분야별(realm2)·지역별(area2) 목록 — 동등분할"""
import pytest

from tests.api.helpers import DATA

REALM_NAMES = [r["name"] for r in DATA["realms"]]


@pytest.mark.regression
@pytest.mark.tc("FN_INFO_007")
def test_API_분야_값검증_001_분야명이_정의된_12개_중_하나(api, month_range):
    """요청 파라미터 없이 확인 가능: 목록의 realmName 이 12개 분야(동등분할 클래스) 안에 있는지"""
    res = api.period(*month_range, rows=100)
    assert res.ok, res.summary()
    unknown = sorted({i.get("realmName") for i in res.items} - set(REALM_NAMES))
    assert not unknown, f"정의되지 않은 분야명: {unknown}"


@pytest.mark.regression
@pytest.mark.tc("FN_INFO_007")
@pytest.mark.parametrize("realm", DATA["realms"], ids=lambda r: r["name"])
def test_API_분야_동등분할_001_분야별_목록_조회(api, month_range, realm):
    if not realm["code"]:
        pytest.skip("data/test_data.json 에 분야 코드를 채운 뒤 실행")
    res = api.realm(realm["code"], *month_range, rows=30)
    assert res.ok, res.summary()
    wrong = [i.get("realmName") for i in res.items if i.get("realmName") != realm["name"]]
    assert not wrong, f"요청 분야({realm['name']})와 다른 항목: {wrong[:10]}"


@pytest.mark.regression
@pytest.mark.parametrize("area", DATA["areas"])
def test_API_지역_정상_001_지역별_목록_조회(api, month_range, area):
    res = api.area(area, *month_range, rows=30)
    assert res.ok, res.summary()
    wrong = [i.get("area") for i in res.items if area not in i.get("area", "")]
    assert not wrong, f"요청 지역({area})과 다른 항목: {wrong[:10]}"
