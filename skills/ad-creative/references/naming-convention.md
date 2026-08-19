# GrowthQuest Ad Naming Convention

Standard naming for Meta campaigns, ad sets, and ads. Use this whenever producing creative or setting up an account so names are consistent and instantly scannable. Mirrors the media-buyer SOP (`references/sops/media-buyer-sop.md`, "Account Structure").

## Rules
- Fields separated by ` | ` (space-pipe-space).
- **Same field order every time.**
- Short, consistent tokens (see glossary).
- One date format: **DD.MM.YYYY** (never mix with MM.DD).
- Title Case. No random ALLCAPS.
- Use a clean omission (drop the field and its separator) when a field is N/A, don't leave double separators.

## Patterns

| Level | Pattern | Example |
|---|---|---|
| Campaign | `Platform \| Type \| Funnel \| Objective \| Geo` | `M \| PRO \| TOF \| Purchase \| US` |
| Ad set | `Date \| Audience \| Angle/Persona \| Exclusion \| Geo` | `15.06.2026 \| Broad \| Self-Giver \| Excl. 180d Purchasers \| US` |
| Ad | `Date \| Format \| Concept/Hook \| Variation` | `15.06.2026 \| UGC Video \| Self-Giver Hook \| V02` |

## Token glossary
- **Type:** PRO (cold prospecting), RTG (retargeting), ASC (Advantage+ Shopping), AWA (awareness), TST (test)
- **Funnel:** TOF, MOF, BOF
- **Audience:** Broad, LAL X% (name the seed, e.g. `LAL 1% Purchasers`), Int: X, Retargeting XXd, Engaged XXd, Customers
- **Exclusion:** Excl. Warm, Excl. Purchasers XXXd, Excl. Engaged XXd
- **Format:** Static, Video, UGC, Carousel, Flexible
- **Geo:** US, UK, AU, CA, ROW, Global

## When producing creative
For every concept / variation you output (static briefs and video scripts), include a ready-to-use **Ad name** using the Ad pattern above. The Concept/Hook field = the angle or hook of that creative; Variation = `V01`, `V02`, … (or `Batch N` for batches). This is the name the media buyer pastes into Ads Manager, so the creative and the account stay in sync.
