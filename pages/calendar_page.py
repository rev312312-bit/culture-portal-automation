"""즐겨요 문화정보 > 문화캘린더 (팀 TC FN_INFO_027~033)"""
from __future__ import annotations

import re

from config.settings import PAGES
from pages.base_page import BasePage

_YM = re.compile(r"(\d{4})\s*[.년\-/]\s*(\d{1,2})")


class CalendarPage(BasePage):
    PATH = PAGES["calendar"]

    # ── 로케이터 (확인 필요) ────────────────────────────────────────────────
    @property
    def title(self):
        # '2026.10' 또는 '2026년 10월' 처럼 연월이 보이는 제목 영역
        return self.page.get_by_text(_YM).first

    @property
    def prev_button(self):
        return self.page.get_by_role("button", name=re.compile(r"이전\s*달|이전|<")).first

    @property
    def next_button(self):
        return self.page.get_by_role("button", name=re.compile(r"다음\s*달|다음|>")).first

    # ── 동작 ─────────────────────────────────────────────────────────────────
    def year_month(self) -> tuple[int, int]:
        text = self.title.inner_text()
        m = _YM.search(text)
        if not m:
            raise ValueError(f"캘린더 제목에서 연월을 찾지 못함: {text!r}")
        return int(m.group(1)), int(m.group(2))

    def _move(self, button) -> None:
        before = self.year_month()
        button.click()
        for _ in range(20):  # 최대 약 5초 동안 연월이 바뀌기를 기다림
            self.page.wait_for_timeout(250)
            if self.year_month() != before:
                return

    def go_prev(self) -> None:
        self._move(self.prev_button)

    def go_next(self) -> None:
        self._move(self.next_button)
