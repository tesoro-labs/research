"""Generate the paper's figures as standalone SVG files.

Each figure is drawn from data written out below or read from a sealed record, so a figure can be
regenerated and checked rather than redrawn by hand. Layout follows the diagram-design conventions
(cathrynlavery/diagram-design, MIT): orthogonal connectors, masked arrow labels with a gap, one or
two accent elements, a legend strip at the bottom, an accessible <title>/<desc>. The skin is a
print variant: white paper and system fonts, so the PDF renders the same offline.

    python paper/figures/make_figures.py
"""

from __future__ import annotations

import json
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).resolve().parent
EXP007 = HERE.parents[2] / "aegs" / "research" / "experiments" / "EXP-007" / "results.json"

PAPER = "#ffffff"
INK = "#1f2430"
MUTED = "#4f5d75"
SOFT = "#5a6580"
RULE = "rgba(31,36,48,0.14)"
ACCENT = "#bf4520"
ACCENT_TINT = "rgba(191,69,32,0.08)"

SERIF = "Charter, 'Bitstream Charter', Georgia, Cambria, serif"
SANS = "'Segoe UI', system-ui, -apple-system, Helvetica, Arial, sans-serif"
MONO = "'Cascadia Mono', Consolas, ui-monospace, Menlo, monospace"


def svg(slug: str, width: int, height: int, title: str, desc: str, body: list[str]) -> str:
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" '
        f'height="{height}" role="img" aria-labelledby="{slug}-title {slug}-desc">',
        f'<title id="{slug}-title">{escape(title)}</title>',
        f'<desc id="{slug}-desc">{escape(desc)}</desc>',
        "<defs>",
        f'<marker id="{slug}-arrow" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">'
        f'<polygon points="0 0, 8 3, 0 6" fill="{MUTED}"/></marker>',
        f'<marker id="{slug}-arrow-accent" markerWidth="8" markerHeight="6" refX="7" refY="3" '
        f'orient="auto"><polygon points="0 0, 8 3, 0 6" fill="{ACCENT}"/></marker>',
        "</defs>",
        f'<rect width="100%" height="100%" fill="{PAPER}"/>',
        *body,
        "</svg>",
    ]) + "\n"


def text(x, y, s, size=9, fill=INK, family=SANS, anchor="middle", weight=400, spacing=None,
         italic=False):
    extra = f' letter-spacing="{spacing}"' if spacing else ""
    style = ' font-style="italic"' if italic else ""
    return (f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" font-family="{family}" '
            f'font-weight="{weight}" text-anchor="{anchor}"{extra}{style}>{escape(s)}</text>')


def label(x, y_line, s, above=True):
    """Arrow label: masked, all caps, with a 6px gap from its stroke."""
    w = round(len(s) * 0.62 * 8 + 12)
    top = y_line - 20 if above else y_line + 8
    return [
        f'<rect x="{x - w / 2}" y="{top}" width="{w}" height="12" rx="2" fill="{PAPER}"/>',
        text(x, top + 9, s, size=8, fill=SOFT, family=MONO, spacing="0.06em"),
    ]


def node(x, y, w, h, name, sub, focal=False):
    stroke = ACCENT if focal else INK
    fill = ACCENT_TINT if focal else PAPER
    return [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{PAPER}"/>',
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}" '
        f'stroke-width="1"/>',
        text(x + w / 2, y + h / 2 - 2, name, size=12, weight=600),
        text(x + w / 2, y + h / 2 + 14, sub, size=9, fill=MUTED, family=MONO),
    ]


def legend(y, width, items):
    out = [f'<line x1="30" y1="{y - 8}" x2="{width - 30}" y2="{y - 8}" stroke="{RULE}" '
           f'stroke-width="0.8"/>',
           text(30, y + 8, "LEGEND", size=8, fill=MUTED, family=MONO, anchor="start",
                spacing="0.14em")]
    out += items
    return out


# ── Figure 1: the x402 payment path and where a control can sit ─────────────────────────────

def figure_payment_path() -> str:
    slug, W, H = "fig-payment-path", 760, 560
    lanes = [("Agent", "LLM + tools", 80), ("x402 client", "wallet, signer", 230),
             ("Agent gateway", "MCP proxy", 380), ("Paid tool", "x402 seller", 530),
             ("Facilitator", "verify, settle", 680)]
    body = [text(30, 22, "WHERE A SPENDING CONTROL CAN SIT ON ONE x402 PAYMENT", size=8,
                 fill=MUTED, family=MONO, anchor="start", spacing="0.14em")]
    top, bottom = 36, 444
    for _, _, cx in lanes:  # lifelines first, so boxes and arrows sit over them
        body.append(f'<line x1="{cx}" y1="{top + 44}" x2="{cx}" y2="{bottom}" stroke="{RULE}" '
                    f'stroke-width="1" stroke-dasharray="4,4"/>')

    def msg(y, x1, x2, s, dashed=False, accent=False):
        color = ACCENT if accent else MUTED
        marker = f"{slug}-arrow-accent" if accent else f"{slug}-arrow"
        dash = ' stroke-dasharray="5,4"' if dashed else ""
        end = x2 - 6 if x2 > x1 else x2 + 6
        mid = (x1 + x2) / 2
        if abs(x1 - x2) > 300:  # long arrows: keep the label clear of the lifelines it crosses
            mid = 305
        return [f'<line x1="{x1}" y1="{y}" x2="{end}" y2="{y}" stroke="{color}" '
                f'stroke-width="1.2"{dash} marker-end="url(#{marker})"/>', *label(mid, y, s)]

    a, c, g, t, f = (lane[2] for lane in lanes)
    body += msg(120, a, t, "TOOLS/CALL")
    body += msg(164, t, a, "402 + PRICE", dashed=True, accent=True)
    body += msg(208, a, c, "SIGN PAYMENT")
    body += msg(252, c, a, "AUTHORIZATION", dashed=True)
    body += msg(296, a, t, "RETRY W/ PAY")
    body += msg(340, t, f, "VERIFY+SETTLE")
    body += msg(384, f, t, "SETTLED", dashed=True)
    body += msg(428, t, a, "RESULT+RECEIPT", dashed=True)

    for name, sub, cx in lanes:
        body += node(cx - 60, top, 120, 44, name, sub)

    def point(n, cx, y, focal=False):
        stroke = ACCENT if focal else INK
        return [f'<circle cx="{cx}" cy="{y}" r="9" fill="{PAPER}" stroke="{stroke}" '
                f'stroke-width="1.2"/>',
                text(cx, y + 3.5, str(n), size=9, weight=600, fill=stroke)]

    body += point(1, a, 120, focal=True)  # decides before the price exists
    body += point(2, c, 208)
    body += point(3, c, 252)
    body += point(4, g, 296)
    body += point(5, t, 164)
    body += point(6, f, 340)

    keys = [
        (1, "pre-tool hook: decides before any price exists"),
        (2, "client spend controls: price known, not yet signed"),
        (3, "custodial signer: can refuse to sign"),
        (4, "gateway: sees the signed amount in transit"),
        (5, "seller: sets the price (the price authority)"),
        (6, "facilitator: sees settlement, not intent"),
    ]
    items = []
    for i, (n, s) in enumerate(keys):
        col, row = i % 2, i // 2
        x, y = 110 + col * 330, 486 + row * 22
        items += [f'<circle cx="{x}" cy="{y - 3}" r="7" fill="{PAPER}" '
                  f'stroke="{ACCENT if n == 1 else INK}" stroke-width="1"/>',
                  text(x, y, str(n), size=8, weight=600, fill=ACCENT if n == 1 else INK),
                  text(x + 14, y, s, size=9, fill=INK, anchor="start")]
    body += legend(470, W, items)
    return svg(slug, W, H, "Where a spending control can sit on one x402 payment",
               "Sequence of one x402 payment between agent, x402 client, agent gateway, paid tool "
               "and facilitator, marking six places a spending control can act; the pre-tool hook "
               "acts before the seller has named a price.", body)


# ── Figure 2: same verdict, different attributed control ─────────────────────────────────────

def figure_attribution_tie() -> str:
    slug, W, H = "fig-attribution-tie", 760, 300
    body = [text(30, 22, "TWO CONTROLS BOTH REFUSE. ORDER DECIDES WHICH ONE THE RECORD NAMES.",
                 size=8, fill=MUTED, family=MONO, anchor="start", spacing="0.14em")]
    rows = [("ORDER A: BUDGET RUNS FIRST", 52, [("Budget envelope", "REJECT, narrows"),
                                                ("Sanctions screen", "REJECT, no change")],
             "budget"),
            ("ORDER B: SANCTIONS RUNS FIRST", 160, [("Sanctions screen", "REJECT, narrows"),
                                                    ("Budget envelope", "REJECT, no change")],
             "sanctions")]
    for eyebrow, y, controls, who in rows:
        body.append(text(40, y, eyebrow, size=8, fill=MUTED, family=MONO, anchor="start",
                         spacing="0.12em"))
        by = y + 12
        # arrows first: control 1 -> control 2 -> result, all on one horizontal line
        cy = by + 28
        body.append(f'<line x1="200" y1="{cy}" x2="254" y2="{cy}" stroke="{MUTED}" '
                    f'stroke-width="1.2" marker-end="url(#{slug}-arrow)"/>')
        body.append(f'<line x1="420" y1="{cy}" x2="474" y2="{cy}" stroke="{MUTED}" '
                    f'stroke-width="1.2" marker-end="url(#{slug}-arrow)"/>')
        body += node(40, by, 160, 56, *controls[0])
        body += node(260, by, 160, 56, *controls[1])
        body += node(480, by, 240, 56, "Verdict: REJECT", f"record names: {who}", focal=True)
    body.append(text(380, 272, "Same verdict both ways; a different control on the record. "
                     "A declared dispositive control (sanctions) removes the ambiguity.",
                     size=13, fill=INK, family=SERIF, italic=True))
    return svg(slug, W, H, "Same verdict, different attributed control",
               "Two evaluation orders of a budget envelope and a sanctions screen both reach "
               "REJECT, but the record attributes the refusal to whichever control ran first.",
               body)


# ── Figure 3: benchmark outcomes by attack class ─────────────────────────────────────────────

BENCHMARK = [  # from tesoro/redteam/baseline.json, live run 2026-10-23 identical
    ("Numeric", "RT-NUM", ["D"] * 5),
    ("Economic", "RT-ECON", ["U:RT-ECON-001", "D", "A:RT-ECON-003", "D"]),
    ("Evidence", "RT-EVID", ["D", "U:RT-EVID-002", "D", "D"]),
    ("Authority", "RT-AUTH", ["D"] * 5),
    ("Advisor", "RT-ADV", ["D"] * 2),
]


def figure_benchmark() -> str:
    slug, W, H = "fig-benchmark", 760, 330
    body = [text(30, 22, "20 ATTACKS, 5 CLASSES: 17 DEFENDED, 1 BY ACCIDENT, 2 OPEN", size=8,
                 fill=MUTED, family=MONO, anchor="start", spacing="0.14em")]
    x0, cell, gap = 150, 92, 4
    for i, (name, _, outcomes) in enumerate(BENCHMARK):
        y = 44 + i * 44
        body.append(text(x0 - 14, y + 20, name, size=12, weight=600, anchor="end"))
        for j, o in enumerate(outcomes):
            x = x0 + j * (cell + gap)
            kind, _, ident = o.partition(":")
            if kind == "D":
                body.append(f'<rect x="{x}" y="{y}" width="{cell}" height="28" rx="3" '
                            f'fill="rgba(79,93,117,0.30)"/>')
            elif kind == "A":
                body.append(f'<rect x="{x}" y="{y}" width="{cell}" height="28" rx="3" '
                            f'fill="{ACCENT}"/>')
                body.append(text(x + cell / 2, y + 18, ident, size=8, fill=PAPER, family=MONO))
            else:
                body.append(f'<rect x="{x + 0.5}" y="{y + 0.5}" width="{cell - 1}" height="27" '
                            f'rx="3" fill="{PAPER}" stroke="{INK}" stroke-width="1" '
                            f'stroke-dasharray="4,3"/>')
                body.append(text(x + cell / 2, y + 18, ident, size=8, fill=INK, family=MONO))
        defended = sum(1 for o in outcomes if o == "D")
        body.append(text(x0 + 5 * (cell + gap) + 12, y + 18, f"{defended}/{len(outcomes)}",
                         size=9, fill=MUTED, family=MONO, anchor="start"))
    items = [
        f'<rect x="110" y="282" width="18" height="10" rx="2" fill="rgba(79,93,117,0.30)"/>',
        text(134, 291, "defended by the control the attack targets", size=9, anchor="start"),
        f'<rect x="400" y="282" width="18" height="10" rx="2" fill="{ACCENT}"/>',
        text(424, 291, "defended by accident (a finding)", size=9, anchor="start"),
        f'<rect x="110.5" y="302.5" width="17" height="9" rx="2" fill="{PAPER}" stroke="{INK}" '
        f'stroke-dasharray="4,3"/>',
        text(134, 311, "undefended, open by design", size=9, anchor="start"),
    ]
    body += legend(272, W, items)
    return svg(slug, W, H, "Benchmark outcomes by attack class",
               "Twenty attacks in five classes; seventeen are defended by their target control, "
               "one trust-farming attack is refused by an unrelated control, and two remain open.",
               body)


# ── Figure 4: ten runs of the same latency measurement ──────────────────────────────────────

def figure_latency() -> str:
    data = json.loads(EXP007.read_text(encoding="utf-8"))["latencyP50Us"]
    runs, median = data["runs"], data["median"]
    slug, W, H = "fig-latency", 760, 260
    lo, hi, x0, x1 = 100, 350, 120, 720

    def X(v):
        return x0 + (v - lo) * (x1 - x0) / (hi - lo)

    body = [text(30, 22, "p50 DECISION LATENCY, TEN IDENTICAL RUNS (EXP-007), MICROSECONDS",
                 size=8, fill=MUTED, family=MONO, anchor="start", spacing="0.14em")]
    axis_y = 180
    body.append(f'<line x1="{x0}" y1="{axis_y}" x2="{x1}" y2="{axis_y}" stroke="{INK}" '
                f'stroke-width="1"/>')
    for v in range(lo, hi + 1, 50):
        body.append(f'<line x1="{X(v)}" y1="{axis_y}" x2="{X(v)}" y2="{axis_y + 5}" '
                    f'stroke="{INK}" stroke-width="1"/>')
        body.append(text(X(v), axis_y + 18, f"{v} µs", size=9, fill=MUTED, family=MONO))
    # median rule
    # stops above the single-run row so it never crosses that row's label
    body.append(f'<line x1="{X(median)}" y1="56" x2="{X(median)}" y2="118" stroke="{MUTED}" '
                f'stroke-width="1" stroke-dasharray="4,3"/>')
    body.append(text(X(median) + 6, 64, f"median {median:g} µs", size=9, fill=MUTED,
                     family=MONO, anchor="start"))
    body.append(text(x0 - 12, 104, "ten runs", size=12, weight=600, anchor="end"))
    placed: list[float] = []
    for v in runs:  # beeswarm: lift a dot that would overlap one already placed
        x, y = X(v), 100
        while any(abs(x - px) < 11 and abs(y - py) < 11 for px, py in placed):
            y -= 12
        placed.append((x, y))
        body.append(f'<circle cx="{x}" cy="{y}" r="5" fill="{MUTED}"/>')
    body.append(text(x0 - 12, 154, "one earlier run", size=12, weight=600, anchor="end"))
    body.append(f'<circle cx="{X(128)}" cy="150" r="5.5" fill="{ACCENT}"/>')
    body.append(text(X(128) + 12, 154, "128 µs, single run: below the minimum of all ten",
                     size=9, fill=ACCENT, family=MONO, anchor="start"))
    body.append(text(380, 236, f"Fastest and slowest of ten identical runs differ "
                     f"{data['spread']}×. One laptop, shared with other work.",
                     size=13, fill=INK, family=SERIF, italic=True))
    return svg(slug, W, H, "Ten runs of one latency measurement",
               f"Dot plot of p50 decision latency over ten identical runs, {min(runs)} to "
               f"{max(runs)} microseconds, with an earlier single-run figure of 128 microseconds "
               f"below all of them.", body)


def main() -> None:
    for name, make in [("payment-path", figure_payment_path),
                       ("attribution-tie", figure_attribution_tie),
                       ("benchmark", figure_benchmark), ("latency", figure_latency)]:
        out = HERE / f"{name}.svg"
        out.write_text(make(), encoding="utf-8", newline="\n")
        print(f"wrote {out.name}")


if __name__ == "__main__":
    main()
