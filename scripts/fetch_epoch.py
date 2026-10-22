#!/usr/bin/env python3
"""Read the estimates of Epoch AI for the sites that its database of AI data centres shares with this dataset.

Epoch AI publishes a database of large AI data centres, with the IT power and the AI compute of each
one estimated from satellite imagery, permits and company documents, under the Creative Commons
Attribution licence. A person matches a site in data/sites.csv to an entry of the database in
config/epoch_links.csv, with the passage of the Epoch page that supports the match, and
scripts/check_sources.py checks that passage. This script downloads the database file, saves it in
data/raw/epoch, and writes data/epoch_estimates.csv with the estimates for each matched site, read
from the file and not typed by hand.

    python scripts/fetch_epoch.py              downloads the database file
    python scripts/fetch_epoch.py --offline    reads the saved file instead
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
SAVED = ROOT / "data" / "raw" / "epoch" / "data_centers.csv"
LINKS = ROOT / "config" / "epoch_links.csv"
OUT = ROOT / "data" / "epoch_estimates.csv"
FIELDS = ["site_id", "epoch_name", "it_power_mw", "h100_equivalents", "chip_types", "owner", "users",
          "source_url", "retrieved"]


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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--offline", action="store_true", help="read the saved file instead of downloading")
    args = parser.parse_args()

    if args.offline:
        text = SAVED.read_text()
        retrieved = datetime.fromtimestamp(SAVED.stat().st_mtime, timezone.utc).strftime("%Y-%m-%d")
    else:
        text = fcr.download(EPOCH_URL)
        retrieved = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        SAVED.parent.mkdir(parents=True, exist_ok=True)
        SAVED.write_text(text)
    with LINKS.open(newline="") as f:
        links = list(csv.DictReader(f))
    rows = estimates(links, entries(text), retrieved)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} estimates written to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
