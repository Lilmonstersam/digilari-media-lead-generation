"""Build the case study list and the case study pages (one page per project).

Run from the repository root, then synchronise the shared header:

    python3 scripts/build_case_studies.py
    python3 scripts/sync_header.py

Figures come from Mars's paid social notes and Celine's organic social notes
(November 2026), checked against Meta Ads, LinkedIn Ads and GA4 via Optmyzr.
"""

from html import escape
from pathlib import Path
import sys

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "case-studies"
sys.path.insert(0, str(REPO / "social-media-marketing" / "scripts"))
from components import navigation  # noqa: E402

LIVE = "https://digilari.com.au/"
UPLOADS = LIVE + "wp-content/uploads/"

FILTERS = [("all", "All"), ("cro", "CRO"), ("paid-ads", "Paid Ads"), ("seo", "SEO"), ("social-media", "Social Media")]

# Existing case studies published on digilari.com.au. Cards link to the live pages.
LIVE_CASES = [
    {"name": "Topdrill", "url": LIVE + "case-studies/topdrill/", "image": UPLOADS + "2026/02/Topdrill_img.png", "categories": ["cro", "paid-ads", "seo"],
     "stats": [("+2.89%", "Click-Through Rate", "YoY growth"), ("+15.9%", "Audience Penetration", "YoY growth"), ("+4.97%", "Engagement Rate", "YoY increase")],
     "excerpt": "Topdrill is one of Australia’s most respected drilling contractors, known for its strong on-site culture, reliable crews, and long-standing relationships across the mining sector."},
    {"name": "TyreDoctor", "url": LIVE + "case-studies/tyredoctor/", "image": UPLOADS + "2024/07/Web-elements-6-e1722220543427.png", "categories": ["cro", "paid-ads", "seo"],
     "stats": [("+84%", "Organic Traffic", "YoY growth"), ("+141%", "Conversions", "YoY growth"), ("+78%", "Conversion Rate", "YoY increase")],
     "excerpt": "Tyre Doctor provides premium tyre and wheel solutions for Australia’s earthmoving and mining industries, offering OTR, loader, and crane tyres with expert service, innovation, safety, and sustainability for long-term customer partnerships."},
    {"name": "Scholz Electrical", "url": LIVE + "case-studies/scholz-electrical/", "image": UPLOADS + "2024/07/Web-elements-9-e1722224239443.png", "categories": ["cro", "paid-ads", "seo"],
     "stats": [("+16%", "Organic Traffic", "YoY growth"), ("+57%", "Key Event (Conv.)", "YoY growth"), ("+43%", "Conversion Rate", "YoY increase")],
     "excerpt": "Founded in 1970 by Michael Scholz, Scholz Electrical provides expert electrical services with a commitment to quality, customer satisfaction, and sustainability, offering skilled professionals and solar solutions for reliable, eco-friendly results."},
    {"name": "OzHitch", "url": LIVE + "case-studies/ozhitch/", "image": UPLOADS + "2024/07/Web-elements-e1721719061682.png", "categories": ["cro", "seo"],
     "stats": [("+50%", "Organic Traffic", "YoY growth"), ("+328%", "Conversions", "YoY growth"), ("+3624%", "Conversion Rate", "YoY increase")],
     "excerpt": "OzHitch delivers durable off-road trailer and caravan couplings for Australian 4x4 enthusiasts. With self-aligning technology and top safety standards, they ensure reliable, easy-to-use towing solutions backed by excellent after-sales support."},
    {"name": "RCR Services", "url": LIVE + "case-studies/rcr-services/", "image": UPLOADS + "2024/07/Web-elements-2-e1722211368334.png", "categories": ["cro", "paid-ads", "seo"],
     "stats": [("+31.6%", "Key event rate", "YoY growth"), ("+301.4%", "Events per session", "YoY growth"), ("+46.2%", "Average engagement time per session", "YoY increase")],
     "excerpt": "RCR specialises in locating and identifying damage in commercial and industrial buildings and provides remedial services including: waterproofing, roof repairs, roof restorations, roof coatings, concrete repair and more."},
    {"name": "Elite Liquid Waste", "url": LIVE + "case-studies/elite-liquid-waste/", "image": UPLOADS + "2024/07/Web-elements-1-2-e1722214034210.png", "categories": ["cro", "seo"],
     "stats": [("+42%", "Organic Traffic", "YoY growth"), ("+74%", "Key Events (Conv.)", "YoY growth"), ("+32%", "Conversion Rate", "YoY increase")],
     "excerpt": "Elite Liquid Waste Management specialise in the collection, transportation and disposal of all kinds of liquid waste as well as drain cleaning, vacuum excavation and in-line camera diagnosis. Elite also operate a number of potable water delivery trucks and low-level car park access vehicles."},
]

ICONS = {
    "search": '<svg viewBox="0 0 24 24"><circle cx="10.5" cy="10.5" r="6"/><path d="m15 15 5 5"/></svg>',
    "target": '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1" fill="currentColor"/></svg>',
    "image": '<svg viewBox="0 0 24 24"><rect x="3.5" y="4.5" width="17" height="15" rx="2.5"/><circle cx="9" cy="10" r="1.8"/><path d="m4.5 17.5 5-5 3.5 3.5 2.5-2.5 4 4"/></svg>',
    "chart": '<svg viewBox="0 0 24 24"><path d="M4 19.5h16M7 16v-5M12 16V7M17 16v-8"/></svg>',
    "refresh": '<svg viewBox="0 0 24 24"><path d="M19 8.5A7.5 7.5 0 0 0 5.6 7M5 15.5A7.5 7.5 0 0 0 18.4 17"/><path d="M5 3.5V7h3.5M19 20.5V17h-3.5"/></svg>',
    "video": '<svg viewBox="0 0 24 24"><rect x="3.5" y="6" width="12.5" height="12" rx="2.5"/><path d="m16 10.5 4.5-2.5v8L16 13.5"/></svg>',
    "people": '<svg viewBox="0 0 24 24"><circle cx="9" cy="8.5" r="3"/><path d="M3.5 19c.6-3.2 2.8-5 5.5-5s4.9 1.8 5.5 5"/><circle cx="17" cy="9.5" r="2.4"/><path d="M15.5 14.4c2.4-.4 4.4 1.2 5 4.1"/></svg>',
    "pin": '<svg viewBox="0 0 24 24"><path d="M12 21s-6.5-6.2-6.5-11a6.5 6.5 0 0 1 13 0c0 4.8-6.5 11-6.5 11Z"/><circle cx="12" cy="10" r="2.3"/></svg>',
    "calendar": '<svg viewBox="0 0 24 24"><rect x="3.5" y="5" width="17" height="15" rx="2.5"/><path d="M3.5 10h17M8 3v4M16 3v4"/></svg>',
    "chat": '<svg viewBox="0 0 24 24"><path d="M4.5 5.5h15v10h-8l-4.5 3.5v-3.5h-2.5Z"/><path d="M8.5 9.5h7M8.5 12h4.5"/></svg>',
    "shield": '<svg viewBox="0 0 24 24"><path d="M12 3.5 19 6v5.5c0 4.3-3 7.6-7 9-4-1.4-7-4.7-7-9V6Z"/><path d="m8.8 12 2.2 2.2 4.2-4.4"/></svg>',
    "layers": '<svg viewBox="0 0 24 24"><path d="m12 4 8.5 4.5L12 13 3.5 8.5Z"/><path d="m3.5 12.5 8.5 4.5 8.5-4.5M3.5 16.5 12 21l8.5-4.5"/></svg>',
}

# New social media case studies built in this mockup.
CASES = [
    {
        "slug": "streamline-carports-facebook-ads",
        "name": "Streamline Carports",
        "subtitle": "Cutting the Cost of Every Quote Request with Meta Lead Ads",
        "tag": "Paid Social",
        "platform": "Meta Ads",
        "theme": "meta",
        "categories": ["paid-ads", "social-media"],
        "description": "How Digilari cut Streamline Carports' Meta cost per lead by 62% and grew enquiries from about 2 to about 20 a month.",
        "excerpt": "Streamline Carports builds steel carports for Auckland homeowners. A refined Meta audience and durability-led creative cut its cost per lead by 62% while enquiries grew tenfold.",
        "screen": ("Facebook lead ads", "−62%", "cost per lead"),
        "phone": ("Streamline Carports", "Auckland's strongest carports", "Get Quote"),
        "challenge_ad": ("IMAGES/ads/streamline-carports-ad.jpg", "Streamline Carports Facebook ad: Durable and low-maintenance carports, Auckland's strongest carports with a 10-year structural warranty, with a Get quote button", "Top ad (Carports | Oct 2025 | Ad 2): 156 leads at NZ$52.40 each over the last 12 months"),
        "facts": [("Industry", "Steel carports"), ("Location", "Auckland, New Zealand"), ("Channels", "Facebook and Instagram (Meta Ads)"), ("Objective", "Quote and contact enquiries"), ("Period", "May 2024 to October 2026")],
        "about": "Streamline Carports designs and builds steel carports for homeowners across Auckland, with sustainable PurlinDek steel roofing and a 10-year structural warranty. Meta Ads is one of its main sources of quote requests, sending people to the carports page to request a quote or get in touch.",
        "challenge": [
            "Streamline needed a steady flow of quote requests from Meta at a cost that made sense for a considered home purchase.",
            "At launch (May to October 2024), a broad Auckland campaign was costing NZ$148 per enquiry and bringing in about 2 enquiries a month. The audience was too wide, and the creative wasn't giving homeowners a clear reason to choose Streamline over a cheaper alternative.",
        ],
        "solutions_intro": "Digilari rebuilt the audience and creative, then kept moving budget towards what the results supported:",
        "solutions": [
            ("target", "Refined lookalike audience", "Built an ad set from a 1% lookalike of recent website visitors, layered with homeowner, home improvement and vehicle-owner interests. Run side by side with the original broad audience, it cost 42% less per lead (NZ$61.44 against NZ$105.49)."),
            ("image", "Durability-led creative", "Rebuilt the ads around what matters to carport buyers: strength, rust protection, PurlinDek steel roofing and a 10-year structural warranty. Meta's flexible format tested three images with several headlines and primary texts in each ad."),
            ("chart", "Budget that follows results", "Paused the weaker broad ad set and moved its budget to the refined one. When GA4 showed a separate traffic campaign's visitors weren't engaging, 70% of its budget moved into lead generation."),
            ("refresh", "Creative fatigue monitoring", "Tracked cost per lead month by month and refreshed copy and creative when results slipped, rather than letting ageing ads absorb more budget."),
        ],
        "results_title": "Lower Cost per Lead, Ten Times the Enquiries",
        "results": [
            ("Cost per lead", "down 62%, from NZ$148.22 at launch to NZ$56.57 over the last 12 months."),
            ("Lead volume", "from about 2 enquiries a month at launch to about 20 a month, with 234 Meta-reported leads in the last 12 months."),
            ("Click efficiency", "click-through rate up from 1.14% to 1.56%, and cost per click down from NZ$1.09 to NZ$0.82."),
            ("Website activity", "GA4 recorded 80 quote and contact form submissions and 54 phone-link clicks from Meta visitors over the same 12 months."),
        ],
        "counters": [("−62%", "Cost per Lead", "vs launch"), ("10×", "Monthly Enquiries", "vs launch"), ("+37%", "Click-Through Rate", "vs launch")],
        "stats": [("−62%", "Cost per Lead", "vs launch"), ("10×", "Monthly Enquiries", "vs launch"), ("+37%", "Click-Through Rate", "vs launch")],
        "table": (["Metric (NZD)", "Launch: May to Oct 2024", "Last 12 months: Nov 2025 to Oct 2026"], [
            ["Spend", "$1,630", "$13,237"], ["Impressions", "131,369", "1,031,819"], ["Click-through rate", "1.14%", "1.56%"],
            ["Cost per click", "$1.09", "$0.82"], ["Leads", "11", "234"], ["Cost per lead", "$148.22", "$56.57"], ["Leads per month", "About 2", "About 20"]]),
        "source": "Sources: Meta Ads (via Optmyzr) and GA4. Figures in NZD. Meta-reported leads use the pixel Contact event, which fires when someone submits a quote or contact enquiry.",
        "service": ("Facebook Advertising", "../../social-media-marketing/facebook-advertising-agency/index.html"),
    },
    {
        "slug": "three-springs-farm",
        "name": "Three Springs Farm",
        "subtitle": "Harvesting Growth with Targeted Paid Ads Across Google and Meta",
        "tags": ["Paid Ads", "Paid Social"],
        "badge": "Now with Meta Ads",
        "platform": "Google + Meta Ads",
        "theme": "meta",
        "categories": ["paid-ads", "social-media"],
        "description": "How Digilari grew Three Springs Farm's paid search revenue by 230% and delivered 338 Meta-attributed online orders at a 7.51x return on ad spend.",
        "excerpt": "Located in Australia’s Northern Rivers, Three Springs Farm is a certified organic grower specializing in medicinal herbs. Their Complete•3 Turmeric Liquid Extract embodies a “food as medicine” approach, blending tradition and science for health.",
        "image": UPLOADS + "2024/07/Web-elements-7-e1722222419247.png",
        "logo": UPLOADS + "2024/07/image-3.png",
        "challenge_image": UPLOADS + "2024/07/Web-elements-8-e1722222494897.png",
        "facts": [("Industry", "Certified organic herbs"), ("Location", "Northern Rivers, Australia"), ("Channels", "Google Ads and Meta Ads (Facebook and Instagram)"), ("Objective", "Online sales")],
        "about": "Nestled in Australia’s Northern Rivers, Three Springs Farm is a certified organic producer with a focus on medicinal herbs and sustainable farming. Their flagship product, Complete•3 Turmeric Liquid Extract, reflects their commitment to a “food as medicine” philosophy, bringing together traditional knowledge and scientific backing to promote health. Digilari manages its paid advertising on both Google and Meta: Google captures people already searching, while Meta finds new customers likely to buy.",
        "challenge": [
            ("Google Ads", "Three Springs Farm faced substantial obstacles in digital advertising, primarily due to high conversion costs that restricted ad visibility and effectiveness. The challenge was twofold: enhancing ad delivery to reach a wider yet targeted audience within a tight budget, and addressing gaps in online customer engagement."),
            ("Meta Ads", "With a fixed budget of $300 a month, Meta needed to bring in new customers profitably, not just traffic. The previous Meta campaign was already returning 6.92x, so the task was to keep finding new buyers across Australia without letting the cost per purchase climb."),
        ],
        "solution_groups": [
            ("Google Ads", "Digilari embarked on a comprehensive optimisation strategy to tackle these challenges:", [
                ("image", "Google Ads Optimisation", "Conducted rigorous ad copy testing to identify messaging that would engage the target audience effectively."),
                ("target", "Strategic Bid Adjustments", "Implemented strategic bid adjustments to maximise reach without overspending, optimising visibility among high-intent users."),
                ("search", "Performance Max campaigns", "Launched through a newly established Google Merchant Centre account, allowing products to appear in Google Shopping searches. This integration used machine learning to distribute ads across multiple channels, enhancing targeting and efficiency."),
            ]),
            ("Meta Ads", "On Meta, Digilari focused spend on people close to buying and kept testing the creative:", [
                ("people", "Near-buyer audiences", "The main prospecting ad set targeted health, wellness, organic food, fitness and gardening interests, with recent buyers excluded so budget went to new customers. It was refined over time into a 3% lookalike of people who added to cart but didn't buy, and took 85% of spend for 291 orders at 7.53x."),
                ("image", "Credibility and offer-led creative", "Single image ads and a 10-card carousel led with the product's credentials (certified organic, grown on the family farm) and the subscription and free-delivery offers. The carousel returned 10.2x."),
                ("calendar", "Seasonal Christmas push", "A separate, time-limited ad set promoted the returning 500ml bottle for Christmas, optimised to checkouts. It delivered 47 orders at 7.38x."),
                ("layers", "Facebook and Instagram together", "The campaign ran across both placements and let Meta allocate spend. Instagram took 12% of spend and returned 14.4x, against 6.5x on Facebook. A September 2025 creative refresh with subscription-saving messaging reached 16.5x."),
            ]),
        ],
        "result_groups": [
            {
                "eyebrow": "Results: Google Ads",
                "title": "Significant Gains in Paid Search Metrics",
                "items": [
                    ("Revenue Growth", "Year-over-year revenue generated from paid ads surged by 230%, showcasing the effectiveness of the optimised campaigns in converting clicks into sales."),
                    ("Paid Search Traffic", "Paid search sessions increased by 96%, demonstrating heightened visibility and engagement among potential customers."),
                    ("Key Events Growth", "Key events triggered by users from paid search channels grew by 112%, indicating improved interaction and engagement with site content."),
                ],
                "counters": [("+96%", "Paid Search Traffic", "YoY growth"), ("+230%", "Revenue", "YoY growth"), ("+112%", "Key Events", "YoY increase")],
            },
            {
                "eyebrow": "Results: Meta Ads",
                "title": "Meta-Attributed Sales at a 7.5x Return on Ad Spend",
                "items": [
                    ("Revenue", "$33,062 in Meta-attributed online sales from $4,404 in ad spend over 15 months (December 2024 to February 2026)."),
                    ("Orders", "338 orders at $13.03 each, with average order value up from $90.04 to $97.82."),
                    ("Return on ad spend", "7.51x, up from 6.92x on the previous campaign. Instagram placements returned 14.4x."),
                    ("Best month", "April 2025, with 44 orders and $4,735 in revenue from $299 in spend (15.8x)."),
                ],
                "counters": [("7.51×", "Return on Ad Spend", "Meta-attributed"), ("338", "Online Orders", "in 15 months"), ("+9%", "Average Order Value", "vs previous campaign")],
                "ads": [
                    ("IMAGES/ads/three-springs-farm-carousel-ad.jpg", "Three Springs Farm carousel ad for Complete 3 Turmeric Liquid Extract with an Order now button", "Carousel ad (AD4): 71 orders at 10.2x"),
                    ("IMAGES/ads/three-springs-farm-refreshed-ad.jpg", "Three Springs Farm refreshed ad offering up to 25% off with a monthly subscription and free shipping", "Refreshed ad, September 2025: 18 orders at 16.5x"),
                ],
                "timeline": [
                    ("Ongoing", "Monthly budget held at $300, with daily budgets reviewed and adjusted weekly."),
                    ("Jun 2025", "Reviewed targeting, budgets and creative, and adjusted Advantage+ creative settings."),
                    ("Aug 2025", "Fixed audience targeting after a Meta audience update removed some segments, and enabled Advantage+ creative adjustments."),
                    ("Sep 2025", "Refreshed the creative with subscription-saving messaging."),
                    ("Nov 2025", "Created a 3% lookalike audience and narrowed the broad targeting."),
                    ("Feb 2026", "Moved to a new campaign that also retargets people who added to cart without buying in the previous 90 days."),
                ],
                "table": (["Metric (AUD)", "Previous campaign: Jul to Nov 2024", "Sales campaign: Dec 2024 to Feb 2026"], [
                    ["Spend", "$1,352", "$4,404"], ["Orders", "104", "338"], ["Revenue", "$9,364", "$33,062"], ["Revenue per month", "$1,873", "$2,204"],
                    ["Return on ad spend", "6.92x", "7.51x"], ["Cost per order", "$13.00", "$13.03"], ["Average order value", "$90.04", "$97.82"], ["Conversion rate", "3.49%", "3.96%"]]),
                "source": "Source: Meta Ads (via Optmyzr). Figures in AUD. Orders and revenue are attributed by Meta and can include conversions that Google Analytics credits to another visit.",
            },
        ],
        "stats": [("+230%", "Paid Search Revenue", "YoY growth"), ("+96%", "Paid Search Traffic", "YoY growth"), ("7.51×", "Meta Ads ROAS", "Meta-attributed")],
        "services": [("Google Ads Management", LIVE + "ppc-agency/"), ("Instagram Ads", "../../social-media-marketing/instagram-ads-agency/index.html")],
        "draft_note": "This page merges the published Google Ads case study with new Meta Ads results. Client approval to be confirmed before publishing.",
    },
    {
        "slug": "duracube",
        "name": "Duracube",
        "subtitle": "Achieving Significant Growth Across Organic Search and LinkedIn",
        "tags": ["SEO", "CRO", "Paid Ads", "Paid Social"],
        "badge": "Now with LinkedIn Ads",
        "platform": "SEO + LinkedIn Ads",
        "theme": "linkedin",
        "categories": ["cro", "paid-ads", "seo", "social-media"],
        "description": "How Digilari grew Duracube's organic traffic by 50% and lifted its LinkedIn click-through rate from 0.53% to 4.97%.",
        "excerpt": "Duracube is an Australian-owned company specialising in wet area joinery solutions since 1987. They offer a comprehensive range of products, including toilet and shower partitions, lockers, bench seating, vanities, and privacy panels. With in-house manufacturing and a national network of installers, Duracube ensures efficient delivery and installation across Australia.",
        "image": UPLOADS + "2025/03/Web-elements.png",
        "card_image": UPLOADS + "2024/07/Web-elements-3-e1722212746144.png",
        "logo": UPLOADS + "2024/07/image-11-1024x233.png",
        "challenge_image": UPLOADS + "2025/03/Web-elements-1-e1747355899648-775x1024.png",
        "facts": [("Industry", "Wet area joinery for commercial projects"), ("Location", "Australia"), ("Channels", "SEO, CRO and LinkedIn Ads"), ("Objective", "Organic visibility, conversions and specifier reach")],
        "about": "Duracube, a leading provider of wet area joinery solutions, engaged in a comprehensive digital marketing strategy to enhance its online presence, drive traffic, and increase conversions. Its buyers include architects, designers, builders and project managers. This case study outlines the challenges faced, solutions implemented, and results achieved across organic search, the website and LinkedIn Ads.",
        "challenge": [
            ("Keyword Targeting and SEO Optimisation", "Duracube needed to optimise its content for a diverse set of keywords related to bathroom and toilet partitions, compact laminate, and accessibility standards, ensuring visibility across various search terms."),
            ("Technical SEO and Site Structure", "Ensuring the website was technically sound, with optimised meta tags, schema markup, and a logical site structure to improve search engine rankings and user experience."),
            ("Content and Local SEO", "Creating relevant content that addresses the needs of local audiences in multiple regions, including Melbourne, Sydney, Brisbane, and Adelaide."),
            ("Analytics and Performance Monitoring", "Implementing effective tracking and analysis of web traffic and user behaviour to continually refine the marketing strategy."),
            ("Reaching Specifiers on LinkedIn", "Duracube wanted to promote its Specifier Portal to senior people in architecture, design and building management. Its first LinkedIn campaigns used static and carousel ads optimised for website conversions, running at a 0.53% click-through rate and $1.95 per click."),
        ],
        "solution_groups": [
            ("Search and website", "Digilari embarked on a comprehensive optimisation strategy to tackle these challenges:", [
                ("search", "Keyword Optimisation & Content Strategy", "Implemented a targeted keyword strategy focusing on high-traffic and niche keywords such as “disabled toilet standards australia,” “toilet partitions brisbane,” and “compact laminate.” Created and optimised content around these keywords, ensuring alignment with user search intent and addressing frequently asked questions and common issues."),
                ("shield", "Technical SEO Improvements", "Conducted technical audits and implemented fixes for site speed, mobile usability, and crawl errors. Added schema markup for local businesses and sitelinks searchbox to enhance search engine visibility and click-through rates. Implemented universal search bars and sticky headers to improve navigation and user experience."),
                ("pin", "Local SEO & Content Marketing", "Developed a content plan focusing on localised keywords and services, such as “toilet partitions sydney” and “toilet partitions melbourne.” Published case studies, how-to guides, and industry news to engage the local audience and establish Duracube as an authority in the industry."),
                ("chart", "Performance Tracking & Analytics", "Set up comprehensive tracking through Google Analytics 4 (GA4) to monitor traffic acquisition, user behaviour, and engagement metrics. Regularly reviewed and optimised campaigns based on performance data, focusing on high-performing channels and addressing underperforming areas."),
            ]),
            ("LinkedIn Ads", "On LinkedIn, Digilari changed the format, the bidding and the targeting:", [
                ("video", "Video-first creative", "Replaced static and carousel ads with single video Sponsored Content: specifier-focused videos promoting the 15-year warranty and architect-ready tools such as Revit BIM models, then launch videos for the new First Nations Range. The best videos reached a 6.2% to 7.5% click-through rate."),
                ("target", "Click-focused bidding", "Switched from conversion bidding, which had too little data to learn from, to landing page click optimisation so LinkedIn could find the people most likely to visit."),
                ("people", "Senior decision-maker targeting", "Targeted 17 job titles at Senior, Manager, Director, Partner and Owner level, layered with relevant skills, industries and fields of study such as architecture. Companies with 1 to 10 staff and competitor employees were excluded."),
                ("layers", "Sector pages and tighter seniority", "In October 2026, targeting moved to job function and Manager-and-above seniority at companies with 51 or more staff, sending people to industrial, commercial and sports facility pages."),
            ]),
        ],
        "result_groups": [
            {
                "eyebrow": "Results: Search and website",
                "title": "Outstanding Performance Metrics and Achievements",
                "items": [
                    ("Increased Organic Traffic", "Organic search traffic increased by 50.38%, with users growing from 15,509 to 23,908 during the comparison period. Significant growth in key regions, with traffic from Melbourne, Sydney, and Brisbane showing marked improvements."),
                    ("Enhanced User Engagement", "Improved average session duration and pages per session, indicating better user engagement and content relevance."),
                    ("Successful Keyword Rankings", "Achieved top rankings for targeted keywords such as “disabled toilet standards australia,” “toilet partitions brisbane,” and “compact laminate.” Effective keyword strategy led to increased visibility and higher click-through rates for key search terms."),
                    ("Improved Technical Performance", "Technical SEO enhancements resulted in better mobile usability, and fewer crawl errors, contributing to overall site health and user experience. Schema markup and enhanced site structure facilitated better indexing and richer search results."),
                ],
                "counters": [("+52%", "New Users", "YoY growth"), ("+8%", "Key Events (Conv.)", "YoY growth"), ("+39%", "Engaged Sessions", "YoY increase")],
            },
            {
                "eyebrow": "Results: LinkedIn Ads",
                "title": "Nine Times the Click-Through Rate at Less Than Half the Cost per Click",
                "items": [
                    ("Click-through rate", "up from 0.53% to 4.97% on the video campaign."),
                    ("Cost per click", "down 58%, from $1.95 to $0.82."),
                    ("Website clicks", "83% more clicks (7,237 against 3,961) on 24% less spend ($5,860 against $7,716)."),
                    ("Sector pages", "the refined October 2026 campaign is running at a 3.89% click-through rate and $0.72 per click."),
                ],
                "counters": [("4.97%", "Click-Through Rate", "from 0.53%"), ("−58%", "Cost per Click", "vs static ads"), ("+83%", "Website Clicks", "on 24% less spend")],
                "ads": [
                    ("IMAGES/ads/duracube-specifier-video.jpg", "DuraCube LinkedIn video ad: DuraCube sets the standard in bathroom joinery systems, with an Access Our Specifier Resources call to action", "Specifier resources video: 7.5% click-through rate at $0.86 per click"),
                    ("IMAGES/ads/duracube-first-nations-range-video.jpg", "DuraCube LinkedIn video ad launching the First Nations Range, a DuraCube x Blaklash collaboration", "First Nations Range launch video: 6.2% click-through rate at $0.66 per click, 1,956 clicks"),
                    ("IMAGES/ads/duracube-blaklash-video.jpg", "DuraCube x Blaklash LinkedIn video ad: The Future of Built Environments is Here", "Launch teaser video: 5.4% click-through rate at $0.66 per click"),
                ],
                "table": (["Metric (AUD)", "Static + carousel: Aug 2024 to Sep 2025", "Video + sector pages: Sep 2025 to Nov 2026"], [
                    ["Spend", "$7,716", "$5,860"], ["Impressions", "750,232", "150,182"], ["Clicks", "3,961", "7,237"],
                    ["Click-through rate", "0.53%", "4.82%"], ["Cost per click", "$1.95", "$0.81"]]),
                "source": "Source: LinkedIn Ads (via Optmyzr). Figures in AUD. The 4.97% click-through rate is the video campaign alone; the table also includes the sector pages campaign.",
            },
        ],
        "stats": [("+52%", "New Users", "YoY growth"), ("+39%", "Engaged Sessions", "YoY increase"), ("4.97%", "LinkedIn CTR", "from 0.53%")],
        "services": [("SEO", LIVE + "seo-agency-brisbane/"), ("LinkedIn Advertising", "../../social-media-marketing/linkedin-advertising-agency/index.html")],
        "draft_note": "This page merges the published SEO case study with new LinkedIn Ads results. Client approval to be confirmed before publishing.",
    },
    {
        "slug": "cv-sheds-meta-ads",
        "name": "CV Sheds",
        "subtitle": "A Seasonal Meta Campaign That Reaches Shed Buyers Before the Busy Season",
        "tag": "Paid Social",
        "platform": "Meta Ads",
        "theme": "meta",
        "categories": ["paid-ads", "social-media"],
        "description": "How a seasonal Meta campaign for CV Sheds lifted click-through rate by 49% and cut cost per click by 41% across Central Victoria.",
        "excerpt": "CV Sheds builds custom steel sheds across Central Victoria. A seasonal Meta series with tight local targeting brought in more relevant visitors at a 41% lower cost per click.",
        "screen": ("Meta traffic campaign", "−41%", "cost per click"),
        "phone": ("CV Sheds", "Summer doesn't wait for you to be ready.", "See Details"),
        "challenge_ad": ("IMAGES/ads/cv-sheds-ad.jpg", "CV Sheds Facebook ad: Summer doesn't wait for you to be ready. Don't face summer without the right shed, with a See details button", "Summer Campaign single image ad: 3.12% click-through rate at $0.18 per click"),
        "facts": [("Industry", "Custom steel sheds"), ("Location", "Central Victoria"), ("Channels", "Facebook and Instagram (Meta Ads)"), ("Objective", "Website visits ahead of the build season"), ("Period", "February to November 2026")],
        "about": "CV Sheds designs and builds custom steel sheds across Central Victoria. Google Ads captures people already searching for a shed. Meta's job is different: reach property owners earlier and bring them to the website before the busy summer build season.",
        "challenge": [
            "The client's brief was a single line: plan a January campaign along the lines of “New Year, New Shed”, with the concept left to Digilari.",
            "The campaign needed to bring low-cost, relevant visitors to the site from the right towns, without spending on Melbourne or audiences unlikely to build a shed. The New Year's campaign finished at a 1.85% click-through rate and $0.44 per landing page view.",
        ],
        "solutions_intro": "Digilari turned the brief into a seasonal series and tightened every part of the targeting:",
        "solutions": [
            ("calendar", "A seasonal campaign series", "New Year's ran in three creative phases from February to May 2026. Summer Campaign 2026 followed in August with the same “prepare before the season” angle: protect vehicles, machinery, boats and caravans from summer sun and storms."),
            ("pin", "Local targeting around 22 towns", "Ads reached people within 25 miles of 22 Central Victorian towns, including Bendigo, Ballarat, Castlemaine and Echuca, with Melbourne excluded. Interests matched shed buyers: farming and machinery, boating, caravans and 4WD, DIY and home improvement, plus the Recently moved life event."),
            ("image", "Three formats tested", "Single image, carousel and video ads launched side by side. The single image won clearly (3.12% click-through rate at $0.18 per click), and Meta put 81% of September's budget behind it."),
            ("shield", "Cleaner placements and tracking", "Audience Network placements were excluded, Advantage+ creative enhancements were switched on, and UTM parameters were standardised so GA4 attributes Meta visits correctly."),
        ],
        "results_title": "Cheaper, More Relevant Visits Ahead of Summer",
        "results": [
            ("Click-through rate", "2.75%, against 1.85% on the previous seasonal campaign."),
            ("Cost per click", "$0.22, down from $0.37."),
            ("Cost per landing page view", "$0.37, down from $0.44, across 2,190 landing page views."),
            ("Best month", "September 2026, at a 3.63% click-through rate, $0.16 per click and $0.30 per landing page view."),
        ],
        "results_note": "This is an awareness and website traffic campaign. Enquiries are captured mainly through Google Ads, so this case study reports visits rather than leads.",
        "counters": [("+49%", "Click-Through Rate", "vs previous campaign"), ("−41%", "Cost per Click", "vs previous campaign"), ("−16%", "Cost per Page View", "vs previous campaign")],
        "stats": [("+49%", "Click-Through Rate", "vs previous campaign"), ("−41%", "Cost per Click", "vs previous campaign"), ("−16%", "Cost per Page View", "vs previous campaign")],
        "table": (["Metric (AUD)", "New Year's Phase 3: May 2026", "Summer Campaign: 6 Aug to 11 Nov 2026"], [
            ["Spend", "$945", "$812"], ["Impressions", "138,374", "135,766"], ["Clicks", "2,558", "3,737"], ["Click-through rate", "1.85%", "2.75%"],
            ["Cost per click", "$0.37", "$0.22"], ["Landing page views", "2,137", "2,190"], ["Cost per landing page view", "$0.44", "$0.37"]]),
        "source": "Source: Meta Ads (via Optmyzr). Figures in AUD.",
        "service": ("Facebook Advertising", "../../social-media-marketing/facebook-advertising-agency/index.html"),
    },
    {
        "slug": "cummins-social-media",
        "name": "Cummins",
        "subtitle": "Building a Social Presence for a Global Power Brand in the Philippines",
        "tag": "Social Media",
        "platform": "Organic Social",
        "theme": "organic",
        "categories": ["social-media"],
        "description": "How Digilari built and managed an industry-focused Facebook presence for Cummins Power Generation in the Philippines.",
        "excerpt": "Cummins had no established social presence in the Philippines. Digilari built an industry-focused Facebook programme that educated buyers, supported the local sales team and stayed on brand.",
        "screen": ("Facebook content", "4", "industry audiences"),
        "phone": ("Cummins", "Cummins genset or an OEM genset powered by Cummins?", "Learn More"),
        "facts": [("Industry", "Power generation"), ("Market", "Philippines"), ("Channel", "Facebook (organic)"), ("Focus", "Brand awareness, product education and sales support")],
        "about": "Cummins is a global power technology company. Its Philippine power generation team needed a Facebook presence that would introduce Cummins gensets to the businesses that rely on dependable power and support the local sales team's priorities.",
        "challenge": [
            "Cummins didn't have an established social media presence in the Philippines. It wanted to build brand awareness across key industries, particularly commercial, data centre and healthcare, while also supporting its sales efforts.",
            "Creative freedom was limited by established global brand templates and guidelines, so the content had to stand out through its topics and relevance rather than a new look.",
        ],
        "solutions_intro": "Digilari built a content programme around the industries that buy gensets and refined it with data:",
        "solutions": [
            ("layers", "Industry-specific content streams", "Content started with commercial businesses such as petrol stations, fast-food franchises, banks, malls and supermarkets, plus agricultural businesses that need power for irrigation, aerators and ventilation. Data centres and healthcare facilities were added as the programme grew."),
            ("chat", "Education alongside product", "Posts explained topics such as the difference between a Cummins Power Generation genset and an OEM genset powered by Cummins. Value-added, educational content ran alongside product and sales posts, so the page never felt like a sales pitch."),
            ("calendar", "A data-led posting schedule", "Daily single-image posts first established when target audiences were most active. Content topics were then tested against publishing days over three months, setting the posting schedule and message exposure for the following quarters."),
            ("video", "Formats that kept pace with the platform", "Reels were introduced as Meta began favouring video, keeping the content fresh and reducing creative fatigue while staying within Cummins' brand guidelines."),
        ],
        "results_title": "A Consistent, Industry-Focused Presence the Local Team Valued",
        "results": [
            ("New presence", "established and managed Cummins Power Generation's Facebook presence in the Philippines."),
            ("Wider reach into industry", "content expanded from general awareness to commercial, agricultural, data centre and healthcare audiences."),
            ("A tested schedule", "a structured, data-backed posting schedule used through to the end of the engagement."),
            ("Client feedback", "the Philippine team reported being happy with the campaign throughout, with no requests to change direction."),
        ],
        "counters": [("4", "Industry Audiences", "commercial, agriculture, data centres, healthcare"), ("3 mo", "Content Testing", "topics against publishing days")],
        "stats": [("4", "Industry Audiences", "content streams"), ("3 mo", "Content Testing", "before scheduling"), ("Reels", "Video Format", "added as Meta shifted")],
        "source": "Results are based on campaign management records and client feedback.",
        "service": ("Social Media Marketing", "../../social-media-marketing/index.html"),
    },
    {
        "slug": "cosmetics-plus-social-media",
        "name": "Cosmetics Plus",
        "subtitle": "Cleaning Up and Growing a Beauty Retailer's Social Presence",
        "tag": "Social Media",
        "platform": "Organic Social",
        "theme": "organic",
        "categories": ["social-media"],
        "description": "How Digilari consolidated Cosmetics Plus' Facebook pages, managed its reputation and grew engagement on Facebook and Instagram.",
        "excerpt": "Cosmetics Plus had duplicate Facebook pages and a backlog of negative reviews. Digilari consolidated its presence, set up a review process and built content that kept local stores top of mind.",
        "screen": ("Facebook + Instagram", "1", "official page"),
        "phone": ("Cosmetics Plus", "Self-care tips, piercing advice and new arrivals", "Visit Store"),
        "facts": [("Industry", "Beauty and piercing retail"), ("Channels", "Facebook and Instagram, with Pinterest maintained"), ("Focus", "Community management, reputation and local store visits")],
        "about": "Cosmetics Plus is a beauty retailer offering cosmetics, self-care products and in-store piercing services through its local stores. Social media supports both its online reputation and foot traffic to each store.",
        "challenge": [
            "When Cosmetics Plus came on board it had very little social media presence. Its Facebook page was largely inactive, and there were several duplicate pages and negative reviews that needed attention.",
            "Before the brand could grow online, its digital footprint had to be cleaned up, its pages consolidated and its customer feedback addressed.",
        ],
        "solutions_intro": "Digilari fixed the foundations first, then built a content programme on top of them:",
        "solutions": [
            ("layers", "Page clean-up and consolidation", "Claimed the duplicate and existing public business pages and consolidated them into one official Facebook page."),
            ("shield", "Reputation management", "Responded to the backlog of reviews and complaints, de-escalated where possible, and wrote a standard process for answering every type of review, from positive feedback to complaints."),
            ("chat", "Consistent community replies", "Created scripts for frequently asked questions and repeat enquiries, so replies stayed consistent across platforms before chatbots were widely available."),
            ("image", "Content beyond promotions", "Aligned social content with the promotional calendar, then filled the gaps with self-care tips, piercing education and product features. Reels moved from slideshows to creative videos with transitions, movement and music."),
            ("pin", "Focused channels and local promotion", "Narrowed active posting from Facebook, Instagram, X and Pinterest to Facebook and Instagram, while keeping Pinterest boards up to date. Paid piercing promotions reached people within 20 km of each store."),
        ],
        "results_title": "One Official Page, a Clear Process and More Engaging Content",
        "results": [
            ("Consolidated presence", "duplicate pages resolved into one official Facebook page."),
            ("Reputation", "the backlog of reviews and complaints answered, with a documented process for handling feedback from then on."),
            ("Community management", "consistent, scripted replies to common questions across platforms."),
            ("Content", "reworked Reels performed well with the algorithm and increased reach and impressions."),
        ],
        "counters": [("1", "Official Page", "from several duplicates"), ("20 km", "Local Targeting", "around each store")],
        "stats": [("1", "Official Page", "from duplicates"), ("2", "Core Channels", "Facebook and Instagram"), ("20 km", "Local Reach", "around each store")],
        "source": "Results are based on campaign management records.",
        "service": ("Social Media Marketing", "../../social-media-marketing/index.html"),
    },
]


def head(title: str, description: str, prefix: str) -> str:
    return f'''<!doctype html>
<html lang="en-AU">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex, nofollow">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(description, quote=True)}">
  <link rel="stylesheet" href="{prefix}social-media-marketing/styles.css">
  <link rel="stylesheet" href="{prefix}case-studies/case-studies.css">
  <script src="{prefix}case-studies/case-studies.js" defer></script>
</head>'''


def device(case: dict) -> str:
    label, value, caption = case["screen"]
    return (f'<div class="cs-device cs-theme-{case["theme"]}" aria-hidden="true"><div class="cs-screen">'
            f'<div class="cs-screen-bar"><span></span><span></span><span></span><em>{escape(case["platform"])}</em></div>'
            f'<div class="cs-screen-body"><p class="cs-screen-label">{escape(label)}</p><p class="cs-screen-client">{escape(case["name"])}</p>'
            f'<p class="cs-screen-value">{escape(value)}</p><p class="cs-screen-caption">{escape(caption)}</p>'
            '<div class="cs-screen-bars"><i></i><i></i><i></i><i></i><i></i><i></i></div></div></div>'
            '<div class="cs-stand"></div><div class="cs-base"></div></div>')


def phone(case: dict) -> str:
    brand, line, cta = case["phone"]
    return (f'<figure class="cs-phone-wrap"><div class="cs-phone cs-theme-{case["theme"]}" aria-hidden="true"><div class="cs-phone-notch"></div>'
            f'<div class="cs-post-head"><span class="cs-avatar">{escape(brand[:1])}</span><span><strong>{escape(brand)}</strong><small>{"Sponsored" if case["theme"] != "organic" else "2h"}</small></span></div>'
            f'<div class="cs-post-media"><p>{escape(line)}</p></div><div class="cs-post-cta"><span>{escape(case["platform"])}</span><b>{escape(cta)}</b></div>'
            '<div class="cs-post-lines"><i></i><i></i></div></div>'
            '<figcaption>Illustration based on the campaign messaging</figcaption></figure>')


def stat_row(stats) -> str:
    return '<div class="cs-stats">' + "".join(
        f'<div><strong>{escape(v)}</strong><span>{escape(label)}</span><small>{escape(sub)}</small></div>' for v, label, sub in stats) + "</div>"


def card(item: dict, prefix: str) -> str:
    cats = " ".join(item["categories"])
    if "slug" in item:
        url = f'{prefix}case-studies/{item["slug"]}/index.html'
        live = ""
    else:
        url = item["url"]
        live = ' data-live="true"'
    image = item.get("card_image") or item.get("image")
    visual = (f'<img class="cs-card-image" src="{escape(resolve(image, prefix), quote=True)}" alt="" loading="lazy" width="600" height="433">'
              if image else device(item))
    badge_text = item.get("badge") or ((item.get("tags") or [item.get("tag", "")])[-1] if "slug" in item else "")
    badge = f'<span class="cs-card-badge">{escape(badge_text)}</span>' if badge_text else ""
    return (f'<article class="cs-card" data-categories="{cats}"{live}><a class="cs-card-link" href="{escape(url, quote=True)}">'
            f'<div class="cs-card-visual">{visual}{badge}</div>{stat_row(item["stats"])}'
            f'<h3>{escape(item["name"])}</h3><p>{escape(item["excerpt"])}</p></a></article>')


def footer(prefix: str) -> str:
    return f'''  <section class="final-cta" aria-labelledby="final-title"><div class="wrap final-inner"><div><p class="eyebrow">Have a project in mind?</p><h2 id="final-title">Let's talk about your next result.</h2><p>Tell us what you need to grow. Email <a href="mailto:marketing@digilari.com.au">marketing@digilari.com.au</a> or call us to discuss the right channels for your business.</p></div><div class="final-actions"><a class="button button-light" href="https://digilari.com.au/contact-us/">Contact us <span aria-hidden="true">↗</span></a><a href="tel:1300859358">Or call 1300 859 358</a></div></div></section>
  </main>
  <footer class="site-footer"><div class="wrap footer-inner"><a href="https://digilari.com.au/" aria-label="Digilari Media home"><img src="{prefix}assets/dig-logo-c5.png" width="286" height="150" alt="Digilari Media"></a><p>Real campaigns. Measured results.</p><div><a href="{prefix}case-studies/index.html">Case studies</a><a href="{prefix}social-media-marketing/index.html">Social media</a><a href="https://digilari.com.au/contact-us/">Contact</a></div></div></footer>
  <div class="mobile-action"><a href="tel:1300859358">Call us</a><a href="https://digilari.com.au/contact-us/">Start a project <span aria-hidden="true">↗</span></a></div>
</body>
</html>
'''


def list_page() -> str:
    prefix = "../"
    filters = "".join(
        f'<button class="cs-filter{" is-active" if key == "all" else ""}" type="button" data-filter="{key}" aria-pressed="{"true" if key == "all" else "false"}">{label}</button>'
        for key, label in FILTERS)
    cards = "\n".join(card(c, prefix) for c in CASES + LIVE_CASES)
    return f'''{head("Case Studies | Digilari Media", "Digital marketing case studies from Digilari Media: SEO, CRO, paid ads and social media results for Australian businesses.", prefix)}
<body class="cs-page cs-list-page">
  <a class="skip-link" href="#main">Skip to content</a>
  {navigation(prefix + "social-media-marketing/", mockup_root=prefix, current_url=prefix + "case-studies/index.html")}
  <main id="main">
    <section class="cs-list-hero" aria-labelledby="cs-title"><div class="wrap">
      <h1 id="cs-title">Case Studies</h1>
      <div class="cs-filters" role="group" aria-label="Filter case studies">{filters}</div>
    </div></section>
    <section class="cs-list" aria-label="Case studies"><div class="wrap">
      <div class="cs-grid" data-cs-grid>
{cards}
      </div>
      <p class="cs-empty" hidden>No case studies match this filter yet.</p>
    </div></section>
{footer(prefix)}'''


def solution_groups(case: dict):
    if case.get("solution_groups"):
        return case["solution_groups"]
    return [(None, case["solutions_intro"], case["solutions"])]


def result_groups(case: dict):
    if case.get("result_groups"):
        return case["result_groups"]
    return [{"eyebrow": "Results", "title": case["results_title"], "items": case["results"], "note": case.get("results_note"),
             "counters": case["counters"], "table": case.get("table"), "source": case.get("source"),
             "ads": case.get("ads"), "timeline": case.get("timeline")}]


def table_html(table) -> str:
    head_cells, rows = table
    header = "".join(f'<th scope="col">{escape(c)}</th>' for c in head_cells)
    body = "".join("<tr>" + f'<th scope="row">{escape(r[0])}</th>' + "".join(f"<td>{escape(c)}</td>" for c in r[1:]) + "</tr>" for r in rows)
    return f'<div class="cs-table-block"><h3>Before and after</h3><div class="cs-table-wrap"><table><thead><tr>{header}</tr></thead><tbody>{body}</tbody></table></div></div>'


def local_images(case: dict) -> None:
    """Use Canva-exported mockups in case-studies/images/ when they exist."""
    if "slug" not in case:
        return
    monitor = OUT / "images" / f'{case["slug"]}-monitor.png'
    phone_image = OUT / "images" / f'{case["slug"]}-phone.png'
    if monitor.exists() and not case.get("image"):
        case["image"] = f'IMAGES/{monitor.name}'
    if phone_image.exists() and not case.get("challenge_image"):
        case["challenge_image"] = f'IMAGES/{phone_image.name}'


def resolve(url: str, prefix: str) -> str:
    return url.replace("IMAGES/", prefix + "case-studies/images/")


def detail_page(case: dict) -> str:
    prefix = "../../"
    name = escape(case["name"])
    tags = "".join(f'<span class="cs-tag">{escape(t)}</span>' for t in case.get("tags") or [case["tag"]])
    hero_visual = (f'<img class="cs-hero-image" src="{escape(resolve(case["image"], prefix), quote=True)}" alt="{name} website shown on a desktop screen" width="933" height="673">'
                   if case.get("image") else device(case))
    logo = f'<img class="cs-logo" src="{escape(case["logo"], quote=True)}" alt="{name} logo" loading="lazy">' if case.get("logo") else ""
    facts = "".join(f'<div><dt>{escape(k)}</dt><dd>{escape(v)}</dd></div>' for k, v in case["facts"])
    about_link = ""
    if case.get("about_link"):
        text, url = case["about_link"]
        about_link = f'<a class="cs-text-link" href="{escape(url, quote=True)}">{escape(text)} <span aria-hidden="true">↗</span></a>'
    challenge = "".join(
        f"<p><strong>{escape(item[0])}:</strong> {escape(item[1])}</p>" if isinstance(item, tuple) else f"<p>{escape(item)}</p>"
        for item in case["challenge"])
    if case.get("challenge_ad"):
        src, alt, caption = case["challenge_ad"]
        challenge_visual = (f'<figure class="cs-ad cs-ad-feature"><img src="{escape(resolve(src, prefix), quote=True)}" alt="{escape(alt, quote=True)}" loading="lazy">'
                            f'<figcaption>{escape(caption)}</figcaption></figure>')
    elif case.get("challenge_image"):
        challenge_visual = f'<img class="cs-challenge-image" src="{escape(resolve(case["challenge_image"], prefix), quote=True)}" alt="{name} website on a mobile phone" loading="lazy">'
    else:
        challenge_visual = phone(case)
    solutions = ""
    for heading, intro, items in solution_groups(case):
        boxes = "".join(
            f'<article class="cs-solution"><span class="cs-solution-icon" aria-hidden="true">{ICONS[icon]}</span><div><h3>{escape(title)}</h3><p>{escape(text)}</p></div></article>'
            for icon, title, text in items)
        group_head = f'<h3 class="cs-group-title">{escape(heading)}</h3>' if heading else ""
        solutions += f'<div class="cs-solution-group">{group_head}<p class="cs-solutions-intro">{escape(intro)}</p><div class="cs-solution-list">{boxes}</div></div>'
    results = ""
    for group in result_groups(case):
        items = "".join(f"<li><strong>{escape(label)}:</strong> {escape(text)}</li>" for label, text in group["items"])
        note = f'<p class="cs-results-note">{escape(group["note"])}</p>' if group.get("note") else ""
        counters = "".join(
            f'<div class="cs-counter"><span class="cs-counter-circle">{escape(v)}</span><strong>{escape(label)}</strong><span>{escape(sub)}</span></div>'
            for v, label, sub in group["counters"])
        table = table_html(group["table"]) if group.get("table") else ""
        timeline = ""
        if group.get("timeline"):
            steps = "".join(f"<li><strong>{escape(when)}</strong><span>{escape(text)}</span></li>" for when, text in group["timeline"])
            timeline = f'<div class="cs-timeline-block"><h3>What changed and when</h3><ol class="cs-timeline">{steps}</ol></div>'
        ads = ""
        if group.get("ads"):
            figures = "".join(
                f'<figure class="cs-ad"><img src="{escape(resolve(src, prefix), quote=True)}" alt="{escape(alt, quote=True)}" loading="lazy"><figcaption>{escape(caption)}</figcaption></figure>'
                for src, alt, caption in group["ads"])
            ads = f'<div class="cs-ads-block"><h3>{escape(group.get("ads_title", "The ads behind the results"))}</h3><div class="cs-ads cs-ads-{len(group["ads"])}">{figures}</div></div>'
        source = f'<p class="cs-source">{escape(group["source"])}</p>' if group.get("source") else ""
        results += (f'<div class="cs-result-group"><div class="cs-results-grid"><div class="cs-results-copy"><p class="cs-results-eyebrow">{escape(group["eyebrow"])}</p>'
                    f'<h2>{escape(group["title"])}</h2><ul>{items}</ul>{note}</div>'
                    f'<div class="cs-counters cs-counters-{len(group["counters"])}">{counters}</div></div>{ads}{timeline}{table}{source}</div>')
    services = case.get("services") or [case["service"]]
    actions = "".join(
        f'<a class="button{"" if i == 0 else " button-outline"}" href="{escape(url, quote=True)}">Explore {escape(label)} <span aria-hidden="true">↗</span></a>'
        for i, (label, url) in enumerate(services))
    others = [c for c in CASES if c["slug"] != case["slug"]][:3]
    other_cards = "\n".join(card(c, prefix) for c in others)
    draft = case.get("draft_note", "Client approval and final figures to be confirmed before publishing.")
    return f'''{head(case["name"] + " | Digilari Media", case["description"], prefix)}
<body class="cs-page cs-detail-page">
  <a class="skip-link" href="#main">Skip to content</a>
  {navigation(prefix + "social-media-marketing/", mockup_root=prefix, current_url=prefix + "case-studies/index.html")}
  <main id="main">
    <p class="cs-draft-note"><span>Mockup draft</span> {escape(draft)}</p>
    <section class="cs-hero" aria-labelledby="cs-title"><div class="wrap cs-hero-grid">
      <div class="cs-hero-copy">
        <nav class="cs-breadcrumb" aria-label="Breadcrumb"><a href="../index.html">Case Studies</a><span aria-hidden="true">/</span><span>{name}</span></nav>
        <h1 id="cs-title">{name}</h1>
        <p class="cs-subtitle">{escape(case["subtitle"])}</p>
        <div class="cs-tags">{tags}</div>
      </div>
      <div class="cs-hero-visual">{hero_visual}</div>
    </div></section>
    <section class="cs-about" aria-labelledby="about-title"><div class="wrap cs-about-grid">
      <div class="cs-facts-panel">{logo}<dl class="cs-facts">{facts}</dl></div>
      <div><h2 id="about-title">About {name}</h2><p>{escape(case["about"])}</p>{about_link}</div>
    </div></section>
    <section class="cs-challenge" aria-labelledby="challenge-title"><div class="wrap cs-challenge-grid">
      <div class="cs-challenge-visual">{challenge_visual}</div>
      <div><h2 id="challenge-title">Challenges</h2>{challenge}</div>
    </div></section>
    <section class="cs-solutions" aria-labelledby="solutions-title"><div class="wrap">
      <h2 id="solutions-title">Solutions</h2>
      {solutions}
    </div></section>
    <section class="cs-results" aria-label="Results"><div class="wrap">
      {results}
      <div class="cs-detail-actions">{actions}<a class="cs-text-link" href="../index.html">All case studies <span aria-hidden="true">↗</span></a></div>
    </div></section>
    <section class="cs-others" aria-labelledby="others-title"><div class="wrap">
      <h2 id="others-title">Other Case Studies</h2>
      <div class="cs-grid">
{other_cards}
      </div>
    </div></section>
{footer(prefix)}'''


def redirect_page(target: str, name: str) -> str:
    return f'''<!doctype html>
<html lang="en-AU">
<head>
  <meta charset="utf-8">
  <meta name="robots" content="noindex, nofollow">
  <meta http-equiv="refresh" content="0; url={target}">
  <link rel="canonical" href="{target}">
  <title>{escape(name)} | Digilari Media</title>
</head>
<body><p>This case study has moved: <a href="{target}">{escape(name)}</a>.</p></body>
</html>
'''


# Old case study slugs that should redirect to a new page, e.g. {"old-slug": ("new-slug", "Name")}.
MOVED = {}


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for case in CASES:
        local_images(case)
    (OUT / "index.html").write_text(list_page(), encoding="utf-8")
    print(OUT / "index.html")
    for case in CASES:
        target = OUT / case["slug"] / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(detail_page(case), encoding="utf-8")
        print(target)
    for old, (new, name) in MOVED.items():
        stub = OUT / old / "index.html"
        stub.parent.mkdir(parents=True, exist_ok=True)
        stub.write_text(redirect_page(f"../{new}/index.html", name), encoding="utf-8")
        print(stub, "-> redirect")
