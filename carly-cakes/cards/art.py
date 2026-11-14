"""Cartoon art for the 18 cakes. Each function returns SVG for a 120 x 84 viewBox.
Flat bright colours, thick chocolate outline, a face on every cake."""

OUT = "#3a2118"
def S(w=2.4, extra=""):
    return f'stroke="{OUT}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round" {extra}'

def face(cx, cy, k=1.0, mouth="smile"):
    e = []
    for dx in (-6.2 * k, 6.2 * k):
        e.append(f'<ellipse cx="{cx+dx:.1f}" cy="{cy:.1f}" rx="{2.3*k:.1f}" ry="{3.0*k:.1f}" fill="{OUT}"/>')
        e.append(f'<circle cx="{cx+dx-.8*k:.1f}" cy="{cy-1.1*k:.1f}" r="{.9*k:.1f}" fill="#fff"/>')
    for dx in (-10.6 * k, 10.6 * k):
        e.append(f'<ellipse cx="{cx+dx:.1f}" cy="{cy+4.2*k:.1f}" rx="{3.3*k:.1f}" ry="{2*k:.1f}" fill="#ff7f9d" opacity=".75"/>')
    if mouth == "o":
        e.append(f'<ellipse cx="{cx:.1f}" cy="{cy+6.2*k:.1f}" rx="{2.2*k:.1f}" ry="{2.8*k:.1f}" fill="{OUT}"/>')
    elif mouth == "grin":
        e.append(f'<path d="M{cx-4.5*k:.1f} {cy+3.4*k:.1f} Q{cx:.1f} {cy+10*k:.1f} {cx+4.5*k:.1f} {cy+3.4*k:.1f} Z" fill="{OUT}" {S(1.4*k)}/>'
                 f'<path d="M{cx-2.2*k:.1f} {cy+6.8*k:.1f} Q{cx:.1f} {cy+5.2*k:.1f} {cx+2.2*k:.1f} {cy+6.8*k:.1f} Q{cx:.1f} {cy+8.8*k:.1f} {cx-2.2*k:.1f} {cy+6.8*k:.1f}Z" fill="#ff6b81"/>')
    else:
        e.append(f'<path d="M{cx-3.6*k:.1f} {cy+3.6*k:.1f} Q{cx:.1f} {cy+8.2*k:.1f} {cx+3.6*k:.1f} {cy+3.6*k:.1f}" fill="none" {S(1.8*k)}/>')
    return "".join(e)

def sparkle(x, y, r=4, c="#fff"):
    return (f'<path d="M{x} {y-r} Q{x} {y} {x+r} {y} Q{x} {y} {x} {y+r} Q{x} {y} {x-r} {y} Q{x} {y} {x} {y-r}Z" fill="{c}" {S(1.2)}/>')

def shadow(cx=60, cy=79, rx=40):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="4" fill="{OUT}" opacity=".16"/>'

def plate(cx=60, cy=74, rx=48, c="#ffffff"):
    return (f'<ellipse cx="{cx}" cy="{cy+2}" rx="{rx}" ry="8" fill="{c}" {S()}/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{rx-8}" ry="5" fill="#e8f0f5" opacity=".9"/>')

def cherry(x, y, r=5):
    return (f'<path d="M{x} {y-r+1} Q{x+3} {y-r-8} {x+8} {y-r-10}" fill="none" {S(1.8)}/>'
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="#e0243f" {S(2)}/><circle cx="{x-1.8}" cy="{y-1.8}" r="1.3" fill="#fff" opacity=".85"/>')

def strawberry(x, y, r=6):
    seeds = "".join(f'<ellipse cx="{x+dx}" cy="{y+dy}" rx=".8" ry="1.3" fill="#ffe27a"/>' for dx, dy in ((-2.5, -1), (2.5, -1), (0, 1.6), (-2.2, 3), (2.2, 3)))
    return (f'<path d="M{x-r} {y-r*.6} Q{x} {y-r*1.1} {x+r} {y-r*.6} Q{x+r*.9} {y+r*1.2} {x} {y+r*1.5} Q{x-r*.9} {y+r*1.2} {x-r} {y-r*.6}Z" fill="#ff4a5e" {S(2)}/>'
            f'{seeds}<path d="M{x-4} {y-r*.7} L{x-1.5} {y-r*1.5} L{x} {y-r*.8} L{x+1.5} {y-r*1.5} L{x+4} {y-r*.7}Z" fill="#59b84a" {S(1.4)}/>')

def drip(x0, x1, y, depth, color, n=5, w=2.0):
    """A wavy icing edge from x0..x1 at height y with n drips."""
    step = (x1 - x0) / n; p = f"M{x0} {y}"
    for i in range(n):
        a = x0 + i * step; d = depth * (0.55 + 0.45 * ((i * 37) % 7) / 6)
        p += f" Q{a+step*.25:.1f} {y+d*1.15:.1f} {a+step*.5:.1f} {y+d*.55:.1f} Q{a+step*.75:.1f} {y+d*1.25:.1f} {a+step:.1f} {y}"
    return p

# ---------------------------------------------------------------- the cakes
def souffle():
    steam = "".join(f'<path d="M{x} 10 q-4 -4 0 -8 q4 -4 0 -7" fill="none" stroke="{OUT}" stroke-width="1.8" stroke-linecap="round" opacity=".4"/>' for x in (46, 60, 74))
    flutes = "".join(f'<path d="M{x} 58 L{x2} 78" stroke="{OUT}" stroke-width="1.7" opacity=".4" stroke-linecap="round"/>' for x, x2 in ((42, 43), (50, 50.5), (58, 58.5), (66, 66), (74, 73.5), (80, 79)))
    return (shadow() + steam +
        f'<path d="M26 52 C6 26 34 4 60 9 C86 4 114 26 94 52 Z" fill="#f7b84b" {S()}/>'
        f'<path d="M30 32 C34 21 46 15 57 16" fill="none" stroke="#fff3c4" stroke-width="3.8" stroke-linecap="round"/>'
        f'<path d="M64 12 C68 19 78 19 84 15" fill="none" stroke="#e08a1e" stroke-width="2" stroke-linecap="round"/>'
        f'<path d="M36 55 L84 55 L80 77 Q60 83 40 77 Z" fill="#d6ecff" {S()}/>' + flutes +
        f'<rect x="30" y="49" width="60" height="9" rx="4.5" fill="#ffffff" {S()}/>'
        f'<path d="M36 53.5 L84 53.5" stroke="#9fd0f5" stroke-width="2" stroke-linecap="round"/>'
        + face(60, 33, 1.05, "o") + sparkle(106, 14, 5, "#fff3c4") + sparkle(14, 20, 3.5, "#fff3c4"))

def macaron(cx, cy, w, shell, cream, tilt=0):
    h = w * .34
    return (f'<g transform="rotate({tilt} {cx} {cy})">'
        f'<path d="M{cx-w/2} {cy+h*.35} Q{cx-w/2} {cy+h*1.05} {cx} {cy+h*1.05} Q{cx+w/2} {cy+h*1.05} {cx+w/2} {cy+h*.35}Z" fill="{shell}" {S()}/>'
        f'<rect x="{cx-w/2+1.5}" y="{cy-h*.05}" width="{w-3}" height="{h*.42}" rx="{h*.2}" fill="{cream}" {S(2)}/>'
        f'<path d="M{cx-w/2} {cy-h*.05} Q{cx-w/2} {cy-h*1.0} {cx} {cy-h*1.0} Q{cx+w/2} {cy-h*1.0} {cx+w/2} {cy-h*.05}Z" fill="{shell}" {S()}/>'
        f'<path d="M{cx-w*.3} {cy-h*.55} Q{cx-w*.15} {cy-h*.85} {cx+w*.05} {cy-h*.8}" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" opacity=".7"/></g>')

def macarons():
    return (shadow() + macaron(36, 62, 36, "#7ed6a6", "#fff7d6", -8) + macaron(84, 62, 36, "#b99bf0", "#fff7d6", 9)
        + macaron(60, 46, 46, "#ff8fb3", "#fff7d6", 0) + face(60, 40, 1.0)
        + sparkle(14, 30, 4) + sparkle(106, 28, 4) + sparkle(96, 10, 3))

def scone(cx, cy, w, h, c, jam=True):
    dots = "".join(f'<circle cx="{cx+dx}" cy="{cy-h*.75+dy}" r=".9" fill="#a8641f"/>' for dx, dy in ((-w*.2, 1), (w*.1, 0), (w*.22, 3), (-w*.05, 3.5)))
    return (f'<path d="M{cx-w/2} {cy} Q{cx-w/2} {cy-h*1.5} {cx} {cy-h*1.5} Q{cx+w/2} {cy-h*1.5} {cx+w/2} {cy} Q{cx} {cy+h*.35} {cx-w/2} {cy}Z" fill="{c}" {S()}/>'
            f'<path d="M{cx-w/2+3} {cy-h*.4} Q{cx} {cy-h*.1} {cx+w/2-3} {cy-h*.4}" fill="none" stroke="#c98a3d" stroke-width="2"/>{dots}')

def scones():
    jam = f'<path d="M40 36 Q40 24 52 26 Q64 24 64 36 Q52 42 40 36Z" fill="#d6243f" {S(2)}/><circle cx="48" cy="31" r="1.7" fill="#fff" opacity=".8"/>'
    cream = f'<path d="M64 38 Q62 28 72 28 Q74 22 82 26 Q92 26 88 36 Q76 42 64 38Z" fill="#fffaf0" {S(2)}/>'
    return (shadow(60, 80, 44) + scone(40, 74, 50, 24, "#f0b96a") + scone(82, 70, 46, 22, "#e9a957") +
        jam + cream + face(40, 58, .95) + sparkle(104, 28, 4) + sparkle(14, 40, 3))

def puff(cx, cy, r, c="#f4c06a", choc=True):
    bumps = "".join(f'<circle cx="{cx+dx*r}" cy="{cy+dy*r}" r="{r*.32}" fill="{c}" {S(1.8)}/>' for dx, dy in ((-.7, .05), (.7, .05), (0, -.75)))
    return (bumps + f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c}" {S()}/>'
        + (f'<path d="M{cx-r*.8} {cy-r*.35} Q{cx-r*.4} {cy+r*.15} {cx} {cy-r*.2} Q{cx+r*.4} {cy+r*.3} {cx+r*.85} {cy-r*.3} Q{cx+r*.55} {cy-r*.95} {cx} {cy-r*.98} Q{cx-r*.55} {cy-r*.95} {cx-r*.8} {cy-r*.35}Z" fill="#6b3a26" {S(1.6)}/>' if choc else ""))

def choux():
    return (shadow() + puff(36, 62, 17) + puff(84, 62, 17) + puff(60, 40, 18) + face(60, 44, .9, "grin")
        + "".join(f'<circle cx="{x}" cy="{y}" r="1.2" fill="#fff"/>' for x, y in ((46, 22), (74, 24), (22, 52), (98, 50), (60, 70)))
        + sparkle(14, 24, 4) + sparkle(106, 22, 4))

def cupcake(cx, cy, c1, c2, sw=True):
    liner = (f'<path d="M{cx-17} {cy-4} L{cx+17} {cy-4} L{cx+12} {cy+20} Q{cx} {cy+24} {cx-12} {cy+20}Z" fill="{c1}" {S()}/>'
             + "".join(f'<path d="M{cx+d} {cy-3} L{cx+d*.74} {cy+21}" stroke="{OUT}" stroke-width="1.5" opacity=".4"/>' for d in (-10, -3.5, 3.5, 10)))
    top = (f'<ellipse cx="{cx}" cy="{cy-5}" rx="20" ry="7" fill="#e3a65a" {S()}/>'
           f'<path d="M{cx-17} {cy-6} Q{cx-19} {cy-17} {cx-7} {cy-17} Q{cx-5} {cy-26} {cx+5} {cy-24} Q{cx+14} {cy-24} {cx+12} {cy-16} Q{cx+20} {cy-14} {cx+17} {cy-6} Q{cx} {cy} {cx-17} {cy-6}Z" fill="{c2}" {S()}/>'
           f'<path d="M{cx-9} {cy-16} Q{cx} {cy-21} {cx+7} {cy-18}" fill="none" stroke="#fff" stroke-width="2" opacity=".7" stroke-linecap="round"/>')
    return liner + top

def cupcakes():
    spr = "".join(f'<rect x="{x}" y="{y}" width="3.4" height="1.7" rx=".8" fill="{c}" transform="rotate({r} {x} {y})"/>' for x, y, c, r in ((34, 42, "#ffd23f", 20), (44, 45, "#4fc3f7", -30), (92, 40, "#fff", 40), (80, 44, "#ffd23f", 10), (66, 40, "#6ee7a0", -20)))
    return (shadow() + cupcake(36, 54, "#ff9bb8", "#fff0f5") + cupcake(84, 52, "#6fd1c2", "#ffe4a3") + spr
        + cherry(36, 26, 4.6) + cherry(84, 24, 4.6) + face(36, 62, .95) + sparkle(60, 20, 4) + sparkle(8, 34, 3) + sparkle(112, 40, 3))

def genoise():
    return (shadow() + plate(60, 70, 50) +
        f'<path d="M20 38 L20 62 Q60 76 100 62 L100 38Z" fill="#f4c565" {S()}/>'
        f'<path d="M20 49 Q60 63 100 49 L100 53 Q60 67 20 53Z" fill="#fffaf0" {S(2)}/>'
        f'<ellipse cx="60" cy="38" rx="40" ry="13" fill="#f9d98a" {S()}/><ellipse cx="60" cy="38" rx="31" ry="8.5" fill="#fff7dd" opacity=".9"/>'
        + strawberry(42, 36, 6.5) + strawberry(78, 36, 6.5) + strawberry(60, 31, 6.5)
        + "".join(f'<circle cx="{x}" cy="{y}" r="1.1" fill="#fff"/>' for x, y in ((50, 42), (68, 42), (60, 40), (36, 40), (86, 40)))
        + face(60, 55, 1.0) + sparkle(100, 20, 4) + sparkle(18, 22, 3))

def lemon_drizzle():
    slice_ = (f'<circle cx="34" cy="24" r="12" fill="#ffe65a" {S()}/><circle cx="34" cy="24" r="8.3" fill="#fff9c2" {S(1.4)}/>'
              + "".join(f'<path d="M34 24 L{34+8.3*__import__("math").cos(a):.1f} {24+8.3*__import__("math").sin(a):.1f}" stroke="{OUT}" stroke-width="1.2"/>' for a in (0, 1.05, 2.1, 3.14, 4.19, 5.24)))
    return (shadow() +
        f'<path d="M14 36 Q14 28 24 28 L96 28 Q106 28 106 36 L102 70 Q60 80 18 70Z" fill="#f6cf5e" {S()}/>'
        f'<path d="{drip(12, 108, 29, 16, "#fff")} L108 24 Q60 18 12 24Z" fill="#ffffff" {S(2.2)}/>'
        + slice_ + f'<path d="M56 18 q4 -8 10 -2 M72 20 q6 -8 11 -1" fill="none" stroke="#9bd24a" stroke-width="2.6" stroke-linecap="round"/>'
        + face(60, 54, 1.05, "grin") + sparkle(96, 14, 4) + sparkle(10, 60, 3))

def layer_cake(cx, top, w, h, bands, topc, creamc="#fffaf0"):
    """Cylinder layer cake. bands = list of colours for sponge layers separated by cream."""
    n = len(bands); lh = h / n; out = []
    rx = w / 2; ry = w * .16
    y = top + ry
    for i, c in enumerate(bands):
        y0 = y + i * lh
        out.append(f'<path d="M{cx-rx} {y0} L{cx-rx} {y0+lh} Q{cx} {y0+lh+ry*2} {cx+rx} {y0+lh} L{cx+rx} {y0}Z" fill="{c}" {S()}/>')
        if i:
            out.append(f'<path d="M{cx-rx} {y0-1.5} Q{cx} {y0+ry*2-1.5} {cx+rx} {y0-1.5} L{cx+rx} {y0+1.8} Q{cx} {y0+ry*2+1.8} {cx-rx} {y0+1.8}Z" fill="{creamc}" {S(1.6)}/>')
    out.append(f'<ellipse cx="{cx}" cy="{y}" rx="{rx}" ry="{ry}" fill="{topc}" {S()}/>')
    return "".join(out)

def red_velvet():
    crumbs = "".join(f'<circle cx="{x}" cy="{y}" r="1.6" fill="#c0182f"/>' for x, y in ((46, 26), (54, 22), (66, 23), (74, 27), (60, 28), (52, 30), (70, 31)))
    return (shadow() + plate(60, 72, 50) + layer_cake(60, 18, 70, 34, ["#d42b44", "#d42b44", "#d42b44"], "#fffaf0") + crumbs
        + f'<path d="M60 14 C56 6 46 10 52 17 L60 24 L68 17 C74 10 64 6 60 14Z" fill="#ff5f7e" {S(1.8)}/>'
        + face(60, 46, 1.0) + sparkle(14, 30, 4) + sparkle(108, 26, 4))

def brownies():
    def block(x, y, w, h, c):
        return (f'<path d="M{x} {y} L{x+w} {y} L{x+w} {y+h} L{x} {y+h}Z" fill="{c}" {S()}/>'
                f'<path d="M{x} {y} L{x+8} {y-8} L{x+w+8} {y-8} L{x+w} {y}Z" fill="#8a4b2f" {S()}/>'
                f'<path d="M{x+w} {y} L{x+w+8} {y-8} L{x+w+8} {y+h-8} L{x+w} {y+h}Z" fill="#4a2417" {S()}/>')
    return (shadow() + block(18, 52, 58, 22, "#6b3622") + block(30, 32, 58, 20, "#6b3622") + block(22, 14, 52, 18, "#6b3622")
        + f'<path d="M30 40 Q60 36 88 40" fill="none" stroke="#3b1a10" stroke-width="2.4"/>'
        + f'<path d="M28 20 Q40 15 50 18 L52 12 L36 12Z" fill="#c98a4b" {S(1.4)}/><path d="M60 20 q8 -5 14 0 q-2 5 -8 4z" fill="#c98a4b" {S(1.4)}/>'
        + f'<path d="M26 56 Q40 61 56 58 Q66 62 72 57" fill="none" stroke="#fff0d6" stroke-width="2" opacity=".35"/>'
        + face(46, 62, 1.0, "grin") + sparkle(100, 26, 4) + sparkle(100, 60, 3, "#ffd8a8"))

def victoria():
    return (shadow() + plate(60, 72, 50) +
        f'<path d="M22 34 L22 66 Q60 80 98 66 L98 34Z" fill="#f4c565" {S()}/>'
        f'<path d="M22 46 Q60 60 98 46 L98 51 Q60 65 22 51Z" fill="#fffaf0" {S(2)}/>'
        f'<path d="M22 51 Q60 65 98 51 L98 56 Q60 70 22 56Z" fill="#e0243f" {S(2)}/>'
        f'<ellipse cx="60" cy="34" rx="38" ry="12" fill="#fbe0a0" {S()}/>'
        f'<path d="M30 33 Q36 28 44 31 M70 28 Q78 26 88 32 M44 37 Q60 41 78 36" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" opacity=".85"/>'
        + strawberry(60, 26, 6.5)
        + "".join(f'<circle cx="{x}" cy="{y}" r="1.1" fill="#fff"/>' for x, y in ((40, 36), (82, 34), (52, 30), (70, 38)))
        + face(60, 56, 1.0, "grin") + f'<path d="M48 12 L53 20 L60 8 L67 20 L72 12 L72 22 L48 22Z" fill="#ffd23f" {S(1.8)}/>' + sparkle(100, 18, 4) + sparkle(16, 20, 3))

def carrot_cake():
    carrot = (f'<path d="M62 8 Q68 4 70 10 M66 8 Q72 2 76 8" fill="none" stroke="#4fae3f" stroke-width="3" stroke-linecap="round"/>'
              f'<path d="M58 16 L76 14 L68 36Z" fill="#ff8a1f" {S(2)}/><path d="M63 20 l5 1 M65 26 l4 0" stroke="#d96a00" stroke-width="1.5" fill="none"/>')
    return (shadow() +
        f'<path d="M16 38 L16 70 L98 70 L98 38Z" fill="#c9783c" {S()}/>'
        f'<path d="M16 38 L30 24 L112 24 L98 38Z" fill="#fff6e6" {S()}/><path d="M98 38 L112 24 L112 56 L98 70Z" fill="#a85f2b" {S()}/>'
        f'<path d="M16 50 L98 50 L98 55 L16 55Z" fill="#fff6e6" {S(1.8)}/><path d="M98 50 L112 36 L112 41 L98 55Z" fill="#f2dfc1" {S(1.8)}/>'
        f'<path d="M16 38 L98 38 L98 43 L16 43Z" fill="#fff6e6" {S(1.8)}/>'
        + "".join(f'<ellipse cx="{x}" cy="{y}" rx="3.2" ry="1.5" fill="#ff8a1f" transform="rotate({r} {x} {y})"/>' for x, y, r in ((30, 62, 20), (52, 60, -15), (74, 63, 30), (88, 58, 0), (40, 47, 10)))
        + f'<path d="M24 48 q3 -3 6 0 M60 66 q3 -3 6 0" stroke="#7a3f12" stroke-width="2" fill="none"/>'
        + carrot + face(56, 58, 1.0) + sparkle(14, 20, 4) + sparkle(110, 14, 3))

def banana_bread():
    banana = lambda x, y: (f'<ellipse cx="{x}" cy="{y}" rx="7" ry="5.4" fill="#ffe14d" {S(2)}/><ellipse cx="{x}" cy="{y}" rx="3.2" ry="2.3" fill="#fff4a8"/>')
    return (shadow() +
        f'<path d="M12 40 Q12 26 28 26 L92 26 Q108 26 108 40 L102 70 Q60 80 18 70Z" fill="#b8742f" {S()}/>'
        f'<path d="M12 40 Q12 22 30 22 L90 22 Q108 22 108 40 Q60 48 12 40Z" fill="#8a5220" {S()}/>'
        f'<path d="M30 33 Q60 29 90 33" fill="none" stroke="#5c3412" stroke-width="2.6" stroke-linecap="round"/>'
        + banana(34, 34) + banana(52, 30) + banana(70, 30) + banana(88, 34)
        + "".join(f'<circle cx="{x}" cy="{y}" r="1.2" fill="#5c3412"/>' for x, y in ((24, 50), (96, 52), (70, 62), (40, 64)))
        + face(60, 56, 1.05) + sparkle(14, 16, 4) + sparkle(106, 14, 4))

def pavlova():
    swirls = "".join(f'<path d="M{x} 26 Q{x+3} 44 {x+1} 62" fill="none" stroke="#e7d8f0" stroke-width="2.2" stroke-linecap="round"/>' for x in (32, 44, 58, 72, 86))
    return (shadow() + plate(60, 72, 50, "#ffffff") +
        f'<path d="M18 62 Q16 34 36 28 Q60 20 84 28 Q104 34 102 62 Q60 74 18 62Z" fill="#fff4fb" {S()}/>' + swirls +
        f'<path d="M30 32 Q60 18 90 32 Q96 40 60 42 Q24 40 30 32Z" fill="#ffffff" {S(2)}/>'
        + strawberry(44, 28, 6) + strawberry(76, 28, 6)
        + f'<circle cx="60" cy="24" r="7" fill="#7ed957" {S(2)}/><circle cx="60" cy="24" r="3" fill="#e9ffc9"/>'
        + "".join(f'<circle cx="{x}" cy="{y}" r="3" fill="#5a67e8" {S(1.6)}/>' for x, y in ((52, 32), (68, 32), (36, 36), (84, 36)))
        + face(60, 54, 1.05) + sparkle(104, 16, 4) + sparkle(12, 20, 4))

def tiramisu():
    return (shadow() +
        f'<path d="M18 34 L18 66 Q18 76 28 76 L92 76 Q102 76 102 66 L102 34Z" fill="#e8f6ff" opacity=".75" {S()}/>'
        f'<path d="M20 38 L100 38 L100 48 L20 48Z" fill="#6b3a26" {S(1.8)}/>'
        f'<path d="M20 48 L100 48 L100 56 L20 56Z" fill="#fff3d0" {S(1.8)}/>'
        f'<path d="M20 56 L100 56 L100 63 L20 63Z" fill="#b97b45" {S(1.8)}/>'
        f'<path d="M20 63 L100 63 L100 70 Q100 74 90 74 L30 74 Q20 74 20 70Z" fill="#fff3d0" {S(1.8)}/>'
        f'<ellipse cx="60" cy="34" rx="42" ry="7" fill="#7a4228" {S()}/>'
        + "".join(f'<circle cx="{x}" cy="{y}" r="1.2" fill="#c89a72"/>' for x, y in ((30, 34), (48, 32), (66, 35), (84, 33), (92, 36)))
        + "".join(f'<ellipse cx="{x}" cy="{y}" rx="3" ry="2.1" fill="#3a1f12" {S(1.2)} transform="rotate({r} {x} {y})"/>' for x, y, r in ((44, 28, 20), (60, 26, -10), (76, 28, 30)))
        + f'<path d="M96 14 L104 4 L108 8 L100 18Z" fill="#c9d0d6" {S(1.6)}/>'
        + face(60, 55, 1.0, "grin") + sparkle(12, 24, 4) + sparkle(110, 40, 3))

def black_forest():
    curls = "".join(f'<path d="M{x} {y} q3 -5 6 0 q-3 4 -6 0" fill="#7a4a30" {S(1.2)}/>' for x, y in ((36, 24), (52, 20), (68, 21), (84, 25), (60, 25)))
    return (shadow() + plate(60, 72, 50) + layer_cake(60, 20, 72, 36, ["#4a2417", "#4a2417", "#4a2417"], "#fff7ea", "#ffffff") +
        f'<path d="M20 28 Q24 36 22 44 M100 28 Q96 38 98 46" fill="none" stroke="#fff" stroke-width="2" opacity=".5"/>'
        + curls + cherry(44, 20, 5) + cherry(60, 17, 5) + cherry(76, 20, 5)
        + face(60, 48, 1.0, "grin") + sparkle(12, 22, 4) + sparkle(108, 22, 4))

def croquembouche():
    rows = []
    ys = [70, 56, 43, 31, 20]; ns = [5, 4, 3, 2, 1]
    for y, n in zip(ys, ns):
        for i in range(n):
            x = 60 + (i - (n - 1) / 2) * 20
            rows.append(f'<circle cx="{x}" cy="{y}" r="10" fill="#f0b45e" {S(2.2)}/><path d="M{x-6} {y-3} Q{x} {y-9} {x+6} {y-3}" fill="none" stroke="#fff3c4" stroke-width="2" stroke-linecap="round"/>')
    threads = "".join(f'<path d="M{x} 6 Q{x+dx} 36 {x+dx*1.4} 72" fill="none" stroke="#ff9d2e" stroke-width="1.8" stroke-linecap="round" opacity=".8"/>' for x, dx in ((60, -26), (60, 26), (60, -12), (60, 12)))
    return (shadow() + "".join(rows) + threads + f'<circle cx="60" cy="9" r="5" fill="#ff7aa2" {S(1.8)}/>' + sparkle(60, 4, 4, "#fff3c4")
        + face(60, 49, .8) + sparkle(12, 30, 4) + sparkle(108, 34, 4))

def cheesecake():
    return (shadow() + plate(60, 72, 52) +
        f'<path d="M14 54 L104 40 L104 62 L14 66Z" fill="#b97a3a" {S()}/>'
        f'<path d="M14 40 L104 28 L104 40 L14 54Z" fill="#ffe9a8" {S()}/>'
        f'<path d="M14 40 L60 12 L104 28 L104 40Z" fill="#ffd9a0" opacity="0" />'
        f'<path d="M14 40 Q40 20 66 14 L104 28 Q70 34 14 40Z" fill="#f9f1d6" {S()}/>'
        f'<path d="M30 33 Q60 26 100 27 Q100 36 94 38 Q92 44 88 38 Q84 46 78 36 Q70 40 66 32 Q54 36 30 36Z" fill="#e0243f" {S(2)}/>'
        + strawberry(70, 22, 6) + "".join(f'<circle cx="{x}" cy="{y}" r="3" fill="#5a67e8" {S(1.6)}/>' for x, y in ((50, 27), (84, 24)))
        + face(50, 53, 1.0) + sparkle(100, 12, 4) + sparkle(10, 28, 3))

def fruitcake():
    cherries = "".join(f'<circle cx="{x}" cy="{y}" r="4.8" fill="{c}" {S(1.8)}/><circle cx="{x-1.4}" cy="{y-1.4}" r="1.1" fill="#fff" opacity=".8"/>' for x, y, c in ((30, 32, "#e0243f"), (50, 28, "#2fb36a"), (72, 28, "#e0243f"), (90, 32, "#2fb36a")))
    nuts = "".join(f'<ellipse cx="{x}" cy="{y}" rx="3.6" ry="2" fill="#f3dca4" {S(1.4)} transform="rotate({r} {x} {y})"/>' for x, y, r in ((40, 32, 30), (62, 30, -20), (82, 31, 20), (60, 38, 10)))
    holly = (f'<path d="M84 18 q8 -8 14 -2 q-4 8 -14 2z M86 20 q10 2 12 10 q-8 2 -12 -10z" fill="#2f9a52" {S(1.6)}/>'
             f'<circle cx="86" cy="21" r="2.6" fill="#e0243f" {S(1.2)}/><circle cx="91" cy="23" r="2.6" fill="#e0243f" {S(1.2)}/>')
    return (shadow() +
        f'<path d="M12 42 Q12 28 28 28 L92 28 Q108 28 108 42 L102 72 Q60 82 18 72Z" fill="#6a3b22" {S()}/>'
        f'<path d="M12 42 Q12 24 30 24 L90 24 Q108 24 108 42 Q60 52 12 42Z" fill="#fff4dc" {S()}/>'
        + cherries + nuts + f'<path d="M12 58 L108 58 L106 66 L14 66Z" fill="#e0243f" {S(2)}/>'
        + f'<path d="M60 58 L50 76 L60 70 L70 76Z" fill="#e0243f" {S(1.8)}/>' + holly
        + face(60, 50, .95) + sparkle(14, 14, 4) + sparkle(108, 60, 3))


# ---------------------------------------------------------------- Carly's own cakes
import math

def cookie(cx, cy, r, rot=0, bite=False):
    chips = "".join(f'<ellipse cx="{cx+dx*r:.1f}" cy="{cy+dy*r:.1f}" rx="{r*.13:.1f}" ry="{r*.1:.1f}" fill="#4a2417" transform="rotate({ra} {cx+dx*r:.1f} {cy+dy*r:.1f})"/>'
                    for dx, dy, ra in ((-.45, -.35, 20), (.25, -.5, -30), (.55, .05, 40), (-.1, .1, 10), (-.55, .35, -20), (.2, .55, 30), (.62, .5, 0)))
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#dca25e" {S()}/><circle cx="{cx}" cy="{cy}" r="{r*.82}" fill="#e8b878" opacity=".75"/>'
            f'<path d="M{cx-r*.7} {cy-r*.55} Q{cx-r*.35} {cy-r*.85} {cx+r*.1} {cy-r*.8}" fill="none" stroke="#fff3d6" stroke-width="2.4" stroke-linecap="round" opacity=".8"/>' + chips)

def cookies():
    return (shadow() + cookie(32, 56, 21) + cookie(88, 54, 20) + cookie(60, 50, 26)
        + f'<path d="M26 18 q4 -5 8 0 M84 16 q4 -5 8 0" fill="none" stroke="none"/>'
        + face(60, 49, 1.05, "grin") + "".join(f'<circle cx="{x}" cy="{y}" r="1.3" fill="#c98a4b"/>' for x, y in ((14, 74), (24, 78), (98, 76), (108, 72), (60, 80)))
        + sparkle(14, 22, 4) + sparkle(106, 20, 4) + sparkle(60, 12, 3.5))

def candle(x, top, c1, c2):
    return (f'<rect x="{x-2}" y="{top}" width="4" height="13" rx="1.2" fill="{c1}" {S(1.6)}/>'
            f'<path d="M{x-2} {top+4} l4 2 M{x-2} {top+8} l4 2" stroke="{c2}" stroke-width="1.6"/>'
            f'<path d="M{x} {top-9} Q{x+4.6} {top-3} {x} {top-1} Q{x-4.6} {top-3} {x} {top-9}Z" fill="#ffc933" {S(1.4)}/>'
            f'<path d="M{x} {top-5.5} Q{x+1.8} {top-2.8} {x} {top-1.8} Q{x-1.8} {top-2.8} {x} {top-5.5}Z" fill="#ff7a2e"/>')

def balloon(x, y, c):
    return (f'<path d="M{x} {y+11} Q{x+3} {y+22} {x-2} {y+30}" fill="none" {S(1.4)}/>'
            f'<ellipse cx="{x}" cy="{y}" rx="8.2" ry="10" fill="{c}" {S(2)}/><path d="M{x-2} {y+10} l-2 3 h5z" fill="{c}" {S(1.2)}/>'
            f'<path d="M{x-4.6} {y-5} Q{x-5} {y-1} {x-3.4} {y+1}" fill="none" stroke="#fff" stroke-width="1.8" stroke-linecap="round" opacity=".7"/>')

def birthday_cake():
    spr = "".join(f'<rect x="{x}" y="{y}" width="3.2" height="1.6" rx=".8" fill="{c}" transform="rotate({r} {x} {y})"/>' for x, y, c, r in ((44, 52, "#ffd23f", 20), (78, 50, "#4fc3f7", -30), (50, 62, "#7ee0a6", 40), (72, 66, "#ffd23f", 10), (36, 60, "#4fc3f7", -20), (84, 60, "#7ee0a6", 30)))
    return (shadow() + balloon(14, 24, "#4fc3f7") + balloon(106, 18, "#ffd23f") +
        f'<path d="M28 40 L28 68 Q60 86 92 68 L92 40Z" fill="#ff93b9" {S()}/>'
        f'<path d="M28 52 Q60 70 92 52 L92 57 Q60 75 28 57Z" fill="#fffaf0" {S(2)}/>'
        f'<path d="{drip(28, 92, 42, 12, "#fff", 6)} L92 36 Q60 28 28 36Z" fill="#ffffff" {S(2.2)}/>'
        f'<ellipse cx="60" cy="38" rx="32" ry="10" fill="#fff6fa" {S()}/>'
        + candle(46, 22, "#7ee0a6", "#fff") + candle(60, 20, "#ffd23f", "#fff") + candle(74, 22, "#4fc3f7", "#fff") + spr
        + face(60, 60, 1.0, "grin") + sparkle(98, 52, 3.5) + sparkle(24, 66, 3))

def celebration_cake():
    flags = "".join(f'<path d="M{x} 9 L{x+8} 9 L{x+4} 18Z" fill="{c}" {S(1.6)}/>' for x, c in ((14, "#ff6f98"), (28, "#ffd23f"), (42, "#4fc3f7"), (76, "#ff6f98"), (90, "#ffd23f"), (104, "#7ee0a6")))
    stars = "".join(f'<path d="M{x} {y-3.2} L{x+1.1} {y-1} L{x+3.4} {y-.8} L{x+1.6} {y+.8} L{x+2.1} {y+3.2} L{x} {y+1.9} L{x-2.1} {y+3.2} L{x-1.6} {y+.8} L{x-3.4} {y-.8} L{x-1.1} {y-1}Z" fill="#ffd23f" {S(1)}/>'
                    for x, y in ((38, 50), (82, 50), (48, 64), (72, 64)))
    spark = "".join(f'<path d="M60 22 L{60+11*math.cos(a):.1f} {22+11*math.sin(a):.1f}" stroke="#ffb100" stroke-width="2" stroke-linecap="round"/>' for a in [i * math.pi / 4 for i in range(8)])
    return (shadow() + f'<path d="M6 9 Q60 22 114 9" fill="none" {S(1.6)}/>' + flags + plate(60, 72, 48) +
        layer_cake(60, 30, 64, 32, ["#8c6ff0", "#8c6ff0", "#8c6ff0"], "#ffffff", "#ffd23f") + stars
        + f'<path d="M60 40 V25" {S(2.2)}/><path d="M60 24 v-4" stroke="#c9d0d6" stroke-width="2.4"/>' + spark
        + "".join(f'<circle cx="{x}" cy="{y}" r="1.7" fill="{c}"/>' for x, y, c in ((16, 34, "#ff6f98"), (104, 40, "#ffd23f"), (24, 50, "#4fc3f7"), (98, 58, "#7ee0a6"), (12, 62, "#ffd23f")))
        + face(60, 54, 1.0, "grin"))

def cherry_bakewell():
    flakes = "".join(f'<path d="M{x} {y} q3 -2 5 1 q-2 3 -5 -1z" fill="#fff0c9" {S(1)}/>' for x, y in ((26, 66), (40, 72), (58, 74), (78, 72), (92, 66)))
    feather = "".join(f'<path d="M60 {42} L{60+30*math.cos(a):.1f} {42+8.5*math.sin(a):.1f}" stroke="#ff8fb3" stroke-width="1.4" opacity=".9"/>' for a in [i * math.pi / 5 + .1 for i in range(10)])
    return (shadow() + plate(60, 74, 50) +
        f'<path d="M22 44 L22 64 Q60 82 98 64 L98 44Z" fill="#f2bf62" {S()}/>'
        f'<path d="M22 54 Q60 72 98 54 L98 58 Q60 76 22 58Z" fill="#e0243f" {S(2)}/>'
        f'<ellipse cx="60" cy="44" rx="38" ry="12" fill="#ffffff" {S()}/><ellipse cx="60" cy="44" rx="31" ry="8.6" fill="none" stroke="#ff8fb3" stroke-width="2"/>' + feather
        + flakes + cherry(60, 36, 6.4) + cherry(44, 41, 4.6) + cherry(76, 41, 4.6)
        + face(60, 62, .95) + sparkle(106, 26, 4) + sparkle(14, 28, 3.5))

def blueberry_lemon():
    berry = lambda x, y, r=4.6: (f'<circle cx="{x}" cy="{y}" r="{r}" fill="#5a67e8" {S(1.8)}/><circle cx="{x-1.4}" cy="{y-1.4}" r="1.1" fill="#fff" opacity=".8"/>'
                                 f'<path d="M{x-1.2} {y+.4} l1.2 -1.4 l1.2 1.4" fill="none" stroke="#2c357f" stroke-width="1"/>')
    seeds = "".join(f'<circle cx="{x}" cy="{y}" r="1.6" fill="#5a67e8"/>' for x, y in ((34, 58), (46, 64), (74, 62), (86, 56), (60, 68)))
    lemon = (f'<circle cx="100" cy="64" r="11" fill="#ffe65a" {S()}/><circle cx="100" cy="64" r="7.6" fill="#fff9c2" {S(1.3)}/>'
             + "".join(f'<path d="M100 64 L{100+7.6*math.cos(a):.1f} {64+7.6*math.sin(a):.1f}" stroke="{OUT}" stroke-width="1.1"/>' for a in [i * math.pi / 3 for i in range(6)]))
    return (shadow() + plate(56, 74, 46) +
        f'<path d="M20 42 L20 66 Q56 82 92 66 L92 42Z" fill="#f6d466" {S()}/>' + seeds +
        f'<path d="{drip(20, 92, 44, 15, "#fff", 6)} L92 38 Q56 30 20 38Z" fill="#ffffff" {S(2.2)}/>'
        f'<ellipse cx="56" cy="40" rx="36" ry="11" fill="#fffbe0" {S()}/>'
        + berry(40, 36) + berry(52, 32) + berry(66, 34) + berry(76, 39) + berry(46, 42, 4) + berry(62, 41, 4)
        + f'<path d="M56 22 q4 -8 9 -3 M70 24 q6 -6 10 0" fill="none" stroke="#9bd24a" stroke-width="2.6" stroke-linecap="round"/>'
        + lemon + face(56, 58, 1.0, "grin") + sparkle(12, 24, 4) + sparkle(106, 30, 3))

def pecan(x, y, r=0):
    return (f'<g transform="rotate({r} {x} {y})"><path d="M{x-5} {y} Q{x-5} {y-5} {x} {y-6} Q{x+5} {y-5} {x+5} {y} Q{x+3} {y+6} {x} {y+7} Q{x-3} {y+6} {x-5} {y}Z" fill="#b8742f" {S(1.6)}/>'
            f'<path d="M{x} {y-5} V{y+5}" stroke="#7a4a1e" stroke-width="1.4"/></g>')

def coffee_pecan():
    bean = lambda x, y, r: (f'<ellipse cx="{x}" cy="{y}" rx="4.2" ry="3" fill="#5a3320" {S(1.4)} transform="rotate({r} {x} {y})"/>'
                            f'<path d="M{x-3.6} {y} Q{x} {y-1.6} {x+3.6} {y}" fill="none" stroke="#2a150c" stroke-width="1" transform="rotate({r} {x} {y})"/>')
    cup = (f'<path d="M92 50 H112 L110 68 Q102 72 94 68Z" fill="#fff" {S(2)}/><path d="M112 54 Q119 56 112 62" fill="none" {S(2)}/>'
           f'<path d="M94 53 H110" stroke="#6b3a1e" stroke-width="3"/><path d="M98 46 q-3 -4 0 -7 M105 46 q-3 -4 0 -7" fill="none" stroke="{OUT}" stroke-width="1.8" stroke-linecap="round" opacity=".5"/>')
    return (shadow(56, 80, 44) + plate(52, 74, 44) +
        f'<path d="M18 40 L18 66 Q52 82 86 66 L86 40Z" fill="#a9703c" {S()}/>'
        f'<path d="M18 52 Q52 68 86 52 L86 57 Q52 73 18 57Z" fill="#fff0d6" {S(2)}/>'
        f'<path d="{drip(18, 86, 41, 14, "#e8a33a", 5)} L86 36 Q52 30 18 36Z" fill="#e8a33a" {S(2.2)}/>'
        f'<ellipse cx="52" cy="38" rx="34" ry="10.5" fill="#8a5530" {S()}/><path d="M32 38 Q52 30 72 38" fill="none" stroke="#b9854f" stroke-width="2.2" stroke-linecap="round"/>'
        + pecan(38, 36, -30) + pecan(52, 31, 10) + pecan(66, 36, 35) + pecan(52, 41, 80)
        + "".join(f'<rect x="{x}" y="{y}" width="2" height="2" fill="#fff" {S(.7)} transform="rotate(30 {x} {y})"/>' for x, y in ((30, 34), (44, 29), (60, 28), (74, 34), (46, 40), (60, 40)))
        + cup + bean(14, 74, 20) + bean(24, 79, -30) + face(52, 58, 1.0) + sparkle(12, 18, 4) + sparkle(78, 12, 3.5))

def tier(cx, top, rx, ry, h, fill="#ffffff"):
    return (f'<path d="M{cx-rx} {top} L{cx-rx} {top+h} Q{cx} {top+h+ry*2} {cx+rx} {top+h} L{cx+rx} {top}Z" fill="{fill}" {S()}/>'
            f'<ellipse cx="{cx}" cy="{top}" rx="{rx}" ry="{ry}" fill="#fffdf8" {S()}/>')

def pearls(cx, top_y, rx, ry, h, n):
    out = []
    for i in range(n):
        x = cx - rx + 3 + (2 * rx - 6) * i / (n - 1)
        y = top_y + h + ry * math.sqrt(max(0, 1 - ((x - cx) / rx) ** 2))
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.9" fill="#fff" {S(1.1)}/>')
    return "".join(out)

def rose(x, y, c="#ff6f98"):
    return (f'<circle cx="{x}" cy="{y}" r="5.4" fill="{c}" {S(1.8)}/><path d="M{x-2.6} {y} Q{x-2.6} {y-3} {x} {y-3} Q{x+3} {y-3} {x+3} {y} Q{x+3} {y+3.4} {x} {y+3.4}" fill="none" stroke="{OUT}" stroke-width="1.3" stroke-linecap="round"/>')

def wedding_cake():
    leaf = lambda x, y, r: f'<path d="M{x} {y} q6 -4 10 1 q-5 5 -10 -1z" fill="#59b84a" {S(1.3)} transform="rotate({r} {x} {y})"/>'
    return (shadow() + plate(60, 76, 50) +
        tier(60, 52, 34, 8, 20) + tier(60, 34, 25, 6.5, 18) + tier(60, 20, 16, 5, 14)
        + f'<path d="M26 58 Q60 74 94 58 L94 63 Q60 79 26 63Z" fill="#ff9bb8" {S(1.8)}/>'
        + pearls(60, 34, 25, 6.5, 18, 9) + pearls(60, 20, 16, 5, 14, 6) + pearls(60, 52, 34, 8, 20, 12)
        + leaf(24, 54, 160) + leaf(86, 54, 20) + rose(30, 52) + rose(90, 52) + rose(60, 8, "#ff6f98") + leaf(48, 10, 190) + leaf(62, 10, -10)
        + f'<path d="M60 3 C54 -3 46 3 52 8 L60 14 L68 8 C74 3 66 -3 60 3Z" fill="#ff6f98" {S(1.6)} transform="translate(0 0) scale(.7) translate(25 6)"/>'
        + face(60, 44, .85) + sparkle(12, 22, 4) + sparkle(108, 26, 4) + sparkle(100, 8, 3))

ART = {"Souffle": souffle, "Macarons": macarons, "Scones": scones, "Choux Puffs": choux, "Cupcakes": cupcakes,
       "Genoise": genoise, "Lemon Drizzle": lemon_drizzle, "Red Velvet": red_velvet, "Brownies": brownies,
       "Victoria Sponge": victoria, "Carrot Cake": carrot_cake, "Banana Bread": banana_bread, "Pavlova": pavlova,
       "Tiramisu": tiramisu, "Cookies": cookies, "Birthday Cake": birthday_cake, "Celebration Cake": celebration_cake, "Cherry Bakewell": cherry_bakewell, "Blueberry & Lemon Cake": blueberry_lemon, "Coffee & Salted Pecan": coffee_pecan, "Wedding Cake": wedding_cake, "Black Forest": black_forest, "Croquembouche": croquembouche, "Cheesecake": cheesecake,
       "Fruitcake": fruitcake}

def svg(name):
    return f'<svg viewBox="0 0 120 84" xmlns="http://www.w3.org/2000/svg">{ART[name]()}</svg>'
