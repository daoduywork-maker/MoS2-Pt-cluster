#!/usr/bin/env python3
"""Step 03: build the 6x6 MoS2 benchmark jobs (pristine, one S vacancy, one Pt on each).

Usage:  python3 03_benchmarks/setup.py [--a 3.18] [--encut 450]
"""
import argparse
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import structures as st

def build(a, encut):
    cell, mo, s_top, s_bot, ks, s0, m0, h0 = st.sites(a, 6)
    zs = st.Z_MO + st.DZ_S
    tag = "a=%.4f" % a
    jobs = [
     ("P",             "MoS2 6x6 pristine " + tag,       (),    ()),
     ("V1",            "MoS2 6x6 one S vacancy " + tag,  (ks,), ()),
     ("Pt1_P_Mo-top",  "Pt1 on pristine, Mo-top " + tag, (),    [(m0[0], m0[1], st.Z_MO + 2.76)]),
     ("Pt1_P_S-top",   "Pt1 on pristine, S-top " + tag,  (),    [(s0[0], s0[1], zs + 2.10)]),
     ("Pt1_P_hollow",  "Pt1 on pristine, hollow " + tag, (),    [(h0[0], h0[1], zs + 1.50)]),
     ("Pt1_V1",        "Pt1 in S vacancy " + tag,        (ks,), [(s0[0], s0[1], zs + 0.20)]),
    ]
    return [st.write_job(HERE, f, n, "slab_relax", (1, 1, 1), cell, st.slab_atoms(mo, s_top, s_bot, rem, pt), encut)
            for f, n, rem, pt in jobs]

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", type=float, default=3.18, help="MoS2 lattice constant from step 02 (A); 3.18 is provisional")
    ap.add_argument("--encut", type=int, default=450, help="plane-wave cutoff chosen in step 01 (eV)")
    args = ap.parse_args()
    print("wrote %d job folders in 03_benchmarks" % len(build(args.a, args.encut)))
