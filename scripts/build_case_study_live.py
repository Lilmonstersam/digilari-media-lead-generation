"""Export the merged Duracube and Three Springs Farm case studies for the live site.

The live case studies are Elementor posts (post type case-study) that share one
layout. This script turns the mockup data in build_case_studies.py into the
content needed to extend those posts in place: the new subtitle, a Paid Social
tag, the facts panel, the extra challenge, a second solutions group, a second
results group, and an HTML block with the ads, timeline, table and links.

Output: live-export/case-study-updates.json
"""
import html
import importlib.util
import json
import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "live-export"
SITE = "https://digilari.com.au"

spec = importlib.util.spec_from_file_location("cs", ROOT / "scripts" / "build_case_studies.py")
cs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cs)

ICONS = {
    "video": "fas fa-video", "target": "fas fa-bullseye", "people": "fas fa-users",
    "layers": "fas fa-layer-group", "image": "fas fa-image", "calendar": "fas fa-calendar-alt",
    "search": "fas fa-search", "chart": "fas fa-chart-line", "shield": "fas fa-shield-alt", "pin": "fas fa-map-marker-alt",
}
LINKS = {
    "../../social-media-marketing/linkedin-advertising-agency/index.html": SITE + "/social-media-marketing-smm/linkedin-advertising-agency/",
    "../../social-media-marketing/instagram-ads-agency/index.html": SITE + "/social-media-marketing-smm/instagram-ads-agency/",
}
# Live post element ids (same layout on both posts)
POSTS = {
    "duracube": {"post": 22606, "subtitle": "7db8ad4", "last_tag": "408126d2", "about": "13cdbb27", "logo": "5739a2c8",
                 "challenge": "7c06ab11", "sol_intro": "7cac88bd", "sol_first": "405596be", "sol_last": "1fd2e7e9",
                 "results": "3df020f9", "results_heading": "52a25feb"},
    "three-springs-farm": {"post": 22662, "subtitle": "75647100", "last_tag": "74484699", "about": "70b632c9", "logo": "48ebc179",
                           "challenge": "3aa7d62c", "sol_intro": "65099bd7", "sol_first": "273d5d07", "sol_last": "5f5d4016",
                           "results": "59d4b034", "results_heading": "5513a219"},
}

CSS = """
/* ---- merged case study additions ---- */
.dcs{--pink:#e41b6f;--pink-dark:#b5124f;--ink:#211b29;--line:#eadfe4;--cream:#fbf8f5;color:var(--ink);font-family:'Red Hat Text',sans-serif}
.dcs-facts{margin:22px 0 0;padding:22px 24px;border:1px solid var(--line);border-radius:18px;background:var(--cream)}
.dcs-facts div{padding:10px 0;border-bottom:1px solid var(--line)}
.dcs-facts div:first-child{padding-top:0}
.dcs-facts div:last-child{padding-bottom:0;border:0}
.dcs-facts dt{color:var(--pink-dark);font:800 11px/1.3 'Red Hat Display',sans-serif;letter-spacing:.1em;text-transform:uppercase}
.dcs-facts dd{margin:3px 0 0;font:700 16px/1.35 'Red Hat Display',sans-serif;color:var(--ink)}
.dcs-pill{display:block;width:max-content;margin:28px auto 6px;padding:7px 16px;border-radius:99px;background:#fff;color:var(--pink-dark);font:800 13px/1.2 'Red Hat Display',sans-serif;letter-spacing:.08em;text-transform:uppercase;box-shadow:0 0 0 1px var(--line)}
.dcs-wrap{max-width:1140px;margin:0 auto;padding:0 20px 70px}
.dcs h3{margin:0 0 22px;font:800 22px/1.2 'Red Hat Display',sans-serif;color:var(--ink)}
.dcs-block{margin-top:56px}
.dcs-block:first-child{margin-top:0}
.dcs-ads{display:grid;gap:28px;align-items:start}
.dcs-ads-2{grid-template-columns:repeat(2,minmax(0,300px))}
.dcs-ads-3{grid-template-columns:repeat(3,minmax(0,1fr))}
.dcs-ad{margin:0;display:flex;flex-direction:column;align-items:center;gap:12px}
.dcs-ad img{display:block;width:100%;height:auto;border:1px solid var(--line);border-radius:14px;background:#fff;box-shadow:0 18px 40px rgba(33,27,41,.12)}
.dcs-ad figcaption{max-width:340px;color:#6f6470;font-size:13px;line-height:1.5;text-align:center}
.dcs-timeline{margin:0;padding:0;list-style:none;border-left:2px solid #f3c9da}
.dcs-timeline li{position:relative;display:grid;grid-template-columns:110px 1fr;gap:16px;margin:0;padding:0 0 18px 24px;color:#4b4550;font-size:15px;line-height:1.6}
.dcs-timeline li::before{content:"";position:absolute;left:-7px;top:6px;width:12px;height:12px;border-radius:50%;background:var(--pink)}
.dcs-timeline li strong{color:var(--pink-dark);font:800 14px/1.6 'Red Hat Display',sans-serif}
.dcs-table{overflow-x:auto;border:1px solid var(--line);border-radius:14px}
.dcs-table table{width:100%;min-width:560px;margin:0;border:0;border-collapse:collapse;font-size:15px}
.dcs-table th,.dcs-table td{padding:13px 18px;text-align:left;border:0;border-bottom:1px solid var(--line);background:none}
.dcs-table tr:last-child>*{border-bottom:0}
.dcs-table thead th{background:var(--cream);color:var(--pink-dark);font:800 12px/1.3 'Red Hat Display',sans-serif;letter-spacing:.06em;text-transform:uppercase}
.dcs-table tbody th{font-weight:700;color:var(--ink)}
.dcs-table td{color:#4b4550;font-variant-numeric:tabular-nums}
.dcs-table td:last-child{color:var(--ink);font-weight:800}
.dcs-source{margin:18px 0 0;color:#7b6f78;font-size:13px;line-height:1.6}
.dcs-actions{display:flex;flex-wrap:wrap;align-items:center;gap:20px 24px;margin-top:48px}
.dcs-btn{display:inline-flex;align-items:center;gap:14px;min-height:52px;padding:14px 26px;border-radius:999px;background:var(--pink);color:#fff!important;text-decoration:none;font:800 15px/1.25 'Red Hat Display',sans-serif;border:2px solid var(--pink);transition:background .2s}
.dcs-btn:hover{background:var(--pink-dark);border-color:var(--pink-dark)}
.dcs-btn-outline{background:#fff;color:var(--pink-dark)!important}
.dcs-btn-outline:hover{background:#fbf0f5}
.dcs-link{color:var(--pink-dark)!important;font:800 15px/1.3 'Red Hat Display',sans-serif;text-decoration:none;border-bottom:2px solid currentColor;padding-bottom:3px}
@media(max-width:1000px){.dcs-ads-3{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:640px){.dcs-ads-2,.dcs-ads-3{grid-template-columns:1fr;max-width:360px;margin-inline:auto}.dcs-timeline li{grid-template-columns:1fr;gap:2px}}
"""


def esc(s):
    return html.escape(s, quote=False)


def counter(value):
    m = re.match(r"^([+−-]?)([\d.,]+)(.*)$", value)
    prefix, number, suffix = m.groups()
    return {"prefix": prefix, "ending_number": number.replace(",", ""), "suffix": suffix}


def sentences(text):
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z])", text.strip())
    return "<ul>" + "".join(f"<li>{esc(p)}</li>" for p in parts) + "</ul>"


def build(case):
    slug = case["slug"]
    ids = POSTS[slug]
    groups = case["solution_groups"]
    second = groups[1]
    results = case["result_groups"][1]

    blocks = []
    ads = results.get("ads") or []
    if ads:
        def size(src):
            w, h = Image.open(ROOT / "case-studies" / "images" / "ads" / Path(src).name).size
            return f'width="{w}" height="{h}"'

        figs = "".join(
            f'<figure class="dcs-ad"><img src="{{{{AD:{Path(src).name}}}}}" alt="{html.escape(alt)}" loading="lazy" {size(src)}><figcaption>{esc(cap)}</figcaption></figure>'
            for src, alt, cap in ads)
        blocks.append(f'<div class="dcs-block"><h3>The ads behind the results</h3><div class="dcs-ads dcs-ads-{len(ads)}">{figs}</div></div>')
    if results.get("timeline"):
        items = "".join(f"<li><strong>{esc(d)}</strong><span>{esc(t)}</span></li>" for d, t in results["timeline"])
        blocks.append(f'<div class="dcs-block"><h3>What changed and when</h3><ol class="dcs-timeline">{items}</ol></div>')
    if results.get("table"):
        head, rows = results["table"]
        thead = "".join(f'<th scope="col">{esc(h)}</th>' for h in head)
        tbody = "".join("<tr>" + f'<th scope="row">{esc(r[0])}</th>' + "".join(f"<td>{esc(c)}</td>" for c in r[1:]) + "</tr>" for r in rows)
        blocks.append(f'<div class="dcs-block"><h3>Before and after</h3><div class="dcs-table"><table><thead><tr>{thead}</tr></thead><tbody>{tbody}</tbody></table></div><p class="dcs-source">{esc(results["source"])}</p></div>')
    actions = []
    for i, (label, url) in enumerate(case["services"]):
        url = LINKS.get(url, url)
        cls = "dcs-btn" if i == 0 else "dcs-btn dcs-btn-outline"
        actions.append(f'<a class="{cls}" href="{url}">Explore {esc(label)} <span aria-hidden="true">↗</span></a>')
    actions.append(f'<a class="dcs-link" href="{SITE}/case-studies/">All case studies <span aria-hidden="true">↗</span></a>')
    blocks.append('<div class="dcs-actions">' + "".join(actions) + "</div>")

    facts = "".join(f"<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>" for k, v in case["facts"])
    challenge = "<ol>" + "".join(
        f'<li><span style="font-weight: bold;">{esc(t)}</span>: {esc(d)}</li>' for t, d in case["challenge"]) + "</ol>"
    res_items = "<ol>" + "".join(
        f'<li><span style="font-weight: bold;">{esc(t)}:</span><ul><li>{esc(d[0].upper() + d[1:])}</li></ul></li>' for t, d in results["items"]) + "</ol>"

    return {
        **ids,
        "slug": slug,
        "subtitle_text": case["subtitle"],
        "tag": {"text": "Paid Social", "url": SITE + "/social-media-marketing-smm/"},
        "about_text": esc(case["about"]),
        "facts_html": f'<div class="dcs"><dl class="dcs-facts">{facts}</dl></div>',
        "challenge_html": challenge,
        "sol1_label": groups[0][0],
        "sol2": {
            "label": second[0], "intro": f"<p>{esc(second[1])}</p>",
            "boxes": [{"icon": ICONS[i], "title": t, "description": sentences(d)} for i, t, d in second[2]],
        },
        "results1_eyebrow": case["result_groups"][0]["eyebrow"],
        "results2": {"eyebrow": results["eyebrow"], "title": results["title"], "editor": res_items,
                     "counters": [{**counter(v), "label": lab, "sub": sub} for v, lab, sub in results["counters"]]},
        "extra_html": '<div class="dcs"><div class="dcs-wrap">' + "".join(blocks) + "</div></div>",
        "ads": [Path(src).name for src, _, _ in ads],
    }


def main():
    cases = {c["slug"]: c for c in cs.CASES}
    data = {"css": CSS.strip(), "cases": [build(cases[s]) for s in POSTS]}
    OUT.mkdir(exist_ok=True)
    (OUT / "case-study-updates.json").write_text(json.dumps(data, ensure_ascii=False, indent=1))
    for c in data["cases"]:
        print(c["slug"], len(c["extra_html"]), c["ads"], [x["prefix"] + x["ending_number"] + x["suffix"] for x in c["results2"]["counters"]])


if __name__ == "__main__":
    main()
