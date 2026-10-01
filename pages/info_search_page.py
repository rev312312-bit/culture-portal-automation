"""즐겨요 문화정보 > 한눈에 보는 문화정보 (팀 TC FN_INFO_001~012)"""
from __future__ import annotations

import re

from config.settings import PAGES
from pages.base_page import BasePage


class InfoSearchPage(BasePage):
    PATH = PAGES["info_list"]

    # ── 로케이터 (확인 필요: 실제 화면에서 한 번 확인 후 고칠 것) ──────────────
    @property
    def search_input(self):
        return self.page.locator(
            "input[type='search'], input[name*='keyword' i], input[id*='keyword' i], "
            "input[title*='검색']"
        ).first

    @property
    def search_button(self):
        return self.page.get_by_role("button", name="검색", exact=True).first

    @property
    def detail_toggle(self):
        return self.page.get_by_role("button", name=re.compile(r"상세\s*검색\s*(열기|닫기)")).first

    @property
    def reset_all_button(self):
        return self.page.get_by_role("button", name=re.compile(r"전체\s*해제")).first

    @property
    def filter_checkboxes(self):
        # 상세검색 패널 안의 체크박스
        return self.page.locator("input[type='checkbox']")

    @property
    def result_items(self):
        # 검색 결과 목록의 항목 하나하나
        return self.page.locator("ul[class*='list' i] > li, div[class*='list' i] li")

    # ── 동작 ─────────────────────────────────────────────────────────────────
    def search(self, keyword: str) -> None:
        self.search_input.fill(keyword)
        self.search_button.click()
        self.page.wait_for_load_state("domcontentloaded")

    def toggle_detail(self) -> None:
        self.detail_toggle.click()

    def detail_toggle_label(self) -> str:
        return (self.detail_toggle.inner_text() or "").strip()

    def check_filters(self, count: int = 3) -> None:
        boxes = self.filter_checkboxes
        for i in range(min(count, boxes.count())):
            boxes.nth(i).check(force=True)

    def checked_filter_count(self) -> int:
        boxes = self.filter_checkboxes
        return sum(1 for i in range(boxes.count()) if boxes.nth(i).is_checked())

    def result_count(self) -> int:
        self.page.wait_for_load_state("networkidle")
        return self.result_items.count()
