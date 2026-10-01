"""기간별 문화정보 목록 (period2)"""
import pytest

from tests.api.helpers import overlaps


@pytest.mark.smoke
def test_API_기간_정상_001_이번달_목록_조회(api, month_range):
    res = api.period(*month_range, rows=10)
    assert res.status_code == 200, res.summary()
    assert res.result_code == "00", res.summary()
    assert len(res.items) >= 1, f"이번 달 문화정보가 0건임: {res.summary()}"


@pytest.mark.regression
def test_API_기간_정상_002_조회기간과_항목기간_일치(api, month_range):
    res = api.period(*month_range, rows=50)
    assert res.ok, res.summary()
    outside = [i for i in res.items if not overlaps(i, *month_range)]
    assert not outside, f"조회 기간을 벗어난 항목 {len(outside)}건: {[o.get('seq') for o in outside][:10]}"


@pytest.mark.regression
def test_API_기간_경계값_001_시작일이_종료일보다_늦음(api, month_range):
    start, end = month_range
    res = api.period(from_=end, to=start)
    assert not (res.ok and res.items), (
        f"시작일 > 종료일인데 목록이 정상 반환됨(오류 처리 없음): {res.summary()}"
    )


@pytest.mark.regression
def test_API_기간_경계값_002_하루짜리_기간(api, today):
    day = f"{today:%Y%m%d}"
    res = api.period(from_=day, to=day, rows=50)
    assert res.ok, res.summary()
    outside = [i for i in res.items if not overlaps(i, day, day)]
    assert not outside, f"해당 일자를 포함하지 않는 항목: {[o.get('seq') for o in outside][:10]}"


@pytest.mark.regression
def test_API_기간_형식_001_하이픈_날짜형식(api, today):
    res = api.period(from_=f"{today:%Y-%m}-01", to=f"{today:%Y%m}28")
    assert not (res.ok and res.items), f"잘못된 날짜 형식인데 목록이 반환됨: {res.summary()}"


@pytest.mark.regression
def test_API_기간_탐색_001_과거기간_2019년(api, record_property):
    res = api.period(from_="20190616", to="20191231", rows=10)
    record_property("totalCount", res.total_count)  # 리포트에 건수 기록 (관찰사항 OBS-003)
    assert res.ok, res.summary()


@pytest.mark.regression
def test_API_기간_페이징_001_한페이지_결과수(api, month_range):
    res = api.period(*month_range, rows=5)
    assert res.ok, res.summary()
    assert len(res.items) <= 5
    assert res.num_of_rows == 5, f"numOfrows 값: {res.num_of_rows}"


@pytest.mark.regression
def test_API_기간_페이징_002_페이지간_중복없음(api, month_range):
    first = api.period(*month_range, page=1, rows=10)
    second = api.period(*month_range, page=2, rows=10)
    assert first.ok and second.ok, f"{first.summary()} | {second.summary()}"
    if (first.total_count or 0) <= 10:
        pytest.skip("결과가 10건 이하라 2페이지가 없음")
    dup = {i["seq"] for i in first.items} & {i["seq"] for i in second.items}
    assert not dup, f"1·2페이지에 중복된 seq: {dup}"
