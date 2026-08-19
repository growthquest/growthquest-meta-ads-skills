import json, urllib.request, base64, ssl, os, sys

api_key = os.environ['GEMINI_API_KEY']
ctx = ssl.create_default_context()
RUN = sys.argv[1]
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
    payload = json.dumps({'contents': [{'parts': parts}],
        'generationConfig': {'responseModalities': ['TEXT', 'IMAGE'], 'imageConfig': {'aspectRatio': '1:1'}}}).encode()
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent?key={api_key}'
    req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
    try:
        resp = urllib.request.urlopen(req, timeout=240, context=ctx)
    except urllib.error.HTTPError as e:
        print(f'[{name}] HTTP {e.code}: {e.read()[:300]}'); return
    data = json.loads(resp.read())
    ok = False
    for part in data.get('candidates', [{}])[0].get('content', {}).get('parts', []):
        if 'inlineData' in part:
            img = base64.b64decode(part['inlineData']['data'])
            with open(f'{BASE}/{name}.png', 'wb') as f:
                f.write(img)
            print(f'[{name}] SAVED {len(img)} bytes'); ok = True
        elif 'text' in part:
            print(f'[{name}] note: {part["text"][:120]}')
    if not ok:
        print(f'[{name}] NO IMAGE: {json.dumps(data)[:300]}')

PROD = ("REFERENCE IMAGE 1 is the ACTUAL Lumin Root Revive product. Reproduce this exact bottle with "
    "photographic accuracy: clear glass bottle, brushed SILVER metallic screw lid (never black), matte "
    "BLACK label with white 'Lumin', huge white 'ROOT REVIVE', gold sub-lines 'BLACK SEED EXTRACT / "
    "BAMBOO EXTRACT / PUMPKIN SEED EXTRACT / +17 Growth ingredients', a GOLD band near the bottom reading "
    "'DIETARY SUPPLEMENT 60 CAPSULES', white capsules inside. Match every logo, colour and word exactly. ")

ANTI = ("\n\nThis must look like a bold, award-winning DTC campaign someone screenshots and sends to a friend, "
    "NOT a generic stock photo. All text crisp, correctly spelled, high-contrast, instantly legible at phone "
    "size. STRICT: do NOT use em dashes or en dashes (— –) anywhere; use only periods, commas, or the middot '·' "
    "exactly as written. The bottle lid must be SILVER.")

ads = [
  ("ad-5-wake-your-roots", [f'{REF}/v5-glowing-roots.jpg'],
   f"""You are a world-class advertising art director and CGI/macro photographer creating a bold, conceptual ad for Lumin Root Revive, a hair-growth supplement for Black women.

{PROD}

THE CONCEPT (an impossible underground perspective of the scalp): a dramatic cross-section view showing what happens BENEATH a Black woman's scalp. Across the top of the frame, a thin band shows the top of her scalp with beautiful healthy dark coily hair. Below the scalp line, we descend underground into rich dark soil. On the LEFT, dormant follicles look like dry, grey, shrivelled dead roots in 'sleep mode', producing thin wispy hairs. On the RIGHT, the follicles have been REVIVED: glowing golden roots pulse with warm light and erupt upward into thick, healthy, full hair strands. In the centre, the REFERENCE IMAGE 1 product bottle stands, and glowing golden capsules dissolve into warm light that travels down through the soil and lights up the roots, waking them. REFERENCE IMAGE 2 is the glowing-roots visual style.

COLOUR WORLD: deep black soil, luminous warm gold light in the living roots, contrasted with cold grey on the dormant side. Cinematic, hyperreal macro, glowing bioluminescent-root feel. Canon EOS R5 100mm macro.

TEXT OVERLAY: Small gold all-caps kicker at very top: 'HAIR GROWTH STARTS AT THE ROOT'. Below, bold cream-white sans-serif headline: 'Wake your roots up.' Bottom subtext: 'Root Revive reactivates sleeping follicles from within. Made for Black women.' plus a gold button: 'SHOP NOW'.

FEELING in 0.5s: 'oh, THAT is what is happening under my scalp', wonder plus hope.{ANTI}"""),

  ("ad-6-reclaim-your-crown", [f'{REF}/v6-sculpted-hair.jpg'],
   f"""You are a world-class advertising art director and beauty photographer creating a bold, regal, conceptual ad for Lumin Root Revive, a hair-growth supplement for Black women.

{PROD}

THE CONCEPT (a literal visual metaphor of 'our hair is our crown'): a majestic royal CROWN sculpted entirely out of lush, healthy, natural Black coily/curly hair. The hair twists and rises into the tall points of a queen's crown, every coil defined and glossy, gold thread and tiny gold beads woven through it like jewels. It can be worn by a Black woman shown from the brow up (regal, chin lifted, serene powerful expression), OR presented as a floating hair-crown sculpture on a black pedestal. Set REFERENCE IMAGE 1 product bottle as the glowing centrepiece 'jewel' at the front centre of the crown, lit like fine jewellery, rendered LARGE and sharp enough that the label is fully readable. REFERENCE IMAGE 2 is the sculpted-hair reference. CRITICAL LABEL ACCURACY: the label text must be perfectly, correctly spelled exactly as: 'Lumin', 'ROOT REVIVE', 'BLACK SEED EXTRACT', 'BAMBOO EXTRACT', 'PUMPKIN SEED EXTRACT', '+17 Growth ingredients', 'DIETARY SUPPLEMENT', '60 CAPSULES'. Do NOT misspell any word (no 'BAMODO', no garbled text); every letter crisp.

COLOUR WORLD: the ENTIRE scene is deep matte black and luminous gold. Black background, gold rim light tracing every coil, warm gold glow on rich brown skin. Editorial Vogue-beauty lighting, Hasselblad medium format, hyperreal hair and skin texture.

TEXT OVERLAY: Small gold all-caps kicker top: 'GROW THICKER, FULLER HAIR'. Below, bold cream-white elegant serif headline: 'Reclaim your crown.' Bottom subtext: 'Fuller hair, healed from within. Made for Black women.' plus a gold pill button: 'TAKE THE QUIZ'.

FEELING in 0.5s: power, royalty, 'that is who I am'.{ANTI}"""),

  ("ad-7-done-hiding", [f'{REF}/v4-black-woman-hair.jpg', f'{REF}/v1-gold-portrait.jpg'],
   f"""You are a world-class advertising art director and cinematic portrait photographer creating an emotional, identity-driven ad for Lumin Root Revive, a hair-growth supplement for Black women.

{PROD}

THE CONCEPT (straight from real customer words, 'I was done hiding behind wigs'): a cinematic scene of liberation. A radiant Black woman in her 30s-40s steps FORWARD out of shadow into a warm shaft of golden light, her full, healthy, natural coily crown out and free, chin up, eyes closed or softly smiling with relief and pride, genuine emotion (not a posed model smile). BEHIND her, receding into the cool dark shadow, sits a wig on a faceless wig stand, left behind, clearly abandoned. The contrast: the dim grey past (the wig) versus the golden lit present (her real hair). On a surface in the warm light beside her, REFERENCE IMAGE 1 product bottle glows. REFERENCE IMAGE 2 and 3 are the vibe of authentic joy and healthy natural hair.

COLOUR WORLD: cool dark shadow on the left/behind (the wig), warm luminous gold light on her and the product. Cinematic, emotional, hyperreal skin and hair. Sony A7 85mm f/1.8.

TEXT OVERLAY: bold cream-white sans-serif headline top: 'Done hiding.' Bottom subtext: 'Real hair, regrown from within. Join 45,000+ Black women.' plus a gold button: 'START YOUR JOURNEY'.

FEELING in 0.5s: relief, freedom, 'I can finally be me'.{ANTI}"""),

  ("ad-8-edges-gardener", [f'{REF}/v8-tiltshift.jpg', f'{REF}/v4-black-woman-hair.jpg'],
   f"""You are a world-class advertising art director creating a whimsical, delightful, highly sharable miniature-diorama ad for Lumin Root Revive, a hair-growth supplement for Black women.

{PROD}

THE CONCEPT (a tilt-shift miniature world): an extreme close-up macro of the edges and hairline along a Black woman's temple, where the fine baby hairs and edges become a tiny GARDEN. A team of tiny miniature gardener figurines (in little overalls) lovingly tend her edges like crops: one waters a row of new baby-hair sprouts with a tiny watering can that pours glowing gold droplets, another plants tiny seedlings that become new hairs, another pushes a wheelbarrow of golden capsules. The edges visibly get fuller and healthier where they have worked. In the scene, REFERENCE IMAGE 1 product bottle stands giant in the background like a silo, the source of the golden capsules. Tilt-shift macro lens, shallow focus, toy-like miniature look. REFERENCE IMAGE 2 is the tilt-shift style; REFERENCE IMAGE 3 is the skin and hair reference.

COLOUR WORLD: warm honey-gold light, rich brown skin, healthy dark coily edges, gold accents, soft dark background. Playful but premium.

TEXT OVERLAY: bold cream-white rounded sans-serif headline top: 'Your edges need a gardener.' Bottom subtext: 'Root Revive feeds your follicles from within. Made for Black women.' plus a gold button: 'GROW YOUR EDGES'.

FEELING in 0.5s: a delighted smile, 'that is so cute I have to send this', plus instant understanding it grows edges.{ANTI}"""),
]

target = sys.argv[2] if len(sys.argv) > 2 else None
for name, refs, prompt in ads:
    if target and target not in name:
        continue
    print(f'\n===== {name} =====')
    gen(name, prompt, refs)
