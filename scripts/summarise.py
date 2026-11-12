#!/usr/bin/env python3
"""Count the checked rows of the files of sites, cloud regions and capacity, and write the figures to data/summary.json.

The figures cover the sites and their levels, the roles of firms at the sites, the cloud regions, the
capacity that operators report by market, the census of each market, the grades of evidence of each file and the low
and high bounds of the capacity estimate. Only rows whose passage was found on the page are counted. The file of
government data centres from AidData has its own summary in data/aiddata_summary.json.

    python scripts/summarise.py
"""

from __future__ import annotations

import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_site_data import level  # noqa: E402
from estimate_capacity import estimate  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "summary.json"
GRADED = ["sites", "site_roles", "cloud_regions", "operator_markets", "capacity_definitions", "firm_links",
          "operator_customers", "ai_compute", "site_capacity", "rules", "epoch_links"]


def read(name: str) -> list[dict]:
    with (ROOT / name).open(newline="") as f:
        return [r for r in csv.DictReader(f) if r.get("check_status", "found") == "found"]


def censuses() -> list[str]:
    """Names of the census files in data, one for each market, such as johor_census."""
    return sorted(path.stem for path in (ROOT / "data").glob("*_census.csv"))


def number(value: str) -> float:
    return float(value) if value not in ("", None) else 0.0


def summarise() -> dict:
    sites, roles = read("data/sites.csv"), read("data/site_roles.csv")
    regions, markets = read("data/cloud_regions.csv"), read("data/operator_markets.csv")
    firms_at = defaultdict(set)
    for r in roles:
        firms_at[r["firm"]].add(r["site_id"])
    capacity = defaultdict(float)
    for s in sites:
        if s["capacity_mw"]:
            capacity[s["capacity_basis"] or "unspecified"] += number(s["capacity_mw"])
    figures, reports = defaultdict(list), Counter(a["site_id"] for a in read("data/ai_compute.csv"))
    for c in read("data/site_capacity.csv"):
        figures[c["site_id"]].append(c["capacity_mw"])
    levels = {s["site_id"]: level([s["capacity_mw"]] + figures[s["site_id"]], reports[s["site_id"]]) for s in sites}
    operational = [r for r in regions if r["status"] == "operational" and r["hong_kong_macau"] == "no"]
    by_operator = defaultdict(lambda: defaultdict(float))
    for m in markets:
        for field in ("in_service_mw", "under_construction_mw", "secured_powered_land_mw", "total_mw"):
            by_operator[m["firm"]][field] += number(m[field])
    return {
        "sites": len(sites),
        "site_countries": len({s["country_iso3"] for s in sites}),
        "sites_by_status": dict(Counter(s["status"] for s in sites)),
        "sites_by_country": dict(Counter(s["country"] for s in sites).most_common()),
        "roles": len(roles),
        "roles_by_role": dict(Counter(r["role"] for r in roles).most_common()),
        "sites_by_firm": {firm: len(ids) for firm, ids in sorted(firms_at.items(), key=lambda x: -len(x[1]))},
        "sites_by_level": dict(sorted(Counter(levels.values()).items())),
        "sites_with_capacity": sum(1 for s in sites if s["capacity_mw"]),
        "site_capacity_mw_by_basis": {k: round(v) for k, v in capacity.items()},
        "cloud_regions_operational_outside_china_hk_macau": len(operational),
        "cloud_region_countries": len({r["country_iso3"] for r in operational}),
        "cloud_regions_by_provider": dict(Counter(r["provider"] for r in operational).most_common()),
        "operator_market_mw": {firm: {k: round(v) for k, v in fields.items()} for firm, fields in by_operator.items()},
        "rules": len(read("data/rules.csv")),
        "census": {rows[0]["market"]: {"facilities": len(rows), "operators": len({c["operator"] for c in rows}),
                                       "by_chinese_link": dict(Counter(c["chinese_link"] for c in rows).most_common())}
                   for rows in (read(f"data/{name}.csv") for name in censuses()) if rows},
        "evidence_by_file": {name: dict(Counter(r["evidence"] for r in read(f"data/{name}.csv")))
                             for name in GRADED + censuses()},
        "capacity_estimate_mw": estimate()[1],
    }


def main() -> None:
    summary = summarise()
    OUT.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
    for key, value in summary.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
