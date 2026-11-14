"""Builds rules.html: the Carly Cakes rules sheet, two A4 pages, cartoon style."""
import sys
sys.path.insert(0, "..")
from sim import CAKES
from build_cards import card, CSS as CARD_CSS
from art import svg as cake_svg
import json

L = json.load(open("../ladder.json")); RV = json.load(open("../rival_results.json"))

CSS = CARD_CSS + '''
html, body { background: #fff }
.pg { width: 210mm; height: 297mm; position: relative; overflow: hidden; page-break-after: always; break-after: page; padding: 10mm 12mm 9mm; background: #fffdf8; display: flex; flex-direction: column; gap: 4.2mm; font-size: 3.15mm; line-height: 1.3 }
.banner { height: 31mm; border-radius: 5mm; background: #ff6f98; border: .5mm solid #3a2118; position: relative; overflow: hidden; display: flex; align-items: center; padding: 0 7mm; gap: 6mm; flex: none }
.banner::before { content: ""; position: absolute; inset: 0; background-image: radial-gradient(circle, rgba(255,255,255,.5) .5mm, transparent .55mm); background-size: 4.6mm 4.6mm }
.banner h1 { position: relative; font-family: "Fredoka", sans-serif; font-weight: 700; font-size: 13.5mm; line-height: .95; color: #fff; -webkit-text-stroke: 1.6mm #3a2118; paint-order: stroke fill; letter-spacing: .2mm }
.banner .sub { position: relative; display: flex; gap: 1.6mm; flex-wrap: wrap; margin-top: 2.2mm }
.chip { font-family: "Fredoka", sans-serif; font-weight: 600; font-size: 2.9mm; background: #fffdf8; border: .4mm solid #3a2118; border-radius: 3mm; padding: .6mm 2.4mm; white-space: nowrap }
.banner .cake { position: absolute; right: 4mm; top: 2mm; width: 50mm; height: 35mm }
.banner .cake svg { width: 100%; height: 100% }
h2 { font-family: "Fredoka", sans-serif; font-weight: 700; font-size: 5mm; line-height: 1; text-transform: uppercase; letter-spacing: .25mm; display: inline-block; padding: 1.1mm 3.4mm; border-radius: 2.6mm; border: .45mm solid #3a2118; color: #3a2118; margin-bottom: 2mm }
.h-pink { background: #ffb3c9 } .h-yellow { background: #ffd966 } .h-violet { background: #c6b8f8 } .h-teal { background: #8fe0d4 }
h3 { font-family: "Fredoka", sans-serif; font-weight: 600; font-size: 3.5mm; margin-bottom: .6mm }
p { margin-bottom: 1.2mm } b { font-weight: 800 } .m { color: #7b665a }
ol, ul { padding-left: 4.6mm } li { margin-bottom: .8mm }
.row { display: flex; gap: 6mm } .col { flex: 1; min-width: 0 }
.cardfig { width: 46mm; height: 64mm; flex: none; position: relative } .cardfig .card { transform: scale(.73); transform-origin: top left; position: absolute; left: 0; top: 0; border-radius: 3mm; border: .45mm solid #3a2118 }
.tiles { display: grid; grid-template-columns: repeat(4, 1fr); gap: 2.6mm }
.tile { border: .45mm solid #3a2118; border-radius: 3mm; padding: 2mm 2.4mm; display: flex; flex-direction: column; gap: .8mm; background: #fff }
.tile .t { font-family: "Fredoka", sans-serif; font-weight: 700; font-size: 4.3mm; line-height: 1 }
.tile.pull { background: #fff3c4 } .tile.bake { background: #ffe0ea } .tile.slam { background: #e6defc } .tile.bin { background: #d6f3ee }
.callout { border: .5mm dashed #3a2118; border-radius: 4mm; padding: 3mm 4mm; background: #fff1f5 }
.steps3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 2.4mm; margin-top: 1.4mm }
.steps3 div { background: #fff; border: .4mm solid #3a2118; border-radius: 2.4mm; padding: 1.4mm 2mm; font-size: 2.95mm }
.steps3 b { font-family: "Fredoka", sans-serif; font-weight: 700 }
.mini { display: flex; align-items: center; gap: 1.6mm; margin-bottom: 1.2mm }
.chip.e { background: #ffe9a8 } .chip.q { background: #3a2118; color: #fff }
.efx { display: grid; grid-template-columns: 31mm 1fr; gap: 1.1mm 2.6mm; align-items: center }
.efx .chip { text-align: center; font-size: 2.9mm; padding: .5mm 1.2mm }
.fam3 { display: flex; gap: 2mm; margin-top: 1.4mm } .fam3 span { flex: 1; text-align: center; border: .4mm solid #3a2118; border-radius: 2.4mm; padding: 1mm 1.4mm; font-size: 2.9mm; line-height: 1.2 }
.fam3 b { display: block; font-family: "Fredoka", sans-serif; font-size: 3.2mm }
table.lad { border-collapse: separate; border-spacing: 0 1.2mm; width: 100% }
table.lad td { padding: 1.2mm 2.6mm; font-size: 3.1mm; border-top: .4mm solid #3a2118; border-bottom: .4mm solid #3a2118 }
table.lad td:first-child { border-left: .4mm solid #3a2118; border-radius: 3mm 0 0 3mm; font-family: "Fredoka", sans-serif; font-weight: 700; font-size: 3.7mm }
table.lad td:last-child { border-right: .4mm solid #3a2118; border-radius: 0 3mm 3mm 0 }
.lw td:nth-child(3) { font-weight: 800 }
.foot2 { margin-top: auto; display: flex; justify-content: space-between; font-size: 2.6mm; color: #7b665a }
'''

def effects():
    E = [("Tip jar", "+1 point."), ("Glaze", "+1 point for each other cake in your oven."), ("Second helping", "Take another Counter card and use it."),
         ("Chef's pick", "Use the top card of the deck."), ("Fresh batch", "Bin the whole Counter and deal a new one."),
         ("Draught", "Slam any one of your opponent's cakes, at any stage."), ("Cooling rack", "Your cakes don't turn at the start of your next turn."),
         ("Reheat", "Use the most recently discarded card.")]
    return "".join(f'<span class="chip e">{a}</span><span>{b}</span>' for a, b in E)

def ladder():
    rows = [("Burnt Offering", "36 or less", "Lose", "#c98b6b", "The batch is ruined."), ("Soggy Bottom", "37–42", "Lose", "#e3b08f", "It rose, then it didn't hold."),
            ("Apprentice", "43–49", "Win", "#ffe08a", "You got it out of the oven."), ("Journeyman", "50–56", "Win", "#ffb25e", "Competent. You'd get hired."),
            ("Head Baker", "57–62", "Win", "#ff7aa2", "You ran the bakery well."), ("Master Baker", "63+", "Win", "#b99bf0", "Near-perfect. Rare.")]
    return "".join(f'<tr class="{"lw" if w == "Win" else ""}"><td style="background:{c}">{n}</td><td>{r}</td><td>{w}</td><td>{m}</td></tr>' for n, r, w, c, m in rows)

def build():
    sou = card(1, *CAKES[0][:1], list(CAKES[0][1]), CAKES[0][2], CAKES[0][3])
    p1 = f'''<div class="pg">
<div class="banner"><div><h1>Carly Cakes</h1><div class="sub"><span class="chip">1&ndash;2 bakers</span><span class="chip">25 minutes</span><span class="chip">18 cards</span><span class="chip">ages 10+</span></div></div>
<div class="cake">{cake_svg("Victoria Sponge")}</div></div>

<div><h2 class="h-pink">The idea</h2>
<p>You run a one-oven bakery. Every card is a cake with a <b>dial</b>: you turn it every turn, it rises, peaks and then burns. <b>Pull</b> each cake when it is worth the most. Or <b>slam the oven door</b> on a rival's rising cake and wreck their timing. Most points wins, and you can also play it alone.</p></div>

<div class="row">
 <div class="cardfig">{sou}</div>
 <div class="col"><h2 class="h-yellow">Your cards</h2>
  <p>Each card is a cake, and its four edges are the dial. At the start of your turn, give every cake in your oven a <b>quarter-turn clockwise</b>. The edge now on top is the cake's stage:</p>
  <ul><li><b>Batter</b> (top edge): nothing to score yet.</li><li><b>Risen, Golden, Dark</b>: points. The gold badge shows the peak.</li><li>One more turn after Dark and it is <b>cinders</b>: the card goes in the Bin and scores nothing.</li></ul>
  <div class="fam3"><span style="background:#ffe3ec"><b>Pink</b>Quick riser. Peaks at Risen.</span><span style="background:#fff2c9"><b>Yellow</b>Steady baker. Peaks at Golden.</span><span style="background:#e9e2fd"><b>Violet</b>Slow burn. Peaks at Dark.</span></div>
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
<div class="tiles">
 <div class="tile pull"><span class="t">Pull</span><span>Take a cake that is Risen, Golden or Dark. Score the number on its top edge, do its effect, then put it on the Sold pile.</span></div>
 <div class="tile bake"><span class="t">Bake</span><span>Take a Counter card into an empty rack, Batter edge up.</span></div>
 <div class="tile slam"><span class="t">Slam</span><span>Tuck a Counter card sideways under an opposing cake that is Batter or Risen. Turn that cake a quarter-turn at once. The card goes in the Bin.</span></div>
 <div class="tile bin"><span class="t">Bin</span><span>Take a Counter card and put it in the Bin, so your rival can't have it.</span></div>
</div>
<p class="m" style="margin-top:1.6mm">If the Counter is empty you must pull. If you can do nothing, skip your turn.</p></div>

<div class="callout"><h3>Slam the door: how it works</h3>
<p>A slam makes the cake <b>skip a stage</b>. It turns once when you slam it, and again when its owner starts their turn. Slam when the next number is the peak, and they lose it.</p>
<div class="steps3"><div><b>Their Soufflé is Batter.</b> Its next numbers are 9 (Risen), then 2 (Golden).</div><div><b>You slam it.</b> It jumps to Risen at once. Then on their turn it turns on to Golden.</div><div><b>They score 2, not 9.</b> But slam a cake whose next number is small and the one after is big, and you help them!</div></div>
<p class="m" style="margin-top:1.4mm">Only Batter or Risen cakes can be slammed: once a cake is Golden or Dark it has set.</p></div>
</div>'''

    p2 = f'''<div class="pg">
<div><h2 class="h-yellow">Card effects</h2>
<p>Most cakes have an effect that happens when you <b>pull</b> them. <i>Use a card</i> means: bake it, slam with it, or put it in the Bin.</p>
<div class="efx">{effects()}</div>
<div class="mini" style="margin-top:2.4mm"><span class="chip q">Water bath</span><span>Can't be slammed (Cheesecake, Fruitcake).</span></div>
<div class="mini"><span class="chip q">Preheated</span><span>Bake it with the Risen edge up (Coffee &amp; Salted Pecan).</span></div></div>

<div class="row">
 <div class="col"><h2 class="h-pink">Winning</h2>
  <p>After day 2, the baker with the <b>most points</b> wins. A tie is a shared win.</p>
  <h3>Quick answers</h3>
  <ul><li><b>Can I pull a Batter cake?</b> No. It must be Risen, Golden or Dark.</li><li><b>Can I throw away a cake of my own?</b> No. Pull it, or let it burn.</li><li><b>What happens to a Dark cake that gets Draughted?</b> It turns to cinders.</li><li><b>Do I turn a cake I just baked?</b> Not on that turn. It starts turning on your next one.</li></ul></div>
 <div class="col"><h2 class="h-violet">Playing alone</h2>
  <p>There are two ways to play solo.</p>
  <p><b>Score attack.</b> One oven with two racks, and a Counter of <b>3</b>. After each turn the oldest Counter card goes cold and leaves the game. No slamming, and ignore Draught. Play two days and grade yourself below.</p>
  <p><b>Rival Baker.</b> Play the two-player game against an automated rival, using the Rival Baker deck. Its rules are on the deck sheet. Casual players beat it about {RV["casual"]["win"]*100:.0f} games in 100, and strong players about {RV["strong"]["win"]*100:.0f}.</p></div>
</div>

<div><h2 class="h-teal">Score attack grades</h2>
<table class="lad"><tbody>{ladder()}</tbody></table>
<p class="m">A win is Apprentice or better. In simulation a casual player earns Apprentice or better about {sum(L["shares"]["casual"][2:])*100:.0f} games in 100 and a good player about {sum(L["shares"]["good"][2:])*100:.0f}. Master Baker is rare.</p></div>

<div><h2 class="h-yellow">Tips for new bakers</h2>
<ul><li><b>Pull at the peak.</b> Check the next edge: if it is no bigger than the one showing, pull now.</li>
<li><b>Two cakes peaking together?</b> You can only pull one. Bake so your peaks take turns.</li>
<li><b>A Golden cake is safe from a slam</b>, but a Draught can still hit it, and a slow cake keeps a rack busy for longer.</li>
<li><b>Spend a slam where it hurts.</b> Look for a rising cake whose next number is the biggest.</li></ul></div>

<div class="foot2"><span>Carly Cakes &middot; rules, draft 0.1</span><span>A cake game made for Carly Cakes</span></div>
</div>'''
    head = ('<meta charset="utf-8"><title>Carly Cakes rules</title>'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600;700&family=Nunito:ital,wght@0,600;0,700;0,800;1,700&display=swap">'
            f'<style>{CSS}</style>')
    open("rules.html", "w").write(f"<!doctype html><html><head>{head}</head><body>{p1}{p2}</body></html>")
    print("rules.html written")

if __name__ == "__main__":
    build()
