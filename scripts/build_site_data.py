#!/usr/bin/env python3
"""Write the data file that the dashboard in site/ reads, from the checked layers.

The dashboard shows the sites with the roles of firms at each site and the cloud regions, each at
the point of its city in config/places.csv, and the rules recorded for each country. The government data centres of the AidData layer are
left out of the dashboard until the article pitched on them has been answered, as CONTRIBUTING.md asks.

    python scripts/build_site_data.py    writes site/data/dashboard.json
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "site" / "data" / "dashboard.json"


def read(name: str) -> list[dict]:
    with (ROOT / name).open(newline="") as f:
        return list(csv.DictReader(f))


def point(places: dict, city: str, country: str) -> list[float] | None:
    place = places.get((city, country))
    if not place or not place.get("lat"):
        return None
    return [round(float(place["lat"]), 4), round(float(place["lon"]), 4)]


def build() -> dict:
    places = {(p["city"], p["country"]): p for p in read("config/places.csv")}
    roles = defaultdict(list)
    for r in read("data/site_roles.csv"):
        roles[r["site_id"]].append({"firm": r["firm"], "origin": r["firm_origin"], "role": r["role"],
                                    "source": r["source_url"], "quote": r["source_quote"], "check": r["check_status"]})
    compute = defaultdict(list)
    for a in read("data/ai_compute.csv"):
        compute[a["site_id"]].append({"firm": a["firm"], "chips": a["chips"], "count": a["chip_count"], "access": a["access"],
                                      "status": a["status"], "source": a["source_url"], "quote": a["source_quote"]})
    records = []
    for s in read("data/sites.csv"):
        records.append({
            "layer": "site", "id": s["site_id"], "name": s["site_name"], "city": s["city"], "country": s["country"],
            "status": s["status"], "capacity_mw": s["capacity_mw"], "capacity_basis": s["capacity_basis"],
            "note": s["note"], "source": s["source_url"], "quote": s["source_quote"], "check": s["check_status"],
            "iso3": s["country_iso3"], "roles": roles[s["site_id"]], "ai": compute[s["site_id"]],
            "point": point(places, s["city"], s["country"]),
        })
    for c in read("data/cloud_regions.csv"):
        records.append({
            "layer": "cloud_region", "id": c["region_id"] or c["region_label"], "name": f"{c['provider']} {c['region_label']}".strip(),
            "city": c["city"], "country": c["country"], "status": c["status"], "capacity_mw": "", "capacity_basis": "",
            "note": f"Launched {c['launch_year']}" if c["launch_year"] else "", "source": c["source_url"],
            "quote": c["source_quote"], "check": c["check_status"],
            "roles": [{"firm": c["provider"], "origin": "", "role": "operator", "source": c["source_url"],
                       "quote": c["source_quote"], "check": c["check_status"]}],
            "iso3": c["country_iso3"], "point": point(places, c["city"], c["country"]),
        })
    rules = [{"id": r["rule_id"], "jurisdiction": r["jurisdiction"], "iso3": r["country_iso3"], "applies_in": r["applies_in"].split(";"),
              "instrument": r["instrument"], "covers": r["covers"], "status": r["status"], "date": r["date"],
              "note": r["note"], "source": r["source_url"], "quote": r["source_quote"], "check": r["check_status"]}
             for r in read("data/rules.csv")]
    return {"built": date.today().isoformat(), "records": records, "rules": rules}


def main() -> None:
    data = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n")
    missing = [r["id"] for r in data["records"] if r["point"] is None]
    print(f"Wrote {len(data['records'])} records to {OUT.relative_to(ROOT)}; {len(missing)} without a point")


if __name__ == "__main__":
    main()
