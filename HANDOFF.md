# KeynoteData.com — Website Build Handoff

## Project Brief

**Product:** keynotedata.com — B2B conference intelligence platform
**What it is:** A curated database of conference speakers, sponsors, and sessions for B2B SaaS events.
**Data:** 887 speakers, 487 sponsors, 1,256 sessions across 20 conferences (Dreamforce, INBOUND, SaaStr, MozCon, etc.)
**ICP:** Event marketing managers at B2B SaaS companies ($100K+ event budgets) + PR agencies doing speaker placement
**Goal:** Launch a marketing site with a landing page and SEO content to validate organic demand before investing further.

**Primary CTA:** Email capture / waitlist — collect emails to validate demand. "Get early access" or "See the data."

---

## Build Infrastructure

### Pattern
Same static site generator pattern used across all other projects:
- Single `build.py` script with all data inline
- Generates static HTML to `output/` directory
- No framework, no build tools, no dependencies beyond Python stdlib
- Inline CSS using `brand/tokens.css` variables (import tokens, don't rewrite them)
- GitHub Pages hosting at keynotedata.com

### File Structure (target)
```
keynotedata-website/
├── build.py                    ← ALL data + page generators (source of truth)
├── brand/
│   ├── tokens.css              ← CSS design tokens (DO NOT EDIT)
│   ├── head-snippet.html       ← Copy-paste <head> for every page
│   ├── brand-guidelines.md     ← Full brand system reference
│   ├── logos/                  ← SVG logo files
│   └── favicons/               ← All favicon sizes + OG images
├── assets/
│   ├── css/
│   │   ├── tokens.css          ← Symlink or copy from brand/tokens.css
│   │   └── styles.css          ← Site styles (built on top of tokens)
│   └── js/
│       └── main.js             ← Minimal JS (email capture, nav toggle)
├── docs/
│   ├── LANDING-PAGE-FORMULA.md ← Harry Dry 10-element formula
│   ├── copywriting-principles.md ← Harry Dry copywriting rules
│   └── seo-principles.md       ← SEO content strategy
├── output/                     ← Generated site (git ignored except for deploy)
├── HANDOFF.md                  ← This file
├── PROMPT.md                   ← Copy-paste prompt for new Claude sessions
└── CLAUDE.md                   ← Quick reference for Claude in this project
```

### Build & Preview Commands
```bash
cd /Users/rome/Documents/projects/keynotedata-website
python3 build.py
cd output && python3 -m http.server 8089
# Preview at http://localhost:8089/
```

### Hosting: GitHub Pages
```bash
# Setup (one time)
cd output && git init && git remote add origin git@github.com:romelikethecity/keynotedata-website.git
git checkout -b gh-pages

# Deploy
cd /Users/rome/Documents/projects/keynotedata-website
python3 build.py
cd output && git add -A && git commit -m "Build $(date +%Y-%m-%d)" && git push origin gh-pages

# DNS: Point keynotedata.com CNAME → romelikethecity.github.io
# Add CNAME file to output/ with content: keynotedata.com
```

### Data Source
The master database lives at `/Users/rome/Documents/projects/conference-intel/data/conferences.db`.
For the website build, extract data at build time or pre-export CSVs/JSON files from the DB.
Do NOT connect to the DB directly from the website — pre-bake all data into `build.py`.

---

## Brand System

**See:** `brand/brand-guidelines.md` for the full system. Key points:

### Identity
- **Concept:** "The Signal" — data-forward SaaS meets research publication
- **Logo:** Speaker mic silhouette + "KeynoteData" wordmark (Plus Jakarta Sans 700)
- **Primary logo:** `brand/logos/lockup-horizontal-primary.svg`
- **On dark backgrounds:** `brand/logos/lockup-horizontal-white.svg`
- **Standalone icon:** `brand/logos/icon-accent.svg` or `icon-black.svg`

### Colors
| Token | Hex | Use |
|-------|-----|-----|
| `--color-primary` | `#0F5132` | Forest green — CTAs, headings, nav |
| `--color-accent` | `#5B9E7A` | Sage — links, highlights, tags |
| `--color-bg` | `#F0F4F3` | Mist — page background |
| `--color-card` | `#FAFBFA` | Ivory — card backgrounds |
| `--color-text` | `#2D3748` | Slate — body text |

### Fonts
- **Headings:** Plus Jakarta Sans (600, 700, 800) — hero, titles, CTAs
- **Body:** Source Sans 3 (400, 500, 600) — copy, descriptions
- **Mono:** IBM Plex Mono (400, 500) — data values, tags, metadata

### Tone
Credible and approachable. Data-forward. Not flashy. Think: Clearbit meets a research publication.
NOT corporate/enterprise (that's Vendelux). NOT cheap/directory (that's ConferenceDatabase).

---

## Writing Style

**See:** `docs/copywriting-principles.md` and `docs/LANDING-PAGE-FORMULA.md`
**Also:** https://github.com/coreyhaines31/marketingskills (`skills/programmatic-seo`, `skills/content-strategy`)

### Hard Rules (never break these)
- **NEVER use false reframes:** No "not X, it's Y" / "isn't X. It's Y." / "less about X, more about Y." Just say what the thing IS. Directly.
- **Never use:** unlock, unleash, enhance, empower, supercharge, game-changer, paradigm shift
- **No em-dashes** for parenthetical asides. Use periods.
- **No passive voice.** Active, direct language only.
- **No "landing page words"** — if your competitor could say the same thing, rewrite it.

### Voice for KeynoteData
- Direct and analytical. Smart colleague, not a sales pitch.
- Use contractions. Write how you talk.
- Lead with specifics: "887 speakers across 20 B2B conferences" not "thousands of data points"
- Competitive framing: winners/losers, who's investing, who's missing
- Make the data tangible — speaker cards, sample tables, real names and companies

### Harry Dry Copywriting Rules (from `docs/copywriting-principles.md`)
1. **Can I visualize it?** Concrete beats abstract.
2. **Can I falsify it?** Specific and provable beats vague.
3. **Can nobody else say this?** If a competitor could say it, rewrite it.
4. Write with your eraser. Cut, then cut more.
5. "Call to value" not "call to action" — "See the Data" not "Sign Up"

---

## Landing Page Plan

Follow the Harry Dry 10-element formula from `docs/LANDING-PAGE-FORMULA.md`.

### Above the Fold

**Headline (option A — explain what you do, product is unique):**
> "Conference intelligence for B2B marketers."

**Or (option B — hook, addresses objection "I already know which conferences to attend"):**
> "You know which conferences to attend. Do you know who'll be in the room?"

**Subtitle (specific, introduces the product):**
> "KeynoteData tracks speakers, sponsors, and sessions across the top B2B SaaS conferences — so you can research before you budget, pitch before you apply, and target before you sponsor."

**Visual:** A real data preview — speaker cards or a data table showing actual speakers with names, titles, companies, and conference appearances. NOT an abstract illustration.

**Social Proof (metrics):**
- 887 speakers tracked
- 487 sponsors indexed
- 13 conferences with full data
- 1,256 sessions tagged by topic

**CTA:**
> "Get early access" [email input] → Button: "See the Data"
Sub-copy: "Free to start. No credit card."

---

### Below the Fold

**Section 1 — Features / Use Cases (3 cards):**

Card 1: **Event marketing managers**
> "Know which sponsors keep showing up — and which ones are new. Budget smarter."
Feature: Multi-event sponsor tracker with tier data.

Card 2: **PR agencies / speaker placement**
> "See who speaks at every conference in your space. Find the gaps. Pitch the right events."
Feature: Speaker database with conference appearances + LinkedIn.

Card 3: **Conference organizers / sponsors**
> "Benchmark your speaker roster. See who's speaking everywhere else."
Feature: Cross-conference speaker analysis.

**Section 2 — Sample Data Preview**
Real, browsable sample data. Speaker table: name / title / company / conferences spoken at / LinkedIn link.
CTA: "See all 887 speakers" → email gate.

**Section 3 — How It Works (3 steps)**
1. We scrape and verify speaker/sponsor data from 20+ B2B conferences
2. Enrich with LinkedIn profiles, seniority, and function tags
3. You search, filter, export — or get a custom data pull

**Section 4 — More Social Proof / Credibility**
- Conference list with logos (Dreamforce, INBOUND, SaaStr, MozCon, etc.)
- "Data updated after every conference cycle"

**Section 5 — FAQ**
- Q: How often is data updated? A: After each conference (typically 2x per year per event).
- Q: Can I export? A: Yes, CSV export included.
- Q: What conferences are covered? A: 20 now, growing to 50+.
- Q: Is there an API? A: Not yet — on the roadmap.

**Section 6 — 2nd CTA**
> "Stop guessing who'll be in the room."
[email input] → "Get Early Access"

**Section 7 — Founder's Note**
> "I built KeynoteData after spending $40K on conferences where I had no idea who was speaking or why they were there. The data existed — it just wasn't organized. Now it is."
— Rome, Founder

---

## SEO Page Plan

Target keywords for the actual ICP (event marketing managers, PR agencies, B2B conference sponsors).
NOT job-seeker keywords (those are in the existing 70-page export for audience sites).

### Conference Index Pages
One page per major conference. Target: "[Conference Name] speakers 2025", "[Conference] sponsors"
- /conferences/dreamforce/
- /conferences/inbound/
- /conferences/saastr/
- /conferences/mozcon/
- /conferences/b2b-marketing-exchange/
- /conferences/ (index)
~20 conference pages total (one per scraped conference)

Each page has:
- Conference overview (date, location, attendance, focus)
- Speaker list (top 10 visible, rest gated behind email)
- Sponsor list (top 10 visible)
- Related conferences
- CTA: "See full data — get early access"

### Category/Topic SEO Pages
- /conference-speaker-database/ (primary category page)
- /b2b-conference-sponsors/ (sponsor intelligence use case)
- /event-marketing-intelligence/ (broad category)
- /conference-speaking-opportunities/ (PR agency angle)
- /speaker-placement-strategy/ (PR agency content)
- /b2b-conference-data/ (data product angle)
- /conference-sponsorship-roi/ (thought leadership)
- /how-to-get-speaking-opportunities/ (top-of-funnel)

### Roundup / Comparison Pages
- /best-b2b-saas-conferences-2026/ (high intent, high volume)
- /best-b2b-marketing-conferences-2026/
- /best-revops-conferences-2026/
- /best-sales-conferences-2026/
- /best-ai-conferences-2026/

### Total Page Count Target
- 1 Homepage
- 1 About
- 1 Sample Data / Preview page
- 1 Pricing page
- 13 Conference pages (one per conference with data)
- 8 Category/topic pages
- 5 Roundup pages
= ~30 pages for launch

---

## Email Capture Setup

**Tool:** Beehiiv or a simple Formspree/Netlify form → export CSV → manual follow-up for now.
For launch, keep it simple: Formspree (free) POSTs to email. Upgrade to Beehiiv when list hits 50+.

```html
<!-- Formspree email capture -->
<form action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
  <input type="email" name="email" placeholder="your@company.com" required>
  <button type="submit">See the Data</button>
</form>
```

Or use a mailto: fallback for the very first version if Formspree isn't set up.

---

## Competitive Context

| Competitor | Price | What they have | Weakness |
|------------|-------|----------------|----------|
| Vendelux | $20K–$125K/yr | Attendee prediction, enterprise | Too expensive for SMB, no session data |
| ConferenceDatabase | $49/yr | Conference listings | Thin data, no speakers/sponsors |
| Kuration AI | $49–$400/mo | On-demand extraction | Manual/slow, not pre-built |
| **KeynoteData** | TBD ($49–$199/mo) | Speaker+sponsor+session DB | The whitespace |

**Positioning:** "The conference intelligence database for B2B marketers who can't afford Vendelux."

---

## Data Files (pre-exported — ready to use)

All data is pre-exported to `data/` as JSON. Load directly in `build.py` — no DB connection needed.

```
data/
├── stats.json               ← Summary counts (use for hero metrics)
├── conferences.json         ← 13 conferences with speaker/sponsor/session counts
├── speakers.json            ← 887 speakers with all fields
├── sponsors.json            ← 487 sponsors with event counts
├── sessions.json            ← 1,256 sessions with abstracts
└── speakers_by_conference.json  ← {conference_slug: [speaker list]}
```

### Stats (for homepage social proof)
- **887 speakers** tracked
- **605** with LinkedIn URLs (68%)
- **152** C-level speakers, **183** VP+
- **487 sponsors** indexed, **11** appearing at 2+ events
- **1,256 sessions** with abstracts
- **13 conferences** with full scraped data

### Conferences with data (build one page per row)
| Conference | Speakers | Sponsors | Sessions |
|------------|----------|----------|----------|
| INBOUND | 393 | 112 | 279 |
| Slush | 120 | 0 | 0 |
| LeadsCon | 88 | 26 | 0 |
| Spryng | 72 | 3 | 0 |
| Dreamforce | 70 | 0 | 910 |
| Sandler Summit | 54 | 0 | 18 |
| SaaStr Annual | 30 | 38 | 0 |
| ERE | 23 | 0 | 16 |
| MozCon | 16 | 0 | 0 |
| 6sense Breakthrough | 12 | 11 | 0 |
| OutBound Conference | 7 | 0 | 33 |
| SaaStock | 6 | 0 | 0 |
| Sales 3.0 | 1 | 104 | 0 |

To refresh from source: `/Users/rome/Documents/projects/conference-intel/data/conferences.db`
SQL reference: `/Users/rome/Documents/projects/conference-intel/viewer.py`

---

## Build Order (for new context window)

1. **Set up `build.py` skeleton** — constants, output directory, CSS/JS linking, sitemap generation
2. **Build `assets/css/styles.css`** — base styles using `tokens.css` variables, nav, footer, cards, tables
3. **Build the homepage** — full Harry Dry 10-element landing page with email capture
4. **Build 13 conference pages** — one per row in the table above, using `data/conferences.json`
5. **Build 8 category SEO pages** — written content + CTA
6. **Build 5 roundup pages** — "Best B2B Conferences 2026" etc.
7. **Build About and Pricing pages**
8. **Generate sitemap.xml and robots.txt**
9. **Deploy to GitHub Pages**

---

## Reference Links

- **Brand guidelines:** `brand/brand-guidelines.md`
- **CSS tokens:** `brand/tokens.css`
- **Head HTML snippet:** `brand/head-snippet.html`
- **Landing page formula:** `docs/LANDING-PAGE-FORMULA.md`
- **Copywriting principles:** `docs/copywriting-principles.md`
- **SEO/content strategy:** https://github.com/coreyhaines31/marketingskills
  - `skills/programmatic-seo` — keyword targeting, page structure, internal linking
  - `skills/content-strategy` — content hierarchy, pillar pages, cluster strategy
- **Data source:** `/Users/rome/Documents/projects/conference-intel/data/conferences.db`
- **Viewer (for SQL reference):** `/Users/rome/Documents/projects/conference-intel/viewer.py`
- **Similar builds for code reference:**
  - SultanOfSaaS: `/Users/rome/Documents/projects/sultanofsaas/scripts/build.py`
  - B2BSalesTools: `/Users/rome/Documents/projects/b2bsalestools/build.py`
  - Cannabisers: `/Users/rome/Documents/projects/cannabisers/scripts/build.py`
