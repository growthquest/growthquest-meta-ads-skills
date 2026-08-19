# GrowthQuest Meta Ads Skills

Claude Code skill pack for the Meta ads creative workflow: research a client, build a Creative DNA, write the copy, and generate the creatives.

Everything here runs inside Claude Code. Drop the `skills/` folders into your `.claude/skills/` directory and the skills activate automatically when a matching task comes up (or invoke them by name).

---

## What's in the pack

11 skills across three groups plus one shared reference.

### 1. Creative DNA + copy
| Skill | What it does |
|-------|-------------|
| `meta-ads-research` | Deep pre-campaign research → **Creative DNA** workbook (business analysis, personas, awareness stages, 13 angles, 100 hooks, objection handling) as an Excel file. This is the DNA *creator*. Run at new-client onboarding. |
| `dna-reader` | Reads an existing Creative DNA workbook and pulls the exact insights other skills need (angles, hooks, personas). |
| `ad-creative` | Ad copy, static image briefs, and video scripts. Three modes: write from scratch, iterate from a performance CSV, or build static briefs from a DNA. |
| `copywriting` | The master writing engine: every framework (PAS, AIDA, BAB, Hook-Story-Offer...), all formats. |
| `sound-human` | Strips the AI voice out of generated copy. Voice-only pass, runs after copywriting. |

### 2. Standalone generation
| Skill | What it does |
|-------|-------------|
| `generate-ads` | End-to-end from a product name/URL: research → 4 art-directed briefs → final ad images (Gemini Nano Banana). One command, four creatives. |
| `banana` | The image-generation engine (Google Gemini Nano Banana). Used by `generate-ads` and the `/ads` pipeline. |

### 3. The `/ads` pipeline
A step-by-step alternative to `generate-ads`, driven by a router skill:
| Skill | Step |
|-------|------|
| `ads` | Router. Dispatches `/ads dna`, `/ads create`, `/ads generate`, and audit/plan/test subcommands. |
| `ads-dna` | `/ads dna` — extracts brand identity from a URL → `brand-profile.json`. |
| `ads-create` | `/ads create` — campaign concepts + copy briefs → `campaign-brief.md`. |
| `ads-generate` | `/ads generate` — platform-sized images from the brief. |

### Shared
- `_shared/lead-gen-static-framework.md` — the Lead Gen Static Ad Framework. `ad-creative`, `ads-create`, and `ads-generate` all read this before producing any lead-gen static. Keep it alongside the skills.

---

## Two ways to generate creatives

Pick one, don't run both for the same job:

- **`generate-ads`** — fastest path. Give it a product, it does research + briefs + 4 images in one shot. Best default for ecommerce.
- **`/ads` pipeline** — more control. Run `dna → create → generate` as discrete steps, inspecting the `brand-profile.json` and `campaign-brief.md` between each. Best when you want to review/edit the brief before images render.

Both call `banana` under the hood.

---

## Install

1. Copy each folder in `skills/` into your Claude Code skills directory:
   ```bash
   cp -R skills/* ~/.claude/skills/
   ```
   (or into a project's `.claude/skills/` for project-scoped use)
2. Restart Claude Code so it picks up the new skills.
3. Set up dependencies below.

---

## Dependencies (required for image generation)

Image generation needs a Gemini API key and the Nano Banana MCP. Copy/research skills work without these.

- **Google Gemini API key** — set `GOOGLE_API_KEY` (or `GOOGLE_AI_API_KEY`) in your environment. Get one at console.cloud.google.com/apis/credentials.
- **nanobanana-mcp** — `banana` and `ads-generate` generate through this MCP. See `skills/banana/scripts/setup_mcp.py` and `skills/banana/references/mcp-tools.md`.
- **Python deps** for the `/ads` scripts: see `skills/ads/requirements.txt`.
- `meta-ads-research` builds the DNA from a Google Form intake and uses web search — no image key needed.

The `ads/` pipeline can also target OpenAI, Stability, or Replicate instead of Gemini (set the matching `OPENAI_API_KEY` / `STABILITY_API_KEY` / `REPLICATE_API_TOKEN`). See `skills/ads/references/image-providers.md`.

---

## Notes

- **No secrets in this repo.** Every key reference is an environment-variable name or a placeholder. Supply your own keys locally.
- The Lead Gen Static Framework cites past GrowthQuest client work (e.g. Van Media) as pattern examples. Internal reference only.
- The heavy asset cache from `generate-ads` (prior render outputs) was stripped before packaging. The skill regenerates its own workspace on first run.
