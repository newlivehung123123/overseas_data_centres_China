# Changelog

This file lists the versions of the dataset and the changes between them. Each version is identified by the commit on the branch `main` at which the version was complete, because the repository records no tags.

## Changes after version 0.2.0

1. A census of the 143 data-centre facilities that Baxtel lists in Greater Tokyo, in `config/tokyo_census.csv`. DayOne operates 2 of them, at Fuchu and Kodaira, and no source found names a Chinese link at the other 141. With Tokyo, the censuses cover 639 facilities in seven markets, and a role is recorded at 73 of them.
2. 14 further web searches, which raise the log to 91: 7 for Tokyo and 7 for named Chinese tenants at the largest operators of Johor, Greater Bangkok and Singapore, none of which found such a tenant.
3. Figures of total IT capacity from Bridge's own pages for 6 sites: 508 MW at MY06, 374 MW at MY07, 98 MW at MY01 and MY02 together, 48 MW at MY03, 193 MW in Chonburi and 0.2 MW in Samut Prakan. The low estimate of capacity under construction or planned rises from 5,052 MW to 6,163 MW and the high estimate from 6,006 MW to 6,984 MW, and without the 4 firms that count on origin alone the range rises from 1,259 MW to 1,917 MW to between 1,657 MW and 2,182 MW, because MY06 also has ByteDance as its anchor tenant.

## Version 0.2.0, 14 November 2026

Version 0.2.0 is commit `8d3204a` on the branch `main` and holds 879 graded rows, of which 208 rest on a primary source, 649 on a secondary source and 22 are unconfirmed, against 376 rows in version 0.1.0, of which 176 were primary, 185 secondary and 15 unconfirmed. Most of the 503 new rows belong to the censuses of five further markets.

### Additions

1. Censuses of the 20 data-centre facilities that Baxtel lists in Batam, the 88 in Greater Bangkok, the 110 in Singapore, the 90 in Greater Kuala Lumpur and the 104 in Jakarta, in `config/batam_census.csv`, `config/bangkok_census.csv`, `config/singapore_census.csv`, `config/kuala_lumpur_census.csv` and `config/jakarta_census.csv`. With the 84 facilities of Johor, the censuses cover 496 facilities, and a Chinese firm or a fund of a Chinese state lender holds a role at 52 of them.
2. A log of the 77 web searches behind the five new censuses, in `config/census_searches.csv`, and a script, `scripts/scan_census_pages.py`, that searches the Baxtel page of each of the 496 facilities for the names of Chinese firms and for places in mainland China and Hong Kong and writes `data/census_page_scan.csv`.
3. 22 new sites, which raise the count from 67 to 89 sites and the count of roles from 89 to 114: the site of RangeIDC in Batam, Aesler Greenix Mark 1 in Batam, the data centre of China Mobile International in Chonburi, the data centres of Beijing Haoyang, Stratus Technology and Galaxy Data Center in Rayong, the second site of AirTrunk in Singapore, Digital Realty's SIN11 facility in Singapore, the data centre of Bitdeer in Singapore, the site in Johor on which Bitdeer AI holds 86.8 MW, Bitdeer AI's site in Cyberjaya, the land that a subsidiary of DayOne is buying near Dengkil, the land in Kapar that Baxtel links to DayOne, the two data centres that NexAI plans in Cikarang and Batang, where Megaspeed's Indonesian subsidiary is named as a tenant, and 7 sites of Bridge Data Centres in Johor, Greater Kuala Lumpur and Greater Bangkok.
4. 4 new rules, which raise the count from 16 to 20: the draft US rule on renting Nvidia chips to Chinese AI firms through servers in Thailand and Singapore, as reported in August 2026, Singapore's advisory of April 2025, and two reported requirements of Nvidia for its cloud partners in Southeast Asia.
5. 3 new reports of AI chips, all of Bitdeer, which raise the count from 10 to 13.
6. A row on the share of revenue that GDS received from its largest customer in 2021, from the firm's filing at the Hong Kong Stock Exchange.
7. Primary sources from Thailand's Board of Investment for 6 sites in Thailand from Green Mountain for the data centre at Hamar in Norway, and from Bitdeer's update filed at the SEC for its site in Johor, which raise the grade of those rows from secondary to primary.
8. One standard for which firms count as Chinese: headquarters in mainland China, a controlling owner in mainland China, or origin in a firm that met one of those grounds. `config/firms.csv` records the grounds of 27 firms, parents and lenders with a passage for each, the source check refuses a role whose firm has no row, and the capacity estimate is also given without the 4 firms that count on origin alone.
9. `CHANGELOG.md` and the section on versions in `README.md`.

### Corrections

1. Four facilities of the census of Johor carried names that Baxtel invents for facilities whose names it withholds, such as "Hub Max" and "Station Gamma". The names are now empty, and the passages start at the words that Baxtel shows in place of the name.
2. The capacity estimate counted the whole planned total of a site beside the capacity already in service at the same site. Each estimate now counts only the part of a planned total that exceeds the capacity in service, so the 150 MW planned at Hamar adds 60 MW to the 90 MW in service.
3. The capacity estimate now leaves out sites at which a Chinese firm is only the builder or the supplier of equipment, because the codebook counts the capacity of a site only where a Chinese firm owns, operates, rents, uses or finances the site.
4. The row on the land of Megaspeed in Johor now records that the purchase was completed in September 2026.
5. Version 0.1.0 left Bridge Data Centres out because Bridge has never had a controlling owner in mainland China, a test that would also have left out DayOne. Under the standard of version 0.2.0, Bridge counts by its origin in ChinData Group, which had its headquarters in Beijing, and 23 facilities of Bridge in the censuses of Johor, Greater Kuala Lumpur and Greater Bangkok are recoded as operator. The 4 buildings of MY06, where ByteDance is the anchor tenant, are now coded by their operator, because the census codes the first of operator, owner, tenant and financier.

### Effect on the capacity estimate

The low estimate of capacity in service rose from 1,323 MW in version 0.1.0 to 1,416 MW, and the high estimate rose from 1,652 MW to 1,654 MW. The capacity under construction or planned rose from between 4,183 MW and 5,041 MW to between 5,052 MW and 6,006 MW, mainly because of the data centres in Rayong that Thailand's Board of Investment approved, Bitdeer AI's site in Cyberjaya and the two data centres of NexAI in Indonesia. Without the 4 firms that count as Chinese on their origin alone, version 0.2.0 gives between 452 MW and 585 MW in service and between 1,259 MW and 1,917 MW under construction or planned. The public post of November 2026, "Where Chinese AI firms rent the chips they cannot buy", gives the figures of version 0.1.0.

## Version 0.1.0, 10 November 2026

Version 0.1.0 is commit 80c3d88, the dataset that the public post of November 2026 describes. The version holds 67 sites in 17 countries and territories, 89 roles of Chinese firms and funds, 10 reports of AI chips, 16 rules and a census of the 84 data-centre facilities that Baxtel lists in Johor. The low and high capacity estimates give between 1,323 MW and 1,652 MW in service and between 4,183 MW and 5,041 MW under construction or planned.
