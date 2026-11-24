# Live export: Social Media Marketing page

Files for rebuilding digilari.com.au/social-media-marketing-smm/ in Elementor from the mockup.

- `smm-page-blocks.json`: one HTML block per page section (hero with the Contact Form 7 shortcode, proof strip, page nav, services, platforms, process, case studies, why Digilari, FAQs, final CTA). Each block goes in its own full-width Elementor container, wrapped in `<div class="dsmm">`.
- `smm-page.css`: the mockup styles scoped under `.dsmm`, for the page's Custom CSS.

Links to pages that are not live yet (platform subpages, new case studies) point to `#enquiry` or the existing case study URLs.

# Live export: Lead generation page

Files for updating digilari.com.au/lead-generation/ (post 18955) in Elementor. Built by `scripts/build_lead_export.py` from `index.html`.

- `lead-generation-plan.json`: settings changes for existing Elementor widgets and containers, new service boxes, new `dlg-*` sections as HTML blocks with their position in the page, elements to delete, and logo files to upload to the media library (`{{LOGO:file}}` placeholders).
- `lead-generation-page.css`: the mockup's lead generation styles for the page's Custom CSS. Header rules are left out because the site header is a global template.

Links to the ABM page point to `#audit` until that page is live.

# Live export: social media platform pages

`scripts/build_platform_export.py <slug> <platform>` exports a platform mockup (for example `facebook-advertising-agency facebook`) to `<slug>-blocks.json` and `<slug>-page.css`. Each block goes in its own full-width Elementor container wrapped in the `wrapper` div. The CSS is the live SMM page CSS plus `platform.css` scoped under `.dsmm`.
