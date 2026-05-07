# Youth Civic Engagement & Voting Attitudes — Analysis

Sample: 83 SFUHS respondents collected April 2026 (67 students, 16 faculty/staff). All Likert items are 1–5.

## 1. Headline numbers

| Question | Students (Yes / No / Unsure) | Faculty (Yes / No / Unsure) |
|---|---|---|
| Lower **local** voting age to 16 | 44.8% / 40.3% / 14.9% | 56.2% / 25.0% / 18.8% |
| Lower **federal** voting age to 16 | 29.9% / 53.7% / 16.4% | 37.5% / 37.5% / 25.0% |

Both groups are more permissive about a *local* lowering than a *federal* one. Faculty are nominally more supportive than students of both, but the role × support contingency tables are not statistically significant in this sample (chi-square p = 0.52 for local, p = 0.49 for federal). With n = 16 on the faculty side, the test has very little power to detect anything but a large gap.

## 2. Self-reported engagement

Means on the 1–5 Likert items:

| Item | Students | Faculty |
|---|---|---|
| Follow local politics | 2.90 | 3.69 |
| Follow federal politics | 3.45 | 4.19 |
| Influence in local elections | 1.55 | — |
| Influence in federal elections | 1.39 | — |
| Views align with parents | 4.06 | — |
| Likelihood to vote in SF if eligible | 4.22 | — |
| 16–18 yr olds informed enough — local | 2.91 | 3.06 |
| 16–18 yr olds informed enough — federal | 2.78 | 2.81 |

Two patterns stand out. First, students rate themselves very high on parental alignment (mean 4.06 / 5) and very low on perceived influence (1.55 local, 1.39 federal). They believe their views match their parents' and that their vote does not matter much — which is exactly the combination opponents of lowering the age cite ("voting twice for the parent"). Second, students and faculty give nearly identical assessments of whether 16–18 year-olds are informed enough (means within 0.15 of each other). The disagreement between the groups is not really about competence; it's elsewhere.

## 3. What predicts a "Yes" among students?

I fit two L2-regularized logistic regressions on the student subsample (Unsure responses dropped, Likert features z-scored). These are exploratory — n=57 with 9 features, so coefficients are directional only.

**Local lowering (n=57, base "Yes" rate 53%, in-sample acc 95%):**
The strongest positive predictors are believing 16–18 year-olds are informed enough about *local* issues (+1.99) and about *federal* issues (+1.17). The strongest negative predictor is "follow local politics" (−1.00) — students who say they follow local politics closely are *less* likely to support a local lowering. Age is also negative (−0.41): younger students (9th–10th graders) lean more supportive than seniors. Alignment with parents is mildly positive (+0.49).

**Federal lowering (n=57, base "Yes" rate 35%, in-sample acc 91%):**
Similar shape. Believing 16–18 year-olds are informed enough — federally (+1.96) and locally (+0.90) — dominates. "Follow federal politics" is positive (+0.42). Likelihood to vote is mildly negative (−0.33).

The story the model tells: support tracks belief that one's peers are competent voters, much more than self-reported engagement or self-rated influence. Students who follow politics closely are slightly more skeptical, not less — they're aware of how unevenly informed the peer group is.

## 4. Correlations worth flagging (students)

- Age and grade correlate −0.41 / −0.41 with "16–18 year-olds informed enough — local." Older students are more skeptical of their peers' readiness.
- Likelihood to vote correlates +0.42 with informed-local and +0.34 with informed-federal. Students who would vote also believe peers are ready.
- Following local and federal politics correlate 0.55 with each other but only weakly with perceived peer readiness — closely-following students do not automatically endorse lowering the age.
- Self-reported "influence in local elections" (mean 1.55) is barely correlated with any informed-or-engagement variable. Students rate their influence as low almost universally.

## 5. Open-text themes

Substring counts in students' explanations (top hits): "inform" 13, "influenc" 12, "educat" 11, "local" 11, "federal" 10, "parent" 6, "mature" 5, "social media" 3, "cortex" 2. Faculty explanations + reasoning: "inform" 16, "educat" 9, "local" 4, "parent" 3, "mature" 2, "cortex" 2.

Two clusters of opposition appear repeatedly in student write-ins:

1. *Parental capture* — variants of "16-year-olds are influenced by their parents," "would essentially give parents 2 votes," "easily swayed."
2. *Brain development* — explicit references to "prefrontal cortex" / "frontal lobe," sometimes citing it as a hard biological argument.

The supportive arguments cluster around two ideas: (a) that local issues directly affect students so they should have a vote (housing, schools, transit), and (b) that the average adult voter is not noticeably more informed, so a competence bar excludes younger people unfairly.

A faculty respondent with a social-science background made the most-developed pro argument: parental partisanship is the number-one predictor for everyone's partisanship, so the "parents get two votes" objection generalizes; lowering the age might also create habit-forming voting behavior that would lift adult turnout.

## 6. News sources

Both groups rely heavily on traditional news (NYT, WSJ, SF Chronicle). Students supplement with social media (TikTok/Instagram/X) at much higher rates than faculty; faculty lean more on podcasts and traditional news. School and family/friends are also common student sources. Several open-text answers express explicit distrust of social media as a primary news source and tie that distrust to skepticism about peer voting readiness.

## 7. What the data does not say

- **Causal claims.** Cross-sectional, single-school, self-selected sample. None of these correlations imply causation.
- **Generalizability.** SFUHS is a private high school in San Francisco. The sample is not representative of California or US teenagers. The faculty respondent who flagged this — that SF teens are unusually engaged compared to teens elsewhere — is probably right.
- **Statistical significance.** The role × support chi-square tests do not clear conventional significance. With this sample size, the data is descriptive, not inferential.
- **Open-text analysis.** Substring counting is a crude summary. A richer analysis would code each response on multiple dimensions (concern type, reasoning style, valence) — feasible at this N if done by hand.

## 8. Bottom line

Among these respondents, support for a local 16+ lowering is roughly a coin flip; federal support is meaningfully lower. The strongest predictor of a student saying "Yes" is whether they believe their peers are informed enough — not their own engagement or self-rated influence. The most common reason for "No" is fear of parental capture and concerns about teen impressionability, often framed in developmental-biology terms. Faculty are slightly more supportive than students but disagree among themselves.

If the goal is to use this data to inform a position, the actionable observation is that the local/federal distinction matters more than the role distinction: respondents are notably more comfortable with 16-year-olds voting on issues that demonstrably affect their daily lives than on national questions.
