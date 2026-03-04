#!/usr/bin/env python3
"""Ocean waves using the classic rolling ASCII wave pattern with perspective."""

import random
import unicodedata

W = 72
H = 20
canvas = [[' '] * W for _ in range(H)]
random.seed(42)

SKY_ROWS = 5
# Classic ASCII wave cycle (16 chars: trough _ through crest ^ and back)
WAVE = ",.-=~'`^`'~=-.,_"
WL = len(WAVE)

# ── Stars ────────────────────────────────────────────────────────
for _ in range(10):
    sx = random.randint(0, W - 1)
    sy = random.randint(0, SKY_ROWS - 2)
    if canvas[sy][sx] == ' ':
        canvas[sy][sx] = random.choice(['.', '·', '✦', '˚', '*'])

# ── Ocean with perspective ───────────────────────────────────────
ocean_rows = H - SKY_ROWS
for row_idx in range(SKY_ROWS, H):
    ri = row_idx - SKY_ROWS
    t = ri / max(1, ocean_rows - 1)  # 0 = horizon, 1 = foreground

    # Perspective: wave period grows from ~10 cols (horizon) to ~30 cols (near)
    scale = 0.6 + 1.6 * t

    # Gentle diagonal flow (waves approaching viewer)
    offset = ri * 0.6

    for col in range(W):
        phase = (col / scale + offset) % WL
        ch = WAVE[int(phase) % WL]
        canvas[row_idx][col] = ch

    # Prevent 3+ consecutive backticks (breaks markdown code fences)
    row_str = canvas[row_idx]
    for col in range(2, W):
        if row_str[col] == '`' and row_str[col - 1] == '`' and row_str[col - 2] == '`':
            row_str[col] = "'"

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
