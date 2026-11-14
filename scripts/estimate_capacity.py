#!/usr/bin/env python3
"""Estimate the capacity of the sites outside mainland China in which a Chinese firm holds a role, as a low and a high estimate.

The estimate counts each data centre once. Where a firm reports its capacity by market or as one total for the firm,
as DayOne and Global Switch do in data/operator_markets.csv, the estimate takes the firm's own figures and leaves out
the figures of the sites of that firm for each stage that the firm reports. Global Switch reports only the capacity in
service, so the planned capacity of its sites is still taken from the sites. For every other site, the estimate takes the largest figure that the sources
give for each stage: capacity in service, and capacity under construction or planned.

The low estimate counts only figures stated by the firm itself or by a public authority (evidence "primary"), at sites
where the role of a Chinese firm is not graded "unconfirmed" and the status of the site is known. The high estimate
counts every figure, and uses the estimate of Epoch AI where Epoch's figure of IT power in service is larger than the
figure that the sources state. Figures of IT capacity, of power and of an unspecified basis are added as the sources
state them, so each estimate can mix the three bases, and the output gives the megawatts of each basis. The basis of the
figures that a firm reports comes from the firm's own definitions in data/capacity_definitions.csv. A builder or a
supplier of equipment does not hold or use the capacity of a site, so the estimate leaves out a site at which Chinese
firms hold only those two roles.

    python scripts/estimate_capacity.py    writes data/capacity_estimate.csv and data/capacity_estimate.json
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_CSV = ROOT / "data" / "capacity_estimate.csv"
OUT_JSON = ROOT / "data" / "capacity_estimate.json"
FIELDS = ["component", "firm", "site_id", "stage", "mw", "basis", "evidence", "counted_in", "source_table", "note"]
PIPELINE_COLUMNS = ("under_construction_mw", "secured_powered_land_mw")
SUPPLY_ROLES = {"builder", "equipment supplier"}
IN_SERVICE_STAGES = {"in_service"}
PIPELINE_STAGES = {"first_phase", "planned_total", "contracted"}


def read(name: str) -> list[dict]:
    with (ROOT / name).open(newline="") as f:
        return [r for r in csv.DictReader(f) if r.get("check_status", "found") == "found"]


def number(value: str) -> float:
    return float(value) if value not in ("", None) else 0.0


def basis_of(definitions: list[dict], firm: str, columns: list[str]) -> str:
    """The basis that the firm's definitions give for every one of the columns, or unspecified when they give none or differ."""
    given = {d["column"]: d["basis"] for d in definitions if d["firm"] == firm and d["column"] in columns}
    bases = set(given.values())
    return bases.pop() if columns and set(given) == set(columns) and len(bases) == 1 else "unspecified"


def components(sites, roles, markets, capacity, epoch, definitions=()) -> list[dict]:
    rows = []
    totals = defaultdict(lambda: defaultdict(float))
    for m in markets:
        firm = m["firm"]
        rows.append({"component": f"{firm}, {m['market']}", "firm": firm, "site_id": "", "stage": "in_service",
                     "mw": number(m["in_service_mw"]), "basis": basis_of(definitions, firm, ["in_service_mw"]),
                     "evidence": m["evidence"], "counted_in": "both", "source_table": "operator_markets",
                     "note": "Total that the firm reports"})
        reported = [c for c in PIPELINE_COLUMNS if m[c]]
        pipeline = sum(number(m[c]) for c in reported)
        if pipeline:
            rows.append({"component": f"{firm}, {m['market']}", "firm": firm, "site_id": "", "stage": "pipeline",
                         "mw": pipeline, "basis": basis_of(definitions, firm, reported), "evidence": m["evidence"],
                         "counted_in": "both", "source_table": "operator_markets",
                         "note": "Capacity under construction and on secured powered land that the firm reports"})
        totals[firm][m["market"]] = number(m["in_service_mw"])
    covered_firms = set(totals)
    reports_pipeline = {m["firm"] for m in markets if any(m[c] for c in PIPELINE_COLUMNS)}
    site = {s["site_id"]: s for s in sites}
    roles_at = defaultdict(list)
    for r in roles:
        if r.get("role") not in SUPPLY_ROLES:
            roles_at[r["site_id"]].append(r)
    covered = {sid for sid, rs in roles_at.items() if any(r["firm"] in covered_firms for r in rs)}
    covered_pipeline = {sid for sid, rs in roles_at.items() if any(r["firm"] in reports_pipeline for r in rs)}

    # A covered site adds to the high estimate only where Epoch AI estimates more IT power in service than the firm reports.
    by_market = defaultdict(float)
    for e in epoch:
        s = site.get(e["site_id"])
        if not s or e["site_id"] not in covered:
            continue
        firm = next(r["firm"] for r in roles_at[e["site_id"]] if r["firm"] in covered_firms)
        market = next((m for m in totals[firm] if m in s["city"] or m in s["site_name"]), None)
        if market:
            by_market[(firm, market)] += number(e["it_power_mw"])
    for (firm, market), mw in by_market.items():
        extra = mw - totals[firm][market]
        if extra > 0:
            rows.append({"component": f"{firm}, {market}", "firm": firm, "site_id": "", "stage": "in_service", "mw": extra,
                         "basis": "it", "evidence": "secondary", "counted_in": "high", "source_table": "epoch_estimates",
                         "note": f"Epoch AI estimates {mw:.0f} MW of IT power at the sites of the market, against "
                                 f"{totals[firm][market]:.0f} MW that the firm reports in service"})

    figures = defaultdict(list)
    for s in sites:
        if s["capacity_mw"]:
            stage = "in_service" if s["status"] == "operational" else "pipeline"
            figures[s["site_id"]].append((stage, number(s["capacity_mw"]), s["capacity_basis"] or "unspecified",
                                          s["evidence"], "sites", False))
    for c in capacity:
        status = site[c["site_id"]]["status"] if c["site_id"] in site else ""
        if c["stage"] in IN_SERVICE_STAGES or (c["stage"] in ("leased", "first_phase") and status == "operational"):
            stage = "in_service"
        elif c["stage"] in PIPELINE_STAGES:
            stage = "pipeline"
        else:
            continue
        # A planned total describes the whole site, so the estimate counts only the part that is not yet in service.
        whole = c["stage"] == "planned_total"
        figures[c["site_id"]].append((stage, number(c["capacity_mw"]), c["basis"], c["evidence"], "site_capacity", whole))
    epoch_mw = {e["site_id"]: number(e["it_power_mw"]) for e in epoch}

    for sid in sorted(figures):
        if sid not in site or not roles_at[sid] or (sid in covered and sid in covered_pipeline):
            continue
        s = site[sid]
        confirmed = any(r["evidence"] != "unconfirmed" for r in roles_at[sid])
        known = s["status"] != "unclear"
        firms = "; ".join(sorted({r["firm"] for r in roles_at[sid]}))
        in_service = [f for f in figures[sid] if f[0] == "in_service"] if sid not in covered else []
        in_low = max([f[1] for f in in_service if f[3] == "primary" and confirmed and known], default=0.0)
        in_high = max([f[1] for f in in_service] + [epoch_mw.get(sid, 0.0) if sid not in covered else 0.0], default=0.0)

        def remainder(f, counted):
            """Megawatts of a figure that an estimate counts: all of it, or a planned total less the capacity in service."""
            return max(0.0, f[1] - counted) if f[5] else f[1]

        for stage in ("in_service", "pipeline"):
            if sid in covered and stage == "in_service":
                continue
            options = [f for f in figures[sid] if f[0] == stage]
            if sid in covered and s["status"] == "operational":
                options = [f for f in options if not f[5]]     # the firm's total already holds the part in service
            if not options:
                continue
            low = [f for f in options if f[3] == "primary" and confirmed and known]
            best = max(options, key=lambda f: remainder(f, in_high))
            high_mw = remainder(best, in_high)

            def row(f, mw, counted_in, note):
                if f[5] and mw < f[1]:
                    note = (note + "; " if note else "") + f"Planned total of {f[1]:.0f} MW less {f[1] - mw:.0f} MW in service"
                return {"component": s["site_name"], "firm": firms, "site_id": sid, "stage": stage, "mw": mw, "basis": f[2],
                        "evidence": f[3], "counted_in": counted_in, "source_table": f[4], "note": note}

            if low:
                pick = max(low, key=lambda f: remainder(f, in_low))
                low_mw = remainder(pick, in_low)
                same = pick == best and low_mw == high_mw
                if low_mw:
                    rows.append(row(pick, low_mw, "both" if same else "low", ""))
                if not same and high_mw:
                    rows.append(row(best, high_mw, "high", "Larger figure from a source below the grade that the low estimate requires" if pick != best
                                    else "The high estimate counts more capacity in service at the site"))
            elif high_mw:
                reason = "the role of the Chinese firm is unconfirmed" if not confirmed else (
                    "the status of the site is unclear" if not known else "the figure is not from a primary source")
                rows.append(row(best, high_mw, "high", f"High estimate only, because {reason}"))
        if sid in epoch_mw and sid not in covered:
            stated = max([f[1] for f in figures[sid] if f[0] == "in_service"], default=0.0)
            if epoch_mw[sid] > stated:
                rows.append({"component": s["site_name"], "firm": firms, "site_id": sid, "stage": "in_service",
                             "mw": epoch_mw[sid] - stated, "basis": "it", "evidence": "secondary", "counted_in": "high",
                             "source_table": "epoch_estimates",
                             "note": f"Epoch AI estimates {epoch_mw[sid]:.0f} MW of IT power, against {stated:.0f} MW stated"})
    return rows


def totals(rows: list[dict], sites: list[dict], with_figure: set[str]) -> dict:
    """The low estimate adds the rows counted in both estimates and in the low estimate alone, the high estimate those in both and in the high estimate alone."""
    out = {}
    for bound in ("low", "high"):
        stages, basis = defaultdict(float), defaultdict(float)
        for r in rows:
            if r["counted_in"] in ("both", bound):
                stages[r["stage"]] += r["mw"]
                basis[r["basis"]] += r["mw"]
        out[bound] = {"in_service_mw": round(stages["in_service"]), "pipeline_mw": round(stages["pipeline"]),
                      "total_mw": round(stages["in_service"] + stages["pipeline"]),
                      "mw_by_basis": {k: round(v) for k, v in sorted(basis.items())}}
    out["sites"] = len(sites)
    out["sites_without_a_figure"] = len([s for s in sites if s["site_id"] not in with_figure])
    return out


def with_a_figure(sites, roles, markets, capacity) -> set[str]:
    """Sites with a figure of their own, and sites whose stage is covered by a figure that a firm reports."""
    reports_pipeline = {m["firm"] for m in markets if any(m[c] for c in PIPELINE_COLUMNS)}
    reports_in_service = {m["firm"] for m in markets}
    operational = {s["site_id"] for s in sites if s["status"] == "operational"}
    out = {s["site_id"] for s in sites if s["capacity_mw"]} | {c["site_id"] for c in capacity}
    out |= {r["site_id"] for r in roles if r["firm"] in reports_pipeline}
    out |= {r["site_id"] for r in roles if r["firm"] in reports_in_service and r["site_id"] in operational}
    return out


def origin_only(firms: list[dict]) -> set[str]:
    """Firms that count as Chinese on their origin alone, such as DayOne, which the second estimate leaves out."""
    return {f["firm"] for f in firms if {g.strip() for g in f["grounds"].split(";")} == {"origin"}}


def summarise_rows(sites, roles, markets, capacity, epoch, definitions) -> tuple[list[dict], dict]:
    rows = components(sites, roles, markets, capacity, epoch, definitions)
    held = {r["site_id"] for r in roles if r["role"] not in SUPPLY_ROLES}
    summary = totals(rows, [s for s in sites if s["site_id"] in held], with_a_figure(sites, roles, markets, capacity))
    return rows, summary


def estimate() -> tuple[list[dict], dict]:
    sites, roles = read("data/sites.csv"), read("data/site_roles.csv")
    markets, capacity = read("data/operator_markets.csv"), read("data/site_capacity.csv")
    epoch, definitions = read("data/epoch_estimates.csv"), read("data/capacity_definitions.csv")
    rows, summary = summarise_rows(sites, roles, markets, capacity, epoch, definitions)
    summary["sites_with_supply_roles_only"] = len(sites) - summary["sites"]
    # The second estimate leaves out the roles and the reported totals of firms that count on their origin alone.
    left_out = origin_only(read("data/firms.csv")) if (ROOT / "data" / "firms.csv").exists() else set()
    kept_roles = [r for r in roles if r["firm"] not in left_out]
    kept_markets = [m for m in markets if m["firm"] not in left_out]
    _, without = summarise_rows(sites, kept_roles, kept_markets, capacity, epoch, definitions)
    without["firms_left_out"] = sorted(left_out)
    summary["without_origin_only"] = without
    return rows, summary


def main() -> None:
    rows, summary = estimate()
    with OUT_CSV.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows([{**r, "mw": f"{r['mw']:.0f}"} for r in rows])
    OUT_JSON.write_text(json.dumps(summary, indent=2) + "\n")
    for bound in ("low", "high"):
        s = summary[bound]
        print(f"{bound}: {s['in_service_mw']} MW in service, {s['pipeline_mw']} MW under construction or planned, "
              f"{s['total_mw']} MW in all; by basis {s['mw_by_basis']}")
    w = summary["without_origin_only"]
    print(f"without {', '.join(w['firms_left_out'])}: low {w['low']['in_service_mw']} MW in service and {w['low']['pipeline_mw']} MW "
          f"under construction or planned; high {w['high']['in_service_mw']} MW and {w['high']['pipeline_mw']} MW")
    print(f"{summary['sites_without_a_figure']} of {summary['sites']} sites have no figure of capacity; "
          f"{summary['sites_with_supply_roles_only']} further sites, where Chinese firms only build or supply equipment, are left out")


if __name__ == "__main__":
    main()
