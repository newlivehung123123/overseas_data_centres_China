#!/usr/bin/env python3
"""Write the data file that the dashboard in site/ reads, from the checked layers.

The dashboard shows the sites with the roles of firms at each site and the cloud regions, each at
the point of its city in config/places.csv, and the rules recorded for each country. Each site carries its reports of AI chips,
its statements of capacity and the estimates of Epoch AI where Epoch's database holds the site, and reports of AI chips
whose sources name no site are listed apart. The government data centres of the AidData layer are left out of the
dashboard until the article pitched on them has been answered, as CONTRIBUTING.md asks.

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
LEVEL_B_MW = 20    # announced capacity from which a site is coded at level B, as the codebook sets out


def level(figures: list[str], ai_reports: int) -> str:
    """Level B for a site with announced capacity of at least 20 MW or with a report of AI chips, else level A."""
    if ai_reports or any(f and float(f) >= LEVEL_B_MW for f in figures):
        return "B"
    return "A"


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
                                      "status": a["status"], "date": a["date"], "note": a["note"], "source": a["source_url"],
                                      "quote": a["source_quote"], "check": a["check_status"]})
    links = {link["site_id"]: link for link in read("data/epoch_links.csv")}
    epoch = {}
    for e in read("data/epoch_estimates.csv"):
        link = links[e["site_id"]]
        epoch[e["site_id"]] = {"name": e["epoch_name"], "mw": e["it_power_mw"], "h100e": e["h100_equivalents"],
                               "chips": e["chip_types"], "owner": e["owner"], "users": e["users"], "retrieved": e["retrieved"],
                               "page": link["source_url"], "quote": link["source_quote"], "check": link["check_status"]}
    capacity = defaultdict(list)
    for c in read("data/site_capacity.csv"):
        capacity[c["site_id"]].append({"mw": c["capacity_mw"], "basis": c["basis"], "stage": c["stage"], "date": c["date"],
                                       "note": c["note"], "source": c["source_url"]})
    records = []
    for s in read("data/sites.csv"):
        records.append({
            "layer": "site", "id": s["site_id"], "name": s["site_name"], "city": s["city"], "country": s["country"],
            "status": s["status"], "capacity_mw": s["capacity_mw"], "capacity_basis": s["capacity_basis"],
            "note": s["note"], "source": s["source_url"], "quote": s["source_quote"], "check": s["check_status"],
            "iso3": s["country_iso3"], "roles": roles[s["site_id"]], "ai": compute[s["site_id"]], "capacity": capacity[s["site_id"]],
            "epoch": epoch.get(s["site_id"]), "point": point(places, s["city"], s["country"]),
            "level": level([s["capacity_mw"]] + [c["mw"] for c in capacity[s["site_id"]]], len(compute[s["site_id"]])),
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
    return {"built": date.today().isoformat(), "records": records, "rules": rules, "ai_without_site": compute[""]}


def main() -> None:
    data = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n")
    missing = [r["id"] for r in data["records"] if r["point"] is None]
    print(f"Wrote {len(data['records'])} records to {OUT.relative_to(ROOT)}; {len(missing)} without a point")


if __name__ == "__main__":
    main()
