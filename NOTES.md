# Working notes — Project 2

Day-to-day notes: cluster, jobs, decisions, commands, checklists. The plan itself is in `README.md`.

## Cluster

Source for modules, launch line and queues: the lab's Wuzhou job templates (`pbs_s40wz_vasp-std.sh`, `pbs_std2wz_vasp-std.sh`, `pbs_f96wz_vasp-std.sh`), received 2026-10-09.

- WUZHOU-HPC, Torque/PBS (`qsub`, `qstat`, `pbsstat`).
- Queues: `std40` = 1 node × 40 cores (92 GB); `std2` = 2 nodes × 40; `fat96` = 2 nodes × 96.
- Modules, in this order: `module load intel/intel2020`, then `module load vasp/vasp544elpa`.
- Launch line: `mpirun -np $nproc -genv I_MPI_FABRICS=shm:ofi vasp_std`. Scripts carry `#PBS -V`.
- Other VASP builds installed: `vasp541scala`, `vasp544mod`, `vasp544scala`, `vasp632`, `vasp632vtst`, `vasp632vaspsol`, `vasp632vaspsol.vtst`, `vasp632wannier90`, `vasp643`.
- POTCARs: `/public/shared-data/pot/vasp/544/` holds `PAW_LDA`, `PAW_PBE`, `PAW_PW91`, `USPP_LDA`, `USPP_PW91`. We use `/public/shared-data/pot/vasp/544/PAW_PBE` (set in `01_convergence/run_all.pbs`). Confirmed present (2026-10-09): `Mo_pv`, `S`, `Pt`; alternatives `Mo`, `Mo_sv`, `Pt_pv` are also there.
- `vasp_gam`: **not yet checked**. Job scripts fall back to `vasp_std` if it is absent.

## Checklist before every submission

- [ ] `POTCAR` built and its species order matches line 6 of `POSCAR`
- [ ] `vasp_bin` matches `KPOINTS` (`vasp_gam` only for Γ-only)
- [ ] Memory checked against the node (92 GB on `std40`); for NEB, multiply by the number of images run at once
- [ ] Cores requested suit the job (the tiny step-01 jobs do not need 40)
- [ ] `NCORE` suits the core count

## Commands

    # build inputs
    python3 01_convergence/setup.py
    python3 02_references/setup.py --encut <E> --kprim <k>
    python3 03_benchmarks/setup.py --a <a> --encut <E>

    # step 01 on the cluster: all 40 jobs in one submission
    cd 01_convergence && qsub run_all.pbs      # set module name and VASP_PP_PATH inside first
    cat run_all.log                             # time, memory and status per job

    # a single job, inside its folder
    bash <repo>/make_potcar.sh
    qsub <repo>/run_vasp.pbs

    # results
    python3 01_convergence/collect.py
    python3 02_references/fit_lattice.py
    python3 03_benchmarks/collect.py

## Job log

| Date | Step / job | Job ID | Nodes | Result |
|---|---|---|---|---|
| 2026-10-11 | 01 convergence, `p2_conv` | 217422 | 1 × std40 | Stopped at the pre-flight check, nothing ran: POTCAR path had `shared_data` instead of `shared-data`. Fixed. |

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
| 2026-10-09 | NEB kinetics deferred | Not needed to answer G1 |
| 2026-10-09 | Nanoparticles (~1.9 nm) out of scope; stand-in deferred | Too large for a structure search in this cell |
| 2026-10-09 | Graphene comparison papers not added | Not needed for the current scope |

## Provisional values (replace when measured)

| Quantity | Provisional | Source of final value |
|---|---|---|
| MoS₂ lattice constant | 3.18 Å | `02_references/fit_lattice.py` |
| Cutoff | 450 eV | Step 01 |
| k-mesh, 6×6 relaxations | Γ | Step 01 (`kpts_MoS2`), confirmed in step 03 |
| Memory, largest job | a few GB (estimate) | `OUTCAR` of `03_benchmarks/Pt1_V1` |
| Compute, whole project | 1,000–1,500 node-hours (guess) | Step 03 timings |

## Open questions

- Largest cluster size: Pt₁₃ or Pt₆?
- Cited-by check on Li 2017 and Shi 2018: has anyone computed Ptₙ at S vacancies?
- Yan 2025 supporting information: does it contain a charge analysis or extra H sites?
- LICENSE for the repository: not chosen yet.
