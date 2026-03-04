#!/usr/bin/env python3
"""3D ocean: art-directed wave rendering with high contrast."""

import math
import random
import unicodedata

W = 72
H = 20
canvas = [[' '] * W for _ in range(H)]
random.seed(71)

HORIZON = 4
FOV_X = 1.8


# ── Render ocean ─────────────────────────────────────────────────
for sy in range(HORIZON + 1, H):
    t = (sy - HORIZON) / (H - 1 - HORIZON)

    # Phase mapping: ~5 wave crests, compressed near horizon
    row_phase = (1 - t) ** 0.55 * 10 * math.pi

    dom_val = math.sin(row_phase)

    # Distance for cross-wave world coords
    dist = 2.5 / (t + 0.01)

    for sx in range(W):
        world_x = (sx - W / 2.0) * dist * FOV_X / W

        # Cross-wave texture (horizontal variation within each band)
        cross = 0.0
        cross += 0.20 * math.sin(0.3 * world_x + row_phase * 0.35 + 1.0)
        cross += 0.15 * math.sin(0.55 * world_x - row_phase * 0.25 + 2.5)
        cross += 0.10 * math.sin(0.9 * world_x + row_phase * 0.15 + 4.0)
        cross += 0.06 * math.sin(1.4 * world_x - row_phase * 0.1 + 0.5)

        h = dom_val + cross

        # Height → character: high contrast between crests and troughs
        r = random.random()
        if h > 0.65:
            ch = '~'                                        # solid crest
        elif h > 0.30:
            ch = '~' if r > 0.12 else ':'                   # crest edge
        elif h > 0.0:
            ch = ':' if r > 0.10 else '~'                   # upper slope
        elif h > -0.30:
            ch = ';' if r > 0.08 else ':'                   # lower slope
        elif h > -0.60:
            ch = '.' if r > 0.15 else (' ' if r > 0.07 else ';')
        else:
            ch = '.' if r > 0.35 else (' ' if r > 0.10 else ';')

        # Fog near horizon: override distant pixels
        fog = max(0.0, (dist - 35) / 200)
        if fog > 0 and random.random() < fog:
            ch = ';' if random.random() > 0.3 else ':'

        canvas[sy][sx] = ch

# ── Horizon ──────────────────────────────────────────────────────
for sx in range(W):
    canvas[HORIZON][sx] = '~'

# ── Stars ────────────────────────────────────────────────────────
for _ in range(10):
    sx = random.randint(0, W - 1)
    sy = random.randint(0, HORIZON - 2)
    if canvas[sy][sx] == ' ':
        canvas[sy][sx] = random.choice(['.', '·', '✦', '˚', '*'])

# ── Output ───────────────────────────────────────────────────────
art = [''.join(row) for row in canvas]

for i, line in enumerate(art):
    assert len(line) == W, f"Line {i}: len={len(line)}"
    dw = sum(
        2 if unicodedata.east_asian_width(c) in ('W', 'F') else 1
        for c in line
    )
    assert dw == W, f"Line {i}: dw={dw}"

print(f"✓ {len(art)} lines, {W} chars\n")
for line in art:
    print(line)

readme = '```\n' + '\n'.join(art) + '\n```\n'
readme += """
- **Head of AI** @ [Quadrivia](https://quadrivia.ai)
- **13 years** in ML & AI
- **Voice AI** for healthcare
- **Prompt optimization**
- **Serial startup builder**

---

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/eherreros/)
[![X](https://img.shields.io/badge/X-000000?style=flat&logo=x&logoColor=white)](https://twitter.com/eherrerosj)
[![Web](https://img.shields.io/badge/bull--labs.com-FF6F00?style=flat&logo=googlechrome&logoColor=white)](https://bull-labs.com)

<img align="right" src="https://visitor-badge.laobi.icu/badge?page_id=eherrerosj.visitor-badge">
"""

with open('/tmp/eherrerosj-profile/README.md', 'w') as f:
    f.write(readme)
print("\nREADME.md written!")
