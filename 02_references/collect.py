#!/usr/bin/env python3
"""Step 02: fit the MoS2 lattice constant and print the reference energies with their status."""
import glob
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import structures as st

def status(d):
    steps, nelm = st.scf_status(d)
    if steps is None: return "missing"
    if steps >= nelm: return "UNCONVERGED (%d/%d steps)" % (steps, nelm)
    return "%d steps" % steps

# ---- lattice constant
pts = []
for d in sorted(glob.glob(os.path.join(HERE, "MoS2_ascan", "a_*"))):
    e = st.last_energy(d)
    if e is not None: pts.append((float(os.path.basename(d)[2:]), e, status(d)))
print("MoS2 lattice scan")
for a, e, s in pts: print("  a = %.2f A   E0 = %.6f eV   %s" % (a, e, s))
if len(pts) >= 3:
    # least-squares parabola E = c0 + c1 x + c2 x^2, x measured from the mean for stability
    xm = sum(p[0] for p in pts) / len(pts)
    S = [sum((p[0] - xm) ** k for p in pts) for k in range(5)]
    T = [sum(p[1] * (p[0] - xm) ** k for p in pts) for k in range(3)]
    A = [[S[0], S[1], S[2], T[0]], [S[1], S[2], S[3], T[1]], [S[2], S[3], S[4], T[2]]]
    for i in range(3):
        A[i] = [v / A[i][i] for v in A[i]]
        for j in range(3):
            if j != i: A[j] = [vj - A[j][i] * vi for vj, vi in zip(A[j], A[i])]
    c1, c2 = A[1][3], A[2][3]
    if c2 <= 0: print("  no minimum in the scanned range; extend the scan")
    else:
        a0 = xm - c1 / (2 * c2)
        print("  equilibrium a = %.4f A%s" % (a0, "" if pts[0][0] < a0 < pts[-1][0] else "   WARNING: outside the scanned range"))
        print("  rebuild step 03 with:  python3 03_benchmarks/setup.py --a %.4f --encut 450" % a0)
else:
    print("  need at least 3 finished points")

# ---- references
print("\nReferences")
E = {}
for name in ("Pt_bulk", "Pt_bulk/static", "Pt_atom", "S_atom"):
    d = os.path.join(HERE, name)
    E[name] = st.last_energy(d)
    print("  %-15s %14s   %s" % (name, "%.6f" % E[name] if E[name] is not None else "-", status(d)))
if E["Pt_atom"] is not None and E["Pt_bulk/static"] is not None:
    print("\n  Pt cohesive energy = %.2f eV   (experiment 5.84; PBE typically ~5.5)" % (E["Pt_atom"] - E["Pt_bulk/static"]))
