#!/usr/bin/env python3
"""Step 04: build the 6x6 vacancy-pair and vacancy-triplet relaxations (fixed cell).

Jobs: V2_1nn, V2_2nn, V2_3nn, V2_far (two top-layer vacancies at increasing distance), V2_vert (top and
bottom S at the same site), V3_row (three in a line), V3_tri (the three top S bonded to one Mo).
Usage:  python3 04_vacancy_pairs/setup.py [--a 3.1514] [--encut 450]
"""
import argparse, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import structures as st

N = 6

def dist(cell, p, q):
    """Minimum-image in-plane distance."""
    best = 1e9
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            dx = q[0] - p[0] + i * cell[0][0] + j * cell[1][0]
            dy = q[1] - p[1] + i * cell[0][1] + j * cell[1][1]
            best = min(best, math.hypot(dx, dy))
    return best

def build(a, encut):
    cell, mo, s_top, s_bot, ks, s0, m0, h0 = st.sites(a, N)
    d = [round(dist(cell, s0, q) / a, 3) for q in s_top]           # distances from the central S, in units of a
    pick = lambda r: next(k for k in range(len(s_top)) if abs(d[k] - r) < 1e-3)
    k1, k2, k3 = pick(1.0), pick(round(math.sqrt(3), 3)), pick(2.0)
    kfar = max(range(len(s_top)), key=lambda k: d[k])
    # row: central S and two more along a1;  triangle: the three top S nearest to the Mo next to s0
    a1 = (a, 0.0)
    row = [ks] + [st.nearest(s_top, (s0[0] + m * a1[0], s0[1] + m * a1[1])) for m in (1, 2)]
    tri = sorted(range(len(s_top)), key=lambda k: dist(cell, m0, s_top[k]))[:3]
    tag = "a=%.4f" % a
    jobs = [("V2_1nn", (ks, k1)), ("V2_2nn", (ks, k2)), ("V2_3nn", (ks, k3)), ("V2_far", (ks, kfar)),
            ("V2_vert", (ks,)), ("V3_row", tuple(row)), ("V3_tri", tuple(tri))]
    out = []
    for name, rem in jobs:
        atoms = st.slab_atoms(mo, s_top, s_bot, rem)
        if name == "V2_vert":                                       # also remove the bottom S under s0
            zb = st.Z_MO - st.DZ_S
            atoms = [x for x in atoms if not (x[0] == "S" and abs(x[3] - zb) < 1e-6
                                              and math.hypot(x[1] - s0[0], x[2] - s0[1]) < 1e-6)]
        sep = ", ".join("%.2f" % (d[k] * a) for k in rem if k != ks) or "vertical"
        out.append(st.write_job(HERE, name, "MoS2 6x6 %s (%s A) %s" % (name, sep, tag), "slab_relax", (1, 1, 1),
                                cell, atoms, encut))
        print("%-8s %3d atoms (%d S removed); separations from the central vacancy: %s A" % (name, len(atoms), 108 - len(atoms), sep))
    return out

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", type=float, default=3.1514, help="MoS2 lattice constant from step 02 (A)")
    ap.add_argument("--encut", type=int, default=450, help="plane-wave cutoff from step 01 (eV)")
    args = ap.parse_args()
    print("wrote %d job folders in 04_vacancy_pairs" % len(build(args.a, args.encut)))
