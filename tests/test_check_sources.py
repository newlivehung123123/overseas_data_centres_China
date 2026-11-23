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


class CensusTest(unittest.TestCase):
    def test_a_facility_needs_a_market_and_a_known_code_of_the_chinese_link(self):
        c.validate_census("batam_census", [{"market": "Batam", "chinese_link": "none_found"}])
        with self.assertRaises(ValueError):
            c.validate_census("batam_census", [{"market": "Batam", "chinese_link": ""}])
        with self.assertRaises(ValueError):
            c.validate_census("batam_census", [{"market": "", "chinese_link": "operator"}])


class EvidenceTest(unittest.TestCase):
    def test_known_grades_pass(self):
        c.validate_evidence("sites", [{"evidence": "primary"}, {"evidence": "unconfirmed", "link_source_url": "",
                                                                   "link_evidence": ""}])

    def test_unknown_grade_is_an_error(self):
        with self.assertRaises(ValueError):
            c.validate_evidence("sites", [{"evidence": "likely"}])

    def test_second_passage_needs_a_grade(self):
        with self.assertRaises(ValueError):
            c.validate_evidence("johor_census", [{"evidence": "secondary", "link_source_url": "https://example.org",
                                                  "link_evidence": ""}])


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


class OnlyNewTest(unittest.TestCase):
    def test_unchanged_row_keeps_its_result_and_is_not_downloaded(self):
        old = [{"source_url": "https://a.example", "source_quote": "a passage", "check_status": "found",
                "share_found": "1.00", "retrieved": "2026-10-21"}]
        rows = [{"source_url": "https://a.example", "source_quote": "a passage"},
                {"source_url": "https://b.example", "source_quote": "ByteDance System Sdn. Bhd"}]
        with mock.patch.object(c, "page", return_value=(PAGE, "2026-11-23")) as fetched:
            checked = c.check(rows, False, c.earlier_results(old))
        fetched.assert_called_once_with("https://b.example", False)
        self.assertEqual((checked[0]["check_status"], checked[0]["retrieved"]), ("found", "2026-10-21"))
        self.assertEqual((checked[1]["check_status"], checked[1]["retrieved"]), ("found", "2026-11-23"))

    def test_changed_passage_is_checked_again(self):
        old = [{"source_url": "https://a.example", "source_quote": "old words", "check_status": "found",
                "share_found": "1.00", "retrieved": "2026-10-21"}]
        rows = [{"source_url": "https://a.example", "source_quote": "Alibaba Cloud will be the anchor tenant in Batam"}]
        with mock.patch.object(c, "page", return_value=(PAGE, "2026-11-23")):
            checked = c.check(rows, False, c.earlier_results(old))
        self.assertEqual(checked[0]["check_status"], "not_found")


class FinancingTest(unittest.TestCase):
    FIRMS = [{"firm": "Bank of China"}, {"firm": "Industrial Bank"}]
    SITES = [{"site_id": "MYS-0003"}]
    ROLES = [{"site_id": "MYS-0003", "firm": "Bank of China", "role": "financier"}]

    def row(self, **kw):
        base = {"financing_id": "FIN-0001", "lender": "Bank of China", "instrument": "loan", "site_id": "MYS-0003"}
        return {**base, **kw}

    def test_loan_tied_to_a_site_with_a_financier_role_passes(self):
        c.validate_financing([self.row(), self.row(financing_id="FIN-0002", lender="Industrial Bank", site_id="")],
                             self.FIRMS, self.SITES, self.ROLES)

    def test_loan_at_a_site_without_the_role_is_refused(self):
        with self.assertRaises(ValueError):
            c.validate_financing([self.row(lender="Industrial Bank")], self.FIRMS, self.SITES, self.ROLES)

    def test_unknown_lender_instrument_or_site_is_refused(self):
        for bad in (self.row(lender="Unknown Bank", site_id=""), self.row(instrument="bond"), self.row(site_id="MYS-9999")):
            with self.assertRaises(ValueError):
                c.validate_financing([bad], self.FIRMS, self.SITES, self.ROLES)

    def test_repeated_identifier_is_refused(self):
        with self.assertRaises(ValueError):
            c.validate_financing([self.row(), self.row()], self.FIRMS, self.SITES, self.ROLES)


if __name__ == "__main__":
    unittest.main()
