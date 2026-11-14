"""Builds cards.html: 18 cake cards + backs, poker size (63 x 88 mm), nine to an A4 sheet.
Card data comes straight from sim.CAKES so the printed numbers are the simulated ones."""
import sys, html
sys.path.insert(0, "..")
from sim import CAKES
from art import svg, red_velvet

EFF = {
    "none": ("No tricks", "Just a lovely cake. Points only."),
    "tip": ("Tip jar", "+1 point."),
    "glaze": ("Glaze", "+1 point for each other cake in your oven."),
    "twofor": ("Second helping", "Take another Counter card and use it."),
    "draw": ("Chef's pick", "Use the top card of the deck."),
    "fresh": ("Fresh batch", "Bin the whole Counter and deal a new one."),
    "free_slam": ("Draught", "Slam any one of your opponent's cakes, at any stage."),
    "rest": ("Cooling rack", "Your cakes don't turn at the start of your next turn."),
    "scrap": ("Reheat", "Use the most recently discarded card."),
}
QUIRK = {"sturdy": ("Water bath", "Can't be slammed."), "preheated": ("Preheated", "Bake with the Risen edge up.")}
TAG = {"Souffle": "Shhh... don't slam the door!", "Celebration Cake": "Any excuse will do.", "Cookies": "Never enough in the jar.",
       "Choux Puffs": "Light as air. Mostly.", "Birthday Cake": "Make a wish. Blow hard.", "Cherry Bakewell": "Cherry on top. Obviously.",
       "Lemon Drizzle": "Sharp wit, sweet finish.", "Red Velvet": "Dressed to impress.", "Brownies": "Fudgy. Gooey. Unbothered.",
       "Victoria Sponge": "Jam, cream and a crown.", "Carrot Cake": "Cream cheese frosting, obviously.",
       "Blueberry & Lemon Cake": "Zesty, juicy, bursting.", "Pavlova": "Crisp outside, cloud inside.", "Coffee & Salted Pecan": "Sweet, salty, wide awake.",
       "Black Forest": "Dark, deep and cherry-topped.", "Wedding Cake": "Three tiers of patience.",
       "Cheesecake": "Slow, smooth, slam-proof.", "Fruitcake": "Holiday legend. Built to last."}
CARLY = {"Celebration Cake", "Cookies", "Birthday Cake", "Cherry Bakewell", "Lemon Drizzle", "Red Velvet", "Victoria Sponge",
         "Carrot Cake", "Blueberry & Lemon Cake", "Coffee & Salted Pecan", "Wedding Cake"}
FAM = {"quick": ("QUICK RISER", "#ff6f98", "#ffe3ec", "#ffb3c9"),
       "steady": ("STEADY BAKER", "#ffbe2e", "#fff2c9", "#ffe08a"),
       "slow": ("SLOW BURN", "#7f63ee", "#e9e2fd", "#c6b8f8")}

def family(d):
    pk = max(d)
    if d[0] == pk and d[0] > d[1]: return "quick"
    if d[2] == pk: return "slow" if d[2] > d[1] or d[1] == d[2] and d[2] >= 6 else "steady"
    return "steady"

ICO = {
 "batter": '<svg viewBox="0 0 24 24"><path d="M3 10h18q-1 10-9 10T3 10z" fill="currentColor"/><path d="M6 10q3-7 6-2 3-5 6 2" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>',
 "risen": '<svg viewBox="0 0 24 24"><path d="M12 21V6M5.5 12.5 12 5l6.5 7.5" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 "golden": '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="5" fill="currentColor"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M19 5l-2 2M7 17l-2 2" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>',
 "dark": '<svg viewBox="0 0 24 24"><path d="M12 2Q19 9 17 16q-1 6-5 6t-5-6q-1-4 3-7 0-3 2-7z" fill="currentColor"/></svg>',
}
STAGES = [("left", "RISEN", "risen"), ("bottom", "GOLDEN", "golden"), ("right", "DARK", "dark")]

def pill(edge, num, label, icon, peak=False):
    if num is None:
        inner = f'<span class="ico">{ICO[icon]}</span><span class="lab">{label}</span>'
    else:
        inner = (f'<span class="num{" peak" if peak else ""}">{num}</span><span class="lab">{label}</span>'
                 f'<span class="ico">{ICO[icon]}</span>')
    return f'<div class="pill e-{edge}{" batter" if num is None else ""}">{inner}</div>'

def card(i, name, d, eff, quirk):
    fam = family(d); ftag, c_main, c_pale, c_mid = FAM[fam]
    pk = max(d); nm = html.escape(name.replace("Souffle", "Souffl&eacute;")).replace("&amp;eacute;", "&eacute;")
    en, et = EFF[eff]
    q = QUIRK.get(quirk)
    own = '<span class="own">&#9733; Carly&rsquo;s</span>' if name in CARLY else ''
    qhtml = f'<div class="quirk"><b>{q[0]}</b> {q[1]}</div>' if q else ""
    pills = pill("top", None, "BATTER", "batter")
    first_peak = d.index(pk)
    for k, (edge, lab, ic) in enumerate(STAGES):
        pills += pill(edge, d[k], lab, ic, peak=(k == first_peak))
    return f'''<div class="card" style="--main:{c_main};--pale:{c_pale};--mid:{c_mid}">
  <div class="dots"></div>{pills}
  <div class="panel">
    <div class="name{" two" if len(name) > 16 else ""}{" xtwo" if len(name) > 21 else ""}">{nm}</div>
    <div class="tag">{html.escape(TAG[name])}</div>
    <div class="art">{svg(name)}</div>
    {qhtml}
    <div class="eff"><span class="et">{html.escape(en)}</span><span class="ex">{html.escape(et)}</span></div>
    <div class="foot"><span class="fam">{ftag}</span>{own}<span class="no">{i:02d}/18</span></div>
  </div>
</div>'''

BACK = ('''<div class="card back"><svg viewBox="0 0 63 88" xmlns="http://www.w3.org/2000/svg">
<defs><pattern id="sc" width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="4.5" cy="4.5" r="1.7" fill="#fff" opacity=".35"/></pattern>
<pattern id="sc2" width="9" height="9" x="4.5" y="4.5" patternUnits="userSpaceOnUse"><circle cx="4.5" cy="4.5" r="1.1" fill="#ffd23f" opacity=".6"/></pattern></defs>
<rect width="63" height="88" fill="#ff5c8a"/><rect width="63" height="88" fill="url(#sc)"/><rect width="63" height="88" fill="url(#sc2)"/>
<rect x="5" y="5" width="53" height="78" rx="5" fill="none" stroke="#fff" stroke-width="1.2" stroke-dasharray="1.4 2.2" stroke-linecap="round"/>
<circle cx="31.5" cy="38" r="21" fill="#fff" stroke="#3a2118" stroke-width="1.3"/>
<circle cx="31.5" cy="38" r="17.5" fill="#ffe3ec"/>
<svg x="13.5" y="24.5" width="36" height="25.2" viewBox="0 0 120 84">{CAKE}</svg>
<path d="M13 28 A19 19 0 0 1 26 19.5" fill="none" stroke="#7f63ee" stroke-width="2" stroke-linecap="round"/><path d="M27.2 16.4 L28 22.6 L22.6 19.6Z" fill="#7f63ee"/>
<text x="31.5" y="68.5" text-anchor="middle" font-family="Fredoka, 'Baloo 2', sans-serif" font-weight="700" font-size="6.6" fill="#fff" stroke="#3a2118" stroke-width="1.9" paint-order="stroke" stroke-linejoin="round" letter-spacing=".3">CARLY CAKES</text>
<text x="31.5" y="75.6" text-anchor="middle" font-family="Nunito, sans-serif" font-weight="700" font-size="2.5" fill="#fff" letter-spacing=".3">BAKING GAME &#183; 1-2 BAKERS</text>
<path d="M8 12 l1.2 2.4 2.4 1.2 -2.4 1.2 -1.2 2.4 -1.2 -2.4 -2.4 -1.2 2.4 -1.2z M55 70 l1 2 2 1 -2 1 -1 2 -1 -2 -2 -1 2 -1z" fill="#fff" stroke="#3a2118" stroke-width=".6"/>
</svg></div>''').replace('{CAKE}', red_velvet())

CSS = '''
@page { size: A4; margin: 0 }
* { box-sizing: border-box; margin: 0; padding: 0 }
html, body { background: #fff; -webkit-print-color-adjust: exact; print-color-adjust: exact }
body { font-family: "Nunito", system-ui, sans-serif; color: #3a2118 }
.sheet { width: 210mm; height: 297mm; position: relative; overflow: hidden; page-break-after: always; break-after: page }
.grid { position: absolute; left: 10.5mm; top: 16.5mm; width: 189mm; height: 264mm; display: grid; grid-template-columns: repeat(3, 63mm); grid-template-rows: repeat(3, 88mm) }
.mark { position: absolute; background: #9a8c84 }
.mark.v { width: .2mm; height: 5mm } .mark.h { height: .2mm; width: 5mm }
.note { position: absolute; left: 10.5mm; right: 10.5mm; bottom: 5.5mm; font-size: 2.7mm; color: #7b665a; display: flex; justify-content: space-between; gap: 4mm }
.card { width: 63mm; height: 88mm; position: relative; overflow: hidden; background: var(--main) }
.dots { position: absolute; inset: 0; background-image: radial-gradient(circle, rgba(255,255,255,.55) 0.45mm, transparent 0.5mm); background-size: 4.2mm 4.2mm }
.panel { position: absolute; left: 8mm; top: 8mm; width: 47mm; height: 72mm; background: #fffdf8; border: .5mm solid #3a2118; border-radius: 3mm; padding: 1.5mm 2mm 1.2mm; display: flex; flex-direction: column; gap: .7mm }
.name { font-family: "Fredoka", sans-serif; font-weight: 700; font-size: 4.9mm; line-height: 1.05; text-align: center; letter-spacing: .1mm }
.tag { font-style: italic; font-weight: 700; font-size: 2.35mm; text-align: center; color: #7b665a; line-height: 1.1 }
.art { background: var(--pale); border: .4mm solid #3a2118; border-radius: 2.2mm; margin-top: .4mm; aspect-ratio: 120 / 84; width: 100%; overflow: hidden }
.art svg { width: 100%; height: 100%; display: block }
.quirk { background: #3a2118; color: #fff; font-size: 2.4mm; line-height: 1.15; padding: .5mm 1.6mm; border-radius: 1.2mm; text-align: center }
.quirk b { font-family: "Fredoka", sans-serif; letter-spacing: .1mm; text-transform: uppercase; color: var(--mid) }
.eff { flex: 1; min-height: 0; background: var(--pale); border: .4mm solid #3a2118; border-radius: 2mm; padding: .9mm 1.8mm; display: flex; flex-direction: column; justify-content: center; gap: .3mm; text-align: center }
.eff .et { font-family: "Fredoka", sans-serif; font-weight: 600; font-size: 3.1mm; line-height: 1 }
.eff .ex { font-weight: 700; font-size: 2.55mm; line-height: 1.14 }
.foot { display: flex; justify-content: space-between; align-items: center; font-size: 2.1mm; font-weight: 700; padding: 0 .4mm }
.fam { font-family: "Fredoka", sans-serif; letter-spacing: .2mm; background: var(--main); color: #3a2118; padding: .3mm 1.6mm; border-radius: 1mm; border: .3mm solid #3a2118 }
.no { color: #7b665a }
.own { font-family: "Fredoka", sans-serif; font-weight: 600; letter-spacing: .15mm; color: #3a2118; font-size: 2.15mm }
.name.two { font-size: 3.8mm; line-height: 1.25; white-space: nowrap }
.name.xtwo { font-size: 3.3mm; line-height: 1.45 }
.pill { position: absolute; width: 25mm; height: 7mm; margin-left: -12.5mm; margin-top: -3.5mm; background: #fffdf8; border: .45mm solid #3a2118; border-radius: 3.5mm; display: flex; align-items: center; gap: 1mm; padding: 0 1.6mm 0 .35mm }
.e-top { left: 31.5mm; top: 4.3mm } .e-bottom { left: 31.5mm; top: 83.7mm; transform: rotate(180deg) }
.e-left { left: 4.3mm; top: 44mm; transform: rotate(-90deg) } .e-right { left: 58.7mm; top: 44mm; transform: rotate(90deg) }
.num { flex: none; width: 5.8mm; height: 5.8mm; border-radius: 50%; background: var(--pale); border: .4mm solid #3a2118; font-family: "Fredoka", sans-serif; font-weight: 700; font-size: 4.2mm; line-height: 5mm; text-align: center }
.num.peak { background: #ffd23f; box-shadow: 0 0 0 .35mm #fffdf8, 0 0 0 .75mm #3a2118 }
.lab { font-family: "Fredoka", sans-serif; font-weight: 600; font-size: 2.6mm; letter-spacing: .25mm; flex: 1 }
.ico { width: 3.9mm; height: 3.9mm; color: var(--main); flex: none; filter: drop-shadow(0 0 .01mm #3a2118) } .ico svg { width: 100%; height: 100%; display: block; stroke: #3a2118; stroke-width: .0 }
.ico svg * { paint-order: stroke }
.batter { padding-left: 1.4mm } .batter .lab { flex: none }
.turn { font-size: 2.1mm; font-weight: 700; color: #7b665a; white-space: nowrap }
.card.back { background: #ff5c8a } .card.back svg { width: 100%; height: 100% }
'''

def marks():
    out = []
    xs = [10.5 + 63 * i for i in range(4)]; ys = [16.5 + 88 * i for i in range(4)]
    for x in xs:
        out.append(f'<div class="mark v" style="left:{x-.1:.2f}mm;top:{16.5-6:.2f}mm"></div><div class="mark v" style="left:{x-.1:.2f}mm;top:{280.5+1:.2f}mm"></div>')
    for y in ys:
        out.append(f'<div class="mark h" style="top:{y-.1:.2f}mm;left:{10.5-6:.2f}mm"></div><div class="mark h" style="top:{y-.1:.2f}mm;left:{199.5+1:.2f}mm"></div>')
    return "".join(out)

def sheet(inner, note_l, note_r):
    return f'<div class="sheet"><div class="grid">{inner}</div>{marks()}<div class="note"><span>{note_l}</span><span>{note_r}</span></div></div>'

def build():
    cards = [card(i + 1, n, list(d), e, q) for i, (n, d, e, q) in enumerate(CAKES)]
    pages = []
    for s in range(2):
        chunk = cards[s * 9:(s + 1) * 9]
        pages.append(sheet("".join(chunk), f"Carly Cakes &middot; Cakes {s*9+1:02d}&ndash;{s*9+9:02d} &middot; fronts",
                           "Print at 100% on A4, double-sided, flip on the long edge. Cut on the marks."))
        pages.append(sheet(BACK * 9, "Carly Cakes &middot; backs", "Back of the sheet before. Cut on the marks."))
    head = ('<meta charset="utf-8"><title>Carly Cakes cards</title>'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600;700&family=Nunito:ital,wght@0,600;0,700;1,700&display=swap">'
            f'<style>{CSS}</style>')
    open("cards.html", "w").write(f"<!doctype html><html><head>{head}</head><body>{''.join(pages)}</body></html>")
    print("cards.html written;", len(cards), "cards")

if __name__ == "__main__":
    build()
