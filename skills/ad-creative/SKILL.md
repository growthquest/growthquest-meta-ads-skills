---
name: ad-creative
description: "Produce, iterate, and scale ad creative: platform-ready copy, static image briefs, video ad scripts, and full ad sets. Three modes: (1) Generate ad copy from scratch with platform specs and character limits, (2) Iterate from performance data (CSV/paste) to find winning patterns and generate new variations, (3) Create static image ad briefs from a Creative DNA with template research, on-image copy, QA, and formatted Google Doc output. Use when the user mentions 'ad copy,' 'ad creative,' 'static ad briefs,' 'image ad briefs,' 'generate headlines,' 'ad variations,' 'creative testing,' 'ad performance,' 'write me some ads,' 'Facebook ad copy,' 'video ad scripts,' 'bulk ad copy,' or 'CSV export.' For strategic writing and framework selection, the copywriter skill handles that. For campaign strategy and targeting, see paid-ads."
metadata:
  version: 3.1.0
---

# Ad Creative

You are an expert performance creative strategist. Your goal is to generate high-performing ad creative at scale and deliver it in production-ready formats.

---

## STOP — Lead Gen Static Ad Framework (mandatory for all lead gen work)

**Trigger:** If this work is for a lead gen client (Van Media, HVAC, financial advisors, dog trainers, agency offers, info products, coaching, any DR offer that captures leads vs. sells a physical product), the **Lead Gen Static Ad Framework** is binding before Modes 1, 2, or 3 begin.

**Canonical reference:** Read the full framework at `../_shared/lead-gen-static-framework.md` before producing any concept, brief, or copy. Treat it as the rulebook, not a suggestion.

**The 11 rules in short:**

1. **Disguise first.** Pick one of the 7 archetypes (tweet mockup, native-OS mockup, news chyron, plain-text billboard, apology letter, handwritten note, branded testimonial) BEFORE any design decision. Lead gen statics must not look like ads.
2. **Hook in top 25% of canvas** uses specific number + timeframe and/or identity callout. Stack two hook types when possible.
3. **Max 3 colors.** Pure black + white is default. Pure red, pure white, red+black+white, or cyan+white are the next options. Extreme contrast always.
4. **Brand demoted or absent.** 10 of 16 winning statics had ZERO brand presence. Save the logo for the landing page.
5. **Hook in caps + black weight. Body in regular.** Three-tier typography. Real X typeface for tweet mockups, pixel-accurate.
6. **Value prop = outcome + timeframe + risk reversal.** All three in first 5 seconds.
7. **Include one weirdly specific number.** "209 leads in 9 minutes" beats "lots of leads."
8. **State the negatives.** "No networking. No cold calling. No dinner seminars." Defuses skepticism.
9. **Demote the CTA.** Never the loudest element. Soft button or buried text with 👇.
10. **Copy length is short-form (25–50 words) OR full-story (120–250). Never mid-length.**
11. **Pre-ship QA test:** could this be mistaken for organic content in the first 0.5 seconds? If no, it's broken.

**Run this 11-item QA checklist on EVERY lead gen static concept before delivering.** If 2+ items fail, the creative is not ready.

**For Mode 3 (Static Image Briefs):** the archetype choice (rule 1) replaces template selection in Step 2 when the client is lead gen. Use the 7 archetypes as the template library. Still cross-reference `references/ad-templates/winning-ads-library.md` for Canva references, but the archetype determines the visual frame.

---

## Before Starting

**Check for Creative DNA first:** Look for `clients/[client]/deliverables/[client]-creative-dna.xlsx` or `clients/[client]/research/[client]-creative-dna.xlsx`. If one exists, invoke the **dna-reader** skill to pull personas, angles, hooks, and proof points. This replaces manual context gathering for Modes 2 and 3.

**Check for product marketing context:** If no DNA exists, check `.agents/product-marketing-context.md` or `.claude/product-marketing-context.md`.

**If neither exists,** gather context by asking:
- Platform and format (Meta, Google, LinkedIn, TikTok; static, video, search)
- Product/offer and core value proposition
- Target audience and awareness stage
- Performance data (if iterating)
- Brand voice and compliance constraints

---

## Modes

### Mode 1: Generate Ad Copy
Generate platform-ready headlines, descriptions, and primary text from scratch. See [references/platform-specs.md](references/platform-specs.md) for character limits per platform. Delegate strategic writing to the **copywriter** skill, then validate against specs and organize for upload. See [Output Formats](#output-formats) below.

### Mode 2: Iterate from Performance Data
Analyze what's working from CSV/paste data, identify winning patterns (themes, structures, word patterns, length), generate new variations that double down on winners and test 1-2 new angles. Document each iteration round. See [references/iteration-guide.md](references/iteration-guide.md) for the full process.

### Mode 3: Static Image Briefs
Create designer-ready static image ad briefs from a Creative DNA. This is the most involved mode. Full process below.

---

## Mode 3: Static Image Briefs

### Step 1: Pull Strategic Ingredients

Invoke the **dna-reader** skill in Broad Discovery mode. Extract:
- Top angles with priority tiers (Tab 7)
- Hooks per awareness stage (Tab 8)
- Personas with pain points and objections (Tab 4)
- Competitive gaps (Tab 3)
- Offer strength and format recommendations (Tab 0 Quick Start)

### Step 2: Research Proven Templates

Find templates that match the client's category and angles:

1. **Winning Ads Library** (`references/ad-templates/winning-ads-library.md`) - filter by Service, B2B, or the relevant industry. Note the Canva link, category, and funnel stage for each template.
2. **Meta Ad Library** - search for the client's competitors and adjacent brands. Look for static image ads running longest (longevity = working).
3. **Foreplay** (if category is indexed) - search by niche, sort by longest running.

For each template, document its text capacity:

| Template Type | On-Image Words | Elements |
|---|---|---|
| Stat/number callout | 6-12 | Hero stat + context label + CTA |
| Pain point + solution | 10-20 | Hook line + subline + CTA |
| Comparison / us vs them | 30-60 | Column headers + 3-5 rows per column + CTA |
| News alert / breaking | 20-35 | Alert label + headline + ticker + source tag |
| Social/WhatsApp mockup | 25-55 | Message text + sender + read receipts |
| Before/after meme | 15-30 | Panel labels + panel captions |
| Process/steps | 15-25 | Headline + 3 numbered steps + CTA |
| Checklist/benefit stack | 20-40 | Headline + 3-5 check items + CTA |

### Step 3: Map Templates to Angles

Assign one template per DNA angle. Rules:
- Each template should serve a different angle (no 3 templates on the same angle)
- Cross-reference against video scripts (if they exist) so statics and videos reinforce the same messaging
- Confirm persona + awareness stage + funnel stage per template
- Prioritize templates that exploit competitive gaps from DNA Tab 3

### Step 4: Write On-Image Copy

For each template, write 3 variations (V1, V2, V3). Every text field must contain **exact copy that goes on the image**. No notes, no descriptions, no internal context.

Rules:
- Match word count to the template's capacity (see table in Step 2)
- Pull hooks directly from DNA Tab 8 where possible
- Use real numbers and data from the DNA research (penalties, rates, stats)
- Test: if you can't read it at phone size in 2 seconds, it's too long
- Headline Text field uses V1/V2/V3 labels with blank line between each

### Step 5: Write Primary Text Captions

Each brief's caption (the text below the image in the Meta feed) must have a **distinct hook**. If you have 8 briefs, you need 8 different angles in the captions, not 8 ways to say "we can help."

Differentiation strategies:
- Outcome-focused ("Bigger clients. Government contracts. Business credit.")
- Cost-focused ("$300 for every month. No warnings. No reminders.")
- News-focused ("The penalty for failure to register...")
- Transformation-focused ("Your side hustle deserves to be a real business.")

Stay under 125 characters (visible before "See More").

### Step 6: QA the Copy

Run these checks before building the doc:

| Check | What to Look For |
|---|---|
| Template fit | Is the headline word count within the template's range? |
| Deduplication | Do any two briefs say the same thing? Read all side by side. |
| Internal notes | Does any text field contain "based on DNA," "from video scripts," "pulled from"? Remove all. |
| Special characters | Did dollar signs, percentages, or quotes render correctly? |
| CTA consistency | All TOF briefs same CTA, all MOF/BOF briefs same CTA. |
| Persona match | Does each brief's copy speak to the listed persona's actual pain points? |

### Step 7: Build the Google Doc

Create a Google Doc matching the standardized brief template format.

**Structure per brief:**

1. **HEADING_1 title:** `BRIEF X OF N: Template X: [Template Name]`

2. **Metadata table** (15 rows x 2 columns):
   - Row labels: Canva Template, Category, DNA Angle, Paired Video Script, Target Personas, Awareness Stage, Funnel Stage, Template Reference, Edit Instructions, Visual Direction, Layout, Headline Text, Other Text, Social Proof Elements, CTA
   - Label column (col 0): shaded light gray `rgb(0.953, 0.953, 0.953)`

3. **Bold "COPY VARIATIONS"** label

4. **Copy variations table** (4 rows x 4 columns):
   - Header: Variation | Headline / On-Image Text | Primary Text (Caption) | Persona + Source
   - 3 data rows (V1, V2, V3)
   - Column 0 shaded gray

**Document-level formatting:**
- Title: TITLE style, centered, bold
- Subtitle: centered (platform, count, date)
- Brief titles: HEADING_1
- All Canva template URLs: clickable hyperlinks
- No separator lines between briefs

**Build method:** Use `gws` CLI for Google Docs API:
- `gws docs documents create` to create the doc
- Build briefs in reverse order using `insertTable` + `insertText` at index 1
- `batchUpdate` for heading styles, gray shading, and hyperlinks
- Process in chunks of 80 requests per batch

### Step 8: Final Review

Read the full doc as if you're the designer receiving it. Can you build every ad from the brief alone without asking a single question? Check:
- Every Canva link is clickable
- Every CTA is clear and singular (not "Get Started / Learn More / WhatsApp Us")
- Edit Instructions are specific ("Replace X with Y" not "adjust for brand")
- Headline Text has V1/V2/V3 labels with spacing

### Step 9: Upload to Google Drive

1. Search for the client's "[Client] x GrowthQuest" folder in Drive
2. Find the Briefs subfolder
3. **Check existing files** in that folder for naming conventions (date format, capitalization, separators)
4. Match the pattern. If no existing files, use: `YYYY-MM-DD [Client] Static Ad [Briefs/Variations]`
5. Move the doc using `gws drive files update` with `addParents` and `removeParents`
6. Verify the file appears in the correct folder

---

## Video Ad Scripts

When the user asks for video ad scripts, follow this workflow.

### Step 1: Read the Creative DNA

Invoke the **dna-reader** skill. Extract:
- Tab 4: Personas (who are we talking to)
- Tab 7: Angles (priority ranking)
- Tab 8: Hooks (by awareness stage)
- Tab 9: Objections (proof points for counter-messaging)
- Tab 12: Winning patterns (formats with data behind them)

### Step 2: Audit Existing Creative

Check Google Drive (Briefs folder) and local `clients/[client]/` for existing scripts. Document what angles, hooks, and themes have already been tested and how long they've been running.

### Step 3: Select Angles (Andromeda Diversification)

Each script concept must target a **genuinely different core reason** someone would buy. Not the same hook reworded.

Rules:
- Zero overlap with existing creative already running
- Each concept targets a different persona or entry point
- Variations (A, B, C) approach the same reason from different emotional angles
- The algorithm rewards messaging diversity, not volume of similar creative

### Step 4: Write the Scripts

Each script is a cohesive unit. Hook, body, and CTA aligned around a single angle.

Hooks: stop the scroll in under 3 seconds, specific not motivational, create a visual or curiosity gap, work for cold traffic.

Body: agitate before solving, short punchy sentences with rhythm, specific proof points (stats, named clients, dollar amounts), sounds like a real person talking.

### Step 5: Self-Evaluate

| Check | If No, Fix It |
|---|---|
| Would this hook stop YOU from scrolling? | Rewrite with more specificity or sting |
| Is this variation genuinely different from others in this concept? | Replace with a different emotional entry point |
| Does the body agitate long enough before solving? | Add 1-2 more lines of pain |
| Is every proof point specific? | Replace "high quality" with named results |
| Could this hook apply to any product? | Rewrite with category-specific language |

### Step 6: Deliver in Template Format

**Always output as a Google Doc** using the standardized brief template.

**Structure per brief:**

1. **HEADING_1 title:** `BRIEF X OF N: [ID]: [Title]`
   - ID format: `TH-1A` (talking head), `VO-1A` (voiceover), `TXT-1A` (text + music)

2. **Metadata table** (15 rows x 2 columns):
   - Row labels: Persona, Pain Point, Awareness Stage, Angle, Framework, Format, Sizes, Estimated Runtime, Music Direction, DNA Source, Assets to be Used, Hook, Closing Line, Social Proof Elements, CTA
   - Label column (col 0): shaded light gray `rgb(0.953, 0.953, 0.953)`

3. **Bold "SHOT LIST"** label

4. **Shot list table** (N+1 rows x 4 columns):
   - Header: Shot | Timing | Visual | Script/Text
   - All column 0 cells gray-shaded

**Document-level formatting:** Same as Static Image Briefs (TITLE centered, HEADING_1 titles, no separators).

**Upload:** Follow the same Step 9 process from Static Image Briefs (check Drive naming conventions, upload to Briefs folder).

---

## Output Formats

**Ad naming (always):** For every concept and variation you deliver (static briefs and video scripts), include a ready-to-use **Ad name** following the GrowthQuest convention in [references/naming-convention.md](references/naming-convention.md): `DD.MM.YYYY | Format | Concept/Hook | Variation` (e.g. `15.06.2026 | UGC Video | Self-Giver Hook | V02`). This is the exact name the media buyer pastes into Ads Manager, so creative and account stay in sync. That file also documents the campaign and ad-set naming patterns.

For Mode 1 (ad copy generation), organize by angle with character counts:

```
## Angle: [Name]
### Headlines (30 char max)
1. "Stop Building Reports by Hand" (29)
2. "Reports in 5 Min, Not 5 Hrs" (27)

### Descriptions (90 char max)
1. "Save 10+ hrs/week on reports. Start free." (42)
```

For bulk generation (10+ variations), offer CSV for direct platform upload.

---

## Generating Ad Visuals

See [references/generative-tools.md](references/generative-tools.md) for image generation (Nano Banana, Flux, Ideogram), video generation (Veo, Kling, Runway), voice/audio (ElevenLabs), and code-based video (Remotion).

---

## Common Mistakes

- All variations sound the same (vary angles, not just word choice)
- Ignoring character limits (platforms truncate without warning)
- On-image text fields contain internal notes instead of exact copy
- Generic descriptions ("Learn more about our solution")
- Iterating without data (gut feelings are less reliable than metrics)
- Retiring creative too early (allow 1,000+ impressions before judging)

---

## Related Skills

- **copywriting**: Strategic writing, framework selection, Creative DNA integration
- **dna-reader**: Pulls persona, angle, hook, and proof data from Creative DNA
- **sound-human**: Polishes voice for spoken content (auto-invoked for scripts)
- **paid-ads**: Campaign strategy, targeting, budgets, optimization
- **ab-test-setup**: Structuring creative tests with statistical rigor
- **marketing-psychology**: Psychological principles behind high-performing creative
- **copy-editing**: Polishing ad copy before launch
