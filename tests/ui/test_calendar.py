"""features/calendar.feature 의 단계(step) 구현"""
import pytest
from pytest_bdd import given, scenarios, then, when

from pages.calendar_page import CalendarPage

scenarios("calendar.feature")


def shift_month(year: int, month: int, delta: int) -> tuple[int, int]:
    index = year * 12 + (month - 1) + delta
    return index // 12, index % 12 + 1


@pytest.fixture
def ctx() -> dict:
    return {}


@given("문화캘린더 화면에 접속함", target_fixture="calendar_page")
def open_calendar(page):
    return CalendarPage(page).open()


@when("이전 달 버튼을 클릭함")
def click_prev(calendar_page, ctx):
    ctx["before"] = calendar_page.year_month()
    calendar_page.go_prev()


@when("다음 달 버튼을 클릭함")
def click_next(calendar_page, ctx):
    ctx["before"] = calendar_page.year_month()
    calendar_page.go_next()


@then("캘린더 제목에 오늘의 연월이 표시됨")
def shows_this_month(calendar_page, today):
    assert calendar_page.year_month() == (today.year, today.month)


@then("캘린더 제목이 한 달 전 연월로 바뀜")
def moved_back(calendar_page, ctx):
    assert calendar_page.year_month() == shift_month(*ctx["before"], -1)


@then("캘린더 제목이 한 달 뒤 연월로 바뀜")
def moved_forward(calendar_page, ctx):
    assert calendar_page.year_month() == shift_month(*ctx["before"], +1)
