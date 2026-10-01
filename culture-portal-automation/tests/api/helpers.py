import json
from pathlib import Path

DATA = json.loads((Path(__file__).resolve().parents[2] / "data" / "test_data.json").read_text(encoding="utf-8"))

REQUIRED_ITEM_FIELDS = ["seq", "title", "startDate", "endDate", "place", "realmName", "area"]


def overlaps(item: dict, from_: str, to: str) -> bool:
    """항목의 기간(startDate~endDate)이 조회 기간(from~to)과 겹치는지"""
    return item.get("startDate", "") <= to and item.get("endDate", "") >= from_
