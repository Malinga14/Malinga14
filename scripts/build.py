#!/usr/bin/env python3
"""Generates the Swiss-style SVG panels used by README.md.

Edit the CONTENT section, then run:  python3 scripts/build.py
Every panel sits on a shared 12-column grid (840 units wide), so the
sections line up with each other when GitHub stacks them.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"

# ── Grid ─────────────────────────────────────────────────────────────
W, M, G, COLS = 840, 32, 16, 12
CW = (W - 2 * M - (COLS - 1) * G) / COLS  # 50 units per column
END = W - M


def col(i):
    return M + i * (CW + G)


# ── Palette (matches GitHub dark so panels blend into the page) ─────
BG = "#0D1117"
FG = "#E6EDF3"
MUTED = "#7D8590"
RULE = "#30363D"
GUIDE = "#161B22"
ACCENT = "#FF4F2B"

FONT = "'Helvetica Neue', Helvetica, Arial, Inter, system-ui, sans-serif"

# ── CONTENT ──────────────────────────────────────────────────────────
NAME = ("Malinga", "Pasindu")
ROLES = ["Full-stack engineer", "AI integration", "Real-time systems", "Cross-platform apps"]
STATEMENT = [
    "Building scalable, AI-powered full-stack",
    "systems — from enterprise web apps to",
    "real-time microservices and mobile.",
]
PROFILE = [
    ("I build software that scales", FG),
    ("quietly and feels considered —", FG),
    ("clean architecture underneath,", MUTED),
    ("a polished experience on top.", MUTED),
]
FACTS = [
    ("Focus", ["Full-stack web", "& AI integration"]),
    ("Method", ["Clean architecture,", "typed end to end"]),
    ("Range", ["Web, mobile, desktop,", "real-time systems"]),
]
STACK = [
    ("Frontend", ["Angular", "Next.js", "React", "TypeScript", "Tailwind CSS", "Zustand"]),
    ("Backend & AI", ["Java", "Spring Boot", "Node.js", "Express", "MySQL", "AI integration"]),
    ("Platforms & Tools", ["Flutter", "Electron", "JavaFX", "WebGL", "Git", "Figma"]),
]
LINKS = [
    ("website", "Website", "malingapasindu.com"),
    ("email", "Email", "Write to me"),
    ("linkedin", "LinkedIn", "malinga-pasindu"),
    ("x", "X / Twitter", "@malinga14"),
    ("instagram", "Instagram", "@__malii__14"),
]

# ── Primitives ───────────────────────────────────────────────────────
BASE_CSS = f"""
:root{{--out:cubic-bezier(0.23,1,0.32,1);--io:cubic-bezier(0.77,0,0.175,1)}}
text{{font-family:{FONT};fill:{FG};font-kerning:normal}}
.m{{fill:{MUTED}}}.a{{fill:{ACCENT}}}
.draw{{transform-box:fill-box;transform-origin:left center;animation:draw 1100ms var(--io) both}}
.rise{{animation:rise 700ms var(--out) both}}
.up{{animation:up 1000ms var(--out) both}}
@keyframes draw{{from{{transform:scaleX(0)}}}}
@keyframes rise{{from{{opacity:0;transform:translateY(8px)}}}}
.lift{{transform-box:fill-box;animation:lift 900ms var(--out) both}}
.nudge{{animation:nudge 800ms var(--out) both}}
@keyframes up{{from{{transform:translateY(190px)}}}}
@keyframes lift{{from{{transform:translateY(110%)}}}}
@keyframes nudge{{from{{opacity:0;transform:translate(-6px,6px)}}}}
@keyframes fade{{from{{opacity:0}}}}
@media (prefers-reduced-motion:reduce){{
 .draw,.rise,.up,.lift,.nudge{{animation-name:fade;animation-duration:400ms}}}}
"""


def svg(w, h, body, title, css=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}">'
        f"<title>{escape(title)}</title><style>{BASE_CSS}{css}</style>"
        f'<rect width="{w}" height="{h}" fill="{BG}"/>{body}</svg>\n'
    )


def t(x, y, s, size=13, weight=400, cls="", anchor="start", track=0, extra="", raw=False):
    attrs = f'x="{x:g}" y="{y:g}" font-size="{size}" font-weight="{weight}"'
    if cls:
        attrs += f' class="{cls}"'
    if anchor != "start":
        attrs += f' text-anchor="{anchor}"'
    if track:
        attrs += f' letter-spacing="{track:g}"'
    return f"<text {attrs}{extra}>{s if raw else escape(s)}</text>"


def rule(x1, x2, y, color=RULE, anim=""):
    a = f' class="draw" style="animation-delay:{anim}"' if anim else ""
    return f'<rect x="{x1:g}" y="{y:g}" width="{x2 - x1:g}" height="1" fill="{color}"{a}/>'


def d(ms):
    """Inline animation delay."""
    return f' style="animation-delay:{ms}ms"'


def line(cid, x, y, s, size, weight=700, cls="", track=0, delay=0, raw=False):
    """A line of type that rises out of its own mask, like the hero name."""
    top, bottom = y - size * 0.95, y + size * 0.3
    return (
        f'<clipPath id="{cid}"><rect x="0" y="{top:g}" width="{W}" height="{bottom - top:g}"/></clipPath>'
        f'<g clip-path="url(#{cid})">'
        + t(x, y, s, size, weight, f"{cls} lift".strip(), track=track, raw=raw, extra=d(delay))
        + "</g>"
    )


def section_head(num, label, aside):
    """Shared header: hairline draws in, then number, label and aside rise."""
    return (
        rule(M, END, 32, anim="0ms")
        + t(col(0), 64, num, 13, 700, "a rise", extra=d(160))
        + t(col(1), 64, label, 13, 700, "rise", extra=d(220))
        + t(END, 64, aside, 13, 400, "m rise", "end", extra=d(280))
    )


# ── Panels ───────────────────────────────────────────────────────────
def hero():
    b = "".join(
        f'<rect x="{col(i):g}" y="0" width="1" height="572" fill="{GUIDE}"/>' for i in range(COLS)
    ) + f'<rect x="{END - 1:g}" y="0" width="1" height="572" fill="{GUIDE}"/>'

    # Meta row
    b += f'<rect x="{M}" y="40" width="10" height="10" fill="{ACCENT}" class="rise"/>'
    meta = [
        (col(0) + 18, "Malinga Pasindu", 700, "start"),
        (col(3), "Software Engineer", 400, "start"),
        (col(6), "Sri Lanka — GMT+5:30", 400, "start"),
        (END, "malingapasindu.com", 400, "end"),
    ]
    for i, (x, s, w, anc) in enumerate(meta):
        b += t(x, 50, s, 13, w, "rise", anc, extra=f' style="animation-delay:{100 + i * 60}ms"')
    b += rule(M, END, 70, anim="0ms")

    # Name — each line rises out of its own mask
    size, track = 168, -7.5
    lines = [(NAME[0], 210, 60, 255), (NAME[1] + '<tspan class="a">.</tspan>', 374, 250, 380)]
    for i, (s, y, top, bottom) in enumerate(lines):
        b += (
            f'<clipPath id="n{i}"><rect x="0" y="{top}" width="{W}" height="{bottom - top}"/></clipPath>'
            f'<g clip-path="url(#n{i})">'
            + t(M - 6, y, s, size, 700, "up", track=track, raw=True,
                extra=f' style="animation-delay:{280 + i * 90}ms"')
            + "</g>"
        )
    b += rule(M, END, 410, anim="520ms")

    # Bottom grid: discipline / statement / index
    labels = [(col(0), "(Discipline)"), (col(3), "(Statement)"), (col(9), "(Index)")]
    for i, (x, s) in enumerate(labels):
        b += t(x, 444, s, 13, 400, "m rise", extra=f' style="animation-delay:{760 + i * 60}ms"')

    for i, r in enumerate(ROLES):
        b += t(col(0), 474, r, 17, 500, f"role r{i}",
               extra=f' style="animation-delay:{1100 + i * 3000}ms"')

    for i, s in enumerate(STATEMENT):
        b += t(col(3), 474 + i * 24, s, 17, 400, "rise",
               extra=f' style="animation-delay:{880 + i * 60}ms"')

    for i, s in enumerate(["Profile", "Capabilities", "Contact"]):
        d = f' style="animation-delay:{940 + i * 50}ms"'
        b += t(col(9), 474 + i * 20, f"0{i + 1}", 13, 400, "m rise", extra=d)
        b += t(col(9) + 26, 474 + i * 20, s, 13, 400, "rise", extra=d)

    css = """
.role{opacity:0;animation:role 12000ms linear infinite both}
@keyframes role{
 0%{opacity:0;transform:translateY(6px);filter:blur(4px);animation-timing-function:cubic-bezier(0.23,1,0.32,1)}
 5%{opacity:1;transform:none;filter:blur(0)}
 22%{opacity:1;transform:none;filter:blur(0);animation-timing-function:cubic-bezier(0.23,1,0.32,1)}
 25%,100%{opacity:0;transform:translateY(-6px);filter:blur(4px)}}
@media (prefers-reduced-motion:reduce){.role{animation:none}.r0{opacity:1}}
"""
    title = f"{NAME[0]} {NAME[1]}. Software engineer, Sri Lanka. " + " ".join(STATEMENT)
    return svg(W, 572, b, title, css)


def profile():
    b = section_head("01", "Profile", "About")
    for i, (s, c) in enumerate(PROFILE):
        cls = "m" if c == MUTED else ""
        b += line(f"p{i}", col(3), 122 + i * 40, s, 30, 500, cls, -0.6, 320 + i * 70)
    b += rule(col(3), END, 300, anim="560ms")
    for i, (label, vals) in enumerate(FACTS):
        x = col(3 + i * 3)
        b += t(x, 330, label, 13, 400, "m rise", extra=d(760 + i * 60))
        for j, v in enumerate(vals):
            b += t(x, 356 + j * 21, v, 15, 400, "rise", extra=d(820 + i * 60 + j * 40))
    title = "01 Profile. " + " ".join(s for s, _ in PROFILE)
    return svg(W, 420, b, title)


def capabilities():
    b = section_head("02", "Capabilities", "Stack")
    for i, s in enumerate(["Tools I reach for to", "ship production software,", "front to back."]):
        b += t(col(0), 122 + i * 20, s, 14, 400, "m rise", extra=d(320 + i * 60))
    # Columns cascade diagonally: each column starts 90ms after the last,
    # each row 45ms after the one above, so the table "builds" itself.
    for g, (title, items) in enumerate(STACK):
        x1, x2 = col(3 + g * 3), col(3 + g * 3) + 3 * CW + 2 * G
        base = 380 + g * 90
        b += t(x1, 122, title, 15, 700, "rise", extra=d(base))
        b += rule(x1, x2, 140, anim=f"{base + 40}ms")
        for k, item in enumerate(items):
            y, delay = 140 + k * 36, base + 120 + k * 45
            b += t(x1, y + 23, f"0{k + 1}", 12, 400, "m rise", extra=d(delay))
            b += t(x1 + 28, y + 23, item, 15, 400, "rise", extra=d(delay + 30))
            b += rule(x1, x2, y + 36, anim=f"{delay + 30}ms")
    title = "02 Capabilities. " + ". ".join(f"{h}: {', '.join(i)}" for h, i in STACK)
    return svg(W, 400, b, title)


def contact():
    b = section_head("03", "Contact", "Say hello")
    b += line("c0", col(3), 140, "Let’s build something", 46, 700, track=-1.4, delay=320)
    b += line("c1", col(3), 192, 'considered<tspan class="a">.</tspan>', 46, 700,
              track=-1.4, delay=410, raw=True)
    b += t(col(3), 242, "Projects, collaborations or just a good conversation —", 15, 400,
           "m rise", extra=d(680))
    b += t(col(3), 264, "hello@malingapasindu.com", 15, 500, "rise", extra=d(740))
    return svg(W, 304, b, "03 Contact. Let's build something considered. hello@malingapasindu.com")


def link_buttons():
    """Five linkable tiles that tile the grid exactly when placed side by side."""
    bw = (END - M - 4 * G) / 5
    files = []
    for i, (slug, label, sub) in enumerate(LINKS):
        left = M if i == 0 else 0
        right = M if i == 4 else G
        w = left + bw + right
        x1, x2 = left, left + bw
        base = i * 70
        b = rule(x1, x2, 0, FG, anim=f"{base}ms")
        b += t(x1, 28, label, 15, 700, "rise", extra=d(base + 200))
        b += t(x1, 48, sub, 12, 400, "m rise", extra=d(base + 260))
        b += t(x2, 29, "↗", 15, 400, "a nudge", "end", extra=d(base + 380))
        files.append((f"link-{slug}.svg", svg(round(w, 2), 72, b, f"{label}: {sub}"), w / W * 100))
    return files


def footer():
    b = rule(M, END, 32, anim="0ms")
    b += t(col(0), 66, "© 2026 Malinga Pasindu", 12, 400, "rise", extra=d(240))
    b += t(col(4), 66, "Set in Helvetica Neue on a 12-column grid.", 12, 400, "m rise", extra=d(300))
    b += t(END, 66, "Probably Batman.", 12, 400, "m rise", "end", extra=d(360))
    return svg(W, 96, b, "© 2026 Malinga Pasindu. Probably Batman.")


def main():
    OUT.mkdir(exist_ok=True)
    panels = {
        "hero.svg": hero(),
        "profile.svg": profile(),
        "capabilities.svg": capabilities(),
        "contact.svg": contact(),
        "footer.svg": footer(),
    }
    for name, content, pct in link_buttons():
        panels[name] = content
        print(f"{name}: width {pct:.3f}%")
    for name, content in panels.items():
        (OUT / name).write_text(content, encoding="utf-8")
    print(f"Wrote {len(panels)} files to {OUT}")


if __name__ == "__main__":
    main()
