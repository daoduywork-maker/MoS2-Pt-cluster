#!/usr/bin/env python3
"""Step 02: fit E(a) from MoS2_ascan to a parabola and print the equilibrium lattice constant."""
import glob
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import structures as st

pts = []
for d in sorted(glob.glob(os.path.join(HERE, "MoS2_ascan", "a_*"))):
    e = st.last_energy(d)
    if e is not None: pts.append((float(os.path.basename(d)[2:]), e))
if len(pts) < 3:
    raise SystemExit("need at least 3 finished points, found %d" % len(pts))

# least-squares parabola E = c0 + c1 x + c2 x^2, x measured from the mean for stability
xm = sum(p[0] for p in pts) / len(pts)
S = [sum((p[0] - xm) ** k for p in pts) for k in range(5)]
T = [sum(p[1] * (p[0] - xm) ** k for p in pts) for k in range(3)]
A = [[S[0], S[1], S[2], T[0]], [S[1], S[2], S[3], T[1]], [S[2], S[3], S[4], T[2]]]
for i in range(3):                       # Gauss elimination
    A[i] = [v / A[i][i] for v in A[i]]
    for j in range(3):
        if j != i: A[j] = [vj - A[j][i] * vi for vj, vi in zip(A[j], A[i])]
c0, c1, c2 = A[0][3], A[1][3], A[2][3]
for a, e in pts: print("a = %.2f A   E0 = %.6f eV" % (a, e))
if c2 <= 0: raise SystemExit("no minimum in the scanned range; extend the scan")
a0 = xm - c1 / (2 * c2)
print("\nequilibrium a = %.4f A" % a0)
if not (pts[0][0] < a0 < pts[-1][0]): print("WARNING: minimum is outside the scanned range; extend the scan")
print("rebuild step 03 with:  python3 03_benchmarks/setup.py --a %.4f --encut <E>" % a0)
