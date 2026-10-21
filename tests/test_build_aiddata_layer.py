"""Offline tests of the government data centre layer, on small tables written here."""

import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import build_aiddata_layer as b  # noqa: E402


def gcdf_row(record_id, **values):
    row = {column: None for column in b.COLUMNS if column not in ("coding", "note")}
    row.update({"AidData Record ID": record_id, "Recipient": "Kenya", "Recipient ISO-3": "KEN",
                "Recipient Region": "Africa", "Commitment Year": 2019, "Status": "Implementation",
                "Recommended For Aggregates": "Yes", "Flow Type Simplified": "Loan",
                "Funding Agencies": "Export-Import Bank of China (China Eximbank)",
                "Implementing Agencies": "Huawei Technologies Co., Ltd.", "Amount (Nominal USD)": 100.0,
                "Amount (Constant USD 2021)": 110.0, "First Loan Repayment Date": "2026-04-25",
                "Title": "Loan for a data centre", "Description": "This project built a data centre."})
    row.update(values)
    return row


class BuildLayerTest(unittest.TestCase):
    def setUp(self):
        self.gcdf = pd.DataFrame([
            gcdf_row(1),
            gcdf_row(2, **{"Recipient": "Fiji", "Recipient Region": "Oceania", "Flow Type Simplified": "Grant",
                           "Implementing Agencies": "Alcatel-Lucent Shanghai Bell Co., Ltd.",
                           "First Loan Repayment Date": None}),
            gcdf_row(3, **{"Recommended For Aggregates": "No", "Status": "Pipeline: Pledge"}),
            gcdf_row(4, **{"Description": "A submarine cable that ends at a data center in Marseille."}),
            gcdf_row(5, **{"Title": "E-Government Project", "Description": "Fibre for ministries."}),
        ])
        self.coding = pd.DataFrame({"aiddata_id": [1, 2, 3, 4],
                                    "coding": ["primary", "component", "component", "excluded"],
                                    "note": ["a", "b", "c", "cable"]})

    def test_excluded_records_are_left_out(self):
        layer = b.build_layer(self.gcdf, self.coding)
        self.assertEqual(sorted(layer["aiddata_id"]), [1, 2, 3])
        self.assertTrue(layer["aiddata_url"].str.startswith(b.PROJECT_URL).all())

    def test_summary_counts_only_records_for_aggregates(self):
        summary = b.summarise(b.build_layer(self.gcdf, self.coding))
        self.assertEqual(summary["government_records"], 2)
        self.assertEqual(summary["government_records_not_in_totals"], 1)
        self.assertEqual(summary["countries"], 2)
        self.assertEqual(summary["amount_usd_nominal"], 200)
        self.assertEqual(summary["loans"], 1)
        self.assertEqual(summary["grants"], 1)
        self.assertEqual(summary["huawei_records"], 1)
        self.assertEqual(summary["primary_purpose_records"], 1)
        self.assertEqual(summary["loans_first_principal_repayment_2024_2027"], 1)

    def test_coded_id_missing_from_file_is_an_error(self):
        coding = pd.concat([self.coding, pd.DataFrame({"aiddata_id": [99], "coding": ["component"], "note": ["x"]})])
        with self.assertRaises(ValueError):
            b.build_layer(self.gcdf, coding)

    def test_candidates_skip_coded_records(self):
        found = b.candidates(self.gcdf, self.coding)
        self.assertEqual(found["AidData Record ID"].tolist(), [5])
        self.assertFalse(found["names_data_centre"].iloc[0])

    def test_unknown_coding_value_is_an_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "coding.csv"
            path.write_text("aiddata_id,coding,note\n1,maybe,x\n")
            with self.assertRaises(ValueError):
                b.read_coding(path)


if __name__ == "__main__":
    unittest.main()
