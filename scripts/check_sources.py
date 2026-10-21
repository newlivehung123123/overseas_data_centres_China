#!/usr/bin/env python3
"""Download the page behind each site and each role and check that its passage is on that page.

A person writes each site in config/sites.csv and each role of a firm at a site in
config/site_roles.csv, with the page that supports the row and a passage copied from the page. The
check downloads every page once, saves its text in data/raw/pages/sources, and looks for the
passage on the page. A passage counts as found when at least 90 percent of its overlapping pieces
of eight characters appear on the page, with spacing, punctuation, accents and case ignored, and as
partly found from 50 percent. The check writes data/sites.csv and data/site_roles.csv with the
result for each row, and checks config/operator_markets.csv, config/firm_links.csv and
config/rules.csv in the same way. Pages on sec.gov need a contact email in SEC_CONTACT_EMAIL.

    python scripts/check_sources.py              downloads pages not saved yet
    python scripts/check_sources.py --refetch    downloads every page again
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fetch_cloud_regions as fcr  # noqa: E402

ROOT = fcr.ROOT
PAGES = ROOT / "data" / "raw" / "pages" / "sources"
SITES_IN = ROOT / "config" / "sites.csv"
ROLES_IN = ROOT / "config" / "site_roles.csv"
SITES_OUT = ROOT / "data" / "sites.csv"
ROLES_OUT = ROOT / "data" / "site_roles.csv"
# Further tables whose rows each carry a page and a passage, checked in the same way.
OTHER_TABLES = [(ROOT / "config" / "operator_markets.csv", ROOT / "data" / "operator_markets.csv"),
                (ROOT / "config" / "firm_links.csv", ROOT / "data" / "firm_links.csv"),
                (ROOT / "config" / "rules.csv", ROOT / "data" / "rules.csv")]

PIECE = 8          # characters in each piece of a passage looked up on the page
FOUND = 0.9        # share of a passage's pieces that must be on the page for the passage to count as found
PARTLY_FOUND = 0.5
ROLES = {"owner", "operator", "tenant", "user", "builder", "equipment supplier", "financier"}
STATUSES = {"operational", "under_construction", "planned", "unclear"}


def squash(text: str) -> str:
    """Letters and digits only, without accents and in lower case."""
    return "".join(c for c in fcr.fold(text) if c.isalnum())


def share_found(passage: str, page: str) -> float:
    quote, text = squash(passage), squash(page)
    if not quote:
        return 0.0
    if len(quote) <= PIECE:
        return 1.0 if quote in text else 0.0
    pieces = [quote[i:i + PIECE] for i in range(len(quote) - PIECE + 1)]
    return sum(piece in text for piece in pieces) / len(pieces)


def verdict(share: float) -> str:
    if share >= FOUND:
        return "found"
    if share >= PARTLY_FOUND:
        return "partly_found"
    return "not_found"


def page(url: str, refetch: bool) -> tuple[str, str] | None:
    """Text of the page and the date of download, read from the saved copy unless refetch is set."""
    PAGES.mkdir(parents=True, exist_ok=True)
    saved = PAGES / (hashlib.sha1(url.encode()).hexdigest()[:16] + ".json")
    if saved.exists() and not refetch:
        data = json.loads(saved.read_text())
        return data["text"], data["retrieved"]
    try:
        raw = fcr.download(url)
    except Exception as error:  # noqa: BLE001 - any failure leaves the row not read
        print(f"  could not read {url}: {error}", file=sys.stderr)
        return None
    text = fcr.page_text(raw)
    retrieved = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    saved.write_text(json.dumps({"url": url, "retrieved": retrieved, "text": text}, ensure_ascii=False))
    return text, retrieved


def check(rows: list[dict], refetch: bool) -> list[dict]:
    out = []
    for r in rows:
        got = page(r["source_url"], refetch)
        r = dict(r)
        if got is None:
            r.update(check_status="not_read", share_found="", retrieved="")
        else:
            share = share_found(r["source_quote"], got[0])
            r.update(check_status=verdict(share), share_found=f"{share:.2f}", retrieved=got[1])
        out.append(r)
    return out


def validate(sites: list[dict], roles: list[dict]) -> None:
    ids = [s["site_id"] for s in sites]
    problems = [f"duplicate site_id {i}" for i in set(ids) if ids.count(i) > 1]
    problems += [f"{s['site_id']}: unknown status {s['status']!r}" for s in sites if s["status"] not in STATUSES]
    problems += [f"{r['site_id']}: unknown role {r['role']!r}" for r in roles if r["role"] not in ROLES]
    problems += [f"role for unknown site {r['site_id']}" for r in roles if r["site_id"] not in ids]
    if problems:
        raise ValueError("; ".join(problems))


def read(path: Path) -> list[dict]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def write(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--refetch", action="store_true", help="download every page again")
    args = parser.parse_args()

    sites, roles = read(SITES_IN), read(ROLES_IN)
    validate(sites, roles)
    tables = [("sites", sites, SITES_OUT), ("roles", roles, ROLES_OUT)]
    tables += [(src.stem, read(src), out) for src, out in OTHER_TABLES if src.exists()]
    for name, rows, path in tables:
        checked = check(rows, args.refetch)
        write(path, checked)
        counts = {status: sum(r["check_status"] == status for r in checked)
                  for status in ("found", "partly_found", "not_found", "not_read")}
        print(f"{len(checked)} {name} written to {path.relative_to(ROOT)}: {counts}")


if __name__ == "__main__":
    main()
