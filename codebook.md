# Codebook

The dataset records data-centre capacity outside mainland China in which a Chinese firm or a Chinese state lender has a role. A Chinese firm is a firm that meets at least one of three grounds: its headquarters are in mainland China, its controlling owner is in mainland China, or the firm was once part of a firm that met one of the first two grounds at the time. The third ground, origin, covers DayOne, which was a subsidiary of GDS until 31 December 2024, Bitdeer, which was spun off from Bitmain in 2021, and Bridge Data Centres, which was part of ChinData Group, a firm with its headquarters in Beijing, from 2019. `config/firms.csv` records the grounds of every firm with a source, and the capacity estimate is also given without the firms that count on origin alone, so that a user can see how much of the estimate rests on them. Hong Kong and Macau are recorded but marked, so that a user can include or exclude them.

## Roles

A record enters the dataset when a listed firm holds at least one of the roles in Table 1. One site can carry several roles held by different firms, and the dataset records each role with its own source. A point of presence, which holds a carrier's network equipment in another firm's data centre, is not recorded as a role, because it holds no computing capacity. China Telecom Global, for example, appears in the sources found so far mainly through points of presence in third-party data centres.

**Table 1. Roles**

| Role | Definition |
|---|---|
| owner | Holds the land, the building or the company that owns the site |
| operator | Runs the site day to day |
| tenant | Rents space, power or servers in a site that another firm owns or operates, including a cloud region hosted in a third-party building |
| user | Stores data or runs servers at the site, where the source does not say whether the firm owns or rents the site |
| builder | Designed or built the site under contract |
| equipment supplier | Supplied the servers, storage, network or power equipment |
| financier | Lent or granted the money that paid for the site, or invested in the firm that owns the site without a disclosed share |

## Firms

The first version covers the firms in Table 2. A firm is added when a source shows that it holds one of the roles in Table 1 outside mainland China.

**Table 2. Firms**

| Group | Firms |
|---|---|
| Cloud and AI | Alibaba Cloud, Huawei Cloud, Tencent Cloud and Tencent, ByteDance (including BytePlus, Volcano Engine and Spring (SG)), Baidu AI Cloud |
| State telecom | China Mobile International, China Telecom Global, China Unicom Global |
| Data-centre operators | GDS, VNET, zData, ChinData, DayOne (origin in GDS), Bridge Data Centres (origin in ChinData Group), Global Switch (controlled by Jiangsu Shagang Group), Shanghai DC-Science, RangeIDC (Range Intelligent Computing Technology), Beijing Haoyang, Galaxy Data Center (origin in Hoyinn Technologies) |
| Builders and equipment | Huawei, ZTE, Inspur, Sugon |
| Other subsidiaries of Chinese groups | Huanbang (Hong Kong), a subsidiary of Jiangsu Shagang Group |
| AI developers and compute brokers | INF Tech, Moonshot AI, Megaspeed (origin in a Chinese gaming firm), Bitdeer (origin in Bitmain) |
| State lenders | China Eximbank, China Development Bank, the state commercial banks, the Ministry of Commerce and CIDCA, and funds that they sponsor, such as the China-ASEAN Investment Cooperation Fund II |

Bridge Data Centres is a listed firm on the ground of origin. Bain Capital merged ChinData, which had its headquarters in Beijing, and Bridge under the parent ChinData Group in 2019, separated the two after taking ChinData private in 2023, and kept Bridge when it sold ChinData to a Chinese-led consortium in September 2025. Bridge has never had a controlling owner in mainland China, and version 0.1.0 left Bridge out on that ground alone. The same test would leave out DayOne, which also has no controlling owner in mainland China, so version 0.2.0 applies the three grounds above to every firm and counts Bridge by its origin, as it counts DayOne and Bitdeer.

Ownership can change, so each link between a firm and its Chinese owner in `data/firm_links.csv` carries the date of its source. Global Switch has been under the control of a consortium of Chinese companies including Jiangsu Shagang Group since 2018. Its annual report for 2025 states that Shagang holds an indirect stake of 51.8 percent and that the directors consider Shagang to control the group. Global Switch stays a listed firm until a source reports a change of control.

## Levels

Every record is coded at level A. Records with announced capacity of at least 20 MW, or with announced AI chips, are also coded at level B, and the level B sites with the largest capacity are checked at level C. The scripts code level B from the checked rows: a site is at level B when its row in `sites.csv` or a row of `site_capacity.csv` gives at least 20 MW, or when `ai_compute.csv` holds a report of AI chips at the site. The estimates of Epoch AI do not count, because no firm has announced them, and a capacity that an operator reports for a whole market does not count for any one site in it.

**Table 3. Levels**

| Level | Coverage | Variables added |
|---|---|---|
| A | Every record | Firm, role, country, city, status, the source of each value and the grade of evidence of each row |
| B | Capacity of at least 20 MW or announced AI chips | Capacity in MW with a low and a high estimate, chips, power density, cooling, evidence of AI workloads, the rules that cover the site |
| C | Level B sites with the largest capacity | Satellite imagery, permits and power allocations |

Power density and cooling are not recorded for any site yet. The low and the high estimate of capacity come from `scripts/estimate_capacity.py`, which the section on `data/capacity_estimate.csv` below describes.

## Evidence

Every row of the files written by hand in `config`, and every row of `cloud_regions.csv`, carries a grade of the evidence for the row in the variable `evidence`, with one of the three values in Table 4. The grade records who states the value in the source that the row cites, while `check_status` records only whether the passage is on the page. A news report of a filing is therefore graded secondary, because the row cites the report and not the filing. A row of a census carries a second grade, `link_evidence`, for the page that supports the Chinese link.

**Table 4. Grades of evidence**

| Grade | Definition |
|---|---|
| primary | The firm that the row concerns, another firm that holds a role at the site or signed the agreement, such as the builder or the lender, or a public authority states the value in a document that the firm or the authority publishes, such as a filing at the SEC, an annual report, a press release, a website or a notice of a government or a legislature |
| secondary | A third party states the value, such as a news outlet, a commercial directory, an industry body or a research database, and no source found doubts the value |
| unconfirmed | The source rests on people whom the source does not name or reports an accusation without public evidence, or another source doubts the value, or the firms concerned have not confirmed the value |

The low estimate of the capacity estimate counts only figures graded primary, as rule 3 of the section on `data/capacity_estimate.csv` states.

## Files

### data/cloud_regions.csv

One row for each public cloud region that a Chinese provider lists outside mainland China. A region is a service area and can span several buildings, so a region is linked to its buildings at level B. The script `scripts/fetch_cloud_regions.py` reads the operational regions from each provider's own region page and keeps the passage of the page that supports each row. Regions that the provider pages do not list, such as announced regions, come from `config/cloud_regions_manual.csv`, and the script checks each of those rows against the page it cites.

**Table 5. Variables in cloud_regions.csv**

| Variable | Type | Values | Description |
|---|---|---|---|
| provider | text | | Cloud provider as it names itself |
| region_label | text | | Name of the region as the page writes it, such as Malaysia (Johor) or ME-Riyadh |
| region_id | text | | Code of the region where the page gives one, such as ap-johorbahru |
| city | text | | City or area of the region, empty for a planned region with no city announced |
| country | text | | Country in English |
| country_iso3 | text | ISO 3166-1 alpha-3 | Country code |
| status | category | operational, planned, unclear | operational when the provider's region page lists the region, planned when a source reports an announcement, unclear when sources disagree on whether the region exists |
| launch_year | integer | | Year the page gives for the launch, empty when the page gives none |
| availability_zones | integer | | Number of zones the page gives, empty when it gives none |
| hong_kong_macau | category | yes, no | yes for Hong Kong and Macau |
| evidence | category | primary, secondary, unconfirmed | Grade of the evidence for the row, as in Table 4: primary for a region read from the provider's own page, and the grade written in `config/cloud_regions_manual.csv` for the other regions |
| source_url | text | | Page that supports the row |
| source_quote | text | | Passage of the page that supports the row |
| check_status | category | found, not_found, not_read | found when the passage is on the downloaded page, not_found when the page was read and the passage is not on it, not_read when the page could not be downloaded |
| retrieved | date | YYYY-MM-DD | Date the page was downloaded |

### data/sites.csv and data/site_roles.csv

`data/sites.csv` has one row for each site, which is a building or a group of data-centre buildings on one plot of land, and `data/site_roles.csv` has one row for each role that a listed firm holds at a site. A person writes both files in `config/sites.csv` and `config/site_roles.csv`, with the page that supports each row and a passage copied from the page. The script `scripts/check_sources.py` downloads each page and adds the result of the check. A site enters the file only when at least one row of `site_roles.csv` gives a listed firm a role at the site.

**Table 6. Variables in sites.csv**

| Variable | Type | Values | Description |
|---|---|---|---|
| site_id | text | ISO 3166-1 alpha-3 code, a hyphen and four digits | Identifier of the site, assigned once and never reused |
| site_name | text | | Name of the site as the source gives it |
| city | text | | City or area, with the state or province where the source gives one |
| country, country_iso3 | text | | Country and its code |
| status | category | operational, under_construction, planned, unclear | Stage of the site at the date of the source |
| capacity_mw | number | | Capacity in megawatts that the source gives, empty when it gives none |
| capacity_basis | category | it, power, unspecified | it for IT capacity, power for the installed power or the power contracted, unspecified when the source does not say |
| note | text | | Limits of the source, such as a capacity that covers several phases |
| evidence | category | primary, secondary, unconfirmed | Grade of the evidence for the row, as in Table 4 |
| source_url, source_quote | text | | Page that supports the row and the passage copied from it |
| check_status | category | found, partly_found, not_found, not_read | Result of the check, as defined below |
| share_found | number | 0 to 1 | Share of the passage's pieces found on the page |
| retrieved | date | YYYY-MM-DD | Date the page was downloaded |

**Table 7. Variables in site_roles.csv**

| Variable | Type | Values | Description |
|---|---|---|---|
| site_id | text | | Site in `sites.csv` |
| firm | text | | Firm as Table 2 names it |
| firm_origin | text | | Chinese firm from which the firm began, such as GDS for DayOne, empty when the firm is itself Chinese |
| role | category | Table 1 | Role of the firm at the site |
| evidence, source_url, source_quote, check_status, share_found, retrieved | | | As in Table 6 |

A passage counts as found when at least 90 percent of its overlapping pieces of eight characters appear on the page, with spacing, punctuation, accents and case ignored, and as partly found from 50 percent. A role recorded as owner can rest on an investment in the project whose share is not disclosed, and the passage then says so.

### data/operator_markets.csv and data/firm_links.csv

`data/operator_markets.csv` has one row for each market in which an operator in Table 2 reports its capacity, for operators that report by market or for the whole firm and not by site. Global Switch reports one figure for the group, so the row of Global Switch has the market All markets and records in `in_service_mw` the 252 MW of saleable capacity that the annual report for 2025 gives. The report does not say whether saleable capacity includes the data centres under development, and the row records the figure as capacity in service. The basis of each figure comes from the definitions of the operator in `data/capacity_definitions.csv`, which Table 21 describes. `data/firm_links.csv` has one row for each ownership link between a listed firm and a Chinese firm, such as the share of DayOne that GDS holds. Both files are written by hand in `config` and checked by `scripts/check_sources.py` in the same way as `config/sites.csv`.

**Table 8. Variables in operator_markets.csv**

| Variable | Type | Description |
|---|---|---|
| firm, firm_origin | text | Operator and the Chinese firm from which it began |
| market, country, country_iso3, hong_kong_macau | text | Market as the operator names it, with its country |
| in_service_mw, under_construction_mw, secured_powered_land_mw, total_mw | number | Capacity in MW as the operator reports it, with 0 where the source shows a dash and empty where the source gives no figure |
| as_of | date | Date of the figures |
| evidence, source_url, source_quote, check_status, share_found, retrieved | | As in Table 6 |

**Table 9. Variables in firm_links.csv**

| Variable | Type | Description |
|---|---|---|
| firm, related_firm | text | The listed firm and the Chinese firm linked to it |
| relation | category | shareholder, parent, former parent, former group member, or sponsor for a fund whose main sponsor is a Chinese state lender |
| share | number | Share held, from 0 to 1, empty when the source gives none |
| as_of | date | Date of the share, empty when the source gives none |
| evidence, source_url, source_quote, check_status, share_found, retrieved | | As in Table 6 |

### data/firms.csv

`data/firms.csv` has one row for each firm with a role in `site_roles.csv`, for each firm named in `firm_origin`, and for each state lender, with the grounds on which the firm counts as Chinese and a passage that supports them. The file is written by hand in `config/firms.csv`, and `scripts/check_sources.py` refuses a role whose firm or origin has no row, so that every firm is tested in the same way. The headquarters and the owners are recorded only where the cited passage gives them, and the note gives what other sources add.

**Table 10. Variables in firms.csv**

| Variable | Type | Values | Description |
|---|---|---|---|
| firm | text | | Firm as `site_roles.csv` names it |
| grounds | category | headquarters, control, origin, state lender, state lender fund | Grounds on which the firm counts, separated by semicolons: headquarters in mainland China, a controlling owner in mainland China, origin in a firm that met one of those grounds, a Chinese state lender, or a fund that such a lender sponsors |
| headquarters | text | | Place of the headquarters as the passage gives it, empty when the passage does not give it |
| controlling_owner | text | | Controlling owner as the passage gives it, for a firm on the ground of control |
| origin | text | | Firm of which the firm was once part, for a firm on the ground of origin |
| note | text | | What other sources add, such as the present owner of a firm counted by origin |
| evidence, source_url, source_quote, check_status, share_found, retrieved | | | As in Table 6 |

### data/rules.csv

`data/rules.csv` has one row for each rule, bill or guidance that bears on the AI chips in a host country or on remote access to them, with the part of the rule that the row records. A clause of a private contract that imposes such a control, such as a lender's requirement that an operator watch how a customer uses the chips, is recorded in the same way and marked as a private contract. A rule with several parts, such as a permit that covers exports but not use within the country, has one row for each part. The file is written by hand in `config/rules.csv` and checked by `scripts/check_sources.py`.

**Table 11. Variables in rules.csv**

| Variable | Type | Values | Description |
|---|---|---|---|
| rule_id | text | ISO 3166-1 alpha-3 code, a hyphen and four digits | Identifier of the row, with EUU for the European Union, which has no alpha-3 code |
| jurisdiction, country_iso3 | text | | Country whose rule it is, or Private contract for a clause of a contract or a requirement of a supplier that imposes such a control, with the country where the contract applies or the country of the supplier |
| applies_in | text | all, or ISO 3166-1 alpha-3 codes separated by semicolons | Countries where the rule applies, with all for a US export rule that follows US-origin chips everywhere |
| instrument | text | | Name of the law, rule, bill or guidance |
| covers | category | chip_export, chip_transit, remote_access, use_in_country, guidance | Part of the chain from shipment to use that the row records |
| status | category | in_force, pending, rescinded, announced, enforcement | in_force for a rule or guidance that applies, pending for a bill not yet passed, rescinded for a rule or draft withdrawn, announced for a measure whose taking effect the source does not confirm, enforcement for a prosecution or investigation under general law |
| date | date | | Date of the vote, notice or announcement |
| note | text | | What the row records, in one sentence |
| evidence, source_url, source_quote, check_status, share_found, retrieved | | | As in Table 6 |

### data/ai_compute.csv

`data/ai_compute.csv` has one row for each report of AI chips at a site, which is the evidence of AI workloads that level B records. A report whose source names no site, such as a lease of chips at several data centres in a region, has an empty `site_id` and gives the place in its note. The file is written by hand in `config/ai_compute.csv` and checked by `scripts/check_sources.py`.

**Table 12. Variables in ai_compute.csv**

| Variable | Type | Values | Description |
|---|---|---|---|
| site_id | text | | Site in `sites.csv`, empty when the source names no site |
| firm | text | | Firm that uses the chips |
| chips | text | | Model of the chips and of the systems that hold them, as the source names them |
| chip_count | integer | | Number of chips the source gives |
| access | category | owned, rented, unknown | rented when the firm reaches chips that another firm owns, for example through a cloud service |
| status | category | operational, planned, unclear | Stage of the deployment at the date of the source |
| date | date | | Date of the source |
| note | text | | Limits of the source |
| evidence, source_url, source_quote, check_status, share_found, retrieved | | | As in Table 6 |

### data/site_capacity.csv

`data/site_capacity.csv` has one row for each figure of capacity at a site, because sources give a site's capacity at several stages and on several bases, such as the grid capacity of a first phase and the planned total of the site. The `capacity_mw` of `sites.csv` keeps the figure of the source that supports the site. The file is written by hand in `config/site_capacity.csv` and checked by `scripts/check_sources.py`.

**Table 13. Variables in site_capacity.csv**

| Variable | Type | Values | Description |
|---|---|---|---|
| site_id | text | | Site in `sites.csv` |
| capacity_mw | number | | Capacity in MW as the source states it |
| basis | category | it, power, unspecified | As in Table 6 |
| stage | category | in_service, first_phase, planned_total, contracted, leased | Stage of the site that the figure describes, with contracted for power bought under an agreement and leased for capacity that customers have taken under an agreement |
| date | date | | Date of the statement |
| note | text | | What the figure covers |
| evidence, source_url, source_quote, check_status, share_found, retrieved | | | As in Table 6 |

### data/epoch_links.csv and data/epoch_estimates.csv

Epoch AI publishes a database of large AI data centres, "AI data centers", that estimates the IT power and the AI compute of each one from satellite imagery, permits and company documents, under the Creative Commons Attribution 4.0 licence. `data/epoch_links.csv` has one row for each site of `sites.csv` that the database also holds, written by hand in `config/epoch_links.csv` with the passage of the Epoch page that supports the match and checked by `scripts/check_sources.py`. `scripts/fetch_epoch.py` reads the estimates for those sites from Epoch's database file into `data/epoch_estimates.csv`, and the stages of construction that Epoch dates from satellite imagery and other evidence into `data/epoch_timelines.csv`, which is the first material for level C. The estimates are Epoch's models and not figures that the firms publish, so they are kept apart from `site_capacity.csv`.

**Table 14. Variables in epoch_links.csv**

| Variable | Type | Description |
|---|---|---|
| site_id | text | Site in `sites.csv` |
| epoch_name | text | Name of the data centre in Epoch's database |
| note | text | Why the two records describe the same site |
| evidence, source_url, source_quote, check_status, share_found, retrieved | | As in Table 6, for the Epoch page of the data centre |

**Table 15. Variables in epoch_estimates.csv**

| Variable | Type | Description |
|---|---|---|
| site_id, epoch_name | text | As in Table 14 |
| it_power_mw | number | Current IT power in MW that Epoch estimates, rounded to whole megawatts |
| h100_equivalents | number | Current AI compute that Epoch estimates, in Nvidia H100 equivalents |
| chip_types | text | Chips that Epoch estimates the site uses |
| owner, users | text | Owner and users of the chips that Epoch names, with its own confidence, such as #likely or #speculative |
| source_url, retrieved | text | Epoch's database file and the date it was read |

**Table 16. Variables in epoch_timelines.csv**

| Variable | Type | Description |
|---|---|---|
| site_id, epoch_name | text | As in Table 14 |
| date | date | Date of the stage, from satellite imagery or another source that Epoch cites |
| buildings_operational | number | Buildings that Epoch judges operational at that date |
| it_power_mw, h100_equivalents | number | IT power and AI compute that Epoch estimates at that date |
| construction_status | text | Epoch's description of the stage, with the links it gives |
| source_url, retrieved | text | Epoch's timeline file and the date it was read |

### data/operator_customers.csv

`data/operator_customers.csv` has one row for each figure or report of how much an operator depends on a customer that is a Chinese firm or that a source identifies as one, such as a share of the operator's revenue. Filings often describe a customer without naming it, so the description is kept as the source gives it, and another row records the source that names the customer. The file is written by hand in `config/operator_customers.csv` and checked by `scripts/check_sources.py`.

**Table 17. Variables in operator_customers.csv**

| Variable | Type | Description |
|---|---|---|
| firm | text | Operator or cloud provider that serves the customer |
| customer | text | Customer as the source refers to it, such as largest customer |
| customer_description | text | Description of the customer in the words of the source |
| identified_as | text | Chinese firm that the source names as the customer, empty when the source names none |
| share_of_revenue | number | Share of the operator's revenue, from 0 to 1, empty when the source gives none |
| revenue | text | Revenue from the customer as the source gives it |
| period | text | Period or date of the statement |
| note | text | Limits of the source |
| evidence, source_url, source_quote, check_status, share_found, retrieved | | As in Table 6 |

### data/johor_census.csv, data/batam_census.csv, data/bangkok_census.csv, data/singapore_census.csv, data/kuala_lumpur_census.csv, data/jakarta_census.csv and data/tokyo_census.csv

Each census file has one row for each data-centre facility that Baxtel's public list named in one market: Johor on 22 October 2026, Batam, Greater Bangkok and Singapore on 12 and 13 November 2026, and Greater Kuala Lumpur, Jakarta and Greater Tokyo on 14 November 2026. Baxtel's market of Bangkok includes Chon Buri, Rayong and Chachoengsao, and the census calls the market Greater Bangkok. Baxtel's market of Kuala Lumpur includes Cyberjaya and parts of Selangor and Negeri Sembilan, and the census calls the market Greater Kuala Lumpur. Baxtel's market of Jakarta includes Bekasi, Cikarang, Bogor, Depok, Tangerang and Serang, and Baxtel's market of Tokyo includes Inzai in Chiba and Kawasaki in Kanagawa, which the census calls Greater Tokyo. The list is the frame of the census, and each row copies the operator and the status as the list gives them, with the passage of the list. A person coded the Chinese link of each facility from the sites of `sites.csv`, from the page of the facility on Baxtel and from web searches, and a row with a link carries a second passage from the page that supports the link, unless the operator on the list is itself a listed firm. Where listed firms hold more than one role at a facility, the census codes the first of operator, owner, tenant and financier, and the note names the others. The files are written in `config` and both passages are checked by `scripts/check_sources.py`, which also rejects a row without a market or with an unknown code of the Chinese link.

**Table 18. Variables in the census files**

| Variable | Type | Values | Description |
|---|---|---|---|
| market | text | Johor, Batam, Greater Bangkok, Singapore, Greater Kuala Lumpur, Jakarta, Greater Tokyo | Market of the census |
| facility, operator, baxtel_status | text | | Facility, operator and status as Baxtel's list gives them; the name is empty where Baxtel withholds it, because Baxtel shows in its place an invented name that changes on each load, and `baxtel_page` then identifies the facility |
| baxtel_page | text | | Baxtel's page of the facility |
| chinese_link | category | operator, owner, tenant, financier, unconfirmed, none_found | Role of a listed firm or of a fund of a Chinese state lender at the facility; unconfirmed for a link that a source reports but another source doubts, that the firms have not confirmed, that the source does not date, or that rests on an owner the source does not name; none_found when no source found names one |
| site_id | text | | Site in `sites.csv` that the facility belongs to, empty when the dataset has none |
| note | text | | Limits of the coding |
| evidence, source_url, source_quote, check_status, share_found, retrieved | | | Baxtel's list and the passage of the facility, as in Table 6 |
| link_source_url, link_source_quote, link_evidence, link_check_status, link_share_found | | | Page and passage that support the Chinese link, the grade of their evidence as in Table 4, and the result of their check |

### config/census_searches.csv and data/census_page_scan.csv

A census codes a facility as none_found when no source names a Chinese firm there, and two files record the searches behind that code. `config/census_searches.csv` is a log, written by hand, of each web search behind the censuses of November 2026, which were made by Chinese firm and by group of operators and not for every operator by name. The searches of 22 October 2026 for Johor were not logged. `data/census_page_scan.csv` has one row for each facility of the censuses, written by `scripts/scan_census_pages.py`, which searches the description of the facility on Baxtel for the firms of Table 2 and for words that point to mainland China or Hong Kong. The scan reads only the description of the facility itself, which ends where the page begins to list nearby sites. A term found is a lead for a person to read and not a coded link, because a page can name a Chinese firm for another reason.

**Table 19. Variables in census_searches.csv**

| Variable | Type | Description |
|---|---|---|
| market | text | Market of the census that the search served |
| date | date | Date of the search |
| query | text | Words of the search |
| result | text | What the search found, in one sentence |

**Table 20. Variables in census_page_scan.csv**

| Variable | Type | Description |
|---|---|---|
| market, facility, operator, baxtel_page | text | As in Table 18 |
| terms_found | text | Terms found in the description of the facility, separated by semicolons; empty when none was found, and not_read when the page could not be downloaded |
| passage | text | Text around the first term found that the name of the facility or of the operator does not already hold |
| retrieved | date | Date the page was downloaded |

### data/capacity_definitions.csv, data/capacity_estimate.csv and data/capacity_estimate.json

The script `scripts/estimate_capacity.py` estimates the capacity of the sites in which a Chinese firm holds a role, as a low and a high estimate, from the checked rows of `sites.csv`, `site_roles.csv`, `operator_markets.csv`, `site_capacity.csv`, `epoch_estimates.csv` and `capacity_definitions.csv`. `data/capacity_definitions.csv` has one row for each definition of capacity that an operator in `operator_markets.csv` gives in the source of its figures, so that the basis of each figure that a firm reports rests on a passage of the source. DayOne's registration statement defines capacity in service, capacity under construction and secured powered land as IT power capacity, and Global Switch's annual report for 2025 describes the capacity that the expenditure of Global Switch creates as saleable IT capacity. The file is written by hand in `config/capacity_definitions.csv` and checked by `scripts/check_sources.py`.

**Table 21. Variables in capacity_definitions.csv**

| Variable | Type | Values | Description |
|---|---|---|---|
| firm | text | | Operator in `operator_markets.csv` |
| measure | text | | Measure of capacity as the source names it, such as Capacity In Service |
| column | text | in_service_mw, under_construction_mw, secured_powered_land_mw | Variable of `operator_markets.csv` that holds the measure |
| basis | category | it, power, unspecified | As in Table 6 |
| note | text | | How the passage supports the basis, where the passage does not define the measure itself |
| evidence, source_url, source_quote, check_status, share_found, retrieved | | | As in Table 6 |

The estimate counts each data centre once and follows seven rules.

1. Where a firm reports capacity by market or for the whole firm, the estimate takes the firm's figures and leaves out the figures of the firm's sites for each stage that the firm reports. DayOne reports capacity in service, under construction and on secured powered land, so no figure of a DayOne site is counted. Global Switch reports only capacity in service, so the capacity of the planned sites of Global Switch comes from the sites.
2. For every other site, the estimate takes the largest figure that the sources give for each of two stages: capacity in service, and capacity under construction or planned. A figure of a first phase counts as in service when the site is operational and as under construction or planned otherwise, and a figure of leased capacity counts only when the site is operational.
3. The low estimate counts only figures graded primary, at sites where at least one role of a Chinese firm is not graded unconfirmed and whose status is not unclear. The high estimate counts every figure.
4. The high estimate also counts the IT power that Epoch AI estimates above the figure that the sources state for a site, and, for a market whose total a firm reports, above the firm's figure for the market.
5. A planned total describes a whole site, so each estimate counts only the part of a planned total that exceeds the capacity in service that the same estimate counts at the site.
6. A builder or a supplier of equipment does not hold or use the capacity of a site, so the estimate leaves out a site at which Chinese firms hold only those two roles.
7. A second estimate leaves out the firms that count as Chinese on the ground of origin alone in `firms.csv`, together with their reported totals and their roles, so that a user can see how much of each estimate rests on such firms. `data/capacity_estimate.json` gives the second estimate as `without_origin_only`.

Figures of IT capacity, of power and of an unspecified basis are added as the sources state them, so each estimate can mix the three bases, and `data/capacity_estimate.json` gives the megawatts of each basis. A site counts as having a figure when `sites.csv` or `site_capacity.csv` gives one, or when the firm reports the capacity of the stage of the site, and both estimates leave out every site without a figure.

**Table 22. Variables in capacity_estimate.csv**

| Variable | Type | Values | Description |
|---|---|---|---|
| component | text | | Firm and market, or site, that the row describes |
| firm | text | | Firm that reports the figure, or the firms with a role at the site, separated by semicolons |
| site_id | text | | Site in `sites.csv`, empty for a figure that a firm reports by market or for the whole firm |
| stage | category | in_service, pipeline | in_service for capacity in service, pipeline for capacity under construction, planned or on secured powered land |
| mw | number | | Megawatts that the row adds, rounded to whole megawatts |
| basis | category | it, power, unspecified | As in Table 6 |
| evidence | category | primary, secondary, unconfirmed | Grade of the evidence for the figure, as in Table 4, with secondary for an estimate of Epoch AI |
| counted_in | category | both, low, high | Estimate that counts the row: both estimates, the low estimate alone or the high estimate alone |
| source_table | text | operator_markets, sites, site_capacity, epoch_estimates | File that gives the figure |
| note | text | | Why the row counts in one estimate only, the two figures whose difference an estimate of Epoch AI adds, or the planned total from which the capacity in service was taken |

`data/capacity_estimate.json` gives, for each estimate, the megawatts in service, under construction or planned, and in all, and the megawatts of each basis, together with the number of sites that the estimate covers, the number of those sites without a figure, and the number of sites left out because Chinese firms only build or supply equipment there.

### data/government_data_centres_aiddata.csv

One row for each record in AidData's Global Chinese Development Finance Dataset, Version 3.0, that paid for a data centre or a computing centre. A person read each record and wrote the coding in `config/aiddata_coding.csv`. AidData counts loans and grants, not buildings, and one project financed in phases has one row for each phase.

**Table 23. Coding values**

| Coding | Meaning |
|---|---|
| primary | The data centre is the main purpose of the project |
| component | The data centre is one part of a wider e-government, broadband, security or education project |
| scientific | A seismic, research or high-performance computing centre |
| building | A building financed by China that contains a data centre |
| command_centre | A security or emergency command centre that receives surveillance data, which the record does not describe as a data centre |
| unspecified | An e-government or network project whose record does not say whether it built a data centre |
| excluded | The record matched a search term by chance, with the reason, and is left out of the file |

**Table 24. Variables in government_data_centres_aiddata.csv**

| Variable | Type | Description |
|---|---|---|
| aiddata_id | integer | AidData record ID |
| coding | category | Value from Table 23 |
| note | text | The data centre that the record describes |
| country, country_iso3, region | text | Recipient as AidData records it |
| commitment_year | integer | Year the loan or grant was signed |
| status | category | AidData status: Pipeline: Pledge, Pipeline: Commitment, Implementation, Completion, Suspended or Cancelled |
| recommended_for_aggregates | category | Yes when AidData recommends the record for totals, which excludes pledges, suspended and cancelled records and umbrella agreements |
| flow_type | category | Loan, Grant or another AidData flow type |
| funder, implementers | text | Chinese lender or agency, and the contractors and agencies that carried out the project |
| amount_usd_nominal | number | Amount in US dollars at the time of signing, for the whole project |
| amount_usd_2021 | number | Amount adjusted for inflation to 2021 prices, for the whole project |
| interest_rate, grace_years, maturity_years | number | Loan terms in the original agreement |
| first_principal_repayment | date | Commitment date plus the grace period, as AidData calculates it. A later rescheduling can change the real date |
| financial_distress | category | Yes when AidData finds signs that the borrower had difficulty repaying |
| title | text | AidData title |
| aiddata_url | text | Page of the record on china.aiddata.org |

The amounts cover the whole project, because AidData does not separate the cost of the data centre from the rest of each project.

### data/remote_access_rule.csv

The script `scripts/flag_remote_access.py` sorts each of the sites in `sites.csv` by the way in which the US interim final rule of 19 November 2026 on remote access to advanced chips, recorded in `rules.csv` as `USA-0013` and `USA-0014`, can apply to the site. The rule requires a licence for advanced chips used at a data centre that provides more than 12,000,000 aggregate TPP to companies headquartered, or whose ultimate parent company is headquartered, in Country Group D:5 or Macau, and a data centre that provided such computing power before 19 November 2026 must obtain a licence within 90 days of that date, by 17 February 2027, in order to continue. Computing power used only for a commercial recommender system is exempt when the data centre reports the customer, the TPP of the chips and its checks to the Bureau of Industry and Security. The file is derived only from the checked rows of `sites.csv`, `site_roles.csv` and `firms.csv`, and it does not decide whether a site needs a licence, because the sources give neither the TPP of the chips at a site nor the share of the computing power that each customer uses.

**Table 25. Categories in remote_access_rule.csv**

| Category | Meaning |
|---|---|
| named_customer | A firm that counts as Chinese on the ground of headquarters or control is named as a tenant or user of the site, so the licence requirement of `USA-0014` can apply |
| chinese_operator_owner | No such tenant or user is named, but a firm on the ground of headquarters or control operates or owns the site, so chips that the firm itself receives already need a licence under the rule of October 2023, recorded as `USA-0007` |
| no_chinese_customer | The only firms named are firms on the ground of origin, a fund of a Chinese state lender or a supplier of equipment, so the rule can apply only through customers that the sources do not name |

**Table 26. Variables in remote_access_rule.csv**

| Variable | Type | Values | Description |
|---|---|---|---|
| site_id, site_name, country_iso3, status | text | | As in Table 6 |
| category | category | Table 25 | Way in which the rule can apply to the site |
| chinese_customers | text | | Firms on the ground of headquarters or control named as tenant or user, separated by semicolons |
| customer_evidence | category | primary, secondary, unconfirmed | Lowest grade of evidence among the roles of those firms, as in Table 4 |
| chinese_operators_owners | text | | Firms on the ground of headquarters or control named as operator or owner, separated by semicolons |
| other_firms | text | | Every other firm with a role at the site, separated by semicolons |
| capacity_mw, capacity_basis | | | As in Table 6 |
| licence_deadline | date | YYYY-MM-DD | 2027-02-17 for an operational site with a named customer, which needed a licence by that date to continue if it provided more than 12,000,000 aggregate TPP to the customer, and empty otherwise |
| note | text | | What the category means for a licence under the rule |

The status of a site is the status at the date of the source, so an operational site is taken to have provided computing power before 19 November 2026, and a planned site or a site under construction is not.
