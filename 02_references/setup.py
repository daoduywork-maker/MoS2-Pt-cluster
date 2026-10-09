#!/usr/bin/env python3
"""Step 02: build the MoS2 lattice-constant scan and the reference-energy jobs.

Usage:  python3 02_references/setup.py [--encut 450] [--kprim 15]
"""
import argparse
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import structures as st

def build(encut, kprim):
    made = []
    for a in (3.14, 3.15, 3.16, 3.17, 3.18, 3.19, 3.20):
        cell, at = st.prim_mos2(a)
        made.append(st.write_job(HERE, "MoS2_ascan/a_%.2f" % a, "MoS2 primitive a=%.2f" % a, "prim_relax", (kprim, kprim, 1), cell, at, encut))
    cell, at = st.fcc_pt()
    made.append(st.write_job(HERE, "Pt_bulk", "Pt fcc bulk", "bulk_relax", (15, 15, 15), cell, at, 600))
    made.append(st.write_job(HERE, "Pt_atom", "Pt atom", "atom", (1, 1, 1), st.BOX, [("Pt", 7.0, 7.5, 8.0)], encut))
    made.append(st.write_job(HERE, "S_atom", "S atom", "atom", (1, 1, 1), st.BOX, [("S", 7.0, 7.5, 8.0)], encut))
    return made

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--encut", type=int, default=450, help="plane-wave cutoff chosen in step 01 (eV)")
    ap.add_argument("--kprim", type=int, default=15, help="k-mesh for the primitive MoS2 cell chosen in step 01")
    args = ap.parse_args()
    print("wrote %d job folders in 02_references" % len(build(args.encut, args.kprim)))
