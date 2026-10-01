"""features/info_search.feature 의 단계(step) 구현"""
import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from pages.info_search_page import InfoSearchPage

scenarios("info_search.feature")


@pytest.fixture
def ctx() -> dict:
    """한 시나리오 안에서 단계끼리 값을 주고받는 공간"""
    return {}


@given("한눈에 보는 문화정보 화면에 접속함", target_fixture="info_page")
def open_info_page(page):
    return InfoSearchPage(page).open()


@given("상세검색을 열고 필터를 3개 선택함")
def open_detail_and_check(info_page):
    info_page.toggle_detail()
    info_page.check_filters(3)
    assert info_page.checked_filter_count() >= 1, "사전조건 실패: 필터를 선택하지 못함"


@when(parsers.re(r'검색어 "(?P<keyword>.*)" 로 검색함'))
def search(info_page, keyword):
    info_page.search(keyword)


@when("상세검색 버튼을 클릭함")
def click_detail_toggle(info_page, ctx):
    label = info_page.detail_toggle_label()
    ctx.setdefault("first_label", label)
    ctx["before"] = label
    info_page.toggle_detail()
    info_page.page.wait_for_timeout(300)


@when("전체해제 버튼을 클릭함")
def click_reset_all(info_page):
    info_page.reset_all_button.click()


@then(parsers.parse('"{message}" 안내 메시지가 노출됨'))
def message_is_shown(info_page, message):
    assert info_page.message_shown(message), (
        f"'{message}' 안내 메시지 미노출 (알림창 기록: {info_page.dialog_messages})"
    )


@then("안내 메시지 없이 검색 결과가 1건 이상 노출됨")
def results_are_shown(info_page):
    assert not info_page.dialog_messages, f"예상하지 못한 알림창: {info_page.dialog_messages}"
    assert info_page.result_count() >= 1, "검색 결과가 0건임"


@then("상세검색 버튼 문구가 바뀜")
def toggle_label_changed(info_page, ctx):
    assert info_page.detail_toggle_label() != ctx["before"], "버튼 문구가 바뀌지 않음"


@then("상세검색 버튼 문구가 처음과 같아짐")
def toggle_label_restored(info_page, ctx):
    assert info_page.detail_toggle_label() == ctx["first_label"]


@then("선택된 필터가 0개임")
def no_filter_checked(info_page):
    assert info_page.checked_filter_count() == 0
