# Overseas data centres of Chinese firms

This project records the data-centre capacity outside mainland China in which Chinese firms and Chinese state lenders have a role, as owner, operator, tenant, builder, equipment supplier or financier. For each site the dataset will record how much of the capacity can run large AI workloads and which country's rules cover it. US export controls govern shipments of AI chips but not the remote use of those chips, and the Remote Access Security Act, which would add remote use, passed the House on 12 January 2026 and has not passed the Senate. Capacity that Chinese firms use in third countries can therefore sit outside the rules of the United States, of China and of the host country at once, and no open dataset records that capacity site by site together with the role of each Chinese firm and the rules that cover the site. The database of AI data centres of Epoch AI estimates the IT power of 4 of the sites in this dataset, as the section on Epoch's estimates below sets out. The codebook in `codebook.md` defines the roles, the firms covered, the three levels of detail and every variable.

## Status

The repository holds three layers as of 22 October 2026: the government data centres financed by Chinese state lenders and agencies, the public cloud regions of Chinese providers, and the first sites in which Chinese firms hold a role, with the estimates of Epoch AI for the sites that its database also holds. Every row of the cloud region and site layers carries a passage of its source page, and a script checks the passage against the downloaded page. The rows of the AidData layer come from AidData's own dataset file.

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

`data/sites.csv` holds 63 sites in 17 countries and territories, and `data/site_roles.csv` holds 85 roles of ByteDance, DayOne, China Mobile International, China Unicom Global, Global Switch, Huanbang (Hong Kong), zData, Alibaba Cloud, Huawei Cloud, Tencent Cloud, INF Tech, Megaspeed and Moonshot AI at those sites. All 148 passages were found on their pages. The sites are a first sample for testing the method, not a complete list.

ByteDance holds a role at 13 sites. It is a tenant at 6 of them: the Nvidia Blackwell cluster that Aolani Cloud plans in Malaysia, the 110 MW MY06 campus in Johor, the 90 MW OSL-Hamar campus of Green Mountain in Norway, the Pecém campus in Ceará, which has 300 MW of installed power and 200 MW of planned capacity and is expected to operate by late 2027, the Glomfjord data centre of Nscale in Norway, where its Singapore subsidiary Spring (SG) rents 2,304 Nvidia B200 chips, and the Johor data centre that zData plans on 38 acres, where Alibaba and Tencent are also named as clients. At the other 7 the sources say that TikTok uses or plans the site but not whether it owns or rents it, so the role is coded user. These are Kouvola and Lahti in Finland, two sites in Ireland, the second of which TikTok planned in 2023 with a third-party service and which no source found confirms as open, and Bangkok, Samut Prakan and Chachoengsao in Thailand, where Thailand's Board of Investment approved in May 2026 an investment of about 842 billion baht by TikTok's Thai unit.

DayOne, which began as the international unit of GDS, holds a role at 16 sites, 12 of them named in its 2026 registration statement at the SEC. DayOne reports capacity by market and not by site, so the capacity of a DayOne site comes from other sources where one gives it: 15 MW of IT capacity in the first phase at Kodaira in Tokyo, which broke ground in September 2026, and 42 MW for the campus, 40 MW at Fuchu, 72 MW of IT load at Nongsa Digital Park in Batam, 20 MW in Singapore, 300 MW planned at Escatrón near Zaragoza, and a first building of 50 MW of a campus of 128 MW in the Kiveriö district of Lahti, where building began in 2026. TikTok places its second Finnish data centre in the same district, but no source found confirms that it is DayOne's campus. Oracle is reported to lease the Nongsa plots, with at least 120 MW of power, as sole tenant. China Mobile International operates a data centre of more than 2,100 racks in Singapore, and Uptime Institute lists Tier awards for its sites in Slough, Mörfelden and Hong Kong. China Unicom Global operates a data centre of 37,000 square metres in Tseung Kwan O and was reported in 2023 to be rolling out data centres in Singapore, Tokyo and Frankfurt. Global Switch, which a consortium of Chinese companies including Jiangsu Shagang Group has controlled since 2018, lists in its annual report for 2025 12 completed data centres in Amsterdam, Frankfurt, Hong Kong, London, Madrid, Paris and Singapore and 4 under development in Frankfurt, London, Madrid and Johor. Its website also lists a new site in Bangkok, which the annual report does not include. The same report states that Shagang holds an indirect stake of 51.8 percent in Global Switch and that the directors consider Shagang to control the group. A subsidiary of Shagang, Huanbang (Hong Kong), has held a service agreement for 15 MW in the Hong Kong data centre since 1 January 2023, with a term until 31 December 2027, and the report does not say who uses that capacity. Global Switch is coded as owner and operator of each building, with the ownership from the annual report and the location from the page of each city.

Alibaba Cloud operates five data centres in Malaysia, two of them in the Johor region that opened in June 2026, and holds an undisclosed share of the Saudi Cloud Computing Company, a joint venture with stc and other Saudi partners that opened two data centres in Riyadh in 2022. Huawei Cloud leases its Johannesburg data centre from a partner that the source does not name, and announced a third data centre in Bangkok in 2021. Tencent Cloud has two data centres in Jakarta and plans a third in Indonesia as part of an investment of US$500 million by 2030.

An earlier version also listed Bridge Data Centres, the operator of MY06, as a Chinese operator, which was wrong. Bain Capital separated Bridge from ChinData and kept it when it sold ChinData in September 2025, so the codebook now explains why Bridge is not a listed firm.

### DayOne by market

DayOne's registration statement at the SEC, which DayOne filed for its listing in 2026, reports its capacity by market as of 20 September 2026 and not by site. `data/operator_markets.csv` records the 10 markets: 962 MW in service, 1,328 MW under construction and 2,308 MW of secured powered land, or 4,597 MW in all, in Malaysia, Indonesia, Singapore, Thailand, Japan, Hong Kong, Finland and Spain. Johor holds 789 MW of the 962 MW in service. The rows add up to 1 MW more or less than the totals in the filing, because the filing rounds each figure. The same filing states that GDS holds 19.4 percent of DayOne's shares, which `data/firm_links.csv` records together with the former link between Bridge Data Centres and ChinData, three sources on the control of Global Switch by Jiangsu Shagang Group, the latest its annual report for 2025, and the origin of Megaspeed in a Chinese gaming firm. All 16 passages were found on their pages.

### Customers of operators

Operators seldom name their customers, but their filings show how much of their revenue comes from Chinese firms. `data/operator_customers.csv` records 6 such statements, and all 6 passages were found on their pages. DayOne's registration statement does not name its largest customer but describes it as a global technology company with a leading short-form video platform serving a worldwide audience, and that customer provided 69.4 percent of DayOne's revenue in 2025 and 69.2 percent in the first half of 2026. Bloomberg reported in July 2025 that ByteDance is DayOne's largest customer. Nscale's registration statement states that its largest customer provided 73 percent of its revenue in 2025, and Tom's Hardware, citing the Financial Times, reports that this customer was Spring (SG), a subsidiary of ByteDance, with US$24 million of Nscale's US$33 million. Global Switch recognised £28.4 million of revenue in 2025 under its agreement with Huanbang (Hong Kong), a subsidiary of its controlling shareholder.

### AI chips

`data/ai_compute.csv` records the reports of AI chips that Chinese firms reach outside China, which are the evidence of AI workloads that level B needs, and all 7 passages were found on their pages. In 6 of the 7 reports a Chinese firm reaches US chips that sit outside China, and the seventh does not disclose the model of chip. In 6 of the 7 the firm rents the use of the chips from a firm that holds them, and the sources of 2 of the reports do not name the site.

1. ByteDance is set to reach about 36,000 Nvidia B200 chips in 500 GB200 NVL72 systems that the cloud operator Aolani Cloud deploys in Malaysia, valued at more than US$2.5 billion, as the Wall Street Journal reported in March 2026 from unnamed sources.
2. INF Tech, a Shanghai start-up, reached about 2,300 Nvidia Blackwell chips in 32 GB200 racks that the Indonesian telecom firm Indosat bought and operates in Jakarta, as the Wall Street Journal reported in November 2025.
3. Spring (SG), a Singapore subsidiary of ByteDance, rents 2,304 Nvidia B200 chips at the Glomfjord data centre of Nscale in Norway under a cloud services agreement of 15 May 2025. The loan agreement that Nscale filed with its registration statement at the SEC in September 2026 gives the number of chips and names Spring (SG) as the customer, and Tom's Hardware, citing the Financial Times, identifies Spring (SG) as a subsidiary of ByteDance.
4. Megaspeed, a Singapore firm spun off from a Chinese gaming firm in 2023, bought through its Malaysian unit Nvidia chips worth nearly US$2 billion that were shipped to data centres in Malaysia and Indonesia and appeared to serve Chinese clients remotely. The US is investigating it, and Bridge Data Centres removed Megaspeed from its Malaysian hub in April 2026.
5. A White House official accused Moonshot AI in 2026 of reaching Nvidia chips remotely through an unnamed party in Thailand, an accusation for which the source reports no public evidence.
6. Tencent leases about 100,000 advanced AI chips at several Oracle data centres in Southeast Asia for five years, in a deal worth about US$7 billion, as the Financial Times reported in October 2026. The companies have not confirmed the deal, and the countries, sites and models of chip are not disclosed.
7. Tencent holds contracts worth more than US$1.2 billion for Blackwell chips of the Japanese firm Datasection in Japan and Australia, as the Financial Times reported in December 2025. Datasection has not confirmed that Tencent is its customer.

### Estimates of Epoch AI

Epoch AI's database of AI data centres, read on 22 October 2026, holds 95 data centres, 77 of them in the United States and 5 in mainland China. 4 of the other 13 are sites in this dataset, and `data/epoch_estimates.csv` holds Epoch's estimates for them, read from Epoch's database file. Epoch estimates 473 MW of IT power at DayOne's Nusajaya Tech Park campus and 422 MW at its Kempas Tech Park campus in Johor, and names no owner or user of the chips at either. It estimates 243 MW at MY06, where it judges ByteDance the likely owner and user of the chips, and 72 MW at the campus in Batam that it names after Oracle, where it judges Oracle the likely owner of the chips and Tencent a possible user. Epoch names the Batam campus after its tenant, so the match to DayOne's Nongsa Digital Park campus rests on Epoch's own sources, which place it at DayOne's campus, and on the three buildings of 72 MW that both describe. Epoch's database does not record the role of each Chinese firm or the rules that cover a site, which this dataset adds. The estimates are Epoch's models and are kept apart from the statements of capacity in `data/site_capacity.csv`.

### Rules in the host countries

`data/rules.csv` records 14 parts of rules, bills, guidance, reviews and prosecutions that bear on the AI chips in a host country or on remote access to them, each with its passage and the countries where it applies, and all 14 passages were found on their pages. US export rules control shipments of advanced chips but not access to the chips through a cloud service. The Remote Access Security Act, which would cover such access, passed the House by 369 votes to 22 on 12 January 2026 and has not passed the Senate. The AI Diffusion Rule, issued on 15 January 2025, was rescinded in May 2025 before it took effect, and the notice of rescission announced licensing requirements for exports of advanced chips to Malaysia and Thailand. Commerce later shelved the draft rule on Malaysia and Thailand, as reported in August 2026. BIS guidance of 31 May 2026 states that a licence is needed for advanced chips sent to any entity whose ultimate parent is in China or Macau, wherever the entity is, and in August 2026 the enforcement arm of BIS began a review that lists the countries where Chinese firms reach the chips remotely, which remains legal. Malaysia has required a permit since July 2025 for exports, transshipments and transits of US-origin AI chips, but the permit does not cover the use of the chips within Malaysia. Malaysia's trade ministry also stated in June 2025 that servers with Nvidia and other AI chips are not controlled goods in Malaysia and that data centres may decide whom to serve within Malaysian law. Singapore has acted through prosecutions for fraud on server suppliers about the end users of the servers, under general law, and no rule on AI chips in Singapore was found. A Chinese firm that rents servers in Johor and trains a model on them therefore falls under none of these rules, as the sources stand. In the Gulf, the US approved in November 2025 exports of up to the equivalent of 35,000 Nvidia GB300 chips each to G42 in the United Arab Emirates and Humain in Saudi Arabia, on condition of security and reporting requirements that are not public, and the UAE describes a Regulated Technology Environment of audits and oversight for organisations that acquire such chips.

### Figures

The script `scripts/summarise.py` counts the checked rows of the compute layer and writes `data/summary.json`, so that every figure in the text above can be reproduced. Of the 63 sites, 29 are operational, 8 are under construction, 19 are planned and 7 are unclear, and Malaysia holds 12 of them, more than any other country. Of the 85 roles, 42 are operator, 22 owner, 13 tenant and 8 user. 18 of the 63 sites are coded at level B, 13 of them for an announced capacity of at least 20 MW and 5 for a report of AI chips. DayOne's two campuses in Johor stay at level A only because DayOne reports the capacity of Johor as a whole, and Epoch AI estimates 473 MW and 422 MW of IT power for them. Only 8 sites have a capacity of their own in the sources that support them, 270 MW of IT capacity, 460 MW of power and 310 MW whose basis the sources do not give, and `data/site_capacity.csv` holds a further 15 statements of capacity at several stages, so most of the capacity recorded so far is the 4,597 MW that DayOne reports by market.

### Next steps

1. Add the remaining sites of ByteDance, the portfolios of VNET and zData outside mainland China, and the capacity of each building of Global Switch. The sources found so far show China Telecom Global only through points of presence in third-party data centres, which the codebook does not record as roles, and through an agreement of 2017 for access to the data centres of Global Switch.
2. Add the capacity of each DayOne site where another source gives it, such as a permit or a power purchase agreement, to `data/site_capacity.csv`, which holds 15 statements so far, all of whose passages were found on their pages.
3. Find out from other sources whether the 12 e-government and network projects coded unspecified built a data centre.
4. Link each cloud region to its buildings, and begin level C with satellite imagery, permits and power allocations for the largest level B sites in Johor, Batam and Bangkok.
5. Add the rules of the other host countries, such as Singapore, Thailand, Indonesia, Brazil and the members of the European Union.
6. Identify the Oracle data centres in Southeast Asia at which Tencent is reported to lease chips, and the sites of Datasection in Japan and Australia that serve its largest customer.
7. Match further sites to Epoch AI's database as it grows, and compare its estimates with the statements of capacity in `data/site_capacity.csv`.

## Dashboard

The dashboard is published at [https://newlivehung123123.github.io/overseas_data_centres_China/](https://newlivehung123123.github.io/overseas_data_centres_China/). The folder `site` holds it as a static page in HTML, CSS and JavaScript with no build step. It shows the sites and the cloud regions on a map and in a table, with filters by firm, role and country and a search box, and each row shows the cited passage and the result of its check. A section lists the rules recorded in `data/rules.csv`, and the point of each city lists the rules recorded for its country. Each point marks the centre of the city that the source names, from OpenStreetMap, because most sources name the city and not the building. The government data centres of the AidData layer are left out of the dashboard until the article pitched on them has been answered.

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

The estimates of Epoch AI need no download by hand either. The script downloads Epoch's database file, saves it in `data/raw/epoch`, and writes `data/epoch_estimates.csv` for the sites matched in `config/epoch_links.csv`.

```bash
.venv/bin/python scripts/fetch_epoch.py
```

The cloud region layer needs no download by hand. The script downloads each provider page, saves the page with its text in `data/raw/pages`, which is not committed, and writes `data/cloud_regions.csv`. The option `--offline` reads the saved pages instead.

```bash
.venv/bin/python scripts/fetch_cloud_regions.py
```

The site layer is written by hand in `config/sites.csv` and `config/site_roles.csv`, and the check downloads each cited page, reads the text of PDF files such as annual reports with pypdf, saves the text in `data/raw/pages/sources` and writes `data/sites.csv` and `data/site_roles.csv` with the result for each row.

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
| `config/ai_compute.csv` | Reports of AI chips at sites, each with its page and passage |
| `config/site_capacity.csv` | Statements of capacity at sites, each with its page and passage |
| `config/operator_customers.csv` | Statements of how much operators depend on Chinese customers, each with its page and passage |
| `config/epoch_links.csv` | Sites that Epoch AI's database also holds, each with the passage of the Epoch page that supports the match |
| `config/cloud_regions_manual.csv` | Regions that the provider pages do not list, each with the page that reports it |
| `config/aiddata_coding.csv` | Coding of each AidData record read, with a note on the data centre or the reason for exclusion |
| `data/ai_compute.csv` | Reports of AI chips with the result of the check |
| `data/aiddata_candidates.csv` | AidData records that match a related term and are not coded yet |
| `data/aiddata_summary.json` | Figures of the government data centre layer |
| `data/cloud_regions.csv` | Public cloud regions of Chinese providers outside mainland China |
| `data/epoch_estimates.csv` | Estimates of Epoch AI for the matched sites, read from Epoch's database file |
| `data/epoch_links.csv` | Matches to Epoch AI's database with the result of the check |
| `data/firm_links.csv` | Ownership links with the result of the check |
| `data/operator_customers.csv` | Customers of operators with the result of the check |
| `data/operator_markets.csv` | Capacity by market with the result of the check |
| `data/rules.csv` | Rules with the result of the check |
| `data/summary.json` | Figures of the compute layer |
| `data/site_capacity.csv` | Statements of capacity with the result of the check |
| `data/site_roles.csv` | Roles with the result of the check |
| `data/sites.csv` | Sites with the result of the check |
| `data/government_data_centres_aiddata.csv` | AidData records coded as data centres or computing centres |
| `scripts/build_aiddata_layer.py` | Build of the government data centre layer from the AidData file and the coding |
| `scripts/build_site_data.py` | Build of the dashboard data from the checked layers |
| `scripts/check_sources.py` | Check that each passage of the site layer is on its page |
| `scripts/summarise.py` | Figures of the compute layer, written to `data/summary.json` |
| `scripts/fetch_cloud_regions.py` | Download of the provider region pages and build of the cloud region layer |
| `scripts/fetch_epoch.py` | Download of Epoch AI's database file and the estimates for the matched sites |
| `site/` | Dashboard, with its data in `site/data/dashboard.json` |
| `scripts/geocode_places.py` | Map point of each city from OpenStreetMap |
| `tests/test_build_aiddata_layer.py` | Offline tests of the AidData build |
| `tests/test_check_sources.py` | Offline tests of the passage check |
| `tests/test_fetch_cloud_regions.py` | Offline tests of the region parsers and of the reading of PDF files |
| `tests/test_fetch_epoch.py` | Offline tests of the reading of Epoch AI's database file |
| `tests/test_build_site_data.py` | Offline tests of the dashboard data |

## Licence and attribution

The code is under the MIT licence in `LICENSE`. The data files are under the Creative Commons Attribution 4.0 licence. The government data centre layer is derived from AidData's Global Chinese Development Finance Dataset, Version 3.0, which AidData publishes under the Open Data Commons Attribution License. AidData asks that the dataset be cited as both of the works below.

Custer, S., Dreher, A., Elston, T.B., Escobar, B., Fedorochko, R., Fuchs, A., Ghose, S., Lin, J., Malik, A., Parks, B.C., Solomon, K., Strange, A., Tierney, M.J., Vlasto, L., Walsh, K., Wang, F., Zaleski, L., and Zhang, S. 2023. Tracking Chinese Development Finance: An Application of AidData's TUFF 3.0 Methodology. Williamsburg, VA: AidData at William & Mary.

Dreher, A., Fuchs, A., Parks, B. C., Strange, A., & Tierney, M.J. 2022. Banking on Beijing: The Aims and Impacts of China's Overseas Development Program. Cambridge, UK: Cambridge University Press.

The estimates in `data/epoch_estimates.csv` come from Epoch AI's database of AI data centres, which Epoch AI publishes under the Creative Commons Attribution 4.0 licence and asks to be cited as below.

Epoch AI, 'AI data centers'. Published online at epoch.ai. Retrieved from 'https://epoch.ai/data/ai-data-centers' [online resource]. Accessed 22 October 2026.
