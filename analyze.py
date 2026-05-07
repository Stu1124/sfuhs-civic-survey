"""
Youth Civic Engagement Survey - Data Analysis & Modeling
Builds cleaned dataset, runs descriptive stats, correlation analysis,
logistic regression on support-for-lowering-voting-age, and exports JSON
for the interactive dashboard.
"""
import pandas as pd
import numpy as np
import json
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

# Load
raw = pd.read_csv("survey.csv")

# The form has separate question blocks for students vs faculty.
# Columns 1..17 are student questions; columns 18..27 are faculty questions.
# Build a unified "long" frame where each row has a 'role' and a normalized set of fields.

cols = list(raw.columns)
# Index the original columns by position for clarity
# 0  Timestamp
# 1  Role (Student / Faculty or Staff)
# 2  Age
# 3  Grade
# 4  Local follow (S)
# 5  Federal follow (S)
# 6  Local influence (S)
# 7  Federal influence (S)
# 8  Align with parents (S)
# 9  Support local 16 (S)
# 10 Support fed 16 (S)
# 11 Explanation (S)
# 12 Likelihood to vote (S)
# 13 SF 16-18 informed local (S)
# 14 SF 16-18 informed fed (S)
# 15 Mayor knowledge (S)
# 16 News sources (S)
# 17 Subject (F)
# 18 Years in education (F)
# 19 Local follow (F)
# 20 Federal follow (F)
# 21 Support local 16 (F)
# 22 Support fed 16 (F)
# 23 Explanation (F)
# 24 16-18 informed local (F)
# 25 16-18 informed fed (F)
# 26 Reasoning (F)
# 27 Civic skills (F)
# 28 News sources (F)

records = []
for _, row in raw.iterrows():
    role = row.iloc[1]
    if role == "Student":
        rec = {
            "role": "Student",
            "age": row.iloc[2],
            "grade": row.iloc[3],
            "follow_local": row.iloc[4],
            "follow_federal": row.iloc[5],
            "influence_local": row.iloc[6],
            "influence_federal": row.iloc[7],
            "align_parents": row.iloc[8],
            "support_local_16": row.iloc[9],
            "support_federal_16": row.iloc[10],
            "explanation": row.iloc[11],
            "likelihood_vote": row.iloc[12],
            "informed_local": row.iloc[13],
            "informed_federal": row.iloc[14],
            "mayor_knowledge_text": row.iloc[15],
            "news_sources": row.iloc[16],
            "subject": None,
            "years_in_ed": None,
            "civic_skills_text": None,
            "reasoning_text": None,
        }
    else:
        rec = {
            "role": "Faculty",
            "age": None,
            "grade": None,
            "follow_local": row.iloc[19],
            "follow_federal": row.iloc[20],
            "influence_local": None,
            "influence_federal": None,
            "align_parents": None,
            "support_local_16": row.iloc[21],
            "support_federal_16": row.iloc[22],
            "explanation": row.iloc[23],
            "likelihood_vote": None,
            "informed_local": row.iloc[24],
            "informed_federal": row.iloc[25],
            "mayor_knowledge_text": None,
            "news_sources": row.iloc[28],
            "subject": row.iloc[17],
            "years_in_ed": row.iloc[18],
            "civic_skills_text": row.iloc[27],
            "reasoning_text": row.iloc[26],
        }
    records.append(rec)

df = pd.DataFrame(records)

# Numeric coercion
for c in ["age","grade","follow_local","follow_federal","influence_local",
          "influence_federal","align_parents","likelihood_vote",
          "informed_local","informed_federal"]:
    df[c] = pd.to_numeric(df[c], errors="coerce")

print("=== Sample sizes ===")
print(df["role"].value_counts())
print()

# ----- Descriptive stats -----
def pct(series):
    out = series.value_counts(dropna=False, normalize=True).round(3) * 100
    return out.to_dict()

summary = {
    "n_total": int(len(df)),
    "n_student": int((df.role == "Student").sum()),
    "n_faculty": int((df.role == "Faculty").sum()),
    "support_local_by_role": {
        r: pct(g["support_local_16"]) for r, g in df.groupby("role")
    },
    "support_federal_by_role": {
        r: pct(g["support_federal_16"]) for r, g in df.groupby("role")
    },
}

print("=== Support for lowering LOCAL voting age (by role) ===")
for r, d in summary["support_local_by_role"].items():
    print(r, d)
print()
print("=== Support for lowering FEDERAL voting age (by role) ===")
for r, d in summary["support_federal_by_role"].items():
    print(r, d)
print()

# Means of Likert scales
likert_cols = ["follow_local","follow_federal","influence_local","influence_federal",
               "align_parents","likelihood_vote","informed_local","informed_federal"]
likert_means = {}
for c in likert_cols:
    by_role = df.groupby("role")[c].agg(["mean","std","count"]).round(2)
    likert_means[c] = {r: {"mean": float(by_role.loc[r,"mean"]) if r in by_role.index and not pd.isna(by_role.loc[r,"mean"]) else None,
                           "std": float(by_role.loc[r,"std"]) if r in by_role.index and not pd.isna(by_role.loc[r,"std"]) else None,
                           "n": int(by_role.loc[r,"count"]) if r in by_role.index else 0}
                       for r in ["Student","Faculty"]}

print("=== Likert means by role ===")
for c, v in likert_means.items():
    print(f"{c}: {v}")
print()

# ----- News sources -----
def split_sources(s):
    if pd.isna(s) or not s:
        return []
    # Use a careful split that handles parens with commas
    parts = []
    depth = 0
    cur = ""
    for ch in s:
        if ch == "(": depth += 1
        elif ch == ")": depth -= 1
        if ch == "," and depth == 0:
            parts.append(cur.strip())
            cur = ""
        else:
            cur += ch
    if cur.strip():
        parts.append(cur.strip())
    return parts

source_rows = []
for _, r in df.iterrows():
    for s in split_sources(r["news_sources"]):
        source_rows.append({"role": r["role"], "source": s})
sources_df = pd.DataFrame(source_rows)
news_counts = sources_df.groupby(["role","source"]).size().unstack(fill_value=0)
print("=== News source counts ===")
print(news_counts)
print()

# ----- Chi-squared: role vs support -----
def chi2_table(df, col):
    tab = pd.crosstab(df["role"], df[col])
    chi2, p, dof, _ = stats.chi2_contingency(tab)
    return tab, chi2, p, dof

tab_local, chi_l, p_l, dof_l = chi2_table(df, "support_local_16")
tab_fed, chi_f, p_f, dof_f = chi2_table(df, "support_federal_16")
print(f"Chi2 role x support_local: chi2={chi_l:.3f}, p={p_l:.4f}, dof={dof_l}")
print(f"Chi2 role x support_federal: chi2={chi_f:.3f}, p={p_f:.4f}, dof={dof_f}")
print()

# ----- Correlation matrix (students only) -----
students = df[df.role == "Student"].copy()
corr_cols = ["age","grade","follow_local","follow_federal","influence_local",
             "influence_federal","align_parents","likelihood_vote",
             "informed_local","informed_federal"]
corr = students[corr_cols].corr().round(3)
print("=== Student correlation matrix ===")
print(corr)
print()

# ----- Logistic regression: predict student support for local lowering -----
# Encode support: Yes=1, No=0, Unsure dropped
m = students.copy()
m = m[m["support_local_16"].isin(["Yes","No"])]
m["y_local"] = (m["support_local_16"] == "Yes").astype(int)
m["y_federal"] = (m["support_federal_16"] == "Yes").astype(int)

features = ["age","follow_local","follow_federal","influence_local",
            "influence_federal","align_parents","informed_local","informed_federal","likelihood_vote"]
X = m[features].apply(pd.to_numeric, errors="coerce").fillna(m[features].apply(pd.to_numeric, errors="coerce").mean())
scaler = StandardScaler()
Xs = scaler.fit_transform(X)

def fit_logit(y_col):
    y = m[y_col].values
    if len(np.unique(y)) < 2:
        return None
    lr = LogisticRegression(max_iter=1000, solver="liblinear")
    lr.fit(Xs, y)
    return {
        "intercept": float(lr.intercept_[0]),
        "coefs": {f: float(c) for f, c in zip(features, lr.coef_[0])},
        "accuracy": float(lr.score(Xs, y)),
        "n": int(len(y)),
        "support_yes_rate": float(y.mean()),
    }

logit_local = fit_logit("y_local")
logit_federal = fit_logit("y_federal")

print("=== Logit: support local lowering (students, Yes=1) ===")
print(json.dumps(logit_local, indent=2))
print()
print("=== Logit: support federal lowering (students, Yes=1) ===")
print(json.dumps(logit_federal, indent=2))
print()

# Word counts in qualitative explanations (very basic)
def keyword_counts(series, keywords):
    text = " ".join(str(x).lower() for x in series.dropna())
    return {k: text.count(k) for k in keywords}

themes = ["parent","influenc","mature","inform","educat","brain","cortex","social media",
         "manipulat","local","federal","biased","critical","misinformation"]
student_kw = keyword_counts(students["explanation"], themes)
faculty_expl = df[df.role=="Faculty"]["explanation"]
faculty_reason = df[df.role=="Faculty"]["reasoning_text"]
faculty_kw = keyword_counts(pd.concat([faculty_expl.fillna(""), faculty_reason.fillna("")]), themes)
print("=== Student explanation keyword counts ===")
print(student_kw)
print("=== Faculty explanation+reasoning keyword counts ===")
print(faculty_kw)

# Save cleaned long-form CSV and JSON for dashboard
df.to_csv("survey_clean.csv", index=False)

# Prepare JSON for dashboard
dashboard_data = {
    "rows": json.loads(df.to_json(orient="records")),
    "summary": {
        "n_total": int(len(df)),
        "n_student": int((df.role == "Student").sum()),
        "n_faculty": int((df.role == "Faculty").sum()),
        "support_local_by_role": summary["support_local_by_role"],
        "support_federal_by_role": summary["support_federal_by_role"],
        "likert_means": likert_means,
        "news_counts": {r: news_counts.loc[r].to_dict() for r in news_counts.index},
        "chi2": {
            "role_x_local":  {"chi2": chi_l, "p": p_l, "dof": dof_l, "table": tab_local.to_dict()},
            "role_x_federal":{"chi2": chi_f, "p": p_f, "dof": dof_f, "table": tab_fed.to_dict()},
        },
        "correlations": corr.to_dict(),
        "logit_local_student": logit_local,
        "logit_federal_student": logit_federal,
        "keywords_student": student_kw,
        "keywords_faculty": faculty_kw,
    }
}

with open("dashboard_data.json","w") as f:
    json.dump(dashboard_data, f, indent=2, default=str)

print("\nWrote survey_clean.csv and dashboard_data.json")
