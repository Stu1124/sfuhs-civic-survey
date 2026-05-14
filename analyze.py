"""
Youth Civic Engagement Survey - Analysis & Knowledge Scoring (v2)
=================================================================
Pipeline:
  1. Load + clean the raw Google Form export (separate student/faculty blocks).
  2. Score every open-text answer on transparent, documented rubrics:
       - mayor_knowledge_score   (0-10)  factual recall, students
       - reasoning_depth_score   (0-10)  argument quality, everyone
       - civic_skills_score      (0-10)  articulation of civic literacy, faculty
  3. Build composite indices:
       - engagement_index        (0-100) self-reported following + vote intent
       - civic_literacy_index    (0-100) knowledge + reasoning + engagement
  4. Run descriptive stats, chi-square, correlations, logistic regression.
  5. Export cleaned CSV + a single JSON the dashboard reads.

All scoring rules are kept in code (see RUBRIC docstrings) so they are
reproducible and auditable. Facts about SF Mayor Daniel Lurie verified
against news sources, May 2026.
"""
import pandas as pd
import numpy as np
import json, re
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

raw = pd.read_csv("data/raw_survey.csv")

# ----------------------------------------------------------------------
# 1. CLEAN  -- the form has a student block (cols 1-16) and a faculty
#    block (cols 17-28). Reshape into one tidy row per respondent.
# ----------------------------------------------------------------------
records = []
for _, row in raw.iterrows():
    role = row.iloc[1]
    if role == "Student":
        rec = dict(
            role="Student", age=row.iloc[2], grade=row.iloc[3],
            follow_local=row.iloc[4], follow_federal=row.iloc[5],
            influence_local=row.iloc[6], influence_federal=row.iloc[7],
            align_parents=row.iloc[8], support_local_16=row.iloc[9],
            support_federal_16=row.iloc[10], explanation=row.iloc[11],
            likelihood_vote=row.iloc[12], informed_local=row.iloc[13],
            informed_federal=row.iloc[14], mayor_knowledge_text=row.iloc[15],
            news_sources=row.iloc[16], subject=None, years_in_ed=None,
            civic_skills_text=None, reasoning_text=None,
        )
    else:
        rec = dict(
            role="Faculty", age=None, grade=None,
            follow_local=row.iloc[19], follow_federal=row.iloc[20],
            influence_local=None, influence_federal=None, align_parents=None,
            support_local_16=row.iloc[21], support_federal_16=row.iloc[22],
            explanation=row.iloc[23], likelihood_vote=None,
            informed_local=row.iloc[24], informed_federal=row.iloc[25],
            mayor_knowledge_text=None, news_sources=row.iloc[28],
            subject=row.iloc[17], years_in_ed=row.iloc[18],
            civic_skills_text=row.iloc[27], reasoning_text=row.iloc[26],
        )
    records.append(rec)

df = pd.DataFrame(records)
df.insert(0, "id", range(1, len(df) + 1))

for c in ["age", "grade", "follow_local", "follow_federal", "influence_local",
          "influence_federal", "align_parents", "likelihood_vote",
          "informed_local", "informed_federal"]:
    df[c] = pd.to_numeric(df[c], errors="coerce")


# ----------------------------------------------------------------------
# 2. KNOWLEDGE SCORING
# ----------------------------------------------------------------------
def _clean(t):
    return "" if (t is None or (isinstance(t, float) and np.isnan(t))) else str(t).strip()

NULL_ANSWERS = {"", "idk", "i dont know", "i don't know", "no idea", "no idea lmao",
                "none", "n/a", "na", "nothing", "no", "not much", "."}

# --- 2a. Mayor knowledge rubric (students) --------------------------------
# Each tuple: (regex, points, label). Daniel Lurie is SF's actual mayor
# (took office Jan 2025). Facts verified against news, May 2026:
#   Family Zoning Plan signed Dec 2025; ~$643M budget deficit; charter
#   reform Nov ballot measure w/ Board Pres. Mandelman; affordability +
#   childcare agenda; homelessness/fentanyl focus; downtown recovery;
#   Tipping Point founder / Levi Strauss heir; sister-city diplomacy.
MAYOR_RUBRIC = [
    (r"\blurie\b",                                          2.0, "Names the mayor (Lurie)"),
    (r"\bdaniel\b",                                         0.5, "Knows first name"),
    (r"democrat|moderate|left|progressive|centrist",        1.0, "Party / ideology"),
    (r"homeless|encampment",                                1.0, "Homelessness focus"),
    (r"drug|fentanyl|overdose|addiction",                   1.0, "Drug crisis focus"),
    (r"downtown|econom|small business|touris|revitaliz|revive|bring .*back", 1.0, "Downtown / economic recovery"),
    (r"crime|public safety|police|safe[r]?\b",              1.0, "Public safety / crime"),
    (r"budget|deficit|\$6\d\d|643|billion|cuts?\b|fiscal",  1.5, "Budget deficit / fiscal challenge"),
    (r"zoning|housing|sb ?79|affordab|childcare|child care",1.5, "Housing / zoning / affordability"),
    (r"charter",                                            1.5, "Charter reform"),
    (r"shanghai|beijing|china|sister cit",                  1.0, "Sister-city diplomacy"),
    (r"climate",                                            1.0, "Climate plan"),
    (r"tiktok|instagram|social media|influencer|posts? on", 0.5, "Media presence"),
    (r"let'?s go san francisco|lets go sf",                 0.5, "Campaign slogan"),
    (r"tipping point|levi|wealthy|rich|billionaire|nonprofit", 1.0, "Background (wealth / Tipping Point)"),
]

def score_mayor_knowledge(text):
    """0-10 factual recall score. Returns (score, hit_labels)."""
    t = _clean(text).lower()
    if t in NULL_ANSWERS or len(t) < 3:
        return 0.0, []
    score, hits = 0.0, []
    for pattern, pts, label in MAYOR_RUBRIC:
        if re.search(pattern, t):
            score += pts
            hits.append(label)
    # A non-empty but factually empty answer still shows engagement effort.
    if score == 0 and len(t) > 8:
        score = 0.5
        hits.append("Attempted, no verifiable facts")
    return round(min(score, 10.0), 2), hits

# --- 2b. Reasoning depth rubric (everyone) --------------------------------
# Measures *argument quality*, not opinion. Components:
#   length (0-3) | specificity (0-3) | multi-perspective (0-2) | nuance (0-2)
NUANCE_MARKERS   = [" but ", " however", " although", " though", " while ",
                    " on the other hand", " whereas", " yet "]
CONCESSION_MARKERS = ["not all", "some ", "depends", "to some degree", "i concede",
                      "not necessarily", "at the same time", "even if", "i worry",
                      "i'm not sure", "im not sure"]
SPECIFIC_MARKERS = ["local", "federal", "prefrontal", "cortex", "frontal lobe",
                    "turnout", "habit", "civics", "education", "informed",
                    "research", "ballot", "prop", "policy", "misinformation",
                    "critical thinking", "economic", "housing", "rights",
                    "constitution", "drive", "work", "tax"]

def score_reasoning_depth(text):
    """0-10 argument-quality score. Returns (score, parts dict)."""
    t = _clean(text)
    tl = t.lower()
    if tl in NULL_ANSWERS or len(tl) < 4:
        return 0.0, {"length": 0, "specificity": 0, "perspective": 0, "nuance": 0, "words": 0}
    words = len(re.findall(r"\w+", t))
    # length: 0-3
    length = min(3.0, words / 25.0)
    # specificity: 0-3, distinct concept markers present
    spec_hits = sum(1 for mk in SPECIFIC_MARKERS if mk in tl)
    specificity = min(3.0, spec_hits * 0.6)
    # multi-perspective: 0-2
    persp_hits = sum(1 for mk in NUANCE_MARKERS if mk in tl)
    perspective = min(2.0, persp_hits * 1.0)
    # nuance / concession: 0-2
    nuance_hits = sum(1 for mk in CONCESSION_MARKERS if mk in tl)
    nuance = min(2.0, nuance_hits * 1.0)
    score = length + specificity + perspective + nuance
    return round(min(score, 10.0), 2), {
        "length": round(length, 2), "specificity": round(specificity, 2),
        "perspective": round(perspective, 2), "nuance": round(nuance, 2),
        "words": words,
    }

# --- 2c. Civic-skills articulation (faculty) ------------------------------
# Faculty answered "what civic knowledge/skills matter most for voting?"
# Score how concretely they articulate civic literacy concepts.
CIVIC_CONCEPTS = ["critical think", "evidence", "evaluat", "government", "structure",
                  "function", "rights", "amendment", "constitution", "empathy",
                  "perspective", "data", "misinformation", "bias", "history",
                  "candidate", "ballot", "proposition", "implications", "impact",
                  "listening", "geography", "economics", "finance", "values"]

def score_civic_skills(text):
    t = _clean(text).lower()
    if t in NULL_ANSWERS or len(t) < 4:
        return 0.0, {"concepts": 0, "words": 0}
    words = len(re.findall(r"\w+", t))
    concept_hits = sum(1 for mk in CIVIC_CONCEPTS if mk in t)
    # concepts 0-7, length bonus 0-3
    score = min(7.0, concept_hits * 1.4) + min(3.0, words / 30.0)
    return round(min(score, 10.0), 2), {"concepts": concept_hits, "words": words}

# Apply scoring
mayor_scores, mayor_hits = [], []
for t in df["mayor_knowledge_text"]:
    s, h = score_mayor_knowledge(t)
    mayor_scores.append(s); mayor_hits.append(h)
df["mayor_knowledge_score"] = mayor_scores
df["mayor_knowledge_hits"] = mayor_hits

reason_scores, reason_parts = [], []
for t in df["explanation"]:
    s, p = score_reasoning_depth(t)
    reason_scores.append(s); reason_parts.append(p)
df["reasoning_depth_score"] = reason_scores
df["reasoning_parts"] = reason_parts

# faculty reasoning_text also gets a depth score (their longer answer)
fac_reason = []
for _, r in df.iterrows():
    if r["role"] == "Faculty":
        s, _ = score_reasoning_depth(r["reasoning_text"])
        fac_reason.append(s)
    else:
        fac_reason.append(np.nan)
df["faculty_reasoning_score"] = fac_reason

civic_scores, civic_parts = [], []
for t in df["civic_skills_text"]:
    s, p = score_civic_skills(t)
    civic_scores.append(s); civic_parts.append(p)
df["civic_skills_score"] = civic_scores

# ----------------------------------------------------------------------
# 3. COMPOSITE INDICES
# ----------------------------------------------------------------------
# Engagement index (0-100): mean of follow_local, follow_federal,
# likelihood_vote -- each 1-5 -> rescaled.
def to_100(series_1to5):
    return (series_1to5 - 1) / 4 * 100

df["engagement_index"] = np.nan
stu_mask = df["role"] == "Student"
eng = (to_100(df.loc[stu_mask, "follow_local"]) +
       to_100(df.loc[stu_mask, "follow_federal"]) +
       to_100(df.loc[stu_mask, "likelihood_vote"])) / 3
df.loc[stu_mask, "engagement_index"] = eng.round(1)

# Civic literacy index (0-100), students: blends factual knowledge (40%),
# reasoning quality (35%), and self-reported following (25%).
df["civic_literacy_index"] = np.nan
follow_component = (to_100(df.loc[stu_mask, "follow_local"]) +
                    to_100(df.loc[stu_mask, "follow_federal"])) / 2
lit = (df.loc[stu_mask, "mayor_knowledge_score"] * 10 * 0.40 +
       df.loc[stu_mask, "reasoning_depth_score"] * 10 * 0.35 +
       follow_component * 0.25)
df.loc[stu_mask, "civic_literacy_index"] = lit.round(1)

# Knowledge band (categorical, for grouping)
def band(s):
    if pd.isna(s): return None
    if s >= 6: return "High (6-10)"
    if s >= 3: return "Medium (3-5.9)"
    if s > 0:  return "Low (0.1-2.9)"
    return "None (0)"
df["mayor_knowledge_band"] = df["mayor_knowledge_score"].apply(band)

print("=== Sample ===")
print(df["role"].value_counts().to_dict())
print("\n=== Mayor knowledge score (students) ===")
sk = df.loc[stu_mask, "mayor_knowledge_score"]
print(f"mean={sk.mean():.2f} median={sk.median():.2f} max={sk.max()} "
      f"%zero={100*(sk==0).mean():.0f}%")
print(df.loc[stu_mask, "mayor_knowledge_band"].value_counts().to_dict())
print("\n=== Reasoning depth score (all) ===")
print(f"student mean={df.loc[stu_mask,'reasoning_depth_score'].mean():.2f} "
      f"faculty mean={df.loc[~stu_mask,'reasoning_depth_score'].mean():.2f}")
print("\n=== Civic skills score (faculty) ===")
print(f"mean={df.loc[~stu_mask,'civic_skills_score'].mean():.2f}")
print("\n=== Civic literacy index (students) ===")
print(df.loc[stu_mask, "civic_literacy_index"].describe().round(1).to_dict())


# ----------------------------------------------------------------------
# 4. STATS
# ----------------------------------------------------------------------
def pct(series):
    return (series.value_counts(dropna=False, normalize=True).round(4) * 100).to_dict()

summary = {}
summary["n_total"] = int(len(df))
summary["n_student"] = int(stu_mask.sum())
summary["n_faculty"] = int((~stu_mask).sum())
summary["support_local_by_role"] = {r: pct(g["support_local_16"]) for r, g in df.groupby("role")}
summary["support_federal_by_role"] = {r: pct(g["support_federal_16"]) for r, g in df.groupby("role")}

# Likert means
likert_cols = ["follow_local", "follow_federal", "influence_local", "influence_federal",
               "align_parents", "likelihood_vote", "informed_local", "informed_federal"]
likert_means = {}
for c in likert_cols:
    g = df.groupby("role")[c].agg(["mean", "std", "count"])
    likert_means[c] = {}
    for r in ["Student", "Faculty"]:
        if r in g.index and not pd.isna(g.loc[r, "mean"]):
            likert_means[c][r] = {"mean": round(float(g.loc[r, "mean"]), 2),
                                  "std": round(float(g.loc[r, "std"]), 2) if not pd.isna(g.loc[r,"std"]) else None,
                                  "n": int(g.loc[r, "count"])}
        else:
            likert_means[c][r] = {"mean": None, "std": None, "n": 0}
summary["likert_means"] = likert_means

# Full distributions for each Likert item (for histograms)
distributions = {}
for c in likert_cols:
    distributions[c] = {}
    for r in ["Student", "Faculty"]:
        sub = df[df.role == r][c].dropna()
        if len(sub):
            vc = sub.round(0).astype(int).value_counts().sort_index()
            distributions[c][r] = {str(k): int(v) for k, v in vc.items()}
# score distributions in bins
for c in ["mayor_knowledge_score", "reasoning_depth_score"]:
    distributions[c] = {}
    for r in ["Student", "Faculty"]:
        sub = df[df.role == r][c].dropna()
        if len(sub):
            vc = pd.cut(sub, bins=[-0.01, 0, 2, 4, 6, 8, 10.01],
                        labels=["0", "0-2", "2-4", "4-6", "6-8", "8-10"]).value_counts().sort_index()
            distributions[c][r] = {str(k): int(v) for k, v in vc.items()}
summary["distributions"] = distributions

# News sources
def split_sources(s):
    s = _clean(s)
    if not s: return []
    parts, depth, cur = [], 0, ""
    for ch in s:
        if ch == "(": depth += 1
        elif ch == ")": depth -= 1
        if ch == "," and depth == 0:
            parts.append(cur.strip()); cur = ""
        else:
            cur += ch
    if cur.strip(): parts.append(cur.strip())
    return parts

CANON_SOURCES = ["Social media (TikTok, Instagram, X)", "YouTube", "Podcasts",
                 "Traditional news (NYT, WSJ, SF Chronicle)", "Family or friends",
                 "School", "Other"]
df["news_list"] = df["news_sources"].apply(split_sources)
news_counts = {}
for r in ["Student", "Faculty"]:
    sub = df[df.role == r]
    news_counts[r] = {}
    for src in CANON_SOURCES:
        key = src.split(" (")[0]
        cnt = sub["news_list"].apply(lambda L: any(key in x for x in L)).sum()
        news_counts[r][src] = int(cnt)
summary["news_counts"] = news_counts
df["news_diversity"] = df["news_list"].apply(len)

# news source vs mean knowledge (students) -- does source mix track knowledge?
src_knowledge = {}
for src in CANON_SOURCES:
    key = src.split(" (")[0]
    sub = df[stu_mask & df["news_list"].apply(lambda L: any(key in x for x in L))]
    if len(sub):
        src_knowledge[src] = {"n": int(len(sub)),
                              "mean_mayor_knowledge": round(float(sub["mayor_knowledge_score"].mean()), 2),
                              "mean_engagement": round(float(sub["engagement_index"].mean()), 1)}
summary["source_knowledge"] = src_knowledge

# Chi-square: role x support
def chi2(col):
    tab = pd.crosstab(df["role"], df[col])
    c, p, dof, _ = stats.chi2_contingency(tab)
    return {"chi2": round(float(c), 3), "p": round(float(p), 4), "dof": int(dof),
            "table": {str(k): {str(kk): int(vv) for kk, vv in v.items()}
                      for k, v in tab.to_dict("index").items()}}
summary["chi2"] = {"role_x_local": chi2("support_local_16"),
                   "role_x_federal": chi2("support_federal_16")}

# Support by grade (students)
grade_support = {}
for g, sub in df[stu_mask].groupby("grade"):
    if pd.isna(g): continue
    grade_support[int(g)] = {
        "n": int(len(sub)),
        "local": pct(sub["support_local_16"]),
        "federal": pct(sub["support_federal_16"]),
        "mean_mayor_knowledge": round(float(sub["mayor_knowledge_score"].mean()), 2),
        "mean_engagement": round(float(sub["engagement_index"].mean()), 1),
        "mean_reasoning": round(float(sub["reasoning_depth_score"].mean()), 2),
    }
summary["grade_support"] = grade_support

# Support by knowledge band (students) -- does knowing more change views?
band_order = ["None (0)", "Low (0.1-2.9)", "Medium (3-5.9)", "High (6-10)"]
band_support = {}
for b in band_order:
    sub = df[stu_mask & (df["mayor_knowledge_band"] == b)]
    if len(sub):
        band_support[b] = {"n": int(len(sub)),
                           "local": pct(sub["support_local_16"]),
                           "federal": pct(sub["support_federal_16"]),
                           "mean_engagement": round(float(sub["engagement_index"].mean()), 1)}
summary["band_support"] = band_support

# Faculty: by years in education and subject
fac = df[~stu_mask]
summary["faculty_by_years"] = {
    str(y): {"n": int(len(s)), "local": pct(s["support_local_16"]),
             "federal": pct(s["support_federal_16"])}
    for y, s in fac.groupby("years_in_ed")
}
summary["faculty_by_subject"] = {
    str(sj): {"n": int(len(s)),
              "local_yes": int((s["support_local_16"] == "Yes").sum()),
              "mean_civic_skills": round(float(s["civic_skills_score"].mean()), 2)}
    for sj, s in fac.groupby("subject")
}

# Correlation matrix (students) -- now includes the new scores
corr_cols = ["age", "grade", "follow_local", "follow_federal", "influence_local",
             "influence_federal", "align_parents", "likelihood_vote",
             "informed_local", "informed_federal", "mayor_knowledge_score",
             "reasoning_depth_score", "engagement_index", "civic_literacy_index",
             "news_diversity"]
corr = df[stu_mask][corr_cols].corr().round(3)
summary["correlations"] = {k: {kk: (None if pd.isna(vv) else float(vv))
                               for kk, vv in v.items()}
                           for k, v in corr.to_dict("index").items()}

# Logistic regression (students, Yes/No only)
m = df[stu_mask & df["support_local_16"].isin(["Yes", "No"])].copy()
m["y_local"] = (m["support_local_16"] == "Yes").astype(int)
m2 = df[stu_mask & df["support_federal_16"].isin(["Yes", "No"])].copy()
m2["y_federal"] = (m2["support_federal_16"] == "Yes").astype(int)
features = ["age", "follow_local", "follow_federal", "influence_local",
            "influence_federal", "align_parents", "informed_local",
            "informed_federal", "likelihood_vote", "mayor_knowledge_score",
            "reasoning_depth_score"]

def fit_logit(frame, ycol):
    X = frame[features].apply(pd.to_numeric, errors="coerce")
    X = X.fillna(X.mean())
    Xs = StandardScaler().fit_transform(X)
    y = frame[ycol].values
    if len(np.unique(y)) < 2: return None
    lr = LogisticRegression(max_iter=1000, solver="liblinear")
    lr.fit(Xs, y)
    return {"intercept": round(float(lr.intercept_[0]), 3),
            "coefs": {f: round(float(c), 3) for f, c in zip(features, lr.coef_[0])},
            "accuracy": round(float(lr.score(Xs, y)), 3),
            "n": int(len(y)),
            "support_yes_rate": round(float(np.mean(y)), 3)}

summary["logit_local_student"] = fit_logit(m, "y_local")
summary["logit_federal_student"] = fit_logit(m2, "y_federal")

# Support pattern: local vs federal divergence
def support_pattern(r):
    l, f = r["support_local_16"], r["support_federal_16"]
    if l == "Yes" and f == "Yes": return "Both"
    if l == "Yes" and f != "Yes": return "Local only"
    if l != "Yes" and f == "Yes": return "Federal only"
    if l == "No" and f == "No":   return "Neither"
    return "Mixed/Unsure"
df["support_pattern"] = df.apply(support_pattern, axis=1)
summary["support_pattern"] = {r: pct(g["support_pattern"]) for r, g in df.groupby("role")}

# Keyword themes
THEMES = ["parent", "influenc", "mature", "inform", "educat", "brain", "cortex",
          "social media", "manipulat", "local", "federal", "biased", "critical",
          "misinformation", "research", "responsib", "habit", "turnout"]
def kw(series):
    text = " ".join(_clean(x).lower() for x in series)
    return {k: text.count(k) for k in THEMES}
summary["keywords_student"] = kw(df[stu_mask]["explanation"])
summary["keywords_faculty"] = kw(pd.concat([df[~stu_mask]["explanation"].fillna(""),
                                            df[~stu_mask]["reasoning_text"].fillna("")]))

# Headline KPIs
summary["headline"] = {
    "support_local_yes_overall": round(float((df["support_local_16"] == "Yes").mean()) * 100, 1),
    "support_federal_yes_overall": round(float((df["support_federal_16"] == "Yes").mean()) * 100, 1),
    "mean_mayor_knowledge_student": round(float(df[stu_mask]["mayor_knowledge_score"].mean()), 2),
    "pct_mayor_knowledge_zero": round(float((df[stu_mask]["mayor_knowledge_score"] == 0).mean()) * 100, 1),
    "mean_engagement_student": round(float(df[stu_mask]["engagement_index"].mean()), 1),
    "mean_civic_literacy_student": round(float(df[stu_mask]["civic_literacy_index"].mean()), 1),
    "mean_reasoning_student": round(float(df[stu_mask]["reasoning_depth_score"].mean()), 2),
    "mean_reasoning_faculty": round(float(df[~stu_mask]["reasoning_depth_score"].mean()), 2),
}

# ----------------------------------------------------------------------
# 5. EXPORT
# ----------------------------------------------------------------------
export_df = df.drop(columns=["mayor_knowledge_hits", "reasoning_parts", "news_list"])
export_df.to_csv("data/cleaned_survey.csv", index=False)

rows_for_json = []
for _, r in df.iterrows():
    d = r.to_dict()
    for k, v in list(d.items()):
        if isinstance(v, float) and np.isnan(v):
            d[k] = None
    rows_for_json.append(d)

with open("data/dashboard_data.json", "w") as f:
    json.dump({"rows": rows_for_json, "summary": summary,
               "rubrics": {
                   "mayor_knowledge": [{"label": l, "points": p} for _, p, l in MAYOR_RUBRIC],
                   "reasoning_depth": "length(0-3) + specificity(0-3) + multi-perspective(0-2) + nuance(0-2)",
                   "civic_skills": "civic-concept hits (0-7) + length bonus (0-3)",
                   "engagement_index": "mean of follow_local, follow_federal, likelihood_vote rescaled to 0-100",
                   "civic_literacy_index": "40% mayor knowledge + 35% reasoning depth + 25% political following",
               }}, f, indent=2, default=str)

print("\nWrote data/cleaned_survey.csv and data/dashboard_data.json")
