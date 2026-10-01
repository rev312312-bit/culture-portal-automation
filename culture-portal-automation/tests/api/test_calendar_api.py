"""문화캘린더 목록 (livelihood2) — 2주 차"""
import pytest


@pytest.mark.regression
@pytest.mark.tc("FN_INFO_030")
def test_API_캘린더_정상_001_캘린더_목록_조회(api, month_range):
    # 확인 필요: livelihood2 의 요청 파라미터는 미리보기 화면으로 확인 후 맞출 것
    res = api.calendar(**{"from": month_range[0], "to": month_range[1], "cPage": 1, "rows": 10})
    assert res.ok, res.summary()
