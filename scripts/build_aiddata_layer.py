#!/usr/bin/env python3
"""Build the layer of government data centres financed by Chinese state lenders and agencies.

The source is AidData's Global Chinese Development Finance Dataset, Version 3.0, which is not
committed because AidData distributes the file itself. The coding of each record is in
config/aiddata_coding.csv, written by a person after reading the record, and a record that
matched a search term by chance is coded excluded with the reason. The script joins the coding
to the AidData records, writes data/government_data_centres_aiddata.csv and
data/aiddata_summary.json, and prints the figures in the summary. With --candidates it also lists
the records that mention a data centre or a related term and are not coded yet, so that a person
can read and code them.

    python scripts/build_aiddata_layer.py --gcdf path/to/AidDatasGlobalChineseDevelopmentFinanceDataset_v3.0.xlsx
    python scripts/build_aiddata_layer.py --gcdf ... --candidates    also writes data/aiddata_candidates.csv
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
CODING_CSV = ROOT / "config" / "aiddata_coding.csv"
LAYER_CSV = ROOT / "data" / "government_data_centres_aiddata.csv"
SUMMARY_JSON = ROOT / "data" / "aiddata_summary.json"
CANDIDATES_CSV = ROOT / "data" / "aiddata_candidates.csv"
DEFAULT_GCDF = ROOT / "data" / "raw" / "AidDatasGlobalChineseDevelopmentFinanceDataset_v3.0.xlsx"
SHEET = "GCDF_3.0"
PROJECT_URL = "https://china.aiddata.org/projects/"

CODINGS = {"primary", "component", "scientific", "building", "excluded"}
GOVERNMENT = {"primary", "component"}

# Terms that name a data centre, searched in the title and description of every record.
DATA_CENTRE = re.compile(
    r"data[\s\-]?cent(?:er|re)s?|datacent(?:er|re)s?|internet data cent|cloud comput|cloud data|cloud platform"
    r"|government cloud|national cloud|disaster recovery cent|server room|data processing cent|data storage cent",
    re.I)
# Wider terms for projects that may hold a data centre without naming one.
RELATED = re.compile(r"e-?govern|computing cent|supercomput|high[\s\-]performance comput|safe city|smart city"
                     r"|big data|identity card|biometric", re.I)

COLUMNS = {
    "AidData Record ID": "aiddata_id",
    "coding": "coding",
    "note": "note",
    "Recipient": "country",
    "Recipient ISO-3": "country_iso3",
    "Recipient Region": "region",
    "Commitment Year": "commitment_year",
    "Status": "status",
    "Recommended For Aggregates": "recommended_for_aggregates",
    "Flow Type Simplified": "flow_type",
    "Funding Agencies": "funder",
    "Implementing Agencies": "implementers",
    "Amount (Nominal USD)": "amount_usd_nominal",
    "Amount (Constant USD 2021)": "amount_usd_2021",
    "Interest Rate": "interest_rate",
    "Grace Period": "grace_years",
    "Maturity": "maturity_years",
    "First Loan Repayment Date": "first_principal_repayment",
    "Financial Distress": "financial_distress",
    "Title": "title",
}


def read_coding(path: Path = CODING_CSV) -> pd.DataFrame:
    coding = pd.read_csv(path, dtype={"aiddata_id": int})
    unknown = set(coding["coding"]) - CODINGS
    if unknown:
        raise ValueError(f"Unknown coding values in {path.name}: {sorted(unknown)}")
    if coding["aiddata_id"].duplicated().any():
        raise ValueError(f"Duplicate AidData IDs in {path.name}")
    return coding


def read_gcdf(path: Path) -> pd.DataFrame:
    return pd.read_excel(path, sheet_name=SHEET, engine="openpyxl")


def build_layer(gcdf: pd.DataFrame, coding: pd.DataFrame) -> pd.DataFrame:
    coding = coding[coding["coding"] != "excluded"]
    merged = coding.merge(gcdf, left_on="aiddata_id", right_on="AidData Record ID", how="left", indicator=True)
    missing = merged.loc[merged["_merge"] == "left_only", "aiddata_id"].tolist()
    if missing:
        raise ValueError(f"Coded IDs not found in the AidData file: {missing}")
    layer = merged[list(COLUMNS)].rename(columns=COLUMNS)
    layer["first_principal_repayment"] = pd.to_datetime(layer["first_principal_repayment"]).dt.date
    layer["aiddata_url"] = PROJECT_URL + layer["aiddata_id"].astype(str)
    return layer.sort_values(["coding", "country", "commitment_year", "aiddata_id"]).reset_index(drop=True)


def summarise(layer: pd.DataFrame) -> dict:
    """Figures for the government records that AidData recommends for aggregates."""
    gov = layer[layer["coding"].isin(GOVERNMENT) & (layer["recommended_for_aggregates"] == "Yes")]
    loans = gov[gov["flow_type"] == "Loan"]
    huawei = gov["implementers"].fillna("").str.contains("Huawei")
    repayment_year = pd.to_datetime(loans["first_principal_repayment"]).dt.year
    return {
        "government_records": int(len(gov)),
        "government_records_not_in_totals": int((layer["coding"].isin(GOVERNMENT)
                                                 & (layer["recommended_for_aggregates"] != "Yes")).sum()),
        "countries": int(gov["country"].nunique()),
        "countries_by_region": {k: int(v) for k, v in gov.groupby("region")["country"].nunique().items()},
        "commitment_years": [int(gov["commitment_year"].min()), int(gov["commitment_year"].max())],
        "amount_usd_nominal": round(float(gov["amount_usd_nominal"].sum())),
        "amount_usd_2021": round(float(gov["amount_usd_2021"].sum())),
        "loans": int(len(loans)),
        "grants": int((gov["flow_type"] == "Grant").sum()),
        "china_eximbank_records": int(gov["funder"].str.contains("Eximbank", na=False).sum()),
        "huawei_records": int(huawei.sum()),
        "huawei_countries": int(gov.loc[huawei, "country"].nunique()),
        "primary_purpose_records": int((gov["coding"] == "primary").sum()),
        "financial_distress_records": int((gov["financial_distress"] == "Yes").sum()),
        "loans_first_principal_repayment_2024_2027": int(repayment_year.between(2024, 2027).sum()),
        "scientific_records": int((layer["coding"] == "scientific").sum()),
        "building_records": int((layer["coding"] == "building").sum()),
    }


def candidates(gcdf: pd.DataFrame, coding: pd.DataFrame) -> pd.DataFrame:
    """Records that mention a data centre or a related term and are not coded yet."""
    text = gcdf["Title"].fillna("") + " " + gcdf["Description"].fillna("")
    hit = text.str.contains(DATA_CENTRE) | text.str.contains(RELATED)
    out = gcdf[hit & ~gcdf["AidData Record ID"].isin(coding["aiddata_id"])]
    out = out.assign(names_data_centre=text[out.index].str.contains(DATA_CENTRE))
    return out[["AidData Record ID", "Recipient", "Commitment Year", "Status", "names_data_centre", "Title"]]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--gcdf", type=Path, default=DEFAULT_GCDF, help="path to the AidData GCDF 3.0 Excel file")
    parser.add_argument("--candidates", action="store_true", help="also list records not coded yet")
    args = parser.parse_args()

    gcdf = read_gcdf(args.gcdf)
    coding = read_coding()
    layer = build_layer(gcdf, coding)
    LAYER_CSV.parent.mkdir(parents=True, exist_ok=True)
    layer.to_csv(LAYER_CSV, index=False)
    summary = summarise(layer)
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2) + "\n")
    print(f"Wrote {len(layer)} records to {LAYER_CSV.relative_to(ROOT)}")
    for key, value in summary.items():
        print(f"  {key}: {value}")
    if args.candidates:
        cand = candidates(gcdf, coding)
        cand.to_csv(CANDIDATES_CSV, index=False)
        print(f"Wrote {len(cand)} uncoded candidates to {CANDIDATES_CSV.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
