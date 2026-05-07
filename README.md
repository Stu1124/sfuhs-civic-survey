# SFUHS Youth Civic Engagement & Voting Attitudes — Survey Dashboard

Interactive dashboard and statistical analysis of an April 2026 survey at SFUHS on youth voting attitudes (lowering local/federal voting age to 16, civic engagement, news consumption).

**Live dashboard:** see the published GitHub Pages URL for this repo.

## Sample
- N = 83 (67 students, 16 faculty/staff)
- Single-school convenience sample, San Francisco

## What's in here

| File | What it is |
|---|---|
| `index.html` / `dashboard.html` | Self-contained interactive dashboard (Chart.js + Grid.js via CDN). Open in any browser. |
| `ANALYSIS.md` | Written findings: descriptives, chi-square, correlation, logistic regression, qualitative themes, caveats. |
| `data/raw_survey.csv` | Original survey export. |
| `data/cleaned_survey.csv` | Long-form cleaned dataset (one row per respondent, normalized columns). |
| `data/dashboard_data.json` | Pre-computed metrics powering the dashboard. |
| `analyze.py` | Cleaning + statistical analysis script. Regenerates the JSON and cleaned CSV. |
| `build_dashboard.py` | Builds `index.html` by embedding `dashboard_data.json`. |

## Reproducing
```bash
pip install pandas numpy scipy scikit-learn
python analyze.py          # writes data/cleaned_survey.csv + data/dashboard_data.json
python build_dashboard.py  # writes index.html
```

## Headline findings
- Local-16 support: students 45/40/15 (Yes/No/Unsure), faculty 56/25/19. Federal-16 support is notably lower for both.
- Role × support chi-square is not statistically significant (p ≈ 0.5 for both questions) — small N.
- Strongest predictor of student "Yes" in logit: belief that 16–18 year-olds are informed enough — *not* their own engagement.
- Common opposition themes: parental capture ("two votes for parent"), brain-development arguments. Common support themes: local-impact, adult-voter parity.

Full detail in `ANALYSIS.md`.

## Caveats
Single-school convenience sample. The modeling (n=57 after dropping Unsure) is exploratory; in-sample accuracy is inflated. Treat as descriptive.
