"""Builds hub.html for Crumb Coat from results.json and ladder.json."""
import json, html

R = json.load(open("results.json")); L = json.load(open("ladder.json"))
EFF = {
    "none": ("", ""),
    "tip": ("Tip jar", "+1 point."),
    "glaze": ("Glaze", "+1 point for each other cake in your oven."),
    "twofor": ("Second helping", "Take another Counter card and use it."),
    "draw": ("Chef's pick", "Use the top card of the deck."),
    "fresh": ("Fresh batch", "Bin the whole Counter and deal a new one."),
    "free_slam": ("Draught", "Slam any one of your opponent's cakes, at any stage."),
    "rest": ("Cooling rack", "Your cakes don't turn at the start of your next turn."),
    "scrap": ("Reheat", "Use the most recently discarded card."),
}
QUIRK = {"": "", "sturdy": ("Water bath", "Can't be slammed."), "preheated": ("Preheated", "Bake it with the Risen edge up.")}
NOTE = {"Souffle": "Biggest single number in the deck, gone a turn later.",
        "Croquembouche": "Three turns of waiting for the highest Dark in the deck.",
        "Cupcakes": "Risen and Golden are equal, so it forgives a late pull.",
        "Cheesecake": "Slow and safe.", "Fruitcake": "Slow and safe, and the Glaze pays for a full oven."}

def e(s): return html.escape(s)

rows = ""
for i, c in enumerate(R["cards"], 1):
    n = c["name"].replace("Souffle", "Soufflé")
    d = c["dial"]; pk = max(d)
    bars = "".join(
        f'<span class="b{" pk" if v == pk else ""}"><i style="--v:{v}"></i><b>{v}</b></span>' for v in d)
    en, et = EFF[c["eff"]]
    eff = f"<b>{e(en)}</b> {e(et)}" if en else '<span class="muted">No effect.</span>'
    q = QUIRK[c["quirk"]]
    if q: eff += f'<br><span class="quirk">{e(q[0])}.</span> {e(q[1])}'
    note = NOTE.get(c["name"], "")
    if note: eff += f'<br><span class="muted">{e(note)}</span>'
    rows += (f'<tr><td class="num">{i:02d}</td><th scope="row">{e(n)}</th><td><div class="dial" role="img" '
             f'aria-label="Risen {d[0]}, Golden {d[1]}, Dark {d[2]}">{bars}</div></td>'
             f'<td class="fx">{eff}</td><td class="c">{c["ppb"]:.1f}</td></tr>\n')

names = ["Burnt Offering", "Soggy Bottom", "Apprentice", "Journeyman", "Head Baker", "Master Baker"]
rng = ["36 or less", "37–42", "43–49", "50–56", "57–62", "63+"]
blurb = ["The batch is ruined.", "It rose, then it didn't hold.", "You got it out of the oven.",
         "Competent. You'd get hired.", "You ran the bakery well.", "Near-perfect. Rare."]
ladder_rows = ""
for i, nm in enumerate(names):
    ladder_rows += (f'<tr class="{"win" if i >= 2 else "lose"}"><th scope="row"><span class="sw s{i}"></span>{nm}</th>'
                    f'<td>{rng[i]}</td><td>{"Win" if i >= 2 else "Lose"}</td><td class="muted">{blurb[i]}</td></tr>\n')
who = [("casual", "Casual bot", "Pulls at 5+ or on Dark; bakes the biggest peak."),
       ("good", "Good bot", "Playout search, 2 trials a choice."),
       ("expert", "Expert bot", "Playout search, 10 trials a choice.")]
bars = ""
for k, label, sub in who:
    segs = ""
    for i, sh in enumerate(L["shares"][k]):
        txt = f"{sh*100:.0f}%" if sh >= 0.07 else ""
        segs += f'<span class="seg s{i}" style="flex:{max(sh,0.0001)}" title="{names[i]} {sh*100:.0f}%">{txt}</span>'
    win = sum(L["shares"][k][2:])
    bars += (f'<div class="lrow"><div class="llabel"><b>{label}</b><span class="muted">{sub}</span></div>'
             f'<div class="lbar" role="img" aria-label="{label}: '
             + ", ".join(f"{names[i]} {s*100:.0f}%" for i, s in enumerate(L["shares"][k])) +
             f'">{segs}</div><div class="lwin"><b>{win*100:.0f}%</b><span class="muted">win</span></div></div>\n')

legend = "".join(f'<span><span class="sw s{i}"></span>{n}</span>' for i, n in enumerate(names))

page = open("hub_template.html").read()
page = (page.replace("%%CARDROWS%%", rows).replace("%%LADDER%%", ladder_rows).replace("%%LBARS%%", bars)
        .replace("%%LEGEND%%", legend)
        .replace("%%P1%%", f"{R['p1']*100:.1f}").replace("%%P2%%", f"{R['p2']*100:.1f}").replace("%%TIE%%", f"{R['tie']*100:.1f}")
        .replace("%%MEAN%%", f"{R['mean']:.0f}").replace("%%TURNS%%", f"{R['turns']:.0f}")
        .replace("%%SLAMS%%", f"{R['slams']:.1f}").replace("%%SKILL%%", f"{R['skill']*100:.0f}")
        .replace("%%MARGIN%%", f"{R['median_margin']:.0f}")
        .replace("%%PPBMIN%%", f"{min(c['ppb'] for c in R['cards']):.1f}").replace("%%PPBMAX%%", f"{max(c['ppb'] for c in R['cards']):.1f}"))
import base64
for k, f in (("%%IMG1%%", "sheet1.jpg"), ("%%IMG2%%", "sheet2.jpg"), ("%%IMG3%%", "back.jpg")):
    page = page.replace(k, "data:image/jpeg;base64," + base64.b64encode(open("cards/" + f, "rb").read()).decode())
open("hub.html", "w").write(page)
print("ok", len(page))
