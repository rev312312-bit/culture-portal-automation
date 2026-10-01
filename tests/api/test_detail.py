"""문화정보 상세 (detail2)"""
import pytest


@pytest.mark.smoke
@pytest.mark.tc("FN_INFO_021")
def test_API_상세_정상_001_목록과_상세정보_일치(api, sample_item):
    res = api.detail(sample_item["seq"])
    assert res.ok, res.summary()
    assert res.items, f"상세 항목이 없음: {res.summary()}"
    detail = res.items[0]
    for key in ["title", "place", "startDate", "endDate"]:
        if key in detail:
            assert detail[key] == sample_item[key], f"{key} 불일치: 목록={sample_item[key]!r}, 상세={detail[key]!r}"
    assert "title" in detail, "상세 응답에 title 필드가 없음"


@pytest.mark.regression
def test_API_상세_예외_001_존재하지_않는_일련번호(api):
    res = api.detail(0)
    assert res.status_code < 500, f"서버 오류 발생: {res.summary()}"
    assert not res.items, f"존재하지 않는 seq 인데 항목이 반환됨: {res.summary()}"
