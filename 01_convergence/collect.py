#!/usr/bin/env python3
"""Step 01: print the cutoff and k-point convergence tables."""
import glob, re
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import structures as st

def table(title, folder, natoms, unit):
    rows = []
    for d in sorted(glob.glob(os.path.join(HERE, folder, "*"))):
        e = st.last_energy(d)
        if e is not None: rows.append((int(re.findall(r"\d+", os.path.basename(d))[0]), e / natoms))
    print("\n" + title)
    if not rows: print("  no finished jobs"); return
    ref = rows[-1][1]
    for v, e in rows:
        print("  %s = %4d   E/atom = %12.6f eV   diff to largest = %+8.2f meV" % (unit, v, e, 1000 * (e - ref)))
    print("  target: within 1 meV/atom of the largest setting")

table("Cutoff, MoS2 primitive (3 atoms)", "encut_MoS2", 3, "ENCUT")
table("Cutoff, bulk Pt (1 atom)", "encut_Pt_bulk", 1, "ENCUT")
table("k-mesh, MoS2 primitive (k x k x 1); k = 6 equals Gamma-only on the 6x6 cell", "kpts_MoS2", 3, "k")
table("k-mesh, bulk Pt (k x k x k)", "kpts_Pt_bulk", 1, "k")

print("\nCutoff, Pt binding in an S vacancy (3x3 cell, fixed geometry)")
rows = []
for d in sorted(glob.glob(os.path.join(HERE, "encut_binding", "encut_*"))):
    e = [st.last_energy(os.path.join(d, x)) for x in ("V1", "Pt_atom", "Pt1_V1")]
    if None not in e: rows.append((int(os.path.basename(d).split("_")[1]), e[0] + e[1] - e[2]))
if not rows: print("  no finished jobs")
else:
    ref = rows[-1][1]
    for v, b in rows: print("  ENCUT = %4d   binding = %8.4f eV   diff to largest = %+7.1f meV" % (v, b, 1000 * (b - ref)))
    print("  target: within 20 meV of the largest setting")
    print("  note: unrelaxed 3x3 geometry, so the absolute value is not the benchmark number")
