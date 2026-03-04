# KeynoteData Brand System — Claude Code Reference

## Brand Identity
- **Product**: keynotedata.com — B2B conference intelligence platform
- **Positioning**: "Conference intelligence for B2B marketers" — credible, data-forward, approachable
- **Concept**: "The Signal" — data-forward SaaS meets research publication

## Logo
- **Icon**: Speaker microphone silhouette (no badge frame)
- **Wordmark**: "KeynoteData" in Plus Jakarta Sans 700, single word, camelCase
- **Lockup**: Mic icon + KeynoteData wordmark, horizontal primary layout
- **Dark mode lockup**: Mic in accent green (#5B9E7A), "Keynote" in light text, "Data" in accent green

### Logo Files
- `logos/icon-primary.svg` — Forest green mic on transparent
- `logos/icon-white.svg` — White mic on transparent (for dark/colored backgrounds)
- `logos/icon-accent.svg` — Sage green mic on transparent
- `logos/icon-black.svg` — Monochrome black mic
- `logos/lockup-horizontal-primary.svg` — Full horizontal lockup, primary
- `logos/lockup-horizontal-white.svg` — Full horizontal lockup, white
- `logos/lockup-horizontal-darkmode.svg` — Dark mode lockup with accent split
- `logos/lockup-stacked-primary.svg` — Vertical/stacked with tagline

### Logo Usage Rules
- Minimum clear space: 1x the width of the mic icon on all sides
- Minimum size: 24px height for icon, 120px width for full lockup
- Never rotate, stretch, recolor outside approved palette, or add effects
- On photography or busy backgrounds, use white variant with subtle shadow

## Color Palette

### Primary
| Name | Hex | Usage |
|------|-----|-------|
| Forest | `#0F5132` | Primary brand, CTAs, headings |
| Forest Dark | `#0A3D26` | Hover states, emphasis |
| Forest Light | `#E8F0EC` | Light tints, selected states |

### Accent
| Name | Hex | Usage |
|------|-----|-------|
| Sage | `#5B9E7A` | Links, highlights, secondary CTAs |
| Sage Hover | `#4A8B69` | Accent hover state |
| Sage 10% | `#5B9E7A1A` | Tag backgrounds, subtle highlights |

### Neutrals
| Name | Hex | Usage |
|------|-----|-------|
| Slate | `#2D3748` | Primary text |
| Gray | `#A0AEC0` | Muted text, placeholders |
| Light Gray | `#CBD5E0` | Disabled text |
| Mist | `#F0F4F3` | Page background |
| Ivory | `#FAFBFA` | Card background |
| Border | `#D4DDD8` | Borders, dividers |
| Border Light | `#E8EDEB` | Subtle dividers |

### Dark Mode
| Name | Hex | Usage |
|------|-----|-------|
| Charcoal | `#1A202C` | Background |
| Graphite | `#2D3748` | Card background |
| Dark Border | `#4A5568` | Borders |
| Light Text | `#E2E8F0` | Primary text |
| Muted Text | `#718096` | Secondary text |

### Status Colors
| Name | Hex | Usage |
|------|-----|-------|
| Success | `#38A169` | Verified, fresh data |
| Warning | `#D69E2E` | Stale data, attention needed |
| Error | `#E53E3E` | Errors, removed |
| Info | `#3182CE` | Informational |

## Typography

### Font Stack
```css
--font-heading: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
--font-body: 'Source Sans 3', -apple-system, BlinkMacSystemFont, sans-serif;
--font-mono: 'IBM Plex Mono', 'Menlo', 'Consolas', monospace;
```

### Google Fonts Load
```html
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&family=Source+Sans+3:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
```

### Type Scale
| Token | Size | Usage |
|-------|------|-------|
| `text-xs` | 12px | Mono tags, metadata, data labels |
| `text-sm` | 14px | Secondary body, captions, filter labels |
| `text-base` | 16px | Body text, descriptions |
| `text-lg` | 18px | Lead paragraphs, card body |
| `text-xl` | 20px | Section headers, speaker names |
| `text-2xl` | 24px | Card titles, conference names |
| `text-3xl` | 30px | Page subtitles |
| `text-4xl` | 36px | Page titles |
| `text-5xl` | 48px | Hero headlines |

### Weight Usage
- **800 ExtraBold**: Hero headlines only (heading font)
- **700 Bold**: Page titles, conference names, CTAs (heading font)
- **600 Semibold**: Section headers, speaker names, emphasis (heading or body font)
- **500 Medium**: Navigation, labels, metadata (body font)
- **400 Regular**: Body copy, descriptions, table cells (body font)

## Component Patterns

### Data Tables
- Header: heading font, 600 weight, primary color, uppercase, text-xs with letter-spacing
- Cells: body font, 400 weight, text-sm
- Numerical values: mono font, 400 weight
- Sortable indicator: accent color arrow
- Row hover: Forest Light (#E8F0EC) background

### Speaker Cards
- Name: heading font, 600 weight, text-xl, Slate
- Title/Company: body font, 400 weight, text-sm, Gray
- Conference count: mono font, 400 weight, text-xs, Accent
- Card: Ivory background, Border, radius-lg, shadow-sm

### Filter Chips / Tags
- Font: mono, 400 weight, text-xs
- Background: Accent 10% opacity
- Text: Primary color
- Border: Primary at 15% opacity
- Border radius: radius-full
- Padding: 4px 12px

### CTAs / Buttons
- Primary: Forest background, white text, heading font 600, radius-md
- Primary hover: Forest Dark background
- Secondary: transparent, Forest text, Forest border
- Ghost: transparent, Accent text

### Navigation
- Font: body, 500 weight, text-sm
- Active: Primary color, bottom border 2px
- Inactive: Gray color
- Hover: Slate color

## Favicon & Meta
- See `favicons/` directory for all assets
- See `head-snippet.html` for copy-paste HTML
- See `favicons/site.webmanifest` for PWA manifest
- See `tokens.css` for CSS custom properties

## File Structure
```
keynotedata-brand/
├── logos/
│   ├── icon-primary.svg
│   ├── icon-white.svg
│   ├── icon-accent.svg
│   ├── icon-black.svg
│   ├── lockup-horizontal-primary.svg
│   ├── lockup-horizontal-white.svg
│   ├── lockup-horizontal-darkmode.svg
│   └── lockup-stacked-primary.svg
├── favicons/
│   ├── favicon.ico
│   ├── favicon-16x16.png
│   ├── favicon-32x32.png
│   ├── favicon-48x48.png
│   ├── favicon-64x64.png
│   ├── favicon-128x128.png
│   ├── favicon-180x180.png
│   ├── favicon-192x192.png
│   ├── favicon-256x256.png
│   ├── favicon-512x512.png
│   ├── apple-touch-icon.png
│   ├── android-chrome-192x192.png
│   ├── android-chrome-512x512.png
│   ├── mstile-150x150.png
│   ├── og-image.png
│   ├── og-image-dark.png
│   ├── site.webmanifest
│   └── browserconfig.xml
├── tokens.css
├── head-snippet.html
└── CLAUDE.md
```
