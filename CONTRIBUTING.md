# Instructions for this repository

## Project

The project records data-centre capacity outside mainland China in which Chinese firms and Chinese state lenders have a role, as owner, operator, tenant, builder, equipment supplier or financier. For each site it records how much of the capacity can run large AI workloads and which country's rules cover it. `codebook.md` defines the roles, the firms covered, the three levels of detail and every variable, and `README.md` gives the status and the next steps.

The project has two uses. The first is a public, open dataset with a dashboard for researchers on compute governance, regulators and journalists. The second is evidence of progress for a BlueDot Rapid Grant application, in which the AI-safety argument rests on the commercial and AI layer, not on the government data centres in the AidData layer.

## Data rules

1. Every value has a source. A row records the page that supports the row in `source_url` and what the page states in `source_note`.
2. A row stays `not_checked` until a script has downloaded the page and confirmed the value. Never mark a row `found` without that check.
3. Never fill a value from memory or estimate it without a source. Leave the cell empty instead.
4. A record that matched a search term by chance is coded `excluded` with the reason, so that the reading of every record can be checked.
5. AidData's GCDF 3.0 file is not committed. A person places it in `data/raw`, which `.gitignore` excludes, and `scripts/build_aiddata_layer.py` reads it from there.
6. The government data centre findings from AidData are held for an article pitched to Rest of World. Do not publish them elsewhere, for example in a blog post or a public summary, before the editor replies.

## Writing rules

These apply to the README, the codebook, commit messages and every text written for the owner of the repository.

- Write plain, rigorous academic English with British spelling, such as centre, organisation and licence.
- Use no em dashes and no figurative phrases. Write what a thing is or does, not what it resembles.
- Each sentence follows from the one before it, and each paragraph has more than one sentence.
- Give every number with its total or its unit, as in 38 of the 45 records or 300 kW.
- Define a term the first time it appears, and never refer back to something the text has not stated.
- Keep the owner's own wording when asked to fix a text. Change only what is wrong and say what was changed.

## Commands

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/build_aiddata_layer.py --candidates
.venv/bin/python -m unittest discover -s tests
```
