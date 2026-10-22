"""Offline tests of the reading of Epoch AI's database file, on a short file written here."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import fetch_epoch as e  # noqa: E402

FILE = ("Name,Current H100 equivalents,Current power (MW),Owner,Users,Current chip types\n"
        "DayOne Kempas,480638.7,421.69,,,B300\n"
        "Oracle Batam,84386.05,72,Oracle #likely,Tencent #speculative,\"B200,B300\"\n")


class EpochTest(unittest.TestCase):
    def test_estimates_are_read_from_the_file(self):
        links = [{"site_id": "MYS-0004", "epoch_name": "DayOne Kempas"}, {"site_id": "IDN-0002", "epoch_name": "Oracle Batam"}]
        rows = e.estimates(links, e.entries(FILE), "2026-10-22")
        self.assertEqual([r["it_power_mw"] for r in rows], ["422", "72"])
        self.assertEqual(rows[0]["h100_equivalents"], "480639")
        self.assertEqual(rows[1]["users"], "Tencent #speculative")
        self.assertEqual(rows[1]["chip_types"], "B200,B300")

    def test_a_name_missing_from_the_file_stops_the_script(self):
        with self.assertRaises(ValueError):
            e.estimates([{"site_id": "MYS-0003", "epoch_name": "DayOne Nusajaya"}], e.entries(FILE), "2026-10-22")


if __name__ == "__main__":
    unittest.main()
