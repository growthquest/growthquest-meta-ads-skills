import json, urllib.request, base64, ssl, os, sys

api_key = os.environ['GEMINI_API_KEY']
ctx = ssl.create_default_context()
RUN = sys.argv[1] if len(sys.argv) > 1 else open('/tmp/lumin_runid.txt').read().strip()
BASE = f'./ad-workspace/{RUN}'
REF = f'{BASE}/references'

def load(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode()

def mime(path):
    return 'image/png' if path.lower().endswith('.png') else 'image/jpeg'

product = (load(f'{REF}/product-bottle-clean.png'), 'image/png')

def gen(name, prompt, refs):
    parts = [{'text': prompt}, {'inlineData': {'mimeType': product[1], 'data': product[0]}}]
    for rp in refs:
        parts.append({'inlineData': {'mimeType': mime(rp), 'data': load(rp)}})
    payload = json.dumps({
        'contents': [{'parts': parts}],
        'generationConfig': {'responseModalities': ['TEXT', 'IMAGE'], 'imageConfig': {'aspectRatio': '1:1'}}
    }).encode()
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent?key={api_key}'
    req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
    try:
        resp = urllib.request.urlopen(req, timeout=240, context=ctx)
    except urllib.error.HTTPError as e:
        print(f'[{name}] HTTP {e.code}: {e.read()[:300]}'); return False
    data = json.loads(resp.read())
    ok = False
    for part in data.get('candidates', [{}])[0].get('content', {}).get('parts', []):
        if 'inlineData' in part:
            img = base64.b64decode(part['inlineData']['data'])
            out = f'{BASE}/{name}.png'
            with open(out, 'wb') as f:
                f.write(img)
            print(f'[{name}] SAVED {len(img)} bytes -> {out}'); ok = True
        elif 'text' in part:
            print(f'[{name}] note: {part["text"][:150]}')
    if not ok:
        print(f'[{name}] NO IMAGE. Raw: {json.dumps(data)[:400]}')
    return ok

PROD_LOCK = ("REFERENCE IMAGE 1 is the ACTUAL Lumin Root Revive product. You MUST reproduce this exact "
    "bottle with photographic accuracy: clear glass bottle, brushed silver screw lid, matte BLACK label "
    "with 'Lumin' in white, huge white 'ROOT REVIVE' text, gold sub-text 'BLACK SEED EXTRACT / BAMBOO "
    "EXTRACT / PUMPKIN SEED EXTRACT / +17 Growth ingredients', a GOLD band near the bottom reading "
    "'DIETARY SUPPLEMENT 60 CAPSULES', white capsules visible inside. Match every logo, color and word exactly. ")

ANTI = ("\n\nThis must NOT look like a generic stock photo or a plain product-on-table shot. It must look "
    "like a bold, award-winning DTC beauty campaign someone screenshots and sends to a friend. All text "
    "crisp, correctly spelled, high-contrast and instantly legible at phone size. "
    "STRICT TYPOGRAPHY RULE: Do NOT use em dashes or en dashes (— or –) anywhere in any text. Use only "
    "the exact punctuation written in the text-overlay instructions (periods, commas, or the middot '·').")

ads = [
  ("ad-1-your-crown", [f'{REF}/v1-gold-portrait.jpg', f'{REF}/v1-black-gold-world.jpg'],
   f"""You are a world-class advertising art director and beauty photographer shooting a high-budget, fully art-directed campaign for Lumin Root Revive, a hair-growth supplement made for Black women.

{PROD_LOCK}

THE CONCEPT: A regal, editorial beauty portrait that says 'your crown, restored.' We build an entire BLACK + GOLD world. A stunning Black woman in her 30s-40s with radiant deep-brown skin and a full, healthy, voluminous natural 4C crown (thick edges, complete healthy hairline) is caught mid genuine warm laugh, eyes softly crinkled with real joy, NOT a posed model smile. Golden rim-light glows through her hair like a halo.

COLOR WORLD: The ENTIRE scene is drenched in deep matte black and luminous warm gold. Seamless black studio background with soft floating gold bokeh and dust. She wears an elegant black off-shoulder top with a hint of gold jewelry. The only brightness comes from her golden-lit skin, her hair's rim light, and the product.

COMPOSITION: She fills the left two-thirds, shot on a Hasselblad medium format 80mm f/2, Rembrandt editorial beauty lighting, hyperreal skin with visible pores and healthy sheen, every curl sharp. On the lower-right, REFERENCE IMAGE 1 product bottle rests on a small black pedestal, lit like fine jewelry with a warm gold glow and soft reflection. CRITICAL PRODUCT ACCURACY: the bottle lid MUST be a brushed SILVER / metallic aluminium screw lid exactly as in REFERENCE IMAGE 1, never black; keep the ingredient text on the label crisp and correctly spelled ('BLACK SEED EXTRACT', 'BAMBOO EXTRACT', 'PUMPKIN SEED EXTRACT'). REFERENCE IMAGE 2 is the model/gold-skin styling mood. REFERENCE IMAGE 3 is the black-and-gold bokeh world mood.

TEXT OVERLAY: At the very top, a small gold all-caps eyebrow kicker in clean spaced letters: 'HAIR GROWTH FROM WITHIN · FOR BLACK WOMEN'. Directly below it, large bold cream-white elegant serif headline: 'Your crown is calling.' Bottom, smaller light sans-serif subtext on two lines: 'Grow thicker, fuller hair. Fill in your edges, from within.' and a small gold pill-shaped button: 'TAKE THE QUIZ'. All text crisp and legible; the gold kicker makes it unmistakable in 0.5s that this is a hair-growth product. Do not use dashes; only the middot, periods and the comma shown.

THE FEELING in 0.5s: dignity, luxury, 'that could be me again.'{ANTI}"""),

  ("ad-2-fire-under-scalp", [f'{REF}/v2-sprout-cracked.jpg'],
   f"""You are a world-class advertising art director and cinematic still photographer creating a bold conceptual ad for Lumin Root Revive, a hair-growth supplement for Black women. This is a high-budget concept shoot.

{PROD_LOCK}

THE CONCEPT — a visual metaphor for the root cause: 'the fire under your scalp.' A dramatic macro split-earth image. LEFT HALF: parched, cracked, scorched dark earth with faint glowing ember-orange light burning deep inside the cracks (this represents scalp inflammation choking the follicles). RIGHT HALF: the SAME ground transformed into rich, moist, healthy black soil out of which a single strong, elegant golden-green sprout rises, a tiny warm gold light glowing at its root. The transformation flows left-to-right: from burning and barren to alive and growing.

AT THE CENTER SEAM, standing upright and heroic, is REFERENCE IMAGE 1 product bottle, glowing with a warm gold halo, clearly the CAUSE of the healing. REFERENCE IMAGE 2 is the cracked-earth-and-sprout mood reference.

COLOR WORLD: charred black earth, ember gold and amber embers as floating gold sparks, one living hit of green in the sprout, deep black background. Cinematic side lighting, Canon EOS R5 100mm macro at f/2.8, hyperreal texture on soil cracks, embers and dewy sprout.

TEXT OVERLAY: At the very top, a small gold all-caps eyebrow kicker in clean spaced letters: 'THE REAL REASON YOUR HAIR WON'T GROW'. Directly below it, bold cream-white condensed sans-serif headline: 'The fire under your scalp.' Bottom, smaller subtext: 'Scalp inflammation stops hair growth. Root Revive calms it and regrows hair from within. Made for Black women.' plus a small gold button: 'LEARN WHY'. Crisp and legible; the kicker plus 'hair growth' wording must make it obvious in 0.5s this is a hair-growth product, not skincare.

THE FEELING in 0.5s: 'so THAT'S why nothing worked' — curiosity plus hope.{ANTI}"""),

  ("ad-3-made-for-you", [f'{REF}/v1-black-gold-world.jpg'],
   f"""You are a world-class advertising art director creating a bold 'us vs. them' comparison ad for Lumin Root Revive, a hair-growth supplement made for Black women.

{PROD_LOCK}

THE CONCEPT: a split-frame that says 'everything else was built for someone else's hair.'

LEFT SIDE (~55% of frame): a desaturated, cool grey-blue, dimly lit messy pile of GENERIC failed hair products — pastel pink and mint biotin gummy bottles, a plain white 'Minoxidil' box, a 'Castor Oil' bottle, a jar of 'Rice Water' — cluttered and lifeless, the graveyard of things that didn't work. Flat dull lighting, drained of color. CRITICAL: NONE of these left-side products may carry the 'Lumin' brand name or logo — they are unbranded generic competitor products with only plain generic labels like 'Biotin', 'Minoxidil', 'Castor Oil', 'Rice Water'. The word 'Lumin' must appear ONLY on the hero bottle on the right side, nowhere else.

RIGHT SIDE (~45% of frame): pure deep matte-black background. REFERENCE IMAGE 1 product bottle stands tall and hero on a round gold-lit podium under a dramatic warm spotlight, radiant gold glow, a few white capsules arranged elegantly at its base. A crisp thin vertical GOLD divider line separates the two worlds. REFERENCE IMAGE 2 is the black-and-gold luxury mood for the right side.

COLOR WORLD: left = desaturated cold grey. right = rich black + luminous gold. The stark contrast IS the message. Sony A7 with 50mm, clean studio product lighting on the right, hyperreal label legibility.

TEXT OVERLAY: Top spanning full width, bold cream-white sans-serif headline: 'Made for you. Finally.' Bottom-left small grey subtext over the left side: 'Built for someone else's hair.' Bottom-right small cream subtext: 'Targets the root causes of thinning in Black women.' plus a gold button: 'SHOP ROOT REVIVE'. All crisp and legible.

THE FEELING in 0.5s: 'finally, one made for ME.'{ANTI}"""),

  ("ad-4-edges-back", [f'{REF}/v4-black-woman-hair.jpg'],
   f"""You are a world-class advertising art director and beauty photographer creating a warm, trust-building social-proof ad for Lumin Root Revive, a hair-growth supplement for Black women.

{PROD_LOCK}

THE CONCEPT: an ICP-mirror social-proof wall in the brand's black + gold world. A joyful, real-feeling Black woman in her 30s with radiant honey-brown skin gently touches her healthy, FILLED-IN edge and temple with a soft proud smile, her natural curly hair styled back to proudly reveal a full restored hairline. Genuine warmth, not a stock pose. REFERENCE IMAGE 2 is the exact vibe of authentic joy and healthy natural hair to match.

Floating around her like clean rounded-corner black notification cards, each with gold ★★★★★ stars and cream text, three real customer quotes:
- 'My edges were filling in'
- 'Finally wearing ponytails again'
- 'Cheaper than my wig budget'

COLOR WORLD: warm matte black background with soft gold glow and gentle gold bokeh, honeyed golden lighting on her skin. REFERENCE IMAGE 1 product bottle glows in the lower-right corner on a small gold-lit surface. A bold gold badge reads '4.8 ★ | 45,000+ WOMEN'.

Nikon Z9 85mm f/1.8, soft warm beauty lighting, hyperreal skin and hair detail.

TEXT OVERLAY: Top, bold cream-white sans-serif headline: '6 weeks. Edges back.' Bottom, smaller subtext: 'Join 45,000+ women. 90-day money-back.' plus a gold button: 'START YOUR JOURNEY'. All text crisp, correctly spelled, legible.

THE FEELING in 0.5s: warmth, proof, 'this is real and it's for me.'{ANTI}"""),
]

target = sys.argv[2] if len(sys.argv) > 2 else None
for name, refs, prompt in ads:
    if target and target not in name:
        continue
    print(f'\n===== GENERATING {name} =====')
    gen(name, prompt, refs)
