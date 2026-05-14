"""
Build the single-file interactive dashboard (index.html) by embedding
data/dashboard_data.json into a self-contained HTML/CSS/JS template.

Run order:  python analyze.py  ->  python build_dashboard.py
"""
import json

with open("data/dashboard_data.json") as f:
    DATA = json.load(f)

DATA_JSON = json.dumps(DATA, separators=(",", ":"))

HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Youth Civic Engagement & Voting Attitudes — SFUHS Survey</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gridjs/6.2.0/gridjs.umd.js"></script>
<link href="https://cdnjs.cloudflare.com/ajax/libs/gridjs/6.2.0/theme/mermaid.min.css" rel="stylesheet" />
<style>
  :root{
    --bg:#f5f6f8; --surface:#ffffff; --surface-2:#fafbfc;
    --ink:#1c2128; --muted:#62708a; --faint:#8b97ad;
    --line:#e4e7ec; --line-strong:#d2d7e0;
    --accent:#4f46e5; --accent-soft:#eef0fe;
    --student:#4f46e5; --faculty:#0e9aa7;
    --yes:#16a34a; --no:#dc2626; --unsure:#d97706;
    --shadow:0 1px 2px rgba(16,24,40,.06), 0 1px 3px rgba(16,24,40,.04);
    --radius:14px;
  }
  *{box-sizing:border-box;}
  html,body{margin:0;padding:0;}
  body{
    background:var(--bg); color:var(--ink);
    font:15px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
    -webkit-font-smoothing:antialiased;
  }
  a{color:var(--accent);}
  h1,h2,h3{line-height:1.25;}
  .wrap{max-width:1180px;margin:0 auto;padding:0 22px;}

  /* ---- top nav ---- */
  nav.top{
    position:sticky;top:0;z-index:50;background:rgba(255,255,255,.86);
    backdrop-filter:saturate(180%) blur(10px);
    border-bottom:1px solid var(--line);
  }
  nav.top .wrap{display:flex;align-items:center;gap:20px;height:56px;}
  nav.top .brand{font-weight:700;font-size:14.5px;letter-spacing:-.01em;white-space:nowrap;}
  nav.top .links{display:flex;gap:4px;flex-wrap:wrap;margin-left:auto;}
  nav.top .links a{
    color:var(--muted);text-decoration:none;font-size:13px;font-weight:500;
    padding:6px 10px;border-radius:8px;
  }
  nav.top .links a:hover{background:var(--accent-soft);color:var(--accent);}

  /* ---- hero ---- */
  header.hero{padding:46px 0 26px;}
  header.hero h1{
    margin:0 0 8px;font-size:31px;font-weight:760;letter-spacing:-.02em;
  }
  header.hero .sub{color:var(--muted);font-size:15px;max-width:680px;}
  header.hero .tags{display:flex;gap:8px;flex-wrap:wrap;margin-top:16px;}
  .tag{
    font-size:12px;font-weight:600;color:var(--muted);
    background:var(--surface);border:1px solid var(--line);
    padding:4px 10px;border-radius:999px;
  }

  /* ---- KPI grid ---- */
  .kpi-grid{
    display:grid;grid-template-columns:repeat(6,1fr);gap:12px;margin:22px 0 8px;
  }
  .kpi{
    background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);
    padding:15px 15px 13px;box-shadow:var(--shadow);
  }
  .kpi .label{font-size:11.5px;font-weight:600;color:var(--faint);text-transform:uppercase;letter-spacing:.04em;}
  .kpi .value{font-size:26px;font-weight:740;margin-top:6px;letter-spacing:-.02em;}
  .kpi .note{font-size:12px;color:var(--muted);margin-top:2px;}
  @media(max-width:900px){.kpi-grid{grid-template-columns:repeat(2,1fr);}}

  /* ---- sections ---- */
  section{padding:34px 0;border-top:1px solid var(--line);}
  section:first-of-type{border-top:none;}
  .sec-head{margin-bottom:6px;}
  .sec-head h2{margin:0;font-size:21px;font-weight:720;letter-spacing:-.02em;}
  .sec-head p{margin:6px 0 0;color:var(--muted);font-size:14px;max-width:760px;}

  .grid{display:grid;gap:16px;margin-top:18px;}
  .g-2{grid-template-columns:1fr 1fr;}
  .g-3{grid-template-columns:repeat(3,1fr);}
  .g-12-5{grid-template-columns:7fr 5fr;}
  .g-5-12{grid-template-columns:5fr 7fr;}
  @media(max-width:860px){.grid{grid-template-columns:1fr !important;}}

  .card{
    background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);
    padding:18px;box-shadow:var(--shadow);
  }
  .card h3{margin:0 0 3px;font-size:15px;font-weight:680;}
  .card .desc{color:var(--muted);font-size:12.5px;margin:0 0 12px;}
  .card .takeaway{
    margin-top:13px;font-size:12.5px;color:var(--muted);
    border-left:2.5px solid var(--accent);padding:2px 0 2px 11px;background:var(--surface-2);
  }
  .card .takeaway b{color:var(--ink);font-weight:650;}
  canvas{max-width:100%;}

  /* ---- filters ---- */
  .filterbar{
    position:sticky;top:56px;z-index:40;background:var(--surface);
    border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);
    padding:12px 14px;margin-top:18px;display:flex;gap:10px;flex-wrap:wrap;align-items:center;
  }
  .filterbar .fl{display:flex;flex-direction:column;gap:3px;}
  .filterbar label{font-size:11px;font-weight:600;color:var(--faint);text-transform:uppercase;letter-spacing:.03em;}
  select,input[type=text]{
    font:inherit;font-size:13px;padding:6px 9px;border:1px solid var(--line-strong);
    border-radius:8px;background:var(--surface);color:var(--ink);min-width:130px;
  }
  input[type=text]{min-width:220px;}
  .btn{
    font:inherit;font-size:13px;font-weight:600;padding:7px 13px;border-radius:8px;
    border:1px solid var(--line-strong);background:var(--surface);color:var(--ink);cursor:pointer;
  }
  .btn:hover{background:var(--surface-2);}
  .btn.primary{background:var(--accent);border-color:var(--accent);color:#fff;}
  .filter-count{margin-left:auto;font-size:12.5px;color:var(--muted);font-weight:600;}

  /* ---- heatmap ---- */
  table.heat{border-collapse:collapse;font-size:10.5px;width:100%;}
  table.heat td,table.heat th{padding:3px 4px;text-align:center;border:1px solid var(--line);}
  table.heat th{background:var(--surface-2);color:var(--muted);font-weight:600;}
  table.heat th.rot{writing-mode:vertical-rl;transform:rotate(180deg);height:96px;white-space:nowrap;}
  table.heat td.lbl{text-align:right;color:var(--muted);font-weight:600;background:var(--surface-2);}

  /* ---- coef bars ---- */
  .coef-row{display:grid;grid-template-columns:165px 1fr 46px;align-items:center;gap:9px;font-size:12px;margin:5px 0;}
  .coef-track{height:16px;background:var(--surface-2);border-radius:5px;position:relative;border:1px solid var(--line);}
  .coef-track .mid{position:absolute;left:50%;top:0;bottom:0;width:1px;background:var(--line-strong);}
  .coef-track .bar{position:absolute;top:1px;bottom:1px;border-radius:3px;}
  .coef-track .bar.pos{left:50%;background:var(--yes);}
  .coef-track .bar.neg{right:50%;background:var(--no);}

  /* ---- response cards ---- */
  .resp-list{display:flex;flex-direction:column;gap:10px;max-height:620px;overflow:auto;padding-right:6px;}
  .resp{border:1px solid var(--line);border-radius:11px;padding:12px 13px;background:var(--surface-2);}
  .resp .meta{display:flex;align-items:center;gap:6px;flex-wrap:wrap;margin-bottom:7px;}
  .pill{font-size:11px;font-weight:650;padding:2px 8px;border-radius:999px;border:1px solid transparent;}
  .pill.role{background:var(--accent-soft);color:var(--accent);}
  .pill.role.fac{background:#e0f5f6;color:var(--faculty);}
  .pill.demo{background:var(--surface);border-color:var(--line-strong);color:var(--muted);}
  .pill.yes{background:#e7f6ec;color:var(--yes);}
  .pill.no{background:#fdeaea;color:var(--no);}
  .pill.unsure{background:#fdf3e3;color:var(--unsure);}
  .resp .qa{font-size:13px;margin:6px 0;}
  .resp .qa .q{color:var(--faint);font-size:11px;font-weight:650;text-transform:uppercase;letter-spacing:.03em;}
  .scorechip{
    display:inline-flex;align-items:center;gap:5px;font-size:11px;font-weight:650;
    background:var(--surface);border:1px solid var(--line-strong);border-radius:999px;padding:2px 8px;color:var(--muted);
  }
  .scorechip b{color:var(--ink);}
  .scorebar{display:inline-block;width:46px;height:5px;border-radius:3px;background:var(--line);position:relative;overflow:hidden;}
  .scorebar i{position:absolute;left:0;top:0;bottom:0;background:var(--accent);}
  details.rubric{margin-top:7px;border-top:1px dashed var(--line);padding-top:7px;}
  details.rubric summary{cursor:pointer;font-size:11.5px;color:var(--muted);font-weight:600;}
  details.rubric .hit{font-size:11.5px;color:var(--muted);padding:2px 0;}
  details.rubric .hit::before{content:"✓ ";color:var(--yes);}

  .legend{font-size:11.5px;color:var(--faint);margin-top:9px;}
  .mini-tab{display:flex;gap:5px;margin-bottom:11px;}
  .mini-tab button{
    font:inherit;font-size:12px;font-weight:600;padding:5px 11px;border-radius:8px;
    border:1px solid var(--line-strong);background:var(--surface);color:var(--muted);cursor:pointer;
  }
  .mini-tab button.on{background:var(--accent);border-color:var(--accent);color:#fff;}
  .pane{display:none;}.pane.on{display:block;}

  .rubric-table{width:100%;border-collapse:collapse;font-size:12.5px;}
  .rubric-table td,.rubric-table th{padding:6px 8px;border-bottom:1px solid var(--line);text-align:left;}
  .rubric-table th{color:var(--faint);font-size:11px;text-transform:uppercase;letter-spacing:.03em;}
  .rubric-table td.pts{text-align:right;font-weight:700;color:var(--accent);width:60px;}

  footer{padding:30px 0 60px;color:var(--faint);font-size:12.5px;}
  .gridjs-wrapper{box-shadow:none !important;border:1px solid var(--line) !important;}
  .gridjs-table{font-size:12px;}
  .note-inline{font-size:12.5px;color:var(--muted);background:var(--surface-2);border:1px solid var(--line);
    border-radius:10px;padding:10px 12px;margin-top:14px;}
</style>
</head>
<body>

<nav class="top">
  <div class="wrap">
    <span class="brand">SFUHS Civic Engagement Survey</span>
    <div class="links">
      <a href="#overview">Overview</a>
      <a href="#question">The Question</a>
      <a href="#knowledge">Knowledge Scores</a>
      <a href="#attitudes">Attitudes</a>
      <a href="#predict">What Predicts Support</a>
      <a href="#explore">Explore</a>
      <a href="#method">Method</a>
    </div>
  </div>
</nav>

<div class="wrap">

  <header class="hero" id="overview">
    <h1>Youth Civic Engagement &amp; Voting Attitudes</h1>
    <div class="sub">
      An interactive look at an April 2026 survey of students and faculty at SFUHS on lowering
      the voting age to 16, political engagement, and how much young people actually know about
      local government. Every open-text answer is scored on a transparent knowledge rubric.
    </div>
    <div class="tags">
      <span class="tag" id="tag-n">N = —</span>
      <span class="tag" id="tag-split">— students · — faculty</span>
      <span class="tag">Single school · San Francisco</span>
      <span class="tag">Convenience sample</span>
    </div>

    <div class="kpi-grid" id="kpis"></div>
    <div class="note-inline">
      <b>How to read this:</b> charts in the upper sections describe the full sample and don't change.
      The <a href="#explore">Explore</a> section and its filters let you slice individual responses.
      Knowledge scores are generated by a documented rubric — open any response to see exactly why it scored what it did.
    </div>
  </header>

  <!-- ============ THE QUESTION ============ -->
  <section id="question">
    <div class="sec-head">
      <h2>Should the voting age be lowered to 16?</h2>
      <p>The survey asked separately about <b>local</b> (San Francisco) and <b>federal</b> elections. Both groups
      are consistently more comfortable with a local lowering than a federal one — the local/federal split
      matters more than the student/faculty split.</p>
    </div>
    <div class="grid g-2">
      <div class="card">
        <h3>Support by role</h3>
        <p class="desc">Share choosing Yes / No / Unsure, students vs faculty.</p>
        <canvas id="ch-support" height="200"></canvas>
        <div class="takeaway" id="tk-support"></div>
      </div>
      <div class="card">
        <h3>Support pattern: local vs federal</h3>
        <p class="desc">Whether each respondent backs lowering in both arenas, one, or neither.</p>
        <canvas id="ch-pattern" height="200"></canvas>
        <div class="takeaway" id="tk-pattern"></div>
      </div>
      <div class="card">
        <h3>Student support by grade</h3>
        <p class="desc">"Yes" share for local lowering across grades 9–12, with sample size per grade.</p>
        <canvas id="ch-grade" height="200"></canvas>
        <div class="takeaway" id="tk-grade"></div>
      </div>
      <div class="card">
        <h3>Does knowing more change the answer?</h3>
        <p class="desc">Student "Yes" share for local lowering, grouped by mayor-knowledge band.</p>
        <canvas id="ch-band" height="200"></canvas>
        <div class="takeaway" id="tk-band"></div>
      </div>
    </div>
  </section>

  <!-- ============ KNOWLEDGE SCORES ============ -->
  <section id="knowledge">
    <div class="sec-head">
      <h2>How much do they actually know?</h2>
      <p>Three open-text answers were scored on fixed rubrics so "knowledge" is measured, not guessed.
      The headline measure is the <b>Mayor Knowledge Score</b>: students were asked what they know about the
      current SF mayor (Daniel Lurie), and answers were checked against verified facts about his agenda.</p>
    </div>
    <div class="grid g-12-5">
      <div class="card">
        <h3>Mayor Knowledge Score — distribution (students)</h3>
        <p class="desc">0 = no answer or no verifiable facts; 10 = names the mayor plus many accurate, specific policies.</p>
        <canvas id="ch-mayor-dist" height="170"></canvas>
        <div class="takeaway" id="tk-mayor"></div>
      </div>
      <div class="card">
        <h3>The scoring rubric</h3>
        <p class="desc">Points awarded per verified fact mentioned. Capped at 10.</p>
        <div style="max-height:300px;overflow:auto;">
          <table class="rubric-table" id="rubric-table"></table>
        </div>
      </div>
    </div>
    <div class="grid g-3">
      <div class="card">
        <h3>Reasoning Depth Score</h3>
        <p class="desc">Argument quality of the "explain your answer" text — length, specificity, multi-perspective, nuance. Not about <i>which</i> side they took.</p>
        <canvas id="ch-reason" height="190"></canvas>
        <div class="takeaway" id="tk-reason"></div>
      </div>
      <div class="card">
        <h3>Civic Literacy Index (students)</h3>
        <p class="desc">0–100 composite: 40% mayor knowledge + 35% reasoning depth + 25% political following.</p>
        <canvas id="ch-literacy" height="190"></canvas>
        <div class="takeaway" id="tk-literacy"></div>
      </div>
      <div class="card">
        <h3>Knowledge vs engagement</h3>
        <p class="desc">Each dot is a student: self-reported engagement (x) vs measured mayor knowledge (y).</p>
        <canvas id="ch-scatter" height="190"></canvas>
        <div class="takeaway" id="tk-scatter"></div>
      </div>
    </div>
  </section>

  <!-- ============ ATTITUDES ============ -->
  <section id="attitudes">
    <div class="sec-head">
      <h2>Attitudes &amp; engagement</h2>
      <p>Self-reported measures on 1–5 scales, plus where respondents get their news. Pick any item to see
      its full distribution rather than just an average.</p>
    </div>
    <div class="grid g-2">
      <div class="card">
        <h3>Self-reported attitudes — averages</h3>
        <p class="desc">Means on 1–5 scales. Higher = more (closer following / more influence / more aligned with parents / more likely to vote / more confident peers are informed).</p>
        <canvas id="ch-likert" height="220"></canvas>
        <div class="takeaway" id="tk-likert"></div>
      </div>
      <div class="card">
        <h3>Distribution explorer</h3>
        <p class="desc">Full response spread for one item at a time.</p>
        <div class="mini-tab" id="dist-tabs"></div>
        <canvas id="ch-dist" height="190"></canvas>
        <div class="legend" id="dist-legend"></div>
      </div>
      <div class="card">
        <h3>Where respondents get news</h3>
        <p class="desc">Share of each group selecting each source (multi-select question).</p>
        <canvas id="ch-news" height="200"></canvas>
        <div class="takeaway" id="tk-news"></div>
      </div>
      <div class="card">
        <h3>News source vs mayor knowledge</h3>
        <p class="desc">Average mayor-knowledge score among students who selected each source.</p>
        <canvas id="ch-news-know" height="200"></canvas>
        <div class="takeaway" id="tk-news-know"></div>
      </div>
    </div>
  </section>

  <!-- ============ WHAT PREDICTS SUPPORT ============ -->
  <section id="predict">
    <div class="sec-head">
      <h2>What predicts support?</h2>
      <p>A logistic regression on the student subsample (Unsure dropped, features standardized) and a
      correlation matrix. Both are <b>exploratory</b> — the sample is small relative to the number of
      variables, so read these as direction and relative strength, not population effects.</p>
    </div>
    <div class="grid g-5-12">
      <div class="card">
        <h3>Logistic regression — student support</h3>
        <p class="desc">Standardized coefficients. Green pushes toward "Yes", red toward "No". Longer bar = stronger association.</p>
        <div class="mini-tab" id="logit-tabs">
          <button class="on" data-pane="logit-local">Local lowering</button>
          <button data-pane="logit-federal">Federal lowering</button>
        </div>
        <div class="pane on" id="logit-local"></div>
        <div class="pane" id="logit-federal"></div>
        <div class="takeaway" id="tk-logit"></div>
      </div>
      <div class="card">
        <h3>Correlation matrix (students)</h3>
        <p class="desc">Pearson correlations among numeric measures, including the new knowledge scores. Green positive, red negative.</p>
        <div style="overflow:auto;">
          <table class="heat" id="heatmap"></table>
        </div>
        <div class="legend">Hover a cell for the exact value.</div>
      </div>
    </div>
  </section>

  <!-- ============ EXPLORE ============ -->
  <section id="explore">
    <div class="sec-head">
      <h2>Explore the responses</h2>
      <p>Filter and search individual responses. Every card shows the respondent's scores and — when you
      expand it — exactly which rubric items they hit. This is the audit trail for the knowledge scores.</p>
    </div>

    <div class="filterbar">
      <div class="fl"><label>Role</label>
        <select id="f-role"><option value="all">All</option><option>Student</option><option>Faculty</option></select>
      </div>
      <div class="fl"><label>Local 16+ support</label>
        <select id="f-local"><option value="all">All</option><option>Yes</option><option>No</option><option>Unsure</option></select>
      </div>
      <div class="fl"><label>Federal 16+ support</label>
        <select id="f-federal"><option value="all">All</option><option>Yes</option><option>No</option><option>Unsure</option></select>
      </div>
      <div class="fl"><label>Mayor knowledge</label>
        <select id="f-band"><option value="all">All</option><option>None (0)</option><option>Low (0.1-2.9)</option><option>Medium (3-5.9)</option><option>High (6-10)</option></select>
      </div>
      <div class="fl"><label>Grade</label>
        <select id="f-grade"><option value="all">All</option><option>9</option><option>10</option><option>11</option><option>12</option></select>
      </div>
      <div class="fl"><label>Sort by</label>
        <select id="f-sort">
          <option value="id">Response order</option>
          <option value="mayor_knowledge_score">Mayor knowledge ↓</option>
          <option value="reasoning_depth_score">Reasoning depth ↓</option>
          <option value="civic_literacy_index">Civic literacy ↓</option>
          <option value="engagement_index">Engagement ↓</option>
        </select>
      </div>
      <div class="fl"><label>Search text</label>
        <input id="f-search" type="text" placeholder="word in any open answer…" />
      </div>
      <button class="btn" id="f-reset">Reset</button>
      <span class="filter-count" id="f-count">—</span>
    </div>

    <div class="grid g-2" style="margin-top:16px;">
      <div class="card">
        <h3>Responses <span style="color:var(--faint);font-weight:500;" id="resp-n"></span></h3>
        <p class="desc">Each card reflects the filters above. Expand "scoring detail" to audit a knowledge score.</p>
        <div class="resp-list" id="resp-list"></div>
      </div>
      <div class="card">
        <h3>Filtered snapshot</h3>
        <p class="desc">Live summary of whoever is currently in the filter.</p>
        <canvas id="ch-filtered" height="150"></canvas>
        <div id="filtered-stats" style="margin-top:14px;"></div>
      </div>
    </div>

    <div class="card" style="margin-top:16px;">
      <h3>Full data table</h3>
      <p class="desc">Every respondent and every computed field. Sortable and searchable; reflects the filters above.</p>
      <div id="table"></div>
    </div>
  </section>

  <!-- ============ METHOD ============ -->
  <section id="method">
    <div class="sec-head"><h2>Methodology &amp; caveats</h2></div>
    <div class="grid g-2">
      <div class="card">
        <h3>How the scores work</h3>
        <table class="rubric-table">
          <tr><td><b>Mayor Knowledge</b> (0–10)</td><td>Points per verified fact about Mayor Lurie's agenda (see rubric above). Names him +2; specific policies +1 to +1.5 each. Null answers ("idk") = 0.</td></tr>
          <tr><td><b>Reasoning Depth</b> (0–10)</td><td>length (0–3) + specificity (0–3) + multi-perspective markers (0–2) + nuance/concession (0–2). Measures argument quality, independent of position.</td></tr>
          <tr><td><b>Civic Skills</b> (0–10)</td><td>Faculty only. Civic-concept hits (0–7) + length bonus (0–3) on the "what skills matter" answer.</td></tr>
          <tr><td><b>Engagement Index</b> (0–100)</td><td>Mean of follow-local, follow-federal, likelihood-to-vote, rescaled.</td></tr>
          <tr><td><b>Civic Literacy Index</b> (0–100)</td><td>40% mayor knowledge + 35% reasoning depth + 25% political following.</td></tr>
        </table>
      </div>
      <div class="card">
        <h3>Limitations — read before citing</h3>
        <p style="font-size:13px;color:var(--muted);">
        <b>Sample.</b> 83 respondents at one private SF high school, self-selected. Not representative of SF, California, or US teenagers.<br><br>
        <b>Significance.</b> The role × support chi-square tests do not reach conventional significance (p ≈ 0.5). Treat group differences as descriptive.<br><br>
        <b>Scores are heuristics.</b> Rubrics use keyword and structure matching, not human grading or NLP. They reward mentioning verifiable facts and structured argument; they can miss correct knowledge phrased unusually, or reward name-dropping. The point is a transparent, reproducible proxy — every score is auditable in the Explore section.<br><br>
        <b>Models.</b> The logistic regressions use ~57 students with 11 features; in-sample accuracy is inflated. Coefficients are directional only.
        </p>
      </div>
    </div>
  </section>

  <footer>
    Built from <code>analyze.py</code> + <code>build_dashboard.py</code>. Data: SFUHS Youth Civic Engagement &amp; Voting Attitudes Survey, April 2026.
    Mayor agenda facts verified against news sources, May 2026. All processing is reproducible from the raw CSV in <code>/data</code>.
  </footer>
</div>

<script>
const DATA = __DATA_JSON__;
const ROWS = DATA.rows, S = DATA.summary, RUBRICS = DATA.rubrics;
const C = {
  student:'#4f46e5', faculty:'#0e9aa7',
  yes:'#16a34a', no:'#dc2626', unsure:'#d97706',
  ink:'#1c2128', muted:'#62708a', line:'#e4e7ec', accent:'#4f46e5'
};
Chart.defaults.font.family = "-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif";
Chart.defaults.font.size = 11.5;
Chart.defaults.color = C.muted;
const charts = {};
function mk(id,cfg){ if(charts[id]) charts[id].destroy(); charts[id]=new Chart(document.getElementById(id),cfg); }
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
function pctOf(obj,key){ return obj && obj[key]!=null ? obj[key] : 0; }

/* ---------- header ---------- */
document.getElementById('tag-n').textContent = 'N = ' + S.n_total;
document.getElementById('tag-split').textContent = S.n_student + ' students · ' + S.n_faculty + ' faculty/staff';
const H = S.headline;
const KPIS = [
  {label:'Support local 16+', value:H.support_local_yes_overall+'%', note:'whole sample says Yes'},
  {label:'Support federal 16+', value:H.support_federal_yes_overall+'%', note:'whole sample says Yes'},
  {label:'Avg mayor knowledge', value:H.mean_mayor_knowledge_student+' / 10', note:'students, scored answer'},
  {label:'No mayor facts', value:H.pct_mayor_knowledge_zero+'%', note:'students scored 0'},
  {label:'Avg engagement', value:H.mean_engagement_student+' / 100', note:'students, self-reported'},
  {label:'Avg civic literacy', value:H.mean_civic_literacy_student+' / 100', note:'students, composite'},
];
document.getElementById('kpis').innerHTML = KPIS.map(k=>
  `<div class="kpi"><div class="label">${k.label}</div><div class="value">${k.value}</div><div class="note">${k.note}</div></div>`
).join('');

/* ---------- support by role ---------- */
(function(){
  const cats=['Yes','No','Unsure'], col={Yes:C.yes,No:C.no,Unsure:C.unsure};
  const labels=['Student · Local','Student · Federal','Faculty · Local','Faculty · Federal'];
  const tabs=[S.support_local_by_role.Student,S.support_federal_by_role.Student,
              S.support_local_by_role.Faculty,S.support_federal_by_role.Faculty];
  mk('ch-support',{type:'bar',data:{labels,datasets:cats.map(c=>({
      label:c,data:tabs.map(t=>+(pctOf(t,c)).toFixed(1)),backgroundColor:col[c],borderWidth:0,borderRadius:3
    }))},options:{indexAxis:'y',responsive:true,
    scales:{x:{stacked:true,max:100,ticks:{callback:v=>v+'%'},grid:{color:C.line}},
            y:{stacked:true,grid:{display:false}}},
    plugins:{legend:{position:'bottom'},tooltip:{callbacks:{label:c=>c.dataset.label+': '+c.parsed.x+'%'}}}}});
  const sl=S.support_local_by_role.Student, fl=S.support_federal_by_role.Student;
  document.getElementById('tk-support').innerHTML =
    `<b>${(+pctOf(sl,'Yes')).toFixed(0)}% of students</b> back a local lowering vs <b>${(+pctOf(fl,'Yes')).toFixed(0)}%</b> for federal. `+
    `Faculty lean more supportive on both, but with only ${S.n_faculty} faculty the gap isn't statistically significant `+
    `(χ²=${S.chi2.role_x_local.chi2}, p=${S.chi2.role_x_local.p}).`;
})();

/* ---------- support pattern ---------- */
(function(){
  const order=['Both','Local only','Federal only','Neither','Mixed/Unsure'];
  const cl={'Both':C.yes,'Local only':C.accent,'Federal only':'#7c3aed','Neither':C.no,'Mixed/Unsure':C.unsure};
  const sp=S.support_pattern;
  mk('ch-pattern',{type:'bar',data:{labels:['Student','Faculty'],datasets:order.map(o=>({
      label:o,data:[+pctOf(sp.Student,o).toFixed(1),+pctOf(sp.Faculty,o).toFixed(1)],
      backgroundColor:cl[o],borderWidth:0,borderRadius:3
    }))},options:{indexAxis:'y',responsive:true,
    scales:{x:{stacked:true,max:100,ticks:{callback:v=>v+'%'},grid:{color:C.line}},y:{stacked:true,grid:{display:false}}},
    plugins:{legend:{position:'bottom'},tooltip:{callbacks:{label:c=>c.dataset.label+': '+c.parsed.x+'%'}}}}});
  document.getElementById('tk-pattern').innerHTML =
    `"<b>Local only</b>" is a real group — students who'd lower the age for city elections but not federal ones. `+
    `Almost nobody supports federal-only. The asymmetry is one-directional: local is the easier ask.`;
})();

/* ---------- support by grade ---------- */
(function(){
  const gs=S.grade_support, grades=Object.keys(gs).map(Number).sort((a,b)=>a-b);
  mk('ch-grade',{type:'bar',data:{labels:grades.map(g=>'Grade '+g),datasets:[
    {label:'% Yes — local',data:grades.map(g=>+pctOf(gs[g].local,'Yes').toFixed(1)),backgroundColor:C.accent,borderRadius:4,
     yAxisID:'y'},
    {label:'Avg mayor knowledge',data:grades.map(g=>gs[g].mean_mayor_knowledge),type:'line',
     borderColor:C.faculty,backgroundColor:C.faculty,tension:.3,yAxisID:'y2',pointRadius:4}
  ]},options:{responsive:true,
    scales:{y:{position:'left',max:100,title:{display:true,text:'% Yes'},ticks:{callback:v=>v+'%'},grid:{color:C.line}},
            y2:{position:'right',max:10,title:{display:true,text:'Knowledge /10'},grid:{display:false}}},
    plugins:{legend:{position:'bottom'},tooltip:{callbacks:{
      afterBody:items=>{const g=grades[items[0].dataIndex];return 'n = '+gs[g].n;}}}}}});
  document.getElementById('tk-grade').innerHTML =
    `Support for a local lowering is <b>highest in the younger grades</b> and softens toward 12th. `+
    `Measured mayor knowledge moves the other way — older students know modestly more but are warier of the idea.`;
})();

/* ---------- support by knowledge band ---------- */
(function(){
  const bs=S.band_support, order=['None (0)','Low (0.1-2.9)','Medium (3-5.9)','High (6-10)'];
  const bands=order.filter(o=>bs[o]);
  mk('ch-band',{type:'bar',data:{labels:bands.map(b=>b.replace(/ \(.*\)/,'')+'  (n='+bs[b].n+')'),datasets:[
    {label:'Yes',data:bands.map(b=>+pctOf(bs[b].local,'Yes').toFixed(1)),backgroundColor:C.yes,borderRadius:3},
    {label:'No',data:bands.map(b=>+pctOf(bs[b].local,'No').toFixed(1)),backgroundColor:C.no,borderRadius:3},
    {label:'Unsure',data:bands.map(b=>+pctOf(bs[b].local,'Unsure').toFixed(1)),backgroundColor:C.unsure,borderRadius:3}
  ]},options:{indexAxis:'y',responsive:true,
    scales:{x:{stacked:true,max:100,ticks:{callback:v=>v+'%'},grid:{color:C.line}},y:{stacked:true,grid:{display:false}}},
    plugins:{legend:{position:'bottom'}}}});
  document.getElementById('tk-band').innerHTML =
    `Students who know more about the mayor are <b>not</b> uniformly more supportive — if anything the most "No" `+
    `responses cluster among those who know a fair amount. Knowledge tracks skepticism here, not enthusiasm. `+
    `(Bands are small — interpret loosely.)`;
})();

/* ---------- mayor knowledge distribution ---------- */
(function(){
  const d=S.distributions.mayor_knowledge_score.Student;
  const labels=Object.keys(d);
  mk('ch-mayor-dist',{type:'bar',data:{labels,datasets:[
    {label:'Students',data:labels.map(k=>d[k]),
     backgroundColor:labels.map(k=>k==='0'?C.no:k==='8-10'?C.yes:C.accent),borderRadius:4}
  ]},options:{responsive:true,
    scales:{y:{title:{display:true,text:'# students'},grid:{color:C.line}},x:{title:{display:true,text:'Mayor knowledge score'},grid:{display:false}}},
    plugins:{legend:{display:false}}}});
  document.getElementById('tk-mayor').innerHTML =
    `<b>${H.pct_mayor_knowledge_zero}% of students scored 0</b> — they left it blank or gave no verifiable facts. `+
    `Only a handful score above 6. Average is <b>${H.mean_mayor_knowledge_student}/10</b>. Civic awareness of city government is thin even at an engaged school.`;
})();

/* ---------- rubric table ---------- */
(function(){
  const t=document.getElementById('rubric-table');
  t.innerHTML='<tr><th>Verified fact mentioned</th><th class="pts">Pts</th></tr>'+
    RUBRICS.mayor_knowledge.map(r=>`<tr><td>${esc(r.label)}</td><td class="pts">+${r.points}</td></tr>`).join('');
})();

/* ---------- reasoning depth ---------- */
(function(){
  const d=S.distributions.reasoning_depth_score;
  const labels=Object.keys(d.Student);
  mk('ch-reason',{type:'bar',data:{labels,datasets:[
    {label:'Student',data:labels.map(k=>d.Student[k]||0),backgroundColor:C.student,borderRadius:4},
    {label:'Faculty',data:labels.map(k=>(d.Faculty&&d.Faculty[k])||0),backgroundColor:C.faculty,borderRadius:4}
  ]},options:{responsive:true,scales:{y:{grid:{color:C.line}},x:{title:{display:true,text:'Reasoning depth score'},grid:{display:false}}},
    plugins:{legend:{position:'bottom'}}}});
  document.getElementById('tk-reason').innerHTML =
    `Faculty average <b>${H.mean_reasoning_faculty}/10</b> vs students' <b>${H.mean_reasoning_student}/10</b>. `+
    `Most student explanations are short and single-angle; the longest, most-qualified arguments come from faculty.`;
})();

/* ---------- civic literacy index ---------- */
(function(){
  const vals=ROWS.filter(r=>r.role==='Student'&&r.civic_literacy_index!=null).map(r=>r.civic_literacy_index);
  const bins=[0,10,20,30,40,50,60,70], counts=new Array(bins.length-1).fill(0);
  vals.forEach(v=>{for(let i=0;i<bins.length-1;i++){if(v>=bins[i]&&v<bins[i+1]){counts[i]++;break;}}});
  mk('ch-literacy',{type:'bar',data:{labels:bins.slice(0,-1).map((b,i)=>b+'–'+bins[i+1]),
    datasets:[{label:'Students',data:counts,backgroundColor:C.accent,borderRadius:4}]},
    options:{responsive:true,scales:{y:{grid:{color:C.line}},x:{title:{display:true,text:'Civic literacy index (0–100)'},grid:{display:false}}},
      plugins:{legend:{display:false}}}});
  const mean=H.mean_civic_literacy_student;
  document.getElementById('tk-literacy').innerHTML =
    `The composite centers low — mean <b>${mean}/100</b> — because two of its three inputs (factual knowledge, reasoning depth) score low. `+
    `Self-reported following alone would paint a rosier picture.`;
})();

/* ---------- scatter: knowledge vs engagement ---------- */
(function(){
  const pts=ROWS.filter(r=>r.role==='Student'&&r.engagement_index!=null)
    .map(r=>({x:r.engagement_index,y:r.mayor_knowledge_score}));
  mk('ch-scatter',{type:'scatter',data:{datasets:[{label:'Student',data:pts,
    backgroundColor:'rgba(79,70,229,.55)',pointRadius:5}]},
    options:{responsive:true,
      scales:{x:{title:{display:true,text:'Engagement index (self-reported)'},min:0,max:100,grid:{color:C.line}},
              y:{title:{display:true,text:'Mayor knowledge (measured)'},min:0,max:10,grid:{color:C.line}}},
      plugins:{legend:{display:false}}}});
  const corr=S.correlations.engagement_index.mayor_knowledge_score;
  document.getElementById('tk-scatter').innerHTML =
    `Self-reported engagement and measured knowledge correlate only <b>r = ${corr!=null?corr.toFixed(2):'—'}</b>. `+
    `Feeling engaged and being able to name what the mayor is doing are loosely related at best.`;
})();

/* ---------- likert means ---------- */
(function(){
  const fields=[['follow_local','Follow local politics'],['follow_federal','Follow federal politics'],
    ['influence_local','Influence — local'],['influence_federal','Influence — federal'],
    ['align_parents','Aligns with parents'],['likelihood_vote','Would vote in SF'],
    ['informed_local','16–18 informed: local'],['informed_federal','16–18 informed: federal']];
  mk('ch-likert',{type:'bar',data:{labels:fields.map(f=>f[1]),datasets:[
    {label:'Student',data:fields.map(f=>S.likert_means[f[0]].Student.mean),backgroundColor:C.student,borderRadius:3},
    {label:'Faculty',data:fields.map(f=>S.likert_means[f[0]].Faculty.mean),backgroundColor:C.faculty,borderRadius:3}
  ]},options:{indexAxis:'y',responsive:true,
    scales:{x:{min:0,max:5,grid:{color:C.line}},y:{grid:{display:false}}},
    plugins:{legend:{position:'bottom'},tooltip:{callbacks:{label:c=>c.dataset.label+': '+(c.parsed.x==null?'n/a':c.parsed.x)}}}}});
  document.getElementById('tk-likert').innerHTML =
    `Students rate their <b>own influence very low</b> (≈1.5/5) yet their <b>alignment with parents very high</b> (≈4/5) — `+
    `exactly the combination skeptics cite. Students and faculty rate teen "informedness" almost identically.`;
})();

/* ---------- distribution explorer ---------- */
(function(){
  const items=[['follow_local','Follow local politics'],['follow_federal','Follow federal politics'],
    ['influence_local','Influence (local)'],['influence_federal','Influence (federal)'],
    ['align_parents','Aligns with parents'],['likelihood_vote','Would vote in SF'],
    ['informed_local','Teens informed: local'],['informed_federal','Teens informed: federal']];
  const tabs=document.getElementById('dist-tabs');
  tabs.innerHTML=items.map((it,i)=>`<button class="${i===0?'on':''}" data-k="${it[0]}">${it[1]}</button>`).join('');
  function draw(key,name){
    const d=S.distributions[key];
    const labels=['1','2','3','4','5'];
    const ds=[];
    if(d.Student) ds.push({label:'Student',data:labels.map(l=>d.Student[l]||0),backgroundColor:C.student,borderRadius:3});
    if(d.Faculty) ds.push({label:'Faculty',data:labels.map(l=>d.Faculty[l]||0),backgroundColor:C.faculty,borderRadius:3});
    mk('ch-dist',{type:'bar',data:{labels:labels.map(l=>'Rating '+l),datasets:ds},
      options:{responsive:true,scales:{y:{grid:{color:C.line}},x:{grid:{display:false}}},
        plugins:{legend:{position:'bottom'},title:{display:false}}}});
    document.getElementById('dist-legend').textContent = name+' — 1 (low) to 5 (high). Faculty did not answer influence/parents/vote items.';
  }
  tabs.addEventListener('click',e=>{
    const b=e.target.closest('button'); if(!b)return;
    tabs.querySelectorAll('button').forEach(x=>x.classList.remove('on')); b.classList.add('on');
    draw(b.dataset.k,b.textContent);
  });
  draw('follow_local','Follow local politics');
})();

/* ---------- news sources ---------- */
(function(){
  const srcs=Object.keys(S.news_counts.Student);
  const short=srcs.map(s=>s.replace(/ \(.*\)/,''));
  const stuTot=S.n_student, facTot=S.n_faculty;
  mk('ch-news',{type:'bar',data:{labels:short,datasets:[
    {label:'Student',data:srcs.map(s=>Math.round(100*S.news_counts.Student[s]/stuTot)),backgroundColor:C.student,borderRadius:3},
    {label:'Faculty',data:srcs.map(s=>Math.round(100*S.news_counts.Faculty[s]/facTot)),backgroundColor:C.faculty,borderRadius:3}
  ]},options:{responsive:true,scales:{y:{max:100,ticks:{callback:v=>v+'%'},grid:{color:C.line}},x:{grid:{display:false}}},
    plugins:{legend:{position:'bottom'}}}});
  document.getElementById('tk-news').innerHTML =
    `Traditional news is the common thread for both groups. Students add <b>social media</b> heavily; `+
    `faculty lean on <b>podcasts</b> and traditional outlets and largely skip social media.`;
})();

/* ---------- news source vs knowledge ---------- */
(function(){
  const sk=S.source_knowledge, srcs=Object.keys(sk);
  mk('ch-news-know',{type:'bar',data:{labels:srcs.map(s=>s.replace(/ \(.*\)/,'')),datasets:[
    {label:'Avg mayor knowledge',data:srcs.map(s=>sk[s].mean_mayor_knowledge),backgroundColor:C.accent,borderRadius:3}
  ]},options:{indexAxis:'y',responsive:true,
    scales:{x:{min:0,max:10,grid:{color:C.line}},y:{grid:{display:false}}},
    plugins:{legend:{display:false},tooltip:{callbacks:{afterBody:it=>'n = '+sk[srcs[it[0].dataIndex]].n}}}}});
  document.getElementById('tk-news-know').innerHTML =
    `Differences are small and the subgroups overlap heavily (most students pick several sources), `+
    `so don't over-read this — but no single source stands out as a knowledge booster in this sample.`;
})();

/* ---------- logistic regression ---------- */
(function(){
  function render(model,elId){
    const el=document.getElementById(elId);
    if(!model){el.innerHTML='<div class="legend">Not enough data.</div>';return;}
    const entries=Object.entries(model.coefs).sort((a,b)=>Math.abs(b[1])-Math.abs(a[1]));
    const max=Math.max(...entries.map(e=>Math.abs(e[1])))||1;
    el.innerHTML=`<div class="legend" style="margin-bottom:8px;">n = ${model.n} · base "Yes" rate ${(model.support_yes_rate*100).toFixed(0)}% · in-sample accuracy ${(model.accuracy*100).toFixed(0)}% (inflated — see Method)</div>`+
      entries.map(([k,v])=>{
        const w=Math.min(50,Math.abs(v)/max*50);
        const bar=v>=0?`<span class="bar pos" style="width:${w}%"></span>`:`<span class="bar neg" style="width:${w}%"></span>`;
        return `<div class="coef-row"><div>${k.replace(/_/g,' ')}</div>`+
               `<div class="coef-track"><span class="mid"></span>${bar}</div>`+
               `<div style="text-align:right;color:${v>=0?C.yes:C.no};font-weight:700;">${v.toFixed(2)}</div></div>`;
      }).join('');
  }
  render(S.logit_local_student,'logit-local');
  render(S.logit_federal_student,'logit-federal');
  const tabs=document.getElementById('logit-tabs');
  tabs.addEventListener('click',e=>{
    const b=e.target.closest('button'); if(!b)return;
    tabs.querySelectorAll('button').forEach(x=>x.classList.remove('on')); b.classList.add('on');
    document.querySelectorAll('#predict .pane').forEach(p=>p.classList.remove('on'));
    document.getElementById(b.dataset.pane).classList.add('on');
  });
  const c=S.logit_local_student.coefs;
  const topPos=Object.entries(c).filter(e=>e[1]>0).sort((a,b)=>b[1]-a[1])[0];
  const topNeg=Object.entries(c).filter(e=>e[1]<0).sort((a,b)=>a[1]-b[1])[0];
  document.getElementById('tk-logit').innerHTML =
    `For local lowering, the strongest "Yes" pull is <b>${topPos[0].replace(/_/g,' ')}</b> and the strongest "No" pull is `+
    `<b>${topNeg[0].replace(/_/g,' ')}</b>. Believing peers are <i>informed enough</i> drives support far more than a student's own engagement or measured knowledge.`;
})();

/* ---------- correlation heatmap ---------- */
(function(){
  const corr=S.correlations, cols=Object.keys(corr);
  const shortName=s=>s.replace(/_/g,' ').replace('mayor knowledge score','mayor knowl.')
    .replace('reasoning depth score','reasoning').replace('civic literacy index','civ. literacy')
    .replace('engagement index','engagement').replace('news diversity','news div.')
    .replace('influence ','infl. ').replace('informed ','inf. ');
  let html='<tr><th></th>'+cols.map(c=>`<th class="rot">${shortName(c)}</th>`).join('')+'</tr>';
  cols.forEach(r=>{
    html+=`<tr><td class="lbl">${shortName(r)}</td>`;
    cols.forEach(c=>{
      const v=corr[r][c];
      if(v==null){html+='<td>—</td>';return;}
      const a=Math.abs(v);
      const bg=v>=0?`rgba(22,163,74,${(a*0.95).toFixed(2)})`:`rgba(220,38,38,${(a*0.95).toFixed(2)})`;
      const fg=a>0.5?'#fff':C.muted;
      html+=`<td style="background:${bg};color:${fg};" title="${shortName(r)} × ${shortName(c)} = ${v.toFixed(3)}">${v.toFixed(2)}</td>`;
    });
    html+='</tr>';
  });
  document.getElementById('heatmap').innerHTML=html;
})();

/* ================= EXPLORE ================= */
const Q = {
  explanation:'Explain your answer', mayor_knowledge_text:'What they know about the SF mayor',
  reasoning_text:'Reasoning on student voting readiness', civic_skills_text:'Civic skills that matter most'
};
function scoreChip(name,val,max){
  const w=Math.max(0,Math.min(100,val/max*100));
  return `<span class="scorechip">${name} <b>${val}</b>/${max} <span class="scorebar"><i style="width:${w}%"></i></span></span>`;
}
function respCard(r){
  const isStu=r.role==='Student';
  let meta=`<span class="pill role ${isStu?'':'fac'}">${r.role}</span>`;
  if(isStu) meta+=`<span class="pill demo">age ${r.age??'?'} · grade ${r.grade??'?'}</span>`;
  else meta+=`<span class="pill demo">${esc(r.subject||'—')} · ${esc(r.years_in_ed||'?')} yrs</span>`;
  meta+=` <span class="pill ${String(r.support_local_16||'').toLowerCase()}">local: ${esc(r.support_local_16||'—')}</span>`;
  meta+=`<span class="pill ${String(r.support_federal_16||'').toLowerCase()}">federal: ${esc(r.support_federal_16||'—')}</span>`;

  let scores='';
  if(isStu){
    scores+=scoreChip('Mayor knowl.',r.mayor_knowledge_score,10);
    scores+=scoreChip('Reasoning',r.reasoning_depth_score,10);
    if(r.civic_literacy_index!=null) scores+=scoreChip('Civ. literacy',r.civic_literacy_index,100);
    if(r.engagement_index!=null) scores+=scoreChip('Engagement',r.engagement_index,100);
  } else {
    scores+=scoreChip('Reasoning',r.reasoning_depth_score,10);
    scores+=scoreChip('Civic skills',r.civic_skills_score,10);
  }

  let qa='';
  if(r.explanation) qa+=`<div class="qa"><span class="q">${Q.explanation}</span><br>${esc(r.explanation)}</div>`;
  if(r.mayor_knowledge_text) qa+=`<div class="qa"><span class="q">${Q.mayor_knowledge_text}</span><br>${esc(r.mayor_knowledge_text)}</div>`;
  if(r.reasoning_text) qa+=`<div class="qa"><span class="q">${Q.reasoning_text}</span><br>${esc(r.reasoning_text)}</div>`;
  if(r.civic_skills_text) qa+=`<div class="qa"><span class="q">${Q.civic_skills_text}</span><br>${esc(r.civic_skills_text)}</div>`;

  let rub='';
  if(isStu){
    const hits=r.mayor_knowledge_hits||[];
    const rp=r.reasoning_parts||{};
    rub=`<details class="rubric"><summary>Scoring detail</summary>`+
      `<div style="margin-top:5px;font-size:11.5px;color:var(--muted);"><b>Mayor knowledge ${r.mayor_knowledge_score}/10</b> — `+
      (hits.length?hits.map(h=>`<span class="hit">${esc(h)}</span>`).join(''):'no verifiable facts')+`</div>`+
      `<div style="margin-top:4px;font-size:11.5px;color:var(--muted);"><b>Reasoning ${r.reasoning_depth_score}/10</b> — `+
      `length ${rp.length??0}, specificity ${rp.specificity??0}, multi-perspective ${rp.perspective??0}, nuance ${rp.nuance??0} (${rp.words??0} words)</div>`+
      `</details>`;
  }
  return `<div class="resp"><div class="meta">${meta}</div><div>${scores}</div>${qa}${rub}</div>`;
}

let gridInstance=null;
function getFiltered(){
  const role=document.getElementById('f-role').value;
  const loc=document.getElementById('f-local').value;
  const fed=document.getElementById('f-federal').value;
  const band=document.getElementById('f-band').value;
  const grade=document.getElementById('f-grade').value;
  const sort=document.getElementById('f-sort').value;
  const q=document.getElementById('f-search').value.trim().toLowerCase();
  let out=ROWS.filter(r=>{
    if(role!=='all'&&r.role!==role) return false;
    if(loc!=='all'&&r.support_local_16!==loc) return false;
    if(fed!=='all'&&r.support_federal_16!==fed) return false;
    if(band!=='all'&&r.mayor_knowledge_band!==band) return false;
    if(grade!=='all'&&String(r.grade)!==grade) return false;
    if(q){
      const blob=[r.explanation,r.mayor_knowledge_text,r.reasoning_text,r.civic_skills_text]
        .filter(Boolean).join(' ').toLowerCase();
      if(!blob.includes(q)) return false;
    }
    return true;
  });
  if(sort!=='id') out=out.slice().sort((a,b)=>(b[sort]??-1)-(a[sort]??-1));
  return out;
}
function renderExplore(){
  const f=getFiltered();
  document.getElementById('f-count').textContent=f.length+' of '+ROWS.length+' shown';
  document.getElementById('resp-n').textContent='('+f.length+')';
  document.getElementById('resp-list').innerHTML=f.length?f.map(respCard).join(''):'<div class="legend">No responses match these filters.</div>';

  // filtered snapshot chart
  const cats=['Yes','No','Unsure'];
  function share(key){
    const known=f.filter(r=>r[key]!=null);
    return cats.map(c=>known.length?Math.round(100*known.filter(r=>r[key]===c).length/known.length):0);
  }
  mk('ch-filtered',{type:'bar',data:{labels:['Local 16+','Federal 16+'],datasets:cats.map((c,i)=>({
    label:c,data:[share('support_local_16')[i],share('support_federal_16')[i]],
    backgroundColor:[C.yes,C.no,C.unsure][i],borderRadius:3
  }))},options:{indexAxis:'y',responsive:true,
    scales:{x:{stacked:true,max:100,ticks:{callback:v=>v+'%'},grid:{color:C.line}},y:{stacked:true,grid:{display:false}}},
    plugins:{legend:{position:'bottom'}}}});

  const stu=f.filter(r=>r.role==='Student');
  function avg(arr,k){const v=arr.map(r=>r[k]).filter(x=>x!=null);return v.length?(v.reduce((a,b)=>a+b,0)/v.length):null;}
  const mk1=avg(stu,'mayor_knowledge_score'), rd=avg(f,'reasoning_depth_score'),
        ci=avg(stu,'civic_literacy_index'), en=avg(stu,'engagement_index');
  document.getElementById('filtered-stats').innerHTML=
    `<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;font-size:12.5px;">`+
    `<div class="note-inline" style="margin:0;">Avg mayor knowledge<br><b style="font-size:18px;color:var(--ink);">${mk1==null?'—':mk1.toFixed(2)+' / 10'}</b><br><span style="font-size:11px;">${stu.length} students</span></div>`+
    `<div class="note-inline" style="margin:0;">Avg reasoning depth<br><b style="font-size:18px;color:var(--ink);">${rd==null?'—':rd.toFixed(2)+' / 10'}</b><br><span style="font-size:11px;">${f.length} responses</span></div>`+
    `<div class="note-inline" style="margin:0;">Avg civic literacy<br><b style="font-size:18px;color:var(--ink);">${ci==null?'—':ci.toFixed(1)+' / 100'}</b></div>`+
    `<div class="note-inline" style="margin:0;">Avg engagement<br><b style="font-size:18px;color:var(--ink);">${en==null?'—':en.toFixed(1)+' / 100'}</b></div>`+
    `</div>`;

  // table
  const cols=['id','role','age','grade','support_local_16','support_federal_16',
    'mayor_knowledge_score','reasoning_depth_score','civic_literacy_index','engagement_index',
    'follow_local','follow_federal','influence_local','align_parents','likelihood_vote',
    'informed_local','informed_federal','news_diversity','subject','years_in_ed','civic_skills_score'];
  const tdata=f.map(r=>cols.map(c=>r[c]==null?'':r[c]));
  if(gridInstance){gridInstance.destroy();}
  gridInstance=new gridjs.Grid({
    columns:cols.map(c=>({name:c.replace(/_/g,' ')})),
    data:tdata,sort:true,search:true,resizable:true,
    pagination:{limit:20},
  }).render(document.getElementById('table'));
}
['f-role','f-local','f-federal','f-band','f-grade','f-sort','f-search'].forEach(id=>{
  const el=document.getElementById(id);
  el.addEventListener('input',renderExplore);
  el.addEventListener('change',renderExplore);
});
document.getElementById('f-reset').addEventListener('click',()=>{
  ['f-role','f-local','f-federal','f-band','f-grade'].forEach(id=>document.getElementById(id).value='all');
  document.getElementById('f-sort').value='id';
  document.getElementById('f-search').value='';
  renderExplore();
});
renderExplore();
</script>
</body>
</html>
"""

with open("index.html", "w") as f:
    f.write(HTML.replace("__DATA_JSON__", DATA_JSON))

# keep dashboard.html as an alias so existing links don't break
with open("dashboard.html", "w") as f:
    f.write(HTML.replace("__DATA_JSON__", DATA_JSON))

print("Wrote index.html and dashboard.html")
