#!/usr/bin/env python3
"""Step 03: collect energies and print the benchmark quantities next to the literature values."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import structures as st

REF = os.path.join(HERE, "..", "02_references")
PATHS = {"bulk": os.path.join(REF, "Pt_bulk"), "bulk_static": os.path.join(REF, "Pt_bulk", "static"),
         "Pt": os.path.join(REF, "Pt_atom"), "S": os.path.join(REF, "S_atom")}
for j in ("P", "V1", "Pt1_P_Mo-top", "Pt1_P_S-top", "Pt1_P_hollow", "Pt1_V1"):
    PATHS[j] = os.path.join(HERE, j)
E = {k: st.last_energy(p) for k, p in PATHS.items()}

def converged(key):
    f = os.path.join(PATHS[key], "OUTCAR")
    return os.path.exists(f) and "reached required accuracy" in open(f, errors="ignore").read()

print("%-16s %16s  %s" % ("job", "E0 (eV)", "relaxation converged"))
for k in PATHS:
    static = k in ("Pt", "S", "bulk_static")
    print("%-16s %16s  %s" % (k, "%.6f" % E[k] if E[k] is not None else "missing",
                              "-" if static or E[k] is None else ("yes" if converged(k) else "NO")))

def diff(*terms):
    if any(E[k] is None for _, k in terms): return None
    return sum(s * E[k] for s, k in terms)

def show(label, value, ref):
    print("%-44s %10s   %s" % (label, "%.2f eV" % value if value is not None else "n/a", ref))

print("\nBenchmarks (positive = bound)")
bulk = "bulk_static" if E["bulk_static"] is not None else "bulk"
show("Pt cohesive energy", diff((1, "Pt"), (-1, bulk)),
     "experiment 5.84" + ("" if bulk == "bulk_static" else "  [from the 600 eV relaxation; run Pt_bulk/static]"))
show("S-vacancy formation (S-atom reference)", diff((1, "V1"), (1, "S"), (-1, "P")), "Le 2014: 5.85")
for site, ref in (("Mo-top", "Li 2017: 3.71 | Saidi 2015: 2.83"), ("S-top", "Li 2017: 3.22 | Saidi 2015: 2.20"),
                  ("hollow", "Li 2017: 3.17 | Saidi 2015: 2.25")):
    show("Pt1 binding, pristine " + site, diff((1, "P"), (1, "Pt"), (-1, "Pt1_P_" + site)), ref)
show("Pt1 binding in S vacancy", diff((1, "V1"), (1, "Pt"), (-1, "Pt1_V1")), "Li 2017: 6.08  (pass if within ~0.2)")

# ---- D3 versus plain PBE (same geometries): E_PBE = E0 - Edisp
print("\nPt1 binding with bulk-Pt reference, with and without the D3 term (positive = bound)")
D = {k: st.last_edisp(p) for k, p in PATHS.items()}
bulk = "bulk_static" if E["bulk_static"] is not None else "bulk"
def both(sub, ads):
    if any(E[k] is None for k in (sub, bulk, ads)): return None, None
    full = E[sub] + E[bulk] - E[ads]
    if any(D[k] is None for k in (sub, bulk, ads)): return full, None
    return full, full - (D[sub] + D[bulk] - D[ads])
for site in ("Pt1_P_Mo-top", "Pt1_P_S-top", "Pt1_P_hollow", "Pt1_V1"):
    f, n = both("V1" if site == "Pt1_V1" else "P", site)
    print("  %-14s PBE+D3 %8s   plain PBE %8s" % (site, "%.3f" % f if f is not None else "n/a", "%.3f" % n if n is not None else "n/a"))
if E["Pt"] is not None and E[bulk] is not None and D[bulk] is not None:
    print("  Pt cohesive energy: PBE+D3 %.2f eV, plain PBE (D3 lattice) %.2f eV, experiment 5.84 eV" %
          (E["Pt"] - E[bulk], E["Pt"] - (E[bulk] - D[bulk])))
