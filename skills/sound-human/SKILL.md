---
name: sound-human
description: "Make AI-generated copy sound like natural human speech. Use when the user says 'make it sound human,' 'this sounds too AI,' 'rewrite conversationally,' 'natural voice,' 'sounds robotic,' 'too formal,' 'loosen this up,' 'make it real,' or 'this reads like a machine wrote it.' Also auto-activates when the copywriter skill outputs spoken content (scripts, voiceovers, UGC). Works standalone as a rewrite pass or as part of the copywriting chain. This skill handles VOICE only, not structure or strategy."
metadata:
  version: 1.0.0
---

# Sound Human

You make AI writing sound like a real person talking.

## The Problem

AI writing is detectable because it's too uniform. Uniform sentence length, uniform structure, uniform vocabulary, uniform register. Humans are messy. They fragment, interrupt themselves, speed up and slow down. That messiness is what makes speech feel real.

This skill encodes 10 rules that break AI uniformity and a kill list of words that instantly flag content as machine-generated.

---

## Two Operating Modes

### Standalone Mode
The user provides text and asks you to make it sound human. Apply all 10 rules, then run the checklist. Return the rewritten version with a brief note on what changed.

### Chain Mode
Called automatically by the copywriter skill after outputting spoken content (video scripts, voiceover scripts, UGC scripts). In chain mode, apply the rules during the writing process. Don't wait for a separate rewrite pass.

---

## The 10 Rules

### Rule 1: Sentence Length Variation

The pattern is short-long-short. Mix it up constantly.

Target: 25%+ of sentences under 8 words. 15%+ over 25 words. If 3 sentences in a row are similar length, break one up.

**Example:**
"Better ads. That's what this does. It takes proven frameworks, the ones behind every high-converting campaign you've seen, and writes scripts from them. Your brand. Your voice. Just... faster."

### Rule 2: Fragments

"Period." "Not even close." "Wild, right?"

Fragments carry emphasis and rhythm. They punch. They land. 8-12% of sentences should be fragments.

AI almost never produces them. This is one of the most reliable signals of human writing.

### Rule 3: Conjunction Starts

Start sentences with: And, But, So, Now, Or, Because, Still, Plus, Yet

Target: ~10% of sentences start with conjunctions. AI typically does ~2%.

**Kill these formal connectors entirely:**
- Furthermore
- Additionally
- Moreover
- Consequently
- However (replace with "But")
- Nevertheless
- In addition
- Nonetheless

Every single formal connector gets replaced with a conjunction start.

### Rule 4: Contractions Everywhere

Don't write "do not." Write "don't." Don't write "it is." Write "it's." Don't write "they are." Write "they're."

20-25% of eligible word pairs should be contracted.

**One exception:** emphatic moments. "I do NOT recommend this" hits harder uncontracted precisely because it's unexpected. Use the uncontracted form only when you want that emphasis to land.

### Rule 5: Discourse Markers

"Honestly," "look," "right," "okay," "so," "I mean," "here's the thing."

These carry rhythm, not meaning. They signal a human is thinking, transitioning, or emphasizing. 2-3 per 100 words.

**Where to place them:**
- At section openings: "Okay so here's what happened."
- Before key points: "Look, the truth is..."
- After claims: "...and honestly, it surprised me."
- As transitions: "So here's where it gets interesting."

### Rule 6: Stress Positioning

Based on George Gopen's reader expectation theory. The end of a sentence is where the listener places emphasis. Put the most important word there.

**Bad:** "You can save up to $300 per month on creative production."
**Good:** "Creative production that used to cost $300 a month? Gone."

The word "Gone" lands at the end. Where it hits.

**Bad:** "Our tool helps you create better content faster."
**Good:** "Better content. And you'll create it in half the time."

### Rule 7: Forward Momentum

Joseph Sugarman's slippery slide: every sentence should compel the listener to hear the next one.

- End sections with open loops: "But that's not even the best part."
- Tease before reveal: "There's one thing nobody talks about."
- Start the next thought before closing the current one
- Use questions to pull forward: "So what happened next?"

AI closes each thought completely before starting the next. Humans overlap. Break the neatness.

### Rule 8: Register Shifting

Human speech shifts between formal and informal constantly. AI stays at one register throughout.

Technical claim with authority: "500+ avatar presets, each with specific lighting conditions."
Followed by casual reaction: "And honestly? The difference is wild."

That shift, precise to casual, is something humans do constantly and AI almost never does. Mix your registers deliberately.

### Rule 9: Specificity Over Vagueness

Replace every "many users" with a number. Replace every "significant improvement" with a measurement. Replace every "people" with a name.

**Vague:** "Many customers have seen great results with our product."
**Specific:** "Sarah, she runs a 3-person creative team in Austin, tested this last month. Her CPA dropped 34% in two weeks."

If you don't have real data, say so honestly rather than going vague. "We're still collecting data" beats "many people have seen results."

### Rule 10: Self-Corrections and Asides

"Actually, let me back up." "Well, okay, not exactly." "This might sound weird, but..."

AI never self-corrects because it generates forward-only. A single self-correction signals "this person is thinking in real time."

At least one per 150 words.

**Examples:**
- "It's fast. Like, really fast. Okay, 'fast' doesn't do it justice."
- "The results were... honestly, I didn't believe them at first."
- "We tested everything. Well, not everything. But close."

---

## The 10-Point Post-Write Checklist

After writing or rewriting, run this verification:

1. **Read-aloud test.** Does any sentence sound like LinkedIn but not speech? Rewrite it.
2. **Sentence length variation.** 3 in a row similar length? Break one.
3. **Conjunction start count.** Below 8%? Add more.
4. **Formal connector scan.** Any Furthermore/Additionally/Moreover/However survivors? Replace all.
5. **Contraction check.** Uncontracted pairs that should be contracted? Fix them.
6. **Discourse marker density.** At least one per 50-75 words.
7. **Stress positioning.** Important word at end of each key sentence?
8. **Forward momentum.** Does each section tease the next or conclude neatly? Break the neatness.
9. **Specificity sweep.** Replace every vague quantifier with a specific.
10. **Self-correction count.** At least one per 150 words.

---

## AI Kill List

Words and phrases that are dead giveaways of AI writing. Replace or remove all of these on sight.

**Formal connectors:**
Furthermore, Additionally, Moreover, In addition, Consequently, Nevertheless, Nonetheless, Henceforth, Accordingly

**Filler qualifiers:**
It's worth noting, It's important to note, It should be noted, Interestingly, Notably, Significantly

**Buzzwords:**
Delve, Landscape, Leverage (as verb), Utilize, Facilitate, Robust, Seamless, Cutting-edge, Game-changer, Revolutionize, Harness, Elevate, Streamline, Empower, Spearhead

**Cliches:**
At the end of the day, In today's [anything], When it comes to, In the world of, It goes without saying, Without further ado, That being said, With that said

**AI-specific patterns:**
- "Not X, but Y" framing ("Not just a tool, but a partner")
- Triple-adjective stacking ("powerful, intuitive, and seamless")
- Starting paragraphs with "In" ("In the fast-paced world of...")
- "Let's dive in" / "Let's explore" / "Let's unpack"
- Ending with "...and beyond"

---

## Scope

This skill handles VOICE only.

- Not script structure (that's the copywriter's framework selection)
- Not strategy (that's the copywriter's principles layer)
- Not data or research (that's the DNA reader)

Think of it as the final polish. Strategy decides WHAT to say. Structure decides the ORDER. This skill decides HOW it sounds when spoken.

---

## Related Skills

- **copywriting**: For strategy, structure, and framework selection. Calls this skill automatically for spoken content.
- **copy-editing**: For systematic editing passes. Different focus: clarity, proof, specificity sweeps.
- **ad-creative**: For platform-specific ad production at scale.
