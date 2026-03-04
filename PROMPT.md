# KeynoteData Website — New Context Window Prompt

Copy-paste this into a new Claude session to start building the site.

---

I'm building the marketing website for **keynotedata.com** — a B2B conference intelligence platform. This is a standalone project at `/Users/rome/Documents/projects/keynotedata-website/`.

**Full brief:** Read `HANDOFF.md` before doing anything.
**Brand system:** Read `brand/brand-guidelines.md` and `brand/tokens.css`.
**Writing rules:** Read `docs/copywriting-principles.md` and `docs/LANDING-PAGE-FORMULA.md`.

## What this product is
A curated database of speakers, sponsors, and sessions from the top 20 B2B SaaS conferences (Dreamforce, INBOUND, SaaStr, MozCon, etc.). 887 speakers tracked, 487 sponsors, 1,256 sessions. ICP: event marketing managers + PR agencies doing speaker placement.

## Build pattern
Same static site generator pattern as my other sites:
- Single `build.py` script, all data inline
- Generates static HTML to `output/` directory
- Uses CSS variables from `brand/tokens.css` (DO NOT rewrite the tokens)
- GitHub Pages hosting at keynotedata.com

**Reference builds (read for code patterns):**
- `/Users/rome/Documents/projects/sultanofsaas/scripts/build.py`
- `/Users/rome/Documents/projects/b2bsalestools/build.py`

**Preview:** `python3 build.py && cd output && python3 -m http.server 8089`

## Build order
1. Set up `build.py` skeleton (constants, output dir, CSS/JS linking, sitemap)
2. Build `assets/css/styles.css` (base styles using tokens, nav, footer, cards)
3. Build the homepage (Harry Dry 10-element formula — see HANDOFF.md for full plan)
4. Build 13 conference pages (one per conference in data/conferences.json with speaker_count > 0)
5. Build SEO category pages (conference-speaker-database, b2b-conference-sponsors, etc.)
6. Build roundup pages (best-b2b-saas-conferences-2026, etc.)
7. About + Pricing pages
8. Sitemap + robots.txt
9. Deploy setup

## Data (pre-exported — use directly)
All data is already exported to `data/` as JSON files — load directly in `build.py`, no DB needed:
- `data/stats.json` — summary counts for hero metrics (887 speakers, 487 sponsors, 13 conferences, 1256 sessions)
- `data/conferences.json` — 13 conferences with speaker/sponsor/session counts
- `data/speakers.json` — 887 speakers (name, title, company, seniority, LinkedIn, conferences)
- `data/sponsors.json` — 487 sponsors (name, category, events_sponsored, conferences)
- `data/sessions.json` — 1,256 sessions with abstracts
- `data/speakers_by_conference.json` — {slug: [speakers]} for conference pages

## Key constraints
- Primary CTA = email capture. "Get early access" → email form → "See the Data"
- Show real data above the fold (speaker cards, actual names/companies)
- Brand: Forest green #0F5132 primary, Sage #5B9E7A accent, Mist #F0F4F3 background
- Fonts: Plus Jakarta Sans (headings) + Source Sans 3 (body) + IBM Plex Mono (data)
- NEVER use: false reframes ("not X, it's Y"), em-dashes for asides, "unlock/unleash/empower"

## Writing style rules (critical)
- Direct and analytical. No AI-sounding filler.
- Lead with specifics: "887 speakers across 13 conferences" not "thousands of data points"
- Every line of copy must pass: Can I visualize it? Can I falsify it? Can nobody else say this?
- "Call to value" CTAs: "See the Data" not "Sign Up", "Get the Intel" not "Get Started"

Start by reading HANDOFF.md, then read one of the reference build.py files to understand the pattern, then ask any clarifying questions before writing code.
