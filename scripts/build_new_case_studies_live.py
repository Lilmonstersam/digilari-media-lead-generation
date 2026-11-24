"""Export the four new case studies (mockup data) for the live site.

Each live case study is an Elementor post of type case-study. The new posts
reuse the published Duracube layout as a template; this script provides the
content that replaces Duracube's text, plus the images to upload.

Output: live-export/new-case-studies.json and live-export/images/<slug>-*.png
(the hero monitor and, for organic campaigns, the phone illustration, rendered
from the mockup).
"""
import html
import importlib.util
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "live-export"
SITE = "https://digilari.com.au"
SHOTS = Path("/tmp/claude-0/-home-claude/e976a4c0-1759-54cc-80b5-c3f88c079375/scratchpad/shots")

spec = importlib.util.spec_from_file_location("cs", ROOT / "scripts" / "build_case_studies.py")
cs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cs)
spec2 = importlib.util.spec_from_file_location("live", ROOT / "scripts" / "build_case_study_live.py")
live = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(live)

SLUGS = {
    "streamline-carports-facebook-ads": "streamline-carports",
    "cv-sheds-meta-ads": "cv-sheds",
    "cummins-social-media": "cummins",
    "cosmetics-plus-social-media": "cosmetics-plus",
}
CATEGORIES = {"paid-ads": 176, "social-media": 178, "seo": 175, "cro": 177}
ICONS = {**live.ICONS, "refresh": "fas fa-sync-alt", "chat": "fas fa-comments"}
SERVICE_URLS = {
    "../../social-media-marketing/facebook-advertising-agency/index.html": SITE + "/social-media-marketing-smm/facebook-advertising-agency/",
    "../../social-media-marketing/index.html": SITE + "/social-media-marketing-smm/",
}
TAG_URLS = {"Paid Social": SITE + "/social-media-marketing-smm/", "Social Media": SITE + "/social-media-marketing-smm/"}

esc = live.esc


def build(case):
    slug = SLUGS[case["slug"]]
    blocks = []
    if case.get("results_note"):
        blocks.append(f'<div class="dcs-block"><p class="dcs-note">{esc(case["results_note"])}</p></div>')
    if case.get("table"):
        head, rows = case["table"]
        thead = "".join(f'<th scope="col">{esc(h)}</th>' for h in head)
        tbody = "".join("<tr>" + f'<th scope="row">{esc(r[0])}</th>' + "".join(f"<td>{esc(c)}</td>" for c in r[1:]) + "</tr>" for r in rows)
        blocks.append(f'<div class="dcs-block"><h3>Before and after</h3><div class="dcs-table"><table><thead><tr>{thead}</tr></thead><tbody>{tbody}</tbody></table></div><p class="dcs-source">{esc(case["source"])}</p></div>')
    else:
        blocks.append(f'<div class="dcs-block"><p class="dcs-source">{esc(case["source"])}</p></div>')
    label, url = case["service"]
    blocks.append('<div class="dcs-actions">'
                  f'<a class="dcs-btn" href="{SERVICE_URLS[url]}">Explore {esc(label)} <span aria-hidden="true">↗</span></a>'
                  f'<a class="dcs-link" href="{SITE}/case-studies/">All case studies <span aria-hidden="true">↗</span></a></div>')

    facts = "".join(f"<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>" for k, v in case["facts"])
    ad = case.get("challenge_ad")
    images = {"hero": f"{slug}-hero.png"}
    src_hero = SHOTS / f'v-{case["slug"]}-hero.png'
    (OUT / "images").mkdir(parents=True, exist_ok=True)
    shutil.copy(src_hero, OUT / "images" / images["hero"])
    if ad:
        images["challenge"] = Path(ad[0]).name  # real ad screenshot, uploaded as cs-<name>
        challenge_caption = ad[2]
    else:
        images["challenge"] = f"{slug}-post.png"
        shutil.copy(SHOTS / f'v-{case["slug"]}-challenge.png', OUT / "images" / images["challenge"])
        challenge_caption = "Illustration based on the campaign messaging"

    stats = case["stats"]
    return {
        "mockup_slug": case["slug"], "slug": slug, "title": case["name"],
        "categories": [CATEGORIES[c] for c in case["categories"]],
        "excerpt": case["excerpt"], "description": case["description"],
        "subtitle": case["subtitle"],
        "tag": {"text": case["tag"], "url": TAG_URLS[case["tag"]]},
        "about_heading": f'About {case["name"]}',
        "about": esc(case["about"]),
        "facts_html": f'<div class="dcs"><dl class="dcs-facts">{facts}</dl></div>',
        "challenge_html": "".join(f"<p>{esc(p)}</p>" for p in case["challenge"]),
        "challenge_caption": challenge_caption,
        "solutions_intro": f'<p>{esc(case["solutions_intro"])}</p>',
        "boxes": [{"icon": ICONS[i], "title": t, "description": live.sentences(d)} for i, t, d in case["solutions"]],
        "results": {"eyebrow": "Results", "title": case["results_title"],
                    "editor": "<ol>" + "".join(f'<li><span style="font-weight: bold;">{esc(t)}:</span><ul><li>{esc(d[0].upper() + d[1:])}</li></ul></li>' for t, d in case["results"]) + "</ol>",
                    "counters": [{**live.counter(v), "label": lab, "sub": sub} for v, lab, sub in case["counters"]]},
        "card": [{"value": v, "label": lab, "note": sub} for v, lab, sub in stats],
        "extra_html": '<div class="dcs"><div class="dcs-wrap">' + "".join(blocks) + "</div></div>",
        "images": images,
    }


def main():
    cases = {c["slug"]: c for c in cs.CASES}
    data = {"css_extra": ".dcs-note{margin:0;padding:18px 22px;border-left:4px solid var(--pink);background:var(--cream);border-radius:0 14px 14px 0;color:#4b4550;font-size:15px;line-height:1.6}",
            "cases": [build(cases[s]) for s in SLUGS]}
    (OUT / "new-case-studies.json").write_text(json.dumps(data, ensure_ascii=False, indent=1))
    for c in data["cases"]:
        print(c["slug"], len(c["boxes"]), [x["prefix"] + x["ending_number"] + x["suffix"] for x in c["results"]["counters"]], c["images"])


if __name__ == "__main__":
    main()
