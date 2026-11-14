"""Builds rival.html: the six Rival Baker cards, their backs and a rules panel (A4, two pages)."""
import html, json
from build_cards import CSS, marks
from art_rival import svg

R = json.load(open("../rival_results.json"))
CARDS = [
    ("By the book", "Follows the recipe to the letter.", "Follow the usual list, reading the Counter from the left."),
    ("Newest first", "Always wants the fresh stuff.", "Follow the usual list, reading the Counter from the right."),
    ("Early bird", "Pulls anything that looks ready.", "First, pull the cake showing the biggest number if that number is 5 or more. Then the usual list."),
    ("Door slammer", "Slams first, bakes later.", "Slam first: if one of your Batter or Risen cakes would lose 2 or more, slam it. Then pull, bake, bin."),
    ("Sweet tooth", "Only bakes the slow, rich ones.", "Usual list, but it bakes the card with the biggest Dark number."),
    ("Regular customer", "The tip jar fills up.", "The Rival scores +1 point. Then follow the usual list."),
]
RCSS = CSS + '''
.card.rv { background: #27b5a6 } .rv .dots { background-image: radial-gradient(circle, rgba(255,255,255,.5) 0.45mm, transparent 0.5mm) }
.rv .panel { left: 5mm; top: 5mm; width: 53mm; height: 78mm; gap: 1mm; padding: 1.8mm 2.2mm 1.4mm }
.rv .label { font-family: "Fredoka", sans-serif; font-weight: 600; font-size: 2.3mm; letter-spacing: .35mm; text-align: center; color: #fff; background: #27b5a6; border-radius: 1mm; padding: .3mm 0; border: .3mm solid #3a2118 }
.rv .name { font-size: 5.4mm } .rv .tag { font-size: 2.5mm }
.rv .art { background: #d6f3ee }
.rv .eff { background: #d6f3ee; justify-content: center } .rv .eff .ex { font-size: 2.85mm; line-height: 1.2 }
.rv .eff .et { font-size: 2.5mm; letter-spacing: .3mm; color: #1b8a7e }
.rules { grid-column: 1 / span 3; width: 189mm; height: 88mm; background: #fffdf8; border: .5mm solid #3a2118; border-radius: 4mm; padding: 4mm 5mm; display: grid; grid-template-columns: 1fr 1fr; gap: 0 6mm; font-size: 2.62mm; line-height: 1.28; overflow: hidden; position: relative }
.rules h3 { grid-column: 1 / span 2; font-family: "Fredoka", sans-serif; font-weight: 700; font-size: 4.4mm; line-height: 1; margin-bottom: 1.4mm; color: #1b8a7e }
.rules h4 { font-family: "Fredoka", sans-serif; font-weight: 600; font-size: 3mm; margin: 1.1mm 0 .3mm; text-transform: uppercase; letter-spacing: .2mm }
.rules p { margin-bottom: .6mm } .rules ol { padding-left: 4.2mm } .rules li { margin-bottom: .5mm }
.rules b { font-family: "Fredoka", sans-serif; font-weight: 600 }
.rules .box { background: #d6f3ee; border: .35mm solid #3a2118; border-radius: 2mm; padding: 1.2mm 2mm; margin-top: 1.2mm }
'''

def card(i, name, tag, text):
    return f'''<div class="card rv"><div class="dots"></div><div class="panel">
  <div class="label">RIVAL BAKER</div><div class="name">{html.escape(name)}</div><div class="tag">{html.escape(tag)}</div>
  <div class="art">{svg(name)}</div>
  <div class="eff"><span class="et">WHAT IT DOES</span><span class="ex">{html.escape(text)}</span></div>
  <div class="foot"><span class="fam" style="background:#27b5a6;color:#fff">SUGAR &amp; SPITE</span><span class="no">{i:02d}/06</span></div>
</div></div>'''

BACK = '''<div class="card back" style="background:#27b5a6"><svg viewBox="0 0 63 88" xmlns="http://www.w3.org/2000/svg">
<defs><pattern id="rs" width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="4.5" cy="4.5" r="1.7" fill="#fff" opacity=".4"/></pattern></defs>
<rect width="63" height="88" fill="#27b5a6"/><rect width="63" height="88" fill="url(#rs)"/>
<rect x="5" y="5" width="53" height="78" rx="5" fill="none" stroke="#fff" stroke-width="1.2" stroke-dasharray="1.4 2.2" stroke-linecap="round"/>
<circle cx="31.5" cy="38" r="21" fill="#fff" stroke="#3a2118" stroke-width="1.3"/><circle cx="31.5" cy="38" r="17.5" fill="#d6f3ee"/>
<svg x="12.5" y="19" width="38" height="26.6" viewBox="0 0 120 84">{FACE}</svg>
<text x="31.5" y="68.5" text-anchor="middle" font-family="Fredoka, sans-serif" font-weight="700" font-size="6.2" fill="#fff" stroke="#3a2118" stroke-width="1.9" paint-order="stroke" stroke-linejoin="round" letter-spacing=".2">RIVAL BAKER</text>
<text x="31.5" y="75.6" text-anchor="middle" font-family="Nunito, sans-serif" font-weight="700" font-size="2.5" fill="#fff" letter-spacing=".3">SUGAR &amp; SPITE BAKERY</text>
</svg></div>'''

def panel():
    c, s, e = R["casual"]["win"], R["strong"]["win"], R["expert"]["win"]
    return f'''<div class="rules">
<h3>Play solo against the Rival Baker</h3>
<div>
<h4>Setup</h4>
<p>Play the normal two-player game with the Rival as Player 2. Deal 3 cakes: you pick one, the Rival takes the left-most of the other two, and the third starts the Counter. You go first. Shuffle the six Rival cards and put them face down.</p>
<h4>The Rival's turn</h4>
<ol><li>Turn its cakes, as you would your own.</li><li>Flip the top Rival card. When they run out, shuffle all six again.</li><li>Do what the card says.</li><li>Refill the Counter.</li></ol>
<div class="box"><b>Winning.</b> Most points wins and a tie goes to the Rival. Casual players win about {c*100:.0f} games in 100, strong players about {s*100:.0f}, in simulation.</div>
</div>
<div>
<h4>The usual list: do the first that works</h4>
<ol><li><b>Pull</b> a cake that can't get better: its next number is the same or lower, or it is Dark. Biggest number first.</li>
<li><b>Slam</b> one of your Batter or Risen cakes if skipping a stage would cost it 3 or more (not a Water bath). Use the Counter card with the smallest biggest-number.</li>
<li><b>Bake</b> if it has an empty rack: the Counter card with the biggest number on it.</li>
<li><b>Bin</b> the left-most Counter card.</li></ol>
<p>If the Counter is empty it pulls its best cake, or skips. Ties go to the left-most card.</p>
<h4>Effects</h4>
<p>It scores <b>Tip jar</b> and <b>Glaze</b>, plays <b>Draught</b> on your cake that would lose most, and plays <b>Chef's pick</b> and <b>Reheat</b> (bakes the card if it has a free rack, otherwise bins it). It ignores every other effect.</p>
</div>
</div>'''

def build():
    cards = "".join(card(i + 1, *c) for i, c in enumerate(CARDS))
    from art_rival import by_the_book
    back = BACK.replace("{FACE}", by_the_book())
    def sheet(inner, nl, nr):
        return f'<div class="sheet"><div class="grid">{inner}</div>{marks()}<div class="note"><span>{nl}</span><span>{nr}</span></div></div>'
    p1 = sheet(cards + panel(), "Carly Cakes &middot; Rival Baker &middot; fronts", "Print at 100% on A4, double-sided, flip on the long edge. Cut the six cards and the rules panel on the marks.")
    p2 = sheet(back * 6, "Carly Cakes &middot; Rival Baker &middot; backs", "Back of the sheet before. The bottom row stays blank.")
    head = ('<meta charset="utf-8"><title>Carly Cakes Rival Baker</title>'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600;700&family=Nunito:ital,wght@0,600;0,700;1,700&display=swap">'
            f'<style>{RCSS}</style>')
    open("rival.html", "w").write(f"<!doctype html><html><head>{head}</head><body>{p1}{p2}</body></html>")
    print("rival.html written")

if __name__ == "__main__":
    build()
