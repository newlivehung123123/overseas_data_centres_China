"""Offline tests of the dashboard data, on small tables written here."""

import csv
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import build_site_data as b  # noqa: E402

TABLES = {
    "config/places.csv": [{"city": "Johor", "country": "Malaysia", "lat": "2.02288", "lon": "103.3114"}],
    "data/sites.csv": [{"site_id": "MYS-0001", "site_name": "A site", "city": "Johor", "country": "Malaysia",
                        "country_iso3": "MYS", "status": "operational", "capacity_mw": "110", "capacity_basis": "it",
                        "note": "", "source_url": "https://example.org", "source_quote": "q", "check_status": "found"}],
    "data/site_roles.csv": [{"site_id": "MYS-0001", "firm": "ByteDance", "firm_origin": "", "role": "tenant",
                             "source_url": "https://example.org", "source_quote": "q", "check_status": "found"}],
    "data/cloud_regions.csv": [{"provider": "Tencent Cloud", "region_label": "Seoul", "region_id": "ap-seoul", "city": "Seoul",
                                "country": "South Korea", "country_iso3": "KOR", "status": "operational", "launch_year": "",
                                "source_url": "https://example.org", "source_quote": "q", "check_status": "found"}],
    "data/ai_compute.csv": [{"site_id": "MYS-0001", "firm": "ByteDance", "chip_count": "36000", "chips": "Nvidia B200",
                             "access": "rented", "status": "planned", "date": "2026-03", "note": "",
                             "source_url": "https://example.org", "source_quote": "q", "check_status": "found"},
                            {"site_id": "", "firm": "Tencent", "chip_count": "100000", "chips": "AI chips",
                             "access": "rented", "status": "unclear", "date": "2026-10", "note": "",
                             "source_url": "https://example.org", "source_quote": "q", "check_status": "found"}],
    "data/epoch_links.csv": [{"site_id": "MYS-0001", "epoch_name": "A site", "note": "", "source_url": "https://example.org/epoch",
                              "source_quote": "q", "check_status": "found"}],
    "data/epoch_estimates.csv": [{"site_id": "MYS-0001", "epoch_name": "A site", "it_power_mw": "243", "h100_equivalents": "221052",
                                  "chip_types": "B200", "owner": "", "users": "", "source_url": "https://example.org/csv",
                                  "retrieved": "2026-10-22"}],
    "data/operator_customers.csv": [{"firm": "Nscale", "customer": "largest customer", "customer_description": "",
                                     "identified_as": "", "share_of_revenue": "0.73", "revenue": "", "period": "year 2025",
                                     "note": "", "source_url": "https://example.org", "source_quote": "q", "check_status": "found"}],
    "data/site_capacity.csv": [{"site_id": "MYS-0001", "capacity_mw": "300", "basis": "power", "stage": "planned_total",
                                "date": "2025-11", "note": "", "source_url": "https://example.org", "source_quote": "q",
                                "check_status": "found"}],
    "data/rules.csv": [{"rule_id": "MYS-0001", "jurisdiction": "Malaysia", "country_iso3": "MYS", "applies_in": "MYS",
                        "instrument": "Permit", "covers": "chip_transit", "status": "in_force", "date": "2025-07", "note": "",
                        "source_url": "https://example.org", "source_quote": "q", "check_status": "found"}],
}


class BuildTest(unittest.TestCase):
    def test_records_carry_roles_points_and_rules(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name, rows in TABLES.items():
                (root / name).parent.mkdir(parents=True, exist_ok=True)
                with (root / name).open("w", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=list(rows[0]))
                    writer.writeheader()
                    writer.writerows(rows)
            with mock.patch.object(b, "ROOT", root):
                data = b.build()
        site, region = data["records"]
        self.assertEqual(site["roles"][0]["firm"], "ByteDance")
        self.assertEqual(site["point"], [2.0229, 103.3114])
        self.assertIsNone(region["point"])
        self.assertEqual(region["roles"][0]["role"], "operator")
        self.assertEqual(data["rules"][0]["applies_in"], ["MYS"])
        self.assertEqual(site["ai"][0]["count"], "36000")
        self.assertEqual(site["capacity"][0]["mw"], "300")
        self.assertEqual(region.get("ai", []), [])
        self.assertEqual(site["epoch"]["mw"], "243")
        self.assertIsNone(region.get("epoch"))
        self.assertEqual([x["firm"] for x in data["ai_without_site"]], ["Tencent"])
        self.assertEqual(len(site["ai"]), 1)
        self.assertEqual(site["level"], "B")
        self.assertEqual(data["customers"][0]["share"], "0.73")

    def test_level_b_needs_20_mw_or_a_report_of_ai_chips(self):
        self.assertEqual(b.level(["15", ""], 0), "A")
        self.assertEqual(b.level(["15", "20"], 0), "B")
        self.assertEqual(b.level([""], 1), "B")


if __name__ == "__main__":
    unittest.main()
