# Codebook

The dataset records data-centre capacity outside mainland China in which a Chinese firm or a Chinese state lender has a role. A Chinese firm is a firm whose controlling owner is in mainland China, or a firm that began as the international arm of such a firm, such as DayOne, which began as the international arm of GDS. Hong Kong and Macau are recorded but marked, so that a user can include or exclude them.

## Roles

A record enters the dataset when a listed firm holds at least one of the roles in Table 1. One site can carry several roles held by different firms, and the dataset records each role with its own source.

**Table 1. Roles**

| Role | Definition |
|---|---|
| owner | Holds the land, the building or the company that owns the site |
| operator | Runs the site day to day |
| tenant | Rents space, power or servers in a site that another firm owns or operates, including a cloud region hosted in a third-party building |
| user | Stores data or runs servers at the site, where the source does not say whether the firm owns or rents the site |
| builder | Designed or built the site under contract |
| equipment supplier | Supplied the servers, storage, network or power equipment |
| financier | Lent or granted the money that paid for the site |

## Firms

The first version covers the firms in Table 2. A firm is added when a source shows that it holds one of the roles in Table 1 outside mainland China.

**Table 2. Firms**

| Group | Firms |
|---|---|
| Cloud and AI | Alibaba Cloud, Huawei Cloud, Tencent Cloud, ByteDance (including BytePlus and Volcano Engine), Baidu AI Cloud |
| State telecom | China Mobile International, China Telecom Global, China Unicom Global |
| Data-centre operators | GDS, VNET, zData, ChinData, DayOne (origin in GDS), Global Switch (controlled by Jiangsu Shagang Group) |
| Builders and equipment | Huawei, ZTE, Inspur, Sugon |
| State lenders | China Eximbank, China Development Bank, the state commercial banks, the Ministry of Commerce and CIDCA |

Bridge Data Centres is not a listed firm. Bain Capital bought ChinData in 2019 and merged it with Bridge, separated the two after taking ChinData private in 2023, and kept Bridge when it sold ChinData to a Chinese-led consortium in September 2025. Bridge is therefore not Chinese-owned and did not begin as the international arm of a Chinese firm, and `data/firm_links.csv` records its former link to ChinData. A site that Bridge operates enters the dataset only when a listed firm holds a role there, such as ByteDance as tenant.

Ownership can change, so each link between a firm and its Chinese owner in `data/firm_links.csv` carries the date of its source. The most recent source found for Global Switch, from May 2022, describes the company as controlled by Jiangsu Shagang Group, and Global Switch stays a listed firm until a source reports a change of control.

## Levels

Every record is coded at level A. Records with announced capacity of at least 20 MW, or with announced AI chips, are also coded at level B, and the largest level B sites in each hub are checked at level C.

**Table 3. Levels**

| Level | Coverage | Variables added |
|---|---|---|
| A | Every record | Firm, role, country, city, status, year, source of each value |
| B | Capacity of at least 20 MW or announced AI chips | Capacity in MW with a low and a high estimate, chips, power density, cooling, evidence of AI workloads, the rules that cover the site |
| C | Largest level B sites in each hub | Satellite imagery, permits and power allocations |

## Files

### data/cloud_regions.csv

One row for each public cloud region that a Chinese provider lists outside mainland China. A region is a service area and can span several buildings, so a region is linked to its buildings at level B. The script `scripts/fetch_cloud_regions.py` reads the operational regions from each provider's own region page and keeps the passage of the page that supports each row. Regions that the provider pages do not list, such as announced regions, come from `config/cloud_regions_manual.csv`, and the script checks each of those rows against the page it cites.

**Table 4. Variables in cloud_regions.csv**

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
| source_url | text | | Page that supports the row |
| source_quote | text | | Passage of the page that supports the row |
| check_status | category | found, not_found, not_read | found when the passage is on the downloaded page, not_found when the page was read and the passage is not on it, not_read when the page could not be downloaded |
| retrieved | date | YYYY-MM-DD | Date the page was downloaded |

### data/sites.csv and data/site_roles.csv

`data/sites.csv` has one row for each site, which is a building or a campus, and `data/site_roles.csv` has one row for each role that a listed firm holds at a site. A person writes both files in `config/sites.csv` and `config/site_roles.csv`, with the page that supports each row and a passage copied from the page. The script `scripts/check_sources.py` downloads each page and adds the result of the check. A site enters the file only when at least one row of `site_roles.csv` gives a listed firm a role at the site.

**Table 5. Variables in sites.csv**

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
| source_url, source_quote | text | | Page that supports the row and the passage copied from it |
| check_status | category | found, partly_found, not_found, not_read | Result of the check, as defined below |
| share_found | number | 0 to 1 | Share of the passage's pieces found on the page |
| retrieved | date | YYYY-MM-DD | Date the page was downloaded |

**Table 6. Variables in site_roles.csv**

| Variable | Type | Values | Description |
|---|---|---|---|
| site_id | text | | Site in `sites.csv` |
| firm | text | | Firm as Table 2 names it |
| firm_origin | text | | Chinese firm from which the firm began, such as GDS for DayOne, empty when the firm is itself Chinese |
| role | category | Table 1 | Role of the firm at the site |
| source_url, source_quote, check_status, share_found, retrieved | | | As in Table 5 |

A passage counts as found when at least 90 percent of its overlapping pieces of eight characters appear on the page, with spacing, punctuation, accents and case ignored, and as partly found from 50 percent. A role recorded as owner can rest on an investment in the project whose share is not disclosed, and the passage then says so.

### data/operator_markets.csv and data/firm_links.csv

`data/operator_markets.csv` has one row for each market in which an operator in Table 2 reports its capacity, for operators that report by market and not by site. `data/firm_links.csv` has one row for each ownership link between a listed firm and a Chinese firm, such as the share of DayOne that GDS holds. Both files are written by hand in `config` and checked by `scripts/check_sources.py` in the same way as the site layer.

**Table 7. Variables in operator_markets.csv**

| Variable | Type | Description |
|---|---|---|
| firm, firm_origin | text | Operator and the Chinese firm from which it began |
| market, country, country_iso3, hong_kong_macau | text | Market as the operator names it, with its country |
| in_service_mw, under_construction_mw, secured_powered_land_mw, total_mw | number | Capacity in MW as the operator reports it, with 0 where the source shows a dash |
| as_of | date | Date of the figures |
| source_url, source_quote, check_status, share_found, retrieved | | As in Table 5 |

**Table 8. Variables in firm_links.csv**

| Variable | Type | Description |
|---|---|---|
| firm, related_firm | text | The listed firm and the Chinese firm linked to it |
| relation | category | shareholder, parent, former parent or former group member |
| share | number | Share held, from 0 to 1, empty when the source gives none |
| as_of | date | Date of the share, empty when the source gives none |
| source_url, source_quote, check_status, share_found, retrieved | | As in Table 5 |

### data/government_data_centres_aiddata.csv

One row for each record in AidData's Global Chinese Development Finance Dataset, Version 3.0, that paid for a data centre or a computing centre. A person read each record and wrote the coding in `config/aiddata_coding.csv`. AidData counts loans and grants, not buildings, and one project financed in phases has one row for each phase.

**Table 9. Coding values**

| Coding | Meaning |
|---|---|
| primary | The data centre is the main purpose of the project |
| component | The data centre is one part of a wider e-government, broadband, security or education project |
| scientific | A seismic, research or high-performance computing centre |
| building | A building financed by China that contains a data centre |
| excluded | The record matched a search term by chance, with the reason, and is left out of the file |

**Table 10. Variables in government_data_centres_aiddata.csv**

| Variable | Type | Description |
|---|---|---|
| aiddata_id | integer | AidData record ID |
| coding | category | Value from Table 9 |
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
