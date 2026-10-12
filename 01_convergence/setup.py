#!/usr/bin/env python3
"""Step 01: build the cutoff and k-point convergence jobs (single points, fixed geometries).

Usage:  python3 01_convergence/setup.py [--a 3.18]
"""
import argparse
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import structures as st

ENCUTS = (350, 400, 450, 500, 550, 600)

def build(a):
    made = []
    pcell, pat = st.prim_mos2(a)
    bcell, bat = st.fcc_pt()
    for e in ENCUTS:                                   # cutoff, total energy
        made.append(st.write_job(HERE, "encut_MoS2/encut_%d" % e, "MoS2 prim ENCUT %d" % e, "prim_static", (15, 15, 1), pcell, pat, e))
        made.append(st.write_job(HERE, "encut_Pt_bulk/encut_%d" % e, "Pt bulk ENCUT %d" % e, "bulk_static", (15, 15, 15), bcell, bat, e))
    for k in (6, 9, 12, 15, 18):                       # k-mesh; k=6 on the primitive cell == Gamma on 6x6
        made.append(st.write_job(HERE, "kpts_MoS2/k_%02d" % k, "MoS2 prim k %d" % k, "prim_static", (k, k, 1), pcell, pat, 450))
    for k in (9, 12, 15, 18, 21):
        made.append(st.write_job(HERE, "kpts_Pt_bulk/k_%02d" % k, "Pt bulk k %d" % k, "bulk_static", (k, k, k), bcell, bat, 450))
    cell, mo, s_top, s_bot, ks, s0, m0, h0 = st.sites(a, 3)   # cutoff, binding energy, 3x3 cell; Pt reference = bulk Pt
    for e in ENCUTS:
        base = "encut_binding/encut_%d/" % e
        # 4x4x1 gives 4 irreducible k-points: KPAR = 4 with 40 ranks -> 10 ranks per k-point, NCORE = 5
        made.append(st.write_job(HERE, base + "V1", "3x3 V1 ENCUT %d" % e, "slab_static", (4, 4, 1), cell,
                                 st.slab_atoms(mo, s_top, s_bot, (ks,)), e, kpar=4, ncore=5))
        made.append(st.write_job(HERE, base + "Pt1_V1", "3x3 Pt1 in V1 ENCUT %d" % e, "slab_static", (4, 4, 1), cell,
                                 st.slab_atoms(mo, s_top, s_bot, (ks,), [(s0[0], s0[1], st.Z_MO + st.DZ_S + 0.20)]), e, kpar=4, ncore=5))
        # Pt reference = bulk Pt at the same cutoff (encut_Pt_bulk); the isolated atom oscillated and is not needed here
    return made

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", type=float, default=3.18, help="provisional MoS2 lattice constant (A)")
    print("wrote %d job folders in 01_convergence" % len(build(ap.parse_args().a)))
