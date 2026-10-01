"""인증키 오류 처리"""
import pytest


@pytest.mark.smoke
def test_API_인증_예외_001_인증키_누락(api, month_range):
    res = api.get("period2", include_key=False, **{"from": month_range[0], "to": month_range[1]})
    assert not res.items, f"인증키 없이 목록이 반환됨: {res.summary()}"
    assert not res.ok, f"인증키 없이 정상 응답함: {res.summary()}"


@pytest.mark.regression
def test_API_인증_예외_002_등록되지_않은_인증키(month_range):
    from utils.api_client import CultureApiClient

    res = CultureApiClient(service_key="INVALID_KEY_FOR_TEST").period(*month_range)
    assert not res.items, f"잘못된 인증키로 목록이 반환됨: {res.summary()}"
    assert not res.ok, res.summary()
