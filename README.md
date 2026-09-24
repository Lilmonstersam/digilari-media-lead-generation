# Digilari Media: Lead Generation Page Mockup

Static mockups of the rebuilt lead generation and account-based marketing pages for digilari.com.au, deployed to GitHub Pages via GitHub Actions.

## Structure

```
index.html                  The mockup page
account-based-marketing/    Separate ABM landing page, linked from the lead generation mockup
assets/                     Theme CSS/JS, fonts, images and client logos saved from the live page
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
- The ABM page uses email and telephone contact links. It does not submit a form.
