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

## Writing Rules
- NEVER: false reframes ("not X, it's Y"), em-dashes for asides, "unlock/unleash/empower"
- ALWAYS: specific numbers, active voice, "call to value" CTAs
- Voice: Direct + analytical. Smart colleague, not sales pitch.

## Reference Builds (for code patterns)
- `/Users/rome/Documents/projects/sultanofsaas/scripts/build.py`
- `/Users/rome/Documents/projects/b2bsalestools/build.py`
- `/Users/rome/Documents/projects/cannabisers/scripts/build.py`

## Hosting
GitHub Pages → keynotedata.com
Repo: `romelikethecity/keynotedata-website` (branch: gh-pages)
