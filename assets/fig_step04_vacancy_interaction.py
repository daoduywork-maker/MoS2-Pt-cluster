"""Step 04 figure: vacancy interaction energy per structure, with a top-view sketch under each bar.
Run:  python3 assets/fig_step04_vacancy_interaction.py   (writes assets/fig_step04_vacancy_interaction.png)"""
import math, os
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import plotstyle as ps
ps.apply()
HERE = os.path.dirname(os.path.abspath(__file__))

r3 = math.sqrt(3)
# (label, E_int PBE+D3, E_int plain PBE, vacancy offsets in units of a, vertical?, Mo marker)
DATA = [
    ("1nn\n3.15 Å",   -0.049, -0.032, [(0, 0), (1, 0)],              False, None),
    ("2nn\n5.46 Å",   +0.007, +0.013, [(0, 0), (1.5, r3 / 2)],       False, None),
    ("3nn\n6.30 Å",   +0.044, +0.051, [(0, 0), (2, 0)],              False, None),
    ("far\n10.9 Å",   +0.028, +0.034, [(0, 0), (3, r3)],             False, None),
    ("vertical\npair", -0.071, -0.031, [(0, 0)],                     True,  None),
    ("row\nof 3",     -0.155, -0.124, [(0, 0), (1, 0), (2, 0)],      False, None),
    ("triangle\nof 3", +0.189, +0.247, [(0, 0), (1, 0), (0.5, r3 / 2)], False, (0.5, r3 / 6)),
]
NOISE = 0.03

fig = plt.figure(figsize=(7.0, 3.9))
ax = fig.add_axes([0.09, 0.36, 0.89, 0.60])
n = len(DATA); w = 0.36
ax.axhspan(-NOISE, NOISE, color=ps.GRID, alpha=0.5, lw=0, zorder=0)
ax.text(2.0, -NOISE - 0.006, "noise ±0.03 eV", ha="center", va="top", fontsize=7, color=ps.MUTED)
ax.axhline(0, color=ps.MUTED, lw=0.8, zorder=1)
for i, (_, d3, pbe, *_r) in enumerate(DATA):
    ax.bar(i - w / 2 - 0.01, d3, w, color=ps.D3, zorder=2, label="PBE+D3" if i == 0 else None)
    ax.bar(i + w / 2 + 0.01, pbe, w, color=ps.PBE, zorder=2, label="plain PBE" if i == 0 else None)
    ax.text(i - w / 2 - 0.01, d3 + (0.008 if d3 >= 0 else -0.008), "%+.2f" % d3, ha="center",
            va="bottom" if d3 >= 0 else "top", fontsize=6.5, color=ps.INK)
ax.set_xlim(-0.6, n - 0.4); ax.set_ylim(-0.20, 0.28)
ax.set_xticks(range(n)); ax.set_xticklabels([d[0] for d in DATA])
ax.tick_params(axis="x", length=0, pad=4)
ax.set_ylabel("Interaction energy (eV)\n← attract    repel →")
ax.axvline(4.5, color=ps.GRID, lw=0.8, ls=(0, (3, 3)), zorder=0)
ax.text(1.5, 0.265, "pairs (top layer)", ha="center", fontsize=8, color=ps.MUTED)
ax.text(5.5, 0.265, "vertical pair and triplets", ha="center", fontsize=8, color=ps.MUTED)
ax.legend(loc="upper left", frameon=False, bbox_to_anchor=(0.0, 0.93))

# top-view sketches: top-layer S lattice (grey dots), removed S (open rings), Mo (black square)
x0, x1 = ax.get_position().x0, ax.get_position().x1
for i, (_, _, _, vac, vert, mo) in enumerate(DATA):
    xc = x0 + (x1 - x0) * (i + 0.6) / (n + 0.2)
    sx = fig.add_axes([xc - 0.058, 0.02, 0.116, 0.20]); sx.set_aspect("equal"); sx.axis("off")
    cx = sum(p[0] for p in vac) / len(vac); cy = sum(p[1] for p in vac) / len(vac)
    R = 2.2 if max(math.hypot(p[0] - cx, p[1] - cy) for p in vac) < 1.2 else 2.6
    if i == 3: R = 2.4
    for a in range(-8, 9):
        for b in range(-8, 9):
            x, y = a - 0.5 * b, b * r3 / 2
            if any(abs(x - p[0]) < 1e-6 and abs(y - p[1]) < 1e-6 for p in vac): continue
            if math.hypot(x - cx, y - cy) <= R: sx.add_patch(Circle((x, y), 0.17, color="#b8b7af", lw=0))
    for p in vac:
        sx.add_patch(Circle(p, 0.30, fill=False, ec="#c0392b", lw=1.3))
        if vert: sx.add_patch(Circle(p, 0.13, color="#c0392b", lw=0))
    if mo: sx.plot(*mo, marker="s", ms=3.5, color=ps.INK)
    sx.set_xlim(cx - R - 0.4, cx + R + 0.4); sx.set_ylim(cy - R - 0.4, cy + R + 0.4)
fig.text(0.09, 0.235, "Top view:  ● S   ○ removed S   ◉ top and bottom S removed   ■ Mo",
         fontsize=7, color=ps.MUTED)
out = os.path.join(HERE, "fig_step04_vacancy_interaction.png")
fig.savefig(out); print("wrote", out)
