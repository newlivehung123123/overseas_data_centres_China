"""Offline tests of the sorting of sites under the US rule on remote access, on small tables written here."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import flag_remote_access as f  # noqa: E402


def site(sid, status="operational", mw="", basis=""):
    return {"site_id": sid, "site_name": f"Site {sid}", "country_iso3": sid[:3], "status": status,
            "capacity_mw": mw, "capacity_basis": basis}


def role(sid, firm, kind, evidence="primary"):
    return {"site_id": sid, "firm": firm, "role": kind, "evidence": evidence}


FIRMS = [{"firm": "ByteDance", "grounds": "headquarters"},
         {"firm": "Global Switch", "grounds": "control"},
         {"firm": "DayOne", "grounds": "origin"},
         {"firm": "China-ASEAN Investment Cooperation Fund II", "grounds": "state lender fund"}]
SITES = [site("MYS-0001", mw="110", basis="it"), site("MYS-0002", status="planned"), site("GBR-0001"),
         site("MYS-0003"), site("MYS-0004")]
ROLES = [role("MYS-0001", "ByteDance", "tenant", "secondary"), role("MYS-0001", "DayOne", "operator"),
         role("MYS-0002", "ByteDance", "user", "unconfirmed"),
         role("GBR-0001", "Global Switch", "owner"),
         role("MYS-0003", "DayOne", "operator"),
         role("MYS-0004", "China-ASEAN Investment Cooperation Fund II", "financier")]


class ClassifyTest(unittest.TestCase):
    def setUp(self):
        self.rows = {r["site_id"]: r for r in f.classify(SITES, ROLES, FIRMS)}

    def test_named_customer_at_operational_site_gets_the_deadline(self):
        r = self.rows["MYS-0001"]
        self.assertEqual(r["category"], "named_customer")
        self.assertEqual(r["chinese_customers"], "ByteDance")
        self.assertEqual(r["other_firms"], "DayOne")
        self.assertEqual(r["licence_deadline"], "2027-02-17")
        self.assertEqual(r["customer_evidence"], "secondary")

    def test_named_customer_at_planned_site_gets_no_deadline(self):
        r = self.rows["MYS-0002"]
        self.assertEqual(r["category"], "named_customer")
        self.assertEqual(r["licence_deadline"], "")
        self.assertEqual(r["customer_evidence"], "unconfirmed")

    def test_firm_on_ground_of_control_that_owns_the_site(self):
        r = self.rows["GBR-0001"]
        self.assertEqual(r["category"], "chinese_operator_owner")
        self.assertEqual(r["chinese_operators_owners"], "Global Switch")
        self.assertEqual(r["licence_deadline"], "")

    def test_former_subsidiary_and_fund_name_no_chinese_customer(self):
        self.assertEqual(self.rows["MYS-0003"]["category"], "no_chinese_customer")
        self.assertEqual(self.rows["MYS-0004"]["category"], "no_chinese_customer")
        self.assertEqual(self.rows["MYS-0004"]["other_firms"], "China-ASEAN Investment Cooperation Fund II")

    def test_every_site_appears_once(self):
        self.assertEqual(sorted(self.rows), sorted(s["site_id"] for s in SITES))


if __name__ == "__main__":
    unittest.main()
