"""
모든 화면(Page Object)의 공통 기능.

로케이터(화면 요소를 찾는 규칙)는 각 화면 클래스 맨 위에 모아 둠.
화면이 바뀌면 테스트 코드는 그대로 두고 그 부분만 고치면 됨.
"""
from __future__ import annotations

import re
import time

from playwright.sync_api import Page


def _squash(text: str) -> str:
    """공백·마침표 차이로 메시지 비교가 깨지지 않게 정리함."""
    return re.sub(r"[\s.'\"]", "", text or "")


class BasePage:
    PATH = "/"

    def __init__(self, page: Page):
        self.page = page
        self.dialog_messages: list[str] = []
        page.on("dialog", self._on_dialog)

    # 알림창(alert/confirm)은 메시지를 기록한 뒤 닫음
    def _on_dialog(self, dialog) -> None:
        self.dialog_messages.append(dialog.message)
        try:
            dialog.dismiss()
        except Exception:  # 다른 핸들러가 이미 닫은 경우
            pass

    def open(self, path: str | None = None) -> "BasePage":
        self.page.goto(path or self.PATH, wait_until="domcontentloaded")
        return self

    def message_shown(self, text: str, timeout_ms: int = 5000) -> bool:
        """알림창 또는 화면 문구로 text 가 노출되는지 timeout 동안 확인함."""
        target = _squash(text)
        deadline = time.monotonic() + timeout_ms / 1000
        while time.monotonic() < deadline:
            if any(target in _squash(m) for m in self.dialog_messages):
                return True
            if target and target in _squash(self.page.inner_text("body")):
                return True
            self.page.wait_for_timeout(250)
        return False

    def has_horizontal_scroll(self) -> bool:
        return self.page.evaluate(
            "() => document.documentElement.scrollWidth > window.innerWidth + 1"
        )
