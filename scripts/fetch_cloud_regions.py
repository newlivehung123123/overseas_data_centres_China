#!/usr/bin/env python3
"""Download the region pages of Chinese cloud providers and write the regions outside mainland China.

Each provider publishes its regions on a page in a fixed format, and the script reads the regions
from the page itself, so that every row carries the passage of the page that supports it. Each
page is saved in data/raw/pages with its text and the time of download. Regions that the provider
pages do not list, such as announced regions, come from config/cloud_regions_manual.csv, and the
script downloads the page that each of those rows cites and checks that the row's city or country
is on the page.

    python scripts/fetch_cloud_regions.py              writes data/cloud_regions.csv
    python scripts/fetch_cloud_regions.py --offline    reads the saved pages instead of downloading
"""

from __future__ import annotations

import argparse
import csv
import html
import io
import json
import os
import re
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "data" / "raw" / "pages"
MANUAL_CSV = ROOT / "config" / "cloud_regions_manual.csv"
OUT_CSV = ROOT / "data" / "cloud_regions.csv"

USER_AGENT = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/128.0.0.0 Safari/537.36")
TIMEOUT = 30
QUOTE_CONTEXT = 40  # characters kept after a match in the passage

SOURCES = {
    "alibaba": ("Alibaba Cloud", "https://www.alibabacloud.com/en/global-locations?_p_lc=1"),
    "huawei_faq": ("Huawei Cloud", "https://support.huaweicloud.com/intl/en-us/intl_faq/en-us_topic_0115884695.html"),
    "huawei_cc": ("Huawei Cloud", "https://support.huaweicloud.com/intl/en-us/productdesc-cc/cc_01_0003.html"),
    "tencent": ("Tencent Cloud", "https://intl.cloud.tencent.com/document/product/213/6091"),
    "byteplus": ("BytePlus", "https://docs.byteplus.com/api/docs/bytehouse/docs-supported-regions-and-providers"),
}

# City or region label as the pages write it, mapped to city, country and ISO 3166-1 alpha-3 code.
PLACES = {
    "singapore": ("Singapore", "Singapore", "SGP"),
    "bangkok": ("Bangkok", "Thailand", "THA"),
    "kuala lumpur": ("Kuala Lumpur", "Malaysia", "MYS"),
    "johor": ("Johor", "Malaysia", "MYS"),
    "johor bahru": ("Johor Bahru", "Malaysia", "MYS"),
    "jakarta": ("Jakarta", "Indonesia", "IDN"),
    "manila": ("Manila", "Philippines", "PHL"),
    "tokyo": ("Tokyo", "Japan", "JPN"),
    "osaka": ("Osaka", "Japan", "JPN"),
    "seoul": ("Seoul", "South Korea", "KOR"),
    "virginia": ("Virginia", "United States", "USA"),
    "silicon valley": ("Silicon Valley", "United States", "USA"),
    "queretaro": ("Queretaro", "Mexico", "MEX"),
    "mexico city": ("Mexico City", "Mexico", "MEX"),
    "frankfurt": ("Frankfurt", "Germany", "DEU"),
    "london": ("London", "United Kingdom", "GBR"),
    "paris": ("Paris", "France", "FRA"),
    "dublin": ("Dublin", "Ireland", "IRL"),
    "dubai": ("Dubai", "United Arab Emirates", "ARE"),
    "riyadh": ("Riyadh", "Saudi Arabia", "SAU"),
    "saudi arabia": ("Riyadh", "Saudi Arabia", "SAU"),
    "cairo": ("Cairo", "Egypt", "EGY"),
    "johannesburg": ("Johannesburg", "South Africa", "ZAF"),
    "istanbul": ("Istanbul", "Turkey", "TUR"),
    "sao paulo": ("Sao Paulo", "Brazil", "BRA"),
    "santiago": ("Santiago", "Chile", "CHL"),
    "buenos aires": ("Buenos Aires", "Argentina", "ARG"),
    "lima": ("Lima", "Peru", "PER"),
    "hong kong": ("Hong Kong", "Hong Kong", "HKG"),
}
# Tencent region IDs in mainland China, and its finance-only regions, which are left out.
TENCENT_MAINLAND = re.compile(r"^ap-(beijing|shanghai|nanjing|guangzhou|chengdu|chongqing|zhongwei|shenzhen)|-fsi")

FIELDS = ["provider", "region_label", "region_id", "city", "country", "country_iso3", "status", "launch_year",
          "availability_zones", "hong_kong_macau", "source_url", "source_quote", "check_status", "retrieved"]


def fold(text: str) -> str:
    """Lower case without accents, so that São Paulo and Sao Paulo match."""
    text = unicodedata.normalize("NFKD", text)
    return "".join(c for c in text if not unicodedata.combining(c)).lower()


def page_text(raw: str) -> str:
    raw = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S | re.I)
    text = html.unescape(re.sub(r"<[^>]+>", " ", raw)).replace("﻿", " ")
    return re.sub(r"\s+", " ", text).strip()


def user_agent(url: str) -> str:
    """The SEC accepts automated requests only with a contact email, read from SEC_CONTACT_EMAIL."""
    if urllib.parse.urlparse(url).hostname in ("www.sec.gov", "sec.gov"):
        email = os.environ.get("SEC_CONTACT_EMAIL", "").strip()
        if not email:
            raise OSError("set SEC_CONTACT_EMAIL to a contact email before reading pages on sec.gov")
        return f"overseas_data_centres_china research {email}"
    return USER_AGENT


def pdf_text(raw: bytes) -> str:
    """Text of every page of a PDF, such as an annual report."""
    import pypdf
    return " ".join(page.extract_text() or "" for page in pypdf.PdfReader(io.BytesIO(raw)).pages)


def download(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": user_agent(url), "Accept-Language": "en"})
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        raw = response.read()
    if raw.startswith(b"%PDF"):
        return pdf_text(raw)
    return raw.decode("utf-8", errors="replace")


def load_page(key: str, url: str, offline: bool) -> tuple[str, str] | None:
    """Return the text of a page and the time of download, saving the page on the first download."""
    PAGES.mkdir(parents=True, exist_ok=True)
    saved = PAGES / f"{key}.json"
    if offline:
        if not saved.exists():
            return None
        data = json.loads(saved.read_text())
        return data["text"], data["retrieved"]
    try:
        raw = download(url)
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        print(f"  could not read {url}: {error}", file=sys.stderr)
        return None
    retrieved = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    text = page_text(raw)
    saved.write_text(json.dumps({"url": url, "retrieved": retrieved, "text": text}, ensure_ascii=False))
    return text, retrieved


def quote(text: str, start: int, end: int) -> str:
    """The matched text and the characters after it, which begin where the entry begins."""
    return text[start:min(len(text), end + QUOTE_CONTEXT)].strip()


def place(label: str) -> tuple[str, str, str] | None:
    return PLACES.get(fold(label).strip())


def row(provider, label, region_id, where, url, passage, retrieved, zones="", year="", status="operational"):
    city, country, iso3 = where
    return {"provider": provider, "region_label": label, "region_id": region_id, "city": city, "country": country,
            "country_iso3": iso3, "status": status, "launch_year": year, "availability_zones": zones,
            "hong_kong_macau": "yes" if iso3 in ("HKG", "MAC") else "no", "source_url": url,
            "source_quote": passage, "check_status": "found", "retrieved": retrieved}


def parse_alibaba(text, provider, url, retrieved):
    rows = []
    for m in re.finditer(r"([A-Z][A-Za-z]*(?: [A-Z][a-z]+)*(?: \(([^)]+)\))?) Availability Zone: (\d+) Released in (\d{4})",
                         text):
        label, inner, zones, year = m.group(1), m.group(2), m.group(3), m.group(4)
        if label.startswith("China (") and inner != "Hong Kong":
            continue
        city = (inner or label).split(" - ")[0]
        where = place(city)
        if where is None:
            print(f"  Alibaba Cloud: no place for {label!r}", file=sys.stderr)
            continue
        status = "operational"
        rows.append(row(provider, label, "", where, url, m.group(0), retrieved, zones, year, status))
    return rows


def parse_huawei_faq(text, provider, url, retrieved):
    m = re.search(r"CN North-Beijing,.*?LA-Lima\.", text)
    if not m:
        return []
    rows = []
    for code in re.split(r",\s*(?:and\s+)?", m.group(0).rstrip(".")):
        code = code.strip()
        if code.startswith("CN ") or (code.startswith("CN-") and code != "CN-Hong Kong"):
            continue
        where = place(code.split("-", 1)[1])
        if where is None:
            print(f"  Huawei Cloud: no place for {code!r}", file=sys.stderr)
            continue
        i = text.find(code, m.start())
        rows.append(row(provider, code, code, where, url, quote(text, i, i + len(code)), retrieved))
    return rows


def parse_huawei_cc(text, provider, url, retrieved):
    rows = []
    for m in re.finditer(r"\bEU-([A-Z][a-z]+)\d?", text):
        where = place(m.group(1))
        if where:
            rows.append(row(provider, m.group(0), m.group(0), where, url, quote(text, m.start(), m.end()), retrieved))
    return rows


def parse_tencent(text, provider, url, retrieved):
    rows = []
    for m in re.finditer(r"\b((?:ap|na|sa|eu|me)-[a-z]+(?:-[a-z]+)*) (\d+) ", text):
        region_id, zones = m.group(1), m.group(2)
        if TENCENT_MAINLAND.search(region_id):
            continue
        start = max(0, m.start() - 160)
        before = text[start:m.start()]
        labels = list(re.finditer(r"\(([^()]+)\)", before))
        label = labels[-1].group(1) if labels else ""
        entry = start + labels[-1].start() if labels else m.start()
        if region_id == "ap-singapore":
            label = "Singapore"
        if region_id == "ap-hongkong":
            label = "Hong Kong"
        where = place(label)
        if where is None:
            print(f"  Tencent Cloud: no place for {region_id} ({label!r})", file=sys.stderr)
            continue
        rows.append(row(provider, label, region_id, where, url, text[entry:m.end()].strip(), retrieved, zones))
    return rows


def parse_byteplus(text, provider, url, retrieved):
    rows = []
    for m in re.finditer(r"(Hong Kong|Southeast Asia \((Johor|Jakarta)\)) \d+\.\d+\.\d+\.\d+", text):
        label = m.group(1)
        where = place(m.group(2) or label)
        rows.append(row(provider, label, "", where, url, quote(text, m.start(), m.end()), retrieved))
    return rows


PARSERS = {"alibaba": parse_alibaba, "huawei_faq": parse_huawei_faq, "huawei_cc": parse_huawei_cc,
           "tencent": parse_tencent, "byteplus": parse_byteplus}


def manual_rows(offline: bool, seen: set[tuple[str, str]]) -> list[dict]:
    """Rows from secondary sources, each checked against its own page when the page can be read."""
    rows = []
    with MANUAL_CSV.open(newline="") as f:
        for i, entry in enumerate(csv.DictReader(f)):
            if (entry["provider"], entry["city"]) in seen and entry["city"]:
                continue
            page = load_page(f"manual_{i}", entry["source_url"], offline)
            out = {field: entry.get(field, "") for field in FIELDS}
            out["hong_kong_macau"] = "yes" if entry["country_iso3"] in ("HKG", "MAC") else "no"
            if page is None:
                out["check_status"], out["retrieved"] = "not_read", ""
            else:
                text, out["retrieved"] = page
                term = entry["city"] or entry["country"]
                j = fold(text).find(fold(term))
                out["check_status"] = "found" if j >= 0 else "not_found"
                out["source_quote"] = quote(text, j, j + len(term)) if j >= 0 else ""
            rows.append(out)
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--offline", action="store_true", help="read the saved pages instead of downloading")
    args = parser.parse_args()

    rows = []
    for key, (provider, url) in SOURCES.items():
        page = load_page(key, url, args.offline)
        if page is None:
            print(f"{provider}: page not read, {url}")
            continue
        found = PARSERS[key](page[0], provider, url, page[1])
        print(f"{provider}: {len(found)} regions from {url}")
        rows.extend(found)
    unique, seen = [], set()
    for r in rows:
        key = (r["provider"], r["city"])
        if key not in seen:
            seen.add(key)
            unique.append(r)
    unique.extend(manual_rows(args.offline, seen))
    unique.sort(key=lambda r: (r["provider"], r["status"], r["country"], r["city"]))
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(unique)
    outside = [r for r in unique if r["status"] == "operational" and r["hong_kong_macau"] == "no"]
    print(f"Wrote {len(unique)} rows to {OUT_CSV.relative_to(ROOT)}; {len(outside)} operational outside mainland "
          f"China, Hong Kong and Macau, in {len({r['country_iso3'] for r in outside})} countries")


if __name__ == "__main__":
    main()
