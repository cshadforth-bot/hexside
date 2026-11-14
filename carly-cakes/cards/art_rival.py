"""Cartoon Rival Bakers (120 x 84 viewBox). Same line style as art.py."""
from art import OUT, S, sparkle

def _hat(c="#ffffff", tilt=0):
    return (f'<g transform="rotate({tilt} 60 22)">'
            + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" {S(2.2)}/>' for x, y, r in ((47, 16, 8), (73, 16, 8), (60, 10, 10)))
            + f'<rect x="43" y="19" width="34" height="11" rx="4" fill="{c}" {S(2.2)}/>'
            + f'<path d="M45 25 H75" stroke="#ff9db8" stroke-width="3" stroke-linecap="round"/></g>')

def _body(apron, skin, arms=None):
    a = ""
    if arms == "up":
        a = (f'<path d="M36 62 Q22 52 24 36" fill="none" stroke="{skin}" stroke-width="7" stroke-linecap="round"/>'
             f'<path d="M84 62 Q98 52 96 36" fill="none" stroke="{skin}" stroke-width="7" stroke-linecap="round"/>'
             f'<circle cx="24" cy="34" r="5.2" fill="{skin}" {S(2)}/><circle cx="96" cy="34" r="5.2" fill="{skin}" {S(2)}/>')
    return (f'<ellipse cx="60" cy="80" rx="38" ry="4" fill="{OUT}" opacity=".16"/>' + a +
            f'<path d="M30 82 L35 58 Q60 50 85 58 L90 82 Z" fill="{apron}" {S()}/>'
            f'<path d="M46 56 L60 66 L74 56" fill="#fffdf8" {S(2)}/>'
            f'<rect x="50" y="68" width="20" height="10" rx="3" fill="#fffdf8" opacity=".85" {S(1.6)}/>')

def _head(skin, cx=60, cy=40):
    return (f'<circle cx="{cx-18}" cy="{cy+2}" r="4" fill="{skin}" {S(2)}/><circle cx="{cx+18}" cy="{cy+2}" r="4" fill="{skin}" {S(2)}/>'
            f'<circle cx="{cx}" cy="{cy}" r="19" fill="{skin}" {S()}/>')

def _eyes(kind, cx=60, cy=40):
    if kind == "dots":
        return "".join(f'<ellipse cx="{cx+d}" cy="{cy}" rx="2.4" ry="3.1" fill="{OUT}"/><circle cx="{cx+d-.8}" cy="{cy-1.1}" r=".9" fill="#fff"/>' for d in (-7, 7))
    if kind == "sleepy":
        return "".join(f'<path d="M{cx+d-3.5} {cy} Q{cx+d} {cy+3.4} {cx+d+3.5} {cy}" fill="none" {S(1.9)}/>' for d in (-7, 7))
    if kind == "angry":
        return ("".join(f'<ellipse cx="{cx+d}" cy="{cy+1}" rx="2.3" ry="2.8" fill="{OUT}"/>' for d in (-7, 7)) +
                f'<path d="M{cx-12} {cy-6} L{cx-3} {cy-3}" {S(2.2)}/><path d="M{cx+12} {cy-6} L{cx+3} {cy-3}" {S(2.2)}/>')
    if kind == "star":
        return "".join(sparkle(cx + d, cy, 3.6, "#ffe14d") for d in (-7, 7))
    if kind == "wide":
        return "".join(f'<circle cx="{cx+d}" cy="{cy}" r="3.6" fill="#fff" {S(1.6)}/><circle cx="{cx+d}" cy="{cy+.4}" r="1.6" fill="{OUT}"/>' for d in (-7, 7))

def _mouth(kind, cx=60, cy=40):
    if kind == "smile": return f'<path d="M{cx-4} {cy+7} Q{cx} {cy+12} {cx+4} {cy+7}" fill="none" {S(1.9)}/>'
    if kind == "grin": return (f'<path d="M{cx-6} {cy+6} Q{cx} {cy+16} {cx+6} {cy+6}Z" fill="{OUT}" {S(1.4)}/>'
                               f'<path d="M{cx-3} {cy+11.5} Q{cx} {cy+9} {cx+3} {cy+11.5} Q{cx} {cy+13.5} {cx-3} {cy+11.5}Z" fill="#ff6b81"/>')
    if kind == "yawn": return f'<ellipse cx="{cx}" cy="{cy+9}" rx="3.6" ry="4.6" fill="{OUT}" {S(1.4)}/><ellipse cx="{cx}" cy="{cy+11}" rx="2" ry="1.9" fill="#ff6b81"/>'
    if kind == "gritted": return (f'<rect x="{cx-6}" y="{cy+6}" width="12" height="6.4" rx="2" fill="#fff" {S(1.6)}/>'
                                  f'<path d="M{cx-2} {cy+6} V{cy+12.4} M{cx+2} {cy+6} V{cy+12.4}" stroke="{OUT}" stroke-width="1.2"/>')
    if kind == "tongue": return (f'<path d="M{cx-5} {cy+7} Q{cx} {cy+11} {cx+5} {cy+7}" fill="none" {S(1.9)}/>'
                                 f'<path d="M{cx-1} {cy+9} Q{cx-1} {cy+16} {cx+3} {cy+13} Q{cx+4} {cy+10} {cx+3} {cy+9.4}Z" fill="#ff6b81" {S(1.3)}/>')

def _blush(skin, cx=60, cy=40):
    return "".join(f'<ellipse cx="{cx+d}" cy="{cy+6}" rx="3.2" ry="2" fill="#ff7f9d" opacity=".7"/>' for d in (-12, 12))

def character(skin, apron, eyes, mouth, hat_tilt=0, arms=None):
    return (_body(apron, skin, arms) + _head(skin) + _hat("#ffffff", hat_tilt) + _eyes(eyes) + _blush(skin) + _mouth(mouth))

# ---- the six
def by_the_book():
    glasses = ('<circle cx="53" cy="40" r="6" fill="#fff" fill-opacity=".35" ' + S(1.8) + '/><circle cx="67" cy="40" r="6" fill="#fff" fill-opacity=".35" ' + S(1.8) + '/>'
               f'<path d="M59 40 H61" {S(1.8)}/>')
    clip = (f'<rect x="84" y="46" width="22" height="30" rx="3" fill="#fff6d6" {S(2)}/><rect x="90" y="43" width="10" height="6" rx="2" fill="#9aa5b1" {S(1.8)}/>'
            + "".join(f'<path d="M88 {y} H102" stroke="{OUT}" stroke-width="1.6" stroke-linecap="round"/>' for y in (56, 62, 68))
            + f'<path d="M88 74 L91 71" stroke="#2fb36a" stroke-width="2" stroke-linecap="round"/>')
    return character("#f6d2b5", "#7fc7d9", "dots", "smile") + glasses + clip + sparkle(14, 26, 3.5) + sparkle(108, 20, 3)

def newest_first():
    return (character("#c68642", "#ff9db8", "wide", "grin", -10, arms="up") + sparkle(12, 14, 4, "#ffe14d") + sparkle(108, 12, 4, "#ffe14d")
            + f'<path d="M12 50 l-5 -5 M108 50 l5 -5 M8 24 l-5 -2 M112 24 l5 -2" stroke="{OUT}" stroke-width="2" stroke-linecap="round"/>')

def early_bird():
    bird = (f'<ellipse cx="60" cy="3.5" rx="7" ry="5" fill="#ffd23f" {S(1.8)}/><circle cx="64" cy="0.5" r="3.4" fill="#ffd23f" {S(1.6)}/>'
            f'<path d="M67 0.5 l4 1 -4 1.4Z" fill="#ff8a1f" {S(1)}/><circle cx="65" cy="-.2" r=".9" fill="{OUT}"/>')
    cup = (f'<path d="M84 52 H102 L100 70 Q93 74 86 70Z" fill="#fff" {S(2)}/><path d="M102 56 Q110 58 102 64" fill="none" {S(2)}/>'
           f'<path d="M86 55 H100" stroke="#8a5220" stroke-width="3"/><path d="M90 48 q-3 -4 0 -7 M96 48 q-3 -4 0 -7" fill="none" stroke="{OUT}" stroke-width="1.8" stroke-linecap="round" opacity=".5"/>')
    sun = f'<circle cx="16" cy="20" r="8" fill="#ffd23f" {S(2)}/>' + "".join(f'<path d="M16 {16-9+a} l0 -3" transform="rotate({a} 16 20)" stroke="{OUT}" stroke-width="2" stroke-linecap="round"/>' for a in (0, 45, 90, 135, 180, 225, 270, 315))
    return character("#ffdcb8", "#ffc233", "sleepy", "yawn") + f'<g transform="translate(0 4)">{bird}</g>' + cup + sun

def door_slammer():
    door = (f'<rect x="80" y="30" width="30" height="40" rx="5" fill="#9aa5b1" {S()}/><rect x="85" y="37" width="20" height="14" rx="3" fill="#2a3340" {S(2)}/>'
            f'<path d="M88 41 l5 3" stroke="#fff" stroke-width="2" stroke-linecap="round" opacity=".6"/><rect x="86" y="58" width="18" height="4" rx="2" fill="#6b7682" {S(1.6)}/>')
    return (character("#8d5a3b", "#e0243f", "angry", "gritted") + door
            + f'<path d="M72 46 l8 -4 M72 54 l9 0 M72 62 l8 4" stroke="{OUT}" stroke-width="2.4" stroke-linecap="round"/>'
            + f'<text x="14" y="22" font-family="Fredoka, sans-serif" font-weight="700" font-size="12" fill="#ffd23f" stroke="{OUT}" stroke-width="2.4" paint-order="stroke" transform="rotate(-12 14 22)">SLAM!</text>')

def sweet_tooth():
    pop = (f'<path d="M92 46 L92 80" stroke="#fff" stroke-width="4" stroke-linecap="round"/><path d="M92 46 L92 80" stroke="{OUT}" stroke-width="1.2" stroke-linecap="round" opacity=".5"/>'
           f'<circle cx="92" cy="34" r="14" fill="#ff6f98" {S()}/><path d="M92 34 m-9 0 a9 9 0 1 1 18 0 a6 6 0 1 1 -12 0 a3 3 0 1 1 6 0" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"/>')
    return character("#f2c9a5", "#b99bf0", "star", "tongue") + pop + sparkle(16, 22, 4, "#ffe14d") + sparkle(26, 8, 3, "#fff")

def regular_customer():
    jar = (f'<path d="M84 44 H108 V74 Q108 80 102 80 H90 Q84 80 84 74Z" fill="#e8f6ff" fill-opacity=".85" {S(2)}/><rect x="82" y="38" width="28" height="7" rx="3" fill="#ffd23f" {S(2)}/>'
           + "".join(f'<circle cx="{x}" cy="{y}" r="4.2" fill="#ffd23f" {S(1.6)}/>' for x, y in ((92, 74), (100, 73), (96, 67)))
           + f'<text x="96" y="62" text-anchor="middle" font-family="Fredoka, sans-serif" font-weight="700" font-size="9" fill="{OUT}">+1</text>')
    return character("#e9b88a", "#6fd1c2", "dots", "smile") + jar + sparkle(16, 20, 4, "#ffe14d") + sparkle(26, 10, 3, "#fff")

RIVALS = {"By the book": by_the_book, "Newest first": newest_first, "Early bird": early_bird,
          "Door slammer": door_slammer, "Sweet tooth": sweet_tooth, "Regular customer": regular_customer}

def svg(name):
    return f'<svg viewBox="0 0 120 84" xmlns="http://www.w3.org/2000/svg">{RIVALS[name]()}</svg>'
