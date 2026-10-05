"""Build the three platform service mockups with the shared Digilari navigation."""

from html import escape
from pathlib import Path

from components import navigation, enquiry_form


ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "index.html"

PAGES = {
    "linkedin-advertising-agency": {
        "platform": "LinkedIn",
        "title": "LinkedIn Advertising Agency Australia | Digilari Media",
        "description": "Digilari is a LinkedIn advertising agency for Australian B2B businesses. Reach decision-makers with targeted LinkedIn Ads, creative, lead capture and clear reporting.",
        "hero": "A LinkedIn advertising agency for considered B2B decisions.",
        "intro": "As a LinkedIn advertising agency, Digilari helps Australian B2B teams reach specific roles, industries and target accounts. We align targeting, creative and landing pages with your sales process, then measure the enquiries that become real opportunities.",
        "services": [
            ("01 / Audience", "Decision-maker targeting", "Build segments around job function, seniority, industry, company size and named accounts where relevant."),
            ("02 / Creative", "Sponsored content & offers", "Match the message to the buying stage with thought leadership, video, documents and clear calls to action."),
            ("03 / Capture", "Lead generation journeys", "Choose between native lead forms and landing pages based on friction, data quality and follow-up needs."),
            ("04 / Improve", "Testing & optimisation", "Review creative, audience overlap, lead quality and cost per qualified opportunity, then refine spend."),
        ],
        "approach_title": "Built for considered B2B decisions.",
        "approach_copy": "LinkedIn is strongest when the offer fits a defined business audience. We map the roles involved in a purchase, develop useful content for each stage and connect campaigns to a credible next step. Account-based campaigns can focus spend on priority organisations, while broader campaigns create new demand.",
        "fit": ["High-value B2B products or services", "Longer sales cycles with several stakeholders", "A clear offer, event, resource or consultation", "A sales team able to follow up and qualify leads"],
        "measurement": "We look beyond clicks and form fills. Useful measures include lead quality, sales-qualified leads, cost per opportunity and pipeline influenced, using CRM feedback where it is available.",
        "case_title": "Topdrill: LinkedIn Ads for mining recruitment",
        "case_copy": "Digilari segmented experienced and entry-level candidates and sent each group to tailored landing pages. LinkedIn delivered 2,461 clicks from 85,024 impressions, a 2.89% click-through rate. Google retargeting supported the wider recruitment journey.",
        "case_label": "Published Digilari case study",
        "case_url": "https://digilari.com.au/case-studies/topdrill/",
        "case_link": "Read the Topdrill case study",
        "faqs": [
            ("What does a LinkedIn advertising agency do?", "It plans audiences and offers, builds LinkedIn campaigns and creative, manages spend and reports on the business outcomes produced by the leads."),
            ("Which LinkedIn ad formats do you use?", "The format depends on the goal. Sponsored content, video, document ads and lead generation forms can all have a role; we choose formats after reviewing the audience and offer."),
            ("Are LinkedIn Ads suitable for a small budget?", "They can be when the audience and offer are tightly defined. We assess whether the available budget can produce enough useful learning before recommending a campaign."),
            ("How much does LinkedIn advertising cost?", "Total investment includes media spend and agency work. It depends on the target audience, creative, account complexity and campaign duration. We provide a tailored proposal after reviewing your goals."),
        ],
    },
    "instagram-ads-agency": {
        "platform": "Instagram",
        "title": "Instagram Ads Agency Australia | Digilari Media",
        "description": "Work with an Instagram Ads agency that plans creative, Reels, Stories, audience testing and conversion tracking around your goals. Digilari serves brands across Australia.",
        "hero": "An Instagram Ads agency that gives attention somewhere to go.",
        "intro": "Digilari builds Instagram advertising campaigns for Australian brands that need more than likes. We combine platform-native creative with audience strategy, product or lead journeys, and reporting tied to sales or enquiries.",
        "services": [
            ("01 / Creative", "Reels, Stories & Feed", "Develop short-form video, static and carousel concepts for the placements your audience actually uses."),
            ("02 / Audience", "Prospecting & retargeting", "Test broad and defined audiences, then re-engage people who have shown genuine interest."),
            ("03 / Journey", "Product & lead pathways", "Connect ads to useful product pages, catalogues or lead pages with a clear next action."),
            ("04 / Learn", "Creative testing", "Compare hooks, formats, messages and offers, then put more budget behind the combinations that convert."),
        ],
        "approach_title": "Designed for discovery and action.",
        "approach_copy": "Instagram is a visual platform. The opening seconds, format and destination all matter. We design campaigns around the moment someone first notices your brand, the questions they need answered and the action you want them to take. Meta Ads Manager allows Instagram and Facebook placements to be coordinated when that helps performance.",
        "fit": ["Products or services with a strong visual story", "Enough creative to test more than one angle", "A clear destination for purchase or enquiry", "A willingness to review performance beyond follower growth"],
        "measurement": "We report on the conversion goal first, such as purchases, qualified enquiries or cost per acquisition. Reach, video engagement and click-through rate help explain why performance changes. We also review tracking quality before drawing conclusions.",
        "case_title": "Instagram campaign case study",
        "case_copy": "Placeholder for a verified Digilari Instagram Ads campaign. Add an approved client brief, creative examples and measured outcomes before publishing a result claim.",
        "case_label": "Case study placeholder",
        "case_url": "../index.html#case-studies",
        "case_link": "See the published social campaign",
        "faqs": [
            ("What does an Instagram Ads agency manage?", "It plans audiences and creative, builds campaigns in Meta Ads Manager, monitors spend and reports on results such as enquiries or purchases."),
            ("Should we use Reels, Stories or Feed ads?", "That depends on the creative and goal. We test placements and formats rather than assuming one will work for every audience."),
            ("Can Instagram ads support ecommerce?", "Yes. Product catalogues and conversion-focused landing pages can connect discovery to purchase when the feed, offer and tracking are in good order."),
            ("How much do Instagram ads cost?", "Budget depends on audience, creative volume, competition and the outcome you need. We separate media spend from management and creative costs in a tailored proposal."),
        ],
    },
    "facebook-advertising-agency": {
        "platform": "Facebook",
        "title": "Facebook Advertising Agency Australia | Digilari Media",
        "description": "Digilari is a Facebook advertising agency for Australian businesses. Plan and manage Meta lead ads, ecommerce campaigns, retargeting, creative and conversion reporting.",
        "hero": "A Facebook advertising agency built to earn its place in your budget.",
        "intro": "Digilari plans and manages Facebook Ads for Australian businesses that need qualified leads, sales or stronger demand. We connect audience strategy, creative, landing pages and measurement so you can see what paid social contributes.",
        "services": [
            ("01 / Leads", "Lead generation ads", "Choose native forms or landing pages, set clear qualification criteria and plan timely follow-up."),
            ("02 / Sales", "Catalogue & sales campaigns", "Use suitable product feeds and conversion journeys for ecommerce offers where the account is ready."),
            ("03 / Reach", "Prospecting & retargeting", "Introduce the offer to new audiences and re-engage people who have already interacted with your brand."),
            ("04 / Control", "Creative & budget testing", "Test messages and formats, review spend allocation and shift budget toward stronger outcomes."),
        ],
        "approach_title": "A plan for leads, sales and the steps between.",
        "approach_copy": "Facebook Ads can reach people before they search for your product or service. That makes the offer, creative and follow-up essential. We define the action first, build a campaign structure around it, and review whether Instagram placements should share the same Meta strategy.",
        "fit": ["A clear offer with a defined audience", "A landing page or lead follow-up process", "Creative assets that can be tested and refreshed", "A way to assess lead quality or sales, not just traffic"],
        "measurement": "Depending on the campaign, we report on cost per qualified lead, purchases, cost per acquisition or return on ad spend. We review event tracking and attribution limitations before treating platform numbers as the whole picture.",
        "case_title": "Facebook campaign case study",
        "case_copy": "Placeholder for a verified Digilari Facebook Ads campaign. Add an approved client brief, account approach and measured outcomes before publishing a result claim.",
        "case_label": "Case study placeholder",
        "case_url": "../index.html#case-studies",
        "case_link": "See the published social campaign",
        "faqs": [
            ("What does a Facebook advertising agency do?", "It plans and manages Meta campaigns, develops creative, monitors spend and reports on outcomes such as qualified leads or sales."),
            ("Are Facebook and Instagram ads managed together?", "Both use Meta Ads Manager. We can coordinate placements and budgets while still tailoring creative and reporting to how each placement performs."),
            ("How much does Facebook advertising cost?", "The budget has three parts: media spend, management and creative. We recommend a scope after reviewing your objectives, audience, account and available assets."),
            ("How do you measure lead quality?", "We define a useful lead with your team, review form or landing-page data and use sales follow-up feedback where possible. That prevents cheap but irrelevant leads from looking like success."),
        ],
    },
}


def header_for(slug: str) -> str:
    return navigation("../", slug, mockup_root="../../")


def cards(items: list[tuple[str, str, str]]) -> str:
    return "\n".join(
        f'<article class="service-card"><span class="card-number">{escape(label)}</span>'
        f'<div class="service-icon" aria-hidden="true">{i:02d}</div><h3>{escape(title)}</h3>'
        f'<p>{escape(copy)}</p></article>'
        for i, (label, title, copy) in enumerate(items, 1)
    )


def faqs(items: list[tuple[str, str]]) -> str:
    return "\n".join(
        f'<details><summary>{escape(question)}</summary><p>{escape(answer)}</p></details>'
        for question, answer in items
    )


def build(slug: str, data: dict) -> str:
    platform = data["platform"]
    sibling_links = "".join(
        f'<a href="../{other}/index.html">{escape(details["platform"])} Ads <span aria-hidden="true">↗</span></a>'
        for other, details in PAGES.items() if other != slug
    )
    fit_items = "".join(f"<li>{escape(item)}</li>" for item in data["fit"])
    published = data["case_label"].startswith("Published")
    metric = '<div class="case-metric"><strong>2.89%</strong><span>LinkedIn click-through rate in the published Topdrill campaign</span></div>' if published else ""
    return f'''<!doctype html>
<html lang="en-AU">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex, nofollow">
  <title>{escape(data["title"])}</title>
  <meta name="description" content="{escape(data["description"], quote=True)}">
  <link rel="stylesheet" href="../../assets/dig-shared.css">
  <link rel="stylesheet" href="../styles.css">
  <link rel="stylesheet" href="../platform.css">
  <script src="../../assets/dig-shared.js" defer></script>
  <script src="../main.js" defer></script>
</head>
<body class="platform-page" data-platform="{platform.lower()}">
  <a class="skip-link" href="#main">Skip to content</a>
  {header_for(slug)}
  <main id="main">
    <section class="hero platform-hero" aria-labelledby="hero-title"><div class="wrap hero-grid">
      <div class="hero-copy"><p class="eyebrow"><span class="eyebrow-line"></span> {platform} advertising agency · Australia</p>
        <h1 id="hero-title">{escape(data["hero"])}</h1><p class="hero-lead">{escape(data["intro"])}</p>
        <div class="hero-actions"><a class="button" href="#enquiry">Discuss {platform} advertising <span aria-hidden="true">↗</span></a><a class="text-link" href="#services">See what we manage <span aria-hidden="true">↓</span></a></div>
        <p class="hero-reassurance">A conversation about your goals. No obligation.</p>
      </div>
      {enquiry_form(platform + " advertising")}
    </div></section>
    <div class="proof-strip"><div class="wrap proof-inner"><p><strong>A campaign with a job to do.</strong> Audience, creative, conversion path and reporting.</p><a href="#case-studies">See the proof <span aria-hidden="true">↗</span></a></div></div>
    <nav class="page-nav" aria-label="On this page"><div class="wrap page-nav-inner"><span class="page-nav-label">On this page</span><div class="page-nav-links"><a href="#services">Services</a><a href="#approach">Approach</a><a href="#measurement">Measurement</a><a href="#case-studies">Case study</a><a href="#faq">FAQs</a></div><a class="page-nav-cta" href="#enquiry">Let's talk ↗</a></div></nav>
    <section class="section" id="services" aria-labelledby="services-title"><div class="wrap"><div class="section-heading split-heading"><div><p class="eyebrow">{platform} Ads management</p><h2 id="services-title">What our {platform} advertising service covers.</h2></div><p>Strategy and execution belong together. Each campaign starts with the audience and the action you need, then moves into creative, launch and ongoing improvement.</p></div><div class="service-grid">{cards(data["services"])}</div></div></section>
    <section class="section platform-section" id="approach" aria-labelledby="approach-title"><div class="wrap platform-layout"><div class="platform-copy"><p class="eyebrow">The approach</p><h2 id="approach-title">{escape(data["approach_title"])}</h2><p>{escape(data["approach_copy"])}</p><a class="text-link" href="#enquiry">Talk through your brief ↗</a></div><div class="fit-panel"><span class="fit-label">A strong starting point</span><h3>{platform} Ads may fit when you have:</h3><ul>{fit_items}</ul><p>We check this in the first conversation before recommending a budget or format.</p></div></div></section>
    <section class="section outcomes-section" id="measurement" aria-labelledby="measurement-title"><div class="wrap outcomes-grid"><div><p class="eyebrow">Measurement</p><h2 id="measurement-title">Know what the campaign is <em>actually producing.</em></h2><p>{escape(data["measurement"])}</p><a class="button button-light" href="#enquiry">Request a campaign review ↗</a></div><div class="outcomes-points"><div><span>01</span><h3>Define the result</h3><p>Agree the outcome and conversion action before launch.</p></div><div><span>02</span><h3>Check the signal</h3><p>Review tracking and lead or sales data so the report is useful.</p></div><div><span>03</span><h3>Use the learning</h3><p>Change creative, audience, offer or budget when evidence supports it.</p></div></div></div></section>
    <section class="section case-section" id="case-studies" aria-labelledby="case-title"><div class="wrap"><div class="section-heading"><p class="eyebrow">Work and proof</p><h2 id="case-title">{escape(data["case_title"])}</h2></div><article class="case-card {'case-card-featured' if published else 'case-card-placeholder'} platform-case"><div class="case-card-top"><span class="case-status">{escape(data["case_label"])}</span><span class="case-platform">{platform} Ads</span></div><p>{escape(data["case_copy"])}</p>{metric}<a class="case-link" href="{escape(data["case_url"], quote=True)}">{escape(data["case_link"])} ↗</a></article></div></section>
    <section class="section pricing-section" aria-labelledby="pricing-title"><div class="wrap pricing-inner"><div><p class="eyebrow">Budget and scope</p><h2 id="pricing-title">What goes into the investment?</h2></div><p>We separate media spend from strategy, creative and campaign management. The right budget depends on your audience, offer and the amount of testing needed. We will give you a clear scope after reviewing your account and goals. <a href="https://digilari.com.au/our-pricing/">View Digilari pricing ↗</a></p></div></section>
    <section class="section faq-section" id="faq" aria-labelledby="faq-title"><div class="wrap faq-grid"><div><p class="eyebrow">The details</p><h2 id="faq-title">{platform} Ads FAQs.</h2><p>Get answers to the practical questions before you commit to a campaign.</p><a class="text-link" href="#enquiry">Ask us a question ↗</a></div><div class="faq-list">{faqs(data["faqs"])}</div></div></section>
    <section class="section related-section" aria-labelledby="related-title"><div class="wrap"><p class="eyebrow">Explore the channel mix</p><h2 id="related-title">See how the platforms work together.</h2><div class="related-links"><a href="../index.html">Social Media Marketing <span aria-hidden="true">↗</span></a>{sibling_links}</div></div></section>
    <section class="final-cta" aria-labelledby="final-title"><div class="wrap final-inner"><div><p class="eyebrow">Ready to plan?</p><h2 id="final-title">Let's put {platform} to work with a clear goal.</h2><p>Tell us what you need to grow. We'll discuss the audience, creative and budget needed to test it properly.</p></div><div class="final-actions"><a class="button button-light" href="#enquiry">Talk to a strategist ↗</a><a href="tel:1300859358">Or call 1300 859 358</a></div></div></section>
  </main>
  <footer class="site-footer"><div class="wrap footer-inner"><a href="https://digilari.com.au/" aria-label="Digilari Media home"><img src="../../assets/dig-logo-c5.png" width="286" height="150" alt="Digilari Media"></a><p>{platform} advertising with a purpose.</p><div><a href="../index.html">Social media</a><a href="https://digilari.com.au/contact-us/">Contact</a><a href="https://digilari.com.au/our-pricing/">Pricing</a></div></div></footer>
  <div class="mobile-action"><a href="tel:1300859358">Call us</a><a href="#enquiry">Discuss {platform} Ads ↗</a></div>
</body>
</html>
'''


if __name__ == "__main__":
    for slug, data in PAGES.items():
        output = ROOT / slug / "index.html"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(build(slug, data), encoding="utf-8")
        print(output)
