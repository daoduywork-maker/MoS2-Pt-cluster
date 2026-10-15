#!/usr/bin/env python3
"""Step 05 (plan B): full search for Pt_n, n = 1-4, on P, V1, V2_1nn, V3_row, V3_tri.

Stage 1 (screen): every symmetry-distinct start, relaxed loosely (EDIFFG = -0.10, EDIFF = 1E-4, PREC = Normal).
Stage 2 (refine): the lowest 3 per (substrate, n) relaxed again with the standard settings (run_all.pbs, STAGE=refine).

Rules for the starts
  - sites: vacancy, Mo-top, hollow, S-top within 3.3 A (in-plane) of any vacancy; around one Mo on the pristine sheet
  - n = 1: every distinct site.  n >= 2: the vacancies are filled first (min(n, number of vacancies) Pt in vacancies)
  - clusters are connected (Pt-Pt <= 3.7 A at the starting heights); sites only 1.82 A apart are allowed, and the
    upper Pt is then raised until every Pt-Pt distance is >= 2.5 A (this gives compact and 3D clusters)
  - duplicates removed exactly with the substrate's symmetry operations (rotations, mirrors, lattice translations)
  - Pt1 on P (3 sites) and Pt1 in V1 are taken from 03_benchmarks and not repeated
Usage:  python3 05_Ptn_small/setup.py [--a 3.1514] [--encut 450] [--dry]
"""
import argparse, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import structures as st

N, R_SITE, D_MIN, D_CON, D_PTPT = 6, 3.3, 1.8, 3.7, 2.5

def geometry(a):
    g = {}
    g["cell"], g["mo"], g["s_top"], g["s_bot"], g["ks"], g["s0"], g["m0"], g["h0"] = st.sites(a, N)
    g["hol"] = st.mos2(a, N)[4]
    zs = st.Z_MO + st.DZ_S
    g["Z"] = {"vac": zs + 0.30, "Mo": st.Z_MO + 2.80, "hol": zs + 1.50, "S": zs + 2.10}   # step-03 relaxed heights
    return g

def tools(g):
    cell = g["cell"]; A = [[cell[0][0], cell[1][0]], [cell[0][1], cell[1][1]]]
    det = A[0][0] * A[1][1] - A[0][1] * A[1][0]; G = 3 * N
    frac = lambda p: (((A[1][1] * p[0] - A[0][1] * p[1]) / det) % 1.0, ((-A[1][0] * p[0] + A[0][0] * p[1]) / det) % 1.0)
    cart = lambda f: (A[0][0] * f[0] + A[0][1] * f[1], A[1][0] * f[0] + A[1][1] * f[1])
    key = lambda f: (int(round(f[0] * G)) % G, int(round(f[1] * G)) % G)        # all sites lie on a 1/(3N) grid
    def mic(p, q):
        best = None
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                d = (q[0] - p[0] + i * cell[0][0] + j * cell[1][0], q[1] - p[1] + i * cell[0][1] + j * cell[1][1])
                if best is None or math.hypot(*d) < math.hypot(*best): best = d
        return best
    ops = []
    for k in range(6):
        for m in (False, True):
            th = math.radians(60 * k); R = [[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]]
            if m: R = [[R[0][0], -R[0][1]], [R[1][0], -R[1][1]]]
            ops.append(R)
    app = lambda R, t, p: (R[0][0] * p[0] + R[0][1] * p[1] + t[0], R[1][0] * p[0] + R[1][1] * p[1] + t[1])
    trans = [cart((i / N, j / N)) for i in range(N) for j in range(N)]
    return frac, cart, key, mic, ops, app, trans, G

def substrates(g, a):
    s_top, s0, m0, ks = g["s_top"], g["s0"], g["m0"], g["ks"]
    k1 = st.nearest(s_top, (s0[0] + a, s0[1])); k2 = st.nearest(s_top, (s0[0] + 2 * a, s0[1]))
    tri = sorted(range(len(s_top)), key=lambda k: math.hypot(s_top[k][0] - m0[0], s_top[k][1] - m0[1]))[:3]
    return {"P": [], "V1": [ks], "V2_1nn": [ks, k1], "V3_row": [ks, k1, k2], "V3_tri": tri}

def enumerate_all(a):
    g = geometry(a); frac, cart, key, mic, ops, app, trans, G = tools(g); Z = g["Z"]
    out = []                                                # (substrate, n, index, [(x, y, z, site)])
    for name, vac in substrates(g, a).items():
        M = {key(frac(p)) for p in g["mo"]}; T = {key(frac(p)) for k, p in enumerate(g["s_top"]) if k not in vac}
        gops = []
        for R in ops:
            for t in trans:
                f = lambda P: {key(frac(app(R, t, cart((q[0] / G, q[1] / G))))) for q in P}
                if f(M) == M and f(T) == T: gops.append((R, t))
        cen = [g["s_top"][k] for k in vac] or [g["m0"]]
        near = lambda p: min(math.hypot(*mic(c, p)) for c in cen) <= R_SITE
        sl = [("vac", g["s_top"][k]) for k in vac]
        sl += [("Mo", p) for p in g["mo"] if near(p)] + [("hol", p) for p in g["hol"] if near(p)]
        sl += [("S", p) for k, p in enumerate(g["s_top"]) if k not in vac and near(p)]
        n_s = len(sl)
        def d3(i, j):
            d = mic(sl[i][1], sl[j][1]); return math.sqrt(d[0] ** 2 + d[1] ** 2 + (Z[sl[j][0]] - Z[sl[i][0]]) ** 2)
        D = [[d3(i, j) for j in range(n_s)] for i in range(n_s)]
        canon = lambda c: min(tuple(sorted((sl[i][0],) + key(frac(app(R, t, sl[i][1]))) for i in c)) for R, t in gops)
        seen, frontier = set(), [frozenset([i]) for i in range(n_s)]
        for n in range(1, 5):
            reps = []
            for c in frontier:
                k = canon(c)
                if k not in seen: seen.add(k); reps.append(sorted(c))
            kept = [c for c in reps if n == 1 or sum(sl[i][0] == "vac" for i in c) >= min(n, len(vac))]
            if n == 1 and name in ("P",): kept = []                       # done in 03_benchmarks
            if n == 1 and name == "V1": kept = [c for c in kept if sl[c[0]][0] != "vac"]
            for idx, c in enumerate(kept):
                out.append((name, n, idx, raise_heights(c, sl, Z, mic)))
            frontier = {frozenset(c + [j]) for c in reps for j in range(n_s)
                        if j not in c and all(D[i][j] >= D_MIN for i in c) and any(D[i][j] <= D_CON for i in c)}
    return g, out

def raise_heights(c, sl, Z, mic):
    """Place Pt from low to high; lift each until all Pt-Pt >= 2.5 A."""
    placed = []
    for i in sorted(c, key=lambda i: Z[sl[i][0]]):
        x, y = sl[i][1]; z = Z[sl[i][0]]
        for (px, py, pz, _) in placed:
            r = math.hypot(*mic((px, py), (x, y)))
            if r < D_PTPT and math.sqrt(r * r + (z - pz) ** 2) < D_PTPT: z = max(z, pz + math.sqrt(D_PTPT ** 2 - r * r))
        placed.append((x, y, z, sl[i][0] if z == Z[sl[i][0]] else "up"))
    return placed

def build(a, encut, dry=False):
    g, configs = enumerate_all(a)
    subs = substrates(g, a); tag = "a=%.4f" % a
    if dry: return configs
    sd = os.path.join(HERE, "screen"); os.makedirs(sd, exist_ok=True)
    man = ["# job  substrate  n  Pt sites (site type and start height in A)"]
    for name, n, idx, pts in configs:
        job = "%s_n%d_%03d" % (name, n, idx)
        atoms = st.slab_atoms(g["mo"], g["s_top"], g["s_bot"], subs[name], [(x, y, z) for x, y, z, _ in pts])
        d = st.write_job(sd, job, "%s screen %s" % (job, tag), "slab_relax", (1, 1, 1), g["cell"], atoms, encut)
        f = os.path.join(d, "INCAR"); s = open(f).read()                    # loose settings for the screen
        s = re.sub(r"(?m)^PREC .*$", "PREC    = Normal", s); s = re.sub(r"(?m)^EDIFF .*$", "EDIFF   = 1E-4", s)
        s = re.sub(r"(?m)^EDIFFG .*$", "EDIFFG  = -0.10", s); s = re.sub(r"(?m)^NSW .*$", "NSW     = 150", s)
        open(f, "w").write(s)
        man.append("%-18s %-7s %d  %s" % (job, name, n, " ".join("%s@%.2f" % (k, z) for _, _, z, k in pts)))
    open(os.path.join(sd, "manifest.txt"), "w").write("\n".join(man) + "\n")
    return configs

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", type=float, default=3.1514); ap.add_argument("--encut", type=int, default=450)
    ap.add_argument("--dry", action="store_true", help="count only, write nothing")
    args = ap.parse_args()
    cf = build(args.a, args.encut, args.dry)
    from collections import Counter
    c = Counter((s, n) for s, n, _, _ in cf)
    for s in ("P", "V1", "V2_1nn", "V3_row", "V3_tri"): print("%-7s n=1..4: %s" % (s, [c[(s, n)] for n in range(1, 5)]))
    print("total %d screening jobs%s" % (len(cf), " (dry run)" if args.dry else " written to 05_Ptn_small/screen"))
