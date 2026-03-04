# KeynoteData Website — Claude Quick Reference

## Project
keynotedata.com — B2B conference intelligence platform marketing site.
Static site generator. Python `build.py` → `output/` → GitHub Pages.

## Commands
```bash
python3 build.py                              # Build site
cd output && python3 -m http.server 8089      # Preview
cd output && git add -A && git commit -m "..." && git push origin gh-pages  # Deploy
```

## Key Files
- `HANDOFF.md` — Full brief, page plan, copy, build order
- `PROMPT.md` — New session copy-paste prompt
- `build.py` — Source of truth for all data and generators
- `brand/tokens.css` — CSS variables (DO NOT EDIT)
- `brand/brand-guidelines.md` — Full brand system
- `brand/head-snippet.html` — Copy into <head> of every page
- `docs/LANDING-PAGE-FORMULA.md` — Harry Dry 10-element formula
- `docs/copywriting-principles.md` — Harry Dry copywriting rules

## Brand
- Primary: Forest `#0F5132` | Accent: Sage `#5B9E7A` | BG: Mist `#F0F4F3`
- Heading: Plus Jakarta Sans | Body: Source Sans 3 | Mono: IBM Plex Mono
- Logo (light bg): `brand/logos/lockup-horizontal-primary.svg`
- Logo (dark bg): `brand/logos/lockup-horizontal-white.svg`

## Data Source
`/Users/rome/Documents/projects/conference-intel/data/conferences.db`
SQL reference: `/Users/rome/Documents/projects/conference-intel/viewer.py`

## Writing & SEO Rules

**Full reference: `CONTENT-BEST-PRACTICES.md`** — read before writing any copy or building any pages.

Quick rules:
- NEVER: false reframes ("not X, it's Y"), em-dashes for asides, "unlock/unleash/empower"
- ALWAYS: specific numbers, active voice, "call to value" CTAs ("See All 393 Speakers")
- Voice: Direct + analytical. Smart colleague, not sales pitch.
- Every page: unique title (50-60 chars), unique meta (120-160 chars), canonical to keynotedata.com
- FAQPage schema on every conference, category, and role page
- BreadcrumbList schema on all inner pages

## Build.py Architecture

ALL data and generation logic is inline in `build.py`. Never create separate data files.

Key data structures:
- `CONFERENCES` — conference dicts (name, slug, location, speakers, sponsors, sessions)
- `CONF_RELATED_PAGES` — slug → related page URLs (controls bidirectional linking)
- `ROUNDUP_PAGES` — "Best X Conferences" pages
- `ROLE_PAGES` — role-specific audience pages
- `CATEGORY_PAGES` — category/topic pages

Adding new pages: add entry to the relevant list, then update `CONF_RELATED_PAGES` so conference pages link back.

## Pre-Deploy Checklist

- [ ] `python3 build.py` runs without errors, page count correct
- [ ] New pages: unique title + meta description + canonical (keynotedata.com)
- [ ] FAQPage + BreadcrumbList schema on new pages
- [ ] `CONF_RELATED_PAGES` updated for any referenced conference pages
- [ ] New pages appear in sitemap.xml

Full checklist in `CONTENT-BEST-PRACTICES.md`.

## Reference Builds (for code patterns)
- `/Users/rome/Documents/projects/sultanofsaas/scripts/build.py`
- `/Users/rome/Documents/projects/b2bsalestools/build.py`
- `/Users/rome/Documents/projects/cannabisers/scripts/build.py`

## Hosting
GitHub Pages → keynotedata.com
Repo: `romelikethecity/keynotedata-website` (branch: gh-pages)
