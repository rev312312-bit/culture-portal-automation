"""즐겨요 문화정보 > 내 주변 문화콘텐츠 (팀 TC FN_INFO_013~019)"""
from __future__ import annotations

import re

from config.settings import PAGES
from pages.base_page import BasePage


class NearbyPage(BasePage):
    PATH = PAGES["nearby"]

    # ── 로케이터 (확인 필요) ────────────────────────────────────────────────
    @property
    def current_location_button(self):
        return self.page.get_by_role("button", name=re.compile(r"현재\s*(내\s*)?위치")).first

    def radius_option(self, km: int):
        return self.page.get_by_text(re.compile(rf"^\s*{km}\s*km\s*$", re.I)).first

    @property
    def result_items(self):
        return self.page.locator("ul[class*='list' i] > li, div[class*='list' i] li")

    # ── 동작 ─────────────────────────────────────────────────────────────────
    def click_current_location(self) -> None:
        self.current_location_button.click()
        self.page.wait_for_load_state("networkidle")

    def select_radius(self, km: int) -> None:
        self.radius_option(km).click()
        self.page.wait_for_load_state("networkidle")

    def result_count(self) -> int:
        return self.result_items.count()

    def result_texts(self, limit: int = 20) -> list[str]:
        items = self.result_items
        return [items.nth(i).inner_text() for i in range(min(limit, items.count()))]
