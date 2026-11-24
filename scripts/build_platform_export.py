"""Export a social media platform mockup page for the live Elementor build.

Usage: python3 scripts/build_platform_export.py facebook-advertising-agency facebook

Output in live-export/:
  <slug>-blocks.json  one HTML block per page section, plus the page-nav script
  <slug>-page.css     live SMM page CSS + platform.css scoped under .dsmm
"""
import json
import re
import sys
from pathlib import Path

import tinycss2
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
SMM = ROOT / "social-media-marketing"
OUT = ROOT / "live-export"
SITE = "https://digilari.com.au"
HUB = SITE + "/social-media-marketing-smm/"
CF7 = '[contact-form-7 id="3128" html_class="dsmm-cf7"]'

LINKS = {
    "../index.html": HUB,
    "../linkedin-advertising-agency/index.html": HUB + "linkedin-advertising-agency/",
    "../instagram-ads-agency/index.html": HUB + "instagram-ads-agency/",
    "../facebook-advertising-agency/index.html": HUB + "facebook-advertising-agency/",
    "../../case-studies/three-springs-farm/index.html": SITE + "/case-studies/three-springs-farm/",
    "../../case-studies/duracube/index.html": SITE + "/case-studies/duracube/",
}


def scope_selector(sel):
    sel = sel.strip()
    if sel.startswith(".platform-page"):
        return ".dsmm" + sel
    if sel in (":root", "html", "body"):
        return ".dsmm"
    return ".dsmm " + sel


def scope_rules(rules):
    out = []
    for rule in rules:
        if rule.type == "qualified-rule":
            sels = ",".join(scope_selector(s) for s in tinycss2.serialize(rule.prelude).split(","))
            out.append(sels + "{" + tinycss2.serialize(rule.content).strip() + "}")
        elif rule.type == "at-rule" and rule.content is not None:
            inner = tinycss2.parse_rule_list(rule.content, skip_comments=True, skip_whitespace=True)
            out.append("@" + rule.at_keyword + tinycss2.serialize(rule.prelude).rstrip() + "{" + "".join(scope_rules(inner)) + "}")
    return out


def main(slug, platform):
    soup = BeautifulSoup((SMM / slug / "index.html").read_text(), "html.parser")
    main_el = soup.find("main")

    # Live enquiry form replaces the mockup's mailto preview form
    form = main_el.find("form", attrs={"data-enquiry-form": True})
    topic = form["data-topic"]
    form.replace_with(BeautifulSoup(CF7, "html.parser"))
    intro = main_el.find(class_="enquiry-intro")
    intro.string = f"Share your details and we’ll be in touch to discuss the right {topic[0].upper() + topic[1:]} approach for your business."

    # Case studies without a live page yet: offer a conversation instead
    for link in main_el.select("a.case-link"):
        href = link.get("href", "")
        if "case-studies/" in href and href not in LINKS and not href.startswith("http"):
            link["href"] = "#enquiry"
            link.string = "Discuss a similar campaign ↗"

    blocks = []
    for child in main_el.find_all(recursive=False):
        html = str(child)
        for old, new in LINKS.items():
            html = html.replace(f'href="{old}"', f'href="{new}"')
        assert 'href="../' not in html and 'src="../' not in html, html[:200]
        blocks.append(html)

    smm_blocks = json.loads((OUT / "smm-page-blocks.json").read_text())
    css = (OUT / "smm-page.css").read_text()
    platform_rules = tinycss2.parse_stylesheet((SMM / "platform.css").read_text(), skip_comments=True, skip_whitespace=True)
    css += "\n/* ---- platform page styles (platform.css) ---- */\n" + "\n".join(scope_rules(platform_rules)) + "\n"

    meta = soup.find("meta", attrs={"name": "description"})
    data = {
        "title": soup.title.string.split("|")[0].strip(),
        "seo_title": soup.title.string,
        "description": meta["content"] if meta else "",
        "wrapper": f'<div class="dsmm platform-page" data-platform="{platform}">',
        "blocks": blocks,
        "script": smm_blocks["script"],
    }
    (OUT / f"{slug}-blocks.json").write_text(json.dumps(data, ensure_ascii=False, indent=1))
    (OUT / f"{slug}-page.css").write_text(css)
    print(slug, len(blocks), "blocks;", len(css), "bytes CSS")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
