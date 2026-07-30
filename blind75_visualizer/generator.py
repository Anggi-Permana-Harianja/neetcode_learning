#!/usr/bin/env python3
"""Builds the Blind 75 Visualizer static site from data/problems.py.

Output is plain, dependency-free HTML/CSS/JS meant to be opened directly
from disk (file://) — no server, no runtime fetch of data. Each problem
page embeds its own code + (optionally) its own step data inline.

Usage: python3 generator.py
"""
import html
import io
import json
import keyword
import tokenize
from pathlib import Path

from data.problems import CATEGORIES, PROBLEMS

ROOT = Path(__file__).parent
OUT_PROBLEMS = ROOT / "problems"
OUT_PROBLEMS.mkdir(exist_ok=True)

BUILTINS = {
    "len", "range", "enumerate", "max", "min", "sum", "sorted", "list", "dict",
    "set", "tuple", "str", "int", "float", "bool", "abs", "isinstance", "zip",
    "map", "filter", "reversed", "print", "all", "any", "divmod", "ord", "chr",
    "super", "type", "frozenset", "round", "hash",
}

TOKEN_CLASS = {
    tokenize.COMMENT: "cm",
    tokenize.STRING: "str",
    tokenize.NUMBER: "num",
}


def highlight_python(code: str) -> list[str]:
    """Returns a list of HTML strings, one per source line (no wrapper tags)."""
    lines = code.splitlines()
    # per-line list of (col_start, col_end, html_fragment)
    spans: list[list[tuple[int, int, str]]] = [[] for _ in lines]

    tok_list = []
    try:
        toks = list(tokenize.generate_tokens(io.StringIO(code).readline))
        for idx, tok in enumerate(toks):
            tok_list.append(tok)
    except tokenize.TokenizeError:
        tok_list = []

    for idx, tok in enumerate(tok_list):
        ttype, tstring, start, end, _ = tok
        if ttype in (tokenize.NEWLINE, tokenize.NL, tokenize.INDENT,
                     tokenize.DEDENT, tokenize.ENDMARKER, tokenize.ENCODING):
            continue
        cls = None
        if ttype == tokenize.NAME:
            if keyword.iskeyword(tstring):
                cls = "kw"
            elif tstring in BUILTINS:
                cls = "bi"
            else:
                nxt = tok_list[idx + 1] if idx + 1 < len(tok_list) else None
                if nxt and nxt[0] == tokenize.OP and nxt[1] == "(":
                    cls = "fn"
        else:
            cls = TOKEN_CLASS.get(ttype)

        escaped = html.escape(tstring)
        frag = f'<span class="{cls}">{escaped}</span>' if cls else escaped

        srow, scol = start
        erow, ecol = end
        if srow == erow:
            if 0 <= srow - 1 < len(spans):
                spans[srow - 1].append((scol, ecol, frag))
        else:
            # multi-line token (e.g. triple-quoted string): split by line
            parts = tstring.split("\n")
            for i, part in enumerate(parts):
                row = srow - 1 + i
                if row < 0 or row >= len(spans):
                    continue
                pescaped = html.escape(part)
                pfrag = f'<span class="{cls}">{pescaped}</span>' if cls else pescaped
                col_s = scol if i == 0 else 0
                col_e = col_s + len(part)
                spans[row].append((col_s, col_e, pfrag))

    out = []
    for i, line in enumerate(lines):
        line_spans = sorted(spans[i], key=lambda s: s[0])
        pieces = []
        cursor = 0
        for s, e, frag in line_spans:
            if s > cursor:
                pieces.append(html.escape(line[cursor:s]))
            pieces.append(frag)
            cursor = max(cursor, e)
        if cursor < len(line):
            pieces.append(html.escape(line[cursor:]))
        out.append("".join(pieces) if pieces else "")
    return out


def code_block_html(code: str, active_line: int | None = None) -> str:
    code = code.strip("\n")
    highlighted = highlight_python(code)
    rows = []
    for i, content in enumerate(highlighted, start=1):
        active = " active" if active_line == i else ""
        rows.append(
            f'<span class="code-line{active}" data-code-line="{i}">'
            f'<span class="ln">{i}</span>{content or "&nbsp;"}</span>'
        )
    return f'<div class="code-block">{"".join(rows)}</div>'


DIFF_CLASS = {"Easy": "badge-easy", "Medium": "badge-medium", "Hard": "badge-hard"}


def head(title: str, depth: int) -> str:
    prefix = "../" * depth
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{html.escape(title)}</title>
<link rel="stylesheet" href="{prefix}shared/style.css" />
</head>
<body>
"""


def topbar(depth: int) -> str:
    prefix = "../" * depth
    home = "index.html" if depth == 0 else f"{prefix}index.html"
    return f"""<div class="topbar">
  <a class="brand" href="{home}"><span class="brand-mark">&gt;_</span> Blind 75 Visualizer <span class="brand-sub">local · no login</span></a>
</div>
"""


def render_index() -> str:
    total = len(PROBLEMS)
    animated = sum(1 for p in PROBLEMS if p.get("js"))
    by_cat: dict[str, list[dict]] = {c["key"]: [] for c in CATEGORIES}
    for p in PROBLEMS:
        by_cat.setdefault(p["category"], []).append(p)

    nav = "".join(
        f'<a href="#{c["key"]}">{html.escape(c["label"])}</a>' for c in CATEGORIES
    )

    blocks = []
    for c in CATEGORIES:
        items = by_cat.get(c["key"], [])
        if not items:
            continue
        cards = []
        for p in items:
            viz = '<span class="viz-tag">Animated</span>' if p.get("js") else '<span class="static-tag">Walkthrough</span>'
            num = f'<span class="problem-number">#{p["number"]}</span>' if p.get("number") else ""
            cards.append(f"""<a class="problem-card" href="problems/{p['slug']}.html">
  <div class="problem-card-top">
    <span class="problem-title">{html.escape(p['title'])}</span>
    <span class="badge {DIFF_CLASS.get(p['difficulty'], '')}">{p['difficulty']}</span>
  </div>
  <div class="problem-card-top">{num}{viz}</div>
</a>""")
        blocks.append(f"""<section class="category-block" id="{c['key']}">
  <div class="category-heading">
    <h2>{html.escape(c['label'])}</h2>
    <span class="category-count">{len(items)} problems</span>
  </div>
  <div class="problem-grid">{''.join(cards)}</div>
</section>""")

    pct = round(100 * animated / total) if total else 0
    body = f"""{topbar(0)}
<div class="page">
  <div class="hub-header">
    <h1>Blind 75 — Code + Visualization</h1>
    <p>The optimal Python solution for each Blind 75 problem, paired with a step-by-step visualization where available. Everything on this page runs locally — nothing is fetched or deployed.</p>
    <div class="progress-strip">
      <span class="tabular">{animated} / {total} animated</span>
      <div class="progress-track"><div class="progress-fill" style="width:{pct}%"></div></div>
    </div>
  </div>
  <nav class="category-nav">{nav}</nav>
  {''.join(blocks)}
</div>
<footer class="site-footer">Personal study reference · built locally · {total} problems</footer>
</body>
</html>
"""
    return head("Blind 75 Visualizer", 0) + body


def render_viz_panel(problem: dict) -> str:
    inputs = problem["inputs"]
    fields_html = "".join(
        f'''<div class="input-field">
      <label for="field-{f['name']}">{html.escape(f['label'])}</label>
      <input type="text" id="field-{f['name']}" value="{html.escape(str(f['default']))}" />
    </div>'''
        for f in inputs
    )
    schema_json = json.dumps(inputs)
    return f"""<div class="panel" data-viz-root>
  <div class="panel-head"><span>Visualization</span><span class="step-counter" data-viz-counter></span></div>
  <div class="panel-body viz-stage">
    <div class="input-form">
      {fields_html}
      <button class="run-btn" data-viz-run>Visualize</button>
    </div>
    <div class="input-error" data-viz-error hidden></div>
    <div data-viz-rows></div>
    <div data-viz-map-block>
      <div class="row-label" data-viz-map-label></div>
      <div class="set-panel" data-viz-map></div>
    </div>
    <div class="narration" data-viz-narration></div>
    <div class="player-controls">
      <button data-viz-reset title="Reset">&#8676; Reset</button>
      <button data-viz-prev title="Previous step">&#8592; Prev</button>
      <button class="primary" data-viz-play title="Play / pause">Play</button>
      <button data-viz-next title="Next step">Next &#8594;</button>
      <span class="spacer"></span>
      <select class="speed-select" data-viz-speed title="Playback speed">
        <option value="1000">0.5x</option>
        <option value="700" selected>1x</option>
        <option value="350">2x</option>
      </select>
    </div>
  </div>
</div>
<script>
window.INPUT_SCHEMA = {schema_json};
{problem['js']}
</script>
<script src="../shared/viz.js"></script>
<script>window.initVizForm();</script>
"""


def render_static_panel(problem: dict) -> str:
    approach = "".join(f"<li>{html.escape(step)}</li>" for step in problem["approach"])
    example = problem.get("example", "")
    return f"""<div class="panel">
  <div class="panel-head"><span>Approach</span></div>
  <div class="panel-body viz-stage">
    {f'<div class="viz-example">{html.escape(example)}</div>' if example else ''}
    <ol class="approach-list">{approach}</ol>
    <div class="static-note">A full step-by-step animation for this problem is planned; for now this walkthrough plus the annotated code covers the approach.</div>
  </div>
</div>
"""


def render_problem(problem: dict) -> str:
    animated = bool(problem.get("js"))
    code_html = code_block_html(problem["code"])
    tags = "".join(f'<span class="tag-chip">{html.escape(t)}</span>' for t in problem.get("tags", []))
    num = f'LeetCode #{problem["number"]} · ' if problem.get("number") else ""

    code_panel = f"""<div class="panel">
  <div class="panel-head"><span>solution.py</span><span>{problem['time']} time · {problem['space']} space</span></div>
  {code_html}
  <div class="complexity-row">
    <span>Time <b>{problem['time']}</b></span>
    <span>Space <b>{problem['space']}</b></span>
  </div>
</div>"""

    viz_panel = render_viz_panel(problem) if animated else render_static_panel(problem)

    body = f"""{topbar(1)}
<div class="page">
  <div class="crumb"><a href="../index.html">Blind 75</a> / {html.escape(problem['category_label'])}</div>
  <div class="problem-header">
    <h1>{html.escape(problem['title'])}</h1>
    <div class="problem-meta">
      <span class="badge {DIFF_CLASS.get(problem['difficulty'], '')}">{problem['difficulty']}</span>
    </div>
  </div>
  <div class="problem-tags">{tags}</div>
  <p style="color:var(--text-dim); max-width:70ch; margin: -12px 0 22px;">{num}{html.escape(problem['summary'])}</p>
  <div class="split">
    {code_panel}
    {viz_panel}
  </div>
</div>
<footer class="site-footer"><a href="../index.html">&larr; back to all problems</a></footer>
</body>
</html>
"""
    return head(f"{problem['title']} · Blind 75 Visualizer", 1) + body


def main():
    cat_label = {c["key"]: c["label"] for c in CATEGORIES}
    for p in PROBLEMS:
        p["category_label"] = cat_label[p["category"]]

    (ROOT / "index.html").write_text(render_index(), encoding="utf-8")

    for p in PROBLEMS:
        out = OUT_PROBLEMS / f"{p['slug']}.html"
        out.write_text(render_problem(p), encoding="utf-8")

    print(f"Wrote index.html + {len(PROBLEMS)} problem pages to {ROOT}")


if __name__ == "__main__":
    main()
