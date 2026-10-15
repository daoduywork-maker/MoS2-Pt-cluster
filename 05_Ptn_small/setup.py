#!/usr/bin/env python3
"""Step 05, round 1 (greedy search): Pt1 on the new vacancy substrates, and Pt2 on P and V1.

Pt1 on P and in V1 are already done in 03_benchmarks; substrate energies come from 03 and 04.
Starting heights follow the relaxed step-03 structures (Pt in vacancy 0.30 A above the S plane,
Pt on Mo-top 2.80 A above the Mo plane). A second Pt starts 2.5 A from the first.
Usage:  python3 05_Ptn_small/setup.py [--a 3.1514] [--encut 450]
"""
import argparse, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import structures as st

D_PTPT = 2.5

def build(a, encut):
    cell, mo, s_top, s_bot, ks, s0, m0, h0 = st.sites(a, 6)
    zs = st.Z_MO + st.DZ_S
    z_vac, z_mo, z_br = zs + 0.30, st.Z_MO + 2.80, zs + 1.00
    xy = lambda p, dx, dy: (p[0] + dx, p[1] + dy)
    mid = lambda p, q: ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
    unit = lambda p, q: ((q[0] - p[0]) / math.hypot(q[0] - p[0], q[1] - p[1]),
                         (q[1] - p[1]) / math.hypot(q[0] - p[0], q[1] - p[1]))
    # substrates, built as in step 04: pair and row along a1, triangle = the 3 top S around m0
    k1 = st.nearest(s_top, xy(s0, a, 0)); k2 = st.nearest(s_top, xy(s0, 2 * a, 0))
    s1, s2 = s_top[k1], s_top[k2]
    tri = sorted(range(len(s_top)), key=lambda k: math.hypot(s_top[k][0] - m0[0], s_top[k][1] - m0[1]))[:3]
    sub = {"P": (), "V1": (ks,), "V2_1nn": (ks, k1), "V3_row": (ks, k1, k2), "V3_tri": tuple(tri)}
    m01 = mo[st.nearest(mo, mid(s0, s1))]                           # Mo shared by the 1nn pair
    # second-Pt helpers
    u_s, u_h = unit(m0, s0), unit(m0, h0)                           # Mo-top -> S-top / -> hollow directions
    # flat-ish dimers on pristine: second Pt tilted up so Pt-Pt = 2.5 A and Pt-S >= 2.27 A (searched over angles)
    p_s = (m0[0] + 2.3 * u_s[0], m0[1] + 2.3 * u_s[1]); p_h = (m0[0] + 2.4 * u_h[0], m0[1] + 2.4 * u_h[1])
    dz2 = math.sqrt(D_PTPT ** 2 - (a / math.sqrt(3)) ** 2)          # height so Pt-Pt = 2.5 A at 1.82 A in-plane
    s_far = s_top[st.nearest(s_top, xy(s0, -a, 0))]                 # S site 3.15 A from s0, away from m0 side
    m_next = mo[st.nearest(mo, xy(m0, a, 0))]
    T = lambda p, z: (p[0], p[1], z)
    jobs = [
        # Pt1 on the new substrates
        ("n1_V2_1nn_vac",      "V2_1nn", [T(s0, z_vac)]),
        ("n1_V2_1nn_bridge",   "V2_1nn", [T(mid(s0, s1), z_br)]),
        ("n1_V2_1nn_Mo-top",   "V2_1nn", [T(m01, z_mo)]),
        ("n1_V3_row_end",      "V3_row", [T(s0, z_vac)]),
        ("n1_V3_row_mid",      "V3_row", [T(s1, z_vac)]),
        ("n1_V3_row_bridge",   "V3_row", [T(mid(s0, s1), z_br)]),
        ("n1_V3_tri_vac",      "V3_tri", [T(s_top[tri[0]], z_vac)]),
        ("n1_V3_tri_Mo-centre", "V3_tri", [T(m0, st.Z_MO + 2.60)]),
        # Pt2 on pristine, first Pt at Mo-top (lowest Pt1 site in step 03)
        ("n2_P_flat-S",   "P",  [T(m0, z_mo), T(p_s, z_mo + 0.98)]),
        ("n2_P_flat-h",   "P",  [T(m0, z_mo), T(p_h, z_mo + 0.70)]),
        ("n2_P_vertical", "P",  [T(m0, z_mo), T(m0, z_mo + D_PTPT)]),
        ("n2_P_Mo-Mo",    "P",  [T(m0, z_mo), T(m_next, z_mo)]),
        # Pt2 on V1, first Pt in the vacancy
        ("n2_V1_side-Mo",   "V1", [T(s0, z_vac), T(m0, z_vac + dz2)]),
        ("n2_V1_side-h",    "V1", [T(s0, z_vac), T(h0, z_vac + dz2)]),
        ("n2_V1_vertical",  "V1", [T(s0, z_vac), T(s0, z_vac + D_PTPT)]),
        ("n2_V1_S-top-nn",  "V1", [T(s0, z_vac), T(s_far, zs + 2.10)]),
    ]
    tag = "a=%.4f" % a
    out = []
    for name, s, pt in jobs:
        atoms = st.slab_atoms(mo, s_top, s_bot, sub[s], pt)
        out.append(st.write_job(HERE, name, "%s (substrate %s) %s" % (name, s, tag), "slab_relax", (1, 1, 1),
                                cell, atoms, encut))
    return out

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", type=float, default=3.1514, help="MoS2 lattice constant from step 02 (A)")
    ap.add_argument("--encut", type=int, default=450, help="plane-wave cutoff from step 01 (eV)")
    args = ap.parse_args()
    print("wrote %d job folders in 05_Ptn_small" % len(build(args.a, args.encut)))
