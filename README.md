# Overseas data centres of Chinese firms

This project records the data-centre capacity outside mainland China in which Chinese firms and Chinese state lenders have a role, as owner, operator, tenant, builder, equipment supplier or financier. For each site the dataset will record how much of the capacity can run large AI workloads and which country's rules cover it. US export controls govern shipments of AI chips but not the remote use of those chips, and the Remote Access Security Act, which would add remote use, passed the House on 12 January 2026 and has not passed the Senate. Capacity that Chinese firms use in third countries can therefore sit outside the rules of the United States, of China and of the host country at once, and no open dataset records that capacity site by site. The codebook in `codebook.md` defines the roles, the firms covered, the three levels of detail and every variable.

## Status

The repository holds three layers as of 21 October 2026: the government data centres financed by Chinese state lenders and agencies, the public cloud regions of Chinese providers, and the first sites in which Chinese firms hold a role. Every row of the cloud region and site layers carries a passage of its source page, and a script checks the passage against the downloaded page. The rows of the AidData layer come from AidData's own dataset file.

### Government data centres financed by Chinese state lenders

A search of the title and description of all 20,985 records in AidData's Global Chinese Development Finance Dataset, Version 3.0, found 69 records that name a data centre. A person read each record and coded it, and 17 of the 69 matched by chance, such as the acronym IDC for industrial development corporations. A second search for related terms such as e-government, safe city and supercomputer added 6 records and found 62 more, which were also read. Of those 62, 18 paid for a security or emergency command centre that receives surveillance data, 12 are e-government or network projects whose records do not say whether they built a data centre, and 32 are unrelated, such as debt suspensions, seminars and broadband networks.

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

`data/sites.csv` holds 42 sites in 15 countries and territories, and `data/site_roles.csv` holds 47 roles of ByteDance, DayOne, China Mobile International, China Unicom Global, Global Switch, zData, Alibaba Cloud and Tencent Cloud at those sites. All 89 passages were found on their pages. The sites are a first sample for testing the method, not a complete list.

ByteDance holds a role at 10 sites. It is a tenant at 4 of them: the 110 MW MY06 campus in Johor, the 90 MW OSL-Hamar campus of Green Mountain in Norway, the Pecém campus in Ceará, which has 300 MW of installed power and is expected to operate in 2027, and the Johor data centre that zData plans on 38 acres, where Alibaba and Tencent are also named as clients. At the other 6 the sources say that TikTok uses or plans the site but not whether it owns or rents it, so the role is coded user. These are Kouvola and Lahti in Finland, a site in Ireland, and Bangkok, Samut Prakan and Chachoengsao in Thailand, where Thailand's Board of Investment approved in May 2026 an investment of about 842 billion baht by TikTok's Thai unit.

DayOne, which began as the international unit of GDS, holds a role at 16 sites, 12 of them named in its 2026 registration statement at the SEC. DayOne reports capacity by market and not by site, so most DayOne sites have no capacity of their own. China Mobile International operates a data centre of more than 2,100 racks in Singapore, and Uptime Institute lists Tier awards for its sites in Slough, Mörfelden and Hong Kong. China Unicom Global operates a data centre of 37,000 square metres in Tseung Kwan O and was reported in 2023 to be rolling out data centres in Singapore, Tokyo and Frankfurt. Global Switch, which a consortium of Chinese companies including Jiangsu Shagang Group has controlled since 2018, lists data centres in Amsterdam, Frankfurt, Hong Kong, London, Madrid, Paris and Singapore and new sites in Johor and Bangkok, recorded for now at the level of the city.

An earlier version also listed Bridge Data Centres, the operator of MY06, as a Chinese operator, which was wrong. Bain Capital separated Bridge from ChinData and kept it when it sold ChinData in September 2025, so the codebook now explains why Bridge is not a listed firm.

### DayOne by market

DayOne's registration statement at the SEC, which DayOne filed for its listing in 2026, reports its capacity by market as of 20 September 2026 and not by site. `data/operator_markets.csv` records the 10 markets: 962 MW in service, 1,328 MW under construction and 2,308 MW of secured powered land, or 4,597 MW in all, in Malaysia, Indonesia, Singapore, Thailand, Japan, Hong Kong, Finland and Spain. Johor holds 789 MW of the 962 MW in service. The rows add up to 1 MW more or less than the totals in the filing, because the filing rounds each figure. The same filing states that GDS holds 19.4 percent of DayOne's shares, which `data/firm_links.csv` records together with the former link between Bridge Data Centres and ChinData and two sources on the control of Global Switch by Jiangsu Shagang Group, the later from January 2023. All 14 passages were found on their pages.

### Rules in the host countries

`data/rules.csv` records 7 parts of rules, bills and guidance that bear on the AI chips in a host country or on remote access to them, each with its passage, and all 7 passages were found on their pages. US export rules control shipments of advanced chips but not access to the chips through a cloud service. The Remote Access Security Act, which would cover such access, passed the House by 369 votes to 22 on 12 January 2026 and has not passed the Senate. The AI Diffusion Rule, issued on 15 January 2025, was rescinded in May 2025 before it took effect, and the notice of rescission announced licensing requirements for exports of advanced chips to Malaysia and Thailand. Malaysia has required a permit since July 2025 for exports, transshipments and transits of US-origin AI chips, but the permit does not cover the use of the chips within Malaysia. A Chinese firm that rents servers in Johor and trains a model on them therefore falls under none of these rules, as the sources stand.

### Next steps

1. Add the remaining sites of ByteDance, such as its second site in Ireland, the portfolios of GDS, VNET and zData outside mainland China, the overseas data centres of China Telecom Global, the buildings of Global Switch in each city, and a source dated after January 2023 on who controls Global Switch.
2. Add the capacity of each DayOne site where another source gives it, such as a permit or a power purchase agreement.
3. Find out from other sources whether the 12 e-government and network projects coded unspecified built a data centre.
4. Link each cloud region to its buildings and code level B for sites of at least 20 MW.
5. Add the rules of the other host countries, such as Singapore, Thailand, Indonesia, the United Arab Emirates and Saudi Arabia, and link each site to the rules of its country.

## Dashboard

The dashboard is published at [https://newlivehung123123.github.io/overseas_data_centres_China/](https://newlivehung123123.github.io/overseas_data_centres_China/). The folder `site` holds it as a static page in HTML, CSS and JavaScript with no build step. It shows the sites and the cloud regions on a map and in a table, with filters by firm, role and country and a search box, and each row shows the cited passage and the result of its check. Each point marks the centre of the city that the source names, from OpenStreetMap, because most sources name the city and not the building. The government data centres of the AidData layer are left out of the dashboard until the article pitched on them has been answered.

The dashboard reads `site/data/dashboard.json`, which `scripts/build_site_data.py` writes from the checked layers and `config/places.csv`. The script `scripts/geocode_places.py` finds the point of each new city from the Nominatim service of OpenStreetMap, at most one request a second, and records the OpenStreetMap object behind each point.

```bash
.venv/bin/python scripts/geocode_places.py
.venv/bin/python scripts/build_site_data.py
python3 -m http.server 8731 --directory site
```

The workflow in `.github/workflows/pages.yml` publishes the folder `site` with GitHub Pages on each push to the default branch of the repository, with Pages set to deploy from GitHub Actions in the repository settings.

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
| `config/places.csv` | Map point of each city, with the OpenStreetMap object it comes from |
| `config/rules.csv` | Parts of rules that bear on AI chips in host countries, each with its page and passage |
| `config/site_roles.csv` | Roles of firms at sites, each with its page and passage |
| `config/sites.csv` | Sites, each with its page and passage |
| `config/cloud_regions_manual.csv` | Regions that the provider pages do not list, each with the page that reports it |
| `config/aiddata_coding.csv` | Coding of each AidData record read, with a note on the data centre or the reason for exclusion |
| `data/aiddata_candidates.csv` | AidData records that match a related term and are not coded yet |
| `data/aiddata_summary.json` | Figures of the government data centre layer |
| `data/cloud_regions.csv` | Public cloud regions of Chinese providers outside mainland China |
| `data/firm_links.csv` | Ownership links with the result of the check |
| `data/operator_markets.csv` | Capacity by market with the result of the check |
| `data/rules.csv` | Rules with the result of the check |
| `data/site_roles.csv` | Roles with the result of the check |
| `data/sites.csv` | Sites with the result of the check |
| `data/government_data_centres_aiddata.csv` | AidData records coded as data centres or computing centres |
| `scripts/build_aiddata_layer.py` | Build of the government data centre layer from the AidData file and the coding |
| `scripts/build_site_data.py` | Build of the dashboard data from the checked layers |
| `scripts/check_sources.py` | Check that each passage of the site layer is on its page |
| `scripts/fetch_cloud_regions.py` | Download of the provider region pages and build of the cloud region layer |
| `site/` | Dashboard, with its data in `site/data/dashboard.json` |
| `scripts/geocode_places.py` | Map point of each city from OpenStreetMap |
| `tests/test_build_aiddata_layer.py` | Offline tests of the AidData build |
| `tests/test_check_sources.py` | Offline tests of the passage check |
| `tests/test_fetch_cloud_regions.py` | Offline tests of the region parsers |

## Licence and attribution

The code is under the MIT licence in `LICENSE`. The data files are under the Creative Commons Attribution 4.0 licence. The government data centre layer is derived from AidData's Global Chinese Development Finance Dataset, Version 3.0, which AidData publishes under the Open Data Commons Attribution License. AidData asks that the dataset be cited as both of the works below.

Custer, S., Dreher, A., Elston, T.B., Escobar, B., Fedorochko, R., Fuchs, A., Ghose, S., Lin, J., Malik, A., Parks, B.C., Solomon, K., Strange, A., Tierney, M.J., Vlasto, L., Walsh, K., Wang, F., Zaleski, L., and Zhang, S. 2023. Tracking Chinese Development Finance: An Application of AidData's TUFF 3.0 Methodology. Williamsburg, VA: AidData at William & Mary.

Dreher, A., Fuchs, A., Parks, B. C., Strange, A., & Tierney, M.J. 2022. Banking on Beijing: The Aims and Impacts of China's Overseas Development Program. Cambridge, UK: Cambridge University Press.
