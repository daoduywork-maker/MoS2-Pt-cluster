"""Step 05 figure: every screening start (top view), by substrate.
Run:  python3 assets/fig_step05_starts.py   (writes assets/fig_step05_starts.png)"""
import math, os, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
spec = importlib.util.spec_from_file_location("s05", os.path.join(HERE, "..", "05_Ptn_small", "setup.py")); s05 = importlib.util.module_from_spec(spec); spec.loader.exec_module(s05)
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.lines import Line2D
import plotstyle as ps
ps.apply()
a = 3.1514
g, cf = s05.enumerate_all(a); subs = s05.substrates(g, a)
mic = s05.tools(g)[3]
mo, s_top = g["mo"], g["s_top"]
ORDER = ["P", "V1", "V2_1nn", "V3_row", "V3_tri"]
TITLE = {"P": "Pristine (P)", "V1": "Single vacancy (V1)", "V2_1nn": "Vacancy pair (V2_1nn)",
         "V3_row": "Row of 3 (V3_row)", "V3_tri": "Triangle of 3 (V3_tri)"}
COLS = 16; W = 0.62
LOW, MID, HIGH = "#0d366b", ps.D3, ps.PBE
rows = []
for s in ORDER:
    grp = [c for c in cf if c[0] == s]
    rows.append(("head", "%s  —  %d starts  (n = 1 / 2 / 3 / 4:  %s)%s" % (TITLE[s], len(grp),
                 " / ".join(str(sum(1 for c in grp if c[1] == n)) for n in range(1, 5)),
                 "   [Pt₁ on P done in step 03]" if s == "P" else ("   [Pt₁ in the vacancy done in step 03]" if s == "V1" else ""))))
    for i in range(0, len(grp), COLS): rows.append(("tiles", grp[i:i + COLS]))
FW = COLS * W + 0.3
H = sum(0.3 if r[0] == "head" else W + 0.16 for r in rows) + 0.6
fig = plt.figure(figsize=(FW, H)); y = H - 0.6
fig.text(0.01, 1 - 0.18 / H, "Step 05: all %d screening starts (top view, 10 Å window)" % len(cf), fontsize=11, weight="bold")
hd = [Line2D([], [], ls="", marker="o", ms=4, color="#cfcec6", label="S (top layer)"),
      Line2D([], [], ls="", marker="o", ms=6, mfc="none", mec="#c0392b", label="S vacancy"),
      Line2D([], [], ls="", marker="s", ms=3, color="#9a998f", label="Mo"),
      Line2D([], [], ls="", marker="o", ms=7, color=LOW, label="Pt in vacancy"),
      Line2D([], [], ls="", marker="o", ms=7, color=MID, label="Pt on surface site"),
      Line2D([], [], ls="", marker="o", ms=7, color=HIGH, label="Pt raised to keep Pt–Pt ≥ 2.5 Å")]
fig.legend(handles=hd, loc="upper left", bbox_to_anchor=(0.005, 1 - 0.27 / H), ncol=6, frameon=False, fontsize=8)
for r in rows:
    if r[0] == "head":
        y -= 0.3; fig.text(0.01, (y + 0.03) / H, r[1], fontsize=9, weight="bold"); continue
    y -= W + 0.16
    for j, (s, n, idx, pts) in enumerate(r[1]):
        ax = fig.add_axes([(0.15 + j * W) / FW, (y + 0.12) / H, (W - 0.05) / FW, (W - 0.05) / H]); ax.set_aspect("equal"); ax.axis("off")
        vac = subs[s]
        cx = sum(p[0] for p in pts) / len(pts); cy = sum(p[1] for p in pts) / len(pts)
        if vac:
            vx = sum(s_top[k][0] for k in vac) / len(vac); vy = sum(s_top[k][1] for k in vac) / len(vac)
            d = mic((vx, vy), (cx, cy)); cx, cy = vx + d[0] / 2, vy + d[1] / 2
        Rw = 5.0
        for p in mo:
            d = mic((cx, cy), p)
            if abs(d[0]) < Rw and abs(d[1]) < Rw: ax.plot(d[0], d[1], "s", ms=1.3, color="#9a998f", mew=0)
        for k, p in enumerate(s_top):
            d = mic((cx, cy), p)
            if abs(d[0]) < Rw and abs(d[1]) < Rw:
                if k in vac: ax.add_patch(Circle(d, 0.55, fill=False, ec="#c0392b", lw=0.8))
                else: ax.add_patch(Circle(d, 0.32, color="#cfcec6", lw=0))
        for p in sorted(pts, key=lambda q: q[2]):
            d = mic((cx, cy), p[:2]); col = LOW if p[3] == "vac" else (HIGH if p[3] == "up" else MID)
            ax.add_patch(Circle(d, 0.62, color=col, ec="white", lw=0.5, zorder=3))
        ax.set_xlim(-Rw, Rw); ax.set_ylim(-Rw, Rw)
        ax.text(0, -Rw - 0.3, "n=%d #%d" % (n, idx), ha="center", va="top", fontsize=5.5, color=ps.MUTED)
fig.savefig(os.path.join(HERE, "fig_step05_starts.png"), dpi=200); print("ok")
