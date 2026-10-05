"""Shared static navigation and enquiry form components."""

from html import escape

DOWN = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="m3 6 5 5 5-5"/></svg>'
RIGHT = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="m6 3 5 5-5 5"/></svg>'


def navigation(prefix="./", current="", mockup_root=None, current_url=None):
    live = "https://digilari.com.au/"
    lead = "../lead-generation/" if prefix == "./" else "../../lead-generation/"
    if mockup_root is not None:
        lead = mockup_root
    home = mockup_root + "index.html" if mockup_root is not None else live
    logo = (mockup_root if mockup_root is not None else prefix) + "assets/dig-logo-c5.png"
    social = prefix + "index.html"
    active = current_url or prefix + (current + "/" if current else "") + "index.html"

    def links(items):
        output = []
        for label, url in items:
            current_attr = ' aria-current="page"' if url == active else ''
            output.append(f'<a href="{escape(url, quote=True)}"{current_attr}>{escape(label)}</a>')
        return "\n".join(output)

    def layered(key, categories):
        sections = []
        for index, (label, items) in enumerate(categories):
            panel = f"dig-{key}-panel-{index}"
            sections.append(
                f'<div class="dig-menu-category{ " is-active" if index == 0 else ""}">'
                f'<button class="dig-category-toggle" type="button" aria-controls="{panel}" '
                f'aria-expanded="{str(index == 0).lower()}">{escape(label)}{RIGHT}</button>'
                f'<div class="dig-menu-panel" id="{panel}"{ " hidden" if index else ""}>'
                f'<p class="dig-menu-panel-title">{escape(label)}</p>{links(items)}</div></div>'
            )
        return f'<div class="dig-submenu dig-layered-menu" id="dig-menu-{key}">{"".join(sections)}</div>'

    def group(label, key, content, url=None):
        if url:
            top = f'<a href="{url}">{label}</a><button class="dig-submenu-toggle" type="button" aria-label="Open {label} submenu" aria-controls="dig-menu-{key}" aria-expanded="false">{DOWN}</button>'
        else:
            top = f'<button class="dig-submenu-toggle dig-nav-label" type="button" aria-controls="dig-menu-{key}" aria-expanded="false">{label}{DOWN}</button>'
        return f'<div class="dig-nav-group"><div class="dig-nav-top">{top}</div>{content}</div>'

    why = layered("why", [
        ("About & team", [("Why Digilari", live + "why-digilari/"), ("Meet the team", live + "why-digilari/#meet-the-team")]),
        ("Partnerships & guarantees", [("Digital Results Guarantee (DRG)", live + "digital-results-guarantee-performance-marketing/"), ("Digital Partner Program (DPP)", live + "articles/digital-marketing-partner-program/")]),
        ("Industry sectors", [("All sectors", live + "core-industry-sector-digital-marketing/"), *[(name + " Marketing Agency", live + slug + "-marketing-agency/") for name, slug in [("Agricultural", "agricultural"), ("Construction", "construction"), ("Mining", "mining"), ("Manufacturing", "manufacturing"), ("Logistics", "logistics")]]]),
    ])
    capabilities = layered("capabilities", [
        ("Growth & conversion", [("Lead Generation", lead + "index.html"), ("Account-Based Marketing (ABM)", lead + "account-based-marketing/index.html"), ("ROI Marketing", live + "roi-marketing-services/"), ("Conversion Rate Optimisation", live + "conversion-rate-optimisation/")]),
        ("Search & visibility", [("Generative Engine Optimisation (GEO)", live + "generative-engine-optimisation-geo-services/"), ("Search Engine Optimisation (SEO)", live + "seo-agency-brisbane/"), ("Website SEO Migration Support", live + "website-seo-migration-support/")]),
        ("Paid & social media", [("Google Ads Management (PPC Marketing)", live + "ppc-agency/"), ("Social Media Marketing", social), ("LinkedIn Advertising", prefix + "linkedin-advertising-agency/index.html"), ("Instagram Ads", prefix + "instagram-ads-agency/index.html"), ("Facebook Advertising", prefix + "facebook-advertising-agency/index.html")]),
        ("Content & retention", [("Inbound Marketing", live + "inbound-and-content-marketing/"), ("Email Marketing (EDM)", live + "email-marketing/")]),
    ])
    knowledge = layered("knowledge", [
        ("Insights & guides", [("Articles", live + "articles/"), ("FAQs", live + "faqs/"), ("Digital Marketing Cost Guide 2026", live + "articles/digital-agency-costs/"), ("Glossary of Digital Marketing Terms", live + "articles/marketing-terms/")]),
        ("Learning & opportunities", [("Marketing Training Program", live + "digital-marketing-course/"), ("Digilari University Scholarship", live + "digilari-scholarship/")]),
    ])
    contact = f'<div class="dig-submenu" id="dig-menu-contact">{links([("Contact Us", live + "contact-us/"), ("Join Us", live + "join-us/")])}</div>'
    meta = '<a class="dig-phone" href="tel:1300859358">1300 859 358</a><a class="dig-pricing" href="https://digilari.com.au/our-pricing/">Our Pricing</a>'
    return f'''<header class="dig-header" id="dig-header"><div class="dig-header-inner">
<a class="dig-brand" href="{home}" aria-label="Digilari Media home"><img src="{logo}" width="286" height="150" alt="Digilari Media"></a>
<button class="dig-menu-toggle" type="button" aria-label="Open menu" aria-controls="dig-primary-nav" aria-expanded="false"><span></span><span></span><span></span></button>
<nav class="dig-primary-nav" id="dig-primary-nav" aria-label="Main navigation">
{group("Why Digilari", "why", why, live + "why-digilari/")}
{group("Our Capabilities", "capabilities", capabilities)}
<a class="dig-nav-direct" href="{live}case-studies/">Case Studies</a>
{group("Knowledge Hub", "knowledge", knowledge, live + "articles/")}
{group("Contact Us", "contact", contact, live + "contact-us/")}
<div class="dig-mobile-meta">{meta}</div></nav><div class="dig-header-meta">{meta}</div>
</div></header>'''


def enquiry_form(topic="Social media marketing"):
    topic = escape(topic, quote=True)
    return f'''<section class="enquiry-panel" id="enquiry" aria-labelledby="enquiry-title">
<p class="eyebrow">Start a conversation</p><h2 id="enquiry-title">Tell us what you want to grow.</h2>
<p class="enquiry-intro">Share your details and goals so we can discuss the right {topic.lower()} approach for your business.</p>
<form class="enquiry-form" data-enquiry-form data-topic="{topic}" action="mailto:marketing@digilari.com.au" method="post" enctype="text/plain" aria-describedby="enquiry-note">
<label for="enquiry-website">Website URL <span aria-hidden="true">*</span></label><input id="enquiry-website" name="website" type="url" placeholder="https://yourbusiness.com.au" autocomplete="url" required maxlength="400">
<div class="enquiry-fields"><div><label for="enquiry-name">Your name <span aria-hidden="true">*</span></label><input id="enquiry-name" name="name" type="text" autocomplete="name" required maxlength="150"></div><div><label for="enquiry-phone">Phone number <span aria-hidden="true">*</span></label><input id="enquiry-phone" name="phone" type="tel" autocomplete="tel" required maxlength="40"></div></div>
<label for="enquiry-email">Work email <span aria-hidden="true">*</span></label><input id="enquiry-email" name="email" type="email" autocomplete="email" required maxlength="254">
<label for="enquiry-goal">What would you like to achieve? <span class="field-optional">Optional</span></label><textarea id="enquiry-goal" name="goal" rows="2" maxlength="1500" placeholder="More qualified enquiries, product sales or a clearer social strategy..."></textarea>
<button class="button enquiry-submit" type="submit">Prepare my enquiry <span aria-hidden="true">↗</span></button>
<p class="enquiry-note" id="enquiry-note">Opens your email app with your enquiry ready to send.</p>
<p class="enquiry-status" role="status" aria-live="polite" hidden></p>
</form><p class="enquiry-call">Prefer to talk? <a href="tel:1300859358">1300 859 358</a></p>
</section>'''
