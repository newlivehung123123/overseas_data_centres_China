# Overseas data centres of Chinese firms

This project records the data-centre capacity outside mainland China in which Chinese firms and Chinese state lenders have a role, as owner, operator, tenant, builder, equipment supplier or financier. For each site the dataset will record how much of the capacity can run large AI workloads and which country's rules cover it. US export controls govern shipments of AI chips but not the remote use of those chips, and the Remote Access Security Act, which would add remote use, passed the House on 12 January 2026 and has not passed the Senate. Capacity that Chinese firms use in third countries can therefore sit outside the rules of the United States, of China and of the host country at once, and no open dataset found records that capacity site by site together with the role of each Chinese firm and the rules that cover the site, as the section on related work below shows. The codebook in `codebook.md` defines the roles, the firms covered, the three levels of detail, the three grades of evidence and every variable. The note in `docs/preliminary_findings.md` gives the main findings so far. A public post on the findings, "Where Chinese AI firms rent the chips they cannot buy", is published on [AI in Society](https://aiinsocietyhub.com/articles/where-chinese-ai-firms-rent-the-chips-they-cannot-buy) and on the [EA Forum](https://forum.effectivealtruism.org/posts/MwC6pXAwo2DbygEKA/where-chinese-ai-firms-rent-the-chips-they-cannot-buy), and `scripts/build_post_figures.py` draws the four figures of the post from the checked files. The post describes version 0.1.0 of the dataset, and the section on versions below states what has changed since.

## Related work

Three open sources come closest to this dataset. Epoch AI's database of AI data centres estimates the IT power, the chips and the stages of construction of large AI data centres from satellite imagery, permits and company documents, and holds 4 of the sites in this dataset, but the database records neither the role of each Chinese firm at a site nor the rules that cover the site. The Australian Strategic Policy Institute relaunched the map of its project Mapping China's Tech Giants on 8 June 2021 with more than 3,800 entries on the overseas activities of 27 Chinese technology firms, among them data centres, but the map records neither the capacity of each data centre nor the rules that cover the data centre. Noah Tan's paper for the Carnegie Endowment for International Peace, "The Geopolitical Debates Over Controlling Cloud Compute", of 5 May 2026, analyses the options for controlling access to AI chips through a cloud service and cites cases of such access, but does not build a dataset of sites. This dataset adds the capacity of each site, the role of each Chinese firm with a grade of the evidence for the role, the dependence of operators on Chinese customers and the rules of the host countries, with a checked passage for every row.

## Status

The repository holds three parts as of 14 November 2026: the government data centres financed by Chinese state lenders and agencies, the public cloud regions of Chinese providers, and the first sites in which Chinese firms hold a role, with the estimates of Epoch AI for the sites that Epoch's database also holds. Every row of the files of cloud regions and sites carries a passage of the source page and a grade of evidence, and a script checks the passage against the downloaded page. The rows of government data centres come from AidData's own dataset file.

### Grades of evidence

Every row of the files of sites, cloud regions and capacity carries a grade of the evidence for the row, which the codebook defines. A row is graded primary when the firm that the row concerns, another firm that holds a role at the site or signed the agreement, or a public authority states the value in a document that the firm or the authority publishes, secondary when a third party such as a news outlet, a commercial directory or a research database states the value, and unconfirmed when the source rests on unnamed people or reports an accusation without public evidence, or when another source doubts the value or the firms have not confirmed the value. Of the 1,028 rows, 214 are graded primary, 792 secondary and 22 unconfirmed. The grade differs from the check of the passage: all 1,072 passages of the 1,028 rows were found on their pages, but a passage found in a news report shows only that the report states the value.

| File | Rows | Primary | Secondary | Unconfirmed |
|---|---|---|---|---|
| `sites.csv` | 89 | 45 | 41 | 3 |
| `site_roles.csv` | 114 | 63 | 45 | 6 |
| `cloud_regions.csv` | 55 | 51 | 4 | 0 |
| `operator_markets.csv` | 11 | 11 | 0 | 0 |
| `capacity_definitions.csv` | 4 | 4 | 0 | 0 |
| `firms.csv` | 27 | 5 | 22 | 0 |
| `firm_links.csv` | 9 | 2 | 7 | 0 |
| `operator_customers.csv` | 9 | 5 | 2 | 2 |
| `ai_compute.csv` | 13 | 3 | 3 | 7 |
| `site_capacity.csv` | 34 | 19 | 14 | 1 |
| `rules.csv` | 20 | 6 | 11 | 3 |
| `epoch_links.csv` | 4 | 0 | 4 | 0 |
| `johor_census.csv` | 84 | 0 | 84 | 0 |
| `batam_census.csv` | 20 | 0 | 20 | 0 |
| `bangkok_census.csv` | 88 | 0 | 88 | 0 |
| `singapore_census.csv` | 110 | 0 | 110 | 0 |
| `kuala_lumpur_census.csv` | 90 | 0 | 90 | 0 |
| `jakarta_census.csv` | 104 | 0 | 104 | 0 |
| `tokyo_census.csv` | 143 | 0 | 143 | 0 |

The 639 rows of the seven censuses are graded secondary because each cites Baxtel's commercial list, and the 44 second passages that support a Chinese link carry grades of their own: 11 primary, 27 secondary and 6 unconfirmed. 7 of the 13 reports of AI chips are graded unconfirmed, because the reports rest on unnamed sources or the firms have not confirmed them. The 3 reports graded primary are the loan agreement that Nscale filed at the SEC, which gives the 2,304 Nvidia B200 chips that Spring (SG), a subsidiary of ByteDance, rents at Glomfjord, and two announcements of Bitdeer.

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

The amounts cover the whole project, and in 41 of the 45 records the data centre is one part of a wider e-government, broadband, security or education project. The count is a minimum, because records that do not describe what was built are not coded and the dataset ends with commitments made in 2021.

### Cloud regions of Chinese providers

`data/cloud_regions.csv` lists 55 regions of Alibaba Cloud, Huawei Cloud, Tencent Cloud and BytePlus. The script read 51 of them from the providers' own region pages on 22 October 2026, and the other 4, three regions that Alibaba Cloud has announced for Finland, the Netherlands and Turkey and a Tencent Cloud region in Toronto that the current Tencent page does not list, come from reports in DatacenterDynamics. All 55 passages were found on their pages.

Of the 55 regions, 47 are operational outside mainland China, Hong Kong and Macau, in 22 countries. Alibaba Cloud, Huawei Cloud and Tencent Cloud account for 45 of the 47, against a count of 43 by WireScreen for the same three providers. The Tencent page lists one region, in Queretaro in Mexico, that an earlier list built from search results had missed. The BytePlus rows come from the documentation of one service and do not cover the other BytePlus services.

### Sites

`data/sites.csv` holds 89 sites in 17 countries and territories, and `data/site_roles.csv` holds 114 roles of 22 firms and funds at those sites: ByteDance, DayOne, GDS, China Mobile International, China Unicom Global, Global Switch, Huanbang (Hong Kong), zData, Shanghai DC-Science, Alibaba Cloud, Huawei Cloud, Huawei, Tencent Cloud, INF Tech, Megaspeed, Moonshot AI, RangeIDC, Beijing Haoyang, Galaxy Data Center, Bitdeer, Bridge Data Centres and the China-ASEAN Investment Cooperation Fund II. All 203 passages were found on their pages. In Johor, Batam, Greater Bangkok, Singapore, Greater Kuala Lumpur, Jakarta and Greater Tokyo, the censuses below cover every facility that a public list names. Elsewhere the dataset records the sites that searches found, and these are not every data centre in which a Chinese firm holds a role.

ByteDance holds a role at 15 sites. It is a tenant at 6 of them: the Nvidia Blackwell cluster that Aolani Cloud plans in Malaysia, the 110 MW MY06 site in Johor, the 90 MW OSL-Hamar site of Green Mountain in Norway, the Pecém site in Ceará, which has 300 MW of installed power and 200 MW of planned capacity and is expected to operate by late 2027, the Glomfjord data centre of Nscale in Norway, where its Singapore subsidiary Spring (SG) rents 2,304 Nvidia B200 chips, and the Johor data centre that zData plans on 38 acres, where Alibaba and Tencent are also named as clients. At 7 others the sources say that TikTok uses or plans the site but not whether it owns or rents it, so the role is coded user. These are Kouvola and Lahti in Finland, two sites in Ireland, the second of which TikTok planned in 2023 with a third-party service and which no source found confirms as open, and Bangkok, Samut Prakan and Chachoengsao in Thailand, where Thailand's Board of Investment approved in May 2026 an investment of about 842 billion baht by TikTok's Thai unit. The two further sites are in Singapore: the second site of AirTrunk, for which Singapore selected a proposal of a consortium of AirTrunk and ByteDance in July 2023, and Digital Realty's SIN11 facility, where ByteDance and Lazada are reported to have seen disruption after the fire of 10 September 2024, a report that ByteDance has not confirmed.

DayOne, which was a subsidiary of GDS until 31 December 2024, holds a role at 18 sites, 12 of them named in its 2026 registration statement at the SEC. DayOne reports capacity by market and not by site, so the capacity of a DayOne site comes from other sources where one gives it: 15 MW of IT capacity in the first phase at Kodaira in Tokyo, which broke ground in September 2026, and 42 MW for the site, 40 MW at Fuchu, 72 MW of IT load at Nongsa Digital Park in Batam, 20 MW in Singapore, 300 MW planned at Escatrón near Zaragoza, and a first building of 50 MW of a site of 128 MW in the Kiveriö district of Lahti, where building began in 2026. TikTok places its second Finnish data centre in the same district, but no source found confirms that it is DayOne's site. Oracle is reported to lease the Nongsa plots, with at least 120 MW of power, as sole tenant. China Mobile International operates a data centre of more than 2,100 racks in Singapore, and Uptime Institute lists Tier awards for its sites in Slough, Mörfelden and Hong Kong. China Unicom Global operates a data centre of 37,000 square metres in Tseung Kwan O and was reported in 2023 to be rolling out data centres in Singapore, Tokyo and Frankfurt. Global Switch, which a consortium of Chinese companies including Jiangsu Shagang Group has controlled since 2018, lists in its annual report for 2025 12 completed data centres in Amsterdam, Frankfurt, Hong Kong, London, Madrid, Paris and Singapore and 4 under development in Frankfurt, London, Madrid and Johor. Its website also lists a new site in Bangkok, which the annual report does not include. The same report states that Shagang holds an indirect stake of 51.8 percent in Global Switch and that the directors consider Shagang to control the group. A subsidiary of Shagang, Huanbang (Hong Kong), has held a service agreement for 15 MW in the Hong Kong data centre since 1 January 2023, with a term until 31 December 2027, and the report does not say who uses that capacity. Global Switch is coded as owner and operator of each building, with the ownership from the annual report and the location from the page of each city. Its annual report for 2023 gives 36 MW of IT capacity for the new data centre beside the Madrid site and 8 MW for the first phase of Amsterdam East, of which about 5 MW had been committed in advance, and the report for 2025 states that this first phase added 8 MW of contracted capacity.

Alibaba Cloud operates five data centres in Malaysia, two of them in the Johor region that opened in June 2026, and holds an undisclosed share of the Saudi Cloud Computing Company, a joint venture with stc and other Saudi partners that opened two data centres in Riyadh in 2022. Huawei Cloud leases its Johannesburg data centre from a partner that the source does not name, and announced a third data centre in Bangkok in 2021. Tencent Cloud has two data centres in Jakarta and plans a third in Indonesia as part of an investment of US$500 million by 2030.

### Which firms count as Chinese

The codebook counts a firm as Chinese on any of three grounds: its headquarters are in mainland China, its controlling owner is in mainland China, or the firm was once part of a firm that met one of the first two grounds at the time. `config/firms.csv` records the grounds of each of the 27 firms, parents and lenders that the dataset names, each with a passage that supports them, and all 27 passages were found on their pages. 15 count on the ground of headquarters, 6 on the ground of control, 4 on the ground of origin alone, and 2 are a state lender and a fund that a state lender sponsors. The source check refuses a role whose firm has no row in the file, so every firm is tested in the same way.

The 4 firms that count on origin alone are DayOne, which was a subsidiary of GDS until 31 December 2024, Bitdeer, which was spun off from Bitmain in 2021, Megaspeed, which was spun off from a Chinese gaming firm in 2023, and Bridge Data Centres. Bain Capital merged ChinData, which had its headquarters in Beijing, and Bridge under the parent ChinData Group in 2019, separated the two after taking ChinData private in 2023, and kept Bridge when it sold ChinData in September 2025. Version 0.1.0 left Bridge out because Bridge has never had a controlling owner in mainland China, but the same test would also have left out DayOne. Version 0.2.0 therefore applies the three grounds to every firm and counts Bridge by its origin, which adds 7 sites of Bridge in Johor, Greater Kuala Lumpur and Greater Bangkok and recodes 23 facilities of Bridge in the censuses. Because the ground of origin carries most of the capacity recorded, the capacity estimate below is also given without these 4 firms.

The censuses of November 2026 added 15 sites. In Batam, RangeIDC, a data-centre firm listed in Shenzhen, backs PT Equator Gate System Batam, which plans a site on 30 hectares in Nongsa valued at US$5 billion, and Huawei supplies prefabricated modules for the Aesler Greenix facility of 16 MW, announced in 2022, whose opening no source found confirms. In Thailand, the Board of Investment approved a data centre of Beijing Haoyang with an IT load of 300 MW in Rayong in March 2025, and a data centre of Stratus Technology, an affiliate of zData, with an IT load of about 203 MW in Rayong in June 2025. Galaxy Data Center, the international business of Hoyinn Technologies of Beijing, plans a site with an IT load of about 150 MW in Rayong, and China Mobile completed the purchase of SUPERNAP Thailand, which runs a data centre in Chonburi, on 18 March 2025. The Board's release of 6 May 2026 is now the source of the three TikTok sites in Thailand. In Singapore, the new sites are the second site of AirTrunk, Digital Realty's SIN11 facility, where Alibaba Cloud is reported to be a tenant, and the facility of Bitdeer. Bitdeer has its headquarters in Singapore and was spun off in 2021 from Bitmain, a Beijing maker of mining machines, so the codebook lists Bitdeer by its origin, as the codebook lists DayOne and Megaspeed. Bitdeer AI also holds agreements for 86.8 MW on a site in Johor, of which 21.7 MW are due in January 2027 and 65.1 MW in the third quarter of 2027. In Greater Kuala Lumpur, Bitdeer AI holds data-centre services agreements for three facilities on its site in Cyberjaya, A101, A102 and A103, with 71.5 MW of IT load in all, of which A103 of 60 MW is due to be energised in the first quarter of 2028. WG Malaysia X, a subsidiary of DayOne, agreed in August 2026 to buy 78.80 acres in the Southville City township near Dengkil, and Baxtel's database links DayOne to the purchase of about 157 acres in Kapar, a link that DayOne has not confirmed and that the dataset therefore grades unconfirmed. DayOne's filing names its sites in Kuala Lumpur as Klang Valley Tech Park and Banting Tech Park, and no source found matches either piece of land to them. In Jakarta, a disclosure of NexAI Digital Infrastruktur, as JournalArta reported on 10 November 2026, names PT Megaspeed International Indonesia and Indosat as tenants of a MettaDC data centre of 36 MW that NexAI plans in Cikarang and of a new data centre of 60 MW in Batang, in Central Java. The report does not give the terms of the leases.

### Censuses of Johor, Batam, Greater Bangkok, Singapore, Greater Kuala Lumpur, Jakarta and Greater Tokyo

A census records every data-centre facility that Baxtel's public list names in a market, and codes for each facility whether a Chinese firm or a fund of a Chinese state lender holds a role there. Johor came first, on 22 October 2026, because Johor holds 789 MW of the 962 MW that DayOne has in service, more than any other market in the dataset. The censuses of Batam, Greater Bangkok and Singapore followed on 12 and 13 November 2026, and the censuses of Greater Kuala Lumpur, Jakarta and Greater Tokyo on 14 November 2026. Baxtel's market of Bangkok includes Chon Buri, Rayong and Chachoengsao, Baxtel's market of Kuala Lumpur includes Cyberjaya and parts of Selangor and Negeri Sembilan, and Baxtel's market of Jakarta includes Bekasi, Cikarang, Bogor, Depok, Tangerang and Serang, and Baxtel's market of Tokyo includes Inzai in Chiba and Kawasaki in Kanagawa. Each row carries the passage of the list and, where a link is coded, a second passage from the page that supports the link, and all 639 first passages and 44 second passages were found on their pages.

| Market | Facilities | Operators | Role of a Chinese firm or fund | Reported but not confirmed | None found |
|---|---|---|---|---|---|
| Johor | 84 | 34 | 30 | 4 | 50 |
| Batam | 20 | 17 | 6 | 0 | 14 |
| Greater Bangkok | 88 | 39 | 8 | 0 | 80 |
| Singapore | 110 | 49 | 11 | 2 | 97 |
| Greater Kuala Lumpur | 90 | 38 | 16 | 1 | 73 |
| Jakarta | 104 | 40 | 0 | 2 | 102 |
| Greater Tokyo | 143 | 40 | 2 | 0 | 141 |
| All seven markets | 639 | | 73 | 9 | 557 |

In Johor, a role is recorded at 30 of the 84 facilities.

- 17 facilities are operated, built or planned by listed firms: 14 buildings of DayOne's Nusajaya Tech Park site and its Kempas Tech Park site, the Johor site of Global Switch and the Johor site of zData.
- 1 facility, the MSFusion site in Kota Tinggi, stands on land that a subsidiary of Megaspeed bought. The sale became unconditional on 27 April 2026, and the seller received the balance of the price on 9 September 2026.
- 9 facilities are operated or planned by Bridge Data Centres, which counts by its origin in ChinData: the 4 buildings of MY06, where ByteDance is the anchor tenant, the planned expansion of MY06, the 3 phases of MY07 in Ulu Tiram and the decommissioned facility at Plentong.
- 3 facilities of Racks Central in Pasir Gudang, a site planned at up to 510 MW, are financed in part by the China-ASEAN Investment Cooperation Fund II, whose main anchor sponsor is China Eximbank.
- At 4 facilities a Chinese link is reported but not confirmed: the 3 buildings of BrightRay in Sedenak, for which Bloomberg reported in 2024 that Shanghai DC-Science was raising a loan, and the land of Digital Hyperspace Malaysia, a subsidiary of a Hong Kong company whose owner the source does not give.

The list of Johor leaves out three sites of the dataset: the co-development of 168 MW that GDS agreed in 2022 at YTL Green Data Center Park, DayOne's land at Gerbang Nusajaya and the two data centres of Alibaba Cloud. The list also cannot be matched to the clusters of Aolani and of Megaspeed in Malaysia, whose sources do not name the place, or to the site on which Bitdeer AI holds 86.8 MW, whose owner the source does not name.

In Batam, a role is recorded at 6 of the 20 facilities. DayOne operates 4 of them, the three buildings at Nongsa Digital Park and the site at Kabil Industrial Tech Park. RangeIDC backs the developer of 1. The China-ASEAN Investment Cooperation Fund II finances Racks Central, which plans 1, under an announcement that ties the investment to the corridor of Singapore, Johor and Batam. The Aesler Greenix facility, for which Huawei supplies modules, is not on Baxtel's list.

In Greater Bangkok, Chinese firms operate 8 of the 88 facilities: DayOne's site in Chonburi, the planned site of Global Switch, the data centre of China Mobile International in Chonburi, the planned data centres of Stratus Technology, Beijing Haoyang and Galaxy Data Center in Rayong, and the two sites of Bridge Data Centres, BKK01 in Samut Prakan and QH101 in Chonburi. The census cannot place the three TikTok sites at any facility, because the Board of Investment names provinces and no facility, and the cloud regions of Alibaba Cloud, Tencent Cloud and Huawei Cloud in Thailand sit in buildings that the sources do not name. China Mobile holds 7.8 percent of True Corporation, the parent of True IDC, which runs 11 facilities on the list, and the codebook does not count such a share as a role at a facility.

In Singapore, a role is recorded at 11 of the 110 facilities. Global Switch operates 2 and owns the building in which 4 other operators lease their sites. DayOne, China Mobile International and Bitdeer operate 1 each. ByteDance is the consortium partner of AirTrunk at 1, and the China-ASEAN Investment Cooperation Fund II finances Racks Central, which operates 1. At 2 more facilities a link is reported but not confirmed: Digital Realty's SIN11 facility, which local reports name as the site of the fire that struck a zone of Alibaba Cloud on 10 September 2024, and a building where Baxtel's undated description names ZTE among the firms with facilities of their own.

In Greater Kuala Lumpur, a role is recorded at 16 of the 90 facilities. Bridge Data Centres operates or plans 12 of them: MY01, the 4 buildings of MY02 in Cyberjaya, the 4 buildings of MY03 in Mranti Park, the land in Banting and the two withdrawn facilities in Southville City. Bitdeer is the tenant of 3 facilities whose names and addresses Baxtel withholds and which Baxtel's list places under Bitdeer. Bitdeer states that its site in Cyberjaya holds A101, A102 and A103 under data-centre services agreements, and no source matches each listed facility to one of the three. A subsidiary of DayOne is buying the land of 1 more facility, and at 1 further facility, the land in Kapar, the link to DayOne is reported but not confirmed. China State Construction Engineering Corporation built Digital Realty's KUL11 building as contractor for Infinaxis, and the census does not code a contractor that the codebook does not list. Alibaba Cloud and Huawei Cloud run cloud regions in Kuala Lumpur in buildings that the sources do not name, and DayOne's sites at Klang Valley Tech Park and Banting Tech Park are not on Baxtel's list. China Mobile International signed a non-binding memorandum with Tanco in June 2026 to consider a data centre of 50 MW in Port Dickson. The memorandum gives China Mobile International no role, and the data centre is not on the list, so the dataset records no site.

In Jakarta, no role is recorded at any of the 104 facilities, and a Chinese link is reported but not confirmed at 2. NexAI's disclosure names Megaspeed's Indonesian subsidiary as a tenant of a MettaDC data centre of 36 MW that NexAI plans in Cikarang, and Baxtel places MettaDC's ID01 in Jababeka, Cikarang, but no source names ID01. Baxtel's undated description of Digital Hyperspace, a subsidiary of Quantum DC (HK) Limited, states that the firm collaborates with China Telecom and with a fund backed by China Telecom, CNIC and New World Development, and gives no role. The cloud regions of Alibaba Cloud, Tencent Cloud, Huawei Cloud and BytePlus in Jakarta, and the Nvidia GB200 systems with which Indosat serves INF Tech, sit in buildings that the sources do not name, so the census cannot place them. Baxtel's page of BDx's CGK3 lists China Mobile among the network carriers in the building, and the codebook does not count the presence of a carrier as a role.

In Greater Tokyo, a role is recorded at 2 of the 143 facilities, the two sites of DayOne at Fuchu and Kodaira, and no source found names a Chinese link at the other 141. Alibaba Cloud reports five data centres in its Japan region and Tencent Cloud two in Tokyo, but no source found names their buildings. Datasection, whose largest customer the Financial Times reported to be Tencent, is reported to use a facility in Inzai that no source names. W.Media, citing the research firm DC Byte, reports that Chinese firms contracted more than 100 MW of planned capacity in Tokyo and Osaka in a few deals by 2025, without naming the facilities, so the census of Tokyo probably understates the Chinese presence more than the other censuses do. Ada Infrastructure, which operates 8 facilities on the list, was founded by GLP in 2023. No single member of the consortium that owns GLP, among them Vanke, Hopu, Hillhouse and Bank of China Group Investment, controls GLP, so GLP does not meet the ground of control and the census does not count Ada by origin.

A facility is coded none found after two searches. `scripts/scan_census_pages.py` searches the description of each facility on Baxtel for the names of the firms in the codebook and for words that point to mainland China or Hong Kong, and `data/census_page_scan.csv` records the result for all 639 facilities: a term was found on 46 pages, and 6 pages could not be read. `config/census_searches.csv` logs the 91 web searches of 12, 13 and 14 November 2026, by Chinese firm and by group of operators, with the result of each. The searches of 22 October 2026 for Johor were not logged. A facility with none found may still have a Chinese tenant that no source names, because operators seldom name their tenants and the searches did not cover every operator by name. Baxtel is a commercial directory and no public register of data centres was found for any of the seven markets, so each list is the frame of a census and not a complete register.

Baxtel withholds the name of some facilities and shows in place of the name an invented one that changes each time the page loads. The censuses leave such a name empty and identify the facility by its page on Baxtel. Version 0.1.0 recorded four invented names in the census of Johor, which version 0.2.0 removes.

### Capacity that operators report by market

DayOne's registration statement at the SEC, which DayOne filed for its listing in 2026, reports its capacity by market as of 20 September 2026 and not by site. `data/operator_markets.csv` records the 10 markets of DayOne: 962 MW in service, 1,328 MW under construction and 2,308 MW of secured powered land, or 4,597 MW in all, in Malaysia, Indonesia, Singapore, Thailand, Japan, Hong Kong, Finland and Spain. Johor holds 789 MW of the 962 MW in service. The rows add up to 1 MW more or less than the totals in the filing, because the filing rounds each figure. The same file records the 252 MW of saleable capacity that Global Switch's annual report for 2025 gives for the group, which the report does not divide by data centre. The same filing states that GDS holds 19.4 percent of DayOne's shares, which `data/firm_links.csv` records together with the former link between Bridge Data Centres and ChinData, three sources on the control of Global Switch by Jiangsu Shagang Group, the latest its annual report for 2025, the origin of Megaspeed in a Chinese gaming firm, of Galaxy Data Center in Hoyinn Technologies and of Bitdeer in Bitmain, and the sponsorship of the China-ASEAN Investment Cooperation Fund II by China Eximbank. All 20 passages of the two files were found on their pages.

### Customers of operators

Operators seldom name their customers, but their filings show how much of their revenue comes from Chinese firms. `data/operator_customers.csv` records 9 such statements, and all 9 passages were found on their pages. DayOne's registration statement does not name its largest customer but describes it as a global technology company with a leading short-form video platform serving a worldwide audience, and that customer provided 69.4 percent of DayOne's revenue in 2025 and 69.2 percent in the first half of 2026. Bloomberg reported in July 2025 that ByteDance is DayOne's largest customer. Nscale's registration statement states that its largest customer provided 73 percent of its revenue in 2025, and Tom's Hardware, citing the Financial Times, reports that this customer was Spring (SG), a subsidiary of ByteDance, with US$24 million of Nscale's US$33 million. The Japanese operator Datasection received JPY 30.5 billion, essentially all its AI infrastructure revenue in the year to March 2026, through one intermediary, NauNau Japan, from an end customer that it does not name, and the Financial Times has reported that this customer is Tencent. Global Switch recognised £28.4 million of revenue in 2025 under its agreement with Huanbang (Hong Kong), a subsidiary of its controlling shareholder. GDS, then the parent of the business that is now DayOne, stated on 15 November 2021 that a major Chinese cloud service provider, which GDS does not name, had agreed to give GDS priority as its data-centre provider in Southeast Asia.

### AI chips

`data/ai_compute.csv` records the reports of AI chips that Chinese firms reach outside China, which are the evidence of AI workloads that level B needs, and all 13 passages were found on their pages. 12 of the 13 reports name Nvidia chips, and the thirteenth does not disclose the model of chip. In 9 of the 13 a Chinese firm rents the use of chips that another firm holds, and in 4 the firm owns the chips: Megaspeed in 1 report and Bitdeer in 3. The sources of 7 of the reports do not name the site.

1. ByteDance is set to reach about 36,000 Nvidia B200 chips in 500 GB200 NVL72 systems that the cloud operator Aolani Cloud deploys in Malaysia, valued at more than US$2.5 billion, as the Wall Street Journal reported in March 2026 from unnamed sources.
2. INF Tech, a Shanghai start-up, reached about 2,300 Nvidia Blackwell chips in 32 GB200 racks that the Indonesian telecom firm Indosat bought and operates in Jakarta, as the Wall Street Journal reported in November 2025.
3. Spring (SG), a Singapore subsidiary of ByteDance, rents 2,304 Nvidia B200 chips at the Glomfjord data centre of Nscale in Norway under a cloud services agreement of 15 May 2025. The loan agreement that Nscale filed with its registration statement at the SEC in September 2026 gives the number of chips and names Spring (SG) as the customer, and Tom's Hardware, citing the Financial Times, identifies Spring (SG) as a subsidiary of ByteDance.
4. Megaspeed, a Singapore firm spun off from a Chinese gaming firm in 2023, bought through its Malaysian unit Nvidia chips worth nearly US$2 billion that were shipped to data centres in Malaysia and Indonesia and appeared to serve Chinese clients remotely. The US is investigating it, and Bridge Data Centres removed Megaspeed from its Malaysian hub in April 2026.
5. A White House official accused Moonshot AI in 2026 of reaching Nvidia chips remotely through an unnamed party in Thailand, an accusation for which the source reports no public evidence.
6. Tencent leases about 100,000 advanced AI chips at several Oracle data centres in Southeast Asia for five years, in a deal worth about US$7 billion, as the Financial Times reported in October 2026. The companies have not confirmed the deal, and the countries, sites and models of chip are not disclosed.
7. Tencent holds contracts worth more than US$1.2 billion for Blackwell chips of the Japanese firm Datasection in Japan and Australia, as the Financial Times reported in December 2025. Datasection has not confirmed that Tencent is its customer.
8. Alibaba trains its latest large language models in data centres in Southeast Asia that non-Chinese firms own and operate, as the Financial Times reported in November 2025 from two people with direct knowledge. Reuters could not verify the report.
9. ByteDance does the same, according to the same report.
10. Engineers of a Chinese firm that the source does not name travelled to Malaysia in March 2025 with hard drives of training data to train AI models at data centres with Nvidia chips, as the Wall Street Journal reported. Malaysia's trade ministry answered that servers with such chips are not controlled goods in Malaysia, which `data/rules.csv` records.
11. Bitdeer completed the deployment of an Nvidia DGX H100 SuperPOD in March 2024, in an announcement dated from Singapore that does not say where the system stands.
12. Bitdeer AI announced in January 2026 the launch of Nvidia GB200 NVL72 systems in Malaysia, at a site that the announcement does not name.
13. Bitdeer AI designs the A202 facility on its site in Johor for Nvidia GB300 NVL72 and Vera Rubin systems, and buys the equipment as customers sign contracts.

### Estimates of Epoch AI

Epoch AI's database of AI data centres, read on 22 October 2026, holds 95 data centres, 77 of them in the United States and 5 in mainland China. 4 of the other 13 are sites in this dataset, and `data/epoch_estimates.csv` holds Epoch's estimates for them, read from Epoch's database file. Epoch estimates 473 MW of IT power at DayOne's Nusajaya Tech Park site and 422 MW at its Kempas Tech Park site in Johor, and names no owner or user of the chips at either. It estimates 243 MW at MY06, where it judges ByteDance the likely owner and user of the chips, and 72 MW at the site in Batam that it names after Oracle, where it judges Oracle the likely owner of the chips and Tencent a possible user. Epoch names the Batam site after its tenant, so the match to DayOne's Nongsa Digital Park site rests on Epoch's own sources, which place it at DayOne's site, and on the three buildings of 72 MW that both describe. Epoch's database does not record the role of each Chinese firm or the rules that cover a site, which this dataset adds. The estimates are Epoch's models and are kept apart from the figures of capacity in `data/site_capacity.csv`. `data/epoch_timelines.csv` holds the 29 stages of construction that Epoch dates for the 4 sites from satellite imagery and other evidence, which are the first material for level C. At MY06 the first building was operational at the end of 2022 with 19 MW, and 7 buildings with 243 MW by May 2025, against the 110 MW of three buildings that the source of the site row gives for the first project. Buildings 8 and 9 looked structurally complete in September 2025 and Building 10 had all its cooling units by March 2026, but Epoch saw no cars in the car parks of Buildings 8 to 10 in September 2026 and does not judge them in use. At Kempas, land clearing began in November 2023 and Epoch assumes 9 buildings with 422 MW operational by October 2026, partly from the state of the buildings before commissioning. At Nusajaya it judges 10 buildings with 473 MW operational by October 2026. At Batam, land clearing began in July 2022, 2 buildings with 33 MW were operational by May 2025, when Oracle announced its Batam region, and 3 buildings with 72 MW by April 2026.

### Capacity estimate

The script `scripts/estimate_capacity.py` adds the checked figures of capacity into a low and a high estimate, and writes each figure that the estimate counts to `data/capacity_estimate.csv` and the totals to `data/capacity_estimate.json`. The estimate counts each data centre once. Where a firm reports capacity by market or for the whole firm, the estimate takes the firm's figures and leaves out the figures of the firm's sites, and for every other site the estimate takes the largest figure that the sources give for capacity in service and for capacity under construction or planned. The low estimate counts only figures graded primary, at sites where the role of a Chinese firm is not graded unconfirmed and whose status is not unclear. The high estimate counts every figure and adds the IT power that Epoch AI estimates above the figure that the sources state. The codebook gives the rules in full.

| Estimate | In service | Under construction or planned | In all |
|---|---|---|---|
| Low | 1,416 MW | 6,163 MW | 7,578 MW |
| High | 1,655 MW | 6,984 MW | 8,638 MW |

In service, the low estimate consists of the 961 MW that the rows of DayOne's markets add up to, the 252 MW of saleable capacity that Global Switch reports for the group, the 110 MW of MY06, the 90 MW that TikTok holds at the OSL-Hamar site in Norway, which the developer, Green Mountain, confirms, the 2.5 MW of the A101 facility in Cyberjaya, which Bitdeer's update filed at the SEC lists as live, and the 0.2 MW of Bridge's BKK01 in Samut Prakan. The high estimate adds 133 MW at MY06 and 106 MW at DayOne's two sites in Johor, by which the estimates of Epoch AI exceed the stated figures. Under construction or planned, the low estimate consists of the 3,637 MW that DayOne reports under construction and on secured powered land, the 510 MW of the Racks Central site in Pasir Gudang, the 300 MW of Beijing Haoyang, the 203 MW of Stratus Technology and the 150 MW of Galaxy Data Center in Rayong, all three of which Thailand's Board of Investment gives, the 86.8 MW of IT load of Bitdeer AI in Johor and the 69 MW that remain of the 71.5 MW of IT load that Bitdeer gives for its site in Cyberjaya, both from Bitdeer's own documents, the 60 MW that remain of the 150 MW planned at OSL-Hamar, the 36 MW of Global Switch Madrid 2, and five figures of IT capacity from Bridge's own pages: the 398 MW that remain of the 508 MW of MY06 after the 110 MW in service, the 374 MW of MY07, the 193 MW of QHI01 and QHI02 in Chonburi, the 98 MW of MY01 and MY02 together and the 48 MW of MY03. Bridge's pages give the total capacity of each site without the part in service, so the estimate counts all of MY01, MY02, MY03 and MY07 as under construction or planned, although some of their buildings are in service. The high estimate adds 300 MW of power at Pecém, 300 MW of power for the MSFusion site in Kota Tinggi, 168 MW at YTL Green Data Center Park, where the status of the GDS project is unclear, 90 MW at BrightRay in Sedenak, where the Chinese link is unconfirmed, and the 36 MW and 60 MW of the data centres that NexAI plans in Cikarang and Batang, where Megaspeed's Indonesian subsidiary is named as a tenant.

Without the 4 firms that count as Chinese on their origin alone, the low estimate falls to 452 MW in service and 1,657 MW under construction or planned, and the high estimate to 585 MW and 2,182 MW. DayOne alone reports 961 MW in service and 3,637 MW under construction or on secured powered land, so most of the capacity recorded rests on a firm whose link to China is its origin and a stake of 19.4 percent that GDS still holds. The 452 MW in service that remain are the 252 MW of Global Switch, the 110 MW of MY06 and the 90 MW that TikTok holds at OSL-Hamar.

Two rules keep the estimate from counting capacity twice or too widely. A planned total describes a whole site, so the estimate counts only the part of a planned total that is not yet in service. A builder or a supplier of equipment does not hold or use the capacity of a site, so the estimate leaves out a site at which Chinese firms hold only those two roles, which applies to 1 of the 89 sites.

DayOne's registration statement defines capacity in service, capacity under construction and secured powered land as IT power capacity, which `data/capacity_definitions.csv` records with the passage of each definition, and Global Switch's annual report describes the capacity that the expenditure of Global Switch creates as saleable IT capacity. Of the low estimate, 6,958 MW are therefore IT capacity and 620 MW have no stated basis, and of the high estimate, 7,064 MW are IT capacity, 600 MW are power and 974 MW have no stated basis. Both estimates include Hong Kong, where DayOne reports 27 MW in service and 39 MW under construction or on secured powered land, and the total of Global Switch includes the Hong Kong data centre of Global Switch without separating it. 38 of the 88 sites that the estimate covers have no figure of capacity, among them the data centres of Alibaba Cloud, Tencent Cloud, Huawei Cloud, China Mobile International and China Unicom Global and the Glomfjord data centre of Nscale, so both estimates understate the capacity of the sites recorded.

### Rules in the host countries

`data/rules.csv` records 20 parts of rules, bills, guidance, reviews, prosecutions, contracts and requirements of suppliers that bear on the AI chips in a host country or on remote access to them, each with its passage and the countries where it applies, and all 20 passages were found on their pages. US export rules control shipments of advanced chips but not access to the chips through a cloud service. The Remote Access Security Act, which would cover such access, passed the House by 369 votes to 22 on 12 January 2026 and has not passed the Senate. The AI Diffusion Rule, issued on 15 January 2025, was rescinded in May 2025 before it took effect, and the notice of rescission announced licensing requirements for exports of advanced chips to Malaysia and Thailand. Commerce later shelved the draft rule on Malaysia and Thailand, as reported in August 2026. BIS guidance of 31 May 2026 states that a licence is needed for advanced chips sent to any entity whose ultimate parent is in China or Macau, wherever the entity is, and in August 2026 BIS began an enforcement review that lists the countries where Chinese firms reach the chips remotely, which remains legal. A draft rule of the Department of Commerce that would bar the renting of Nvidia chips to Chinese AI firms through servers in Thailand and Singapore was reported in the same month. The Department has not published the draft, and lawyers quoted in the report doubt that the Department can enforce such a rule before the Remote Access Security Act passes. Malaysia has required a permit since July 2025 for exports, transshipments and transits of US-origin AI chips, but the permit does not cover the use of the chips within Malaysia. Malaysia's trade ministry also stated in June 2025 that servers with Nvidia and other AI chips are not controlled goods in Malaysia and that data centres may decide whom to serve within Malaysian law. Singapore has acted through prosecutions for fraud on server suppliers about the end users of the servers, under general law, and through an advisory of April 2025, in which Singapore Customs and the Ministry of Trade and Industry warn against the use of Singapore to evade the export controls of other countries. The searches of 13 November 2026 found no rule of Singapore, Thailand or Indonesia on the use of AI chips through a cloud service. A Chinese firm that rents servers in Johor and trains a model on them therefore falls under none of these rules, as the sources stand. The European Union extended its control list on exports in November 2025 to certain advanced computing integrated circuits, but the source does not say whether the entries cover the AI chips that US rules control or access to such chips through a cloud service. The controls on use found outside the rules of states are private. The loan agreement for the chips at Glomfjord requires Nscale to monitor how its customer uses them for signs of a breach of export control law and to report such signs to the lender. Nvidia is reported to require new cloud partners in Southeast Asia to enrol in its Fleet Intelligence monitoring system, and to have instructed cloud and data-centre partners to sell at least 51 percent of their services to non-Chinese customers, an instruction that, according to The Information, Nvidia has not enforced as a mandatory rule. TechRepublic reported both measures on 6 November 2026, citing Bloomberg and the Financial Times, and the dataset grades both unconfirmed. In the Gulf, the US approved in November 2025 exports of up to the equivalent of 35,000 Nvidia GB300 chips each to G42 in the United Arab Emirates and Humain in Saudi Arabia, on condition of security and reporting requirements that are not public, and the UAE describes a Regulated Technology Environment of audits and oversight for organisations that acquire such chips.

### Figures

The script `scripts/summarise.py` counts the checked rows of the files of sites, cloud regions and capacity, with the grades of evidence and the low and high capacity estimates, and writes `data/summary.json`, so that every figure in the text above can be reproduced. Of the 89 sites, 38 are operational, 10 are under construction, 32 are planned and 9 are unclear, and Malaysia holds 25 of them, more than any other country. Of the 114 roles, 52 are operator, 33 owner, 18 tenant, 9 user, 1 financier and 1 equipment supplier. 30 of the 89 sites are coded at level B, 25 of them for an announced capacity of at least 20 MW and 5 for a report of AI chips. DayOne's two sites in Johor stay at level A only because DayOne reports the capacity of Johor as a whole, and Epoch AI estimates 473 MW and 422 MW of IT power for them. Only 16 sites have a capacity of their own in the sources that support them, 1,100 MW of IT capacity, 460 MW of power and 500 MW whose basis the sources do not give, and `data/site_capacity.csv` holds a further 34 figures of capacity at several stages, so most of the capacity recorded so far is the 4,597 MW that DayOne reports by market and the 252 MW that Global Switch reports for the group.

### Next steps

1. Add the remaining sites of ByteDance, the portfolios of VNET and zData outside mainland China, and the capacity of the other buildings of Global Switch. The sources found so far show China Telecom Global only through points of presence in third-party data centres, which the codebook does not record as roles, through an agreement of 2017 for access to the data centres of Global Switch, and through the partnership in which Global Switch launched its Woodlands building in Singapore with China Telecom Global and Daily-Tech in March 2019.
2. Add the capacity of each DayOne site where another source gives it, such as a permit or a power purchase agreement, to `data/site_capacity.csv`, which holds 34 figures so far, all of whose passages were found on their pages.
3. Find out from other sources whether the 12 e-government and network projects coded unspecified built a data centre.
4. Link each cloud region to its buildings, and begin level C with satellite imagery, permits and power allocations for the largest level B sites in Johor, Batam and Bangkok.
5. Add the rules of the other host countries, such as Brazil, Japan, Norway and the members of the European Union, and repeat the search for rules of Thailand and Indonesia in Thai and Indonesian sources.
6. Identify the Oracle data centres in Southeast Asia at which Tencent is reported to lease chips, and the sites of Datasection in Japan and Australia that serve its largest customer.
7. Match further sites to Epoch AI's database as it grows, and compare its estimates with the figures of capacity in `data/site_capacity.csv`.
8. Search the tenants of the 557 facilities in the seven markets at which no Chinese link was found, operator by operator, and confirm or reject the 9 reported links.
9. Find primary sources for the 1,060 MW that only the high capacity estimate counts, and figures of capacity for the 38 sites that have none.

## Versions

`CHANGELOG.md` lists the versions of the dataset and what each changed. Version 0.1.0, of 10 November 2026, is the dataset that the public post describes, at commit `80c3d88`. Version 0.2.0, of 14 November 2026, at commit `8d3204a`, adds the censuses of Batam, Greater Bangkok, Singapore, Greater Kuala Lumpur and Jakarta, 22 sites, 4 rules and 3 reports of AI chips, applies one standard to decide which firms count as Chinese, which adds Bridge Data Centres, and corrects the capacity estimate and four rows of the census of Johor. The low estimate of capacity in service rose from 1,323 MW to 1,416 MW between the two versions, and the high estimate rose from 1,652 MW to 1,654 MW. A release on GitHub can be created by hand from each commit, because the repository records no tags.

## Dashboard

The dashboard is published at [https://newlivehung123123.github.io/overseas_data_centres_China/](https://newlivehung123123.github.io/overseas_data_centres_China/). The folder `site` holds it as a static page in HTML, CSS and JavaScript with no build step. It shows the sites and the cloud regions on a map and in a table, with filters by firm, role and country and a search box, and each row shows the cited passage and the result of its check. A row of figures above the map summarises the dataset. Sections list the rules recorded in `data/rules.csv`, the reports of AI chips whose sources name no site, the Chinese customers of operators and the censuses of the seven markets, with a filter by market, and the point of each city lists the rules recorded for its country. Each point marks the centre of the city that the source names, from OpenStreetMap, because most sources name the city and not the building. The map draws the countries of Natural Earth, which are in the public domain, under the tiles of OpenStreetMap, so the map still shows the countries when a browser blocks the tile server. `scripts/build_world_map.py` writes them to `site/data/world.geojson` from Natural Earth's file of countries at 1:110 million. A section on the capacity estimate gives the low and the high estimate and lists every figure counted, and the passage of each row shows the grade of its evidence. The government data centres from AidData are left out of the dashboard until the article pitched on them has been answered.

The dashboard reads `site/data/dashboard.json`, which `scripts/build_site_data.py` writes from the checked files, the capacity estimate and `config/places.csv`. The script `scripts/geocode_places.py` finds the point of each new city from the Nominatim service of OpenStreetMap, at most one request a second, and records the OpenStreetMap object behind each point.

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

AidData distributes the GCDF 3.0 file itself, so the file is not committed. Download it from AidData, place the Excel file in `data/raw`, and build the file of government data centres.

```bash
.venv/bin/python scripts/build_aiddata_layer.py
.venv/bin/python scripts/build_aiddata_layer.py --candidates
```

The estimates of Epoch AI need no download by hand either. The script downloads Epoch's database and timeline files, saves them in `data/raw/epoch`, and writes `data/epoch_estimates.csv` and `data/epoch_timelines.csv` for the sites matched in `config/epoch_links.csv`.

```bash
.venv/bin/python scripts/fetch_epoch.py
```

The file of cloud regions needs no download by hand. The script downloads each provider page, saves the page with its text in `data/raw/pages`, which is not committed, and writes `data/cloud_regions.csv`. The option `--offline` reads the saved pages instead.

```bash
.venv/bin/python scripts/fetch_cloud_regions.py
```

The sites, the roles and the other checked files are written by hand in `config`, such as `config/sites.csv` and `config/site_roles.csv`. The check downloads each cited page, reads the text of PDF files such as annual reports with pypdf, saves the text in `data/raw/pages/sources` and writes each file to `data`, such as `data/sites.csv` and `data/site_roles.csv`, with the result for each row.

```bash
SEC_CONTACT_EMAIL=you@example.org .venv/bin/python scripts/check_sources.py
```

The SEC accepts automated requests only with a contact email, so the check reads one from `SEC_CONTACT_EMAIL` and refuses pages on sec.gov without it. The email is sent only to the SEC and is not stored in the repository.

The capacity estimate and the figures read the checked files, so both run after the check.

```bash
.venv/bin/python scripts/estimate_capacity.py
.venv/bin/python scripts/summarise.py
```

The search of the page of each facility in the censuses runs after the check, and a person logs each web search behind a census in `config/census_searches.csv`.

```bash
.venv/bin/python scripts/scan_census_pages.py
```

The figures of the public post are drawn from the same files and from Epoch AI's database file, which `scripts/fetch_epoch.py` saves in `data/raw/epoch`. The script writes the four figures to `docs/figures` as SVG files and stops if Figure 3 and `data/rules.csv` do not hold the same rows.

```bash
.venv/bin/python scripts/build_post_figures.py
```

The first command writes `data/government_data_centres_aiddata.csv` and `data/aiddata_summary.json` and prints the figures above. The option `--candidates` also writes `data/aiddata_candidates.csv`, the records that match a search term and are not coded yet. The option `--gcdf` gives another path to the Excel file.

## Tests

The tests use small tables and passages written in the test files and need no download. The workflow in `.github/workflows/tests.yml` runs them on each push.

```bash
.venv/bin/python -m unittest discover -s tests
```

## Files

| Path | Contents |
|---|---|
| `CONTRIBUTING.md` | Purpose of the project, data rules and writing rules for anyone who works on the repository |
| `codebook.md` | Roles, firms, levels and variables |
| `docs/preliminary_findings.md` | Main findings so far, with the figures from the checked rows |
| `docs/figures/` | The four figures of the public post, drawn from the current files as SVG files |
| `docs/figures/post_v0.1.0/` | The four figures as the post published them, drawn from version 0.1.0 |
| `CHANGELOG.md` | Versions of the dataset and what each changed |
| `config/firms.csv` | Grounds on which each firm counts as Chinese, each with its page and passage |
| `config/firm_links.csv` | Ownership links between listed firms and Chinese firms, each with its page and passage |
| `config/operator_markets.csv` | Capacity that operators report by market, each with its page and passage |
| `config/places.csv` | Map point of each city, with the OpenStreetMap object it comes from |
| `config/rules.csv` | Parts of rules that bear on AI chips in host countries, each with its page and passage |
| `config/site_roles.csv` | Roles of firms at sites, each with its page and passage |
| `config/sites.csv` | Sites, each with its page and passage |
| `config/ai_compute.csv` | Reports of AI chips at sites, each with its page and passage |
| `config/site_capacity.csv` | Figures of capacity at sites, each with its page and passage |
| `config/capacity_definitions.csv` | Definitions of capacity that operators give in the sources of their figures, each with its page and passage |
| `config/operator_customers.csv` | Figures of how much operators depend on Chinese customers, each with its page and passage |
| `config/johor_census.csv`, `config/batam_census.csv`, `config/bangkok_census.csv`, `config/singapore_census.csv`, `config/kuala_lumpur_census.csv`, `config/jakarta_census.csv`, `config/tokyo_census.csv` | Facilities of each market from Baxtel's list, with the Chinese link of each and the passages that support the link |
| `config/census_searches.csv` | Web searches behind the censuses of November 2026, with the date, the query and the result of each |
| `config/epoch_links.csv` | Sites that Epoch AI's database also holds, each with the passage of the Epoch page that supports the match |
| `config/cloud_regions_manual.csv` | Regions that the provider pages do not list, each with the page that reports it |
| `config/aiddata_coding.csv` | Coding of each AidData record read, with a note on the data centre or the reason for exclusion |
| `data/ai_compute.csv` | Reports of AI chips with the result of the check |
| `data/aiddata_candidates.csv` | AidData records that match a related term and are not coded yet |
| `data/aiddata_summary.json` | Figures of the government data centres from AidData |
| `data/cloud_regions.csv` | Public cloud regions of Chinese providers outside mainland China |
| `data/epoch_estimates.csv` | Estimates of Epoch AI for the matched sites, read from Epoch's database file |
| `data/epoch_links.csv` | Matches to Epoch AI's database with the result of the check |
| `data/epoch_timelines.csv` | Stages of construction that Epoch AI dates for the matched sites, read from Epoch's timeline file |
| `data/johor_census.csv`, `data/batam_census.csv`, `data/bangkok_census.csv`, `data/singapore_census.csv`, `data/kuala_lumpur_census.csv`, `data/jakarta_census.csv`, `data/tokyo_census.csv` | Census of the facilities of each market that Baxtel lists, with the Chinese link of each and the results of both checks |
| `data/census_page_scan.csv` | Search of the page of each facility on Baxtel for the names of Chinese firms and places |
| `data/firms.csv` | Grounds of each firm with the result of the check |
| `data/firm_links.csv` | Ownership links with the result of the check |
| `data/operator_customers.csv` | Customers of operators with the result of the check |
| `data/operator_markets.csv` | Capacity by market with the result of the check |
| `data/rules.csv` | Rules with the result of the check |
| `data/summary.json` | Figures of the sites, cloud regions and capacity, with the grades of evidence and the capacity estimate |
| `data/site_capacity.csv` | Figures of capacity with the result of the check |
| `data/capacity_definitions.csv` | Definitions of capacity with the result of the check |
| `data/capacity_estimate.csv` | Each figure that the capacity estimate counts, with its grade of evidence and the estimate that counts it |
| `data/capacity_estimate.json` | Low and high capacity estimates |
| `data/site_roles.csv` | Roles with the result of the check |
| `data/sites.csv` | Sites with the result of the check |
| `data/government_data_centres_aiddata.csv` | AidData records coded as data centres or computing centres |
| `scripts/build_aiddata_layer.py` | Build of the file of government data centres from the AidData file and the coding |
| `scripts/build_site_data.py` | Build of the dashboard data from the checked files |
| `scripts/check_sources.py` | Check that each passage of the files written by hand is on its page, and that each row carries a known grade of evidence |
| `scripts/scan_census_pages.py` | Search of the Baxtel page of each facility in the censuses, written to `data/census_page_scan.csv` |
| `scripts/summarise.py` | Figures of the sites, cloud regions and capacity, written to `data/summary.json` |
| `scripts/estimate_capacity.py` | Low and high estimates of the capacity of the sites, written to `data/capacity_estimate.csv` and `data/capacity_estimate.json` |
| `scripts/fetch_cloud_regions.py` | Download of the provider region pages and build of the file of cloud regions |
| `scripts/fetch_epoch.py` | Download of Epoch AI's database and timeline files and the estimates and stages for the matched sites |
| `site/` | Dashboard, with its data in `site/data/dashboard.json` |
| `scripts/geocode_places.py` | Map point of each city from OpenStreetMap |
| `scripts/build_world_map.py` | Outline of the countries under the map tiles, from Natural Earth |
| `scripts/build_post_figures.py` | The four figures of the public post, drawn from the checked files and Epoch AI's database file |
| `tests/test_build_aiddata_layer.py` | Offline tests of the AidData build |
| `tests/test_check_sources.py` | Offline tests of the passage check |
| `tests/test_fetch_cloud_regions.py` | Offline tests of the region parsers and of the reading of PDF files |
| `tests/test_fetch_epoch.py` | Offline tests of the reading of Epoch AI's database file |
| `tests/test_build_site_data.py` | Offline tests of the dashboard data |
| `tests/test_estimate_capacity.py` | Offline tests of the capacity estimate |

## Licence and attribution

The code is under the MIT licence in `LICENSE`. The data files are under the Creative Commons Attribution 4.0 licence. The file of government data centres is derived from AidData's Global Chinese Development Finance Dataset, Version 3.0, which AidData publishes under the Open Data Commons Attribution License. AidData asks that the dataset be cited as both of the works below.

Custer, S., Dreher, A., Elston, T.B., Escobar, B., Fedorochko, R., Fuchs, A., Ghose, S., Lin, J., Malik, A., Parks, B.C., Solomon, K., Strange, A., Tierney, M.J., Vlasto, L., Walsh, K., Wang, F., Zaleski, L., and Zhang, S. 2023. Tracking Chinese Development Finance: An Application of AidData's TUFF 3.0 Methodology. Williamsburg, VA: AidData at William & Mary.

Dreher, A., Fuchs, A., Parks, B. C., Strange, A., & Tierney, M.J. 2022. Banking on Beijing: The Aims and Impacts of China's Overseas Development Program. Cambridge, UK: Cambridge University Press.

The estimates in `data/epoch_estimates.csv` come from Epoch AI's database of AI data centres, which Epoch AI publishes under the Creative Commons Attribution 4.0 licence and asks to be cited as below.

Epoch AI, 'AI data centers'. Published online at epoch.ai. Retrieved from 'https://epoch.ai/data/ai-data-centers' [online resource]. Accessed 22 October 2026.
