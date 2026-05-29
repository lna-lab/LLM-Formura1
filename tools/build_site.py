#!/usr/bin/env python3
"""build_site.py — generate the static LLM Formula site + leaderboard.

Reads results/**/*.json (llmf-result manifests) and emits site/index.html:
a self-contained, backend-free page deployable to any web host (e.g. Xserver
public_html via SFTP). Re-run after each merged result to refresh the board.

  python3 tools/build_site.py            # -> site/index.html
"""
import json, os, glob, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLASSES = ["GP1000", "GP400", "E50"]
DISC = [("efficiency", "Efficiency — tokens / joule", "tokens_per_joule", True),
        ("pace", "Pace — tokens / second", "tokens_per_second", True),
        ("endurance", "Endurance — aggregate t/s", "tokens_per_second", True)]


def load():
    rows = []
    for f in glob.glob(os.path.join(ROOT, "results", "**", "*.json"), recursive=True):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        if d.get("schema", "").startswith("llmf-result"):
            rows.append(d)
    return rows


def g(d, *path, default=None):
    for k in path:
        d = (d or {}).get(k) if isinstance(d, dict) else None
    return d if d is not None else default


def fmt(x, n=4):
    return f"{x:.{n}f}" if isinstance(x, (int, float)) else "—"


def status_badge(d):
    if g(d, "reproduction", "steward_verified"):
        return '<span class="b ok">✔ verified</span>'
    if g(d, "scoring_eligible") is False or g(d, "measurement", "sensor_class") in ("firmware", "manual"):
        return '<span class="b exh">exhibition</span>'
    return '<span class="b prov">provisional</span>'


def table(rows, metric, n):
    rows = [r for r in rows if isinstance(g(r, "results", metric), (int, float))]
    rows.sort(key=lambda r: g(r, "results", metric), reverse=True)
    if not rows:
        return '<p class="empty">No entries yet — <a href="#enter">be the first</a>.</p>'
    out = ['<table><thead><tr><th>#</th><th>Entrant</th><th>Engine</th>'
           f'<th class="m">{"tok/J" if metric=="tokens_per_joule" else "t/s"}</th>'
           '<th>Watts</th><th>Status</th></tr></thead><tbody>']
    for i, r in enumerate(rows, 1):
        out.append(
            f'<tr><td class="rk">{i}</td>'
            f'<td>{html.escape(str(g(r,"entrant","handle",default="?")))}</td>'
            f'<td>{html.escape(str(g(r,"engine","name",default="?")))}</td>'
            f'<td class="m">{fmt(g(r,"results",metric), n)}</td>'
            f'<td>{fmt(g(r,"measurement","avg_system_watts"),1)}</td>'
            f'<td>{status_badge(r)}</td></tr>')
    out.append("</tbody></table>")
    return "".join(out)


def build():
    rows = load()
    sections = []
    for cls in CLASSES:
        crows = [r for r in rows if r.get("class") == cls]
        blocks = []
        for key, title, metric, _ in DISC:
            drows = [r for r in crows if r.get("discipline") == key]
            n = 5 if metric == "tokens_per_joule" else 2
            blocks.append(f'<h3>{title}</h3>{table(drows, metric, n)}')
        sections.append(f'<section class="cls"><h2>{cls}</h2>{"".join(blocks)}</section>')
    page = TEMPLATE.format(classes="".join(sections), n=len(rows))
    os.makedirs(os.path.join(ROOT, "site"), exist_ok=True)
    open(os.path.join(ROOT, "site", "index.html"), "w", encoding="utf-8").write(page)
    print(f"[build_site] {len(rows)} result(s) -> site/index.html")


TEMPLATE = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>LLM Formula — World Championship of Inference Efficiency</title>
<meta name="description" content="The open world championship of LLM inference efficiency. Tokens per joule. Don't burn cash with your tokens — burn passion.">
<style>
:root{{--bg:#0a0c10;--card:#13171f;--fg:#e8edf4;--mut:#8b97a8;--acc:#ff2d2d;--ok:#28c76f;--prov:#f0a500}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 system-ui,"Segoe UI",Roboto,sans-serif}}
.wrap{{max-width:980px;margin:0 auto;padding:0 20px}}
header{{padding:54px 0 28px;border-bottom:2px solid #1c2230;background:
 repeating-linear-gradient(45deg,#0a0c10 0 14px,#0c0f15 14px 28px)}}
h1{{font-size:2.6rem;margin:0 0 .1em;letter-spacing:.04em}}h1 .f{{color:var(--acc)}}
.tag{{color:var(--mut);font-size:1.05rem;margin:.2em 0}}
.motto{{margin:18px 0 4px;font-size:1.35rem;font-weight:700}}
.motto small{{display:block;color:var(--mut);font-weight:400;font-size:.95rem;margin-top:.2em}}
h2{{margin:46px 0 6px;font-size:1.7rem;border-left:5px solid var(--acc);padding-left:.5em}}
h3{{margin:26px 0 8px;color:var(--mut);font-size:1rem;text-transform:uppercase;letter-spacing:.08em}}
table{{width:100%;border-collapse:collapse;background:var(--card);border-radius:10px;overflow:hidden}}
th,td{{padding:9px 12px;text-align:left;border-bottom:1px solid #1c2230;font-variant-numeric:tabular-nums}}
th{{color:var(--mut);font-size:.78rem;text-transform:uppercase;letter-spacing:.06em}}
td.m,th.m{{text-align:right;font-weight:700}}td.rk{{color:var(--acc);font-weight:700;width:2em}}
.b{{font-size:.72rem;padding:2px 8px;border-radius:20px}}
.b.ok{{background:rgba(40,199,111,.15);color:var(--ok)}}
.b.prov{{background:rgba(240,165,0,.15);color:var(--prov)}}
.b.exh{{background:#1c2230;color:var(--mut)}}
.empty{{color:var(--mut)}}.classes-row{{display:flex;gap:10px;flex-wrap:wrap;margin:18px 0}}
.chip{{background:var(--card);border:1px solid #1c2230;border-radius:8px;padding:8px 14px}}
.chip b{{color:var(--acc)}}
a{{color:#6db3ff;text-decoration:none}}a:hover{{text-decoration:underline}}
.docs a{{display:inline-block;margin:6px 14px 6px 0}}
footer{{color:var(--mut);font-size:.85rem;margin:50px 0 30px;border-top:1px solid #1c2230;padding-top:18px}}
.note{{color:var(--mut);font-size:.9rem}}
</style></head><body>
<header><div class="wrap">
<h1>🏁 LLM <span class="f">Formula</span></h1>
<p class="tag">The World Championship of Inference Efficiency</p>
<p class="motto">🔥 Don't burn cash with your tokens — burn passion.
<small>The cleverest joule wins.</small></p>
<div class="classes-row">
<div class="chip"><b>GP1000</b> ≤1000 W · the iconic flagship</div>
<div class="chip"><b>GP400</b> ≤400 W · the grid</div>
<div class="chip"><b>E50</b> ≤50 W · the edge</div>
</div>
<p class="note">Headline metric: <b>tokens / joule</b> at the wall. Any vendor, any interconnect —
Apple Silicon, AMD, CPU, NVIDIA all first-class. Correctness-gated (correctness before speed).</p>
</div></header>
<div class="wrap">
<p class="note">{n} provisional entries · steward-verified results are set on a held-out sealed slice.</p>
{classes}
<section id="enter"><h2>Enter</h2>
<p>Run the one-command harness <code>llmf-bench</code> on a homologated engine, pass scrutineering,
submit your result manifest. Privateers, students, garage tuners — bring your cleverest joule.</p>
<div class="docs">
<a href="https://github.com/lna-lab/LLM-Formura1/blob/main/REGULATIONS.md">📕 Regulations</a>
<a href="https://github.com/lna-lab/LLM-Formura1/blob/main/MEASUREMENT.md">📐 Measurement Standard</a>
<a href="https://github.com/lna-lab/LLM-Formura1/blob/main/ENTRY.md">🏁 How to Enter</a>
<a href="https://github.com/lna-lab/LLM-Formura1/blob/main/PARTNERS.md">🤝 Partners &amp; Sponsors</a>
<a href="https://github.com/lna-lab/LLM-Formura1/tree/main/tools/llmf-bench">🔧 llmf-bench tool</a>
</div></section>
<footer>LLM Formula · Season 1 (2026) · issued by Lna-Lab · Regulations CC BY 4.0 ·
generated by tools/build_site.py · <i>Built with passion. Tuned by physics.</i></footer>
</div></body></html>"""


if __name__ == "__main__":
    build()
