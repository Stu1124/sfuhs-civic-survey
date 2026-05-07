"""Build a single-file HTML dashboard with embedded data."""
import json

with open("dashboard_data.json") as f:
    data = json.load(f)

DATA_JSON = json.dumps(data)

HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>Youth Civic Engagement Survey — Dashboard</title>
<meta name="viewport" content="width=device-width, initial-scale=1" />
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gridjs/6.2.0/gridjs.umd.js"></script>
<link href="https://cdnjs.cloudflare.com/ajax/libs/gridjs/6.2.0/theme/mermaid.min.css" rel="stylesheet" />
<style>
  :root {
    --bg: #0e1116;
    --panel: #161b22;
    --panel2: #1c2128;
    --border: #30363d;
    --text: #e6edf3;
    --muted: #8b949e;
    --accent: #4f8cff;
    --accent2: #d29922;
    --green: #3fb950;
    --red:  #f85149;
    --amber:#d29922;
  }
  * { box-sizing: border-box; }
  body { margin:0; background: var(--bg); color: var(--text); font: 14px/1.45 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
  header { padding: 20px 28px; border-bottom: 1px solid var(--border); display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px;}
  header h1 { margin:0; font-size: 18px; font-weight:600; }
  header .meta { color: var(--muted); font-size: 12px; }
  .filters { display:flex; gap: 10px; flex-wrap:wrap; align-items:center; }
  .filters label { font-size: 12px; color: var(--muted); display:flex; align-items:center; gap:6px; background: var(--panel); border:1px solid var(--border); padding: 6px 10px; border-radius: 6px;}
  select, input[type=text] { background: var(--panel2); border: 1px solid var(--border); color: var(--text); padding: 4px 6px; border-radius: 4px; font: inherit; }
  main { padding: 18px; display: grid; grid-template-columns: repeat(12, 1fr); gap: 14px; }
  .card { background: var(--panel); border:1px solid var(--border); border-radius: 8px; padding: 14px; }
  .card h2 { font-size: 13px; margin: 0 0 10px; color: var(--muted); font-weight: 600; text-transform: uppercase; letter-spacing: .04em; }
  .span-3 { grid-column: span 3; }
  .span-4 { grid-column: span 4; }
  .span-6 { grid-column: span 6; }
  .span-8 { grid-column: span 8; }
  .span-12 { grid-column: span 12; }
  .kpi { font-size: 28px; font-weight: 600; }
  .kpi-sub { color: var(--muted); font-size: 12px; }
  canvas { max-width: 100%; }
  table.heat { border-collapse: collapse; font-size: 11px; }
  table.heat td, table.heat th { padding: 4px 6px; border:1px solid var(--border); text-align:center; }
  table.heat th { background: var(--panel2); color: var(--muted); }
  .resp { border-bottom: 1px dashed var(--border); padding: 8px 0; }
  .resp .who { color: var(--muted); font-size: 12px; }
  .pill { display:inline-block; padding: 1px 7px; border-radius: 999px; background:#222; color: #fff; font-size: 11px; margin-right: 4px; }
  .pill.yes { background: rgba(63,185,80,.15); color: var(--green); border:1px solid rgba(63,185,80,.4); }
  .pill.no { background: rgba(248,81,73,.15); color: var(--red); border:1px solid rgba(248,81,73,.4); }
  .pill.unsure { background: rgba(210,153,34,.15); color: var(--amber); border:1px solid rgba(210,153,34,.4); }
  .pill.role { background:#222; color:var(--text); border:1px solid var(--border); }
  .legend { color: var(--muted); font-size: 11px; }
  .row { display:flex; gap: 14px; flex-wrap:wrap;}
  .stat-grid { display:grid; grid-template-columns: 1fr 1fr; gap:10px; }
  .stat-grid .v { font-size: 20px; font-weight:600;}
  .scroll { max-height: 480px; overflow:auto; padding-right: 6px;}
  .small { color: var(--muted); font-size: 12px; }
  .muted { color: var(--muted); }
  .gridjs-wrapper, .gridjs-table { font-size: 12px; }
  details { background: var(--panel2); border:1px solid var(--border); border-radius: 6px; padding: 8px 10px; margin-top:8px; }
  details > summary { cursor: pointer; color: var(--muted); }
  .coef-bar { height: 14px; background: var(--panel2); border-radius: 4px; position: relative; margin: 2px 0 8px; }
  .coef-bar > span { position: absolute; top: 0; bottom: 0; }
  .coef-bar > span.pos { background: var(--green); left: 50%; }
  .coef-bar > span.neg { background: var(--red); right: 50%; }
  .coef-row { display:grid; grid-template-columns: 200px 1fr 60px; align-items:center; gap:8px; font-size:12px; }
  .tab-bar { display:flex; gap:4px; margin-bottom: 10px; }
  .tab-bar button { background: var(--panel2); color: var(--text); border:1px solid var(--border); padding: 6px 10px; border-radius: 6px; cursor: pointer; font: inherit;}
  .tab-bar button.active { background: var(--accent); border-color: var(--accent); }
  .tab-pane { display:none; }
  .tab-pane.active { display:block; }
</style>
</head>
<body>
<header>
  <div>
    <h1>Youth Civic Engagement & Voting Attitudes — SFUHS Survey</h1>
    <div class="meta">N = <span id="n-total">—</span> respondents · Students <span id="n-stu">—</span> · Faculty/Staff <span id="n-fac">—</span> · Collected April 2026</div>
  </div>
  <div class="filters">
    <label>Role
      <select id="f-role">
        <option value="all">All</option>
        <option value="Student">Students only</option>
        <option value="Faculty">Faculty only</option>
      </select>
    </label>
    <label>Local-16 support
      <select id="f-local">
        <option value="all">All</option>
        <option>Yes</option><option>No</option><option>Unsure</option>
      </select>
    </label>
    <label>Federal-16 support
      <select id="f-federal">
        <option value="all">All</option>
        <option>Yes</option><option>No</option><option>Unsure</option>
      </select>
    </label>
    <label>Search
      <input id="f-search" type="text" placeholder="text in explanation…" />
    </label>
    <button id="reset" style="background:var(--panel2);color:var(--text);border:1px solid var(--border);padding:6px 10px;border-radius:6px;cursor:pointer;">Reset</button>
  </div>
</header>

<main>
  <section class="card span-3">
    <h2>Total responses</h2>
    <div class="kpi" id="kpi-n">—</div>
    <div class="kpi-sub" id="kpi-n-sub">filtered</div>
  </section>
  <section class="card span-3">
    <h2>Support local 16+ (filtered)</h2>
    <div class="kpi" id="kpi-local">—</div>
    <div class="kpi-sub">share saying "Yes"</div>
  </section>
  <section class="card span-3">
    <h2>Support federal 16+ (filtered)</h2>
    <div class="kpi" id="kpi-fed">—</div>
    <div class="kpi-sub">share saying "Yes"</div>
  </section>
  <section class="card span-3">
    <h2>Avg likelihood to vote (students)</h2>
    <div class="kpi" id="kpi-likely">—</div>
    <div class="kpi-sub">scale 1–5</div>
  </section>

  <section class="card span-6">
    <h2>Support for lowering voting age — by role</h2>
    <canvas id="ch-support" height="160"></canvas>
    <div class="legend">Chi-square (full sample) — Role × local: χ²=<span id="chi-l"></span>, p=<span id="p-l"></span> · Role × federal: χ²=<span id="chi-f"></span>, p=<span id="p-f"></span></div>
  </section>

  <section class="card span-6">
    <h2>Self-reported attitudes (means, 1–5)</h2>
    <canvas id="ch-likert" height="160"></canvas>
    <div class="legend">Higher = more (closer following / more influence / more aligned with parents / more likely to vote / more informed)</div>
  </section>

  <section class="card span-6">
    <h2>News sources (% of respondents in each role selecting source)</h2>
    <canvas id="ch-news" height="200"></canvas>
  </section>

  <section class="card span-6">
    <h2>Student correlation matrix (Pearson)</h2>
    <div id="heatmap"></div>
    <div class="legend">Green = positive, red = negative. Cell value rounded to 2 decimals.</div>
  </section>

  <section class="card span-6">
    <h2>Logistic regression — predicting student support</h2>
    <div class="tab-bar">
      <button data-tab="local" class="active">Local lowering</button>
      <button data-tab="federal">Federal lowering</button>
    </div>
    <div id="tab-local" class="tab-pane active"></div>
    <div id="tab-federal" class="tab-pane"></div>
    <div class="legend">Standardized coefficients on z-scored Likert features. Positive = predicts "Yes". n shown per model. Small sample — interpret as exploratory only.</div>
  </section>

  <section class="card span-6">
    <h2>Theme keyword counts (open responses)</h2>
    <canvas id="ch-themes" height="220"></canvas>
    <div class="legend">Substring counts in students' explanations vs. faculty explanations + reasoning.</div>
  </section>

  <section class="card span-12">
    <h2>Response browser</h2>
    <div id="responses" class="scroll"></div>
  </section>

  <section class="card span-12">
    <h2>Raw data table</h2>
    <div id="table"></div>
  </section>

  <section class="card span-12">
    <h2>Methodology & caveats</h2>
    <div class="small">
      <p>Convenience sample at one private school (SFUHS) collected April 2026. N=83 (67 students, 16 faculty/staff) — too small to be statistically conclusive at fine subgroup levels.
      Likert scales are 1–5. Chi-square tests use the role × support contingency table on the full sample. The student logistic regression drops "Unsure" responses (binary Yes/No only), z-scores numeric features, and uses L2 regularization (liblinear) — interpret coefficients as direction-and-relative-magnitude, not population-level effects. The accuracy figures shown are in-sample and inflated by the small N relative to feature count.</p>
      <p>Open-text fields are summarized via simple substring matching, not topic modeling. Keyword counts are illustrative only.</p>
    </div>
  </section>
</main>

<script>
const DATA = __DATA_JSON__;
const rows = DATA.rows;
const summary = DATA.summary;

document.getElementById("n-total").textContent = summary.n_total;
document.getElementById("n-stu").textContent = summary.n_student;
document.getElementById("n-fac").textContent = summary.n_faculty;
document.getElementById("chi-l").textContent = summary.chi2.role_x_local.chi2.toFixed(2);
document.getElementById("p-l").textContent = summary.chi2.role_x_local.p.toFixed(3);
document.getElementById("chi-f").textContent = summary.chi2.role_x_federal.chi2.toFixed(2);
document.getElementById("p-f").textContent = summary.chi2.role_x_federal.p.toFixed(3);

let charts = {};

function getFiltered() {
  const role = document.getElementById("f-role").value;
  const loc = document.getElementById("f-local").value;
  const fed = document.getElementById("f-federal").value;
  const q = document.getElementById("f-search").value.trim().toLowerCase();
  return rows.filter(r => {
    if (role !== "all" && r.role !== role) return false;
    if (loc !== "all" && r.support_local_16 !== loc) return false;
    if (fed !== "all" && r.support_federal_16 !== fed) return false;
    if (q) {
      const blob = [r.explanation, r.mayor_knowledge_text, r.civic_skills_text, r.reasoning_text].filter(Boolean).join(" ").toLowerCase();
      if (!blob.includes(q)) return false;
    }
    return true;
  });
}

function pctYes(arr, key) {
  const known = arr.filter(r => r[key] != null);
  if (!known.length) return null;
  const yes = known.filter(r => r[key] === "Yes").length;
  return yes / known.length;
}

function renderKPIs(filtered) {
  document.getElementById("kpi-n").textContent = filtered.length;
  const lp = pctYes(filtered, "support_local_16");
  const fp = pctYes(filtered, "support_federal_16");
  document.getElementById("kpi-local").textContent = lp == null ? "—" : (lp*100).toFixed(0) + "%";
  document.getElementById("kpi-fed").textContent = fp == null ? "—" : (fp*100).toFixed(0) + "%";
  const stu = filtered.filter(r => r.role === "Student" && r.likelihood_vote != null);
  const m = stu.length ? stu.reduce((s,r)=>s+r.likelihood_vote,0)/stu.length : null;
  document.getElementById("kpi-likely").textContent = m == null ? "—" : m.toFixed(2);
}

function chartSupport() {
  const ctx = document.getElementById("ch-support");
  const cats = ["Yes","No","Unsure"];
  const roles = ["Student","Faculty"];
  const dsets = [];
  const colors = { Yes: "#3fb950", No: "#f85149", Unsure: "#d29922" };
  // Build grouped bars: for each role, show local Yes/No/Unsure and federal Yes/No/Unsure
  const labels = ["Student · Local","Student · Federal","Faculty · Local","Faculty · Federal"];
  const localStu = summary.support_local_by_role.Student || {};
  const fedStu = summary.support_federal_by_role.Student || {};
  const localFac = summary.support_local_by_role.Faculty || {};
  const fedFac = summary.support_federal_by_role.Faculty || {};
  const tables = [localStu, fedStu, localFac, fedFac];
  cats.forEach(c => {
    dsets.push({
      label: c,
      data: tables.map(t => +(t[c] || 0).toFixed(1)),
      backgroundColor: colors[c],
      borderWidth: 0,
    });
  });
  if (charts.support) charts.support.destroy();
  charts.support = new Chart(ctx, {
    type: "bar",
    data: { labels, datasets: dsets },
    options: {
      indexAxis: "y",
      responsive: true,
      scales: {
        x: { stacked: true, ticks: { color: "#8b949e", callback: v => v + "%" }, grid: { color: "#21262d" }},
        y: { stacked: true, ticks: { color: "#e6edf3" }, grid: { color: "#21262d" }}
      },
      plugins: { legend: { labels: { color: "#e6edf3" } }, tooltip: { callbacks: { label: c => c.dataset.label + ": " + c.parsed.x + "%" } } }
    }
  });
}

function chartLikert() {
  const ctx = document.getElementById("ch-likert");
  const fields = [
    ["follow_local", "Follow local politics"],
    ["follow_federal", "Follow federal politics"],
    ["influence_local", "Influence — local (S)"],
    ["influence_federal", "Influence — federal (S)"],
    ["align_parents", "Align with parents (S)"],
    ["likelihood_vote", "Would vote in SF (S)"],
    ["informed_local", "16–18 informed: local"],
    ["informed_federal", "16–18 informed: federal"],
  ];
  const labels = fields.map(f => f[1]);
  const stu = fields.map(f => summary.likert_means[f[0]].Student.mean);
  const fac = fields.map(f => summary.likert_means[f[0]].Faculty.mean);
  if (charts.likert) charts.likert.destroy();
  charts.likert = new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [
        { label: "Student", data: stu, backgroundColor: "#4f8cff" },
        { label: "Faculty", data: fac, backgroundColor: "#d29922" },
      ]
    },
    options: {
      responsive: true,
      scales: {
        y: { min: 0, max: 5, ticks: { color: "#8b949e" }, grid: { color: "#21262d" } },
        x: { ticks: { color: "#e6edf3", maxRotation: 45, minRotation: 35 }, grid: { color: "#21262d" } }
      },
      plugins: { legend: { labels: { color: "#e6edf3" } } }
    }
  });
}

function chartNews(filtered) {
  // Compute % of respondents in each role selecting each source from current filter
  const ctx = document.getElementById("ch-news");
  const sources = ["Social media (TikTok, Instagram, X)","YouTube","Podcasts","Traditional news (NYT, WSJ, SF Chronicle)","Family or friends","School","Other"];
  function shareForRole(role) {
    const base = filtered.filter(r => r.role === role);
    if (!base.length) return sources.map(_=>0);
    return sources.map(src => {
      const c = base.filter(r => (r.news_sources || "").includes(src.split(" (")[0])).length;
      return Math.round(100 * c / base.length);
    });
  }
  const stu = shareForRole("Student");
  const fac = shareForRole("Faculty");
  if (charts.news) charts.news.destroy();
  charts.news = new Chart(ctx, {
    type: "bar",
    data: {
      labels: sources.map(s => s.replace(/ \(.*\)/,"")),
      datasets: [
        { label: "Student", data: stu, backgroundColor: "#4f8cff" },
        { label: "Faculty", data: fac, backgroundColor: "#d29922" },
      ]
    },
    options: {
      responsive: true,
      scales: {
        y: { ticks: { color: "#8b949e", callback: v=>v+"%" }, grid: { color: "#21262d" } },
        x: { ticks: { color: "#e6edf3" }, grid: { color: "#21262d" } }
      },
      plugins: { legend: { labels: { color: "#e6edf3" } } }
    }
  });
}

function renderHeatmap() {
  const corr = summary.correlations;
  const cols = Object.keys(corr);
  let html = "<table class='heat'><thead><tr><th></th>";
  cols.forEach(c => html += `<th>${c.replace(/_/g," ")}</th>`);
  html += "</tr></thead><tbody>";
  cols.forEach(r => {
    html += `<tr><th>${r.replace(/_/g," ")}</th>`;
    cols.forEach(c => {
      const v = corr[r][c];
      const a = Math.abs(v);
      const color = v >= 0
        ? `rgba(63,185,80,${Math.min(1, a*1.2).toFixed(2)})`
        : `rgba(248,81,73,${Math.min(1, a*1.2).toFixed(2)})`;
      html += `<td style="background:${color};color:${a>0.55?'#0e1116':'#e6edf3'}">${v.toFixed(2)}</td>`;
    });
    html += "</tr>";
  });
  html += "</tbody></table>";
  document.getElementById("heatmap").innerHTML = html;
}

function renderLogit() {
  function block(model) {
    if (!model) return "<div class='muted'>No data</div>";
    const entries = Object.entries(model.coefs).sort((a,b)=>Math.abs(b[1])-Math.abs(a[1]));
    const max = Math.max(...entries.map(([_,v])=>Math.abs(v)));
    let html = `<div class="small">n = ${model.n} · base "Yes" rate = ${(model.support_yes_rate*100).toFixed(0)}% · in-sample acc = ${(model.accuracy*100).toFixed(0)}%</div>`;
    entries.forEach(([k,v]) => {
      const pct = Math.min(50, Math.abs(v)/max*50);
      const side = v >= 0 ? `<span class="pos" style="width:${pct}%"></span>` : `<span class="neg" style="width:${pct}%"></span>`;
      html += `<div class="coef-row"><div>${k.replace(/_/g," ")}</div><div class="coef-bar">${side}</div><div style="text-align:right;color:${v>=0?'var(--green)':'var(--red)'}">${v.toFixed(2)}</div></div>`;
    });
    return html;
  }
  document.getElementById("tab-local").innerHTML = block(summary.logit_local_student);
  document.getElementById("tab-federal").innerHTML = block(summary.logit_federal_student);
}

function chartThemes() {
  const ctx = document.getElementById("ch-themes");
  const ks = Object.keys(summary.keywords_student);
  if (charts.themes) charts.themes.destroy();
  charts.themes = new Chart(ctx, {
    type: "bar",
    data: {
      labels: ks,
      datasets: [
        { label: "Student", data: ks.map(k => summary.keywords_student[k]), backgroundColor: "#4f8cff" },
        { label: "Faculty", data: ks.map(k => summary.keywords_faculty[k]), backgroundColor: "#d29922" },
      ]
    },
    options: {
      responsive: true,
      scales: {
        y: { ticks: { color: "#8b949e" }, grid: { color: "#21262d" } },
        x: { ticks: { color: "#e6edf3", maxRotation: 45, minRotation: 30 }, grid: { color: "#21262d" } }
      },
      plugins: { legend: { labels: { color: "#e6edf3" } } }
    }
  });
}

function pillFor(v) {
  if (!v) return "";
  const cls = v.toLowerCase();
  return `<span class="pill ${cls}">${v}</span>`;
}

function renderResponses(filtered) {
  const list = document.getElementById("responses");
  list.innerHTML = "";
  const cap = 200;
  filtered.slice(0, cap).forEach(r => {
    const block = document.createElement("div");
    block.className = "resp";
    const text = r.explanation || r.reasoning_text || "";
    const civic = r.civic_skills_text ? `<details><summary>Civic skills answer</summary><div>${escapeHTML(r.civic_skills_text)}</div></details>` : "";
    const mayor = r.mayor_knowledge_text ? `<details><summary>Mayor knowledge answer</summary><div>${escapeHTML(r.mayor_knowledge_text)}</div></details>` : "";
    block.innerHTML = `
      <div class="who">
        <span class="pill role">${r.role}</span>
        ${r.role === "Student" ? `<span class="pill role">${r.age || "?"}, grade ${r.grade || "?"}</span>` : (r.subject ? `<span class="pill role">${r.subject}, ${r.years_in_ed||"?"} yrs</span>` : "")}
        Local: ${pillFor(r.support_local_16)} Federal: ${pillFor(r.support_federal_16)}
      </div>
      <div>${escapeHTML(text || "(no comment)")}</div>
      ${civic}${mayor}
    `;
    list.appendChild(block);
  });
  if (filtered.length > cap) {
    const note = document.createElement("div");
    note.className = "small";
    note.textContent = `Showing first ${cap} of ${filtered.length}.`;
    list.appendChild(note);
  }
}

function escapeHTML(s) {
  return String(s).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[c]));
}

let grid = null;
function renderTable(filtered) {
  const cols = ["role","age","grade","follow_local","follow_federal","influence_local","influence_federal","align_parents","support_local_16","support_federal_16","likelihood_vote","informed_local","informed_federal","subject","years_in_ed"];
  const data = filtered.map(r => cols.map(c => r[c] == null ? "" : r[c]));
  if (grid) grid.destroy();
  grid = new gridjs.Grid({
    columns: cols,
    data,
    sort: true, search: true, pagination: { limit: 25 },
    style: { table: { fontSize: "12px" } }
  }).render(document.getElementById("table"));
}

function rerender() {
  const filtered = getFiltered();
  renderKPIs(filtered);
  chartSupport();          // (full sample for clarity)
  chartLikert();           // (full sample)
  chartNews(filtered);     // respects filter
  renderHeatmap();         // full sample, students only
  renderLogit();           // full sample, students only
  chartThemes();           // full sample
  renderResponses(filtered);
  renderTable(filtered);
}

["f-role","f-local","f-federal","f-search"].forEach(id => {
  document.getElementById(id).addEventListener("input", rerender);
  document.getElementById(id).addEventListener("change", rerender);
});
document.getElementById("reset").addEventListener("click", () => {
  document.getElementById("f-role").value = "all";
  document.getElementById("f-local").value = "all";
  document.getElementById("f-federal").value = "all";
  document.getElementById("f-search").value = "";
  rerender();
});

// Tab handling for logit
document.querySelectorAll(".tab-bar button").forEach(b => {
  b.addEventListener("click", () => {
    document.querySelectorAll(".tab-bar button").forEach(x=>x.classList.remove("active"));
    document.querySelectorAll(".tab-pane").forEach(x=>x.classList.remove("active"));
    b.classList.add("active");
    document.getElementById("tab-"+b.dataset.tab).classList.add("active");
  });
});

rerender();
</script>
</body>
</html>
"""

with open("dashboard.html","w") as f:
    f.write(HTML.replace("__DATA_JSON__", DATA_JSON))

print("Wrote dashboard.html")
