"""Step 05 figure: how the Pt start structures are chosen (sites, heights, spacing rule, symmetry).
Run:  python3 assets/fig_step05_start_rules.py   (writes assets/fig_step05_start_rules.png)"""
import math, os, sys, importlib.util
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
import plotstyle as ps
spec = importlib.util.spec_from_file_location("s05", os.path.join(HERE, "..", "05_Ptn_small", "setup.py"))
s05 = importlib.util.module_from_spec(spec); spec.loader.exec_module(s05)
ps.apply()
a = 3.1514
g = s05.geometry(a); mic = s05.tools(g)[3]; Z = g["Z"]; zs = Z["vac"] - 0.30
SITE = {"vac": ("#0d366b", "o", "in vacancy"), "Mo": (ps.D3, "^", "Mo-top"),
        "hol": ("#1baf7a", "s", "hollow"), "S": ("#eda100", "D", "S-top")}
GREY, RED = "#cfcec6", "#c0392b"

def lattice(ax, c, R, vac=(), mo_marker=True):
    for k, p in enumerate(g["s_top"]):
        d = mic(c, p)
        if abs(d[0]) < R and abs(d[1]) < R:
            if k in vac: ax.add_patch(Circle(d, 0.42, fill=False, ec=RED, lw=1.3, zorder=2))
            else: ax.add_patch(Circle(d, 0.30, color=GREY, lw=0, zorder=1))
    if mo_marker:
        for p in g["mo"]:
            d = mic(c, p)
            if abs(d[0]) < R and abs(d[1]) < R: ax.plot(*d, "s", ms=2.2, color="#9a998f", mew=0, zorder=1)
    ax.set_xlim(-R, R); ax.set_ylim(-R, R); ax.set_aspect("equal"); ax.axis("off")

fig = plt.figure(figsize=(7.2, 6.4))
# ---- A: candidate sites around a vacancy
ax = fig.add_axes([0.01, 0.50, 0.46, 0.44]); c = g["s0"]; vac = [g["ks"]]; R = 5.2
lattice(ax, c, R, vac)
ax.add_patch(Circle((0, 0), s05.R_SITE, fill=False, ec=ps.MUTED, lw=0.9, ls=(0, (4, 3))))
ax.text(0, -s05.R_SITE - 0.35, "3.3 Å", ha="center", va="top", fontsize=7.5, color=ps.MUTED)
for kind, pts in (("Mo", g["mo"]), ("hol", g["hol"]), ("S", [p for k, p in enumerate(g["s_top"]) if k not in vac])):
    for p in pts:
        d = mic(c, p)
        if math.hypot(*d) <= s05.R_SITE + 1e-6:
            col, m, _ = SITE[kind]; ax.plot(*d, m, ms=6.5, color=col, mec="white", mew=0.6, zorder=3)
col, m, _ = SITE["vac"]; ax.plot(0, 0, m, ms=7.5, color=col, mec="white", mew=0.6, zorder=3)
ax.set_title("A   Candidate Pt sites: within 3.3 Å of a vacancy", loc="left", fontsize=9, pad=2)
for i, (kind, (col, m, lab)) in enumerate(SITE.items()):
    ax.plot([], [], m, color=col, ms=6, label=lab)
ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.12), ncol=4, frameon=False, fontsize=7.5, handletextpad=0.2, columnspacing=0.9)

# ---- B: starting heights (side view)
ax = fig.add_axes([0.56, 0.55, 0.42, 0.37])
ax.plot([-0.6, 3.6], [0, 0], color=GREY, lw=6, solid_capstyle="butt"); ax.text(3.75, 0, "top S plane", va="center", fontsize=7.5, color=ps.MUTED)
ax.plot([-0.6, 3.6], [-1.565, -1.565], color="#9a998f", lw=3, solid_capstyle="butt"); ax.text(3.75, -1.565, "Mo plane", va="center", fontsize=7.5, color=ps.MUTED)
for i, kind in enumerate(["vac", "Mo", "hol", "S"]):
    h = Z[kind] - zs; col, m, lab = SITE[kind]
    ax.plot(i, h, "o", ms=11, color=col, mec="white", mew=0.8, zorder=3)
    ax.plot([i, i], [0 if kind != "vac" else -0.4, h], color=col, lw=0.8, ls=":", zorder=2)
    ax.text(i, h + 0.33, "%+.2f Å" % h, ha="center", fontsize=7.5)
    ax.text(i, -2.25, lab, ha="center", va="top", fontsize=7.5)
ax.set_xlim(-0.6, 5.3); ax.set_ylim(-2.9, 3.0); ax.axis("off")
ax.set_title("B   Starting height above the S plane (from step-03 relaxations)", loc="left", fontsize=9, pad=2)

# ---- C: spacing rule
ax = fig.add_axes([0.03, 0.06, 0.42, 0.36]); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 6.6)
ax.set_title("C   Pt–Pt spacing: neighbours on sites 1.82 Å apart are lifted", loc="left", fontsize=9, pad=2)
ax.plot([0.3, 4.4], [1.2, 1.2], color=GREY, lw=5, solid_capstyle="butt")
for x in (1.0, 4.0): ax.plot(x, 1.95, "o", ms=12, color=ps.D3, mec="white")
ax.annotate("", (1.25, 2.6), (3.75, 2.6), arrowprops=dict(arrowstyle="<->", color=ps.INK, lw=0.8))
ax.text(2.5, 2.8, "3.15 Å: both stay\nat site height", ha="center", va="bottom", fontsize=7.5)
ax.plot([5.6, 9.7], [1.2, 1.2], color=GREY, lw=5, solid_capstyle="butt")
x1, x2 = 6.6, 6.6 + 1.82 * 1.1; h2 = 1.95 + math.sqrt(2.5 ** 2 - 1.82 ** 2) * 1.1
ax.plot(x1, 1.95, "o", ms=12, color="#0d366b", mec="white")
ax.plot(x2, 1.95, "o", ms=12, color=ps.D3, mec="white", alpha=0.25)
ax.plot(x2, h2, "o", ms=12, color=ps.PBE, mec="white")
ax.add_patch(FancyArrowPatch((x2, 2.25), (x2, h2 - 0.3), arrowstyle="-|>", mutation_scale=8, color=ps.MUTED, lw=0.8))
ax.plot([x1, x2], [1.95, h2], color=ps.INK, lw=0.7, ls="--")
ax.text((x1 + x2) / 2 - 0.15, (1.95 + h2) / 2 + 0.25, "2.5 Å", ha="right", fontsize=7.5)
ax.text((x1 + x2) / 2, 0.55, "1.82 Å in plane", ha="center", fontsize=7.5)
ax.text(8.0, h2 + 0.55, "lifted", ha="center", fontsize=7.5, color=ps.PBE)
ax.text(0.2, 5.6, "Clusters must be connected (Pt–Pt ≤ 3.7 Å).\nVacancies are filled first for n ≥ 2 (each gains ~2.5 eV).",
        fontsize=7.5, color=ps.INK, va="top")

# ---- D: symmetry merge example
ax = fig.add_axes([0.53, 0.06, 0.44, 0.36]); R = 4.6
lattice(ax, c, R, vac, mo_marker=False)
col, m, _ = SITE["vac"]; ax.plot(0, 0, "o", ms=9, color=col, mec="white", zorder=4)
nb = [mic(c, p) for k, p in enumerate(g["s_top"]) if k != g["ks"] and abs(math.hypot(*mic(c, p)) - a) < 0.01]
for i, d in enumerate(sorted(nb, key=lambda d: math.atan2(d[1], d[0]))):
    ax.plot(*d, "o", ms=9, color=ps.D3 if i == 0 else ps.D3, alpha=1.0 if i == 0 else 0.25, mec="white", zorder=4)
d0 = sorted(nb, key=lambda d: math.atan2(d[1], d[0]))[0]
ax.text(d0[0], d0[1] - 0.75, "kept", ha="center", va="top", fontsize=7.5, color=ps.D3)
ax.text(0, -R + 0.2, "6 equivalent second-Pt positions → 1 start kept", ha="center", fontsize=7.5)
ax.set_title("D   Symmetry: copies related by rotation or mirror are merged", loc="left", fontsize=9, pad=2)
fig.savefig(os.path.join(HERE, "fig_step05_start_rules.png")); print("ok")
