# Build a custom stats SVG: left labels, middle progress bars with numbers, right rank ring
stats = [
    ("Total Stars",        0,   50),
    ("Commits (last yr)",  3,   100),
    ("Total PRs",          0,   50),
    ("PRs Reviewed",       0,   50),
    ("Total Issues",       0,   50),
    ("Contributed to",     0,   30),
]
rank_label = "Top"
rank_pct   = "99.9%"
ring_frac  = 0.999  # how full the ring looks (percentile)

BG="#0d1117"; ACCENT="#3FB950"; TXT="#c9d1d9"; TRACK="#1b2a20"; MUTED="#8b949e"
W=520; H=250
left_x=24; label_w=150
bar_x=left_x+label_w+6
bar_w=160
ring_cx=430; ring_cy=H//2+6; ring_r=46; stroke=9
row_top=78; row_gap=26

import math
def bar(y, val, mx):
    frac=min(val/mx,1.0) if mx else 0
    fw=max(4, bar_w*frac) if val>0 else 0
    s=f'<rect x="{bar_x}" y="{y-9}" width="{bar_w}" height="10" rx="5" fill="{TRACK}"/>'
    if fw>0:
        s+=f'<rect x="{bar_x}" y="{y-9}" width="{fw:.1f}" height="10" rx="5" fill="{ACCENT}"/>'
    return s

rows=[]
y=row_top
for name,val,mx in stats:
    rows.append(f'<text x="{left_x}" y="{y}" font-size="13" fill="{TXT}">{name}</text>')
    rows.append(bar(y,val,mx))
    rows.append(f'<text x="{bar_x+bar_w+10}" y="{y}" font-size="13" font-weight="700" fill="{ACCENT}">{val}</text>')
    y+=row_gap

circ=2*math.pi*ring_r
dash=circ*ring_frac
ring=f'''<circle cx="{ring_cx}" cy="{ring_cy}" r="{ring_r}" fill="none" stroke="{TRACK}" stroke-width="{stroke}"/>
<circle cx="{ring_cx}" cy="{ring_cy}" r="{ring_r}" fill="none" stroke="{ACCENT}" stroke-width="{stroke}" stroke-linecap="round"
 stroke-dasharray="{dash:.1f} {circ:.1f}" transform="rotate(-90 {ring_cx} {ring_cy})"/>
<text x="{ring_cx}" y="{ring_cy-4}" font-size="15" font-weight="700" fill="{TXT}" text-anchor="middle">{rank_label}</text>
<text x="{ring_cx}" y="{ring_cy+16}" font-size="15" font-weight="700" fill="{TXT}" text-anchor="middle">{rank_pct}</text>'''

svg=f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Ubuntu, sans-serif">
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="{BG}" stroke="#20292f"/>
<text x="{left_x}" y="38" font-size="17" font-weight="700" fill="{ACCENT}">ネオン's GitHub Stats</text>
<line x1="{left_x}" y1="52" x2="{bar_x+bar_w+40}" y2="52" stroke="#20292f"/>
{''.join(rows)}
{ring}
</svg>'''
open("assets/stats.svg","w").write(svg)
print("stats.svg written", len(svg))
