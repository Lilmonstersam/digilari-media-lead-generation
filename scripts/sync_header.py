"""Apply the latest categorised SMM header to every page in this mockup."""
from pathlib import Path
import os
import re
import sys

REPO = Path(__file__).resolve().parents[1]
SMM = REPO / 'social-media-marketing'
sys.path.insert(0, str(SMM / 'scripts'))
from components import navigation

VERSION = '20261005smm'
PAGES = [REPO / 'index.html', REPO / 'account-based-marketing/index.html', SMM / 'index.html', *sorted(SMM.glob('*-agency/index.html'))]
LEGACY = SMM / 'Social Media Marketing Agency Brisbane _ SMM _ Digilari Media.html'
if LEGACY.exists():
    PAGES.append(LEGACY)

for page in PAGES:
    root_prefix = os.path.relpath(REPO, page.parent) + '/'
    social_prefix = os.path.relpath(SMM, page.parent) + '/'
    canonical = SMM / 'index.html' if page == LEGACY else page
    current_url = social_prefix + canonical.relative_to(SMM).as_posix() if canonical.is_relative_to(SMM) else root_prefix + canonical.relative_to(REPO).as_posix()
    header = navigation(social_prefix, mockup_root=root_prefix, current_url=current_url)
    source = page.read_text(encoding='utf-8')
    source, replacements = re.subn(r'<header\b[^>]*\bid="dig-header"[^>]*>.*?</header>', lambda match: header, source, count=1, flags=re.S)
    if replacements != 1:
        raise ValueError(f'Missing shared header in {page}')
    for extension, tag in (
        ('css', f'<link rel="stylesheet" href="{root_prefix}assets/dig-shared.css?v={VERSION}">'),
        ('js', f'<script src="{root_prefix}assets/dig-shared.js?v={VERSION}" defer></script>'),
    ):
        pattern = r'\s*<link\b[^>]*href="[^"]*dig-shared\.css(?:\?[^"]*)?"[^>]*>' if extension == 'css' else r'\s*<script\b[^>]*src="[^"]*dig-shared\.js(?:\?[^"]*)?"[^>]*>\s*</script>'
        source = re.sub(pattern, '', source)
        closing = '</head>' if extension == 'css' else '</body>'
        source = source.replace(closing, '\n  ' + tag + '\n' + closing, 1)
    if page == REPO / 'index.html':
        source = re.sub(r'\s*<link\b[^>]*href="[^"]*lead-page\.css(?:\?[^"]*)?"[^>]*>', '', source)
        source = source.replace('</head>', f'\n  <link rel="stylesheet" href="./assets/lead-page.css?v={VERSION}">\n</head>', 1)
    # Existing body and footer service links also stay within this mockup.
    service_routes = {
        'lead-generation': 'index.html',
        'account-based-marketing': 'account-based-marketing/index.html',
        'social-media-marketing-smm': 'social-media-marketing/index.html',
        'linkedin-advertising-agency': 'social-media-marketing/linkedin-advertising-agency/index.html',
        'instagram-ads-agency': 'social-media-marketing/instagram-ads-agency/index.html',
        'facebook-advertising-agency': 'social-media-marketing/facebook-advertising-agency/index.html',
    }
    for slug, route in service_routes.items():
        source = source.replace(f'href="https://digilari.com.au/{slug}/"', f'href="{root_prefix}{route}"')
    page.write_text(source, encoding='utf-8')
    print(page.relative_to(REPO))

(REPO / 'assets/dig-header.html').write_text(navigation('./social-media-marketing/', mockup_root='./', current_url='./index.html') + '\n', encoding='utf-8')
