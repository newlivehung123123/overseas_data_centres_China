#!/usr/bin/env python3
"""Write the list of facilities that Baxtel names in a market as the first columns of a new census file.

A census records every data-centre facility that Baxtel's public list names in a market. This script downloads the
list of one market, such as https://baxtel.com/data-center/sao-paulo, and writes one row for each facility with the
name, the operator, the status, the page of the facility and the passage of the list that names it, which
scripts/check_sources.py checks in the same way as every other passage. The coding of each facility, in the columns
chinese_link, site_id, note and the second passage, is left empty for a person to write after the page scan and the
web searches of the market. Where Baxtel withholds the name of a facility and shows an invented one, the name is left
empty and the passage starts at the words "Interested in this information? Contact us", as rule 9 of CONTRIBUTING.md
requires. The script refuses to overwrite a census file that exists.

    python scripts/list_census_facilities.py sao-paulo "Greater São Paulo"
"""

from __future__ import annotations

import argparse
import csv
import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fetch_cloud_regions as fcr  # noqa: E402

ROOT = fcr.ROOT
BASE = "https://baxtel.com/data-center/"
HIDDEN = "Interested in this information? Contact us"
COLUMNS = ["market", "facility", "operator", "baxtel_status", "baxtel_page", "chinese_link", "site_id", "note",
           "evidence", "source_url", "source_quote", "link_source_url", "link_source_quote", "link_evidence"]


def cells(row: str) -> list[tuple[str, str]]:
    """Text and link of each cell of a row of the list."""
    out = []
    for cell in re.findall(r"<td[^>]*>(.*?)</td>", row, re.S):
        link = re.search(r'href="(/data-centers?/[^"]+)"', cell)
        text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", cell))).strip()
        out.append((text, link.group(1) if link else ""))
    return out


def facilities(page: str) -> list[dict]:
    """One row for each facility of the list, in the order of the page."""
    rows = []
    for row in re.findall(r'<tr class="border-b[^"]*flex">(.*?)</tr>', page, re.S):
        c = cells(row)
        if len(c) < 6 or not c[1][1].startswith("/data-center/"):
            continue
        name, operator, size, status, kind = c[1][0], c[2][0], c[3][0], c[4][0], c[5][0]
        shown = HIDDEN if HIDDEN in name else name
        rows.append({"facility": "" if HIDDEN in name else name, "operator": operator, "baxtel_status": status,
                     "baxtel_page": "https://baxtel.com" + c[1][1],
                     "source_quote": " ".join(x for x in (shown, operator, size, status, kind) if x)})
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("slug", help="Baxtel's name of the market, such as sao-paulo")
    parser.add_argument("market", help="name of the market in the census, such as Greater São Paulo")
    args = parser.parse_args()
    out = ROOT / "config" / f"{args.slug.replace('-', '_')}_census.csv"
    if out.exists():
        raise SystemExit(f"{out.relative_to(ROOT)} exists; the script does not overwrite a census")
    url = BASE + args.slug
    rows = facilities(fcr.download(url))
    with out.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        for r in rows:
            writer.writerow({**{k: "" for k in COLUMNS}, **r, "market": args.market, "evidence": "secondary",
                             "source_url": url})
    print(f"{len(rows)} facilities of {args.market} written to {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
