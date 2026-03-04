#!/usr/bin/env python3
"""
Build script for keynotedata.com
B2B conference intelligence — speakers, sponsors, sessions.

Run:     python3 build.py
Preview: cd output && python3 -m http.server 8089
"""

import os
import json
import shutil
from datetime import datetime

# =============================================================================
# CONSTANTS
# =============================================================================

SITE_NAME = "KeynoteData"
SITE_URL = "https://keynotedata.com"
CURRENT_YEAR = 2026
BUILD_DATE = datetime.now().strftime("%Y-%m-%d")
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
BRAND_DIR = os.path.join(PROJECT_ROOT, "brand")
CSS_VERSION = "1"
FORMSPREE_ID = "xgolgepl"

ALL_PAGES = []  # Populated by write_page() for sitemap

# =============================================================================
# CONFERENCE METADATA (descriptions, not in JSON)
# =============================================================================

CONFERENCE_DESCRIPTIONS = {
    "inbound": "HubSpot's annual marketing and sales conference, drawing 25,000+ professionals to Boston each year. INBOUND covers content marketing, sales strategy, customer success, and GTM execution. One of the highest-signal conferences for B2B SaaS marketing teams.",
    "slush": "Helsinki's flagship startup and technology conference, bringing together 8,000+ founders, investors, and enterprise executives. Known for high-quality speakers and a curated attendee mix spanning Europe and North America.",
    "leadscon": "The demand generation and lead marketing conference, focused on performance marketing, lead quality, and digital acquisition. Draws marketing leaders from direct-to-consumer and B2B verticals.",
    "spryng": "A boutique B2B messaging conference organized by Wynter. 500 curated attendees, no exhibition floor, no vendor pitches. Known for unusually candid conversations about B2B positioning and messaging strategy.",
    "dreamforce": "Salesforce's flagship annual event — one of the largest software conferences in the world. 40,000+ attendees in San Francisco across four days of keynotes, breakouts, and partner sessions spanning sales, marketing, service, and AI.",
    "sandler-summit": "The annual gathering for the Sandler sales training community. Focused on sales methodology, skill development, and revenue leadership. 1,000+ sales professionals and managers from Sandler-trained organizations.",
    "saastr-annual": "The world's largest SaaS event, held in San Francisco. SaaStr Annual brings together 12,500+ SaaS founders, operators, and investors for three days of speaker sessions. Heavy on GTM, revenue, and product strategy.",
    "ere": "The ERE Recruiting Conference focuses on talent acquisition, sourcing, and HR innovation. 700+ recruiting practitioners and TA leaders from enterprise and mid-market organizations.",
    "mozcon": "The SEO and content marketing conference organized by Moz. Draws 1,500+ SEO practitioners and marketing leaders for two days of tactical sessions on search, content, and digital marketing.",
    "6sense-breakthrough": "6sense's annual customer conference, focused on account-based marketing, buyer intent data, and revenue intelligence. 1,000+ practitioners using 6sense's ABM platform.",
    "outbound-conference": "A sales conference focused on outbound prospecting, cold outreach, and pipeline generation. 800+ sales development and AE practitioners from B2B SaaS organizations.",
    "saastock": "Europe's premier SaaS conference, held in Dublin. SaaStock brings together 4,000+ founders, investors, and GTM leaders from the European SaaS ecosystem.",
    "sales-3-0": "Selling Power's Sales 3.0 Conference focuses on modern sales leadership, methodology, and AI-powered selling. An executive event for VPs and CROs.",
}

# Maps each conference to relevant roundup/category pages for internal linking
CONF_RELATED_PAGES = {
    "inbound":              [("/best-b2b-marketing-conferences-2026/", "Best B2B Marketing Conferences 2026"), ("/best-b2b-saas-conferences-2026/", "Best B2B SaaS Conferences 2026"), ("/best-content-marketing-conferences-2026/", "Best Content Marketing Conferences 2026"), ("/best-demand-gen-conferences-2026/", "Best Demand Gen Conferences 2026"), ("/conferences-for-event-marketers/", "Conferences for Event Marketers"), ("/conference-speaker-database/", "B2B Conference Speaker Database")],
    "slush":                [("/best-b2b-saas-conferences-2026/", "Best B2B SaaS Conferences 2026"), ("/best-saas-founder-conferences-2026/", "Best SaaS Founder Conferences 2026"), ("/conference-speaker-database/", "B2B Conference Speaker Database")],
    "leadscon":             [("/best-b2b-marketing-conferences-2026/", "Best B2B Marketing Conferences 2026"), ("/best-content-marketing-conferences-2026/", "Best Content Marketing Conferences 2026"), ("/best-demand-gen-conferences-2026/", "Best Demand Gen Conferences 2026"), ("/b2b-conference-data/", "B2B Conference Data")],
    "spryng":               [("/best-revops-conferences-2026/", "Best RevOps Conferences 2026"), ("/best-demand-gen-conferences-2026/", "Best Demand Gen Conferences 2026"), ("/conferences-for-event-marketers/", "Conferences for Event Marketers"), ("/conference-speaker-database/", "B2B Conference Speaker Database")],
    "dreamforce":           [("/best-b2b-saas-conferences-2026/", "Best B2B SaaS Conferences 2026"), ("/best-sales-conferences-2026/", "Best Sales Conferences 2026"), ("/conferences-for-vp-marketing/", "Conferences for VP of Marketing"), ("/conferences-for-chief-revenue-officer/", "Conferences for Chief Revenue Officers"), ("/b2b-conference-sponsors/", "B2B Conference Sponsors")],
    "sandler-summit":       [("/best-sales-conferences-2026/", "Best Sales Conferences 2026"), ("/conferences-for-chief-revenue-officer/", "Conferences for Chief Revenue Officers"), ("/conference-speaking-opportunities/", "Conference Speaking Opportunities")],
    "saastr-annual":        [("/best-b2b-saas-conferences-2026/", "Best B2B SaaS Conferences 2026"), ("/best-saas-founder-conferences-2026/", "Best SaaS Founder Conferences 2026"), ("/best-gtm-conferences-2026/", "Best GTM Conferences 2026"), ("/conferences-for-chief-revenue-officer/", "Conferences for Chief Revenue Officers"), ("/conference-speaker-database/", "B2B Conference Speaker Database")],
    "ere":                  [("/best-hr-tech-conferences-2026/", "Best HR Tech Conferences 2026"), ("/best-recruiting-conferences-2026/", "Best Recruiting Conferences 2026"), ("/b2b-conference-data/", "B2B Conference Data")],
    "mozcon":               [("/best-b2b-marketing-conferences-2026/", "Best B2B Marketing Conferences 2026"), ("/best-content-marketing-conferences-2026/", "Best Content Marketing Conferences 2026"), ("/conference-speaker-database/", "B2B Conference Speaker Database")],
    "6sense-breakthrough":  [("/best-b2b-marketing-conferences-2026/", "Best B2B Marketing Conferences 2026"), ("/best-demand-gen-conferences-2026/", "Best Demand Gen Conferences 2026"), ("/conferences-for-demand-gen/", "Conferences for Demand Gen"), ("/b2b-conference-sponsors/", "B2B Conference Sponsors")],
    "outbound-conference":  [("/best-sales-conferences-2026/", "Best Sales Conferences 2026"), ("/conferences-for-chief-revenue-officer/", "Conferences for Chief Revenue Officers"), ("/conference-speaking-opportunities/", "Conference Speaking Opportunities")],
    "saastock":             [("/best-b2b-saas-conferences-2026/", "Best B2B SaaS Conferences 2026"), ("/best-saas-founder-conferences-2026/", "Best SaaS Founder Conferences 2026"), ("/conference-speaker-database/", "B2B Conference Speaker Database")],
    "sales-3-0":            [("/best-sales-conferences-2026/", "Best Sales Conferences 2026"), ("/conference-speaking-opportunities/", "Conference Speaking Opportunities")],
}

# =============================================================================
# CSS (written to output/assets/css/styles.css)
# =============================================================================

STYLES_CSS = """/* =============================================
   KeynoteData — Site Styles
   Uses CSS custom properties from tokens.css
   ============================================= */

/* --- Reset --- */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
img { display: block; max-width: 100%; }
a { color: inherit; text-decoration: none; }
button { cursor: pointer; border: none; background: none; font-family: inherit; }
input { font-family: inherit; }
details > summary { list-style: none; }
details > summary::-webkit-details-marker { display: none; }

/* --- Base --- */
body {
  font-family: var(--font-body);
  font-size: var(--text-base);
  color: var(--color-text);
  background: var(--color-bg);
  line-height: 1.65;
}
h1, h2, h3, h4, h5, h6 {
  font-family: var(--font-heading);
  line-height: 1.2;
  color: var(--color-primary);
}
p { margin-bottom: var(--space-4); }
p:last-child { margin-bottom: 0; }
strong { font-weight: var(--weight-semibold); }

/* --- Layout --- */
.container { max-width: 1100px; margin: 0 auto; padding: 0 var(--space-6); }
.container-narrow { max-width: 720px; margin: 0 auto; padding: 0 var(--space-6); }
section { padding: var(--space-16) 0; }

/* --- Utilities --- */
.mono { font-family: var(--font-mono); }
.text-muted { color: var(--color-text-muted); }
.text-center { text-align: center; }
.tag {
  display: inline-flex; align-items: center;
  font-family: var(--font-mono); font-size: var(--text-xs); font-weight: var(--weight-regular);
  color: var(--color-primary); background: var(--color-accent-light);
  border: 1px solid rgba(15,81,50,0.15); border-radius: var(--radius-full); padding: 3px 10px;
}

/* --- Navigation --- */
.site-nav {
  position: sticky; top: 0; z-index: 100;
  background: #fff;
  border-bottom: 1px solid #E8EDEB;
  box-shadow: 0 1px 2px rgba(15,81,50,0.05);
}
.site-nav-inner {
  max-width: 1100px; margin: 0 auto; padding: 0 var(--space-6);
  height: 60px; display: flex; align-items: center; justify-content: space-between; gap: var(--space-8);
}
.site-logo { display: flex; align-items: center; gap: var(--space-2); flex-shrink: 0; }
.site-logo img { height: 28px; width: auto; }
.site-logo-text {
  font-family: var(--font-heading); font-size: var(--text-lg); font-weight: var(--weight-bold);
  color: #0F5132;
}
.site-nav-links { display: flex; align-items: center; gap: var(--space-6); }
.site-nav-links a {
  font-size: var(--text-sm); font-weight: var(--weight-medium);
  color: #718096; transition: color 0.15s;
}
.site-nav-links a:hover { color: #2D3748; }
.nav-cta {
  font-family: var(--font-heading); font-size: var(--text-sm); font-weight: var(--weight-semibold);
  color: #fff !important; background: var(--color-primary);
  border-radius: var(--radius-md); padding: 8px 16px; transition: background 0.15s;
}
.nav-cta:hover { background: var(--color-primary-dark) !important; }
.nav-toggle { display: none; flex-direction: column; gap: 5px; padding: 4px; }
.nav-toggle span { display: block; width: 22px; height: 2px; background: var(--color-text); border-radius: 2px; }

/* --- Hero --- */
.hero {
  background: var(--color-primary);
  color: #fff;
  padding: var(--space-16) 0 var(--space-12);
  overflow: hidden;
}
.hero-inner {
  max-width: 1100px; margin: 0 auto; padding: 0 var(--space-6);
  display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-12); align-items: center;
}
.hero-eyebrow {
  font-family: var(--font-mono); font-size: var(--text-xs); font-weight: var(--weight-regular);
  color: var(--color-accent); letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: var(--space-4);
}
.hero h1 {
  font-size: var(--text-5xl); font-weight: var(--weight-extrabold);
  color: #fff; line-height: 1.08; margin-bottom: var(--space-6);
}
.hero-subtitle {
  font-size: var(--text-lg); color: rgba(255,255,255,0.85); line-height: 1.6; margin-bottom: var(--space-8);
}
.hero-stats { display: flex; flex-wrap: wrap; gap: var(--space-4); margin-bottom: var(--space-8); align-items: flex-start; }
.hero-stat { display: flex; flex-direction: column; }
.hero-stat-number {
  font-family: var(--font-mono); font-size: var(--text-2xl); font-weight: var(--weight-medium);
  color: #fff; line-height: 1;
}
.hero-stat-label { font-size: var(--text-xs); color: rgba(255,255,255,0.6); margin-top: 3px; }
.stat-divider { width: 1px; height: 36px; background: rgba(255,255,255,0.2); align-self: center; }

/* --- Email Capture --- */
.email-form { display: flex; gap: var(--space-2); flex-wrap: wrap; }
.email-form input[type="email"] {
  flex: 1; min-width: 220px; padding: 12px 16px;
  font-size: var(--text-base); color: var(--color-text);
  background: #fff; border: 1px solid var(--color-border);
  border-radius: var(--radius-md); outline: none; transition: border-color 0.15s;
}
.email-form input[type="email"]:focus { border-color: var(--color-accent); }
.email-form input[type="email"]::placeholder { color: var(--color-text-muted); }
.btn-primary {
  font-family: var(--font-heading); font-size: var(--text-base); font-weight: var(--weight-semibold);
  color: #fff; background: var(--color-accent); border: none;
  border-radius: var(--radius-md); padding: 12px 24px; cursor: pointer; white-space: nowrap;
  transition: background 0.15s;
}
.btn-primary:hover { background: var(--color-accent-hover); }
.email-form-subtext { font-size: var(--text-sm); color: rgba(255,255,255,0.55); margin-top: var(--space-2); }

/* --- Hero Speaker Cards --- */
.hero-visual { display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-3); }
.speaker-card-hero {
  background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15);
  border-radius: var(--radius-lg); padding: var(--space-4);
  backdrop-filter: blur(4px); transition: transform 0.2s;
}
.speaker-card-hero:hover { transform: translateY(-2px); }
.speaker-card-header { display: flex; align-items: center; gap: var(--space-3); margin-bottom: var(--space-3); }
.speaker-avatar {
  width: 40px; height: 40px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-family: var(--font-heading); font-size: var(--text-lg); font-weight: var(--weight-bold);
  color: #fff; flex-shrink: 0;
}
.avatar-green { background: var(--color-accent); }
.avatar-dark { background: rgba(255,255,255,0.2); }
.avatar-sage { background: #4A8B69; }
.avatar-forest { background: #0A3D26; }
.speaker-card-name {
  font-family: var(--font-heading); font-size: var(--text-base); font-weight: var(--weight-semibold);
  color: #fff; line-height: 1.2;
}
.speaker-card-meta { font-size: var(--text-sm); color: rgba(255,255,255,0.7); line-height: 1.3; }
.speaker-card-badges { display: flex; flex-wrap: wrap; gap: var(--space-1); margin-top: var(--space-2); }
.conf-badge {
  font-family: var(--font-mono); font-size: 10px;
  color: var(--color-accent); background: rgba(91,158,122,0.18);
  border: 1px solid rgba(91,158,122,0.3); border-radius: var(--radius-full); padding: 2px 8px;
}

/* --- Section Titles --- */
.section-title { font-size: var(--text-4xl); font-weight: var(--weight-bold); color: var(--color-primary); margin-bottom: var(--space-4); }
.section-subtitle { font-size: var(--text-lg); color: var(--color-text-muted); max-width: 600px; line-height: 1.6; margin-bottom: var(--space-8); }

/* --- Use Cases --- */
.use-cases { background: var(--color-card); }
.use-cases-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--space-6); }
.use-case-card {
  background: var(--color-bg); border: 1px solid var(--color-border-light);
  border-radius: var(--radius-lg); padding: var(--space-6);
}
.use-case-icon { font-size: 28px; margin-bottom: var(--space-4); }
.use-case-card h3 {
  font-size: var(--text-xl); font-weight: var(--weight-semibold);
  color: var(--color-primary); margin-bottom: var(--space-2);
}
.use-case-card p { font-size: var(--text-sm); color: var(--color-text-muted); margin-bottom: var(--space-4); }
.use-case-feature { font-size: var(--text-sm); font-weight: var(--weight-medium); color: var(--color-accent); }

/* --- Data Tables --- */
.data-section { background: var(--color-bg); }
.data-table-wrapper {
  overflow-x: auto; border-radius: var(--radius-lg);
  border: 1px solid var(--color-border); box-shadow: var(--shadow-sm);
}
.data-table { width: 100%; border-collapse: collapse; background: var(--color-card); }
.data-table th {
  font-family: var(--font-heading); font-size: var(--text-xs); font-weight: var(--weight-semibold);
  color: var(--color-primary); text-transform: uppercase; letter-spacing: 0.06em;
  padding: 12px 16px; text-align: left; background: var(--color-primary-light);
  border-bottom: 1px solid var(--color-border);
}
.data-table td {
  font-size: var(--text-sm); color: var(--color-text);
  padding: 12px 16px; border-bottom: 1px solid var(--color-border-light); vertical-align: middle;
}
.data-table tr:last-child td { border-bottom: none; }
.data-table tr:hover td { background: var(--color-primary-light); }
.td-name { font-weight: var(--weight-semibold); color: var(--color-primary); }
.td-mono { font-family: var(--font-mono); font-size: var(--text-xs); color: var(--color-accent); }
.td-link { color: var(--color-accent); font-size: var(--text-xs); font-family: var(--font-mono); }
.td-link:hover { text-decoration: underline; }
.seniority-badge {
  font-family: var(--font-mono); font-size: 10px;
  color: var(--color-primary); background: var(--color-accent-light);
  border: 1px solid rgba(15,81,50,0.12); border-radius: var(--radius-full); padding: 2px 8px;
}

/* --- Data Gate (locked section) --- */
.data-gate {
  text-align: center; padding: var(--space-8) var(--space-4);
  background: linear-gradient(to bottom, transparent, var(--color-card) 40%);
  position: relative; margin-top: -60px;
}
.data-gate-inner {
  background: var(--color-card); border: 1px solid var(--color-border);
  border-radius: var(--radius-lg); padding: var(--space-6); max-width: 480px; margin: 0 auto;
  box-shadow: var(--shadow-md);
}
.data-gate-inner p { font-size: var(--text-sm); color: var(--color-text-muted); margin-bottom: var(--space-4); }
.data-gate-inner .email-form { justify-content: center; }
.data-gate-inner .btn-primary { background: var(--color-primary); }
.data-gate-inner .btn-primary:hover { background: var(--color-primary-dark); }

/* --- How It Works --- */
.how-it-works { background: var(--color-primary); color: #fff; }
.how-it-works .section-title { color: #fff; }
.how-it-works .section-subtitle { color: rgba(255,255,255,0.75); }
.steps-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--space-6); }
.step-card {
  background: rgba(255,255,255,0.07); border: 1px solid rgba(255,255,255,0.12);
  border-radius: var(--radius-lg); padding: var(--space-6);
}
.step-number {
  font-family: var(--font-mono); font-size: var(--text-4xl); font-weight: var(--weight-medium);
  color: rgba(255,255,255,0.15); line-height: 1; margin-bottom: var(--space-4);
}
.step-card h3 { font-size: var(--text-xl); font-weight: var(--weight-semibold); color: #fff; margin-bottom: var(--space-2); }
.step-card p { font-size: var(--text-sm); color: rgba(255,255,255,0.7); }

/* --- Conference Grid --- */
.conference-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: var(--space-4); margin-bottom: var(--space-8); }
.conf-card {
  background: var(--color-card); border: 1px solid var(--color-border);
  border-radius: var(--radius-lg); padding: var(--space-6);
  transition: box-shadow 0.2s, transform 0.2s; display: block;
}
.conf-card:hover { box-shadow: var(--shadow-md); transform: translateY(-2px); }
.conf-card-name {
  font-family: var(--font-heading); font-size: var(--text-xl); font-weight: var(--weight-semibold);
  color: var(--color-primary); margin-bottom: var(--space-2);
}
.conf-card-meta { font-size: var(--text-sm); color: var(--color-text-muted); margin-bottom: var(--space-6); }
.conf-card-stats { display: flex; gap: var(--space-6); }
.conf-stat { display: flex; flex-direction: column; }
.conf-stat-num {
  font-family: var(--font-mono); font-size: var(--text-lg); font-weight: var(--weight-medium);
  color: var(--color-text); line-height: 1;
}
.conf-stat-label { font-size: var(--text-xs); color: var(--color-text-muted); margin-top: 2px; }

/* --- FAQ --- */
.faq-section { background: var(--color-card); }
.faq-list { max-width: 720px; border-top: 1px solid var(--color-border-light); }
.faq-item { border-bottom: 1px solid var(--color-border-light); }
.faq-question {
  font-family: var(--font-heading); font-size: var(--text-base); font-weight: var(--weight-semibold);
  color: var(--color-text); padding: var(--space-5) 0; cursor: pointer;
  display: flex; justify-content: space-between; align-items: center; gap: var(--space-4);
}
.faq-question::after {
  content: '+'; font-family: var(--font-mono); font-size: var(--text-xl);
  font-weight: var(--weight-regular); color: var(--color-accent); flex-shrink: 0;
}
details[open] .faq-question::after { content: '\2212'; }
.faq-answer { padding: 0 0 var(--space-5); color: var(--color-text-muted); font-size: var(--text-sm); line-height: 1.65; }

/* --- CTA Section --- */
.cta-section { background: var(--color-primary-light); text-align: center; }
.cta-section h2 { font-size: var(--text-4xl); font-weight: var(--weight-bold); color: var(--color-primary); margin-bottom: var(--space-4); }
.cta-section p { font-size: var(--text-lg); color: var(--color-text-muted); margin-bottom: var(--space-8); max-width: 500px; margin-left: auto; margin-right: auto; }
.cta-form-wrap { display: flex; justify-content: center; }
.cta-form-wrap .email-form input[type="email"] { background: var(--color-card); }
.cta-form-wrap .btn-primary { background: var(--color-primary); }
.cta-form-wrap .btn-primary:hover { background: var(--color-primary-dark); }

/* --- Founder's Note --- */
.founders-section { background: var(--color-bg); }
.founders-note {
  max-width: 680px; margin: 0 auto; text-align: center;
  background: var(--color-card); border: 1px solid var(--color-border-light);
  border-radius: var(--radius-xl); padding: var(--space-8);
}
.founders-note blockquote {
  font-size: var(--text-lg); color: var(--color-text); line-height: 1.7;
  margin-bottom: var(--space-6); font-style: italic; border: none; padding: 0;
}
.founders-cite {
  font-family: var(--font-mono); font-size: var(--text-sm); color: var(--color-text-muted);
}

/* --- Footer --- */
.site-footer { background: var(--color-dark-bg); color: var(--color-dark-text); padding: var(--space-12) 0 var(--space-8); }
.footer-inner {
  max-width: 1100px; margin: 0 auto; padding: 0 var(--space-6);
  display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: var(--space-8);
}
.footer-brand-col {}
.footer-logo { display: flex; align-items: center; gap: var(--space-2); margin-bottom: var(--space-4); }
.footer-logo img { height: 22px; width: auto; }
.footer-logo-text {
  font-family: var(--font-heading); font-size: var(--text-base); font-weight: var(--weight-bold); color: #fff;
}
.footer-tagline { font-size: var(--text-sm); color: var(--color-dark-text-muted); line-height: 1.6; max-width: 260px; }
.footer-col h3 {
  font-family: var(--font-heading); font-size: var(--text-xs); font-weight: var(--weight-semibold);
  color: #fff; margin-bottom: var(--space-4); text-transform: uppercase; letter-spacing: 0.06em;
}
.footer-col ul { list-style: none; display: flex; flex-direction: column; gap: var(--space-2); }
.footer-col ul li a { font-size: var(--text-sm); color: var(--color-dark-text-muted); transition: color 0.15s; }
.footer-col ul li a:hover { color: var(--color-accent); }
.footer-bottom {
  max-width: 1100px; margin: var(--space-8) auto 0; padding: var(--space-6) var(--space-6) 0;
  border-top: 1px solid var(--color-dark-border);
  display: flex; justify-content: space-between; align-items: center; gap: var(--space-4); flex-wrap: wrap;
}
.footer-copyright { font-size: var(--text-xs); color: var(--color-dark-text-muted); font-family: var(--font-mono); }

/* --- Breadcrumb --- */
.breadcrumb { font-size: var(--text-sm); color: var(--color-text-muted); margin-bottom: var(--space-4); }
.breadcrumb a { color: var(--color-accent); }
.breadcrumb a:hover { text-decoration: underline; }
.breadcrumb span { margin: 0 6px; color: var(--color-border); }

/* --- Conference Page Header --- */
.conf-header { background: var(--color-primary); color: #fff; padding: var(--space-12) 0; }
.conf-header-eyebrow {
  font-family: var(--font-mono); font-size: var(--text-xs); color: var(--color-accent);
  letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: var(--space-3);
}
.conf-header h1 {
  font-size: var(--text-4xl); font-weight: var(--weight-bold); color: #fff; margin-bottom: var(--space-3);
}
.conf-header-desc { font-size: var(--text-base); color: rgba(255,255,255,0.8); max-width: 640px; line-height: 1.6; margin-bottom: var(--space-6); }
.conf-header-stats { display: flex; gap: var(--space-6); flex-wrap: wrap; }
.conf-header-stat { display: flex; flex-direction: column; }
.conf-header-stat-num {
  font-family: var(--font-mono); font-size: var(--text-3xl); font-weight: var(--weight-medium);
  color: #fff; line-height: 1;
}
.conf-header-stat-label { font-size: var(--text-xs); color: rgba(255,255,255,0.6); margin-top: 4px; }

/* --- Page Header (category/roundup) --- */
.page-header { background: var(--color-primary-light); padding: var(--space-12) 0; border-bottom: 1px solid var(--color-border); }
.page-header h1 { font-size: var(--text-4xl); font-weight: var(--weight-bold); color: var(--color-primary); margin-bottom: var(--space-3); }
.page-header p { font-size: var(--text-lg); color: var(--color-text-muted); max-width: 620px; line-height: 1.6; }

/* --- Prose --- */
.prose { font-size: var(--text-base); color: var(--color-text); line-height: 1.7; }
.prose h2 { font-size: var(--text-2xl); font-weight: var(--weight-semibold); color: var(--color-primary); margin-top: var(--space-8); margin-bottom: var(--space-4); }
.prose h3 { font-size: var(--text-xl); font-weight: var(--weight-semibold); color: var(--color-text); margin-top: var(--space-6); margin-bottom: var(--space-3); }
.prose ul, .prose ol { padding-left: var(--space-6); margin-bottom: var(--space-4); }
.prose li { margin-bottom: var(--space-2); }
.prose .highlight-box {
  background: var(--color-primary-light); border-left: 3px solid var(--color-primary);
  border-radius: 0 var(--radius-md) var(--radius-md) 0;
  padding: var(--space-4) var(--space-6); margin: var(--space-6) 0;
}

/* --- Related Conferences --- */
.related-confs { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: var(--space-3); margin-top: var(--space-4); }
.related-conf-card {
  background: var(--color-bg); border: 1px solid var(--color-border-light);
  border-radius: var(--radius-md); padding: var(--space-4); transition: border-color 0.15s;
}
.related-conf-card:hover { border-color: var(--color-accent); }
.related-conf-name { font-family: var(--font-heading); font-size: var(--text-base); font-weight: var(--weight-semibold); color: var(--color-primary); }
.related-conf-speakers { font-family: var(--font-mono); font-size: var(--text-xs); color: var(--color-text-muted); margin-top: 2px; }

/* --- Pricing Cards --- */
.pricing-cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--space-6); }
.pricing-card {
  background: var(--color-card); border: 1px solid var(--color-border);
  border-radius: var(--radius-xl); padding: var(--space-8); position: relative;
}
.pricing-card.featured { border-color: var(--color-primary); box-shadow: var(--shadow-lg); }
.pricing-badge {
  position: absolute; top: -14px; left: 50%; transform: translateX(-50%);
  background: var(--color-primary); color: #fff;
  font-family: var(--font-mono); font-size: var(--text-xs);
  padding: 4px 14px; border-radius: var(--radius-full); white-space: nowrap;
}
.pricing-card-name {
  font-family: var(--font-heading); font-size: var(--text-xl); font-weight: var(--weight-bold);
  color: var(--color-primary); margin-bottom: var(--space-2);
}
.pricing-card-price {
  font-family: var(--font-mono); font-size: var(--text-4xl); font-weight: var(--weight-medium);
  color: var(--color-text); line-height: 1; margin-bottom: var(--space-1);
}
.pricing-card-period { font-size: var(--text-sm); color: var(--color-text-muted); margin-bottom: var(--space-6); }
.pricing-features { list-style: none; padding: 0; display: flex; flex-direction: column; gap: var(--space-3); margin-bottom: var(--space-6); }
.pricing-features li { font-size: var(--text-sm); color: var(--color-text); padding-left: var(--space-6); position: relative; }
.pricing-features li::before { content: '✓'; position: absolute; left: 0; color: var(--color-success); font-weight: var(--weight-semibold); }
.btn-outline {
  display: block; width: 100%; text-align: center;
  font-family: var(--font-heading); font-size: var(--text-base); font-weight: var(--weight-semibold);
  padding: 12px 24px; border-radius: var(--radius-md);
  border: 2px solid var(--color-primary); color: var(--color-primary);
  background: transparent; cursor: pointer; transition: all 0.15s;
}
.btn-outline:hover { background: var(--color-primary); color: #fff; }
.btn-primary-block {
  display: block; width: 100%; text-align: center;
  font-family: var(--font-heading); font-size: var(--text-base); font-weight: var(--weight-semibold);
  padding: 12px 24px; border-radius: var(--radius-md);
  background: var(--color-primary); color: #fff; cursor: pointer; transition: background 0.15s;
}
.btn-primary-block:hover { background: var(--color-primary-dark); }

/* --- Responsive --- */
@media (max-width: 900px) {
  .hero-inner { grid-template-columns: 1fr; }
  .hero-visual { display: none; }
  .hero h1 { font-size: var(--text-4xl); }
  .use-cases-grid, .steps-grid { grid-template-columns: 1fr; }
  .footer-inner { grid-template-columns: 1fr 1fr; }
  .pricing-cards { grid-template-columns: 1fr; }
}
@media (max-width: 640px) {
  .site-nav-links {
    display: none; position: absolute; top: 60px; left: 0; right: 0;
    background: var(--color-card); border-bottom: 1px solid var(--color-border);
    flex-direction: column; padding: var(--space-4); gap: var(--space-4);
    box-shadow: var(--shadow-md);
  }
  .site-nav-links.open { display: flex; }
  .nav-toggle { display: flex; }
  .container { padding: 0 var(--space-4); }
  .container-narrow { padding: 0 var(--space-4); }
  .hero h1 { font-size: var(--text-3xl); }
  .email-form { flex-direction: column; }
  .email-form input[type="email"] { min-width: unset; }
  .footer-inner { grid-template-columns: 1fr; }
  .footer-bottom { flex-direction: column; text-align: center; }
  .conf-header-stats { gap: var(--space-4); }
  .section-title { font-size: var(--text-3xl); }
}
"""

# =============================================================================
# JS
# =============================================================================

MAIN_JS = """/* KeynoteData — main.js */
document.addEventListener('DOMContentLoaded', function() {
  const toggle = document.querySelector('.nav-toggle');
  const links = document.getElementById('nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', function() {
      links.classList.toggle('open');
    });
    document.addEventListener('click', function(e) {
      if (!toggle.contains(e.target) && !links.contains(e.target)) {
        links.classList.remove('open');
      }
    });
  }
});
"""

# =============================================================================
# FILE I/O
# =============================================================================

def write_page(rel_path, html):
    """Write HTML page to output dir. Tracks URL for sitemap."""
    path = os.path.join(OUTPUT_DIR, rel_path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    url_path = '/' + rel_path.replace('index.html', '').replace('\\', '/')
    ALL_PAGES.append(url_path)
    print(f"  + {rel_path}")


def load_data():
    """Load all JSON data files."""
    data = {}
    for fname in ['stats', 'conferences', 'speakers', 'sponsors', 'sessions', 'speakers_by_conference']:
        fp = os.path.join(DATA_DIR, f'{fname}.json')
        with open(fp, encoding='utf-8') as f:
            data[fname] = json.load(f)
    return data

# =============================================================================
# HTML HELPERS
# =============================================================================

LOGO_PRIMARY = '<img src="/logos/lockup-horizontal-primary.svg" alt="KeynoteData" height="28">'
LOGO_WHITE = '<img src="/logos/lockup-horizontal-white.svg" alt="KeynoteData" height="22">'

MIC_SVG = '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
<rect x="9" y="2" width="6" height="11" rx="3" fill="#5B9E7A"/>
<path d="M5 10a7 7 0 0014 0" stroke="#5B9E7A" stroke-width="2" stroke-linecap="round"/>
<line x1="12" y1="17" x2="12" y2="21" stroke="#5B9E7A" stroke-width="2" stroke-linecap="round"/>
<line x1="8" y1="21" x2="16" y2="21" stroke="#5B9E7A" stroke-width="2" stroke-linecap="round"/>
</svg>'''


def html_head(title, desc, canonical="/", og_title=None):
    og_t = og_title or title
    return f'''<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE_URL}{canonical}">
<link rel="icon" type="image/x-icon" href="/favicons/favicon.ico">
<link rel="icon" type="image/png" sizes="32x32" href="/favicons/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicons/favicon-16x16.png">
<link rel="apple-touch-icon" sizes="180x180" href="/favicons/apple-touch-icon.png">
<link rel="manifest" href="/favicons/site.webmanifest">
<meta name="theme-color" content="#0F5132">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&family=Source+Sans+3:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/tokens.css?v={CSS_VERSION}">
<link rel="stylesheet" href="/assets/css/styles.css?v={CSS_VERSION}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{og_t}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE_URL}/favicons/og-image.png">
<meta property="og:url" content="{SITE_URL}{canonical}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{og_t}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE_URL}/favicons/og-image.png">
<script type="application/ld+json">{{"@context":"https://schema.org","@graph":[{{"@type":"Organization","name":"{SITE_NAME}","url":"{SITE_URL}","logo":"{SITE_URL}/logos/lockup-horizontal-primary.svg","description":"B2B conference intelligence — speakers, sponsors, and sessions across the top B2B SaaS and marketing conferences."}},{{"@type":"WebSite","name":"{SITE_NAME}","url":"{SITE_URL}","potentialAction":{{"@type":"SearchAction","target":"{SITE_URL}/conference-speaker-database/?q={{search_term_string}}","query-input":"required name=search_term_string"}}}}]}}</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-GG8Y6BRDZ0"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-GG8Y6BRDZ0');</script>'''


def nav_html():
    return f'''<nav class="site-nav">
<div class="site-nav-inner">
<a href="/" class="site-logo">
{MIC_SVG}
<span class="site-logo-text">KeynoteData</span>
</a>
<div class="site-nav-links" id="nav-links">
<a href="/conferences/">Conferences</a>
<a href="/conference-speaker-database/">Speaker Database</a>
<a href="/b2b-conference-sponsors/">Sponsors</a>
<a href="/about/">About</a>
<a href="/pricing/">Pricing</a>
<a href="/#get-access" class="nav-cta">Get Early Access</a>
</div>
<button class="nav-toggle" aria-label="Menu">
<span></span><span></span><span></span>
</button>
</div>
</nav>'''


def footer_html():
    conf_links = '\n'.join([
        '<li><a href="/conferences/inbound/">INBOUND</a></li>',
        '<li><a href="/conferences/dreamforce/">Dreamforce</a></li>',
        '<li><a href="/conferences/saastr-annual/">SaaStr Annual</a></li>',
        '<li><a href="/conferences/mozcon/">MozCon</a></li>',
        '<li><a href="/conferences/slush/">Slush</a></li>',
        '<li><a href="/conferences/">All Conferences →</a></li>',
    ])
    cat_links = '\n'.join([
        '<li><a href="/conference-speaker-database/">Speaker Database</a></li>',
        '<li><a href="/b2b-conference-sponsors/">Sponsor Intelligence</a></li>',
        '<li><a href="/conference-speaking-opportunities/">Speaking Opportunities</a></li>',
        '<li><a href="/event-marketing-intelligence/">Event Marketing</a></li>',
    ])
    roundup_links = '\n'.join([
        '<li><a href="/best-b2b-saas-conferences-2026/">Best B2B SaaS Conferences</a></li>',
        '<li><a href="/best-b2b-marketing-conferences-2026/">Best Marketing Conferences</a></li>',
        '<li><a href="/best-sales-conferences-2026/">Best Sales Conferences</a></li>',
        '<li><a href="/about/">About</a></li>',
        '<li><a href="/pricing/">Pricing</a></li>',
    ])
    return f'''<footer class="site-footer">
<div class="footer-inner">
<div class="footer-brand-col">
<div class="footer-logo">{MIC_SVG}<span class="footer-logo-text">KeynoteData</span></div>
<p class="footer-tagline">Conference intelligence for B2B marketers. 887 speakers, 487 sponsors, 13 conferences — and growing.</p>
</div>
<div class="footer-col">
<h3>Conferences</h3>
<ul>{conf_links}</ul>
</div>
<div class="footer-col">
<h3>Intelligence</h3>
<ul>{cat_links}</ul>
</div>
<div class="footer-col">
<h3>Resources</h3>
<ul>{roundup_links}</ul>
</div>
</div>
<div class="footer-bottom">
<p class="footer-copyright">&copy; {CURRENT_YEAR} KeynoteData. All rights reserved.</p>
<p class="footer-copyright">Data updated {BUILD_DATE}.</p>
</div>
</footer>
<script src="/assets/js/main.js"></script>'''


def email_form(cta_text="See the Data", input_placeholder="your@company.com", form_class=""):
    return f'''<form action="https://formspree.io/f/{FORMSPREE_ID}" method="POST" class="email-form {form_class}">
<input type="text" name="_gotcha" style="display:none" tabindex="-1" autocomplete="off">
<input type="email" name="email" placeholder="{input_placeholder}" required>
<button type="submit" class="btn-primary">{cta_text}</button>
</form>'''


def breadcrumb_html(crumbs):
    """crumbs: list of (label, url) — last item is current page (no url)."""
    parts = []
    for i, (label, url) in enumerate(crumbs):
        if url and i < len(crumbs) - 1:
            parts.append(f'<a href="{url}">{label}</a>')
        else:
            parts.append(f'<span class="crumb-current">{label}</span>')
    return '<nav class="breadcrumb" aria-label="Breadcrumb">' + '<span> / </span>'.join(parts) + '</nav>'


def seniority_label(tier):
    labels = {
        'c_level': 'C-Level',
        'vp': 'VP',
        'director': 'Director',
        'head_of': 'Head of',
        'manager': 'Manager',
        'individual_contributor': 'IC',
    }
    return labels.get(tier, tier.replace('_', ' ').title() if tier else '')


def speaker_row_html(s, show_linkedin=True):
    conf_list = s.get('conferences', '') or ''
    li_cell = ''
    if show_linkedin and s.get('linkedin_url'):
        li_cell = f'<a href="{s["linkedin_url"]}" class="td-link" target="_blank" rel="noopener">LinkedIn ↗</a>'
    else:
        li_cell = '<span class="text-muted">—</span>'
    tier_label = seniority_label(s.get('seniority_tier', ''))
    tier_html = f'<span class="seniority-badge">{tier_label}</span>' if tier_label else ''
    return f'''<tr>
<td class="td-name">{s.get("name","")}</td>
<td>{s.get("title","") or "<span class='text-muted'>—</span>"}</td>
<td>{s.get("company","") or "<span class='text-muted'>—</span>"}</td>
<td>{tier_html}</td>
<td class="td-mono">{conf_list}</td>
<td>{li_cell}</td>
</tr>'''


def speaker_table_html(speakers, max_rows=12):
    rows = ''.join(speaker_row_html(s) for s in speakers[:max_rows])
    return f'''<div class="data-table-wrapper">
<table class="data-table">
<thead><tr>
<th>Name</th><th>Title</th><th>Company</th><th>Level</th><th>Conference(s)</th><th>LinkedIn</th>
</tr></thead>
<tbody>{rows}</tbody>
</table>
</div>'''


def hero_speaker_card(name, title, company, conferences_list, avatar_class="avatar-green"):
    initial = name[0].upper() if name else "S"
    badges = ''.join(f'<span class="conf-badge">{c.strip()}</span>' for c in conferences_list[:2])
    return f'''<div class="speaker-card-hero">
<div class="speaker-card-header">
<div class="speaker-avatar {avatar_class}">{initial}</div>
<div>
<div class="speaker-card-name">{name}</div>
<div class="speaker-card-meta">{title}</div>
</div>
</div>
<div class="speaker-card-meta" style="margin-bottom:8px;color:rgba(255,255,255,0.55);font-size:12px;">{company}</div>
<div class="speaker-card-badges">{badges}</div>
</div>'''

# =============================================================================
# HOMEPAGE
# =============================================================================

def build_homepage(data):
    stats = data['stats']
    speakers = data['speakers']

    # Top 4 hero speakers (multi-conference)
    hero_speakers = speakers[:4]
    avatar_classes = ['avatar-green', 'avatar-sage', 'avatar-forest', 'avatar-dark']
    hero_cards = ''.join(
        hero_speaker_card(
            s['name'], s.get('title',''), s.get('company',''),
            s.get('conferences','').split(',') if s.get('conferences') else [],
            avatar_classes[i % 4]
        )
        for i, s in enumerate(hero_speakers)
    )

    # Stats
    stats_html = f'''<div class="hero-stats">
<div class="hero-stat">
<span class="hero-stat-number">{stats["total_speakers"]:,}</span>
<span class="hero-stat-label">Speakers tracked</span>
</div>
<div class="stat-divider"></div>
<div class="hero-stat">
<span class="hero-stat-number">{stats["total_sponsors"]:,}</span>
<span class="hero-stat-label">Sponsors indexed</span>
</div>
<div class="stat-divider"></div>
<div class="hero-stat">
<span class="hero-stat-number">{stats["conferences_with_data"]}</span>
<span class="hero-stat-label">Conferences with full data</span>
</div>
<div class="stat-divider"></div>
<div class="hero-stat">
<span class="hero-stat-number">{stats["total_sessions"]:,}</span>
<span class="hero-stat-label">Sessions tagged</span>
</div>
</div>'''

    # Sample data table (top 12 speakers)
    table_html = speaker_table_html(speakers, max_rows=12)

    # Conference grid (only conferences with speaker_count > 0)
    confs_with_data = [c for c in data['conferences'] if c['speaker_count'] > 0]
    conf_cards = ''
    for c in confs_with_data[:9]:
        loc = c.get('city') or c.get('country') or 'Virtual'
        meta = f"{loc} · {c.get('typical_attendees', 0):,} attendees"
        conf_cards += f'''<a href="/conferences/{c['slug']}/" class="conf-card">
<div class="conf-card-name">{c['name']}</div>
<div class="conf-card-meta">{meta}</div>
<div class="conf-card-stats">
<div class="conf-stat">
<span class="conf-stat-num">{c["speaker_count"]}</span>
<span class="conf-stat-label">speakers</span>
</div>
{"<div class='conf-stat'><span class='conf-stat-num'>" + str(c['sponsor_count']) + "</span><span class='conf-stat-label'>sponsors</span></div>" if c.get('sponsor_count') else ""}
{"<div class='conf-stat'><span class='conf-stat-num'>" + str(c['session_count']) + "</span><span class='conf-stat-label'>sessions</span></div>" if c.get('session_count') else ""}
</div>
</a>'''

    # FAQ
    faqs = [
        ("How often is the data updated?", "We refresh the database after each conference cycle — typically twice a year per event. Our scrapers run on a schedule, and every record is reviewed before it goes into the database."),
        ("What conferences are covered?", f"We have full data on {stats['conferences_with_data']} conferences today, including INBOUND, Dreamforce, SaaStr Annual, MozCon, Slush, LeadsCon, and more. We're tracking {stats['total_conferences']} conferences total and adding data as conferences publish their speaker lineups."),
        ("Can I export the data?", "Yes. CSV export is included on all paid plans. You can export speaker lists, sponsor rosters, and session data filtered by conference, seniority, function, or topic."),
        ("What data is included for each speaker?", f"Name, title, company, seniority tier (C-level, VP, Director, etc.), function category, LinkedIn URL (available for {stats['speakers_with_linkedin']} of {stats['total_speakers']} speakers), and every conference they've spoken at."),
        ("Is there an API?", "Not yet. It's on the roadmap. For now, all data is available via CSV export or custom data pulls. If you need API access, reach out — we're working with early customers to scope the requirements."),
        ("How is this different from just looking at conference websites?", "Conference sites list speakers per event, with no cross-conference view. KeynoteData lets you see who speaks everywhere, track sponsor patterns across events, and identify the speakers who keep showing up — all in one searchable, exportable database."),
    ]
    faq_items = ''.join(
        f'<details class="faq-item"><summary class="faq-question">{q}</summary><div class="faq-answer">{a}</div></details>'
        for q, a in faqs
    )
    faq_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]
    })

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
{html_head(
    title="KeynoteData — Conference Intelligence for B2B Marketers",
    desc="Track speakers, sponsors, and sessions across the top B2B SaaS conferences. 887 speakers, 487 sponsors, 13 conferences with full data.",
    canonical="/"
)}
<script type="application/ld+json">{faq_schema}</script>
</head>
<body>
{nav_html()}

<!-- HERO -->
<section class="hero" id="get-access">
<div class="hero-inner">
<div class="hero-content">
<div class="hero-eyebrow">B2B Conference Intelligence</div>
<h1>Conference websites show you the agenda. KeynoteData shows you who's in the room.</h1>
<p class="hero-subtitle">Filter speakers by conference, seniority, and company. Track which sponsors keep showing up. Export everything. Research before you spend.</p>
{stats_html}
{email_form("See the Data")}
<p class="email-form-subtext">Free to start. No credit card.</p>
</div>
<div class="hero-visual">{hero_cards}</div>
</div>
</section>

<!-- USE CASES -->
<section class="use-cases">
<div class="container">
<h2 class="section-title">Who uses KeynoteData</h2>
<p class="section-subtitle">Three teams that can't afford to walk in blind. Which one is yours?</p>
<div class="use-cases-grid">

<div class="use-case-card">
<div class="use-case-icon">📊</div>
<h3>Event Marketing Managers</h3>
<p>Know which sponsors keep showing up — and which ones are new. See who's speaking before you commit your budget. Stop flying blind on $50K+ conference decisions.</p>
<p class="use-case-feature">Multi-event sponsor tracker with tier data. Speaker seniority breakdowns per conference.</p>
</div>

<div class="use-case-card">
<div class="use-case-icon">🎤</div>
<h3>PR Agencies &amp; Speaker Placement</h3>
<p>See who speaks at every conference in your space. Find the gaps — conferences your client's competitors are missing. Pitch the right events with data, not guesswork.</p>
<p class="use-case-feature">Cross-conference speaker database with LinkedIn. {stats["c_level_speakers"]} C-level and {stats["vp_and_above"]} VP+ speakers tracked.</p>
</div>

<div class="use-case-card">
<div class="use-case-icon">🏆</div>
<h3>Conference Sponsors &amp; Organizers</h3>
<p>Benchmark your speaker roster against competing events. Track which brands are sponsoring your competitors. Know the full landscape before you set your strategy.</p>
<p class="use-case-feature">Cross-conference sponsor analysis. {stats["multi_event_sponsors"]} sponsors appearing at 2+ events tracked.</p>
</div>

</div>
</div>
</section>

<!-- SAMPLE DATA -->
<section class="data-section">
<div class="container">
<h2 class="section-title">The data looks like this</h2>
<p class="section-subtitle">Real speakers. Real companies. Real conference appearances. This is the actual database.</p>
{table_html}
<div class="data-gate">
<div class="data-gate-inner">
<p>Showing 12 of {stats["total_speakers"]:,} speakers. See the full database — filtered by conference, seniority, company, or function.</p>
{email_form("Get Full Access", "your@company.com")}
</div>
</div>
</div>
</section>

<!-- THREE THINGS YOU'LL KNOW -->
<section class="how-it-works">
<div class="container">
<h2 class="section-title">Three things you'll know before anyone else</h2>
<p class="section-subtitle">This is what the data actually tells you.</p>
<div class="steps-grid">
<div class="step-card">
<div class="step-number">01</div>
<h3>Which target accounts have speakers at your next conference</h3>
<p>Match the speaker roster against your ICP before you commit the budget. Know who's in the room — by company, title, and seniority — before you book the sponsorship.</p>
</div>
<div class="step-card">
<div class="step-number">02</div>
<h3>Which sponsors keep showing up</h3>
<p>{stats["multi_event_sponsors"]} companies sponsor 2+ events in our database. That's not coincidence — that's where your competitors are spending. Know the pattern before you set your strategy.</p>
</div>
<div class="step-card">
<div class="step-number">03</div>
<h3>What topics the audience actually cares about</h3>
<p>{stats["total_sessions"]:,} sessions tagged by track and format across {stats["conferences_with_data"]} conferences. See what's trending, what's saturated, and where the gaps are.</p>
</div>
</div>
</div>
</section>

<!-- CONFERENCES COVERED -->
<section class="data-section">
<div class="container">
<h2 class="section-title">Conferences in the database</h2>
<p class="section-subtitle">214 conferences tracked. 13 with full speaker and sponsor data — and growing.</p>
<div class="conference-grid">{conf_cards}</div>
<div style="text-align:center;">
<a href="/conferences/" style="font-family:var(--font-heading);font-weight:var(--weight-semibold);color:var(--color-primary);font-size:var(--text-sm);">View all 13 conferences with full data →</a>
</div>
</div>
</section>

<!-- FAQ -->
<section class="faq-section">
<div class="container">
<h2 class="section-title">Questions</h2>
<div class="faq-list">{faq_items}</div>
</div>
</section>

<!-- 2ND CTA -->
<section class="cta-section">
<div class="container">
<h2>Stop guessing who'll be in the room.</h2>
<p>887 speakers. 487 sponsors. 13 conferences. The data exists — now it's organized.</p>
<div class="cta-form-wrap">{email_form("Get Early Access")}</div>
</div>
</section>

<!-- FOUNDER'S NOTE -->
<section class="founders-section">
<div class="container">
<div class="founders-note">
<blockquote>"I built KeynoteData after spending tens of thousands of dollars on conferences where I had no idea who was speaking or why they were there. The data existed — scattered across conference websites, LinkedIn, and speaker directories. I just organized it."</blockquote>
<cite>— Rome, Founder</cite>
</div>
</div>
</section>

{footer_html()}
</body>
</html>'''

    write_page('index.html', html)

# =============================================================================
# CONFERENCE INDEX PAGE
# =============================================================================

def build_conference_index(data):
    confs_with_data = [c for c in data['conferences'] if c['speaker_count'] > 0]
    confs_with_data.sort(key=lambda c: c['speaker_count'], reverse=True)

    cards = ''
    for c in confs_with_data:
        loc_parts = [p for p in [c.get('city'), c.get('country')] if p]
        location = ', '.join(loc_parts) if loc_parts else 'International'
        attendees = f"{c.get('typical_attendees',0):,} attendees" if c.get('typical_attendees') else ''
        meta = ' · '.join(filter(None, [location, attendees]))
        cat_tag = c.get('category','').replace('-',' ').title()
        stat_parts = []
        if c['speaker_count']:
            stat_parts.append(f'<div class="conf-stat"><span class="conf-stat-num">{c["speaker_count"]}</span><span class="conf-stat-label">speakers</span></div>')
        if c.get('sponsor_count'):
            stat_parts.append(f'<div class="conf-stat"><span class="conf-stat-num">{c["sponsor_count"]}</span><span class="conf-stat-label">sponsors</span></div>')
        if c.get('session_count'):
            stat_parts.append(f'<div class="conf-stat"><span class="conf-stat-num">{c["session_count"]}</span><span class="conf-stat-label">sessions</span></div>')
        cards += f'''<a href="/conferences/{c['slug']}/" class="conf-card">
<div class="conf-card-name">{c['name']}</div>
<div class="conf-card-meta">{meta} {f'<span class="tag">{cat_tag}</span>' if cat_tag else ''}</div>
<div class="conf-card-stats">{''.join(stat_parts)}</div>
</a>'''

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
{html_head(
    title="B2B Conference Directory — Speakers, Sponsors & Sessions | KeynoteData",
    desc=f"Browse {len(confs_with_data)} B2B conferences with full speaker and sponsor data. INBOUND, Dreamforce, SaaStr Annual, MozCon, Slush, and more.",
    canonical="/conferences/"
)}
</head>
<body>
{nav_html()}
<section class="page-header">
<div class="container">
{breadcrumb_html([("Home", "/"), ("Conferences", "")])}
<h1>B2B Conference Directory</h1>
<p>Speaker lists, sponsor rosters, and session data for the top B2B SaaS conferences. {len(confs_with_data)} conferences with full data today.</p>
</div>
</section>
<section class="data-section">
<div class="container">
<div class="conference-grid">{cards}</div>
</div>
</section>
<section class="cta-section">
<div class="container">
<h2>Get the full database</h2>
<p>Filter speakers by seniority, company, or conference. Export to CSV for your CRM or pitch deck.</p>
<div class="cta-form-wrap">{email_form("Get Early Access")}</div>
</div>
</section>
{footer_html()}
</body>
</html>'''

    write_page('conferences/index.html', html)

# =============================================================================
# CONFERENCE DETAIL PAGES
# =============================================================================

def build_conference_page(conf, data):
    slug = conf['slug']
    name = conf['name']
    speakers_by_conf = data['speakers_by_conference']
    all_sponsors = data['sponsors']
    all_sessions = data['sessions']
    all_confs = [c for c in data['conferences'] if c['speaker_count'] > 0]

    # Speakers for this conference
    conf_speakers = speakers_by_conf.get(slug, [])

    # Sponsors for this conference
    conf_sponsors = [s for s in all_sponsors if slug in (s.get('conference_slugs') or '')]

    # Sessions for this conference
    conf_sessions = [s for s in all_sessions if s.get('conference_slug') == slug]

    # Description
    desc_text = CONFERENCE_DESCRIPTIONS.get(slug, f"{name} is a B2B conference tracked by KeynoteData.")

    # Location
    loc_parts = [p for p in [conf.get('city'), conf.get('country')] if p]
    location = ', '.join(loc_parts) if loc_parts else 'International'
    attendees = conf.get('typical_attendees', 0)

    # Category label
    cat_label = conf.get('category', '').replace('-', ' ').title()

    # Header stats
    header_stats = []
    if conf['speaker_count']:
        header_stats.append(f'<div class="conf-header-stat"><span class="conf-header-stat-num">{conf["speaker_count"]}</span><span class="conf-header-stat-label">Speakers</span></div>')
    if conf.get('sponsor_count'):
        header_stats.append(f'<div class="conf-header-stat"><span class="conf-header-stat-num">{conf["sponsor_count"]}</span><span class="conf-header-stat-label">Sponsors</span></div>')
    if conf.get('session_count'):
        header_stats.append(f'<div class="conf-header-stat"><span class="conf-header-stat-num">{conf["session_count"]}</span><span class="conf-header-stat-label">Sessions</span></div>')
    if attendees:
        header_stats.append(f'<div class="conf-header-stat"><span class="conf-header-stat-num">{attendees:,}</span><span class="conf-header-stat-label">Attendees</span></div>')

    # Seniority breakdown
    seniority_breakdown_html = ''
    if conf_speakers:
        tier_counts = {}
        for s in conf_speakers:
            tier = s.get('seniority_tier', '')
            if tier:
                tier_counts[tier] = tier_counts.get(tier, 0) + 1
        senior_count = tier_counts.get('c_level', 0) + tier_counts.get('vp', 0)
        director_count = tier_counts.get('director', 0) + tier_counts.get('head_of', 0)
        total = len(conf_speakers)
        senior_pct = round(senior_count / total * 100) if total else 0
        director_pct = round(director_count / total * 100) if total else 0
        other_count = total - senior_count - director_count
        other_pct = 100 - senior_pct - director_pct

        tier_pills = f'''<div style="display:flex;flex-wrap:wrap;gap:var(--space-3);margin-top:var(--space-4);">
<span style="font-family:var(--font-mono);font-size:var(--text-xs);background:var(--color-primary);color:#fff;border-radius:var(--radius-full);padding:4px 14px;">C-Level / VP: {senior_count} ({senior_pct}%)</span>
<span style="font-family:var(--font-mono);font-size:var(--text-xs);background:var(--color-accent);color:#fff;border-radius:var(--radius-full);padding:4px 14px;">Director / Head of: {director_count} ({director_pct}%)</span>
<span style="font-family:var(--font-mono);font-size:var(--text-xs);background:var(--color-border);color:var(--color-text);border-radius:var(--radius-full);padding:4px 14px;">Manager / IC: {other_count} ({other_pct}%)</span>
</div>'''
        if senior_count > 0:
            seniority_breakdown_html = f'''<section class="use-cases">
<div class="container">
<h2 class="section-title">Who speaks at {name}</h2>
<p class="section-subtitle">{total} speakers tracked. {senior_pct}% are C-Level or VP.</p>
{tier_pills}
</div>
</section>'''

    # Top companies
    top_companies_html = ''
    if conf_speakers:
        company_list = [(s.get('company') or '').strip() for s in conf_speakers if (s.get('company') or '').strip()]
        seen = set()
        unique_companies = []
        for c in company_list:
            if c.lower() not in seen:
                seen.add(c.lower())
                unique_companies.append(c)
        top_cos = unique_companies[:12]
        if top_cos:
            cos_html = ' &nbsp;·&nbsp; '.join(f'<span style="font-weight:var(--weight-semibold);">{c}</span>' for c in top_cos)
            top_companies_html = f'''<section class="data-section" style="padding-top:0;">
<div class="container">
<h2 class="section-title">Companies represented</h2>
<p style="font-size:var(--text-sm);color:var(--color-text);line-height:1.8;">{cos_html}{" and more" if len(unique_companies) > 12 else ""}</p>
</div>
</section>'''

    # Conference-specific FAQs
    faq_items = [
        (f"Who speaks at {name}?", f"{name} has {conf['speaker_count']} speakers tracked in the KeynoteData database. {senior_pct if conf_speakers else 0}% are C-Level or VP. Speaker topics vary by conference track — see the full speaker list for details." if conf_speakers else f"{name} has {conf['speaker_count']} speakers tracked in the KeynoteData database."),
        (f"How do I apply to speak at {name}?", f"Conference speaking applications typically open 6-12 months before the event. Check {name}'s official website for speaker submission deadlines and requirements. Our <a href='/how-to-get-speaking-opportunities/'>guide to B2B conference speaking opportunities</a> covers how to pitch effectively."),
        (f"What companies sponsor {name}?", f"We track {len(conf_sponsors) if conf_sponsors else 'sponsor'} sponsors at {name}. {'Sponsors include companies across ' + (conf.get('category', 'B2B SaaS').replace('-', ' ').title()) + ' and adjacent technology categories. ' if conf_sponsors else ''}Get full access to see the complete sponsor list with cross-conference sponsorship history."),
        (f"When and where is {name}?", f"{name} is held in {location}. Check the official {name} website for exact dates — conference schedules shift year to year."),
    ]
    import json as _json_faq
    faq_schema_items = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a.replace('<a href=', '').replace('>', ' (').replace('</a>', ')').replace("'", '').replace('"', '')}} for q, a in faq_items]
    faq_schema_str_conf = _json_faq.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_schema_items})
    faqs_html = ''.join(f'<details class="faq-item"><summary class="faq-question">{q}</summary><div class="faq-answer"><p>{a}</p></div></details>' for q, a in faq_items)
    conf_faq_section = f'''<section class="faq-section">
<div class="container">
<h2 class="section-title">Questions about {name}</h2>
<div class="faq-list">{faqs_html}</div>
</div>
</section>'''

    # Speaker table (top 10 visible)
    visible_speakers = conf_speakers[:10]
    speaker_rows = ''
    for s in visible_speakers:
        tier_label = seniority_label(s.get('seniority_tier', ''))
        tier_html = f'<span class="seniority-badge">{tier_label}</span>' if tier_label else ''
        li_cell = f'<a href="{s["linkedin_url"]}" class="td-link" target="_blank" rel="noopener">LinkedIn ↗</a>' if s.get('linkedin_url') else '<span class="text-muted">—</span>'
        speaker_rows += f'''<tr>
<td class="td-name">{s.get("name","")}</td>
<td>{s.get("title","") or "—"}</td>
<td>{s.get("company","") or "—"}</td>
<td>{tier_html}</td>
<td>{li_cell}</td>
</tr>'''

    speakers_section = ''
    if conf_speakers:
        remaining = conf['speaker_count'] - len(visible_speakers)
        gate_text = f'Showing {len(visible_speakers)} of {conf["speaker_count"]} speakers. Get full access to see all {conf["speaker_count"]} speakers with LinkedIn profiles and seniority data.'
        speakers_section = f'''<section class="data-section">
<div class="container">
<h2 class="section-title">{name} Speakers</h2>
<p class="section-subtitle">Top speakers by seniority. {conf["speaker_count"]} total speakers tracked.</p>
<div class="data-table-wrapper">
<table class="data-table">
<thead><tr><th>Name</th><th>Title</th><th>Company</th><th>Level</th><th>LinkedIn</th></tr></thead>
<tbody>{speaker_rows}</tbody>
</table>
</div>
{"" if remaining <= 0 else f'''<div class="data-gate">
<div class="data-gate-inner">
<p>{gate_text}</p>
{email_form("See All " + str(conf["speaker_count"]) + " Speakers")}
</div>
</div>'''}
</div>
</section>'''

    # Sponsors section
    sponsors_section = ''
    if conf_sponsors:
        sponsor_rows = ''
        for sp in conf_sponsors[:15]:
            sponsor_rows += f'''<tr>
<td class="td-name">{sp["name"]}</td>
<td>{sp.get("category") or "—"}</td>
<td class="td-mono">{sp.get("events_sponsored", 1)}</td>
<td>{"<a href='" + sp["website_url"] + "' class='td-link' target='_blank' rel='noopener'>Website ↗</a>" if sp.get("website_url") else "—"}</td>
</tr>'''
        sponsors_section = f'''<section class="use-cases">
<div class="container">
<h2 class="section-title">{name} Sponsors</h2>
<p class="section-subtitle">{len(conf_sponsors)} sponsors tracked at {name}.</p>
<div class="data-table-wrapper">
<table class="data-table">
<thead><tr><th>Sponsor</th><th>Category</th><th>Events Sponsored</th><th>Website</th></tr></thead>
<tbody>{sponsor_rows}</tbody>
</table>
</div>
</div>
</section>'''

    # Sessions section
    sessions_section = ''
    if conf_sessions:
        session_rows = ''
        for sess in conf_sessions[:15]:
            session_rows += f'<tr><td>{sess.get("title","")}</td><td class="td-mono">{sess.get("format","") or "—"}</td><td class="td-mono">{sess.get("track","") or "—"}</td></tr>'
        sessions_section = f'''<section class="data-section">
<div class="container">
<h2 class="section-title">{name} Sessions</h2>
<p class="section-subtitle">{len(conf_sessions)} sessions tracked. Showing top 15.</p>
<div class="data-table-wrapper">
<table class="data-table">
<thead><tr><th>Session Title</th><th>Format</th><th>Track</th></tr></thead>
<tbody>{session_rows}</tbody>
</table>
</div>
</div>
</section>'''

    # Related conferences
    related = [c for c in all_confs if c['slug'] != slug and c.get('category') == conf.get('category')][:4]
    if not related:
        related = [c for c in all_confs if c['slug'] != slug][:4]
    related_cards = ''.join(
        f'<a href="/conferences/{c["slug"]}/" class="related-conf-card"><div class="related-conf-name">{c["name"]}</div><div class="related-conf-speakers">{c["speaker_count"]} speakers</div></a>'
        for c in related
    )

    # Website link
    website_link = ''
    if conf.get('website_url'):
        website_link = f'<a href="{conf["website_url"]}" target="_blank" rel="noopener" style="font-size:var(--text-sm);color:var(--color-accent);">Official website ↗</a>'

    # Event schema
    event_schema = {
        "@context": "https://schema.org",
        "@type": "Event",
        "name": name,
        "description": desc_text,
        "location": {"@type": "Place", "name": location},
        "organizer": {"@type": "Organization", "name": name},
        "url": conf.get('website_url', f'{SITE_URL}/conferences/{slug}/'),
    }
    if attendees:
        event_schema["maximumAttendeeCapacity"] = attendees
    import json as _json
    event_schema_str = _json.dumps(event_schema)

    # Internal links to related roundup/category pages
    related_page_links = CONF_RELATED_PAGES.get(slug, [])
    related_links_html = ''
    if related_page_links:
        links = ''.join(f'<a href="{url}" style="display:inline-block;font-family:var(--font-heading);font-size:var(--text-sm);font-weight:var(--weight-semibold);color:var(--color-primary);border:1px solid var(--color-border);border-radius:var(--radius-md);padding:8px 16px;margin:4px 4px 4px 0;">{label} →</a>' for url, label in related_page_links)
        related_links_html = f'''<section class="data-section">
<div class="container">
<h2 class="section-title">Explore More Conference Data</h2>
<p class="section-subtitle">Related reports and databases.</p>
{links}
</div>
</section>'''

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
{html_head(
    title=f"{name} Speakers & Sponsors {CURRENT_YEAR} | KeynoteData",
    desc=f"Full speaker list, sponsor roster, and session data for {name}. {conf['speaker_count']} speakers tracked with LinkedIn profiles and seniority data.",
    canonical=f"/conferences/{slug}/"
)}
<script type="application/ld+json">{event_schema_str}</script>
<script type="application/ld+json">{faq_schema_str_conf}</script>
</head>
<body>
{nav_html()}

<section class="conf-header">
<div class="container">
{breadcrumb_html([("Home", "/"), ("Conferences", "/conferences/"), (name, "")])}
<div class="conf-header-eyebrow">{cat_label} · {location}</div>
<h1>{name}</h1>
<p class="conf-header-desc">{desc_text}</p>
<div class="conf-header-stats">{''.join(header_stats)}</div>
{website_link}
</div>
</section>

{seniority_breakdown_html}
{top_companies_html}
{speakers_section}
{sponsors_section}
{sessions_section}
{conf_faq_section}

<section class="use-cases">
<div class="container">
<h2 class="section-title">Related Conferences</h2>
<div class="related-confs">{related_cards}</div>
</div>
</section>

{related_links_html}

<section class="cta-section">
<div class="container">
<h2>See all {conf["speaker_count"]} {name} speakers</h2>
<p>LinkedIn profiles, seniority tiers, and company data for every speaker. Export to CSV.</p>
<div class="cta-form-wrap">{email_form("See All " + str(conf["speaker_count"]) + " Speakers")}</div>
</div>
</section>

{footer_html()}
</body>
</html>'''

    write_page(f'conferences/{slug}/index.html', html)

# =============================================================================
# CATEGORY SEO PAGES
# =============================================================================

CATEGORY_PAGES = [
    {
        "slug": "conference-speaker-database",
        "title": "B2B Conference Speaker Database",
        "desc": "Search and export B2B conference speakers by conference, seniority, company, and function. 887 speakers tracked across INBOUND, Dreamforce, SaaStr, MozCon, and 9 more.",
        "h1": "B2B Conference Speaker Database",
        "intro": "887 speakers tracked across 13 of the top B2B SaaS and marketing conferences. Every record includes name, title, company, seniority tier, LinkedIn URL, and every conference they've spoken at.",
        "sections": [
            ("What's in the database", """<p>Every speaker record includes:</p>
<ul>
<li><strong>Name, title, and company</strong> — exactly as listed on the conference program</li>
<li><strong>Seniority tier</strong> — C-Level, VP, Director, Head of, or IC (classified from title)</li>
<li><strong>Function category</strong> — Sales, Marketing, Engineering, Operations, Founder, etc.</li>
<li><strong>LinkedIn URL</strong> — available for 605 of 887 speakers (68%)</li>
<li><strong>All conferences spoken at</strong> — cross-referenced across every event we track</li>
</ul>
<div class="highlight-box"><strong>152 C-level speakers</strong> and <strong>183 VP+ speakers</strong> in the database. These are the decision-makers in the room at B2B conferences — and now you know who they are before you walk in.</div>"""),
            ("How to use it", """<p>Three common use cases for the speaker database:</p>
<ul>
<li><strong>Event marketing managers:</strong> Research who's speaking at a conference before you commit your budget. Know the seniority mix, the companies represented, and whether your target accounts will be in the room.</li>
<li><strong>PR agencies doing speaker placement:</strong> Identify which conferences your client's competitors are speaking at. Find gaps — events where their industry is underrepresented. Pitch with data behind your recommendation.</li>
<li><strong>Conference sponsors:</strong> Match your target account list against the speaker roster. If three of your top prospects are speaking at the same event, that's worth knowing before you sign the check.</li>
</ul>"""),
            ("Conferences covered", f"""<p>We track speakers from {len(CONFERENCE_DESCRIPTIONS)} conferences today:</p>
<ul>
{''.join('<li><a href="/conferences/' + slug + '/">' + CONFERENCE_DESCRIPTIONS[slug].split('.')[0].replace('"','') + '</a></li>' for slug in list(CONFERENCE_DESCRIPTIONS.keys())[:8])}
<li><a href="/conferences/">View all conferences →</a></li>
</ul>
<p>We're adding conferences continuously. Target: 50+ by end of {CURRENT_YEAR}.</p>"""),
        ],
        "faqs": [
            ("How do I export the speaker list?", "CSV export is included on all paid plans. Filter by conference, seniority, or function, then export. Format works with HubSpot, Salesforce, Apollo, Clay, and most CRMs."),
            ("Can I filter speakers by company size or industry?", "Company-level firmographic filtering (size, industry, tech stack) is on the product roadmap. For now, you can filter by conference, seniority tier, and function category."),
            ("How accurate is the seniority classification?", "We classify seniority from the title listed on the conference program. Accuracy is high for standard titles (CEO, VP of Sales, Head of Marketing). Edge cases exist for custom titles."),
        ],
    },
    {
        "slug": "b2b-conference-sponsors",
        "title": "B2B Conference Sponsor Intelligence",
        "desc": "Track which companies sponsor B2B SaaS conferences and where they invest. 487 sponsors indexed across INBOUND, SaaStr Annual, LeadsCon, 6sense Breakthrough, and more.",
        "h1": "B2B Conference Sponsor Intelligence",
        "intro": "487 sponsors indexed across 13 conferences. See which companies keep showing up, which events attract the biggest sponsor budgets, and which brands are new to the conference circuit.",
        "sections": [
            ("What the sponsor data includes", """<p>Every sponsor record includes:</p>
<ul>
<li><strong>Company name and website</strong></li>
<li><strong>Sponsorship tier</strong> — where available (Gold, Silver, Bronze, etc.)</li>
<li><strong>All conferences sponsored</strong> — cross-referenced across every event we track</li>
<li><strong>Total events sponsored</strong> — see which brands invest across multiple conferences</li>
</ul>
<div class="highlight-box"><strong>11 sponsors appear at 2+ events</strong> in our current database. These are the companies treating conference sponsorship as a core channel — not a one-off experiment.</div>"""),
            ("Why sponsor data matters", """<p>Conference sponsorship is a significant signal:</p>
<ul>
<li>If a competitor is sponsoring a conference you're not, they have a visibility advantage with that audience</li>
<li>If a company is sponsoring 3+ events in your space, they've figured out ROI — which means the audience converts</li>
<li>New sponsors at a conference signal growing interest in that audience; departing sponsors signal declining fit</li>
<li>Sponsor tier data reveals budget commitment — a gold sponsor is very different from a lanyard sponsor</li>
</ul>"""),
            ("How to use sponsor intelligence", """<p>Common use cases:</p>
<ul>
<li><strong>Competitive intelligence:</strong> Which conferences are your competitors sponsoring? Are they increasing or decreasing spend?</li>
<li><strong>Partnership identification:</strong> Find non-competing sponsors at your target conferences. These are companies with overlapping audiences and real event budgets.</li>
<li><strong>Conference selection:</strong> Before committing to a new event, see who else is sponsoring. If your top prospects' vendors are there, your prospects probably are too.</li>
<li><strong>Sales prospecting:</strong> Conference sponsors are often buyers. They have event marketing budgets, tech decisions, and deadlines.</li>
</ul>"""),
        ],
        "faqs": [
            ("How do you get sponsorship tier data?", "We scrape tier data from conference prospectuses and event websites where it's publicly listed. Not every conference publishes tier names — in those cases we record 'sponsor' as the tier."),
            ("Can I export the full sponsor list?", "Yes, CSV export is available on all paid plans. Filter by conference or multi-event status and export directly."),
            ("How current is the sponsor data?", "We update after each conference cycle — typically within a few weeks of the event. Historical sponsorship data goes back to 2024 for most conferences we track."),
        ],
    },
    {
        "slug": "event-marketing-intelligence",
        "title": "Event Marketing Intelligence for B2B Companies",
        "desc": "Data-driven event marketing decisions. Research conference speakers and sponsors before you budget. Track the competitive landscape. Know who'll be in the room.",
        "h1": "Event Marketing Intelligence",
        "intro": "B2B event marketing is a high-stakes, low-data game. You're committing $20K–$200K based on attendee estimates and sales pitches from conference organizers. KeynoteData gives you actual intelligence — speaker rosters, sponsor history, and session data — before you write the check.",
        "sections": [
            ("The problem with conference decisions today", """<p>Most B2B event marketing decisions follow the same broken process:</p>
<ul>
<li>A conference rep sends you a prospectus with impressive attendee numbers</li>
<li>You check with your team about whether they've heard of the event</li>
<li>You look at last year's speaker page (if it's still up)</li>
<li>You decide based on gut feel and relationship with the rep</li>
</ul>
<p>The result: you spend $50K at a conference and spend three days talking to vendors instead of buyers. Or you skip an event that your top three prospects all attended.</p>
<div class="highlight-box">KeynoteData gives you a different starting point: <strong>actual data on who speaks, who sponsors, and what gets discussed</strong> at the conferences you're considering.</div>"""),
            ("What intelligent event marketing looks like", """<p>Before committing to a conference, data-driven event marketers ask:</p>
<ul>
<li>What's the seniority mix of speakers? (Lots of practitioners, few executives = different ROI than an executive-heavy event)</li>
<li>Which companies are in the speaker lineup? (Your target accounts speaking = their teams attend)</li>
<li>Who sponsors this event? (Sponsors reveal who else is chasing this audience)</li>
<li>What topics dominate the sessions? (Session themes reveal audience interests and maturity)</li>
<li>Is this a one-and-done sponsor or a conference with repeat commitment from brands like yours?</li>
</ul>
<p>KeynoteData answers these questions with actual data, not estimates.</p>"""),
        ],
        "faqs": [
            ("Which conferences do you have data for?", f"We have full speaker and sponsor data for {len(CONFERENCE_DESCRIPTIONS)} conferences today, including INBOUND, Dreamforce, SaaStr Annual, MozCon, Slush, and more. See the full list at /conferences/."),
            ("How do I know if a conference has the right seniority mix?", "Our speaker database tags every speaker with a seniority tier — C-Level, VP, Director, Head of, etc. You can filter by conference and see exactly what the seniority breakdown looks like before you decide."),
        ],
    },
    {
        "slug": "conference-speaking-opportunities",
        "title": "B2B Conference Speaking Opportunities",
        "desc": "Find speaking opportunities at top B2B conferences. See who speaks where, identify gaps in your industry's conference representation, and build a data-backed pitch.",
        "h1": "B2B Conference Speaking Opportunities",
        "intro": "Getting speaking slots at the right conferences is one of the highest-leverage PR tactics for B2B brands. But most speaking pitches fail because they're not targeted. KeynoteData shows you who's already speaking where — so you can find the gaps and pitch with data.",
        "sections": [
            ("How to identify the right conferences to pitch", """<p>Before you pitch a speaking slot, you need to know:</p>
<ul>
<li><strong>Who already speaks there</strong> — Is the speaker roster your peers or your aspirational comp set?</li>
<li><strong>What topics dominate</strong> — Does your expertise align with what this audience wants to hear?</li>
<li><strong>Where your competitors speak</strong> — If three competitors speak at a conference and you don't, that's a problem. If none do, that's an opportunity.</li>
<li><strong>Which events are growing their speaker roster</strong> — New conferences often have more accessible application processes</li>
</ul>
<div class="highlight-box">The KeynoteData speaker database lets you search by conference to see exactly who spoke, what title they held, and what company they represented. A pitch that says "I notice you've featured three CMOs from enterprise SaaS — here's our CMO's take on X" converts better than a cold "we'd love to speak."</div>"""),
            ("The cross-conference view", """<p>One of the most useful views in KeynoteData is the cross-conference speaker list — people who've spoken at multiple events in the same space.</p>
<p>These repeat speakers have figured out the circuit. They know what topics land, which conferences have the best audiences, and how to get selected. Studying their topics and conference mix gives you a map of what the market responds to.</p>
<p>We have <strong>{multi_app} speakers who've appeared at 2+ conferences</strong> in our database. Their track record tells you which conferences produce the best engagements for B2B speakers.</p>""".replace('{multi_app}', str(11))),
        ],
        "faqs": [
            ("How do I find out who speaks at a specific conference?", "Search by conference on any conference detail page. You'll see the full speaker list with names, titles, companies, and LinkedIn profiles."),
            ("Can I see the speaker application timeline for each conference?", "Speaker application timelines aren't in the current database — that data lives on conference websites and varies widely. We focus on the post-event data (who actually spoke) rather than the application process."),
        ],
    },
    {
        "slug": "speaker-placement-strategy",
        "title": "Conference Speaker Placement Strategy for PR Agencies",
        "desc": "Data-driven speaker placement for PR agencies. Research which conferences feature your clients' peers, identify speaking gaps, and pitch with real speaker roster data behind your recommendation.",
        "h1": "Speaker Placement Strategy for PR Agencies",
        "intro": "Speaker placement is one of the highest-value services a B2B PR agency can offer. But pitching without data is guesswork. KeynoteData gives you the actual speaker rosters for the conferences your clients should be targeting — so your recommendations are backed by evidence, not relationships.",
        "sections": [
            ("The data-backed pitch", """<p>A strong speaker placement pitch answers three questions:</p>
<ol>
<li><strong>Why this conference?</strong> — Show the speaker roster. Demonstrate that your client's peers and target buyers attend.</li>
<li><strong>Why this topic?</strong> — Show what topics have been covered, and what the gap is. Your client fills the gap.</li>
<li><strong>Why now?</strong> — Show the competitive landscape. If competitors are speaking and your client isn't, that's urgency. If no one from your client's category has spoken there, that's an opportunity.</li>
</ol>
<p>KeynoteData gives you the data for all three arguments.</p>"""),
            ("Building your client's conference map", """<p>A conference map for a B2B SaaS client typically covers:</p>
<ul>
<li>Tier 1 events (2-3 conferences where you actively pursue speaking slots every year)</li>
<li>Tier 2 events (5-8 conferences where you pitch opportunistically)</li>
<li>Tier 3 events (emerging conferences worth monitoring)</li>
</ul>
<p>Building this map requires knowing which conferences feature speakers like your client — same seniority, same function, adjacent or overlapping audience. The KeynoteData speaker database gives you that view across 13 conferences today.</p>"""),
        ],
        "faqs": [
            ("Can I export speaker lists to use in client presentations?", "Yes. CSV export on all paid plans. Export any conference speaker list, filter by seniority or function, and import into your pitch deck or reporting template."),
            ("Do you track conference application deadlines?", "Not currently. The database focuses on confirmed speakers and actual event data. Application deadlines and call-for-speakers timelines are tracked separately by each conference."),
        ],
    },
    {
        "slug": "b2b-conference-data",
        "title": "B2B Conference Data — Speakers, Sponsors & Sessions",
        "desc": "Structured B2B conference data for event marketers, PR teams, and conference organizers. 887 speakers, 487 sponsors, 1,256 sessions across 13 conferences.",
        "h1": "B2B Conference Data",
        "intro": "Conference data exists. It's scattered across hundreds of event websites, LinkedIn profiles, and speaker directories. KeynoteData organizes it into a structured, searchable, exportable database.",
        "sections": [
            ("What the data covers", f"""<p>Three data sets, updated after each conference cycle:</p>
<ul>
<li><strong>Speakers</strong> — 887 speakers with name, title, company, seniority, LinkedIn, and conference history</li>
<li><strong>Sponsors</strong> — 487 sponsors with company, tier, events sponsored, and website</li>
<li><strong>Sessions</strong> — 1,256 session titles with format, track, and abstract (where published)</li>
</ul>
<p>All three data sets are cross-referenced. You can see which sessions featured which speakers, which companies sponsored the same conference where their executives spoke, and which topics dominate at each conference.</p>"""),
            ("Data methodology", """<p>We collect data through a combination of:</p>
<ul>
<li><strong>Web scraping</strong> — Conference websites, speaker pages, and session schedules</li>
<li><strong>Enrichment</strong> — LinkedIn profile matching (68% coverage) and seniority classification from title</li>
<li><strong>Manual review</strong> — Edge cases and data quality checks</li>
</ul>
<p>We update after each conference and track changes over time. Speaker data is more stable than sponsor data — speaker lineups are set months in advance, while sponsor rosters shift closer to event dates.</p>"""),
        ],
        "faqs": [
            ("Can I get raw data access or an API?", "Raw data access is available via CSV export on all paid plans. API access is on the roadmap — contact us if you have a specific use case."),
            ("How does KeynoteData compare to manually scraping conference websites?", "Manual scraping gets you one conference at a time, with no enrichment, no cross-referencing, and no historical data. KeynoteData gives you 13 conferences in a single searchable database, with LinkedIn profiles and seniority tags already added."),
        ],
    },
    {
        "slug": "conference-sponsorship-roi",
        "title": "Conference Sponsorship ROI — What the Data Says",
        "desc": "What makes B2B conference sponsorship worth it? Speaker data, sponsor repeat rates, and session intelligence that help you evaluate ROI before you sign.",
        "h1": "Conference Sponsorship ROI",
        "intro": "Conference sponsorship is expensive and hard to measure. Most teams justify it with brand awareness and hope. The teams that consistently get ROI do something different: they research the event before they commit, and they track patterns across events.",
        "sections": [
            ("The signals that predict ROI", """<p>Before committing to a conference sponsorship, the data points that matter most:</p>
<ul>
<li><strong>Speaker seniority mix</strong> — More C-level and VP speakers means more decision-makers in the audience. Practitioner-heavy events attract buyers earlier in their career.</li>
<li><strong>Repeat sponsors</strong> — Companies don't keep sponsoring conferences that don't work. If you see 5+ sponsors who've been there for 3+ years, the event has proven ROI for at least one business model adjacent to yours.</li>
<li><strong>Target account presence</strong> — Are companies from your ICP in the speaker roster? Speakers' companies tend to send significant delegations. If your top 10 prospects have speakers at a conference, their teams are in the room.</li>
<li><strong>Session topics</strong> — Sessions tell you what the audience cares about this year. If your product solves a problem that's showing up in session titles, the timing is right.</li>
</ul>"""),
            ("What KeynoteData shows you", f"""<p>For each of the {len(CONFERENCE_DESCRIPTIONS)} conferences we track:</p>
<ul>
<li>Full speaker list with seniority and company (match against your ICP)</li>
<li>Full sponsor list with tier data (find the repeat sponsors, avoid crowded categories)</li>
<li>Session titles (match against your messaging and buyer pain points)</li>
</ul>
<p>This takes a 30-second gut-check decision and turns it into a 20-minute data review. Most teams find that 2-3 events they were planning to skip deserve a second look — and 1-2 they were planning to attend don't hold up.</p>"""),
        ],
        "faqs": [
            ("How do you measure conference ROI?", "Measuring conference ROI is hard — most teams track pipeline generated and meetings booked, but attribution is murky. Our data helps with the pre-event decision, not post-event attribution. Better inputs lead to better outputs."),
            ("Which conferences have the best ROI for B2B SaaS?", "It depends on your ICP. INBOUND and SaaStr attract broad B2B SaaS audiences. MozCon is highly specific to SEO and content. LeadsCon is demand gen and lead marketing. We can help you match your ICP to the right conference — see the speaker data for each event."),
        ],
    },
    {
        "slug": "how-to-get-speaking-opportunities",
        "title": "How to Get B2B Conference Speaking Opportunities",
        "desc": "A data-driven guide to landing speaking slots at B2B conferences. Research the right events, build targeted pitches, and track your outreach.",
        "h1": "How to Get B2B Conference Speaking Opportunities",
        "intro": "Getting a speaking slot at a B2B conference is part research, part storytelling, and part timing. The teams that land consistent speaking opportunities share one trait: they research before they pitch. Here's how to do it with data.",
        "sections": [
            ("Step 1: Find the right conferences", """<p>Most people target conferences they've heard of. The better approach: target conferences where your exact peer set is already speaking.</p>
<p>Pull the speaker roster for any conference in your space. Look for:</p>
<ul>
<li>Companies at similar stage and profile to yours</li>
<li>Speakers with similar titles to your executive</li>
<li>Topics that are adjacent to (not identical to) your product category</li>
</ul>
<p>If the conference has speakers like yours, the program committee already understands that profile. Your pitch is familiar, not foreign.</p>
<div class="highlight-box">KeynoteData shows you the full speaker roster for 13 B2B conferences with seniority tags and company data. Start with the conferences where your profile already fits — it's a much shorter path to a yes.</div>"""),
            ("Step 2: Find the gap in the program", """<p>Conference program committees are looking for what they're missing, not more of what they already have. Review the session topics and speaker companies for each conference you're targeting.</p>
<p>Ask yourself:</p>
<ul>
<li>What topic category is underrepresented in the speaker list?</li>
<li>What point of view does your executive have that isn't already covered?</li>
<li>What's changing in the market that none of the existing speakers are addressing?</li>
</ul>
<p>Your pitch should fill a gap, not compete with speakers they've already confirmed.</p>"""),
            ("Step 3: Write a data-backed pitch", """<p>The best speaking pitches reference the event specifically:</p>
<ul>
<li>Name two or three sessions from their most recent program that were in the right neighborhood (but not the same topic as your proposal)</li>
<li>Reference the audience profile — "I saw you featured three CMOs from enterprise SaaS last year; I'm speaking to VP-level demand gen leaders who run $5M+ event budgets"</li>
<li>Lead with the audience benefit, not your credentials — "Here's what your attendees will walk out knowing" beats "Here's why I'm qualified"</li>
</ul>
<p>This level of specificity requires research. Most pitches don't have it. That's the edge.</p>"""),
        ],
        "faqs": [
            ("When should I submit a speaking application?", "Most major B2B conferences open their CFP (Call for Proposals) 4-6 months before the event. INBOUND typically opens in December for their September event. Check the conference website for specific deadlines."),
            ("Is it better to pitch original research or tactical how-to content?", "Depends on the conference. Research-heavy conferences (MozCon, INBOUND) value proprietary data. Sales and practitioner conferences (OutBound, Sandler Summit) value tactical, actionable content. Review the session titles from past years — they tell you exactly what the program committee selects."),
            ("How many conferences should I target at once?", "Start with 3-5 conferences where your profile fits. It's better to pitch 3 conferences with highly tailored pitches than 15 with a generic one. Each pitch should reference the specific conference and show you've done your research."),
        ],
    },
    {
        "slug": "vendelux-alternative",
        "title": "Vendelux Alternative — B2B Conference Intelligence at SMB Pricing",
        "desc": "Looking for a Vendelux alternative? KeynoteData tracks speakers, sponsors, and sessions across 13 top B2B conferences. Fraction of the price, built for marketing teams that don't need enterprise attendee prediction.",
        "h1": "Vendelux Alternative for B2B Conference Intelligence",
        "intro": "Vendelux charges $20K–$125K per year for attendee prediction. KeynoteData tracks speaker rosters, sponsor patterns, and session data across the top B2B conferences — built for marketing teams who need to research before they spend, not enterprise accounts who need ML-driven attendee forecasting.",
        "sections": [
            ("What Vendelux does", """<p>Vendelux uses machine learning to predict who will attend a conference before the event. Their core pitch: give us your target account list and we'll tell you which conferences your buyers will be at.</p>
<p>That's useful if you have a large enterprise sales team, a mature ABM motion, and $20K–$125K/year to spend on conference intelligence tools. It's less useful if you're a two-person event marketing team trying to figure out which conferences are worth the $30K sponsorship budget.</p>"""),
            ("What KeynoteData does differently", """<p>KeynoteData is built around three questions that event marketers actually ask before they decide:</p>
<ul>
<li><strong>Who's speaking?</strong> — Full speaker roster with seniority tier, company, title, and LinkedIn for every tracked conference. 887 speakers across 13 conferences.</li>
<li><strong>Who's sponsoring?</strong> — 487 sponsors tracked with cross-conference sponsorship history. See which companies keep showing up — and which ones don't renew.</li>
<li><strong>What gets discussed?</strong> — 1,256 sessions with titles, formats, and tracks. Understand the content angle before you commit to the event.</li>
</ul>
<p>No attendee prediction. No enterprise contract required. Research the conferences that matter to your ICP and make the call yourself.</p>"""),
            ("Who KeynoteData is for", """<p>KeynoteData is built for two audiences:</p>
<p><strong>Event marketing managers at B2B SaaS companies</strong> with $50K–$200K annual conference budgets. You need to know whether Dreamforce is worth $40K in sponsorship before you sign. You want to see the speaker list, check the sponsor mix for competitors, and confirm the session topics match your ICP's priorities. You don't need a six-figure tool to do that research.</p>
<p><strong>PR agencies placing speakers</strong> for B2B clients. You need to know which conferences have gaps in your client's industry representation, who's already speaking at competing companies, and how to pitch with data behind the recommendation.</p>
<p>If you need ML-driven attendee prediction for a 50-person field marketing team, Vendelux is built for that. If you need to research the right conferences and make smarter event investments, KeynoteData is built for this.</p>"""),
        ],
        "faqs": [
            ("How does KeynoteData compare to Vendelux on price?", "Vendelux pricing starts around $20,000/year and scales to $125,000+ for enterprise accounts. KeynoteData is priced for SMB marketing teams — a fraction of that cost with no enterprise contract required."),
            ("Does KeynoteData predict conference attendees like Vendelux?", "No. Vendelux uses machine learning to predict which of your target accounts will attend a given conference. KeynoteData focuses on speaker rosters, sponsor lists, and session data — the information you need to evaluate a conference before you commit budget to it."),
            ("What conferences does KeynoteData cover?", "We have full speaker and sponsor data for 13 conferences: INBOUND, Dreamforce, SaaStr Annual, Slush, SaaStock, LeadsCon, MozCon, Spryng, Sandler Summit, ERE, 6sense Breakthrough, OutBound Conference, and Sales 3.0. We track 214 conferences total and are adding full data continuously."),
            ("Is there a free version of KeynoteData?", "You can browse speaker previews and conference summaries on the site without signing up. Full database access — all 887 speakers with LinkedIn profiles, complete sponsor lists, and export to CSV — requires an account."),
        ],
    },
]


def build_category_pages(data):
    stats = data['stats']
    speakers = data['speakers']

    for page in CATEGORY_PAGES:
        slug = page['slug']

        sections_html = ''
        for sec_title, sec_body in page['sections']:
            sections_html += f'<h2>{sec_title}</h2>\n{sec_body}\n'

        faqs_html = ''
        faq_schema_items = []
        for q, a in page.get('faqs', []):
            faqs_html += f'<details class="faq-item"><summary class="faq-question">{q}</summary><div class="faq-answer">{a}</div></details>'
            faq_schema_items.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}})

        faq_schema_str = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_schema_items})

        # Sample data (top 6 speakers for sidebar)
        sample_rows = ''.join(speaker_row_html(s) for s in speakers[:6])
        sample_table = f'''<div class="data-table-wrapper" style="margin-top:var(--space-6);">
<table class="data-table">
<thead><tr><th>Name</th><th>Title</th><th>Company</th><th>Level</th><th>Conference(s)</th><th>LinkedIn</th></tr></thead>
<tbody>{sample_rows}</tbody>
</table>
</div>
<div class="data-gate">
<div class="data-gate-inner">
<p>Showing 6 of {stats["total_speakers"]:,} speakers. Get full access to filter and export.</p>
{email_form("See Full Database")}
</div>
</div>'''

        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
{html_head(
    title=f"{page['title']} | KeynoteData",
    desc=page['desc'],
    canonical=f"/{slug}/"
)}
<script type="application/ld+json">{faq_schema_str}</script>
</head>
<body>
{nav_html()}

<section class="page-header">
<div class="container">
{breadcrumb_html([("Home", "/"), (page["h1"], "")])}
<h1>{page["h1"]}</h1>
<p>{page["intro"]}</p>
</div>
</section>

<section>
<div class="container">
<div class="prose">{sections_html}</div>
</div>
</section>

<section class="data-section">
<div class="container">
<h2 class="section-title">Sample Data</h2>
<p class="section-subtitle">A preview of what's in the database.</p>
{sample_table}
</div>
</section>

{"<section class='faq-section'><div class='container'><h2 class='section-title'>Questions</h2><div class='faq-list'>" + faqs_html + "</div></div></section>" if faqs_html else ""}

<section class="data-section">
<div class="container">
<h2 class="section-title">Conferences in the database</h2>
<p class="section-subtitle">Full speaker and sponsor data available for these conferences.</p>
<div style="display:flex;flex-wrap:wrap;gap:8px;">
{''.join(f'<a href="/conferences/{c["slug"]}/" style="font-family:var(--font-heading);font-size:var(--text-sm);font-weight:var(--weight-semibold);color:var(--color-primary);border:1px solid var(--color-border);border-radius:var(--radius-md);padding:8px 16px;">{c["name"]} →</a>' for c in data['conferences'] if c['speaker_count'] > 0)}
</div>
</div>
</section>

<section class="cta-section">
<div class="container">
<h2>Get the full database</h2>
<p>887 speakers, 487 sponsors, 13 conferences. Filter, search, and export.</p>
<div class="cta-form-wrap">{email_form("Get Early Access")}</div>
</div>
</section>

{footer_html()}
</body>
</html>'''

        write_page(f'{slug}/index.html', html)

# =============================================================================
# ROUNDUP PAGES
# =============================================================================

ROUNDUP_PAGES = [
    {
        "slug": "best-b2b-saas-conferences-2026",
        "title": f"Best B2B SaaS Conferences {CURRENT_YEAR}",
        "desc": f"The best B2B SaaS conferences in {CURRENT_YEAR}, ranked by speaker quality, attendee mix, and data coverage. INBOUND, SaaStr Annual, Dreamforce, Slush, SaaStock, and more.",
        "intro": f"Ranking the top B2B SaaS conferences in {CURRENT_YEAR} by what actually matters: speaker seniority, audience quality, and whether the right people are in the room.",
        "conf_slugs": ["inbound", "dreamforce", "saastr-annual", "slush", "saastock"],
    },
    {
        "slug": "best-b2b-marketing-conferences-2026",
        "title": f"Best B2B Marketing Conferences {CURRENT_YEAR}",
        "desc": f"The top B2B marketing conferences in {CURRENT_YEAR} ranked by speaker quality and audience. INBOUND, MozCon, LeadsCon, Spryng, and more — with real speaker data.",
        "intro": f"The best B2B marketing conferences in {CURRENT_YEAR}, ranked with real speaker and sponsor data. Not just name recognition — actual intelligence on who shows up and what gets discussed.",
        "conf_slugs": ["inbound", "mozcon", "leadscon", "spryng"],
    },
    {
        "slug": "best-revops-conferences-2026",
        "title": f"Best RevOps Conferences {CURRENT_YEAR}",
        "desc": f"Top revenue operations conferences in {CURRENT_YEAR}. Where RevOps, GTM, and sales operations leaders gather — with speaker data and sponsor intelligence.",
        "intro": f"RevOps conferences in {CURRENT_YEAR}, ranked by relevance for revenue operations, GTM, and sales operations leaders. Data-backed, not based on marketing spend.",
        "conf_slugs": ["inbound", "saastr-annual", "leadscon", "6sense-breakthrough"],
    },
    {
        "slug": "best-sales-conferences-2026",
        "title": f"Best Sales Conferences {CURRENT_YEAR}",
        "desc": f"Top B2B sales conferences in {CURRENT_YEAR} for AEs, SDRs, VPs, and CROs. Dreamforce, SaaStr Annual, OutBound Conference, Sandler Summit — with real speaker data.",
        "intro": f"The best B2B sales conferences in {CURRENT_YEAR}, ranked by speaker seniority and relevance for sales leaders, AEs, and SDRs. Every ranking backed by actual speaker roster data.",
        "conf_slugs": ["dreamforce", "saastr-annual", "outbound-conference", "sandler-summit", "6sense-breakthrough"],
    },
    {
        "slug": "best-ai-conferences-2026",
        "title": f"Best AI Conferences for B2B Marketers {CURRENT_YEAR}",
        "desc": f"Top AI conferences for B2B marketing and sales teams in {CURRENT_YEAR}. Where AI speakers from Anthropic, OpenAI, and leading SaaS companies are presenting.",
        "intro": f"AI is dominating conference programs in {CURRENT_YEAR}. Here are the B2B conferences with the strongest AI speaker content — ranked by actual speaker data, not hype.",
        "conf_slugs": ["inbound", "dreamforce", "slush", "saastr-annual"],
    },
    {
        "slug": "best-hr-tech-conferences-2026",
        "title": f"Best HR Tech Conferences {CURRENT_YEAR}",
        "desc": f"Top HR technology conferences in {CURRENT_YEAR} for HR leaders, talent acquisition teams, and HR tech vendors. Speaker and sponsor data from ERE and more.",
        "intro": f"The HR tech conference landscape in {CURRENT_YEAR}, ranked by speaker quality and relevance for talent leaders and HR technology vendors. Every ranking uses real speaker roster data.",
        "conf_slugs": ["ere", "saastr-annual"],
    },
    {
        "slug": "best-recruiting-conferences-2026",
        "title": f"Best Recruiting Conferences {CURRENT_YEAR}",
        "desc": f"Top talent acquisition and recruiting conferences in {CURRENT_YEAR}. Where sourcers, talent leaders, and recruiting technology vendors gather — with real speaker data.",
        "intro": f"Recruiting conferences in {CURRENT_YEAR}, ranked by relevance for talent acquisition leaders, sourcers, and TA technology vendors. Speaker data across every event.",
        "conf_slugs": ["ere", "saastr-annual"],
    },
    {
        "slug": "best-content-marketing-conferences-2026",
        "title": f"Best Content Marketing Conferences {CURRENT_YEAR}",
        "desc": f"Top content marketing conferences in {CURRENT_YEAR} for content strategists, SEO teams, and B2B marketers. MozCon, INBOUND, LeadsCon — with real speaker data.",
        "intro": f"Content marketing conferences in {CURRENT_YEAR}, ranked by speaker quality and relevance for content teams. Real speaker roster data — not editorial opinion.",
        "conf_slugs": ["mozcon", "inbound", "leadscon"],
    },
    {
        "slug": "best-demand-gen-conferences-2026",
        "title": f"Best Demand Generation Conferences {CURRENT_YEAR}",
        "desc": f"Top demand generation conferences in {CURRENT_YEAR} for demand gen leaders and B2B marketers. INBOUND, LeadsCon, 6sense Breakthrough, Spryng — with real speaker data.",
        "intro": f"Demand gen conferences in {CURRENT_YEAR}, ranked by relevance for demand generation leaders, growth marketers, and pipeline-focused teams. Data-backed rankings.",
        "conf_slugs": ["inbound", "leadscon", "6sense-breakthrough", "spryng"],
    },
    {
        "slug": "best-saas-founder-conferences-2026",
        "title": f"Best SaaS Founder Conferences {CURRENT_YEAR}",
        "desc": f"Top conferences for SaaS founders and startup leaders in {CURRENT_YEAR}. SaaStr Annual, Slush, SaaStock — with real speaker and sponsor data.",
        "intro": f"SaaS founder conferences in {CURRENT_YEAR}, ranked by relevance for founders, early-stage operators, and investor networks. Based on actual speaker roster data.",
        "conf_slugs": ["saastr-annual", "slush", "saastock"],
    },
    {
        "slug": "best-gtm-conferences-2026",
        "title": f"Best GTM Conferences {CURRENT_YEAR}",
        "desc": f"Top go-to-market conferences in {CURRENT_YEAR} for GTM leaders, revenue teams, and B2B SaaS operators. SaaStr Annual, INBOUND, LeadsCon — with real speaker data.",
        "intro": f"Go-to-market conferences in {CURRENT_YEAR}, ranked for GTM leaders, RevOps teams, and B2B SaaS operators who need to know who's building the playbooks everyone follows.",
        "conf_slugs": ["saastr-annual", "inbound", "leadscon"],
    },
]


def build_roundup_pages(data):
    all_confs_map = {c['slug']: c for c in data['conferences']}
    speakers_by_conf = data['speakers_by_conference']

    for page in ROUNDUP_PAGES:
        slug = page['slug']

        ranked_html = ''
        for i, conf_slug in enumerate(page['conf_slugs'], 1):
            conf = all_confs_map.get(conf_slug)
            if not conf:
                continue
            desc = CONFERENCE_DESCRIPTIONS.get(conf_slug, '')
            loc_parts = [p for p in [conf.get('city'), conf.get('country')] if p]
            location = ', '.join(loc_parts) if loc_parts else 'International'
            top_speakers = speakers_by_conf.get(conf_slug, [])[:3]
            speaker_list = ', '.join(f'<strong>{s["name"]}</strong> ({s.get("company","")})' for s in top_speakers)
            stats_parts = []
            if conf.get('speaker_count'):
                stats_parts.append(f'{conf["speaker_count"]} speakers')
            if conf.get('sponsor_count'):
                stats_parts.append(f'{conf["sponsor_count"]} sponsors')
            if conf.get('session_count'):
                stats_parts.append(f'{conf["session_count"]} sessions')
            stats_str = ' · '.join(stats_parts)

            ranked_html += f'''<div class="conf-card" style="display:block;margin-bottom:var(--space-4);">
<div style="display:flex;align-items:flex-start;gap:var(--space-4);">
<div style="font-family:var(--font-mono);font-size:var(--text-3xl);font-weight:var(--weight-medium);color:var(--color-border);line-height:1;flex-shrink:0;">{i:02d}</div>
<div style="flex:1;">
<div class="conf-card-name"><a href="/conferences/{conf_slug}/" style="color:var(--color-primary);">{conf["name"]}</a></div>
<div class="conf-card-meta">{location} · {stats_str}</div>
<p style="font-size:var(--text-sm);color:var(--color-text);margin:var(--space-2) 0;">{desc.split(".")[0]}.</p>
{"<p style='font-size:var(--text-xs);color:var(--color-text-muted);font-family:var(--font-mono);'>Notable speakers: " + speaker_list + "</p>" if speaker_list else ""}
</div>
</div>
</div>'''

        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
{html_head(
    title=f"{page['title']} | KeynoteData",
    desc=page['desc'],
    canonical=f"/{slug}/"
)}
</head>
<body>
{nav_html()}

<section class="page-header">
<div class="container">
{breadcrumb_html([("Home", "/"), (page["title"], "")])}
<h1>{page["title"]}</h1>
<p>{page["intro"]}</p>
</div>
</section>

<section class="data-section">
<div class="container">
<h2 class="section-title">The Rankings</h2>
<p class="section-subtitle">Ranked using real speaker roster data — not conference marketing claims.</p>
{ranked_html}
<div style="text-align:center;margin-top:var(--space-6);">
<a href="/conferences/" style="font-family:var(--font-heading);font-weight:var(--weight-semibold);color:var(--color-primary);">View all conferences in the database →</a>
</div>
</div>
</section>

<section class="cta-section">
<div class="container">
<h2>See the full speaker data</h2>
<p>Filter speakers by conference, seniority, and company. Export to CSV for your event planning.</p>
<div class="cta-form-wrap">{email_form("Get Early Access")}</div>
</div>
</section>

{footer_html()}
</body>
</html>'''

        write_page(f'{slug}/index.html', html)

# =============================================================================
# ROLE / AUDIENCE PAGES
# =============================================================================

ROLE_PAGES = [
    {
        "slug": "conferences-for-vp-marketing",
        "title": f"Best Conferences for VP of Marketing {CURRENT_YEAR}",
        "h1": "Best Conferences for VP of Marketing",
        "desc": f"Best B2B conferences for VP of Marketing in {CURRENT_YEAR}. Real speaker and sponsor data across INBOUND, Dreamforce, SaaStr Annual, and LeadsCon.",
        "intro": "You're choosing where to send your team — or where to speak yourself. Here's what the speaker and sponsor data says about which conferences VP-level marketers actually attend.",
        "sections": [
            ("What to look for as a VP of Marketing", """<p>Conference ROI for marketing leaders comes down to three things: the seniority of speakers (peers, not vendors), the quality of sponsor mix (signals which companies consider this audience worth paying for), and whether your target accounts send decision-makers.</p>
<p>The conferences below have the highest concentration of VP and C-level marketing speakers in our database. That's the signal that separates a conference where marketing leaders go to learn from one where they go to be sold to.</p>"""),
            ("Speaker seniority matters more than session count", """<p>A conference with 400 sessions and mostly IC-level speakers tells you one thing: lots of practitioners, not many decision-makers. A conference with 70 speakers and 40% VP+ tells you something different.</p>
<p>We track seniority tier for every speaker in our database. The conferences listed here rank highest for VP and C-level marketing representation.</p>"""),
        ],
        "faqs": [
            ("Which conference has the most VP of Marketing speakers?", "INBOUND consistently has the highest volume of senior marketing speakers, with 393 speakers tracked and strong VP and C-level representation. Dreamforce and SaaStr Annual also feature significant VP+ marketing presence."),
            ("Are these conferences worth sponsoring as a B2B marketing vendor?", "That depends on your target buyer. INBOUND and Dreamforce draw large marketing teams with budget authority. SaaStr Annual skews toward SaaS GTM leaders. LeadsCon draws performance marketing and lead gen buyers specifically."),
            ("How is seniority determined?", "We classify speaker seniority from job titles using a consistent taxonomy: C-Level, VP, Director, Head of, Manager, and Individual Contributor. Classification is based on the title as listed on the conference program."),
        ],
        "conf_slugs": ["inbound", "dreamforce", "saastr-annual", "leadscon"],
    },
    {
        "slug": "conferences-for-chief-revenue-officer",
        "title": f"Best Conferences for Chief Revenue Officers {CURRENT_YEAR}",
        "h1": "Best Conferences for Chief Revenue Officers",
        "desc": f"Best B2B conferences for CROs and revenue leaders in {CURRENT_YEAR}. Real speaker and sponsor data from Dreamforce, SaaStr Annual, Sandler Summit, and OutBound Conference.",
        "intro": "Where CROs and revenue leaders actually show up — ranked by speaker seniority and sponsor intelligence, not conference marketing spend.",
        "sections": [
            ("The revenue leader conference stack", """<p>CROs and VP Sales have different conference needs than marketing leaders. They're looking for peer-to-peer content on pipeline, quota attainment, comp structure, and go-to-market execution — not brand awareness panels.</p>
<p>The conferences below have the highest concentration of sales leadership and revenue leadership speakers in our database. Dreamforce is the obvious anchor. SaaStr Annual draws the SaaS operator crowd. Sandler Summit and OutBound Conference are smaller but densely focused on sales craft.</p>"""),
            ("What sponsors signal about conference ROI", """<p>The sponsor list tells you who considers this audience worth a check. At sales leadership conferences, you'll see sales enablement tools, forecasting platforms, CRMs, and compensation software. That sponsor mix is a proxy for buyer intent.</p>
<p>We track sponsors across all 13 conferences in our database. If a company keeps showing up at the same events, they've likely validated the audience is worth it.</p>"""),
        ],
        "faqs": [
            ("Which conference is best for CROs specifically?", "Dreamforce has the largest overall presence including senior sales leadership. SaaStr Annual is strong for SaaS CROs. Sandler Summit focuses on sales methodology and draws sales leadership specifically. OutBound Conference focuses on outbound sales motion."),
            ("Do CRO-level speakers tend to appear at multiple conferences?", "Yes — our data shows a significant overlap of senior speakers across Dreamforce, SaaStr Annual, and the focused sales conferences. Multi-event speakers are a signal of genuine influence in the space."),
            ("What companies typically sponsor CRO-focused conferences?", "Common sponsors include sales engagement platforms, revenue intelligence tools, CRM vendors, and sales training providers. We track sponsor data for all 13 conferences in our database."),
        ],
        "conf_slugs": ["dreamforce", "saastr-annual", "sandler-summit", "outbound-conference"],
    },
    {
        "slug": "conferences-for-event-marketers",
        "title": f"Best Conferences for Event Marketing Managers {CURRENT_YEAR}",
        "h1": "Best Conferences for Event Marketing Managers",
        "desc": f"Best B2B conferences for event marketing managers in {CURRENT_YEAR}. Research INBOUND, Dreamforce, Spryng, and LeadsCon before you commit your event budget.",
        "intro": "You're the one deciding where to send the team and where to spend the sponsorship budget. Here's what the data says about which conferences are worth it.",
        "sections": [
            ("Research before you spend", """<p>The average B2B conference sponsorship runs $15K–$150K before you add travel, booth costs, and staff time. Most event marketers make those decisions based on vendor pitches and gut feel.</p>
<p>KeynoteData gives you actual speaker rosters, sponsor lists, and session data before you commit. You can see whether your target accounts are sending VP-level attendees, which competitors are sponsoring, and whether the conference audience matches your ICP.</p>"""),
            ("What the speaker roster tells you about audience quality", """<p>Conference marketing materials always claim the right audience. The speaker roster is a better signal. Conferences recruit speakers from their attendee base — so a high concentration of VP+ speakers suggests a high concentration of VP+ attendees.</p>
<p>We track seniority for every speaker in our database. Use that as a proxy for attendee seniority before you sign the sponsorship agreement.</p>"""),
        ],
        "faqs": [
            ("How do I evaluate whether a conference is worth sponsoring?", "Start with the speaker roster. High VP+ speaker concentration suggests high VP+ attendee concentration. Then check the sponsor list — if multiple direct competitors are sponsoring, there's likely validated audience match. Our database tracks both for 13 conferences."),
            ("Which conferences are best for B2B SaaS event marketers?", "INBOUND, Dreamforce, and SaaStr Annual have the largest overall scale. Spryng and LeadsCon are more focused and often have better attendee-to-sponsor ratios for niche B2B audiences."),
            ("Can I see which companies are sponsoring specific conferences?", "Yes — we track sponsor data including company name, tier, and cross-conference sponsorship history. Get access to the full database to see which companies keep showing up at which events."),
        ],
        "conf_slugs": ["inbound", "dreamforce", "spryng", "leadscon"],
    },
    {
        "slug": "conferences-for-demand-gen",
        "title": f"Best Conferences for Demand Generation Leaders {CURRENT_YEAR}",
        "h1": "Best Conferences for Demand Generation Leaders",
        "desc": f"Best B2B conferences for demand gen leaders in {CURRENT_YEAR}. INBOUND, LeadsCon, 6sense Breakthrough, and Spryng — ranked with real speaker and sponsor data.",
        "intro": "Demand gen conferences in 2026, ranked for the people building pipeline — not running brand awareness programs.",
        "sections": [
            ("Demand gen vs. brand marketing conferences", """<p>Not all marketing conferences are the same. Brand and content conferences (MozCon, Content Marketing World) draw editorial and SEO teams. Demand gen conferences draw the people responsible for pipeline numbers — paid media, email, lifecycle, and revenue marketing.</p>
<p>The conferences below draw the highest concentration of demand gen speakers and sponsors in our database. That's a proxy for who attends.</p>"""),
            ("The sponsor mix signals intent", """<p>At demand gen conferences, sponsors tend to be intent data platforms, marketing automation tools, ABM software, and data providers. If that's who's paying to be there, it's because that's who attends.</p>
<p>We track sponsors for all 13 conferences in our database. The 6sense Breakthrough conference in particular has strong intent data and ABM vendor presence, which reflects the audience composition.</p>"""),
        ],
        "faqs": [
            ("Which conference is best for demand gen specifically?", "LeadsCon is the most focused on demand gen and lead generation. 6sense Breakthrough draws ABM and intent data practitioners. INBOUND has the highest volume of demand gen speakers overall due to its scale."),
            ("Is INBOUND worth it for demand gen teams?", "INBOUND has 393 speakers and strong demand gen content tracks. The scale means more options but also more noise. LeadsCon and Spryng are smaller and more focused on performance and pipeline marketing."),
            ("What sponsors should I expect at demand gen conferences?", "Common sponsors include intent data platforms (6sense, Bombora), marketing automation tools, ABM platforms, data providers, and paid media technology. We track sponsor data across all 13 conferences."),
        ],
        "conf_slugs": ["inbound", "leadscon", "6sense-breakthrough", "spryng"],
    },
]


def build_role_pages(data):
    import json as _json
    speakers_by_conf = data['speakers_by_conference']
    all_confs_map = {c['slug']: c for c in data['conferences']}

    for page in ROLE_PAGES:
        slug = page['slug']

        # Build prose sections
        sections_html = ''
        for sec_title, sec_body in page['sections']:
            sections_html += f'<h2>{sec_title}</h2>\n{sec_body}\n'

        # Build FAQs
        faqs_html = ''
        faq_schema_items = []
        for q, a in page.get('faqs', []):
            faqs_html += f'<details class="faq-item"><summary class="faq-question">{q}</summary><div class="faq-answer"><p>{a}</p></div></details>'
            faq_schema_items.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}})
        faq_schema_str = _json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_schema_items})

        # Conference cards for this role
        conf_cards_html = ''
        for conf_slug in page['conf_slugs']:
            conf = all_confs_map.get(conf_slug)
            if not conf:
                continue
            desc = CONFERENCE_DESCRIPTIONS.get(conf_slug, '')
            top_speakers = speakers_by_conf.get(conf_slug, [])[:2]
            speaker_snippet = ', '.join(f'<strong>{s["name"]}</strong>' for s in top_speakers)
            loc_parts = [p for p in [conf.get('city'), conf.get('country')] if p]
            location = ', '.join(loc_parts) if loc_parts else 'International'
            stats_parts = []
            if conf.get('speaker_count'):
                stats_parts.append(f'{conf["speaker_count"]} speakers')
            if conf.get('sponsor_count'):
                stats_parts.append(f'{conf["sponsor_count"]} sponsors')
            stats_str = ' · '.join(stats_parts)

            conf_cards_html += f'''<a href="/conferences/{conf_slug}/" class="conf-card" style="display:block;">
<div class="conf-card-name">{conf["name"]}</div>
<div class="conf-card-meta">{location} · {stats_str}</div>
<p style="font-size:var(--text-sm);color:var(--color-text);margin:var(--space-2) 0 var(--space-1);">{desc.split(".")[0]}.</p>
{"<p style='font-size:var(--text-xs);color:var(--color-text-muted);font-family:var(--font-mono);'>Notable: " + speaker_snippet + "</p>" if speaker_snippet else ""}
</a>'''

        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
{html_head(
    title=f"{page['title']} | KeynoteData",
    desc=page['desc'],
    canonical=f"/{slug}/"
)}
<script type="application/ld+json">{faq_schema_str}</script>
</head>
<body>
{nav_html()}

<section class="page-header">
<div class="container">
{breadcrumb_html([("Home", "/"), (page["h1"], "")])}
<h1>{page["h1"]}</h1>
<p>{page["intro"]}</p>
</div>
</section>

<section>
<div class="container">
<div class="prose">{sections_html}</div>
</div>
</section>

<section class="data-section">
<div class="container">
<h2 class="section-title">Conferences in the database</h2>
<p class="section-subtitle">Full speaker and sponsor data available for these conferences.</p>
<div class="conference-grid">{conf_cards_html}</div>
</div>
</section>

{"<section class='faq-section'><div class='container'><h2 class='section-title'>Questions</h2><div class='faq-list'>" + faqs_html + "</div></div></section>" if faqs_html else ""}

<section class="cta-section">
<div class="container">
<h2>See the full speaker and sponsor data</h2>
<p>Filter by conference, seniority, and company. Export to CSV for your planning.</p>
<div class="cta-form-wrap">{email_form("Get Early Access")}</div>
</div>
</section>

{footer_html()}
</body>
</html>'''

        write_page(f'{slug}/index.html', html)


# =============================================================================
# ABOUT PAGE
# =============================================================================

def build_about_page(data):
    stats = data['stats']
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
{html_head(
    title="About KeynoteData — B2B Conference Intelligence",
    desc="KeynoteData tracks speakers, sponsors, and sessions at the top B2B SaaS conferences. Built for event marketers, PR agencies, and conference sponsors who need real data before they decide.",
    canonical="/about/"
)}
</head>
<body>
{nav_html()}

<section class="page-header">
<div class="container">
{breadcrumb_html([("Home", "/"), ("About", "")])}
<h1>About KeynoteData</h1>
<p>We built the database of B2B conference speakers, sponsors, and sessions that should have existed a long time ago.</p>
</div>
</section>

<section>
<div class="container-narrow">
<div class="prose">

<h2>The problem we're solving</h2>
<p>Every year, B2B marketing and sales teams spend tens of millions of dollars on conference sponsorships, speaking opportunities, and event attendance. Most of those decisions are made on gut feel and vendor sales pitches.</p>
<p>The data to make better decisions existed — scattered across hundreds of conference websites, LinkedIn profiles, and speaker directories. Nobody had organized it.</p>
<p>KeynoteData organizes it.</p>

<h2>What we track</h2>
<p>After each conference cycle, we scrape, clean, and enrich data from the top B2B SaaS conferences:</p>
<ul>
<li><strong>Speakers</strong> — {stats["total_speakers"]:,} speakers across {stats["conferences_with_data"]} conferences. Name, title, company, seniority tier, LinkedIn URL, and every conference they've spoken at.</li>
<li><strong>Sponsors</strong> — {stats["total_sponsors"]:,} sponsors with tier data and cross-conference sponsorship history.</li>
<li><strong>Sessions</strong> — {stats["total_sessions"]:,} session titles with format, track, and abstract data (where published).</li>
</ul>

<h2>Who we built this for</h2>
<p><strong>Event marketing managers</strong> at B2B SaaS companies who need to research a conference before they commit $20K–$200K. They want to know who's speaking, who's sponsoring, and whether their target accounts will be in the room.</p>
<p><strong>PR agencies</strong> doing speaker placement for B2B clients. They need to know which conferences feature speakers like their client, which events have gaps in their industry's representation, and how to pitch with data behind the recommendation.</p>
<p><strong>Conference sponsors</strong> evaluating whether to renew or expand their presence at an event. They want to track competitor sponsorship patterns and match speaker rosters against their target account list.</p>

<h2>The data methodology</h2>
<p>We collect data through a combination of automated scraping and manual review:</p>
<ul>
<li>Conference websites (speaker pages, sponsor lists, session schedules)</li>
<li>LinkedIn profile matching for speaker enrichment</li>
<li>Seniority classification based on title parsing</li>
<li>Manual quality review on edge cases</li>
</ul>
<p>We update after each conference cycle — typically 2-4 weeks after the event. Historical data goes back to 2024 for most conferences.</p>

<h2>Where we're headed</h2>
<p>Today: {stats["conferences_with_data"]} conferences with full data. By end of {CURRENT_YEAR}: 50+ conferences. Longer term: historical data going back to 2022, email enrichment for speakers, and API access.</p>
<p>We're building this in public, with early access customers helping shape the product. If you have a specific use case or data request, reach out.</p>

</div>
</div>
</section>

<section class="founders-section">
<div class="container">
<div class="founders-note">
<blockquote>"I built KeynoteData after spending tens of thousands of dollars on conferences where I had no idea who was speaking or why they were there. The data existed — scattered across conference websites, LinkedIn, and speaker directories. I just organized it."</blockquote>
<cite>— Rome, Founder of KeynoteData</cite>
</div>
</div>
</section>

<section class="cta-section">
<div class="container">
<h2>Get early access</h2>
<p>Be among the first to use the full database. Free to start.</p>
<div class="cta-form-wrap">{email_form("Get Early Access")}</div>
</div>
</section>

{footer_html()}
</body>
</html>'''

    write_page('about/index.html', html)

# =============================================================================
# PRICING PAGE
# =============================================================================

def build_pricing_page():
    tiers = [
        {
            "name": "Free",
            "price": "$0",
            "period": "no credit card",
            "features": [
                "Browse speaker database",
                "Top 10 speakers per conference",
                "Conference overview pages",
                "Basic seniority filters",
            ],
            "cta": "Get Started",
            "featured": False,
        },
        {
            "name": "Professional",
            "price": "$99",
            "period": "per month",
            "features": [
                "Full speaker database (887 speakers)",
                "Full sponsor database (487 sponsors)",
                "LinkedIn URLs for all speakers",
                "CSV export (speakers + sponsors)",
                "Filter by conference, seniority, function",
                "Session data and topics",
                "New conference data as released",
            ],
            "cta": "Get Early Access",
            "featured": True,
        },
        {
            "name": "Team",
            "price": "$249",
            "period": "per month",
            "features": [
                "Everything in Professional",
                "Up to 5 team seats",
                "Saved filters and watchlists",
                "Priority data updates",
                "Custom data pulls on request",
                "Slack support",
            ],
            "cta": "Contact Us",
            "featured": False,
        },
    ]

    pricing_cards = ''
    for tier in tiers:
        featured_class = "featured" if tier["featured"] else ""
        badge = '<div class="pricing-badge">Most Popular</div>' if tier["featured"] else ""
        features_html = ''.join(f'<li>{f}</li>' for f in tier["features"])
        cta_class = "btn-primary-block" if tier["featured"] else "btn-outline"
        pricing_cards += f'''<div class="pricing-card {featured_class}">
{badge}
<div class="pricing-card-name">{tier["name"]}</div>
<div class="pricing-card-price">{tier["price"]}</div>
<div class="pricing-card-period">{tier["period"]}</div>
<ul class="pricing-features">{features_html}</ul>
<button class="btn-primary {cta_class}">{tier["cta"]}</button>
</div>'''

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
{html_head(
    title="Pricing — KeynoteData",
    desc="KeynoteData pricing. Free to browse, $99/mo for the full speaker and sponsor database with CSV export. No credit card required to start.",
    canonical="/pricing/"
)}
</head>
<body>
{nav_html()}

<section class="page-header">
<div class="container">
{breadcrumb_html([("Home", "/"), ("Pricing", "")])}
<h1>Simple pricing</h1>
<p>Free to start. No credit card required. Upgrade when you need the full database.</p>
</div>
</section>

<section>
<div class="container">
<div class="pricing-cards">{pricing_cards}</div>
<p style="text-align:center;margin-top:var(--space-8);font-size:var(--text-sm);color:var(--color-text-muted);">
All plans include a 14-day free trial on paid features. Annual billing available (2 months free). Cancel anytime.
</p>
</div>
</section>

<section class="faq-section">
<div class="container">
<h2 class="section-title">Pricing questions</h2>
<div class="faq-list">
<details class="faq-item">
<summary class="faq-question">What's included in the free plan?</summary>
<div class="faq-answer">The free plan lets you browse conference pages, see the top 10 speakers per conference, and explore the database structure. You won't be able to export data or see LinkedIn URLs — those require a paid plan.</div>
</details>
<details class="faq-item">
<summary class="faq-question">How often is the database updated?</summary>
<div class="faq-answer">We update after each conference cycle — typically 2-4 weeks after an event. All plan tiers receive updates at the same time. Professional and Team plans get notifications when new conference data is added.</div>
</details>
<details class="faq-item">
<summary class="faq-question">Can I pay annually?</summary>
<div class="faq-answer">Yes. Annual billing is available on Professional and Team plans at 2 months free (10 months for the price of 12). Contact us to set up annual billing.</div>
</details>
<details class="faq-item">
<summary class="faq-question">Is there a trial period?</summary>
<div class="faq-answer">All paid plans include a 14-day free trial with full access to every feature. No credit card required to start the trial.</div>
</details>
<details class="faq-item">
<summary class="faq-question">What format is the CSV export?</summary>
<div class="faq-answer">Speaker exports include: name, title, company, seniority tier, function category, LinkedIn URL, and all conferences spoken at. Sponsor exports include: company name, website, tier, and all conferences sponsored. Both formats import directly into HubSpot, Salesforce, Clay, and Apollo.</div>
</details>
</div>
</div>
</section>

<section class="cta-section">
<div class="container">
<h2>Get early access</h2>
<p>We're offering early access pricing to the first 100 customers. Free to start.</p>
<div class="cta-form-wrap">{email_form("Get Early Access")}</div>
</div>
</section>

{footer_html()}
</body>
</html>'''

    write_page('pricing/index.html', html)

# =============================================================================
# SITEMAP + ROBOTS
# =============================================================================

def build_sitemap():
    today = BUILD_DATE
    urls = '\n'.join(
        f'''  <url>
    <loc>{SITE_URL}{p}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>{"1.0" if p == "/" else "0.8"}</priority>
  </url>'''
        for p in ALL_PAGES
    )
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>'''
    path = os.path.join(OUTPUT_DIR, 'sitemap.xml')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(xml)
    print('  + sitemap.xml')


def build_robots():
    txt = f'''User-agent: *
Allow: /
Sitemap: {SITE_URL}/sitemap.xml
'''
    path = os.path.join(OUTPUT_DIR, 'robots.txt')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(txt)
    print('  + robots.txt')


def build_cname():
    path = os.path.join(OUTPUT_DIR, 'CNAME')
    with open(path, 'w', encoding='utf-8') as f:
        f.write('keynotedata.com\n')
    print('  + CNAME')


def build_nojekyll():
    path = os.path.join(OUTPUT_DIR, '.nojekyll')
    with open(path, 'w', encoding='utf-8') as f:
        f.write('')
    print('  + .nojekyll')

# =============================================================================
# ASSET COPYING
# =============================================================================

def copy_assets():
    # CSS tokens
    css_dir = os.path.join(OUTPUT_DIR, 'assets', 'css')
    os.makedirs(css_dir, exist_ok=True)
    shutil.copy(
        os.path.join(BRAND_DIR, 'tokens.css'),
        os.path.join(css_dir, 'tokens.css')
    )
    # Write styles.css
    with open(os.path.join(css_dir, 'styles.css'), 'w', encoding='utf-8') as f:
        f.write(STYLES_CSS)
    # Write main.js
    js_dir = os.path.join(OUTPUT_DIR, 'assets', 'js')
    os.makedirs(js_dir, exist_ok=True)
    with open(os.path.join(js_dir, 'main.js'), 'w', encoding='utf-8') as f:
        f.write(MAIN_JS)
    # Favicons
    favicons_src = os.path.join(BRAND_DIR, 'favicons')
    favicons_dst = os.path.join(OUTPUT_DIR, 'favicons')
    if os.path.isdir(favicons_src):
        if os.path.exists(favicons_dst):
            shutil.rmtree(favicons_dst)
        shutil.copytree(favicons_src, favicons_dst)
    # Logos
    logos_src = os.path.join(BRAND_DIR, 'logos')
    logos_dst = os.path.join(OUTPUT_DIR, 'logos')
    if os.path.isdir(logos_src):
        if os.path.exists(logos_dst):
            shutil.rmtree(logos_dst)
        shutil.copytree(logos_src, logos_dst)
    print('  + assets (css, js, favicons, logos)')

# =============================================================================
# MAIN
# =============================================================================

def main():
    print(f"\nBuilding {SITE_NAME} → {OUTPUT_DIR}")
    print("=" * 50)

    # Fresh output directory
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    # Copy assets first
    print("\nAssets:")
    copy_assets()

    # Load data
    data = load_data()

    # Conferences with speaker data
    confs_with_data = [c for c in data['conferences'] if c['speaker_count'] > 0]
    confs_with_data.sort(key=lambda c: c['speaker_count'], reverse=True)

    # Build pages
    print("\nPages:")
    build_homepage(data)
    build_conference_index(data)

    for conf in confs_with_data:
        build_conference_page(conf, data)

    build_category_pages(data)
    build_roundup_pages(data)
    build_role_pages(data)
    build_about_page(data)
    build_pricing_page()

    # Sitemap + robots (must be after pages are registered)
    build_sitemap()
    build_robots()
    build_cname()
    build_nojekyll()

    total = len(ALL_PAGES)
    print(f"\n{'=' * 50}")
    print(f"Done. {total} pages generated.")
    print(f"Preview: cd output && python3 -m http.server 8089")
    print(f"URL: http://localhost:8089/\n")


if __name__ == '__main__':
    main()
