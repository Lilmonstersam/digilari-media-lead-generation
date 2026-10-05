# Digilari Media: Combined Service Mockup

Static mockups of the lead generation, account-based marketing and social media services for digilari.com.au. All six service pages share the latest categorised SMM header and can be navigated from one mockup. The GitHub Pages workflow includes the complete site.

## Structure

```
index.html                  Lead generation entry point
account-based-marketing/    Separate ABM landing page, linked from the lead generation mockup
social-media-marketing/     SMM hub, LinkedIn, Instagram and Facebook advertising subpages
assets/                     Theme CSS/JS, fonts, images and client logos saved from the live page
assets/dig-shared.css/js     Shared categorised navigation and mobile accordions
assets/lead-page.css         Lead-generation typography and form styling
scripts/sync_header.py      Applies the latest SMM header to all six service pages
404.html                    Redirects unknown paths back to the mockup
robots.txt                  Blocks crawling (mockup duplicates live-site content)
.nojekyll                   Serve files as-is, no Jekyll processing
.github/workflows/deploy.yml  Build and deploy to GitHub Pages on every push to main
```

## Deploy

1. Repo **Settings > Pages > Build and deployment > Source: GitHub Actions** (the workflow also tries to enable this automatically).
2. Push to `main` or run the workflow manually from the **Actions** tab.
3. The live URL appears in the workflow summary: `https://<user>.github.io/digilari-media-lead-generation/`.

## Notes

- The page is `noindex, nofollow` and `robots.txt` disallows crawling so the mockup cannot compete with digilari.com.au in search.
- Forms, the chatbot and some Elementor chunks load from the live WordPress site or are disabled; they will not submit from the mockup.
- Account-based marketing links on the lead generation page open the ABM mockup in this repository.
- Our Capabilities > Growth & conversion links to Lead Generation and ABM. Paid & social media links to the SMM hub and all three platform pages. Each page marks its current service in the menu.
- Lead generation retains the ABM page's Red Hat type scale.
- SMM enquiry forms validate the fields and prepare a pre-filled email draft. They have no submission backend.
- Ahrefs research and case-study sources are saved in `social-media-marketing/SERP_NOTES.md`.
- The ABM enquiry form uses the same core fields as the lead generation page. Submitting it opens a pre-filled email draft addressed to Digilari; the visitor must send that email to complete the enquiry.

## Refresh the shared header

```sh
python3 scripts/sync_header.py
```

The navigation component is in `social-media-marketing/scripts/components.py`. The header script uses only the Python standard library and updates relative links for every page, including the legacy SMM filename.

To regenerate the SMM content components or platform pages, use these commands first (they require `lxml`), then synchronise the header:

```sh
python3 social-media-marketing/scripts/update_main_components.py
python3 social-media-marketing/scripts/build_platform_pages.py
python3 scripts/sync_header.py
```
