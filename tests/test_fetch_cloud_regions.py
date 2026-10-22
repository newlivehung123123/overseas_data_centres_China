"""Offline tests of the region parsers, on short passages in the format of each provider page."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import fetch_cloud_regions as f  # noqa: E402

URL = "https://example.org/regions"
DAY = "2026-10-21"


class ParserTest(unittest.TestCase):
    def test_alibaba_keeps_hong_kong_and_drops_mainland(self):
        text = ("Singapore Availability Zone: 4 Released in 2015 Malaysia (Johor) Availability Zone: 3 Released in 2026 "
                "SAU (Riyadh - Partner Region) Availability Zone: 2 Released in 2022 China (Hong Kong) Availability "
                "Zone: 3 Released in 2014 China (Qingdao) Availability Zone: 2 Released in 2012")
        rows = f.parse_alibaba(text, "Alibaba Cloud", URL, DAY)
        self.assertEqual([r["city"] for r in rows], ["Singapore", "Johor", "Riyadh", "Hong Kong"])
        self.assertEqual(rows[1]["launch_year"], "2026")
        self.assertEqual(rows[1]["source_quote"], "Malaysia (Johor) Availability Zone: 3 Released in 2026")
        self.assertEqual(rows[3]["hong_kong_macau"], "yes")

    def test_huawei_list_drops_mainland(self):
        text = ("supported: CN North-Beijing, CN East-Shanghai, CN-Hong Kong, AP-Bangkok, ME-Riyadh, LA-Sao Paulo, "
                "and LA-Lima. Parent topic")
        rows = f.parse_huawei_faq(text, "Huawei Cloud", URL, DAY)
        self.assertEqual([r["region_id"] for r in rows], ["CN-Hong Kong", "AP-Bangkok", "ME-Riyadh", "LA-Sao Paulo", "LA-Lima"])
        self.assertEqual(rows[3]["country_iso3"], "BRA")

    def test_tencent_drops_mainland_and_finance_regions(self):
        text = ("North China (Beijing) ap-beijing 6 Beijing Zone 3 ap-beijing-3 Hong Kong (China), Macao (China), and "
                "Taiwan (China) ap-hongkong 3 Hong Kong Zone 1 Beijing Finance ap-beijing-fsi 2 Zone "
                "Asia Pacific and the Middle East (Johor Bahru) Coverage: Southeast Asia ap-johorbahru 2 Johorbahru "
                "Zone 1 ap-johorbahru-1 Europe and the Americas (Queretaro) Coverage: North America na-queretaro 1 Zone")
        rows = f.parse_tencent(text, "Tencent Cloud", URL, DAY)
        self.assertEqual([r["region_id"] for r in rows], ["ap-hongkong", "ap-johorbahru", "na-queretaro"])
        self.assertEqual(rows[1]["availability_zones"], "2")
        self.assertEqual(rows[2]["country"], "Mexico")

    def test_byteplus_reads_the_exit_ip_table(self):
        text = "Hong Kong 150.5.146.60, 150.5.168.25 Southeast Asia (Johor) 101.47.140.89 Southeast Asia (Jakarta) 163.7.17.61"
        rows = f.parse_byteplus(text, "BytePlus", URL, DAY)
        self.assertEqual([r["city"] for r in rows], ["Hong Kong", "Johor", "Jakarta"])

    def test_fold_ignores_accents_and_case(self):
        self.assertEqual(f.fold("São Paulo"), "sao paulo")
        self.assertEqual(f.place("Querétaro")[2], "MEX")

    def test_page_text_drops_scripts_and_tags(self):
        self.assertEqual(f.page_text("<p>Seoul</p><script>var x = 1;</script> <b>Tokyo</b>"), "Seoul Tokyo")

    def test_pdf_text_reads_the_text_of_a_pdf(self):
        stream = b"BT /F1 12 Tf 72 720 Td (Johor Freehold) Tj ET"
        objects = [b"<< /Type /Catalog /Pages 2 0 R >>", b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
                   b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R "
                   b"/Resources << /Font << /F1 5 0 R >> >> >>",
                   b"<< /Length %d >>\nstream\n%s\nendstream" % (len(stream), stream),
                   b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"]
        pdf, offsets = b"%PDF-1.4\n", []
        for number, body in enumerate(objects, 1):
            offsets.append(len(pdf))
            pdf += b"%d 0 obj\n%s\nendobj\n" % (number, body)
        start = len(pdf)
        pdf += b"xref\n0 6\n0000000000 65535 f \n" + b"".join(b"%010d 00000 n \n" % o for o in offsets)
        pdf += b"trailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % start
        self.assertIn("Johor Freehold", f.pdf_text(pdf))


if __name__ == "__main__":
    unittest.main()
