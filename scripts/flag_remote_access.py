#!/usr/bin/env python3
"""Sort the sites by how the US rule of 19 November 2026 on remote access reaches them, and write data/remote_access_rule.csv.

The interim final rule "Addressing Remote Access to Advanced Semiconductors" (91 FR 74970), recorded in
data/rules.csv as USA-0013 and USA-0014, requires a licence for advanced chips used at a data centre that provides
more than 12,000,000 aggregate TPP to companies headquartered, or whose ultimate parent company is headquartered, in
Country Group D:5 or Macau. A data centre that provided such computing power before 19 November 2026 must obtain a
licence within 90 days of that date, that is, by 17 February 2027, in order to continue. Computing power used only for
a commercial recommender system is exempt when the data centre reports the customer, the TPP of the chips and its
checks to BIS.

The script reads only the checked rows of data/sites.csv, data/site_roles.csv and data/firms.csv and adds no fact of
its own. It does not decide whether a site needs a licence, because the sources give neither the TPP of the chips at a
site nor the share of the computing power that a customer uses. It sorts each site into one of three categories.

    named_customer           a firm headquartered or controlled in mainland China or Hong Kong is named as a tenant
                             or user of the site, so the licence requirement of USA-0014 can apply
    chinese_operator_owner   no such customer is named, but such a firm operates or owns the site, so chips that the
                             firm itself receives already need a licence under the rule of October 2023 (USA-0007)
    no_chinese_customer      the only firms named are former subsidiaries of Chinese firms, a fund of a Chinese state
                             lender or a supplier of equipment, so the rule applies only through customers that the
                             sources do not name

    python scripts/flag_remote_access.py
"""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "remote_access_rule.csv"
DEADLINE = "2027-02-17"
CUSTOMER_ROLES = {"tenant", "user"}
OPERATOR_ROLES = {"operator", "owner"}
CHINESE_GROUNDS = {"headquarters", "control"}
GRADES = ["primary", "secondary", "unconfirmed"]
COLUMNS = ["site_id", "site_name", "country_iso3", "status", "category", "chinese_customers", "customer_evidence",
           "chinese_operators_owners", "other_firms", "capacity_mw", "capacity_basis", "licence_deadline", "note"]
NOTES = {
    "named_customer": "A licence under USA-0014 is needed if the computing power provided to the named firms exceeds "
                      "12,000,000 aggregate TPP and is not used only for a commercial recommender system that the data "
                      "centre reports to BIS; the sources give neither the TPP nor the use",
    "chinese_operator_owner": "Chips that the named firm itself receives need a licence under the rule of October 2023 "
                              "(USA-0007); USA-0014 applies only through customers that the sources do not name",
    "no_chinese_customer": "USA-0014 applies only through customers headquartered in Country Group D:5 or Macau, "
                           "and the sources name none",
}


def read(name: str) -> list[dict]:
    with (ROOT / name).open(newline="") as f:
        return [r for r in csv.DictReader(f) if r.get("check_status", "found") == "found"]


def grounds_of(firms: list[dict]) -> dict[str, set[str]]:
    """Grounds of each firm in firms.csv, such as {"headquarters"} or {"origin"}."""
    return {f["firm"]: {g.strip() for g in f["grounds"].split(";")} for f in firms}


def weakest(grades: list[str]) -> str:
    """Lowest grade of evidence among the roles, so that a category never rests on more than its weakest role."""
    return max(grades, key=GRADES.index) if grades else ""


def classify(sites: list[dict], roles: list[dict], firms: list[dict]) -> list[dict]:
    grounds = grounds_of(firms)
    by_site = defaultdict(list)
    for r in roles:
        by_site[r["site_id"]].append(r)
    rows = []
    for s in sorted(sites, key=lambda s: s["site_id"]):
        customers, operators, others, grades = set(), set(), set(), []
        for r in by_site.get(s["site_id"], []):
            chinese = bool(grounds.get(r["firm"], set()) & CHINESE_GROUNDS)
            if chinese and r["role"] in CUSTOMER_ROLES:
                customers.add(r["firm"])
                grades.append(r["evidence"])
            elif chinese and r["role"] in OPERATOR_ROLES:
                operators.add(r["firm"])
            else:
                others.add(r["firm"])
        if customers:
            category = "named_customer"
        elif operators:
            category = "chinese_operator_owner"
        else:
            category = "no_chinese_customer"
        serving = category == "named_customer" and s["status"] == "operational"
        rows.append({
            "site_id": s["site_id"], "site_name": s["site_name"], "country_iso3": s["country_iso3"],
            "status": s["status"], "category": category, "chinese_customers": "; ".join(sorted(customers)),
            "customer_evidence": weakest(grades), "chinese_operators_owners": "; ".join(sorted(operators)),
            "other_firms": "; ".join(sorted(others - customers - operators)), "capacity_mw": s["capacity_mw"],
            "capacity_basis": s["capacity_basis"], "licence_deadline": DEADLINE if serving else "",
            "note": NOTES[category],
        })
    return rows


def main() -> None:
    rows = classify(read("data/sites.csv"), read("data/site_roles.csv"), read("data/firms.csv"))
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    counts = defaultdict(int)
    for r in rows:
        counts[r["category"]] += 1
    dated = sum(1 for r in rows if r["licence_deadline"])
    print(f"{len(rows)} sites: " + ", ".join(f"{n} {c}" for c, n in sorted(counts.items())))
    print(f"{dated} operational sites with a named customer, which needed a licence by {DEADLINE} to continue "
          f"if they provided more than 12,000,000 aggregate TPP to such customers")


if __name__ == "__main__":
    main()
