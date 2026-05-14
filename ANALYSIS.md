# Youth Civic Engagement & Voting Attitudes — Analysis

Sample: 83 SFUHS respondents collected April 2026 (67 students, 16 faculty/staff). All Likert items are 1–5. This version adds rubric-based knowledge scoring of the open-text answers.

## 1. Headline numbers

| Question | Students (Yes / No / Unsure) | Faculty (Yes / No / Unsure) |
|---|---|---|
| Lower **local** voting age to 16 | 44.8% / 40.3% / 14.9% | 56.2% / 25.0% / 18.8% |
| Lower **federal** voting age to 16 | 29.9% / 53.7% / 16.4% | 37.5% / 37.5% / 25.0% |

Whole-sample "Yes": 47.0% local, 31.3% federal. Both groups are more permissive about a *local* lowering than a *federal* one. Faculty are nominally more supportive than students, but the role × support contingency tables are not statistically significant (chi-square p = 0.52 local, p = 0.49 federal). With n = 16 faculty, the test has very little power.

## 2. Knowledge scoring — the new layer

Every open-text answer is scored on a fixed, code-defined rubric so "knowledge" is measured rather than asserted. Three scores plus two composites:

- **Mayor Knowledge Score (0–10), students.** Students were asked what they know about the current SF mayor (Daniel Lurie). Answers are checked against verified facts about his actual 2026 agenda — Family Zoning Plan (signed Dec 2025), ~$643M budget deficit, November charter-reform ballot measure with Board President Mandelman, affordability/childcare pivot, homelessness and fentanyl focus, downtown recovery, sister-city diplomacy. Naming him scores +2; each specific verified policy +1 to +1.5.
- **Reasoning Depth Score (0–10), everyone.** Argument quality of the "explain your answer" text: length (0–3) + specificity (0–3) + multi-perspective markers (0–2) + nuance/concession (0–2). Independent of which side the respondent took.
- **Civic Skills Score (0–10), faculty.** Civic-concept density + length on the "what skills matter most" answer.
- **Engagement Index (0–100), students.** Mean of follow-local, follow-federal, likelihood-to-vote, rescaled.
- **Civic Literacy Index (0–100), students.** 40% mayor knowledge + 35% reasoning depth + 25% political following.

### What the scores reveal

**Civic knowledge of city government is thin.** Mean mayor knowledge among students is **1.33 / 10**, and **49.3% scored 0** — they left the question blank or named nothing verifiable. Only 2 of 67 students scored 6 or above. Reasoning depth is also low: students average **1.73 / 10**, faculty **2.55 / 10** — most student explanations are short and single-angle. The Civic Literacy Index averages **24.9 / 100**, dragged down by the two measured components; self-reported following alone (which students rate around 3/5) would look far healthier. The gap between how engaged students *say* they are and what they can *demonstrate* is the central finding the scoring exposes.

**Engagement is not knowledge.** The Engagement Index (mean 63.1/100, built from self-ratings) correlates only weakly with measured mayor knowledge (r ≈ 0.17). Feeling politically engaged and being able to name what the mayor is doing are nearly unrelated in this sample.

## 3. Knowledge tracks skepticism, not enthusiasm

This is the most striking pattern the scoring surfaces. Support for lowering the age is **inversely** related to measured knowledge and to age/grade:

| Grade | n | % Yes (local) | Avg mayor knowledge |
|---|---|---|---|
| 9 | 21 | 71.4% | 1.21 |
| 10 | 15 | 46.7% | 0.70 |
| 11 | 19 | 31.6% | 1.26 |
| 12 | 12 | 16.7% | 2.42 |

Twelfth-graders know the most and support a local lowering the least (16.7%); ninth-graders know the least and support it the most (71.4%). In the student logistic regression, **mayor knowledge score carries a negative coefficient** for local support (−0.56 standardized), and "follow local politics" is also negative (−0.99). The students who can actually describe city government lean against extending the vote to 16-year-olds — consistent with the most common written objection, which is precisely that peers are not informed enough.

By knowledge band, the relationship is non-monotonic but clearly not "more knowledge → more support": the "None" band is 36% Yes, "Low" 78%, "Medium" 29%, "High" 0% (n=2). The bands are small, so read loosely, but no version of the data shows knowledge driving enthusiasm.

## 4. Self-reported attitudes

| Item | Students | Faculty |
|---|---|---|
| Follow local politics | 2.90 | 3.69 |
| Follow federal politics | 3.45 | 4.19 |
| Influence in local elections | 1.55 | — |
| Influence in federal elections | 1.39 | — |
| Views align with parents | 4.06 | — |
| Likelihood to vote in SF if eligible | 4.22 | — |
| 16–18 informed enough — local | 2.91 | 3.06 |
| 16–18 informed enough — federal | 2.78 | 2.81 |

Students rate their own influence very low (≈1.5/5) and their alignment with parents very high (≈4/5) — exactly the "parents get two votes" combination that opponents cite. Students and faculty give nearly identical assessments of teen informedness (within 0.15). Notably, **mayor knowledge correlates −0.36 with self-reported parental alignment**: students who know more about city government are somewhat less likely to say their views simply track their parents'.

## 5. What predicts a student "Yes"

L2-regularized logistic regression, student subsample, Unsure dropped, features z-scored. Exploratory only — n ≈ 57 with 11 features, in-sample accuracy inflated.

**Local lowering.** Strongest positive predictors: believing 16–18 year-olds are informed enough — local (+2.01) and federal (+1.11), and reasoning depth (+0.80). Strongest negative: follow-local-politics (−0.99), mayor knowledge (−0.56), age (−0.37). Support tracks *belief that peers are competent*, not the respondent's own engagement or measured knowledge — and the people who follow politics and score higher on knowledge are more skeptical.

**Federal lowering.** Similar shape; belief-in-peer-informedness dominates again.

## 6. Open-text themes

Student explanation keyword hits: "inform" 13, "influenc" 12, "educat" 11, "local" 11, "federal" 10, "parent" 6, "mature" 5, "cortex" 2. Faculty: "inform" 16, "educat" 9. Two opposition clusters recur in student write-ins: **parental capture** ("would essentially give parents 2 votes," "easily swayed") and **brain development** ("prefrontal cortex," "frontal lobe"). Supportive arguments cluster on **local impact** (housing, schools, transit affect students directly) and **adult-voter parity** ("most adults aren't informed either").

## 7. News sources

Both groups rely heavily on traditional news. Students add social media (TikTok/Instagram/X) at much higher rates than faculty; faculty lean on podcasts and traditional outlets. Average mayor knowledge does not differ dramatically by source — and because most students select several sources, the subgroups overlap heavily, so source-to-knowledge differences should not be over-read.

## 8. What the data does not say

- **Causality.** Cross-sectional, single-school, self-selected. Correlations are not effects.
- **Generalizability.** SFUHS is a private SF high school; the sample is not representative of SF, California, or US teenagers.
- **Significance.** Role × support chi-square tests do not clear conventional thresholds. Descriptive, not inferential.
- **Scores are heuristics.** The rubrics use keyword and structure matching, not human grading or NLP. They reward mentioning verifiable facts and structured argument; they can miss correct knowledge phrased unusually, or reward name-dropping. Their value is being transparent and reproducible — every score is auditable in the dashboard's Explore section. They are a proxy for knowledge, not a definitive measure of it.
- **Models.** Logistic regressions are exploratory; coefficients are directional only.

## 9. Bottom line

Support for a local 16+ lowering is roughly a coin flip (47%); federal support is markedly lower (31%). The knowledge scoring exposes a real gap between self-reported engagement and demonstrable knowledge: half of students could not name a single verifiable fact about their own mayor, and the Civic Literacy Index averages only 25/100. And measured knowledge runs *against* support — older, more knowledgeable students are the most skeptical, echoing the dominant written objection that 16-year-olds are not informed enough. The clearest actionable observation remains that the local/federal distinction matters more than the role distinction: respondents are far more comfortable with 16-year-olds voting on issues that demonstrably affect their daily lives.
