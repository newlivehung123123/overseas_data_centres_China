#!/usr/bin/env python3
"""Search the Baxtel page of every facility in the censuses for the names of Chinese firms and places.

A census codes a facility as none_found when no source names a Chinese firm there. This script records one of the two
searches behind that coding: a search of the facility's own page on Baxtel for the firms of Table 2 of the codebook and
for words that point to mainland China or Hong Kong. The search reads only the description of the facility itself, which
ends where the page begins to list nearby sites, so that the description of a neighbour does not count. A term found is
a lead for a person to read and not a coded link, because a page can name a Chinese firm for another reason, such as a
supplier of equipment. The script downloads each page once, at most one request every 1.5 seconds, and keeps the text
in data/raw/pages/sources with the pages of the source check.

    python scripts/scan_census_pages.py    writes data/census_page_scan.csv
"""

from __future__ import annotations

import csv
import hashlib
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_sources as cs  # noqa: E402

ROOT = cs.ROOT
OUT = ROOT / "data" / "census_page_scan.csv"
FIELDS = ["market", "facility", "operator", "baxtel_page", "terms_found", "passage", "retrieved"]
PAUSE = 1.5
CONTEXT = 120      # characters kept on each side of the first term found
START, END = "Clear search Login Get Started -->", "Map and Nearby Locations"
# Firms of Table 2 of the codebook, with the other names under which sources write them.
FIRMS = ["Alibaba", "Aliyun", "Huawei", "Tencent", "ByteDance", "Bytedance", "TikTok", "BytePlus", "Volcano Engine", "Baidu",
         "China Mobile", "China Telecom", "China Unicom", "GDS", "VNET", "21Vianet", "zData", "ZData", "ChinData", "Chindata",
         "DayOne", "Global Switch", "Shagang", "DC-Science", "ZTE", "Inspur", "Sugon", "Huanbang", "INF Tech", "Moonshot",
         "Megaspeed", "Eximbank", "China Development Bank", "China-ASEAN"]
PLACES = ["China", "Chinese", "Beijing", "Shanghai", "Shenzhen", "Hangzhou", "Guangzhou", "Hong Kong"]


def description(text: str) -> str:
    """The part of a Baxtel page that describes the facility itself, before the page lists nearby sites."""
    start = text.find(START)
    start = start + len(START) if start >= 0 else 0
    end = text.find(END, start)
    return text[start:end if end >= 0 else len(text)]


def terms_in(text: str) -> list[tuple[str, int]]:
    """Each term found as a whole word, with the place of its first occurrence, in the order of the lists above."""
    found = []
    for term in FIRMS + PLACES:
        match = re.search(rf"(?<![A-Za-z0-9]){re.escape(term)}(?![A-Za-z0-9])", text)
        if match:
            found.append((term, match.start()))
    return found


def passage(text: str, position: int) -> str:
    return text[max(0, position - CONTEXT):position + CONTEXT].strip()


def scan(rows: list[dict]) -> list[dict]:
    out = []
    for r in rows:
        saved = cs.PAGES / (hashlib.sha1(r["baxtel_page"].encode()).hexdigest()[:16] + ".json")
        fresh = not saved.exists()
        got = cs.page(r["baxtel_page"], False)
        if fresh:
            time.sleep(PAUSE)
        base = {"market": r["market"], "facility": r["facility"], "operator": r["operator"], "baxtel_page": r["baxtel_page"]}
        if got is None:
            out.append({**base, "terms_found": "not_read", "passage": "", "retrieved": ""})
            continue
        own = description(got[0])
        found = terms_in(own)
        # The passage shows a term that the name of the facility or of the operator does not already hold, where there is one.
        named = f"{r['facility']} {r['operator']}"
        fresh_terms = [p for term, p in found if term not in named] or [p for _, p in found]
        out.append({**base, "terms_found": "; ".join(term for term, _ in found),
                    "passage": passage(own, min(fresh_terms)) if found else "", "retrieved": got[1]})
    return out


def main() -> None:
    rows = []
    for src, _ in cs.census_tables():
        rows += cs.read(src)
    result = scan(rows)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(result)
    with_terms = sum(1 for r in result if r["terms_found"] not in ("", "not_read"))
    unread = sum(1 for r in result if r["terms_found"] == "not_read")
    print(f"{len(result)} facility pages scanned, {with_terms} with a term found, {unread} not read; written to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
