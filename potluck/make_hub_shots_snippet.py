# Snippet for source/make_hub.py: the "shots" section (shot types on the reds).
# Written without sight of make_hub.py, so the wiring in step 2 is a guess:
# adapt it to however the script assembles its sections.
#
# 1. Paste SHOTS_HTML (and shots_section) near the other section builders.
# 2. Emit it between the "cards"/"numbers"/"history" sections and the "open" section,
#    e.g. wherever the script concatenates sections, add shots_section() before
#    the block that writes <section id="open">.
# The HTML uses only classes already in the page's stylesheet (.board, .legend,
# .num, .val, .fx, .plain), so no CSS changes are needed.
#
# It is static text with no braces or % signs needing escaping, so it is safe in
# f-strings only if you do not interpolate it: insert it as a plain string.

SHOTS_HTML = """<section id="shots">
  <h2>Proposal: shot types on the reds</h2>
  <p>Not in draft 0.1, not in the print files, not simulated or table-tested. The twelve reds are near-identical (a cut of 3 or 4 and a pair of ends), and the sim says most shots are forced. This gives half of them an identity with its own risk and reward, so that the card changes the decision rather than just the label. Cuts and ends are unchanged from draft 0.1 except that the two trick shots print a cut of 5.</p>
  <p class="legend"><b>P</b> is the number at the top of the leave. <b>T</b> is the number at the top of the card you turn from the pack. "As normal" means the existing rules for going for it, a miss and laying the leave.</p>
  <div class="board"><table>
    <thead><tr><th>#</th><th>Card</th><th>Type</th><th>Cut</th><th>Ends</th><th>Rule printed on the card</th></tr></thead>
    <tbody>
<tr><td class="num">01</td><th scope="row">Over the pocket</th><td>Plain</td><td class="val">3</td><td class="val">1 · 3</td><td class="fx">None.</td></tr>
<tr><td class="num">02</td><th scope="row">Hanging in the middle</th><td>Plain</td><td class="val">3</td><td class="val">2 · 3</td><td class="fx">None.</td></tr>
<tr><td class="num">03</td><th scope="row">A loose red</th><td>Plain</td><td class="val">3</td><td class="val">1 · 4</td><td class="fx">None.</td></tr>
<tr><td class="num">04</td><th scope="row">Sitting nicely</th><td>Plain</td><td class="val">3</td><td class="val">3 · 4</td><td class="fx">None.</td></tr>
<tr><td class="num">05</td><th scope="row">In the open</th><td>Plain</td><td class="val">3</td><td class="val">1 · 3</td><td class="fx">None.</td></tr>
<tr><td class="num">06</td><th scope="row">The showman's red</th><td><b>Exhibition</b></td><td class="val">3</td><td class="val">2 · 4</td><td class="fx">Pot it as normal. It scores 1, plus 1 for each ball already potted this visit, up to +3.</td></tr>
<tr><td class="num">07</td><th scope="row">Long into the corner, called</th><td><b>Trick shot</b></td><td class="val">5</td><td class="val">3 · 4</td><td class="fx">Call it first. It is never free: turn a card, and it is in if P + T is more than 5. Pot: score 3. Miss: your opponent scores 2, and the turned card is the leave as normal.</td></tr>
<tr><td class="num">08</td><th scope="row">Frozen to the top cushion</th><td><b>Safety</b></td><td class="val">4</td><td class="val">1 · 4</td><td class="fx">Either pot it as a plain cut-4 red, or play safe with it: do not turn a card, lay this card as the leave with the 1 up, and put the old leave back with the loose reds. Score nothing; your visit ends.</td></tr>
<tr><td class="num">09</td><th scope="row">Off the side cushion</th><td><b>Fluke</b></td><td class="val">4</td><td class="val">2 · 3</td><td class="fx">Ignore your position. Turn a card. If T is 1 or 2 it drops and the turned red follows it into the pocket: score 2, and lay the fluke as the leave as normal. If T is 3 or 4, a miss as normal. After a double you still take one colour.</td></tr>
<tr><td class="num">10</td><th scope="row">A thin cut, called</th><td><b>Trick shot</b></td><td class="val">5</td><td class="val">2 · 4</td><td class="fx">Same as 07.</td></tr>
<tr><td class="num">11</td><th scope="row">Tight under the black</th><td><b>Fluke</b></td><td class="val">4</td><td class="val">1 · 4</td><td class="fx">Same as 09.</td></tr>
<tr><td class="num">12</td><th scope="row">On the cushion</th><td>Plain</td><td class="val">4</td><td class="val">2 · 4</td><td class="fx">None.</td></tr>
    </tbody>
  </table></div>
  <p class="legend">Six plain, two trick shots, two flukes, one safety, one exhibition. Colours unchanged.</p>
  <h3>Odds, worked by hand</h3>
  <p>On the full twelve reds the ends are 1 five times, 2 five times, 3 six times and 4 eight times, so T is 1 or 2 about 42% of the time. These ignore the pack thinning as a frame goes on.</p>
  <ul class="plain">
    <li><b>Fluke:</b> drops 42% of the time from any position, for 2 points. It is worth taking mainly when you are stuck on a 1 or 2.</li>
    <li><b>Trick shot:</b> at P = 4 it lands about 79% (EV about +1.96, against 1 for a free plain red); at P = 3, 58% (EV about +0.9); at P = 2, 33% (EV about −0.3); at P = 1 it cannot be potted. A card for when you are already high.</li>
    <li><b>Safety:</b> your opponent starts on a 1. They need T of 3 or more for a cut 3 (58%), or a T of 4 for a cut 4 (33%).</li>
  </ul>
  <h3>Weak points and test order</h3>
  <ul class="plain">
    <li>Nothing here is simulated. First knobs to tune: the trick bonus (+2), the trick miss penalty (2), the fluke range (T of 1 or 2).</li>
    <li>The safety is probably the strongest card, since it forces a 1 every time. If it dominates, let the opponent choose the way up, or make it one-shot.</li>
    <li>The exhibition bonus rewards the player already on a break and can snowball; the cap of +3 is there to limit that.</li>
    <li>The fluke's double pockets a pack red, which thins the reds, shortens the frame and adds a third place for a card to go when clearing the leave.</li>
    <li>Test in stages: the safety and the trick shot first (they change decisions and need no new clearing rules), then the exhibition (needs a per-visit pot count), then the fluke.</li>
    <li>These are still snooker terms. If the game should feel less like a copy of snooker, the colours are where to push next.</li>
  </ul>
</section>"""


def shots_section():
    return SHOTS_HTML
