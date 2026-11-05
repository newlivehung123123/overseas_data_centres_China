# Instructions for this repository

## Project

The project records data-centre capacity outside mainland China in which Chinese firms and Chinese state lenders have a role, as owner, operator, tenant, builder, equipment supplier or financier. For each site it records how much of the capacity can run large AI workloads and which country's rules cover it. `codebook.md` defines the roles, the firms covered, the three levels of detail, the three grades of evidence and every variable, and `README.md` gives the status and the next steps.

The project has two uses. The first is a public, open dataset with a dashboard for researchers on compute governance, regulators and journalists. The second is evidence of progress for applications for research funding, in which the argument on AI safety rests on the sites, the AI chips and the rules, not on the government data centres from AidData.

## Data rules

1. Every value has a source. A row records the page that supports the row in `source_url` and a passage copied from the page in `source_quote`.
2. A row is marked `found` only when `scripts/check_sources.py` has downloaded the page and found the passage on it. Never mark a row `found` by hand.
3. Never fill a value from memory or estimate it without a source. Leave the cell empty instead.
4. A record that matched a search term by chance is coded `excluded` with the reason, so that the reading of every record can be checked.
5. AidData's GCDF 3.0 file is not committed. A person places it in `data/raw`, which `.gitignore` excludes, and `scripts/build_aiddata_layer.py` reads it from there.
6. The government data centre findings from AidData are held for an article pitched to Rest of World. Do not publish them elsewhere, for example in a blog post or a public summary, before the editor replies.
7. Every row carries a grade of evidence, primary, secondary or unconfirmed, as the codebook defines. The low bound of the capacity estimate counts only primary figures, so a grade is raised only when a source supports the higher grade.

## Writing rules

These apply to the README, the codebook, commit messages and every text written for the owner of the repository.

- Write plain, rigorous academic English with British spelling, such as centre, organisation and licence.
- Use no em dashes and no figurative phrases. Write what a thing is or does, not what it resembles.
- Each sentence follows from the one before it, and each paragraph has more than one sentence.
- Give every number with its total or its unit, as in 38 of the 45 records or 300 kW.
- Define a term the first time it appears, and never refer back to something the text has not stated.
- Name the subject of a sentence instead of writing it or its, and avoid figurative words such as arm, layer or hub.
- Keep the owner's own wording when asked to fix a text. Change only what is wrong and say what was changed.

## Commits

Every commit is authored and committed as the owner of the repository, Jason H., with the email 109253621+newlivehung123123@users.noreply.github.com. Commit messages carry no attribution lines, no links to sessions and no mention of any tool used to write the code.

## Commands

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/build_aiddata_layer.py --candidates
.venv/bin/python -m unittest discover -s tests
```
