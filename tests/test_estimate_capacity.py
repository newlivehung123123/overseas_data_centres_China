"""Offline tests of the capacity estimate, on small tables written here."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import estimate_capacity as e  # noqa: E402


def site(sid, status, mw="", basis="", evidence="primary", name="A site", city="Johor"):
    return {"site_id": sid, "site_name": name, "city": city, "status": status, "capacity_mw": mw,
            "capacity_basis": basis, "evidence": evidence}


def role(sid, firm, evidence="primary", kind="tenant"):
    return {"site_id": sid, "firm": firm, "evidence": evidence, "role": kind}


MARKETS = [{"firm": "DayOne", "market": "Johor", "in_service_mw": "100", "under_construction_mw": "50",
            "secured_powered_land_mw": "20", "evidence": "primary"},
           {"firm": "Global Switch", "market": "All markets", "in_service_mw": "30", "under_construction_mw": "",
            "secured_powered_land_mw": "", "evidence": "primary"}]
SITES = [site("MYS-0001", "operational", "40", "it"),
         site("MYS-0002", "operational", "10", "it", evidence="secondary"),
         site("MYS-0003", "operational", "999"),
         site("ESP-0003", "planned"),
         site("MYS-0004", "planned", "60", evidence="primary")]
ROLES = [role("MYS-0001", "ByteDance"), role("MYS-0002", "ByteDance"), role("MYS-0003", "DayOne"),
         role("ESP-0003", "Global Switch"), role("MYS-0004", "Shanghai DC-Science", evidence="unconfirmed")]
CAPACITY = [{"site_id": "ESP-0003", "capacity_mw": "36", "basis": "it", "stage": "planned_total", "evidence": "primary"}]
EPOCH = [{"site_id": "MYS-0001", "it_power_mw": "55"}, {"site_id": "MYS-0003", "it_power_mw": "120"}]
DEFINITIONS = [{"firm": "DayOne", "column": "in_service_mw", "basis": "it"},
               {"firm": "DayOne", "column": "under_construction_mw", "basis": "it"}]


class EstimateTest(unittest.TestCase):
    def setUp(self):
        self.rows = e.components(SITES, ROLES, MARKETS, CAPACITY, EPOCH, DEFINITIONS)
        self.total = e.totals(self.rows, SITES, e.with_a_figure(SITES, ROLES, MARKETS, CAPACITY))

    def test_firm_totals_replace_the_figures_of_their_sites(self):
        self.assertFalse(any(r["site_id"] == "MYS-0003" and r["source_table"] == "sites" for r in self.rows))

    def test_low_bound_counts_only_primary_figures_at_confirmed_sites(self):
        self.assertEqual(self.total["low"]["in_service_mw"], 100 + 30 + 40)
        self.assertEqual(self.total["low"]["pipeline_mw"], 70 + 36)

    def test_high_bound_adds_other_figures_and_larger_epoch_estimates(self):
        self.assertEqual(self.total["high"]["in_service_mw"], 100 + 30 + 40 + 10 + 15 + 20)
        self.assertEqual(self.total["high"]["pipeline_mw"], 70 + 36 + 60)

    def test_basis_of_a_firm_total_comes_from_the_firm_definitions(self):
        dayone = {r["stage"]: r["basis"] for r in self.rows if r["firm"] == "DayOne" and r["source_table"] == "operator_markets"}
        # The definitions give the basis of the capacity under construction but not of the secured powered land.
        self.assertEqual(dayone, {"in_service": "it", "pipeline": "unspecified"})

    def test_a_site_where_chinese_firms_only_supply_equipment_is_left_out(self):
        sites = SITES + [site("IDN-0007", "operational", "16", evidence="primary")]
        roles = ROLES + [role("IDN-0007", "Huawei", kind="equipment supplier")]
        rows = e.components(sites, roles, MARKETS, CAPACITY, EPOCH, DEFINITIONS)
        self.assertFalse(any(r["site_id"] == "IDN-0007" for r in rows))

    def test_a_planned_site_of_a_firm_that_reports_only_capacity_in_service_has_no_figure(self):
        self.assertEqual(self.total["sites_without_a_figure"], 0)
        sites = SITES + [site("GBR-0001", "planned")]
        roles = ROLES + [role("GBR-0001", "Global Switch")]
        self.assertNotIn("GBR-0001", e.with_a_figure(sites, roles, MARKETS, CAPACITY))


if __name__ == "__main__":
    unittest.main()
