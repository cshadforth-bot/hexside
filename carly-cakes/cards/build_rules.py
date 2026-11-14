"""Builds rules.html: the Carly Cakes rules sheet, four A4 pages, cartoon style with worked examples.
Example cards are the real card faces (build_cards.card), turned to show the dial."""
import sys, json
sys.path.insert(0, "..")
from sim import CAKES
from build_cards import card, CSS as CARD_CSS
from art import svg as cake_svg, OUT
from art_rival import character, by_the_book, sparkle

L = json.load(open("../ladder.json")); RV = json.load(open("../rival_results.json"))

CSS = CARD_CSS + '''
html, body { background: #fff }
.pg { width: 210mm; height: 297mm; position: relative; overflow: hidden; page-break-after: always; break-after: page; padding: 10mm 12mm 9mm; background: #fffdf8; display: flex; flex-direction: column; gap: 4mm; font-size: 3.15mm; line-height: 1.3 }
.banner { height: 31mm; border-radius: 5mm; background: #ff6f98; border: .5mm solid #3a2118; position: relative; overflow: hidden; display: flex; align-items: center; padding: 0 7mm; gap: 6mm; flex: none }
.banner::before, .hdr::before { content: ""; position: absolute; inset: 0; background-image: radial-gradient(circle, rgba(255,255,255,.5) .5mm, transparent .55mm); background-size: 4.6mm 4.6mm }
.banner h1 { position: relative; font-family: "Fredoka", sans-serif; font-weight: 700; font-size: 13.5mm; line-height: .95; color: #fff; -webkit-text-stroke: 1.6mm #3a2118; paint-order: stroke fill; letter-spacing: .2mm }
.banner .sub { position: relative; display: flex; gap: 1.6mm; flex-wrap: wrap; margin-top: 2.2mm }
.chip { font-family: "Fredoka", sans-serif; font-weight: 600; font-size: 2.9mm; background: #fffdf8; border: .4mm solid #3a2118; border-radius: 3mm; padding: .6mm 2.4mm; white-space: nowrap }
.banner .cake { position: absolute; right: 4mm; top: 2mm; width: 50mm; height: 35mm }
.banner .cake svg { width: 100%; height: 100% }
.hdr { height: 15mm; border-radius: 4mm; background: #ff6f98; border: .5mm solid #3a2118; position: relative; overflow: hidden; display: flex; align-items: center; justify-content: space-between; padding: 0 6mm; flex: none }
.hdr b { position: relative; font-family: "Fredoka", sans-serif; font-weight: 700; font-size: 7.5mm; color: #fff; -webkit-text-stroke: 1.1mm #3a2118; paint-order: stroke fill }
.hdr span { position: relative; font-family: "Fredoka", sans-serif; font-weight: 600; font-size: 3.2mm; background: #fffdf8; border: .4mm solid #3a2118; border-radius: 3mm; padding: .6mm 3mm }
h2 { font-family: "Fredoka", sans-serif; font-weight: 700; font-size: 5mm; line-height: 1; text-transform: uppercase; letter-spacing: .25mm; display: inline-block; padding: 1.1mm 3.4mm; border-radius: 2.6mm; border: .45mm solid #3a2118; color: #3a2118; margin-bottom: 2mm }
.h-pink { background: #ffb3c9 } .h-yellow { background: #ffd966 } .h-violet { background: #c6b8f8 } .h-teal { background: #8fe0d4 }
h3 { font-family: "Fredoka", sans-serif; font-weight: 600; font-size: 3.5mm; margin-bottom: .6mm }
p { margin-bottom: 1.2mm } b { font-weight: 800 } .m { color: #7b665a }
ol, ul { padding-left: 4.6mm } li { margin-bottom: .8mm }
.row { display: flex; gap: 6mm } .col { flex: 1; min-width: 0 }
.cardfig { width: 46mm; height: 64mm; flex: none; position: relative } .cardfig .card { transform: scale(.73); transform-origin: top left; position: absolute; left: 0; top: 0; border-radius: 3mm; border: .45mm solid #3a2118 }
/* rotating example cards: a square box so the turned card never overflows */
.rot { position: relative; flex: none; overflow: hidden; contain: strict } .rin { position: absolute; left: 50%; top: 50%; width: 63mm; height: 88mm; transform-origin: center }
.rin .card { border-radius: 3mm; border: .45mm solid #3a2118 }
.tiles { display: grid; grid-template-columns: repeat(4, 1fr); gap: 2.6mm }
.tile { border: .45mm solid #3a2118; border-radius: 3mm; padding: 2mm 2.4mm; display: flex; flex-direction: column; gap: .8mm; background: #fff; position: relative }
.tile .t { font-family: "Fredoka", sans-serif; font-weight: 700; font-size: 4.3mm; line-height: 1 }
.tile .tico { width: 15mm; height: 15mm; align-self: flex-end; margin: -1mm 0 -1mm }
.tile.pull { background: #fff3c4 } .tile.bake { background: #ffe0ea } .tile.slam { background: #e6defc } .tile.bin { background: #d6f3ee }
.bubble { position: relative; background: #fff; border: .45mm solid #3a2118; border-radius: 4mm; padding: 2mm 3.2mm; font-weight: 700; font-size: 3.2mm; line-height: 1.25 }
.bubble::after { content: ""; position: absolute; width: 3.4mm; height: 3.4mm; background: #fff; border: solid #3a2118; border-width: 0 0 .45mm .45mm; transform: rotate(45deg) }
.bubble.l::after { left: -1.9mm; top: 5mm; transform: rotate(45deg) } .bubble.r::after { right: -1.9mm; top: 5mm; transform: rotate(-135deg) }
.bubble.b::after { left: 8mm; bottom: -1.9mm; transform: rotate(-45deg) }
.chara { width: 36mm; height: 25.2mm; flex: none } .chara svg { width: 100%; height: 100% }
.steps3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 2.4mm; margin-top: 1.4mm }
.mini { display: flex; align-items: center; gap: 1.6mm; margin-bottom: 1.2mm }
.chip.e { background: #ffe9a8 } .chip.q { background: #3a2118; color: #fff }
.efgrid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.8mm 3mm }
.ef { display: flex; gap: 2.4mm; align-items: center; background: #fff; border: .4mm solid #3a2118; border-radius: 3mm; padding: .9mm 2.2mm }
.ef svg { width: 10mm; height: 10mm; flex: none } .ef b { font-family: "Fredoka", sans-serif; font-weight: 700; font-size: 3.4mm; display: block; line-height: 1.1 } .ef span { font-size: 2.9mm; line-height: 1.22; display: block }
.fam3 { display: flex; gap: 2mm; margin-top: 1.4mm } .fam3 span { flex: 1; text-align: center; border: .4mm solid #3a2118; border-radius: 2.4mm; padding: 1mm 1.4mm; font-size: 2.9mm; line-height: 1.2 }
.fam3 b { display: block; font-family: "Fredoka", sans-serif; font-size: 3.2mm }
/* storyboards */
.story { display: grid; grid-template-columns: repeat(3, 1fr); gap: 3mm }
.sp { border: .45mm solid #3a2118; border-radius: 3.4mm; background: #fff; padding: 2mm 2.4mm 2.4mm; display: flex; flex-direction: column; align-items: center; gap: 1mm; position: relative; text-align: center }
.sp .cap { font-size: 3mm; line-height: 1.22 } .sp .cap b { font-family: "Fredoka", sans-serif; font-weight: 700; font-size: 3.4mm }
.sp .stepno { position: absolute; left: 2mm; top: 2mm; width: 6.4mm; height: 6.4mm; border-radius: 50%; background: #ffd23f; border: .4mm solid #3a2118; font-family: "Fredoka", sans-serif; font-weight: 700; font-size: 4mm; line-height: 5.6mm; text-align: center; z-index: 3 }
.burst { position: absolute; z-index: 4; font-family: "Fredoka", sans-serif; font-weight: 700; font-size: 4.6mm; color: #ffd23f; -webkit-text-stroke: 1mm #3a2118; paint-order: stroke fill; transform: rotate(-12deg) }
.dialrow { display: grid; grid-template-columns: repeat(5, 1fr); gap: 1.6mm; align-items: start }
.dtile { border: .45mm solid #3a2118; border-radius: 3.2mm; background: #fff; padding: 1.4mm 1mm 1.8mm; display: flex; flex-direction: column; align-items: center; gap: .6mm; text-align: center }
.dtile .big { font-family: "Fredoka", sans-serif; font-weight: 700; font-size: 6.4mm; line-height: 1; width: 11mm; height: 11mm; border-radius: 50%; background: #fff; border: .45mm solid #3a2118; display: flex; align-items: center; justify-content: center }
.dtile .big.gold { background: #ffd23f; box-shadow: 0 0 0 .5mm #fffdf8, 0 0 0 1mm #3a2118 }
.dtile .big.sad { background: #e8e1dc }
.dtile .cap { font-size: 2.85mm; line-height: 1.2; min-height: 7.2mm } .dtile .cap b { font-family: "Fredoka", sans-serif; font-weight: 700 }
.dtile .art { width: 28mm; height: 19.6mm; border: .4mm solid #3a2118; border-radius: 2mm; background: #e8e1dc; overflow: hidden; margin: 7mm 0 }
.arrowrow { display: flex; justify-content: space-between; font-family: "Fredoka", sans-serif; font-weight: 600; font-size: 3mm; color: #7b665a; margin: 0 7mm }
.scene { display: flex; gap: 3mm; align-items: stretch }
.box { border: .45mm solid #3a2118; border-radius: 3.4mm; padding: 2mm 2.6mm; background: #fff; display: flex; flex-direction: column; gap: 1mm }
.box .lab2 { font-family: "Fredoka", sans-serif; font-weight: 700; font-size: 3.5mm; text-transform: uppercase; letter-spacing: .2mm }
.cards-line { display: flex; gap: 1mm; justify-content: center }
.cards-line .rot { margin: 0 -2.2mm }
.tag2 { font-family: "Fredoka", sans-serif; font-weight: 600; font-size: 2.7mm; text-align: center; margin-top: -4mm; position: relative; z-index: 3 }
.call { border: .5mm dashed #3a2118; border-radius: 4mm; padding: 2.6mm 3.6mm; background: #fff1f5 }
.gr { display: grid; grid-template-columns: repeat(3, 1fr); gap: 2.6mm }
.gt { border: .45mm solid #3a2118; border-radius: 3.4mm; padding: 1.6mm 2mm 2mm; display: flex; flex-direction: column; align-items: center; text-align: center; gap: .4mm }
.gt .gart { width: 33mm; height: 23.1mm; border-radius: 2.2mm; border: .4mm solid #3a2118; overflow: hidden; background: rgba(255,255,255,.75) }
.gt .gart svg { width: 100%; height: 100% }
.gt b { font-family: "Fredoka", sans-serif; font-weight: 700; font-size: 4mm; line-height: 1.1 } .gt .rg { font-size: 3mm; font-weight: 800 } .gt .ms { font-size: 2.85mm; color: #5b463c; line-height: 1.2 }
.gt .wl { font-family: "Fredoka", sans-serif; font-weight: 600; font-size: 2.8mm; padding: .2mm 2.4mm; border-radius: 2mm; border: .35mm solid #3a2118; background: #fff }
.crown { position: absolute; width: 10mm; height: 7mm }
.pg:last-child { page-break-after: auto; break-after: auto }
.foot2 { margin-top: auto; display: flex; justify-content: space-between; font-size: 2.6mm; color: #7b665a }
'''

def rot(name, k=0, s=.4):
    i, c = next((i + 1, c) for i, c in enumerate(CAKES) if c[0] == name)
    side = 88 * s
    return (f'<div class="rot" style="width:{side:.1f}mm;height:{side:.1f}mm"><div class="rin" '
            f'style="transform:translate(-50%,-50%) rotate({k*90}deg) scale({s})">{card(i, c[0], list(c[1]), c[2], c[3])}</div></div>')

def svgi(inner, vb="0 0 40 40"):
    return f'<svg viewBox="{vb}" xmlns="http://www.w3.org/2000/svg">{inner}</svg>'

def st(w=2.2): return f'stroke="{OUT}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"'

ICONS = {
 "pull": svgi(f'<path d="M20 3 L24 13 L35 12 L27 19 L32 30 L20 24 L8 30 L13 19 L5 12 L16 13Z" fill="#ffd23f" {st()}/><text x="20" y="21.5" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="11" fill="{OUT}">+9</text>'),
 "bake": svgi(f'<rect x="5" y="8" width="30" height="27" rx="4" fill="#9aa5b1" {st()}/><rect x="9" y="16" width="22" height="15" rx="3" fill="#2a3340" {st(1.8)}/><circle cx="12" cy="12" r="1.8" fill="#fff"/><circle cx="18" cy="12" r="1.8" fill="#fff"/><path d="M14 28 Q20 20 26 28Z" fill="#ffb25e" {st(1.5)}/><path d="M12 22 q2 -2 4 0" fill="none" stroke="#fff" stroke-width="1.4" opacity=".6"/>'),
 "slam": svgi(f'<rect x="12" y="6" width="24" height="30" rx="4" fill="#9aa5b1" {st()}/><rect x="16" y="11" width="16" height="11" rx="2.5" fill="#2a3340" {st(1.6)}/><path d="M3 14 h7 M2 21 h8 M3 28 h7" {st(2)} fill="none"/><text x="24" y="33.5" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="8" fill="#ffd23f" stroke="{OUT}" stroke-width="1.6" paint-order="stroke">!!</text>'),
 "bin": svgi(f'<path d="M9 13 L12 36 Q20 39 28 36 L31 13Z" fill="#8fe0d4" {st()}/><rect x="6" y="8" width="28" height="6" rx="3" fill="#7bd0c4" {st()}/><path d="M17 4 h6 v4 h-6z" fill="#7bd0c4" {st(1.8)}/><path d="M16 18 V32 M20 18 V33 M24 18 V32" {st(1.8)} fill="none"/>'),
 "tip": svgi(f'<rect x="9" y="12" width="22" height="24" rx="5" fill="#e8f6ff" {st()}/><rect x="7" y="7" width="26" height="7" rx="3" fill="#ffd23f" {st()}/><circle cx="16" cy="31" r="3.6" fill="#ffd23f" {st(1.5)}/><circle cx="25" cy="30" r="3.6" fill="#ffd23f" {st(1.5)}/><circle cx="20" cy="24" r="3.6" fill="#ffd23f" {st(1.5)}/><text x="20" y="26" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="5" fill="{OUT}">+1</text>'),
 "glaze": svgi(f'<path d="M5 14 Q20 6 35 14 L35 18 Q31 18 31 24 Q31 30 28 30 Q25 30 25 22 Q22 22 21 28 Q20 34 17 34 Q14 34 14 24 Q10 22 9 28 Q8 32 6 30 Q5 24 5 18Z" fill="#ff93b9" {st()}/><circle cx="14" cy="12" r="1.1" fill="#fff"/><circle cx="24" cy="11" r="1.1" fill="#ffd23f"/><circle cx="29" cy="14" r="1.1" fill="#4fc3f7"/>'),
 "second": svgi(f'<rect x="4" y="8" width="18" height="25" rx="3" fill="#ffe0ea" {st()} transform="rotate(-10 13 20)"/><rect x="16" y="9" width="18" height="25" rx="3" fill="#fff3c4" {st()} transform="rotate(8 25 21)"/><path d="M25 17 v10 M20 22 h10" {st(2.6)} fill="none"/>'),
 "chef": svgi(f'<rect x="8" y="10" width="20" height="26" rx="3" fill="#c6b8f8" {st()}/><rect x="12" y="6" width="20" height="26" rx="3" fill="#ffe0ea" {st()}/><path d="M22 14 l2 5 5 .5 -4 3.5 1.4 5.2 -4.4 -3 -4.4 3 1.4 -5.2 -4 -3.5 5 -.5Z" fill="#ffd23f" {st(1.4)}/>'),
 "fresh": svgi(f'<path d="M8 20 A12 12 0 0 1 28 11" fill="none" {st(2.6)}/><path d="M30 5 L29.5 14 L21 11Z" fill="{OUT}"/><path d="M32 20 A12 12 0 0 1 12 29" fill="none" {st(2.6)}/><path d="M10 35 L10.5 26 L19 29Z" fill="{OUT}"/><rect x="15" y="15" width="10" height="10" rx="2" fill="#8fe0d4" {st(1.6)}/>'),
 "draught": svgi(f'<rect x="19" y="5" width="17" height="30" rx="3" fill="#9aa5b1" {st()}/><rect x="22" y="10" width="11" height="9" rx="2" fill="#2a3340" {st(1.5)}/><path d="M3 14 h12 Q18 14 17 11 M3 22 h10 Q16 22 15 25 M5 30 h8" fill="none" {st(2)}/>'),
 "rest": svgi(f'<path d="M20 4 V36 M6 12 L34 28 M6 28 L34 12" {st(2.4)} fill="none" stroke="#4fc3f7"/><path d="M20 4 V36 M6 12 L34 28 M6 28 L34 12" stroke="#4fc3f7" stroke-width="1.2" stroke-linecap="round" fill="none"/><circle cx="20" cy="20" r="4" fill="#e8f6ff" {st(1.6)}/>'),
 "reheat": svgi(f'<rect x="9" y="14" width="20" height="24" rx="3" fill="#fff3c4" {st()} transform="rotate(-6 19 26)"/><path d="M26 4 Q36 14 33 24 Q31 32 24 32 Q18 32 17 25 Q16 19 21 15 Q21 9 26 4Z" fill="#ff7a2e" {st()}/><path d="M25 17 Q29 21 27 26 Q25 29 22 27 Q21 23 25 17Z" fill="#ffd23f" {st(1.2)}/>'),
}

def guide(tilt=-6):
    return f'<svg viewBox="0 0 120 84" xmlns="http://www.w3.org/2000/svg">{character("#f2c9a5", "#ff6f98", "dots", "grin", tilt, arms="up")}{sparkle(14, 12, 4, "#ffe14d")}{sparkle(108, 14, 4, "#ffe14d")}</svg>'

def rival_svg():
    return f'<svg viewBox="0 0 120 84" xmlns="http://www.w3.org/2000/svg">{by_the_book()}</svg>'

def hdr(title, tag):
    return f'<div class="hdr"><b>{title}</b><span>{tag}</span></div>'

def footer(n):
    return f'<div class="foot2"><span>Carly Cakes &middot; rules, draft 0.1</span><span>Page {n} of 4</span></div>'

# --------------------------------------------------------------------------- pages
def effects_grid():
    E = [("tip", "Tip jar", "+1 point."), ("glaze", "Glaze", "+1 point for each other cake in your oven."),
         ("second", "Second helping", "Take another Counter card and use it."), ("chef", "Chef's pick", "Use the top card of the deck."),
         ("fresh", "Fresh batch", "Bin the whole Counter and deal a new one."), ("draught", "Draught", "Slam any one of your opponent's cakes, at any stage."),
         ("rest", "Cooling rack", "Your cakes don't turn at the start of your next turn."), ("reheat", "Reheat", "Use the most recently discarded card.")]
    return "".join(f'<div class="ef">{ICONS[k]}<div><b>{n}</b><span>{t}</span></div></div>' for k, n, t in E)

GRADES = [("Burnt Offering", "36 or less", "Lose", "#e8d3c6", "Burnt Cake", "The batch is ruined."),
          ("Soggy Bottom", "37&ndash;42", "Lose", "#d6ecf7", "Soggy Cake", "It rose, then it didn't hold."),
          ("Apprentice", "43&ndash;49", "Win", "#fff2c9", "Cookies", "You got it out of the oven."),
          ("Journeyman", "50&ndash;56", "Win", "#ffe0c2", "Birthday Cake", "Competent. You'd get hired."),
          ("Head Baker", "57&ndash;62", "Win", "#ffd6e3", "Victoria Sponge", "You ran the bakery well."),
          ("Master Baker", "63+", "Win", "#e3dbfb", "Wedding Cake", "Near-perfect. Rare.")]

def grade_tiles():
    return "".join(f'<div class="gt" style="background:{bg}"><div class="gart">{cake_svg(art)}</div><b>{n}</b><span class="rg">{r}</span>'
                   f'<span class="wl" style="{"background:#ffd23f" if w == "Win" else ""}">{w}</span><span class="ms">{m}</span></div>'
                   for n, r, w, bg, art, m in GRADES)

def page1():
    fan = "".join(f'<div style="position:absolute;left:{x}mm;top:{y}mm;transform:rotate({r}deg);transform-origin:bottom center">{rot(n, 0, .27)}</div>'
                  for n, x, y, r in (("Wedding Cake", 4, 5, -14), ("Cookies", 16, 1, -7), ("Birthday Cake", 28, -1, 0), ("Red Velvet", 40, 1, 7), ("Lemon Drizzle", 52, 5, 14)))
    tiles = [("pull", "Pull", "Take a cake that is Risen, Golden or Dark. Score the number on its top edge, do its effect, then put it on the Sold pile."),
             ("bake", "Bake", "Take a Counter card into an empty rack, Batter edge up."),
             ("slam", "Slam", "Tuck a Counter card sideways under an opposing cake that is Batter or Risen. Turn that cake a quarter-turn at once. The card goes in the Bin."),
             ("bin", "Bin", "Take a Counter card and put it in the Bin, so your rival can't have it.")]
    th = "".join(f'<div class="tile {k}"><div class="tico">{ICONS[k]}</div><span class="t">{t}</span><span>{d}</span></div>' for k, t, d in tiles)
    c0 = CAKES[0]
    return f"""<div class="pg">
<div class="banner"><div><h1>Carly Cakes</h1><div class="sub"><span class="chip">1&ndash;2 bakers</span><span class="chip">25 minutes</span><span class="chip">18 cards</span><span class="chip">ages 10+</span></div></div>
<div class="cake">{cake_svg("Victoria Sponge")}</div></div>

<div class="row" style="align-items:center">
 <div class="col"><h2 class="h-pink">The idea</h2>
 <p>You run a one-oven bakery. Every card is a cake with a <b>dial</b>: you turn it every turn, it rises, peaks and then burns. <b>Pull</b> each cake when it is worth the most. Or <b>slam the oven door</b> on a rival's rising cake and wreck their timing. Most points wins, and you can play alone too.</p></div>
 <div style="display:flex;gap:2.4mm;align-items:center;flex:none"><div class="bubble r" style="width:31mm">Pull it at the peak!</div><div class="chara">{guide()}</div></div>
</div>

<div class="row">
 <div class="cardfig">{card(1, c0[0], list(c0[1]), c0[2], c0[3])}</div>
 <div class="col"><h2 class="h-yellow">Your cards</h2>
  <p>Each card is a cake, and its four edges are the dial. At the start of your turn, give every cake in your oven a <b>quarter-turn clockwise</b>. The edge now on top is the cake's stage:</p>
  <ul><li><b>Batter</b> (top edge): nothing to score yet.</li><li><b>Risen, Golden, Dark</b>: points. The gold badge shows the peak.</li><li>One more turn after Dark and it is <b>cinders</b>: the card goes in the Bin and scores nothing.</li></ul>
  <div class="fam3"><span style="background:#ffe3ec"><b>Pink</b>Quick riser. Peaks at Risen.</span><span style="background:#fff2c9"><b>Yellow</b>Steady baker. Peaks at Golden.</span><span style="background:#e9e2fd"><b>Violet</b>Slow burn. Peaks at Dark.</span></div>
  <p class="m" style="margin-top:1.4mm">The <b>&#9733; Carly&rsquo;s</b> tag marks Carly&rsquo;s own cakes. The rest are classic guests.</p>
 </div>
</div>

<div class="row">
 <div class="col"><h2 class="h-teal">Setup</h2>
  <ol><li>Shuffle the 18 cakes and deal 3 face up.</li><li>Player 2 picks one for their oven, then Player 1 picks one. Put it in a rack with Batter on top. Each baker has <b>two racks</b>.</li><li>The third card starts <b>the Counter</b>. Deal it up to 4 cards. The rest is the deck.</li><li>Player 1 goes first.</li></ol></div>
 <div class="col"><h2 class="h-violet">Days</h2>
  <p>The game lasts two <b>days</b>. A day ends when the deck and the Counter are both empty.</p>
  <p><b>Washing up:</b> shuffle the <b>Sold pile</b> into a new deck. Everything in the Bin leaves the game. Deal a new Counter. Cakes still in the oven stay there. <b>Player 2 starts day 2.</b> When day 2 ends, cakes still baking score nothing.</p></div>
</div>

<div><h2 class="h-pink">Your turn</h2>
<p><b>1. Turn</b> every cake in your oven a quarter-turn clockwise.&nbsp; <b>2. Do one thing.</b>&nbsp; <b>3. Refill</b> the Counter to 4 cards.</p>
<div class="tiles">{th}</div>
<p class="m" style="margin-top:1.6mm">If the Counter is empty you must pull. If you can do nothing, skip your turn.</p></div>

<p style="margin:0"><b>In the box:</b> 18 cake cards (11 of Carly's own, 7 classic guests). For solo play against a rival, add the 6 Rival Baker cards.</p>
{footer(1)}
</div>"""

def page2():
    d = [("Souffle", 0, "0", "", "<b>Baked.</b> Batter on top: nothing to score."), ("Souffle", 1, "9", "gold", "<b>Turn 1: Risen.</b> The peak! Pull it now."),
         ("Souffle", 2, "2", "", "<b>Turn 2: Golden.</b> It has sunk."), ("Souffle", 3, "0", "", "<b>Turn 3: Dark.</b> Too late.")]
    tiles = "".join(f'<div class="dtile">{rot(n, k, .36)}<div class="big {g}">{v}</div><div class="cap">{c}</div></div>' for n, k, v, g, c in d)
    tiles += f'<div class="dtile"><div class="art">{cake_svg("Burnt Cake")}</div><div class="big sad">&#215;</div><div class="cap"><b>Turn 4: cinders!</b> To the Bin. No points.</div></div>'
    return f"""<div class="pg">
{hdr("How the dial works", "Page 2")}
<div><h2 class="h-yellow">The dial in action</h2>
<p>Here is one Soufflé over five turns. Each turn you give it a <b>quarter-turn clockwise</b>, so the next edge comes to the top. The number on top is what it scores if you pull it.</p>
<div class="dialrow">{tiles}</div></div>

<div><h2 class="h-pink">A turn, step by step</h2>
<p>It is the start of your turn. Your oven has two racks, and both are full. Four cards are on the Counter.</p>
<div class="scene">
 <div class="box"><span class="lab2">Your oven (after turning)</span><div class="cards-line">{rot("Souffle", 1, .34)}{rot("Victoria Sponge", 2, .34)}</div>
  <span class="m" style="font-size:2.9mm;text-align:center">Soufflé is Risen (9). Victoria Sponge is Golden (6).</span></div>
 <div class="box" style="flex:1"><span class="lab2">The Counter</span><div class="cards-line">{rot("Cookies", 0, .34)}{rot("Pavlova", 0, .34)}{rot("Carrot Cake", 0, .34)}{rot("Cheesecake", 0, .34)}</div>
  <span class="m" style="font-size:2.9mm;text-align:center">Cookies, Pavlova, Carrot Cake and Cheesecake.</span></div>
</div>
<div class="story" style="margin-top:3mm">
 <div class="sp"><span class="stepno">1</span><div class="cap" style="margin-top:6mm"><b>Turn your cakes.</b><br>The Soufflé turns to Risen and the Sponge to Golden. Both are at a peak, and you can only pull one.</div></div>
 <div class="sp"><span class="stepno">2</span><div class="cap" style="margin-top:6mm"><b>Choose.</b><br>The Soufflé's next number is 2: it would lose 7. The Sponge's next is 5: it would lose 1. <b>Pull the Soufflé: +9.</b></div></div>
 <div class="sp"><span class="stepno">3</span><div class="cap" style="margin-top:6mm"><b>Use the effect.</b><br>Second helping: take another Counter card and use it. Bake the Cookies into the free rack. Then <b>refill</b> the Counter.</div></div>
</div>
</div>

<div class="row" style="align-items:center">
 <div class="chara" style="width:40mm;height:28mm">{guide(6)}</div>
 <div class="bubble l col"><b>Next turn:</b> the Sponge turns to Dark (5) and the Cookies turn to Risen (6). Pull the Sponge for 5, plus <b>1 from its Glaze</b> because one other cake (the Cookies) is in your oven. That is <b>6 points</b>.</div>
</div>

<div class="call" style="margin-top:0"><h3>Why not bake first?</h3>
<p style="margin:0">Because both racks were full, so a Bake was not allowed. When your racks are full, your choices are Pull, Slam or Bin. Pulling the cake that would lose the <b>most</b> by waiting is usually right.</p></div>
{footer(2)}
</div>"""

def page3():
    storyboard = f"""<div class="story">
 <div class="sp"><span class="stepno">1</span>{rot("Souffle", 0, .36)}<div class="cap"><b>Their Soufflé is Batter.</b><br>Its next numbers are 9, then 2.</div></div>
 <div class="sp"><span class="stepno">2</span><span class="burst" style="right:3mm;top:8mm">SLAM!</span>
   <div style="position:relative;width:32mm;height:32mm"><div style="position:absolute;left:7mm;top:6mm;z-index:1;opacity:.95">{rot("Pavlova", 1, .27)}</div><div style="position:absolute;left:0;top:0;z-index:2">{rot("Souffle", 1, .36)}</div></div>
   <div class="cap"><b>You slam it.</b><br>Tuck a Counter card sideways under it. It jumps to Risen at once.</div></div>
 <div class="sp"><span class="stepno">3</span>{rot("Souffle", 2, .36)}<div class="cap"><b>On their turn it turns again.</b><br>Golden: <b>2 points, not 9!</b></div></div>
</div>"""
    return f"""<div class="pg">
{hdr("Slam the door", "Page 3")}
<div><h2 class="h-violet">A slam, in pictures</h2>
<p>A slam makes the cake <b>skip a stage</b>. It turns once when you slam it, and again when its owner starts their turn. Slam when the next number is the peak, and they lose it.</p>
{storyboard}</div>

<div class="call"><h3>Careful: a slam can help them</h3>
<div class="row" style="align-items:center;gap:4mm">
 <div style="flex:none;display:flex;gap:0">{rot("Pavlova", 0, .3)}</div>
 <p style="margin:0"><b>Pavlova</b> reads 2 (Risen), then 5 (Golden). Slam it at Batter and it skips the 2 and goes straight to 5. You have <b>helped</b> your rival! Only slam a cake whose <b>next</b> number is its peak.</p>
</div></div>

<div class="row">
 <div class="col"><h3>What can be slammed?</h3>
  <ul><li><b>Batter or Risen cakes</b> with a basic slam.</li><li><b>Golden and Dark cakes are set.</b> A basic slam can't touch them.</li><li><b>Draught</b> can hit any cake at any stage. A Dark cake that gets Draughted turns to cinders.</li></ul></div>
 <div class="col"><h3>Special cakes</h3><div class="mini"><span class="chip q">Sturdy</span><span>Can't be slammed at all.</span></div><div class="mini"><span class="chip q">Preheated</span><span>Bake it with the Risen edge up. Coffee &amp; Salted Pecan starts warm.</span></div></div>
</div>

<div><h2 class="h-yellow">Card effects, in pictures</h2>
<p style="margin-bottom:2mm">Most cakes have an effect that happens when you <b>pull</b> them. <i>Use a card</i> means: bake it, slam with it, or put it in the Bin.</p>
<div class="efgrid">{effects_grid()}</div></div>

<div class="row">
 <div class="col"><h2 class="h-pink">Winning</h2><p>After day 2, the baker with the <b>most points</b> wins. A tie is a shared win.</p></div>
 <div class="col"><h3 style="margin-top:1mm">Quick answers</h3><ul><li><b>Pull a Batter cake?</b> No. It must be Risen, Golden or Dark.</li><li><b>Throw away my own cake?</b> No. Pull it, or let it burn.</li><li><b>Turn a cake I just baked?</b> Not that turn.</li></ul></div>
</div>
{footer(3)}
</div>"""

def page4():
    c, g = sum(L["shares"]["casual"][2:]) * 100, sum(L["shares"]["good"][2:]) * 100
    use = "".join(f'<div class="sp" style="background:{bg}"><span style="position:absolute;left:2mm;top:2mm;width:6.4mm;height:6.4mm;border-radius:50%;background:#ffd23f;border:.4mm solid #3a2118;font-family:Fredoka;font-weight:700;font-size:4mm;line-height:5.6mm">{n}</span><div style="width:15mm;height:15mm">{ICONS[k]}</div><div class="cap"><b>{t}</b><br>{d}</div></div>'
                   for n, k, t, d, bg in ((1, "pull", "Pull", "a cake that can't get better: next number the same or lower, or Dark.", "#fff3c4"),
                                           (2, "slam", "Slam", "a Batter or Risen cake if it would lose 3 or more.", "#e6defc"),
                                           (3, "bake", "Bake", "the biggest Counter card, if it has a free rack.", "#ffe0ea"),
                                           (4, "bin", "Bin", "the left-most Counter card.", "#d6f3ee")))
    tips = [("Pull at the peak.", "Check the next edge. If it is no bigger than the one showing, pull now."),
            ("Two cakes peaking together?", "You can only pull one. Bake so your peaks take turns."),
            ("A Golden cake is safe from a slam,", "but a Draught can still hit it, and a slow cake keeps a rack busy for longer."),
            ("Spend a slam where it hurts.", "Look for a rising cake whose next number is the biggest.")]
    tp = "".join(f'<div class="row" style="align-items:center;gap:2.4mm"><div class="chara" style="width:21mm;height:14.7mm">{guide(-6 if i % 2 else 6)}</div><div class="bubble l col" style="font-weight:600"><b>{a}</b> {b}</div></div>' for i, (a, b) in enumerate(tips))
    return f"""<div class="pg">
{hdr("Playing alone", "Page 4")}
<div><h2 class="h-teal">Score attack</h2>
<p>One oven with two racks, and a Counter of <b>3</b>. After each turn the oldest Counter card goes cold and leaves the game. No slamming, and ignore Draught. Play two days, add up your points and find your grade. <b>A win is Apprentice or better.</b></p>
<div class="gr">{grade_tiles()}</div>
<p class="m" style="margin-top:1.6mm">In simulation a casual player earns Apprentice or better about {c:.0f} games in 100 and a good player about {g:.0f}. Master Baker is rare.</p></div>

<div><h2 class="h-violet">Rival Baker</h2>
<div class="row" style="align-items:center;margin-bottom:2mm">
 <div style="display:flex;gap:2.4mm;align-items:center;flex:none"><div class="chara" style="width:34mm;height:23.8mm">{rival_svg()}</div><div class="bubble r" style="width:30mm">Beat me if you can!</div></div>
 <p class="col" style="margin:0">Play the two-player game against an automated rival, using the 6 Rival Baker cards. Flip a card on its turn. Casual players beat it about {RV["casual"]["win"]*100:.0f} games in 100, and strong players about {RV["strong"]["win"]*100:.0f}. A tie goes to the Rival.</p>
</div>
<h3>The Rival does the first of these that works</h3>
<div class="story" style="grid-template-columns:repeat(4,1fr);gap:2.4mm">{use}</div></div>

<div><h2 class="h-yellow">Tips for new bakers</h2>
<div class="gr" style="grid-template-columns:1fr 1fr;gap:2.4mm 4mm">{tp}</div></div>
{footer(4)}
</div>"""

def build():
    head = ('<meta charset="utf-8"><title>Carly Cakes rules</title>'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600;700&family=Nunito:ital,wght@0,600;0,700;0,800;1,700&display=swap">'
            f'<style>{CSS}</style>')
    open("rules.html", "w").write(f"<!doctype html><html><head>{head}</head><body>{page1()}{page2()}{page3()}{page4()}</body></html>")
    print("rules.html written")

if __name__ == "__main__":
    build()
