# SFUHS Youth Civic Engagement & Voting Attitudes — Survey Dashboard

Interactive dashboard, knowledge scoring, and statistical analysis of an April 2026 survey at SFUHS on youth voting attitudes — lowering the local/federal voting age to 16, political engagement, news consumption, and how much young people actually know about local government.

**Live dashboard:** https://stu1124.github.io/sfuhs-civic-survey/

## Sample
- N = 83 (67 students, 16 faculty/staff)
- Single-school convenience sample, San Francisco

## What's in here

| File | What it is |
|---|---|
| `index.html` / `dashboard.html` | Self-contained interactive dashboard (Chart.js + Grid.js via CDN). Sections: Overview, The Question, Knowledge Scores, Attitudes, What Predicts Support, Explore, Method. |
| `ANALYSIS.md` | Written findings: knowledge scoring, descriptives, chi-square, correlation, logistic regression, qualitative themes, caveats. |
| `data/raw_survey.csv` | Original survey export. |
| `data/cleaned_survey.csv` | Long-form cleaned dataset — one row per respondent, normalized columns, plus all computed scores. |
| `data/dashboard_data.json` | Pre-computed metrics + per-respondent rows powering the dashboard. |
| `analyze.py` | Cleaning, knowledge scoring, statistics. Regenerates the JSON and cleaned CSV. |
| `build_dashboard.py` | Builds `index.html` by embedding `dashboard_data.json`. |

## Knowledge scoring

Every open-text answer is scored on a transparent, code-defined rubric so "knowledge" is measured, not asserted:

- **Mayor Knowledge Score (0–10)** — students. Points per verified fact about the actual SF mayor's (Daniel Lurie) 2026 agenda. Auditable per-response in the dashboard's Explore section.
- **Reasoning Depth Score (0–10)** — everyone. length + specificity + multi-perspective + nuance. Argument quality, independent of position.
- **Civic Skills Score (0–10)** — faculty. Civic-concept density on the "what skills matter" answer.
- **Engagement Index (0–100)** and **Civic Literacy Index (0–100)** — composite indices for students.

## Reproducing
```bash
pip install pandas numpy scipy scikit-learn
python analyze.py          # writes data/cleaned_survey.csv + data/dashboard_data.json
python build_dashboard.py  # writes index.html + dashboard.html
```

## Headline findings
- Local-16 support: 47% Yes overall; federal-16 support markedly lower at 31%.
- Mean student mayor-knowledge score is **1.33 / 10**; **49% of students scored 0** (no verifiable facts). Civic Literacy Index averages 25/100.
- Measured knowledge tracks **skepticism**, not enthusiasm: 12th-graders know the most and support a local lowering the least (17%); 9th-graders the reverse (71%).
- Strongest predictor of student "Yes" in logit: belief that 16–18 year-olds are informed enough — *not* the student's own engagement or measured knowledge.
- Common opposition themes: parental capture ("two votes for parent"), brain-development arguments. Common support themes: local impact, adult-voter parity.

Full detail in `ANALYSIS.md`.

## Caveats
Single-school convenience sample. Role × support chi-square is not statistically significant (p ≈ 0.5). Knowledge scores are reproducible keyword/structure heuristics, not human grading — a transparent proxy, auditable per-response, not a definitive measure. Modeling is exploratory; in-sample accuracy is inflated. Treat everything as descriptive.
