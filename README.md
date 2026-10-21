# Overseas data centres of Chinese firms

This project records the data-centre capacity outside mainland China in which Chinese firms and Chinese state lenders have a role, as owner, operator, tenant, builder, equipment supplier or financier. For each site the dataset will record how much of the capacity can run large AI workloads and which country's rules cover it. US export controls govern shipments of AI chips but not the remote use of those chips, and the Remote Access Security Act, which would add remote use, passed the House on 12 January 2026 and has not passed the Senate. Capacity that Chinese firms use in third countries can therefore sit outside the rules of the United States, of China and of the host country at once, and no open dataset records that capacity site by site. The codebook in `codebook.md` defines the roles, the firms covered, the three levels of detail and every variable.

## Status

The repository holds three layers as of 21 October 2026: the government data centres financed by Chinese state lenders and agencies, the public cloud regions of Chinese providers, and the first sites in which Chinese firms hold a role. Every row of the cloud region and site layers carries a passage of its source page, and a script checks the passage against the downloaded page. The rows of the AidData layer come from AidData's own dataset file.

### Government data centres financed by Chinese state lenders

A search of the title and description of all 20,985 records in AidData's Global Chinese Development Finance Dataset, Version 3.0, found 69 records that name a data centre. A person read each record and coded it, and 17 of the 69 matched by chance, such as the acronym IDC for industrial development corporations. A second search for related terms such as e-government and supercomputer added 6 records, and 62 records that match only the related terms remain to be read.

Of the coded records, 48 paid for a government data centre, 8 for a scientific or high-performance computing centre and 2 for a building that contains a data centre. The figures below use the 45 government records that AidData recommends for totals, which leaves out three pledges.

| Measure | Value |
|---|---|
| Records | 45, of which 39 loans and 6 grants |
| Countries | 23, of which 15 in Africa, 4 in Oceania, 2 in Asia, 1 in the Americas and 1 in Europe |
| Years signed | 2006 to 2020 |
| Amount at the time of signing | $3.50 billion |
| Amount adjusted for inflation to 2021 prices | $4.22 billion |
| Records financed by China Eximbank | 35 |
| Records with Huawei as a contractor | 38, in 21 of the 23 countries |
| Records in which the data centre is the main purpose | 4 |
| Loans that AidData records as in financial distress | 6 |
| Loans whose first repayment of principal falls between 2024 and 2027 | 7 |

The amounts cover the whole project, and in 41 of the 45 records the data centre is one part of a wider e-government, broadband, security or education project. The count is a lower bound, because records that do not describe what was built are not coded and the dataset ends with commitments made in 2021.

### Cloud regions of Chinese providers

`data/cloud_regions.csv` lists 55 regions of Alibaba Cloud, Huawei Cloud, Tencent Cloud and BytePlus. The script read 51 of them from the providers' own region pages on 21 October 2026, and the other 4, three regions that Alibaba Cloud has announced for Finland, the Netherlands and Turkey and a Tencent Cloud region in Toronto that the current Tencent page does not list, come from reports in DatacenterDynamics. All 55 passages were found on their pages.

Of the 55 regions, 47 are operational outside mainland China, Hong Kong and Macau, in 22 countries. Alibaba Cloud, Huawei Cloud and Tencent Cloud account for 45 of the 47, against a count of 43 by WireScreen for the same three providers. The Tencent page lists one region, in Queretaro in Mexico, that an earlier list built from search results had missed. The BytePlus rows come from the documentation of one service and do not cover the other BytePlus services.

### Sites

`data/sites.csv` holds 7 sites in Malaysia, Indonesia, Finland and Brazil, and `data/site_roles.csv` holds 9 roles of ByteDance, DayOne and Bridge Data Centres at those sites. ByteDance is a tenant at 4 sites: the 110 MW MY06 campus of Bridge Data Centres in Johor, the Hyperco campus in Kouvola, a planned site in Lahti and the Pecém campus in Ceará, which has 300 MW of installed power and is expected to operate in 2027. DayOne, which began as the international unit of GDS, holds a role at 4 sites, in Batam, Johor, Kouvola and Lahti. All 16 passages were found on their pages. The sites are a first sample for testing the method, not a complete list.

### DayOne by market

DayOne's registration statement at the SEC, which DayOne filed for its listing in 2026, reports its capacity by market as of 20 September 2026 and not by site. `data/operator_markets.csv` records the 10 markets: 962 MW in service, 1,328 MW under construction and 2,308 MW of secured powered land, or 4,597 MW in all, in Malaysia, Indonesia, Singapore, Thailand, Japan, Hong Kong, Finland and Spain. Johor holds 789 MW of the 962 MW in service. The rows add up to 1 MW more or less than the totals in the filing, because the filing rounds each figure. The same filing states that GDS holds 19.4 percent of DayOne's shares, which `data/firm_links.csv` records. All 11 passages were found in the filing.

### Next steps

1. Add the remaining sites of ByteDance, such as Hamar in Norway and its sites in Ireland and Thailand, the full portfolios of DayOne, Bridge Data Centres, GDS, VNET and zData, and the overseas data centres of the state telecom firms.
2. Link DayOne's markets to its sites, from the site descriptions in the same filing.
3. Read and code the 62 AidData records that match only the related terms.
4. Link each cloud region to its buildings and code level B for sites of at least 20 MW.

## Setup

Python 3.11 or later is needed, with the packages in `requirements.txt`.

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

AidData distributes the GCDF 3.0 file itself, so the file is not committed. Download it from AidData, place the Excel file in `data/raw`, and build the layer.

```bash
.venv/bin/python scripts/build_aiddata_layer.py
.venv/bin/python scripts/build_aiddata_layer.py --candidates
```

The cloud region layer needs no download by hand. The script downloads each provider page, saves the page with its text in `data/raw/pages`, which is not committed, and writes `data/cloud_regions.csv`. The option `--offline` reads the saved pages instead.

```bash
.venv/bin/python scripts/fetch_cloud_regions.py
```

The site layer is written by hand in `config/sites.csv` and `config/site_roles.csv`, and the check downloads each cited page, saves it in `data/raw/pages/sources` and writes `data/sites.csv` and `data/site_roles.csv` with the result for each row.

```bash
SEC_CONTACT_EMAIL=you@example.org .venv/bin/python scripts/check_sources.py
```

The SEC accepts automated requests only with a contact email, so the check reads one from `SEC_CONTACT_EMAIL` and refuses pages on sec.gov without it. The email is sent only to the SEC and is not stored in the repository.

The first command writes `data/government_data_centres_aiddata.csv` and `data/aiddata_summary.json` and prints the figures above. The option `--candidates` also writes `data/aiddata_candidates.csv`, the records that match a search term and are not coded yet. The option `--gcdf` gives another path to the Excel file.

## Tests

The tests use small tables and passages written in the test files and need no download.

```bash
.venv/bin/python -m unittest discover -s tests
```

## Files

| Path | Contents |
|---|---|
| `CONTRIBUTING.md` | Purpose of the project, data rules and writing rules for anyone who works on the repository |
| `codebook.md` | Roles, firms, levels and variables |
| `config/firm_links.csv` | Ownership links between listed firms and Chinese firms, each with its page and passage |
| `config/operator_markets.csv` | Capacity that operators report by market, each with its page and passage |
| `config/site_roles.csv` | Roles of firms at sites, each with its page and passage |
| `config/sites.csv` | Sites, each with its page and passage |
| `config/cloud_regions_manual.csv` | Regions that the provider pages do not list, each with the page that reports it |
| `config/aiddata_coding.csv` | Coding of each AidData record read, with a note on the data centre or the reason for exclusion |
| `data/aiddata_candidates.csv` | AidData records that match a related term and are not coded yet |
| `data/aiddata_summary.json` | Figures of the government data centre layer |
| `data/cloud_regions.csv` | Public cloud regions of Chinese providers outside mainland China |
| `data/firm_links.csv` | Ownership links with the result of the check |
| `data/operator_markets.csv` | Capacity by market with the result of the check |
| `data/site_roles.csv` | Roles with the result of the check |
| `data/sites.csv` | Sites with the result of the check |
| `data/government_data_centres_aiddata.csv` | AidData records coded as data centres or computing centres |
| `scripts/build_aiddata_layer.py` | Build of the government data centre layer from the AidData file and the coding |
| `scripts/check_sources.py` | Check that each passage of the site layer is on its page |
| `scripts/fetch_cloud_regions.py` | Download of the provider region pages and build of the cloud region layer |
| `tests/test_build_aiddata_layer.py` | Offline tests of the AidData build |
| `tests/test_check_sources.py` | Offline tests of the passage check |
| `tests/test_fetch_cloud_regions.py` | Offline tests of the region parsers |

## Licence and attribution

The code is under the MIT licence in `LICENSE`. The data files are under the Creative Commons Attribution 4.0 licence. The government data centre layer is derived from AidData's Global Chinese Development Finance Dataset, Version 3.0, which AidData publishes under the Open Data Commons Attribution License. AidData asks that the dataset be cited as both of the works below.

Custer, S., Dreher, A., Elston, T.B., Escobar, B., Fedorochko, R., Fuchs, A., Ghose, S., Lin, J., Malik, A., Parks, B.C., Solomon, K., Strange, A., Tierney, M.J., Vlasto, L., Walsh, K., Wang, F., Zaleski, L., and Zhang, S. 2023. Tracking Chinese Development Finance: An Application of AidData's TUFF 3.0 Methodology. Williamsburg, VA: AidData at William & Mary.

Dreher, A., Fuchs, A., Parks, B. C., Strange, A., & Tierney, M.J. 2022. Banking on Beijing: The Aims and Impacts of China's Overseas Development Program. Cambridge, UK: Cambridge University Press.
