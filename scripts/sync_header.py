"""Keep both mockup headers in sync with the shared Digilari navigation."""

from pathlib import Path
import re


repo = Path(__file__).resolve().parents[1]
source = repo.parent / "lead-generation"
template = (repo / "assets/dig-header.html").read_text().strip()
version = "20260924b"

pages = (
    (repo / "index.html", "./assets/dig-logo-c5.png", "./index.html", "./account-based-marketing/index.html", True, "./assets/"),
    (repo / "account-based-marketing/index.html", "./dig-logo-c5.png", "../index.html", "./index.html", False, "../assets/"),
    (source / "Lead Generation Services Brisbane _ Digilari Media.html", "./assets/dig-logo-c5.png", "./Lead%20Generation%20Services%20Brisbane%20_%20Digilari%20Media.html", "./account-based-marketing/index.html", True, "./assets/"),
    (source / "account-based-marketing/index.html", "./dig-logo-c5.png", "../Lead%20Generation%20Services%20Brisbane%20_%20Digilari%20Media.html", "./index.html", False, "../assets/"),
)

for path, logo, lead, abm, is_lead, assets in pages:
    html = path.read_text()
    header = template
    for key, value in {
        "LOGO_URL": logo,
        "LEAD_URL": lead,
        "ABM_URL": abm,
        "LEAD_CURRENT": ' aria-current="page"' if is_lead else "",
        "ABM_CURRENT": "" if is_lead else ' aria-current="page"',
    }.items():
        header = header.replace("{{" + key + "}}", value)

    start = html.index("<header", html.index("<body"))
    end = html.index("</header>", start) + len("</header>")
    html = html[:start] + header + "\n" + html[end:].lstrip("\n")
    css = f'<link rel="stylesheet" href="{assets}dig-shared.css?v={version}">'
    js = f'<script src="{assets}dig-shared.js?v={version}" defer></script>'
    html = re.sub(r'\s*<link rel="stylesheet" href="[^"]*dig-shared\.css\?v=[^"]+">', "", html)
    html = html.replace("</head>", "\n  " + css + "\n</head>", 1)
    html = re.sub(r'\s*<script src="[^"]*dig-shared\.js\?v=[^"]+" defer></script>', "", html)
    html = html.replace("</body>", "\n  " + js + "\n</body>", 1)
    if not is_lead:
        html = re.sub(r"styles\.css\?v=[^\"]+", f"styles.css?v={version}", html)
        html = re.sub(r"main\.js\?v=[^\"]+", f"main.js?v={version}", html)
    if is_lead:
        html = html.replace('href="https://digilari.com.au/lead-generation/#content"', 'href="#content"')
    path.write_text(html)

source_assets = source / "assets"
source_assets.mkdir(exist_ok=True)
for name in ("dig-shared.css", "dig-shared.js", "dig-logo-c5.png"):
    (source_assets / name).write_bytes((repo / "assets" / name).read_bytes())
for name in ("styles.css", "main.js"):
    (source / "account-based-marketing" / name).write_bytes(
        (repo / "account-based-marketing" / name).read_bytes()
    )
