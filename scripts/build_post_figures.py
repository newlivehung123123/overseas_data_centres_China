#!/usr/bin/env python3
#!/usr/bin/env python3
"""Draw the four figures of the post "Where Chinese AI firms rent the chips they cannot buy" from the checked files.

The figures are in black, white and grey and carry no titles, because the post gives each figure a caption with its
source and a note. Figure 1 reads Epoch AI's database file in data/raw/epoch, which scripts/fetch_epoch.py downloads.
Figure 3 codes the rows of data/rules.csv by hand against four links, from the export of a chip to its use from
China, and the script stops if a row of data/rules.csv is missing from the figure or the figure names a row that the
file does not hold. The folder docs/figures/post_v0.1.0 keeps the figures as the post published them, drawn from
version 0.1.0 of the dataset, and the script draws the same figures from the current files.

    python scripts/build_post_figures.py    writes docs/figures/figure_1_epoch.svg to docs/figures/figure_4_capacity.svg
"""

from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "docs" / "figures"

W = 760
FONT = "'Liberation Sans', Arial, Helvetica, sans-serif"
BLACK, DARK, MID, LIGHT, PALE, WHITE = "#1a1a1a", "#555555", "#8c8c8c", "#bdbdbd", "#e3e3e3", "#ffffff"


def rows(name):
    with (REPO / name).open(newline="") as f:
        return list(csv.DictReader(f))


def esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size=12, fill=BLACK, weight=400, anchor="start", extra=""):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" font-weight="{weight}" '
            f'text-anchor="{anchor}" {extra}>{esc(s)}</text>')


def line(x1, y1, x2, y2, width=1, colour=BLACK, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{colour}" stroke-width="{width}"{d}/>'


def rect(x, y, w, h, fill, stroke=BLACK, width=0.8):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(w, 0):.1f}" height="{h:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>'


def page(name, svg, height):
    OUT.mkdir(parents=True, exist_ok=True)
    out = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height:.0f}" viewBox="0 0 {W} {height:.0f}" font-family="{FONT}">
<rect width="{W}" height="{height:.0f}" fill="#ffffff"/>
<defs><pattern id="hatch" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
<rect width="5" height="5" fill="#ffffff"/><line x1="0" y1="0" x2="0" y2="5" stroke="{BLACK}" stroke-width="1"/></pattern></defs>
{svg}
</svg>
"""
    (OUT / f"{name}.svg").write_text(out)
    print(f"wrote {(OUT / f'{name}.svg').relative_to(REPO)}")


def x_axis(left, right, y, ticks, scale, label, fmt="{:,}"):
    out = [line(left, y, right, y)]
    for v in ticks:
        x = left + v * scale
        out.append(line(x, y, x, y + 5))
        out.append(text(x, y + 19, fmt.format(v), 11.5, anchor="middle"))
    out.append(text((left + right) / 2, y + 40, label, 12.5, anchor="middle"))
    return out


# Figure 1. IT power that Epoch AI estimates at the data centres outside the United States and mainland China.
def figure_1():
    dc = rows("data/raw/epoch/data_centers.csv")
    tl = rows("data/raw/epoch/data_center_timelines.csv")
    read_on = rows("data/epoch_estimates.csv")[0]["retrieved"]
    latest = {}
    for t in tl:
        if t["Date"] <= read_on and (t["Data center"] not in latest or t["Date"] > latest[t["Data center"]]["Date"]):
            latest[t["Data center"]] = t
    ours = {link["epoch_name"] for link in rows("data/epoch_links.csv")}
    data = [(d["Name"], d["Country"], float(latest[d["Name"]]["IT power (MW)"] or 0) if d["Name"] in latest else 0.0)
            for d in dc if d["Country"] not in ("United States", "China")]
    shown = sorted([x for x in data if x[2] > 0], key=lambda x: -x[2])
    left, right, top, row = 290, W - 40, 20, 30
    scale = (right - left) / 500
    base = top + row * len(shown) + 6
    svg = [line(left, top - 6, left, base)]
    for i, (name, country, mw) in enumerate(shown):
        y = top + i * row
        mine = name in ours
        svg.append(text(left - 8, y + 16, f"{name}, {country}", 12, anchor="end"))
        svg.append(rect(left, y + 5, mw * scale, 17, BLACK if mine else LIGHT, BLACK if mine else DARK, 0.6))
        svg.append(text(left + mw * scale + 5, y + 18, f"{mw:,.0f}", 11.5))
    svg += x_axis(left, right, base, range(0, 501, 100), scale, "IT power in service, October 2026 (MW)")
    lx, ly = right - 250, top + row * 6 + 10
    svg.append(rect(lx, ly, 250, 50, WHITE, BLACK, 0.6))
    svg.append(rect(lx + 10, ly + 10, 14, 10, BLACK, BLACK, 0.6) + text(lx + 32, ly + 19, "Site where a Chinese firm holds a role", 11.5))
    svg.append(rect(lx + 10, ly + 30, 14, 10, LIGHT, DARK, 0.6) + text(lx + 32, ly + 39, "Other data centre", 11.5))
    h = base + 52
    page("figure_1_epoch", "\n".join(svg), h)


# Figure 4. Low and high estimates of capacity.
def figure_4():
    est = rows("data/capacity_estimate.csv")
    parts = [("DayOne, figures by market", BLACK), ("Global Switch", MID), ("Other sites, primary source", PALE),
             ("Added in the high estimate only", "url(#hatch)")]

    def part(r):
        if r["counted_in"] == "high":
            return 3
        return {"DayOne": 0, "Global Switch": 1}.get(r["firm"], 2)

    bars = []
    for stage, name in (("in_service", "In service"), ("pipeline", "Under construction or planned")):
        for bound in ("low", "high"):
            seg = [0.0] * 4
            for r in est:
                if r["stage"] == stage and r["counted_in"] in ("both", bound):
                    seg[part(r)] += float(r["mw"])
            bars.append((name, "Low estimate" if bound == "low" else "High estimate", seg))
    left, right, top, bh = 110, W - 70, 34, 24
    scale = (right - left) / 6600
    ys = [top, top + 32, top + 104, top + 136]
    base = ys[-1] + bh + 12
    svg = [line(left, 8, left, base)]
    for (group, bound, seg), y in zip(bars, ys):
        if bound == "Low estimate":
            svg.append(text(left + 6, y - 9, group, 12, weight=700))
        svg.append(text(left - 8, y + 16, bound, 12, anchor="end"))
        x = left
        for i, mw in enumerate(seg):
            if mw <= 0:
                continue
            w = mw * scale
            svg.append(rect(x, y, w, bh, parts[i][1], BLACK, 0.7))
            if w > 40:
                if i == 3:
                    svg.append(f'<rect x="{x + w / 2 - 17:.1f}" y="{y + 5:.1f}" width="34" height="15" fill="#ffffff"/>')
                svg.append(text(x + w / 2, y + 16.5, f"{mw:,.0f}", 11, WHITE if i == 0 else BLACK, anchor="middle"))
            x += w
        svg.append(text(x + 6, y + 16.5, f"{sum(seg):,.0f}", 12, weight=700))
    svg += x_axis(left, right, base, range(0, 6001, 1000), scale, "Capacity (MW)")
    ly = base + 58
    lx = 24
    for name, fill in parts:
        svg.append(rect(lx, ly, 14, 10, fill, BLACK, 0.7) + text(lx + 20, ly + 9.5, name, 11.5))
        lx += 20 + len(name) * 6.1 + 22
    h = ly + 24
    page("figure_4_capacity", "\n".join(svg), h)


# Figure 3. The rules recorded against the four links from the shipment of a chip to its use from China.
def figure_3():
    cols = ["Export or\nre-export", "Transit or\ntransshipment", "Use in the\nhost country", "Remote access\nfrom China"]
    # Each row: the rows of data/rules.csv it shows, the jurisdiction, the instrument as the figure names it, and the
    # mark for each link. F in force, N not binding (a bill, an announcement, a review or guidance), R rescinded or
    # shelved, X the source states that the link is not controlled, P binds named parties only.
    coded = [
        ("USA-0001", "United States", "Export Administration Regulations", "F", "", "", "X"),
        ("USA-0003", "", "AI Diffusion Rule, January 2025", "R", "", "", ""),
        ("USA-0004", "", "Licences for Malaysia and Thailand, announced May 2025", "N", "", "", ""),
        ("USA-0009", "", "Draft rule on Malaysia and Thailand, shelved August 2026", "R", "", "", ""),
        ("USA-0005", "", "Guidance on training Chinese models with US chips, May 2025", "", "", "", "N"),
        ("USA-0006", "", "Approvals of exports to G42 and Humain, November 2025", "F", "", "", ""),
        ("USA-0007", "", "Licences for entities with a parent in China, May 2026", "F", "", "", ""),
        ("USA-0002", "", "Remote Access Security Act, passed the House January 2026", "", "", "", "N"),
        ("USA-0008", "", "BIS enforcement review of remote access, August 2026", "", "", "", "N"),
        ("USA-0010", "", "Draft rule on renting chips to Chinese firms abroad, reported August 2026", "", "", "", "N"),
        ("USA-0013", "", "Licences for advanced chips to five countries, November 2026", "F", "", "", ""),
        ("USA-0014", "", "Licences for data centres serving firms headquartered in China, November 2026", "", "", "", "F"),
        ("MYS-0001;MYS-0002", "Malaysia", "Strategic Trade Act permit, July 2025", "", "F", "X", ""),
        ("MYS-0003", "", "Trade ministry statement on AI servers, June 2025", "", "", "X", ""),
        ("SGP-0001", "Singapore", "Prosecutions for fraud on server suppliers", "", "P", "", ""),
        ("SGP-0002", "", "Advisory on export controls on advanced chips, April 2025", "N", "", "", ""),
        ("EUU-0001", "European Union", "Update of the Dual-Use Regulation, November 2025", "F", "", "", ""),
        ("ARE-0001", "United Arab Emirates", "Regulated Technology Environment, May 2025", "", "", "N", ""),
        ("NOR-0001", "Private contract or requirement", "Nscale's loan agreement with Macquarie, September 2025", "", "", "", "P"),
        ("USA-0011", "", "Nvidia's monitoring requirement for new cloud partners, November 2026", "", "", "P", ""),
        ("USA-0012", "", "Nvidia's 51 percent instruction to cloud partners, November 2026", "", "", "", "N"),
    ]
    shown = [i for c in coded for i in c[0].split(";")]
    recorded = [r["rule_id"] for r in rows("data/rules.csv")]
    if sorted(shown) != sorted(recorded):
        raise ValueError(f"Figure 3 and data/rules.csv differ: missing {sorted(set(recorded) - set(shown))}, "
                         f"unknown {sorted(set(shown) - set(recorded))}")
    body = [c[1:] for c in coded]
    left_j, left_i, colw, top, row = 16, 30, 86, 58, 22
    col0 = W - 16 - 4 * colw
    xs = [col0 + colw * k + colw / 2 for k in range(4)]
    svg = [line(left_j, 10, W - 16, 10, 1.4)]
    for k, c in enumerate(cols):
        for j, part in enumerate(c.split("\n")):
            svg.append(text(xs[k], 28 + 14 * j, part, 11.5, weight=700, anchor="middle"))
    svg.append(text(left_j, 42, "Instrument", 11.5, weight=700))
    svg.append(line(left_j, top - 8, W - 16, top - 8, 0.8))

    def mark(kind, x, y):
        s = 11
        if kind == "F":
            return rect(x - s / 2, y - s / 2, s, s, BLACK, BLACK, 0.8)
        if kind == "N":
            return rect(x - s / 2, y - s / 2, s, s, LIGHT, DARK, 0.8)
        if kind == "R":
            return rect(x - s / 2, y - s / 2, s, s, WHITE, BLACK, 0.9)
        if kind == "P":
            return rect(x - s / 2, y - s / 2, s, s, "url(#hatch)", BLACK, 0.9)
        if kind == "X":
            return line(x - 5, y - 5, x + 5, y + 5, 1.6) + line(x - 5, y + 5, x + 5, y - 5, 1.6)
        return ""

    y = top
    for i, (jur, inst, *marks) in enumerate(body):
        if jur:
            if i:
                y += 4
            svg.append(text(left_j, y + 8, jur, 11.5, weight=700))
            y += row
        svg.append(text(left_i, y + 8, inst, 11.5))
        for k, m in enumerate(marks):
            svg.append(mark(m, xs[k], y + 4))
        y += row
    svg.append(line(left_j, y - 4, W - 16, y - 4, 1.4))
    # light shading of the column of remote access, in which no rule in force applies to all firms
    svg.insert(0, f'<rect x="{col0 + colw * 3:.1f}" y="10" width="{colw:.1f}" height="{y - 14:.1f}" fill="#efefef"/>')
    ly = y + 14
    legend = [("F", "In force, controls the link"), ("N", "Not binding: bill, announcement, review or guidance"),
              ("P", "Binds named parties only"), ("R", "Rescinded or shelved"),
              ("X", "Source states that the link is not controlled")]
    for n, (kind, name) in enumerate(legend):
        lx = left_j + (0 if n % 2 == 0 else 330)
        yy = ly + 18 * (n // 2)
        svg.append(mark(kind, lx + 6, yy + 4) + text(lx + 18, yy + 8, name, 11))
    lrow = (len(legend) - 1) // 2
    h = ly + 18 * (lrow + 1) + 8
    page("figure_3_rules", "\n".join(svg), h)


# Figure 2. IT power at the 4 sites over time, from Epoch AI's timelines.
def figure_2():
    tl = rows("data/epoch_timelines.csv")
    order = [("MYS-0001", "MY06, Johor (ByteDance as anchor tenant)", DARK), ("IDN-0002", "Nongsa, Batam (DayOne)", MID),
             ("MYS-0003", "Nusajaya, Johor (DayOne)", LIGHT), ("MYS-0004", "Kempas, Johor (DayOne)", PALE)]
    series = {sid: sorted((date.fromisoformat(t["date"]), float(t["it_power_mw"])) for t in tl if t["site_id"] == sid)
              for sid, _, _ in order}
    start, end = date(2022, 1, 1), date.fromisoformat(rows("data/epoch_estimates.csv")[0]["retrieved"])
    days = sorted({d for s in series.values() for d, _ in s if d >= start} | {start, end})

    def value(sid, d):
        v = 0.0
        for when, mw in series[sid]:
            if when <= d:
                v = mw
        return v

    left, right, top, ph = 70, W - 30, 16, 300
    ymax = 1250

    def X(d):
        return left + (d - start).days / (end - start).days * (right - left)

    def Y(v):
        return top + ph - v / ymax * ph

    svg = []
    below = {d: 0.0 for d in days}
    for sid, label, fill in order:
        upper, lower = [], []
        for i, d in enumerate(days[:-1]):
            v = value(sid, d)
            for dd in (d, days[i + 1]):
                lower.append((X(dd), Y(below[d])))
                upper.append((X(dd), Y(below[d] + v)))
        pts = upper + lower[::-1]
        svg.append(f'<path d="M' + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f' Z" fill="{fill}" stroke="{BLACK}" stroke-width="0.6"/>')
        for d in days:
            below[d] += value(sid, d)
    svg.append(line(left, top, left, top + ph) + line(left, top + ph, right, top + ph))
    for v in range(0, ymax + 1, 250):
        svg.append(line(left - 5, Y(v), left, Y(v)) + text(left - 9, Y(v) + 4, f"{v:,}", 11.5, anchor="end"))
    svg.append(text(18, top + ph / 2, "IT power in service (MW)", 12.5, anchor="middle", extra=f'transform="rotate(-90 18 {top + ph / 2})"'))
    for yr in range(2022, 2027):
        x = X(date(yr, 1, 1))
        svg.append(line(x, top + ph, x, top + ph + 5) + text(x, top + ph + 19, str(yr), 11.5, anchor="middle"))
    total = below[end] if end in below else sum(value(s, end) for s, _, _ in order)
    svg.append(text(X(end) - 14, Y(total) + 10, f"{total:,.0f} MW in all", 11.5, weight=700, anchor="end"))
    lx, ly = left + 16, top + 12
    svg.append(rect(lx, ly, 340, 92, WHITE, BLACK, 0.6))
    for i, (sid, label, fill) in enumerate(order[::-1]):
        y = ly + 12 + 19 * i
        svg.append(rect(lx + 10, y, 14, 10, fill, BLACK, 0.6) + text(lx + 32, y + 9.5, f"{label}, {value(sid, end):,.0f} MW", 11.5))
    h = top + ph + 34
    page("figure_2_growth", "\n".join(svg), h)


if __name__ == "__main__":
    figure_1()
    figure_2()
    figure_3()
    figure_4()
