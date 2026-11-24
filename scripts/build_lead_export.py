"""Export the lead generation mockup (index.html) as an Elementor update plan.

The mockup is the live page (post 18955) with edits, so the plan edits the
existing Elementor elements in place and inserts the new dlg-* sections as
HTML widgets. Output:
  live-export/lead-generation-plan.json
  live-export/lead-generation-page.css
"""
import json
import re
from pathlib import Path

import tinycss2
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "index.html"
OUT = ROOT / "live-export"
SITE = "https://digilari.com.au"

LINKS = {
    "./account-based-marketing/index.html": "#audit",  # ABM page not live yet
    "./case-studies/index.html": SITE + "/case-studies/",
}
CASE_LINKS = {
    "Scholz Electrical": SITE + "/case-studies/scholz-electrical/",
    "Duracube": SITE + "/case-studies/duracube/",
}
IMAGES = {
    "./assets/Scholz-Electrical-1.png": SITE + "/wp-content/uploads/2022/06/Scholz-Electrical-1.png",
}

SECTION_IDS = {
    "a78859f": "leads", "84e8f11": "services", "433f63d": "process",
    "e4c1c89": "results", "9d3aba6": "why", "22fbe96": "faq",
}
FORMS = {"5b2ae8a": "audit", "af0f577": "audit-2"}
DELETE = ["2c7d4b6", "804be43", "5e1f331"]


def inner(el):
    return el.decode_contents().strip() if el else ""


def text(el):
    return re.sub(r"\s+", " ", el.get_text(" ", strip=True)) if el else ""


def fix_links(html):
    for old, new in {**LINKS, **IMAGES}.items():
        html = html.replace(f'"{old}"', f'"{new}"')
    # logos are uploaded to the media library at build time
    html = re.sub(r'"\./assets/logos/([^"]+?)\.svg"', r'"./assets/logos/\1.png"', html)  # WordPress blocks SVG uploads
    html = re.sub(r'"\./assets/logos/([^"]+)"', r'"{{LOGO:\1}}"', html)
    return html


def widget_settings(el):
    wtype = el["data-widget_type"].split(".")[0]
    box = el.find(class_="elementor-widget-container")
    if wtype == "heading":
        return {"title": inner(box.find(class_="elementor-heading-title"))}
    if wtype == "text-editor":
        return {"editor": fix_links(inner(box))}
    if wtype == "iheading":
        return {"title": inner(box.find(class_="main-heading"))}
    if wtype == "iservice_box":
        return {
            "title": text(box.find(class_="service-box-title")),
            "des": fix_links(inner(box.find(class_="content-box").find("p"))),
            "number_box": text(box.find(class_="number-box")),
        }
    if wtype == "iprocessbox":
        return {
            "title": text(box.find(class_="process-box-title")),
            "des": inner(box.find(class_="content-box").find("p")),
        }
    if wtype == "icon-box":
        s = {"title_text": text(box.find(class_="elementor-icon-box-title"))}
        d = box.find(class_="elementor-icon-box-description")
        if d:
            s["description_text"] = inner(d)
        a = box.find(class_="elementor-icon-box-title").find("a")
        if a:
            s["link"] = {"url": fix_links(f'"{a["href"]}"').strip('"'), "is_external": "", "nofollow": "", "custom_attributes": ""}
        return s
    if wtype == "iaccordions":
        items = []
        for item in box.select(".acc-item"):
            toggle = item.find(class_="acc-toggle")
            for i in toggle.find_all("i"):
                i.decompose()
            items.append({"acc_title": text(toggle), "acc_content": fix_links(inner(item.find(class_="acc-content")))})
        return {"ot_accs": items}
    if wtype == "html":
        h2 = box.find("h2")
        intro = h2.find_next_sibling("p")
        button = box.select_one("button[type=submit]")
        note = box.find(class_="dlg-form-note")
        return {"_form": {"heading": text(h2), "intro": text(intro), "button": text(button), "note": text(note)}}
    raise ValueError(f"Unhandled widget {wtype}")


def css_bundle(soup_text):
    parts = [(ROOT / "assets" / "lead-page.css").read_text()]
    parts += [m.group(1) for m in re.finditer(r"<style[^>]*>(.*?)</style>", soup_text, re.S) if "dlg-" in m.group(1)]
    drop = re.compile(r"elementor-17569|header\.elementor-location-header|#rcr-wrapper|glasp")
    out = []
    for part in parts:
        for rule in tinycss2.parse_stylesheet(part, skip_comments=True, skip_whitespace=True):
            if rule.type == "qualified-rule":
                if not drop.search(tinycss2.serialize(rule.prelude)):
                    out.append(tinycss2.serialize([rule]))
            elif rule.type == "at-rule" and rule.content is not None and rule.lower_at_keyword == "media":
                kept = [r for r in tinycss2.parse_rule_list(rule.content, True, True)
                        if r.type == "qualified-rule" and not drop.search(tinycss2.serialize(r.prelude))]
                if kept:
                    out.append("@media" + tinycss2.serialize(rule.prelude) + "{" + "".join(tinycss2.serialize([r]) for r in kept) + "}")
            elif rule.type == "at-rule":
                out.append(tinycss2.serialize([rule]))
    css = "\n".join(out)
    # the live theme renders the page header without the mockup's helper class
    css = css.replace("body.elementor-page-18955 .page-header.dlg-compact-header", ".page-header.dlg-compact-header")
    css = css.replace(".page-header.dlg-compact-header", "body.elementor-page-18955 .page-header")
    # The page nav is sticky through its Elementor container (see live-export/README.md)
    css += """
/* ---- live site integration ---- */
html:has(.dlg-sticky),body:has(.dlg-sticky){overflow-x:clip;overflow-y:visible}
.dlg-sticky{position:sticky!important;top:100px;z-index:500}
.admin-bar .dlg-sticky{top:132px}
@media(max-width:1024px){.dlg-sticky,.admin-bar .dlg-sticky{top:80px}}
.dlg-sticky .dlg-subnav{position:static!important;top:auto!important}
.dlg-section-wrap{padding:0!important}
body.elementor-page-18955 .dlg-results-panel .dlg-case2-logo img{max-height:56px;width:auto}
"""
    return css


def main():
    raw = SRC.read_text()
    soup = BeautifulSoup(raw, "html.parser")
    page = soup.find(attrs={"data-elementor-id": "18955"})

    settings, new_widgets = {}, []
    changed = ["4bd13d5", "c7fe01a", "5b2ae8a", "46c8638", "7e7f5af", "9c818ab", "c53542f", "930cb53",
               "6db38a7d", "690daa33", "43dad173", "4b323fc3", "660ee6b0", "be7739c", "7d96204", "83973c0",
               "b81826d", "f1698b1", "72ddc64", "7377c67", "ee29db0", "af0f577", "7df0905", "32ad2633",
               "bf900cd", "1aa711c7", "6af1fb01", "78269d68", "6def9d45"]
    for wid in changed:
        el = page.find(attrs={"data-id": wid})
        settings[wid] = widget_settings(el)
    for wid, anchor in SECTION_IDS.items():
        settings.setdefault(wid, {})["_element_id"] = anchor
    for wid, anchor in FORMS.items():
        settings[wid].update({"_element_id": anchor, "_css_classes": "custom-form-wrapper dlg-anchor"})
    settings["6af1fb01"]["selected_icon"] = {"value": "fas fa-bullseye", "library": "fa-solid"}
    for wid in ["dlgsvc3", "dlgsvc4", "dlgsvc5"]:
        el = page.find(attrs={"data-id": wid})
        new_widgets.append({"parent": "1072d9d7", "clone": "43dad173", "settings": widget_settings(el)})

    # Top-level order: existing container ids, or new HTML sections
    order = []
    script = next(m.group(1) for m in re.finditer(r"<script[^>]*>(.*?)</script>", raw, re.S) if "dlg-subnav" in m.group(1))
    script = script.replace(
        """    var header = document.querySelector('#dig-header');
    if (!header) return 0;
    var r = header.getBoundingClientRect();
    return r.top <= 1 && r.bottom > 0 ? Math.round(r.bottom) : 0;""",
        """    var wrap = nav.closest('.dlg-sticky');
    return wrap ? (parseFloat(getComputedStyle(wrap).top) || 0) : 0;""",
    ).replace("function setTop(){ nav.style.top = headerBottom() + 'px'; }", "function setTop(){}")
    schema = next(m.group(0) for m in re.finditer(r'<script type="application/ld\+json">.*?</script>', raw, re.S) if '"Service"' in m.group(0))
    for child in page.find_all(recursive=False):
        if child.get("data-id"):
            order.append(child["data-id"])
            continue
        cls = child.get("class", [])
        html = fix_links(str(child))
        block = {"html": html, "sticky": "dlg-subnav" in cls}
        if "dlg-mobile-bar" in cls:
            block["html"] = html + schema + "<script>" + script + "</script>"
        order.append(block)

    results = page.find(attrs={"data-id": "64dee34"}).find(class_="dlg-results-panel")
    for art in results.find_all("article"):
        name = text(art.find("h3"))
        link = art.find(class_="dlg-case2-link")
        if name in CASE_LINKS:
            link["href"] = CASE_LINKS[name]
    inner_inserts = [
        {"parent": "64dee34", "after": "72ddc64", "html": fix_links(str(results))},
        {"parent": "22fbe96", "at": 0, "html": str(page.find(attrs={"data-id": "22fbe96"}).find(class_="dlg-wrap", recursive=False))},
    ]

    plan = {"settings": settings, "new_widgets": new_widgets, "order": order,
            "inner_inserts": inner_inserts, "delete": DELETE,
            "logos": []}
    plan["logos"] = sorted(set(re.findall(r"\{\{LOGO:([^}]+)\}\}", json.dumps(plan))))
    OUT.mkdir(exist_ok=True)
    (OUT / "lead-generation-plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=1))
    (OUT / "lead-generation-page.css").write_text(css_bundle(raw))
    print(len(order), "top-level blocks;", len(settings), "settings;", plan["logos"])


if __name__ == "__main__":
    main()
