---
name: meta-ads-research
description: Deep pre-campaign research for a new Meta ads client. Produces a Creative DNA document (business analysis, personas, awareness stages, ad angles, 100 hooks, objection handling) as an Excel workbook from a Google Form intake. Used at new client onboarding and before any creative brief work.
---

# meta-ads-research

## When to Invoke

- New client onboarding (before any creative or campaign work)
- Creative refresh (existing client, new angle exploration)
- Competitor audit request

---

## Execution Notes

**Model routing:** Use the cheapest model that handles each task.

| Task | Model | Why |
|------|-------|-----|
| Phase 1 (form parsing) | Haiku | Structured data extraction |
| Phase 2 (client research) | Sonnet | Research + analysis |
| Phase 3 (competitor research) | Sonnet | Research + analysis at scale |
| Phase 4 (market sentiment) | Sonnet | Search + synthesis |
| Phase 4E (Foreplay API pull) | Haiku | API calls + file downloads |
| Phase 4.5 (research compression) | Opus | Needs to select the best quotes and data |
| Phase 5 (strategic assessment) | Opus | Awareness stages, sophistication, gaps, offer, format strategy |
| Phase 6 (workbook generation) | Opus | Complex synthesis across all research |
| Phase 7 (self-audit) | Opus | Catching subtle quality issues |
| Phase 8 (save + upload) | Haiku | File operations only |

**Single-pass rule:** Each phase runs ONCE. Do not re-run phases to "fill gaps." If a tool fails (login wall, credits exhausted), note the gap and move on. The research compression step handles missing data gracefully.

**Phase 4 runs as one agent.** All market research (Reddit, Amazon, Facebook Groups, Quora, YouTube, X/Twitter, Foreplay) in a single comprehensive pass. Do not split into multiple agents.

**Meta Ads Library runs once per brand** using the page_id extraction method (Steps 1-4 in Phase 2C). Do not fall back to keyword scrolling.

**Token Budget (approximate per run):**
- Phase 1 (Intake): ~1K tokens (Haiku)
- Phase 2 (Client): ~5K tokens (Sonnet)
- Phase 3 (Competitors, 3-5): ~15K tokens (Sonnet)
- Phase 4 (Market): ~10K tokens (Sonnet) + Perplexity API calls
- Phase 4.5 (Compression): ~3K tokens (Opus)
- Phase 5 (Strategy): ~8K tokens (Opus)
- Phase 6 (Workbook): ~15K tokens (Opus)
- Phase 7 (Audit): ~5K tokens (Opus)
- Phase 8 (Save/Upload): ~500 tokens (Haiku)
- **Estimated total: ~60K tokens** (~$2-4 per run depending on model pricing)

Estimates are approximate. Actual usage varies by competitor count and research depth. Update after real runs.

**Playwright Execution Defaults:**
- Default timeout: 30s with `wait_until="networkidle"`
- If page fails to load: retry once with `wait_until="domcontentloaded"` (faster, less strict)
- If retry fails: note the gap in research notes and proceed to the next step
- Cookie/popup handling: dismiss cookie banners and consent dialogs before screenshotting (common blocker for EU competitor sites)

**Subagent file reads (claude-mem File Read Gate):**
The claude-mem plugin runs a `PreToolUse` hook on `Read` that intercepts calls to any file with prior observations and returns a timeline instead of file content. The gate expects the caller to use `get_observations`, `smart_outline`, or `smart_unfold` to fetch what they need — but subagents don't have access to those MCP tools. Result: subagents either bail (first failure mode) or burn tokens on a redundant `cat` fallback.

When dispatching subagents in Phases 2-7, every prompt MUST include this guidance verbatim:

> **File reading:** Read project files via `cat <path>` in Bash, not the Read tool. The claude-mem File Read Gate will intercept Read calls on files with prior observations and the response cannot be acted on without MCP tools you do not have. Use `cat` for the input checkpoint files (intake, phase-2-client.md, phase-3-competitors.md, phase-4-sentiment.md, research-summary.md, phase-5-strategy.md). Read is fine for files you wrote yourself in this run.

This eliminates the gate-failure mode entirely and removes the 2-second-per-attempted-Read timeout penalty.

---

## Resuming a Partial Run

If resuming after a session crash or context limit, check `clients/[client-name]/research/` for existing checkpoint files:
- `phase-2-client.md` (Phase 2 complete)
- `phase-3-competitors.md` (Phase 3 complete)
- `phase-4-sentiment.md` (Phase 4 complete)
- `research-summary.md` (Phase 4.5 complete)

Each checkpoint file has a timestamp header (e.g., `# Generated: 2026-04-09`). Skip completed phases only if the checkpoint is less than 24 hours old. Older checkpoints are stale and should be re-run. To force a completely fresh run, delete the research folder.

---

## Phase 1: Intake from Google Form

Pull the latest form responses and let the user choose which client to research.

### 1A: Fetch Responses

Run:
```bash
gws forms forms responses list --params '{"formId": "11Hp3hDquXAaejM7_IXl4jN3Jto3f3OMfFCQRN1hV8YY"}' 2>/dev/null
```

Extract business names + submission dates from all responses using question ID `54a42aff` (business name).

Sort by `lastSubmittedTime` descending. Take the **last 5** with valid business names.

### 1B: Ask User to Select

Present the 5 most recent clients via `AskUserQuestion`:
- "Which client do you want to run research for?"
- Options: the 5 business names with submission dates

### 1C: Parse Selected Response

Pull the full response for the selected client and map question IDs to fields:

> **Note:** These question IDs are tied to the current Google Form structure. If the form is ever edited (questions added, removed, or reordered), these IDs must be updated.

```
QUESTION ID  | FIELD
-------------|------
54a42aff     | Business name
74e1e793     | Business address
36a3cf0f     | Primary contact name
226f19f9     | Contact number
7e8b9205     | Contact email
13e455f1     | Business overview
57a74ab2     | Key personas targeted
1b8450af     | Social media links
1e5e0a1d     | Website URL
43a2c4dc     | Competitors (3-5 with URLs)
011ec49c     | Top benefits
04d9772d     | USP vs competitors
532fee30     | Additional perks
0d855cff     | Active/planned promotions
498e2767     | Available resources
2ea8463e     | Monthly ad spend
2fd41ea4     | Business type (E-Commerce or Lead Gen)
151e1522     | Breakeven ROAS
41d2cbb9     | Product margins
04c23834     | Target KPIs
```

Build the working summary:

```
CLIENT: [business name]
TYPE: [E-Commerce or Lead Gen]
OFFER: [from business overview]
PRICING/MARGINS: [from margins + breakeven ROAS]
KEY BENEFITS: [from top benefits]
USP: [from USP field]
ADDITIONAL PERKS: [free shipping, guarantees, etc.]
PROMOTIONS: [active/planned]
COMPETITORS: [names + URLs]
WEBSITE: [URL]
SOCIAL: [links]
TARGET PERSONAS: [from form]
AD SPEND: [monthly budget]
TARGET KPIs: [from form]
AVAILABLE RESOURCES: [from resources field]
```

Use this summary as the working reference for all subsequent phases.

**Validation:** After parsing, verify that `Business name` and `Website URL` are non-empty and sensible (a URL should be in the URL field, not the name field). If either core field is empty or looks wrong, halt and ask the user via `AskUserQuestion`: "Form field mapping may be outdated. Got [business name: X, website: Y]. Does this look right?" If `Competitors` is empty, warn the user but proceed (some clients don't list competitors upfront).

---

## Phase 2: Client Research

**Strategic question: "How is the brand positioning itself?"**

### 2A: Website (Visual + Content)
Use `playwright` to visit the client's main website and key landing pages. Screenshot each page, then extract page content via `page.content()` in the same visit.

If content extraction misses dynamic content (SPAs, lazy-loaded sections), fall back to `firecrawl-scrape` for clean markdown.

Look for:
- Overall layout and visual hierarchy
- How CTAs are positioned and styled
- Trust signals (badges, logos, testimonials placement)
- Popups, banners, or offers shown on load
- Mobile experience and responsiveness
- General design quality and brand feel
- Core messaging and positioning
- How they describe their offer and benefits
- Price anchoring and offers
- CTA language
- Social proof (reviews, testimonials, stats)

### 2B: Meta Ads Library
Use `playwright` to find the advertiser's full ad catalog. Do NOT just scroll through keyword search results.

**Step 1: Search by keyword**
```python
url = "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&q=[BRAND_NAME]&search_type=keyword_unordered&media_type=all"
page.goto(url, wait_until="networkidle", timeout=30000)
time.sleep(5)
```

**Step 2: Extract page_id + page_name pairs from the page source**
The search results page contains JSON with page_id and page_name for every advertiser shown. Extract pairs using the primary regex, with a backup pattern:
```python
import re
html = page.content()
# Primary pattern
pairs = re.findall(r'"page_id"\s*:\s*"?(\d+)"?.*?"page_name"\s*:\s*"([^"]+)"', html)
# Backup pattern (Facebook sometimes uses this format)
if not pairs:
    pairs = re.findall(r'"pageID"\s*:\s*"(\d+)".*?"name"\s*:\s*"([^"]+)"', html)
# Build unique map
page_map = {}
for pid, name in pairs:
    name_clean = name.replace('\\/', '/')  # JSON escapes slashes
    if pid not in page_map:
        page_map[pid] = name_clean

# Validate extraction worked
if not page_map:
    print("SCRAPE FAILURE: No page_id/page_name pairs found in HTML. Facebook may have changed their page structure.")
```

**Step 3: Match the brand by page_name (not HTML content)**
Match the brand name against the `page_name` field. Do NOT match against the full HTML (other advertisers mention competitor brands in their ad copy).
```python
brand_lower = '[BRAND_NAME]'.lower()
matched_pid = None
for pid, name in page_map.items():
    if brand_lower in name.lower() or name.lower() in brand_lower:
        matched_pid = pid
        break
```

**Step 4: Load the full ad catalog**
```python
catalog_url = f"https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&view_all_page_id={matched_pid}"
```
Screenshot the page and scroll to capture more ads.

**Fallback chain (if no page_name matches):**
1. Search by the brand's website domain instead of brand name
2. Search by the brand's Facebook Page URL from intake
3. If all fail, log as explicit gap: "Could not find [brand] in Meta Ads Library. Proceeding without client ad data."

Look for:
- Total number of active ads
- Formats in use (image, video, carousel)
- Hook styles and opening lines
- Offers being tested (discount, guarantee, FOMO)
- How long ads have been running (longer = proven)
- Gaps: what angles they're NOT testing

### 2C: Social Media
Use `playwright` to visit their Instagram and Facebook pages.

Look for:
- Tone of voice
- Content themes
- What gets engagement vs. what doesn't
- How they talk to their audience

**Checkpoint:** Save research to `clients/[client-name]/research/phase-2-client.md` with a timestamp header (e.g., `# Generated: 2026-04-09`).

---

## Phase 3: Competitor Research

**Strategic question: "What is the competitive landscape? Where are weaknesses?"**

For EACH competitor in the intake:

### 3A: Competitor Website (Visual + Content)
Use `playwright` to visit the competitor's homepage and key pages. Screenshot and extract content in the same visit. Fall back to `firecrawl-scrape` for JS-heavy sites.

Look for:
- Overall design quality and brand positioning
- How they present pricing and offers
- Trust signals, guarantees, and risk-reversal placement
- CTA style and placement vs. client
- UX differences that stand out
- Positioning and USP
- Pricing vs. client
- Guarantees and risk-reversal offers
- Messaging strengths and gaps

### 3B: Competitor Meta Ads Library
Use `playwright` to find each competitor's full ad catalog. Follow the same 4-step process as 2B:

1. Search Ad Library by competitor name (keyword_unordered)
2. Extract page IDs from page source using primary + backup regex patterns
3. Try each page ID, load `view_all_page_id=[ID]`, check if brand name matches
4. Once on the correct page, screenshot and analyze their full catalog

Do NOT just scroll through keyword search results. Get to the page-level view.

**Fallback:** If competitor name returns no results, search by their website domain or Facebook Page URL from the intake form.

Identify winning ads by:
- Ads running the longest (date started, still active)
- Ads with the most variations (more variants = more spend = it's working)
- Recurring hooks or formats across multiple ads

Save top 5 competitor ad screenshots across all competitors to `clients/[client-name]/research/competitor-creatives/top-winners/` for Tab 12 visual references.

### 3B-ii: Competitor TikTok Ads
Use `WebSearch` (Perplexity) to find competitor TikTok ad activity:
- `"[competitor name]" tiktok ads creative center top performing`
- `"[product category]" tiktok ad trends hooks`

Then use `playwright` to visit `https://ads.tiktok.com/business/creativecenter/inspiration/topads/pc/en` and search by category keyword. Screenshot the top 5 results.

Extract:
- Hook style (text overlay, talking head, product demo, UGC)
- Format (vertical video duration, editing style)
- CTA approach
- What's working on TikTok that isn't being used on Meta

### 3B-iii: Competitor Search Ads
Use `WebSearch` (Perplexity) to find competitor Google Ads intelligence:
- `"[competitor name]" google ads copy headlines`
- `"[product category]" PPC landing page messaging`

Use `playwright` to Google `[product category]` and screenshot the sponsored results to capture which competitors are bidding and their ad copy.

Extract:
- Recurring headlines and descriptions
- Offer framing in search ads vs. social ads
- CTA language differences
- Landing page type from display URLs

### 3B-iv: Competitor Ad Landing Pages
After Phase 3B captures competitor ad catalogs, extract 3-5 unique destination URLs per competitor from the Meta Ads Library ad cards.

Visit each with `playwright` (screenshot) and `firecrawl-scrape` (content).

Analyze:
- Page type (collection vs PDP vs bundle vs quiz vs homepage)
- Headline and subhead messaging
- CTA placement and copy
- Offer structure (discount, bundle, free shipping threshold)
- Trust signals (reviews count, badges, guarantees)
- Above-the-fold content vs. below-the-fold

Feed directly into Tab 12's Landing Page Patterns section.

### 3C: Competitor Reviews (Visual + Content)
Use `playwright` to visit:
- `https://www.trustpilot.com/review/[competitor-domain]`
- `https://www.reviews.io/company-reviews/store/[competitor-domain]`

Browse the review pages to get the full picture: star distribution, review volume, how the company responds, and overall sentiment at a glance. Then extract text content from the same pages.

Mine for:
- Recurring complaints (durability, shipping, customer service, returns)
- What customers wish the product did better
- Exact language customers use to describe their problems
- 3-star reviews (most honest: like something, have a gripe)

### 3C-ii: Competitor Google Reviews
Use `WebSearch` (Perplexity) to find Google Business Profile data:
- `"[competitor name]" google reviews rating`
- `"[competitor name]" google maps reviews complaints`

If Perplexity surfaces a Google Maps listing, use `playwright` to visit it and screenshot the review summary.

Extract:
- Star rating and review count
- Top 3 recurring complaints
- Top 3 recurring praise themes
- Whether the business responds to reviews (signals brand maturity)

Feed into Tab 3 (Competitive Gap) and Tab 9 (Objections).

**Checkpoint:** Save research to `clients/[client-name]/research/phase-3-competitors.md` with a timestamp header.

---

## Phase 4: Market & Sentiment Research

**Strategic question: "What are customers saying in their own words? Where are the gaps?"**

**Primary search tool for all Phase 4 discovery:** Use Perplexity (sonar-pro via WebSearch). It handles Reddit, Quora, Amazon, and community content better than Firecrawl. Use Playwright only for deep-reading specific pages Perplexity surfaces.

**Source relevance filter:** Not every source applies to every client. Use this as a default:
- **E-Commerce:** All sources (Reddit, Amazon, Facebook Groups, Quora, YouTube, X/Twitter, Foreplay)
- **Lead Gen:** Skip Amazon, deprioritize Quora. Focus on Reddit, Facebook Groups, YouTube, X/Twitter, Foreplay
- **B2B:** Skip Amazon + Facebook Groups. Prioritize Reddit, YouTube, X/Twitter, Foreplay

The agent can still check a "skipped" source if it suspects relevance for a specific client.

### 4A: Reddit Research (Discovery)
Use `WebSearch` (Perplexity) with these query patterns:
- `"[product category]" reddit`
- `"[competitor name] review" reddit`
- `"best [product category]" reddit`
- `"[product category] frustrations" OR "complaints" reddit`

### 4A-ii: Reddit Research (Deep Read)
Use `playwright` to visit the top threads found in 4A. Read full comment chains for context that snippets miss.

Extract:
- Recurring frustrations
- What people love about the category
- Questions and doubts before buying
- Exact phrases and words customers use

### 4B: Facebook Groups
Use `WebSearch` (Perplexity) to find relevant Facebook Group discussions:
- `"[product category]" facebook group recommendations`
- `"[product category] community" women apparel recommendations`

Use `playwright` to visit the top groups and read recent discussions/comments.

Extract:
- Common complaints and recommendations
- Questions people ask before buying
- How members describe their problems and needs
- Brand mentions (client or competitors)

### 4C: Quora
Use `WebSearch` (Perplexity) with:
- `"[product category]" quora`
- `"best [product category]" quora`
- `"[product category] worth it" quora`

Use `playwright` to visit the top answers.

Extract:
- How people describe their problems in their own words
- What solutions they've already tried
- What they wish existed
- Objections and hesitations

### 4D: YouTube Research
Use `WebSearch` (Perplexity) to discover top videos:
- `"[product category] review" youtube most viewed`
- `"best [product category]" youtube`

Capture the top 5-10 video titles + view counts from results. Log which title formats get the most views (these are proven hooks).

Then use `playwright` to visit the top 2-3 videos. Read comment sections for unfiltered reactions.

Extract:
- Video title patterns that drive views (feed into Tab 8 as "Video-Proven Hooks")
- What viewers praise or complain about
- Questions they ask
- Alternative products they mention
- Emotional language and frustrations

### 4E: foreplay.co API

**Base URL:** `https://public.api.foreplay.co`
**Endpoint:** `/api/discovery/ads`
**Auth:** `Authorization: [FOREPLAY_API_KEY]` header (no Bearer prefix)

Pull **15-20 ads per competitor** plus 2 broader category searches:

```bash
# Per competitor (repeat for each)
curl -s -H "Authorization: $FOREPLAY_API_KEY" \
  "https://public.api.foreplay.co/api/discovery/ads?query=[COMPETITOR]+golf&limit=20&order=longest_running"

# Broader category searches
curl -s -H "Authorization: $FOREPLAY_API_KEY" \
  "https://public.api.foreplay.co/api/discovery/ads?query=women+golf+apparel&limit=20&order=longest_running"
```

For each ad, extract: headline, description, cta_title, display_format, publisher_platform, running_duration, link_url, full_transcription, image/video/thumbnail URLs.

Download all images and videos to: `clients/[client-name]/research/competitor-creatives/foreplay/[brand-slug]/`

**Fallback chain (if `FOREPLAY_API_KEY` not in `.env`):**
1. Extend the Meta Ads Library scrape from Phase 3B: scroll deeper per competitor, capture 30+ ads instead of a single page of results
2. Extract hook text, format, and CTA directly from the ad cards via Playwright
3. Note reduced fidelity in `research-summary.md` so downstream phases know Foreplay data is absent

### 4F: Amazon Reviews (if applicable)

Use `playwright` to visit top competitor product pages on Amazon. Browse the review section to see star distribution, photo reviews, and top highlighted reviews. Extract text content from the same pages.

Focus on:
- 3-star reviews (most balanced, most honest)
- Recurring themes in 1-star reviews (deal breakers)
- What 5-star reviews praise most (proof points)

### 4G: X/Twitter Research
Use `WebSearch` (Perplexity) with:
- `"[product category]" site:x.com recommendations OR complaints`
- `"[competitor name]" site:x.com review OR problem`
- `"[brand name]" site:x.com complaint OR love`

Use `playwright` to visit any high-engagement threads Perplexity surfaces.

Extract:
- Recurring sentiment (positive and negative)
- Viral complaints or praise
- How the brand responds publicly (if at all)
- Category-level takes and trends

Feed into Tab 4 (Personas, pain points) and Tab 9 (Objections).

### 4H: Seasonal/Timing Intelligence
Use `WebSearch` (Perplexity) with:
- `"[product category]" seasonal trends buying peak months`

Extract 3-5 bullet points: peak season, off-season dynamics, upcoming events or holidays relevant to the category. Feed into the Quick Start tab's Timing Notes section.

**Checkpoint:** Save research to `clients/[client-name]/research/phase-4-sentiment.md` with a timestamp header.

---

## Phase 4.5: Research Compression

Before moving to strategy and workbook generation, compress all raw research into a single summary document (~5K tokens). This is the PRIMARY input for Phase 5-7 agents.

Read all research files in `clients/[client-name]/research/` and produce a condensed summary:

1. **Client positioning** (3-5 bullet points from Phase 2)
2. **Top 20 customer quotes** (exact language from Reddit, reviews, forums, Amazon, X/Twitter)
3. **Competitor comparison matrix** (1-line positioning + key weakness per competitor)
4. **Competitor ad intel** (longest running ads, winning formats, hooks from Foreplay + Meta Ads Library + TikTok)
5. **Search ad intel** (competitor PPC messaging patterns, landing page types)
6. **Market stats** (participation numbers, growth trends, market size)
7. **Gap analysis highlights** (top 5 saturated angles, top 5 open spaces)
8. **Key objections** (top 5 recurring objections from all sources)
9. **Seasonal notes** (peak/off-season, relevant events)

Save to: `clients/[client-name]/research/research-summary.md`

**Quality Gate:** After producing the summary, verify:
- At least 10 customer quotes contain specific product/category language (not generic sentiment like "great product" or "love it")
- Every competitor from intake appears in the comparison matrix
- Gap analysis has both "saturated" and "open space" entries

If any check fails, re-read the raw research files for the missing section and patch the summary. If fewer than 10 specific quotes are available from research, note thin data in the summary header: `**Data note:** Limited customer language found ([N] specific quotes). Downstream phases should compensate with more inference and flag lower-confidence outputs.`

**Important:** The raw research files are ALSO available. The workbook agent should reference them directly for detail-heavy tabs (Hooks, Angles, Objections) where exact customer language matters most. The summary handles everything else.

---

## Phase 5: Strategic Assessment

Using the research summary (primary) and raw files (for detail), build the strategic layer.

### 5A: Persona Validation

Before building frameworks, cross-reference client-supplied personas (from intake field `57a74ab2`) against actual customer language from Phase 4 research.

- Do real people in Reddit threads, reviews, and forums match the personas the client described?
- Split any persona that covers two distinct segments
- Merge personas that are functionally identical
- Flag any client-supplied persona that has zero supporting evidence in research
- Flag any segment that emerged from research but wasn't in the intake

Produce the final 5 personas that will be used for all subsequent tabs.

### 5B: 5 Stages of Awareness Mapping

For each of the 5 validated personas, map where they fall across Eugene Schwartz's awareness stages:

| Stage | Definition | Messaging Approach |
|-------|-----------|-------------------|
| **Unaware** | Don't know they have a problem | Lead with the problem. Agitate. Use storytelling. |
| **Problem Aware** | Know the problem, don't know solutions exist | Name the problem. Introduce the solution category. |
| **Solution Aware** | Know solutions exist, don't know your product | Differentiate. Why THIS solution over alternatives? |
| **Product Aware** | Know your product, haven't bought yet | Overcome objections. Social proof. Risk reversal. |
| **Most Aware** | Know your product well, need a push to buy | Offers, urgency, new angles, retargeting hooks. |

For each persona x awareness stage combination, note:
- What messaging works at this stage
- What messaging does NOT work (too early/too late)
- 2-3 example hook directions
- Estimated volume: high/medium/low

**Volume estimation methodology:** Use research data as proxies:
- **Problem Aware volume:** Reddit/forum thread count discussing the problem. 5+ threads in the last year = High. 2-4 = Medium. 0-1 = Low.
- **Solution Aware volume:** Competitor ad duration at this stage. If competitor ads targeting Solution Aware have been running 90+ days, the audience is large = High.
- **Product Aware volume:** Branded search mentions and review volume for the client. High review count + branded Reddit mentions = High.
- **Unaware and Most Aware:** Estimate relative to the other three stages. Unaware is typically High for broad categories, Low for niche. Most Aware scales with how long the brand has been running ads.

Identify which awareness stage has the most volume for each persona (where to focus spend).

### 5C: Market Sophistication Analysis

Assess the market sophistication level (Eugene Schwartz scale 1-5):

1. **Level 1**: Be first. Simple, direct claim. ("Lose weight fast.")
2. **Level 2**: Enlarge the claim. Bigger, bolder. ("Lose 30 pounds in 30 days.")
3. **Level 3**: Add a mechanism. HOW it works. ("Our patented thermogenic formula...")
4. **Level 4**: Enlarge the mechanism. More specific, more credible. ("3-phase metabolic reset backed by...")
5. **Level 5**: Identification. Connect with who the customer IS. ("For busy moms who...")

Determine:
- What level is the market currently at?
- What claims have ALL competitors already made? (worn out)
- What level of specificity is needed to stand out?
- What mechanisms or proof points are underused?
- What is the next move to cut through?

### 5D: Competitive Gap Analysis

Synthesize all competitor research into a gap map:
- What competitors are ALL doing the same way (saturated angles)
- What NONE of them are addressing (open space)
- Underserved customer segments
- Messaging white space (untapped angles, unaddressed objections)
- Creative format gaps (formats no one is using that could work)

### 5E: Offer Strength Assessment

Evaluate the client's offer against competitor offers identified in Phase 3:

- **Price positioning:** Premium, mid-market, or budget relative to competitors?
- **Risk reversal:** Does the client have a guarantee, free trial, or free shipping? How does it compare to competitors?
- **Urgency mechanics:** Scarcity, time limits, limited editions?
- **Perceived value:** Does the offer feel like a deal at the listed price?

Output an offer strength rating:
- **Strong:** Competitive or better on 3+ dimensions. Ready to scale.
- **Needs Work:** Competitive on 1-2 dimensions. Recommend specific improvements before heavy spend.
- **Weak:** Below competitors on most dimensions. Flag prominently in the Quick Start tab as "improve offer before scaling ad spend."

Include specific recommendations for strengthening the offer (e.g., "Add a 30-day money-back guarantee to match [Competitor X]", "Bundle [product] with [accessory] to increase perceived value").

### 5F: Creative Format Strategy

Cross-reference:
- Competitor format patterns from Phase 3B (what formats are winning)
- Client resources from intake field `498e2767` (what they can produce)
- Monthly ad spend from intake (budget constraints)

Output a prioritized format list:
- "Given your [$X] budget and [resources available], start with [format 1], then test [format 2]. Deprioritize [format 3] until [condition]."
- If client has no video production capability, don't recommend UGC video as the top priority
- If budget is under $3k/month, recommend max 2 formats to avoid spreading too thin

---

## Phase 6: Synthesis and Output

Using all research and strategic assessment, produce the full Creative DNA as an Excel workbook.

### Workbook Structure (12 Tabs)

**Tab 0: Quick Start**
Executive summary for the media buyer. Everything needed to launch the first test on one page:
- Client name and business type
- **Top 3 angles to test first** (from prioritized Tab 7, "Test First" tier)
- **5 highest-confidence hooks per angle** (15 hooks total, cherry-picked from Tab 8)
- **Recommended first campaign structure:** which persona, which awareness stage, which format, TOF/MOF/BOF split
- **3 biggest competitive gaps to exploit** (from Tab 3)
- **Offer strength rating** with any recommendations (from Phase 5E)
- **Format priority:** what to produce first given client resources and budget (from Phase 5F)
- **Budget allocation:** Recommended starting % split across TOF/MOF/BOF based on spend level. Rule of thumb: $500 minimum per angle test. If budget is $3k/month, test max 3 angles. If $5k+, test up to 5. Disclaimer: "Suggested starting allocation for new accounts. Adjust based on early performance data."
- **Timing notes:** Peak season, off-season angles, upcoming relevant events (from Phase 4H)

**Tab 1: Overview**
- Client name, business type, website
- Offer summary, pricing, margins
- Key benefits, USP, perks
- Target KPIs, ad spend, breakeven ROAS

**Tab 2: Business Analysis**
- Business overview (2-3 paragraphs)
- Products and services breakdown
- Main benefits with proof points
- Unique differentiators (reference competitor weaknesses)

**Tab 3: Competitive Gap Analysis**
- Competitor comparison matrix (positioning, pricing, guarantees, messaging)
- **Search ad intel row** (competitor PPC messaging patterns, landing page types from Phase 3B-iii)
- Saturated angles (what everyone is doing)
- Open space (what no one is doing)
- Underserved segments
- Messaging white space

**Tab 4: Customer Personas**
For each of 5 validated personas:
- Demographic profile (age, income, location, lifestyle, education, tech adoption)
- Psychographic characteristics (2-3 sentences: how they think, what they value)
- Pain points (5 specific frustrations)
- Motivators (5 drivers to buy)
- Possible objections (5 hesitations)
- Messaging to overcome objections (5 specific copy lines)

**Tab 5: Awareness Stages**
Matrix: 5 personas x 5 awareness stages
For each cell:
- Messaging approach
- What works / what doesn't
- Example hook directions
- Estimated volume (high/medium/low) with proxy reasoning

**Tab 6: Market Sophistication**
- Current sophistication level (1-5) with reasoning
- Worn-out claims in this market
- Fresh angles and mechanisms
- Recommended sophistication strategy

**Tab 7: Angles**
10-15 copywriting angles. For each:
- Angle name
- Core theme (1 sentence)
- 5 application examples (ready-to-use ad body copy)
- Best-fit personas (primary + secondary)
- Best-fit awareness stages
- **Funnel stage:** TOF, MOF, or BOF (mapping: Unaware + Problem Aware = TOF, Solution Aware = MOF, Product Aware + Most Aware = BOF)
- **Priority:** "Test First" (top 3), "Test Next" (next 5), or "Test Later" (remainder). Rank by: strength of supporting evidence from research, competitive gap size, audience volume at target awareness stage.

**Tab 8: Hooks**
100 hooks total, organized by awareness stage (20 per stage).
For each hook:
- Hook text
- Hook type (question, stat, story, bold claim, pattern interrupt, before/after, testimonial, controversy, curiosity gap, direct address)
- Target persona
- Awareness stage
- **Funnel stage:** TOF, MOF, or BOF
- **Format fit:** `static`, `video-opener`, `carousel-slide-1`, `story/reel`, `UGC-script` (tag best-fit formats)

Include a "Video-Proven Hooks" subset: hooks derived from high-view-count YouTube title patterns identified in Phase 4D.

**Tab 9: Objections & Handling**
For each persona:
- Top 5 objections
- For each objection: specific counter-messaging (not generic)
- Supporting proof points from research (reviews, stats, testimonials)
- Source attribution (e.g., "recurring complaint on Trustpilot", "3-star Amazon reviews", "Google review theme")

**Tab 10: Messaging Strategies**
Angle-to-persona mapping:
- For each persona: primary angles (top 3 with reasoning), secondary angles (3-6)
- Recommended campaign approach per persona (lead message, creative direction, tone, imagery, CTA style)
- **Avoid column:** 2-3 messaging approaches that will fail per persona, with reasoning (e.g., "Don't lead with price for Persona 2 (luxury buyer), it signals low quality"). Source from awareness stage mapping (wrong-stage messages) and competitor research (worn-out claims).

**Tab 11: Testing Framework**

Benchmarks calibrated for the client's business type and price point. Include a note: "Benchmarks calibrated for [E-Commerce/Lead Gen] at [$X] AOV."

**E-Commerce benchmarks:**
| Metric | Benchmark | Winning Threshold |
|--------|-----------|-------------------|
| CTR | 1-3% | 2-4%+ |
| CPC | $0.50-$1.50 | $0.30-$0.80 |
| Conversion Rate | 2-5% | 4-8%+ |
| CPA | Target <30% of AOV | Target <20% of AOV |
| ROAS | 2-4x | 3-5x+ |

**Lead Gen benchmarks:**
| Metric | Benchmark | Winning Threshold |
|--------|-----------|-------------------|
| CTR | 1-2.5% | 2-3.5%+ |
| CPC | $1-$3 | $0.50-$1.50 |
| Lead Conv Rate | 5-15% | 10-25%+ |
| CPL | Varies by industry | Target <50% of LTV |
| Lead Quality | 20-40% qualified | 40-60%+ qualified |

Angle testing decision tree:
- Q1: Is CTR above benchmark? YES: proceed / NO: adjust hook, creative, or audience
- Q2: Is conversion rate above benchmark? YES: scale / NO: test different CTA, offer, or landing page
- Q3: Is CPA/CPL below target? YES: scale aggressively / NO: optimize or cut
- Q4: Is ROAS above target (e-com) or lead quality above threshold (lead gen)? YES: maximize budget / NO: continue testing

**Tab 12: Winning Ad Pattern Analysis**
Synthesize Foreplay API data + Meta Ads Library data + TikTok Creative Center data into:
1. Competitor Ad Spend Overview (table: brand, active ads, longest running, format mix, spend signal)
2. Format Patterns (which formats run longest, winner signals)
3. Hook Patterns from Proven Winners (actual copy from longest-running ads)
4. Copy Structure Patterns (short+punchy vs long-form vs emotional vs trend vs scarcity)
5. Landing Page Patterns (collection vs PDP vs bundle vs homepage, with real data from Phase 3B-iv destination URL analysis)
6. Transcription/Video Script Patterns (from Foreplay video transcriptions)
7. **Cross-Platform Signals** (TikTok ad patterns that translate to Meta: hook styles, UGC formats, trending approaches from Phase 3B-ii)
8. Creative Gaps (what nobody is doing, ranked by priority for client)
9. Recommended Test Matrix (10 test concepts with format, persona, awareness stage, funnel stage, weekly priority)
10. **Reference Screenshots** column: file paths to top competitor ad screenshots saved in `clients/[client-name]/research/competitor-creatives/top-winners/`

### Generate the Workbook

Use Python with openpyxl to create the `.xlsx` file:
```bash
pip install openpyxl  # if not already installed
```

Wrap the full generation in a try/except. If the script crashes mid-generation, save whatever tabs have been completed so far. After generation, verify the workbook has all 12 expected tabs (Tab 0 through Tab 12) and flag any that are missing.

Save locally to: `clients/[client-name]/deliverables/[client-name]-creative-dna.xlsx`

---

## Phase 7: Self-Audit

Before saving and uploading, run a targeted quality check on the tabs most prone to quality drift.

**Full audit (read every row, flag issues):**
- **Tab 7 (Angles):** Confirm no two angles are the same idea reworded. Each should be a genuinely different strategic approach.
- **Tab 8 (Hooks):** Flag any hook that could apply to any product. If it's not specific to this client's category, rewrite it.
- **Tab 9 (Objections):** Flag any counter-messaging that is generic ("High quality" is not copy). Every response must be specific and backed by research.

**Spot-check (scan for obvious issues):**
- **Tab 4 (Personas):** Verify psychographic sections feel like a specific real person, not a demographic checklist.
- **Tab 12 (Winning Patterns):** Verify claims about competitor patterns are backed by actual data from research phases.

**Skip (covered by inline quality gates or derived from audited tabs):**
- Tabs 0, 1, 3, 5, 6, 10, 11

For flagged issues:
1. Rewrite with specific, concrete language
2. Ensure customer language from Reddit/reviews/groups/Quora/X is woven into hooks and angles
3. Regenerate the workbook with corrections applied

---

## Phase 8: Save and Upload

### 8A: Save Locally
Save to both locations:
- `clients/[client-name]/research/[client-name]-creative-dna.xlsx` (research folder, for future reference)
- `clients/[client-name]/deliverables/[client-name]-creative-dna.xlsx` (deliverables folder)

### 8B: Upload to Google Drive
Upload the workbook to the client's **Research/** subfolder in Drive.

1. Find the client's "[Client] x GrowthQuest" folder:
```bash
gws drive files list --params '{"q": "name contains \"x GrowthQuest\" and mimeType=\"application/vnd.google-apps.folder\"", "fields": "files(id,name)"}' 2>/dev/null
```
Fuzzy-match the client name to find the right folder.

**Confirmation:** After matching, surface the folder name to the user via `AskUserQuestion`: "Found Drive folder: [N]. [Client Name] / [Client Name] x GrowthQuest. Upload here?" Only proceed on confirmation.

2. Find the **Research/** subfolder inside it:
```bash
gws drive files list --params '{"q": "\"[CLIENT_X_GQ_FOLDER_ID]\" in parents and name=\"Research\" and mimeType=\"application/vnd.google-apps.folder\"", "fields": "files(id,name)"}' 2>/dev/null
```

3. If the client folder doesn't exist yet, create the full structure:

```bash
# Step 1: Find the next number by listing existing folders
gws drive files list --params '{"q": "\"1XhmRthEr31oJ1Yd5eWu7pv68OIPziOm2\" in parents and mimeType=\"application/vnd.google-apps.folder\"", "fields": "files(name)", "pageSize": 50}' 2>/dev/null
# Parse the highest number and increment by 1

# Step 2: Create numbered client folder in GQ Clients
gws drive files create --json '{"name": "[N]. [Client Name]", "mimeType": "application/vnd.google-apps.folder", "parents": ["1XhmRthEr31oJ1Yd5eWu7pv68OIPziOm2"]}'
# Save the returned ID as CLIENT_FOLDER_ID

# Step 3: Create "[Client Name] x GrowthQuest" inside it
gws drive files create --json '{"name": "[Client Name] x GrowthQuest", "mimeType": "application/vnd.google-apps.folder", "parents": ["CLIENT_FOLDER_ID"]}'
# Save the returned ID as XGQ_FOLDER_ID

# Step 4: Create all standard subfolders inside "[Client Name] x GrowthQuest"
# Create each one and save the returned ID
gws drive files create --json '{"name": "Research", "mimeType": "application/vnd.google-apps.folder", "parents": ["XGQ_FOLDER_ID"]}'
gws drive files create --json '{"name": "Briefs", "mimeType": "application/vnd.google-apps.folder", "parents": ["XGQ_FOLDER_ID"]}'
gws drive files create --json '{"name": "Creatives", "mimeType": "application/vnd.google-apps.folder", "parents": ["XGQ_FOLDER_ID"]}'
gws drive files create --json '{"name": "Reports", "mimeType": "application/vnd.google-apps.folder", "parents": ["XGQ_FOLDER_ID"]}'
gws drive files create --json '{"name": "Brand Assets", "mimeType": "application/vnd.google-apps.folder", "parents": ["XGQ_FOLDER_ID"]}'
gws drive files create --json '{"name": "Strategy", "mimeType": "application/vnd.google-apps.folder", "parents": ["XGQ_FOLDER_ID"]}'

# Step 5: Create sub-subfolders
# Inside Briefs: create References/
gws drive files create --json '{"name": "References", "mimeType": "application/vnd.google-apps.folder", "parents": ["BRIEFS_FOLDER_ID"]}'

# Inside Creatives: create Winning/
gws drive files create --json '{"name": "Winning", "mimeType": "application/vnd.google-apps.folder", "parents": ["CREATIVES_FOLDER_ID"]}'

# Inside Brand Assets: create Logos/ and Photos/
gws drive files create --json '{"name": "Logos", "mimeType": "application/vnd.google-apps.folder", "parents": ["BRAND_ASSETS_FOLDER_ID"]}'
gws drive files create --json '{"name": "Photos", "mimeType": "application/vnd.google-apps.folder", "parents": ["BRAND_ASSETS_FOLDER_ID"]}'
```

The final structure on Drive should be:
```
[N]. [Client Name]/
  [Client Name] x GrowthQuest/
    Research/
    Briefs/
      References/
    Creatives/
      Winning/
    Reports/
    Brand Assets/
      Logos/
      Photos/
    Strategy/
```

4. Upload the workbook to Research/:
```bash
gws drive files create --params '{"fields": "id,name,webViewLink"}' --json '{"name": "[Client Name] Creative DNA.xlsx", "parents": ["[RESEARCH_FOLDER_ID]"]}' --upload clients/[client-name]/research/[client-name]-creative-dna.xlsx --upload-content-type application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
```

The file should be named `[Client Name] Creative DNA.xlsx` in Drive (follows the naming convention: no dates for living docs, client name included, title case).

---

## Quality Checklist

Before considering the Creative DNA complete, confirm:

- [ ] All 5 personas validated against research (not just client-supplied)
- [ ] All 5 personas have all 6 sub-sections (demographics through messaging)
- [ ] Awareness stage mapping covers all 5 personas x 5 stages with volume estimates
- [ ] Market sophistication level identified with reasoning
- [ ] Competitive gap analysis identifies specific opportunities
- [ ] Offer strength assessed (Strong / Needs Work / Weak)
- [ ] 100 hooks produced (20 per awareness stage) with format fit tags
- [ ] At least 10 angles, each with 5 copy examples and priority ranking
- [ ] Every angle and hook has funnel stage (TOF/MOF/BOF) assigned
- [ ] Every angle maps to at least one persona and awareness stage
- [ ] Competitor weaknesses from Phase 3 are reflected in positioning and angles
- [ ] Customer language from Reddit/reviews/groups/Quora/X is woven into copy (not generic)
- [ ] Winning competitor ad formats noted and referenced in angle recommendations
- [ ] foreplay.co insights included (or gap noted with extended Meta Ads Library scrape as fallback)
- [ ] Tab 10 includes "Avoid" messaging per persona
- [ ] Tab 11 benchmarks calibrated for business type
- [ ] Tab 12 includes cross-platform signals (TikTok) and landing page patterns from real data
- [ ] Quick Start tab (Tab 0) has top 3 angles, hooks, campaign structure, budget allocation, and timing
- [ ] Self-audit completed on Tabs 7, 8, 9 with revisions applied
- [ ] Workbook uploaded to correct Google Drive folder (confirmed with user)
- [ ] Checkpoint files saved for resume capability

---

## Common Pitfalls

- **Generic personas**: Demographics alone aren't a persona. The psychographic section should feel like a specific real person. Validate against research.
- **Weak objection handling**: Messaging to overcome objections must be specific, not generic. "High quality" is not copy.
- **Missing competitor intel**: If Phase 3 is thin, the angles won't be differentiated. Go deep on reviews and ad libraries.
- **Ignoring customer language**: The best copy uses the exact words customers use on Reddit, in reviews, in Facebook Groups, and on X. Mine for specific phrases.
- **Too many similar angles**: 10-15 angles should be genuinely different strategic approaches, not the same angle reworded.
- **Wrong awareness stage**: A "most aware" hook shown to an "unaware" audience will flop. Match the message to the stage.
- **Skipping market sophistication**: If you don't know what claims are worn out, you'll write the same copy as everyone else.
- **AI slop in hooks**: Run the self-audit. If a hook could be for any product, it's not specific enough.
- **No funnel mapping**: Hooks and angles without TOF/MOF/BOF labels force the media buyer to translate before using. Always assign funnel stage.
- **Ignoring the offer**: Great hooks on a weak offer still fail. Surface offer issues early in Quick Start.
- **Generic benchmarks**: E-com and lead gen have different KPIs. Calibrate for the business type.
- **Missing landing page data**: Tab 12's Landing Page Patterns should come from actual competitor ad destination URLs, not inference from homepages.
