"""Refresh shared components in the social hub and its legacy entry point."""
from pathlib import Path
from lxml import html
from components import navigation, enquiry_form

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / 'index.html'
document = html.parse(str(source))
header = document.xpath('//header[@id="dig-header"]')[0]
header.getparent().replace(header, html.fromstring(navigation(mockup_root="../")))
hero = document.xpath('//section[contains(concat(" ",normalize-space(@class)," ")," hero ")]')[0]
old = hero.xpath('.//*[@id="enquiry"] | .//div[contains(concat(" ",normalize-space(@class)," ")," hero-art ")]')[0]
old.getparent().replace(old, html.fromstring(enquiry_form()))
for item in document.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," platform-list ")]/div[h3]'):
    if item.findtext('h3') not in {'LinkedIn', 'Instagram', 'Facebook'}:
        item.getparent().remove(item)
for link in document.xpath('//main//a[@href="https://digilari.com.au/contact-us/"] | //div[@class="mobile-action"]/a[@href="https://digilari.com.au/contact-us/"]'):
    link.set('href', '#enquiry')
# Restrict the channel recommendation to the services offered in this mockup.
for paragraph in document.xpath('//details[summary="Which social platforms should my business use?"]/p'):
    paragraph.text = 'That depends on who you need to reach and what you want them to do. We review your audience, resources and goals before recommending the right mix of LinkedIn, Instagram and Facebook.'
output = html.tostring(document, encoding='unicode', doctype='<!doctype html>')
source.write_text(output, encoding='utf-8')
(ROOT / 'Social Media Marketing Agency Brisbane _ SMM _ Digilari Media.html').write_text(output, encoding='utf-8')
print('Updated the social hub and legacy entry point')
