---
name: dna-reader
description: "Read and extract strategic insights from a client's Creative DNA workbook. Use when another skill needs client research data, when the user says 'read the DNA,' 'pull from creative DNA,' 'check the research,' 'what do we know about [client],' 'find angles,' 'generate concepts,' or 'creative brief.' Also auto-activates when the copywriter skill needs client data and a Creative DNA file exists. Requires a Creative DNA .xlsx file produced by the meta-ads-research skill."
metadata:
  version: 1.0.0
---

# DNA Reader

You read Creative DNA spreadsheets and extract strategic ingredients for writing ad scripts, ad copy, graphic copy, or any client creative work.

## The Problem

A Creative DNA is a structured research document produced by the **meta-ads-research** skill. It contains everything we know about a brand's positioning, customers, messaging, and proof. But without this skill, a Creative DNA is just a large batch of data. You can see the words but you can't navigate the structure. You don't know where to find specific data, how tabs relate to each other, or how to cross-reference personas against objections against proof points.

This skill gives you the methodology to turn raw research into actionable creative ingredients.

---

## File Discovery

Search for the Creative DNA file in this order:

1. `clients/[client-name]/research/[client-name]-creative-dna.xlsx`
2. `clients/[client-name]/deliverables/[client-name]-creative-dna.xlsx`

If no client name is provided or obvious from context, list available client directories under `clients/` and ask.

---

## Reading Method

Use Python with openpyxl to read the workbook:

```python
import openpyxl

wb = openpyxl.load_workbook('path/to/creative-dna.xlsx')
sheet_names = wb.sheetnames  # List all tabs to verify structure
```

**Merged cell handling:** When reading merged cells in openpyxl, the value lives in the top-left cell only. All other cells in the merge return None. Always check for None values and skip them rather than treating them as missing data. This is common in header rows and category groupings.

---

## The Creative DNA Has 13 Tabs (Tab 0 through Tab 12)

### Tab 0: Quick Start
The cherry-picked summary tab, generated last. Pre-picked top creative for fast starts.
- Top 3 angles to test first
- 15 highest-confidence hooks (5 per top angle, cherry-picked from Tab 8)
- Recommended first campaign structure and budget allocation
- 3 biggest competitive gaps to exploit (from Tab 3)
- Offer-strength rating and timing notes
- **Use for:** A ready-made creative-brief seed. Start here when you want the best bets without reading the full workbook.

### Tab 1: Overview
- Client name, business type, website
- Offer summary, pricing, margins
- Key benefits, USP, perks
- Target KPIs, ad spend, breakeven ROAS
- **Use for:** Brand context, budget context, KPI targets

### Tab 2: Business Analysis
- Business overview (2-3 paragraphs)
- Products and services breakdown
- Main benefits with proof points
- Unique differentiators (references competitor weaknesses)
- **Use for:** Proof points, feature-to-benefit mapping, brand positioning

### Tab 3: Competitive Gap Analysis
- Competitor comparison matrix (positioning, pricing, guarantees, messaging)
- Saturated angles (what everyone is doing)
- Open space (what no one is doing)
- Underserved segments
- Messaging white space
- **Use for:** Differentiation, finding untapped angles, avoiding saturated messaging

### Tab 4: Customer Personas
The most important tab. 5 distinct personas. For each:
- Demographic profile (age, income, location, lifestyle, education, tech adoption)
- Psychographic characteristics (2-3 sentences: how they think, what they value)
- Pain points (5 specific frustrations)
- Motivators (5 drivers to buy)
- Possible objections (5 hesitations)
- Messaging to overcome objections (5 specific copy lines)
- **Use for:** Every script and ad starts here. The persona drives everything.

### Tab 5: Awareness Stages
Matrix: 5 personas x 5 awareness stages (Unaware, Problem Aware, Solution Aware, Product Aware, Most Aware).
For each cell:
- Messaging approach
- What works / what doesn't
- Example hook directions
- Estimated volume (high/medium/low)
- **Use for:** Determining tone, depth, and hook style for each persona at each stage

### Tab 6: Market Sophistication
- Current sophistication level (1-5) with reasoning
- Worn-out claims in this market
- Fresh angles and mechanisms
- Recommended sophistication strategy
- **Use for:** Complexity of claims, how much explanation is needed, what claims to avoid

### Tab 7: Angles
10-15 copywriting angles. For each:
- Angle name
- Core theme (1 sentence)
- 5 application examples (ready-to-use ad body copy)
- Best-fit personas (primary + secondary)
- Best-fit awareness stages
- **Use for:** Strategic perspective and lens for each ad

### Tab 8: Hooks
100 hooks total, organized by awareness stage (20 per stage).
For each hook:
- Hook text
- Hook type (question, stat, story, bold claim, pattern interrupt, before/after, testimonial, controversy, curiosity gap, direct address)
- Target persona
- Awareness stage
- **Use for:** Opening lines, scroll-stoppers, first 3 seconds of video

### Tab 9: Objections and Handling
For each persona:
- Top 5 objections
- For each objection: specific counter-messaging (not generic)
- Supporting proof points from research (reviews, stats, testimonials)
- **Use for:** Overcoming resistance in scripts, FAQ sections, retargeting copy

### Tab 10: Messaging Strategies
Angle-to-persona mapping:
- For each persona: primary angles (top 3 with reasoning), secondary angles (3-6)
- Recommended campaign approach per persona (lead message, creative direction, tone, imagery, CTA style)
- **Use for:** Campaign planning, matching angles to personas, creative direction

### Tab 11: Testing Framework
- Benchmark metrics (CTR, CPC, CVR, CPA, ROAS)
- Winning thresholds
- Angle testing decision tree
- **Use for:** Setting success criteria, knowing when to scale or cut

### Tab 12: Winning Ad Pattern Analysis
- Longest-running competitor hooks and formats (proven winners by ad duration)
- Landing-page patterns from real destination URLs
- Cross-platform signals (e.g. TikTok)
- Creative gaps ranked by opportunity
- Saved competitor winner screenshots (reference-image gold for creative generation)
- **Use for:** Format selection, what is actually working in-market, reference visuals, gap analysis

---

## Two Operating Modes

### Mode A: Broad Discovery

Trigger: "Find me the best angles," "What should we write about?", "What concepts have the highest potential?"

**Process:**
1. Load the xlsx using openpyxl
2. Scan all 5 personas (Tab 4): pull their core problems, emotional state, motivators
3. For each persona, pull their best-fit angles from Tab 7
4. Cross-reference Tab 2 (Business Analysis) for proof point strength per persona
5. Cross-reference Tab 9 (Objections) for objection difficulty per persona
6. Pull 3-5 matching hooks from Tab 8 based on each persona's emotional state and top awareness stage
7. Check Tab 3 (Competitive Gap) for open space that aligns with each persona
8. Rank concepts by: proof strength + objection weakness + emotional resonance + competitive gap alignment

**Output: Ranked Concept Library**

For each concept (ranked by potential):
- **Angle** (from Tab 7)
- **Target persona** (from Tab 4)
- **Hook category and examples** (from Tab 8)
- **Messaging strategy reference** (from Tab 10)
- **Objection it handles** (from Tab 9)
- **Proof available** (from Tab 2)
- **Competitive gap it exploits** (from Tab 3)

---

### Mode B: Targeted Brief

Trigger: "I'm targeting [specific audience]," "Write for [persona]," "Pull a brief for [audience type]"

**Process:**
1. Match the user's description to the closest persona in Tab 4. If ambiguous, present the top 2-3 matches and ask.
2. Extract their full profile: demographics, psychographics, pain points, motivators, objections, messaging
3. Determine their primary awareness stage using Tab 5
4. Pull their messaging strategy from Tab 10 (primary angles, creative direction, tone, CTA style)
5. Pull 5-10 hooks from Tab 8 matching their awareness stage and persona
6. Pull proof points from Tab 2 that resonate with this persona's pain points
7. Pull their top objections from Tab 9 with all counter-messaging and proof
8. Check Tab 6 (Market Sophistication) for claim complexity guidance
9. Check Tab 3 (Competitive Gap) for differentiation opportunities

**Output: Complete Creative Brief**

- **Persona profile** (full demographic + psychographic)
- **Awareness stage** + messaging approach
- **Primary and secondary angles** with reasoning
- **Customer language** (exact phrases from persona pain points and motivators)
- **Relevant hooks** (5-10, matched to stage and persona)
- **Proof points available**
- **Objections with counter-messaging**
- **Market sophistication context**
- **Competitive gaps to exploit**
- **Recommended creative direction** (from Tab 10)
- Ready to feed directly into the copywriter skill

---

## Quality Rules

- **Persona match must be tight.** The closest row in Tab 4, not a guess.
- **Proof must be real.** Pulled from Tab 2 and Tab 9, never inferred or invented.
- **Language must be exact.** Direct quotes from persona pain points and motivators, never paraphrased.
- **Hooks must match the awareness stage.** An "unaware" hook shown to a "most aware" audience will feel condescending.
- **Objection crushers must be actionable** in a script or ad, not academic.
- **If data is missing from any tab, say so.** Don't fill gaps with assumptions.

---

## Missing Data Handling

For each tab, track and report completeness:

| Status | Meaning |
|--------|---------|
| **Complete** | All expected data present |
| **Partial** | Some data present, some sections empty |
| **Empty** | Tab exists but has no usable data |
| **Missing** | Tab doesn't exist in the workbook |

Return a Coverage Report at the end of every read:

```
## Coverage Report
- Tab 0 (Quick Start): Complete
- Tab 1 (Overview): Complete
- Tab 2 (Business Analysis): Complete
- Tab 3 (Competitive Gap): Partial (missing underserved segments)
- Tab 4 (Customer Personas): Complete (5/5 personas)
- Tab 5 (Awareness Stages): Complete
- Tab 6 (Market Sophistication): Complete
- Tab 7 (Angles): Complete (12 angles)
- Tab 8 (Hooks): Complete (100/100 hooks)
- Tab 9 (Objections): Complete
- Tab 10 (Messaging Strategies): Partial (missing secondary angles for 2 personas)
- Tab 11 (Testing Framework): Complete
- Tab 12 (Winning Ad Patterns): Complete
```

If critical tabs are missing or empty (Tab 4 Personas, Tab 7 Angles, Tab 8 Hooks), flag this prominently and recommend running the **meta-ads-research** skill to regenerate or complete the workbook.

---

## Related Skills

- **meta-ads-research**: Produces the Creative DNA workbook this skill reads
- **copywriting**: Consumes the brief output from this skill for writing copy in any format
- **ad-creative**: Uses persona and angle data for bulk ad production at scale
- **sound-human**: Polishes voice for spoken content after copywriter writes the script
