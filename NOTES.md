# Working notes — Project 2

Day-to-day notes: cluster, jobs, decisions, commands, checklists. The plan itself is in `README.md`.

## Cluster

Source for modules, launch line and queues: the lab's Wuzhou job templates (`pbs_s40wz_vasp-std.sh`, `pbs_std2wz_vasp-std.sh`, `pbs_f96wz_vasp-std.sh`), received 2026-10-09.

- WUZHOU-HPC, Torque/PBS (`qsub`, `qstat`, `pbsstat`).
- Queues: `std40` = 40-core nodes (92 GB each), multi-node requests accepted (own CsPbI₃ jobs run on 2–3 nodes there); `std2` = 2 nodes × 40; `fat96` = 2 nodes × 96.
- Modules, in this order: `module load intel/intel2020`, then `module load vasp/vasp544elpa`.
- Launch line: `mpirun -np $nproc -genv I_MPI_FABRICS=shm:ofi vasp_std`. Scripts carry `#PBS -V`.
- Other VASP builds installed: `vasp541scala`, `vasp544mod`, `vasp544scala`, `vasp632`, `vasp632vtst`, `vasp632vaspsol`, `vasp632vaspsol.vtst`, `vasp632wannier90`, `vasp643`.
- POTCARs: `/public/shared-data/pot/vasp/544/` holds `PAW_LDA`, `PAW_PBE`, `PAW_PW91`, `USPP_LDA`, `USPP_PW91`. We use `/public/shared-data/pot/vasp/544/PAW_PBE` (set in `01_convergence/run_all.pbs`). Confirmed present (2026-10-09): `Mo_pv`, `S`, `Pt`; alternatives `Mo`, `Mo_sv`, `Pt_pv` are also there.
- `vasp_gam` exists (used by the Pt-atom jobs in the first run).
- VASP 5.4.4 writes `Maximum memory used` with a capital M; search case-insensitively.

## Checklist before every submission

- [ ] `POTCAR` built and its species order matches line 6 of `POSCAR`
- [ ] `vasp_bin` matches `KPOINTS` (`vasp_gam` only for Γ-only)
- [ ] Memory checked against the node (92 GB on `std40`); for NEB, multiply by the number of images run at once
- [ ] One job of the batch tested first, and its SCF converged (steps < NELM)
- [ ] Cores requested suit the job (the tiny step-01 jobs do not need 40)
- [ ] `NCORE` suits the core count

## Commands

    # build inputs
    python3 01_convergence/setup.py
    python3 02_references/setup.py              # defaults = step-01 choices (450 eV, 15x15x1, bulk Pt 21^3)
    python3 03_benchmarks/setup.py --a <a> --encut <E>

    # step 01 on the cluster
    cd 01_convergence
    qsub test_one.pbs                           # one slab job, 1 h limit
    cat test_one.log                            # expect < 200 SCF steps, E0 near -197.9 eV
    qsub run_all.pbs                            # the other 33 jobs on 4 nodes
    cat run_all.log                             # node, time, memory, ok(N steps) / UNCONVERGED / FAILED per job

    # step 02 on the cluster
    cd 02_references
    qsub test_one.pbs                           # Pt atom alone, 1 h limit
    cat test_one.log
    qsub run_all.pbs                            # the rest + Pt_bulk/static, 1 node
    cat run_all.log                             # also flags NOT_RELAXED for relaxations

    # step 03 on the cluster
    cd 03_benchmarks
    qsub test_one.pbs                           # Pt1_V1 alone; early report after the first ionic step
    cat test_one.log                            # memory, time per SCF step
    qsub run_all.pbs                            # the other 5 on 2 nodes; skips Pt1_V1 while the test runs
    qsub kcheck.pbs                             # k-point/cutoff check: 8 single points in kcheck/, 2 nodes
    cat kcheck.log                              # binding change in meV; target < 20

    # energies of every finished job, no Python needed
    for d in */; do echo "$d | $(tail -1 $d/OSZICAR) | $(grep 'Edisp' $d/OUTCAR | tail -1)"; done

    # plain-PBE energy of any finished job: E0 - Edisp
    grep -i edisp OUTCAR | tail -1

    # a single job, inside its folder
    bash <repo>/make_potcar.sh
    qsub <repo>/run_vasp.pbs

    # results
    python3 01_convergence/collect.py
    python3 02_references/collect.py
    python3 03_benchmarks/collect.py

## Job log

| Date | Step / job | Job ID | Nodes | Result |
|---|---|---|---|---|
| 2026-10-11 | 01 convergence, `p2_conv` | 217422 | 1 × std40 | Stopped at the pre-flight check, nothing ran: POTCAR path had `shared_data` instead of `shared-data`. Fixed. |
| 2026-10-11 | 01 convergence, `p2_conv` (resubmitted) | not recorded | 1 × std40 | Hit the 6 h walltime after 9 of 40 jobs. **All 9 unconverged**: every job used all 150 SCF steps. Slab energies diverged at the Davidson → RMM-DIIS switch (step 6), e.g. 3×3 V1 at 350 eV reached −197.88 eV at step 5, then −34 778 eV, final E0 +511 eV for Pt1_V1. Pt atom oscillated ±0.025 eV around −0.65 eV. Results discarded; folder renamed `01_convergence_failed` on the cluster. ~5.6 node-hours lost. |
| 2026-10-12 | 01 `test_one.pbs` (3×3 V1, 350 eV) | not recorded | 1 × std40 | Passed: 54 SCF steps, E0 = −197.52 eV, mag 0.00, 519 s, 0.5 GB. |
| 2026-10-12 | 01 `run_all.pbs` | 217587 | 4 requested; log shows node12, node9 | **Done**: all 33 converged (10–89 steps); 1 h 52 min; ≤ 0.6 GB. Only 2 distinct hosts appeared in `$PBS_NODEFILE`; not yet investigated. |
| 2026-10-12 | 02 `test_one.pbs` (Pt atom) | not recorded | 1 × std40 | Passed: 18 CG steps, E0 = −0.568 eV, mag 2.00, 70 s. |
| 2026-10-12 | 02 `run_all.pbs` | 217589 | 1 × std40 | **Done**: all converged; 3 min. a(MoS₂) = 3.1514 Å, a(Pt) = 3.926 Å, E_coh(Pt) = 6.29 eV. |
| 2026-10-12 | 03 `test_one.pbs` (`Pt1_V1`, 6×6, 108 atoms) | `p2_test3`, ID not recorded | 1 × std40 | **Done**: first ionic step 1621 s (21 SCF, 45–72 s each); 12 ionic steps, 7842 s; 0.56 GB on rank 0; E0 = −819.765 eV, mag 0. |
| 2026-10-13 | 03 `run_all.pbs` (other 5) | 217591 | 2 × std40 (node12, node9) | **Done** 00:49–12:42: all `ok`. P 1 ionic step (2978 s); hollow 16 (9625 s); Mo-top 32 (19795 s); S-top 12 (13483 s); V1 29 (20023 s); 0.6 GB per rank. |

## Decisions

| Date | Decision | Reason |
|---|---|---|
| 2026-10-09 | Scope limited to the gaps in Yan 2025 that the 12 downloaded papers leave open | Keeps the project moderate |
| 2026-10-09 | VASP, build `vasp/vasp544elpa` | Same code as all reference papers; this is the build the lab runs, with a known compiler module and launch line |
| 2026-10-09 | NEB step, if revived, would use `vasp632vtst` | The 5.4.4 build has no VTST tools; barriers are differences within one build |
| 2026-10-09 | PBE + D3(BJ), `IVDW = 12` | Yan says only "DFT-D3"; the damping variant is our choice |
| 2026-10-09 | POTCARs `Mo_pv`, `S`, `Pt` | Lighter than `Mo_sv`; to be tested if it matters |
| 2026-10-09 | 6×6 cell, 24 Å cell height | Keeps Pt₁₃ more than 10 Å from its image |
| 2026-10-09 | Convergence tests run before the lattice scan | The scan and everything after inherit the settings |
| 2026-10-09 | Step 01 runs as one PBS job (`run_all.pbs`), 8 MPI ranks for cells of ≤ 3 atoms | 40 tiny jobs would waste queue time; few-band cells do not need 40 ranks |
| 2026-10-09 | `ALGO = Normal` for isolated atoms | More reliable convergence than `Fast` for an atom in a box |
| 2026-10-12 | `ALGO = Normal` for all non-atom jobs (was `Fast`) | `Fast` switches to RMM-DIIS at step 6, which diverged in every vacuum slab |
| 2026-10-12 | `AMIX = 0.2`, `BMIX = 0.0001`, `AMIX_MAG = 0.8`, `BMIX_MAG = 0.0001` for slabs (charge mixing also for the primitive MoS₂ cell) | Standard settings against charge sloshing in cells with vacuum |
| 2026-10-12 | Explicit `MAGMOM`: Mo 0.5, S 0, Pt 1 μB | Default of 1 μB on every atom is a poor start |
| 2026-10-12 | `NELM = 200`, `NELMIN = 6` | Headroom; a job using all NELM steps is now flagged UNCONVERGED |
| 2026-10-12 | Cutoff test of Pt binding uses bulk Pt (same cutoff) as reference; Pt atom dropped from step 01 | The atom oscillated beyond the 20 meV target; bulk Pt converges easily and the jobs exist already |
| 2026-10-12 | `ALGO = All` for isolated atoms (step 02) | Direct minimisation; usual cure for oscillating atoms |
| 2026-10-12 | `KPAR = 4`, `NCORE = 5` for the 3×3 slab jobs (4 irreducible k-points) | Parallelisation only; energies unchanged |
| 2026-10-12 | Step 01 on 4 nodes, one job per node at a time (`run_all.pbs`); `test_one.pbs` runs a single slab job first | User asked for 4 nodes; jobs are independent, so 4 parallel workers use them fully |
| 2026-10-12 | ENCUT = 450 eV; Γ for 6×6; 15×15×1 MoS₂ primitive; 21×21×21 bulk Pt | Step 01 results (see Fixed values) |
| 2026-10-12 | Step 02 on 1 node; Pt atom tested alone first | Ten small cells; the atom is the one job with untested settings (`ALGO = All`) |
| 2026-10-12 | a = 3.1514 Å for all 6×6 cells | Step 02 fit |
| 2026-10-12 | Report every binding energy with and without D3 (E_PBE = E0 − Edisp at the same geometry); re-relax key structures with plain PBE if a conclusion changes | D3 overbinds Pt cohesion by 0.45 eV, which favours clusters and could bias G1 |
| 2026-10-12 | Step 03: test `Pt1_V1` with an early report after the first ionic step; then the rest on 2 nodes | First 108-atom relaxation; memory and timing unmeasured |
| 2026-10-12 | Fixed `Edisp` parsing (VASP 5.4.4 prints `Edisp (eV)` without a colon) | Found when reading the step-02 output |
| 2026-10-13 | Step 03 passes (Pt₁ in vacancy 5.89 eV vs Li 2017 6.08; pristine site ranking matches); no plain-PBE re-relaxation yet | No ranking changes between D3 and plain PBE |
| 2026-10-13 | `kcheck.pbs` without KPAR | Keeps memory per rank low for the `vasp_std` single points (estimate ~1 GB per rank, < 50 GB per node) |
| 2026-10-12 | Always test one job before a batch | The first batch wasted 5.6 node-hours on settings never tried on one job |
| 2026-10-09 | NEB kinetics deferred | Not needed to answer G1 |
| 2026-10-09 | Nanoparticles (~1.9 nm) out of scope; stand-in deferred | Too large for a structure search in this cell |
| 2026-10-09 | Graphene comparison papers not added | Not needed for the current scope |

## Fixed values (measured)

| Quantity | Value | Source |
|---|---|---|
| Cutoff | 450 eV | Step 01: Pt binding varies ≤ 1 meV over 350–600 eV; totals ≤ 0.5 meV/atom at 450 eV |
| k-mesh, 6×6 relaxations | Γ | Step 01: 0.42 meV/atom on the pristine sheet; reconfirmed on the 6×6 cell in step 03 |
| k-mesh, MoS₂ primitive | 15×15×1 | Step 01: converged from k = 9 |
| k-mesh, bulk Pt | 21×21×21 | Step 01: 1–6 meV spread between k = 15 and 21 |
| MoS₂ lattice constant | 3.1514 Å | Step 02 fit (experiment 3.160 Å) |
| Pt lattice constant | 3.926 Å | Step 02 (experiment 3.924 Å) |
| Pt cohesive energy | 6.29 eV (PBE+D3); 5.52 eV plain PBE at the same lattice | Step 02; Edisp(bulk) = −0.777 eV/atom; experiment 5.84 eV |
| Pt₁ binding in S vacancy | 5.89 eV (PBE+D3); 5.16 eV plain PBE | Step 03 (Li 2017: 6.08) |
| Pt₁ binding, pristine Mo-top / S-top / hollow | 3.36 / 2.83 / 2.74 eV (D3); 2.79 / 2.36 / 2.20 eV (PBE) | Step 03 |
| S-vacancy formation, S-atom reference | 6.12 eV (D3); 5.54 eV (PBE) | Step 03 |
| Memory, 6×6 relaxation (Γ) | ≤ 0.6 GB per rank, ~24 GB per node | Step 03 |
| Time, 6×6 relaxation (Γ, 1 node) | 0.8 h (pristine, 1 step) to 5.6 h (32 steps); ~10 min per ionic step | Step 03 |

## Provisional values (replace when measured)

| Quantity | Provisional | Source of final value |
|---|---|---|
| Compute, whole project | 1,000–1,500 node-hours (guess) | Step 03 timings |

## Open questions

- Pt₁ in a vacancy is +0.4 eV relative to bulk Pt (both functionals). Robust, or inside the setup spread? Li 2017's 6.08 eV would flip the sign.
- Largest cluster size: Pt₁₃ or Pt₆?
- Cited-by check on Li 2017 and Shi 2018: has anyone computed Ptₙ at S vacancies?
- Yan 2025 supporting information: does it contain a charge analysis or extra H sites?
- LICENSE for the repository: not chosen yet.
