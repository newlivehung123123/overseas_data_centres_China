"""Offline tests of the passage check and of the validation of sites and roles."""

import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import check_sources as c  # noqa: E402

PAGE = ("Bridge Data Centres (BDC) celebrate the grand opening of the first phase hyperscale data centre (MY06) in "
        "Sedenak, Johor. ByteDance System Sdn. Bhd, will be the anchor tenant of BDC's hyperscale data centre.")


class PassageTest(unittest.TestCase):
    def test_passage_found_despite_spacing_punctuation_and_case(self):
        share = c.share_found("bytedance system sdn bhd will be the ANCHOR tenant", PAGE)
        self.assertEqual(c.verdict(share), "found")

    def test_accents_are_ignored(self):
        self.assertEqual(c.share_found("potência instalada", "A potencia instalada de 300 MW"), 1.0)

    def test_passage_not_on_page(self):
        self.assertEqual(c.verdict(c.share_found("Alibaba Cloud will be the anchor tenant in Batam", PAGE)), "not_found")

    def test_partly_found(self):
        share = c.share_found("ByteDance System Sdn. Bhd, will be the anchor tenant of a campus in Lahti, Finland", PAGE)
        self.assertEqual(c.verdict(share), "partly_found")


class SecondPassageTest(unittest.TestCase):
    def test_a_row_with_a_link_passage_has_both_checked(self):
        pages = {"https://example.org/list": ("Bridge DC: MY06-1 Bridge Data Centres Medium Operational", "2026-10-22"),
                 "https://example.org/my06": (PAGE, "2026-10-22")}
        rows = [{"facility": "MY06-1", "source_url": "https://example.org/list", "source_quote": "Bridge DC: MY06-1 Bridge Data Centres",
                 "link_source_url": "https://example.org/my06", "link_source_quote": "ByteDance System Sdn. Bhd, will be the anchor tenant"},
                {"facility": "JDC1", "source_url": "https://example.org/list", "source_quote": "Bridge DC: MY06-1",
                 "link_source_url": "", "link_source_quote": ""}]
        with mock.patch.object(c, "page", lambda url, refetch: pages[url]):
            checked = c.check(rows, False)
        self.assertEqual([r["check_status"] for r in checked], ["found", "found"])
        self.assertEqual([r["link_check_status"] for r in checked], ["found", ""])


class ValidateTest(unittest.TestCase):
    def site(self, **values):
        row = {"site_id": "MYS-0001", "status": "operational"}
        row.update(values)
        return row

    def test_unknown_role_is_an_error(self):
        with self.assertRaises(ValueError):
            c.validate([self.site()], [{"site_id": "MYS-0001", "role": "landlord"}])

    def test_role_for_unknown_site_is_an_error(self):
        with self.assertRaises(ValueError):
            c.validate([self.site()], [{"site_id": "FIN-0001", "role": "tenant"}])

    def test_duplicate_site_is_an_error(self):
        with self.assertRaises(ValueError):
            c.validate([self.site(), self.site()], [])

    def test_valid_rows_pass(self):
        c.validate([self.site(status="planned")], [{"site_id": "MYS-0001", "role": "equipment supplier"}])


if __name__ == "__main__":
    unittest.main()
