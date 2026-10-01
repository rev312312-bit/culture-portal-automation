"""features/nearby.feature 의 단계(step) 구현"""
from pytest_bdd import given, parsers, scenarios, then, when

from pages.nearby_page import NearbyPage

scenarios("nearby.feature")


@given(parsers.parse("브라우저 위치를 {city}(위도 {lat:f}, 경도 {lon:f})으로 허용함"))
def allow_location(context, lat, lon):
    context.grant_permissions(["geolocation"])
    context.set_geolocation({"latitude": lat, "longitude": lon})


@given("브라우저 위치 권한을 허용하지 않음")
def deny_location(context):
    context.clear_permissions()


@given("내 주변 문화콘텐츠 화면에 접속함", target_fixture="nearby_page")
def open_nearby(page):
    return NearbyPage(page).open()


@when("현재위치 버튼을 클릭함")
def click_current_location(nearby_page):
    nearby_page.click_current_location()


@when(parsers.parse("반경 {km:d}km 를 선택함"))
def select_radius(nearby_page, km):
    nearby_page.select_radius(km)


@then("문화콘텐츠 목록이 1건 이상 노출됨")
def list_shown(nearby_page):
    assert nearby_page.result_count() >= 1, "문화콘텐츠 목록이 0건임"


@then("화면 오류 없이 문화콘텐츠 목록이 1건 이상 노출됨")
def list_shown_without_error(nearby_page):
    assert "에러" not in nearby_page.page.title(), f"오류 화면으로 이동함: {nearby_page.page.title()}"
    assert nearby_page.result_count() >= 1, "문화콘텐츠 목록이 0건임"
