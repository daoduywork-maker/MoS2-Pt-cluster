"""Shared structure and VASP-input builder for Project 2.

Used by the setup.py script in each numbered step folder.
Pure standard-library Python; no ASE needed. POTCAR is never written here.
"""
import math, os

DZ_S = 1.565       # A, S plane height above/below the Mo plane
C_SLAB = 24.0      # A, cell height for all slab jobs
Z_MO = 10.0        # A, height of the Mo plane in the cell
A_PT = 3.97        # A, starting fcc Pt lattice constant
BOX = [(14.0, 0, 0), (0, 15.0, 0), (0, 0, 16.0)]   # box for isolated atoms

# ---------------------------------------------------------------- INCAR pieces
# Electronic settings revised 2026-10-12 after job 217422-follow-up: ALGO = Fast
# (Davidson -> RMM-DIIS) diverged in every vacuum slab at the switch to RMM.
COMMON = """SYSTEM  = {name}
ENCUT   = {encut}
PREC    = Accurate
EDIFF   = 1E-5
ALGO    = {algo}
NELM    = 200
NELMIN  = 6
LASPH   = .TRUE.
IVDW    = 12          ! D3 with Becke-Johnson damping
LWAVE   = .FALSE.
LCHARG  = .FALSE.
NCORE   = {ncore}
"""
SEMI = "ISMEAR  = 0\nSIGMA   = 0.05\n"            # semiconductor / slab smearing
METAL = "ISMEAR  = 1\nSIGMA   = 0.2\n"            # bulk Pt smearing
STATIC = "NSW     = 0\n"
DIPOLE = "LDIPOL  = .TRUE.\nIDIPOL  = 3\n"
MIX = "AMIX    = 0.2         ! gentle mixing against charge sloshing in the vacuum\nBMIX    = 0.0001\n"
MIX_MAG = "AMIX_MAG = 0.8\nBMIX_MAG = 0.0001\n"
INCAR = {
 # relaxations
 "prim_relax": COMMON + "ISPIN   = 1\n" + SEMI + MIX + "LREAL   = .FALSE.\nIBRION  = 2\nNSW     = 50\nISIF    = 2           ! ions only; a is scanned by hand\nEDIFFG  = -0.01\n",
 "bulk_relax": COMMON + "ISPIN   = 1\n" + METAL + "LREAL   = .FALSE.\nIBRION  = 2\nNSW     = 50\nISIF    = 3           ! relax the cell; run at 600 eV for the stress\nEDIFFG  = -0.01\n",
 "slab_relax": COMMON + "ISPIN   = 2\n{magmom}" + SEMI + MIX + MIX_MAG + "LREAL   = Auto\nIBRION  = 2\nNSW     = 300\nISIF    = 2\nEDIFFG  = -0.02\n" + DIPOLE,
 # single points
 "prim_static": COMMON + "ISPIN   = 1\n" + SEMI + MIX + "LREAL   = .FALSE.\n" + STATIC,
 "bulk_static": COMMON + "ISPIN   = 1\n" + METAL + "LREAL   = .FALSE.\n" + STATIC,
 "slab_static": COMMON + "ISPIN   = 2\n{magmom}" + SEMI + MIX + MIX_MAG + "LREAL   = .FALSE.\n" + STATIC + DIPOLE,
 "atom":        COMMON + "ISPIN   = 2\nNUPDOWN = 2           ! triplet\nISYM    = 0\nISMEAR  = 0\nSIGMA   = 0.01\nLREAL   = .FALSE.\n" + STATIC,
}
MAGMOM0 = {"Mo": 0.5, "S": 0.0, "Pt": 1.0}   # starting moments (muB) for spin-polarised slabs

def kmesh(n1, n2, n3):
    return "%dx%dx%d\n0\nGamma\n%d %d %d\n0 0 0\n" % (n1, n2, n3, n1, n2, n3)

def write_job(step_dir, folder, name, kind, kpts, cell, atoms, encut, kpar=1, ncore=4):
    """Write INCAR, KPOINTS, POSCAR and vasp_bin into step_dir/folder.

    atoms: list of (symbol, x, y, z) in Cartesian A. Species order Mo, S, Pt.
    kpts: (n1, n2, n3). Gamma-only meshes get the vasp_gam binary.
    kpar/ncore: parallelisation only; they do not change the energies.
    """
    d = os.path.join(step_dir, folder)
    os.makedirs(d, exist_ok=True)
    order = [s for s in ("Mo", "S", "Pt") if any(a[0] == s for a in atoms)]
    counts = [sum(1 for a in atoms if a[0] == s) for s in order]
    lines = [name, "1.0"]
    lines += ["  %16.10f %16.10f %16.10f" % tuple(v) for v in cell]
    lines += ["  " + "  ".join(order), "  " + "  ".join(str(c) for c in counts), "Cartesian"]
    for s in order:
        lines += ["  %16.10f %16.10f %16.10f" % a[1:] for a in atoms if a[0] == s]
    open(os.path.join(d, "POSCAR"), "w").write("\n".join(lines) + "\n")
    magmom = "MAGMOM  = " + " ".join("%d*%.1f" % (c, MAGMOM0[s]) for s, c in zip(order, counts)) + "\n"
    algo = "All" if kind == "atom" else "Normal"   # All: direct minimisation, for the oscillating isolated atom
    text = INCAR[kind].format(name=name, encut=encut, algo=algo, ncore=ncore, magmom=magmom)
    if kpar > 1: text += "KPAR    = %d\n" % kpar
    open(os.path.join(d, "INCAR"), "w").write(text)
    open(os.path.join(d, "KPOINTS"), "w").write(kmesh(*kpts))
    open(os.path.join(d, "vasp_bin"), "w").write(("vasp_gam" if kpts == (1, 1, 1) else "vasp_std") + "\n")
    return d

# ---------------------------------------------------------------- structures
def lattice(a):
    return (a, 0.0), (-0.5 * a, 0.5 * math.sqrt(3) * a)

def prim_mos2(a):
    a1, a2 = lattice(a)
    cell = [(a1[0], a1[1], 0.0), (a2[0], a2[1], 0.0), (0.0, 0.0, C_SLAB)]
    mo = (a1[0] / 3 + 2 * a2[0] / 3, a1[1] / 3 + 2 * a2[1] / 3)
    s = (2 * a1[0] / 3 + a2[0] / 3, 2 * a1[1] / 3 + a2[1] / 3)
    return cell, [("Mo", mo[0], mo[1], Z_MO), ("S", s[0], s[1], Z_MO + DZ_S), ("S", s[0], s[1], Z_MO - DZ_S)]

def fcc_pt(a=A_PT):
    h = a / 2
    return [(0, h, h), (h, 0, h), (h, h, 0)], [("Pt", 0.0, 0.0, 0.0)]

def mos2(a, n):
    """n x n MoS2 monolayer: cell, Mo sites, top-S sites, bottom-S sites, hexagon centres."""
    a1, a2 = lattice(a)
    mo, s_top, s_bot, hollows = [], [], [], []
    for i in range(n):
        for j in range(n):
            ox, oy = i * a1[0] + j * a2[0], i * a1[1] + j * a2[1]
            mo.append((ox + a1[0] / 3 + 2 * a2[0] / 3, oy + a1[1] / 3 + 2 * a2[1] / 3))
            sx, sy = ox + 2 * a1[0] / 3 + a2[0] / 3, oy + 2 * a1[1] / 3 + a2[1] / 3
            s_top.append((sx, sy)); s_bot.append((sx, sy)); hollows.append((ox, oy))
    cell = [(n * a1[0], n * a1[1], 0.0), (n * a2[0], n * a2[1], 0.0), (0.0, 0.0, C_SLAB)]
    return cell, mo, s_top, s_bot, hollows

def nearest(points, ref):
    return min(range(len(points)), key=lambda k: (points[k][0] - ref[0]) ** 2 + (points[k][1] - ref[1]) ** 2)

def slab_atoms(mo, s_top, s_bot, removed=(), pt=()):
    at = [("Mo", x, y, Z_MO) for x, y in mo]
    at += [("S", x, y, Z_MO + DZ_S) for k, (x, y) in enumerate(s_top) if k not in removed]
    at += [("S", x, y, Z_MO - DZ_S) for x, y in s_bot]
    at += [("Pt", x, y, z) for x, y, z in pt]
    return at

def sites(a, n):
    """Cell plus the central S site, a neighbouring Mo and a neighbouring hexagon centre."""
    cell, mo, s_top, s_bot, hollows = mos2(a, n)
    centre = ((cell[0][0] + cell[1][0]) / 2, (cell[0][1] + cell[1][1]) / 2)
    ks = nearest(s_top, centre); s0 = s_top[ks]
    return cell, mo, s_top, s_bot, ks, s0, mo[nearest(mo, s0)], hollows[nearest(hollows, s0)]

def scf_status(job_dir):
    """(steps used in the last ionic step, NELM) from OSZICAR and INCAR; steps == NELM means not converged."""
    import re
    f = os.path.join(job_dir, "OSZICAR")
    if not os.path.exists(f): return None, None
    steps, n = 0, 0
    for line in open(f):
        if re.match(r"^[A-Z]+ *: *\d+", line): n += 1
        elif "F=" in line: steps, n = n, 0
    m = re.search(r"NELM\s*=\s*(\d+)", open(os.path.join(job_dir, "INCAR")).read())
    return steps, int(m.group(1)) if m else 60

def last_edisp(job_dir):
    """D3 energy (eV) of the last ionic step from OUTCAR. D3 is a pure additive term (it does not change
    the electron density), so E0 - Edisp is the plain-PBE energy at the same geometry."""
    import re
    f = os.path.join(job_dir, "OUTCAR")
    if not os.path.exists(f): return None
    v = re.findall(r"Edisp \(eV\):?\s*([-+.\dE]+)", open(f, errors="ignore").read())
    return float(v[-1]) if v else None

def last_energy(job_dir):
    """Final E0 from OSZICAR, or None if the job has not produced one."""
    import re
    f = os.path.join(job_dir, "OSZICAR")
    if not os.path.exists(f): return None
    e = re.findall(r"E0=\s*([-+.\dE]+)", open(f).read())
    return float(e[-1]) if e else None
