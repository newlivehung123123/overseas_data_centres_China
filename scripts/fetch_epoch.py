#!/usr/bin/env python3
"""Read the estimates of Epoch AI for the sites that its database of AI data centres shares with this dataset.

Epoch AI publishes a database of large AI data centres, with the IT power and the AI compute of each
one estimated from satellite imagery, permits and company documents, under the Creative Commons
Attribution licence. A person matches a site in data/sites.csv to an entry of the database in
config/epoch_links.csv, with the passage of the Epoch page that supports the match, and
scripts/check_sources.py checks that passage. This script downloads the database file, saves it in
data/raw/epoch, and writes data/epoch_estimates.csv with the estimates for each matched site, read
from the file and not typed by hand. It also reads Epoch's timeline file, which dates each stage of
construction from satellite imagery and other evidence, and writes data/epoch_timelines.csv for the
same sites.

    python scripts/fetch_epoch.py              downloads the database files
    python scripts/fetch_epoch.py --offline    reads the saved files instead
"""

from __future__ import annotations

import argparse
import csv
import io
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fetch_cloud_regions as fcr  # noqa: E402

ROOT = fcr.ROOT
EPOCH_URL = "https://epoch.ai/data/data_centers/data_centers.csv"
TIMELINES_URL = "https://epoch.ai/data/data_centers/data_center_timelines.csv"
RAW = ROOT / "data" / "raw" / "epoch"
LINKS = ROOT / "config" / "epoch_links.csv"
OUT = ROOT / "data" / "epoch_estimates.csv"
TIMELINES_OUT = ROOT / "data" / "epoch_timelines.csv"
FIELDS = ["site_id", "epoch_name", "it_power_mw", "h100_equivalents", "chip_types", "owner", "users",
          "source_url", "retrieved"]
TIMELINE_FIELDS = ["site_id", "epoch_name", "date", "buildings_operational", "it_power_mw", "h100_equivalents",
                   "construction_status", "source_url", "retrieved"]


def entries(text: str) -> dict[str, dict]:
    return {row["Name"]: row for row in csv.DictReader(io.StringIO(text))}


def estimates(links: list[dict], found: dict[str, dict], retrieved: str) -> list[dict]:
    missing = [link["epoch_name"] for link in links if link["epoch_name"] not in found]
    if missing:
        raise ValueError(f"not in the Epoch file: {', '.join(missing)}")
    rows = []
    for link in links:
        entry = found[link["epoch_name"]]
        rows.append({
            "site_id": link["site_id"], "epoch_name": link["epoch_name"],
            "it_power_mw": f"{float(entry['Current power (MW)']):.0f}",
            "h100_equivalents": f"{float(entry['Current H100 equivalents']):.0f}",
            "chip_types": entry["Current chip types"], "owner": entry["Owner"], "users": entry["Users"],
            "source_url": EPOCH_URL, "retrieved": retrieved,
        })
    return rows


def timelines(links: list[dict], text: str, retrieved: str) -> list[dict]:
    site = {link["epoch_name"]: link["site_id"] for link in links}
    rows = []
    for row in csv.DictReader(io.StringIO(text)):
        if row["Data center"] not in site:
            continue
        rows.append({
            "site_id": site[row["Data center"]], "epoch_name": row["Data center"], "date": row["Date"],
            "buildings_operational": f"{float(row['Buildings operational'] or 0):.0f}",
            "it_power_mw": f"{float(row['IT power (MW)'] or 0):.0f}",
            "h100_equivalents": f"{float(row['H100 equivalents'] or 0):.0f}",
            "construction_status": row["Construction status"], "source_url": TIMELINES_URL, "retrieved": retrieved,
        })
    return sorted(rows, key=lambda r: (r["site_id"], r["date"]))


def fetch(url: str, offline: bool) -> tuple[str, str]:
    """Text of an Epoch file and the date it was read, saving the file in data/raw/epoch."""
    saved = RAW / url.rsplit("/", 1)[1]
    if offline:
        return saved.read_text(), datetime.fromtimestamp(saved.stat().st_mtime, timezone.utc).strftime("%Y-%m-%d")
    text = fcr.download(url)
    RAW.mkdir(parents=True, exist_ok=True)
    saved.write_text(text)
    return text, datetime.now(timezone.utc).strftime("%Y-%m-%d")


def write(path: Path, fields: list[str], rows: list[dict]) -> None:
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--offline", action="store_true", help="read the saved files instead of downloading")
    args = parser.parse_args()

    with LINKS.open(newline="") as f:
        links = list(csv.DictReader(f))
    text, retrieved = fetch(EPOCH_URL, args.offline)
    rows = estimates(links, entries(text), retrieved)
    write(OUT, FIELDS, rows)
    text, retrieved = fetch(TIMELINES_URL, args.offline)
    stages = timelines(links, text, retrieved)
    write(TIMELINES_OUT, TIMELINE_FIELDS, stages)
    print(f"{len(rows)} estimates written to {OUT.relative_to(ROOT)} and {len(stages)} stages to {TIMELINES_OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
