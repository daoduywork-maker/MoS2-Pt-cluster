# Project 2 — Literature Review

**Topic:** Defect-anchored Pt on monolayer MoS₂: why single atoms, clusters and nanoparticles form at sulfur vacancies
**Started:** 2026-10-09 · **Last updated:** 2026-10-09
**Status:** scope fixed from the 12 papers in this folder; calculations not started

---

## 1. Scope

The project is limited to **the gaps in the anchor paper (Yan 2025) that the downloaded literature leaves open but makes tractable**. Anything those papers already answer is taken as input, and anything they give no handle on is left out.

**Research question**

> One Pt atom in an S vacancy is very strongly bound, and vacancies far outnumber Pt atoms. Why, then, do clusters and nanoparticles form? Specifically: how do Ptₙ (n ≥ 2) bind and grow at a single S vacancy versus at neighbouring vacancies (pairs, rows, patches) on MoS₂?

**In scope**

1. Ptₙ (n = 1 to ~13) at an S vacancy and at vacancy pairs / short rows / triangles: structures, binding and addition energies.
2. The atom-versus-cluster decision: energy of a Pt atom in a fresh vacancy compared with joining an already anchored Ptₙ.
3. The control Yan 2025 lacks: the same cluster free, on pristine MoS₂, and on a vacancy, with charge transfer quantified.
4. ΔG_H* on the resulting realistic structures, as a final check against Yan's activity ranking.

**Out of scope** (none of the 12 papers gives a usable handle)

- The wet route: [PtCl₆]²⁻ adsorption, ligand loss, reduction.
- Solvent, pH and electrode potential; HER barriers and kinetics.
- Long-time dynamics, sintering at scale, machine-learned potentials.
- Other TMDs and other metals.

---

## 2. Files

All papers are in this folder, named `category-FirstauthorYear.pdf`.

| File | Reference | How I read it |
|---|---|---|
| `Pt_on_MoS2-Yan2025.pdf` | **Anchor.** Yan et al., *Adv. Funct. Mater.* 35, 2423262 (2025). DOI 10.1002/adfm.202423262 | Main text in full; SI not available |
| `Pt_on_MoS2-Li2017.pdf` | Li, Wang et al., *ACS Nano* 11, 3392 (2017). DOI 10.1021/acsnano.7b00796 | Main text in full |
| `Pt_on_MoS2-Saidi2015.pdf` | Saidi, *Cryst. Growth Des.* 15 (2015). DOI 10.1021/cg5013395 | Main text in full |
| `Pt_on_MoS2-Shi2018.pdf` | Shi et al., *J. Phys. Chem. Lett.* 9, 2972 (2018). DOI 10.1021/acs.jpclett.8b01233 | Most of main text |
| `Pt_on_MoS2-Shi2022.pdf` | Shi, Rabbani et al., *Nanoscale* 14, 617 (2022). DOI 10.1039/d1nr07836d | Most of main text (not the kinetics section) |
| `Pt_on_MoS2-Wang2018.pdf` | Wang et al., *ACS Nano* (2018). DOI 10.1021/acsnano.8b01418 | Skimmed (keyword search) |
| `Pt_on_MoS2-Ozaydin2014.pdf` | Özaydın et al., *Ann. Phys.* 526, 423 (2014). DOI 10.1002/andp.201400079 | Skimmed |
| `Pt_on_MoS2-Wu2017.pdf` | Wu et al., *PCCP* (2017). DOI 10.1039/C7CP04021K | Skimmed |
| `Pt_on_MoS2-Ramirez2022.pdf` | Ramírez-de-Arellano et al., *Int. J. Mol. Sci.* 23, 11199 (2022) | Skimmed |
| `S_vacancy_MoS2-Sensoy2017.pdf` | Sensoy et al., *Phys. Rev. B* 95, 014106 (2017) | Main text in full |
| `S_vacancy_MoS2-Komsa2013.pdf` | Komsa et al., *Phys. Rev. B* 88, 035301 (2013) | Most of main text |
| `S_vacancy_MoS2-Le2014.pdf` | Le, Rawal, Rahman, *J. Phys. Chem. C* 118, 5346 (2014) | Sections 1–3.2 in full |

Corrections to the first version of this file: "Han et al." is Wang 2018; "Saidi APS 2015" is the *Cryst. Growth Des.* paper; "Le AVS 2013" is the *J. Phys. Chem. C* 2014 paper; "Saidi group 2022" has Shi as first author.

---

## 3. Anchor paper: Yan 2025

**Method.** 5 s Ar plasma → S vacancies (~10% by HRTEM, ~15% by XPS) → H₂PtCl₆ solution → 300 °C, 2 h. Solution volume sets the Pt size. HER measured on one flake through a window on the basal plane.

| Sample | η at 10 mA cm⁻² | Tafel (mV dec⁻¹) | DFT ΔG_H* (eV) |
|---|---|---|---|
| Pristine MoS₂ | 367 mV | 140.9 | 1.81 |
| Pt single atoms | 202 mV | 94.3 | 0.71 |
| Pt clusters (<1 nm) | 94 mV | 65.9 | −0.01 |
| Pt nanoparticles (~1.9 nm) | 259 mV | 112.9 | −0.50 |

**DFT setup.** VASP, PBE-D3, 600 eV. Rectangular 2×5 cell for pristine and single-atom models, 3×6 for nanoparticles. Cluster = Pt₁₃ icosahedron; nanoparticle = 32-atom Wulff shape. One H site per system.

---

## 4. Gap-by-gap: what the literature provides, what is left

| # | Gap in Yan 2025 | Provided by the literature | Still open | Scope |
|---|---|---|---|---|
| 1 | Anchoring of one Pt at an S vacancy is never computed | **Closed by Li 2017** (binding, escape barrier, vacancy-to-vacancy hop); Ramírez 2022 agrees on binding | Nothing for n = 1 beyond recomputing in one consistent setup | Input |
| 2 | Atom → cluster → particle sequence is not explained | Growth on **pristine** MoS₂ (Saidi 2015, Shi 2018); at **grain boundaries** (Shi 2022, Wang 2018); vacancy arrangement and mobility (Sensoy, Komsa, Le) | **Ptₙ, n ≥ 2, at S vacancies and at neighbouring vacancies** | **Core** |
| 3 | "Electron transfer from MoS₂ makes ΔG_H* ≈ 0" has no control | Charge-transfer direction and size on pristine MoS₂ (Saidi 2015); energy and bonding decomposition methods (Saidi 2015, Shi 2022) | Free vs pristine vs vacancy comparison for the same cluster | **Core** |
| 4 | Activity model: idealised Pt₁₃ icosahedron, one site | Real Pt₁₃ on MoS₂ is a two-layer (111) structure, checked by STEM (Shi 2018); ΔG_H* for single-atom sites (Li 2017) | ΔG_H* on realistic vacancy-anchored clusters; H coverage | Limited (single H, a few sites) |
| 5 | "Defects play a negligible role" | Empty S vacancy has ΔG_H* = −0.06 eV, Pt-filled vacancy 0.83 eV (Li 2017) | Contribution of the many unfilled vacancies | Note only |
| 6 | Stability; Pt²⁺ fraction; residual Cl | Pt escape barrier ~3 eV (Li 2017) | Operating conditions, Cl | Out |
| 7 | Wet deposition pathway | Same H₂PtCl₆ route used experimentally (Li 2017, Wang 2018) | Everything computational | Out |

---

## 5. What the literature provides (numbers)

Energies from different papers are **not directly comparable**: setups differ (see 5.5).

### 5.1 One Pt atom on MoS₂

| Quantity | Value | Source |
|---|---|---|
| Binding, Pt in single S vacancy (S-sub) | 6.08 eV | Li 2017 |
| Binding, Pt in double (2S) vacancy | 5.74 eV | Li 2017 |
| Binding on pristine: Mo-top / S-top / valley | 3.71 / 3.22 / 3.17 eV | Li 2017 |
| Pristine surface, other setups | 2.83 eV at Mo-top (Saidi 2015); 2.89 eV (Özaydın 2014); ~3.14 eV, site not checked (Wang 2018) | — |
| Pt in S vacancy, small cell | 5.83 eV, vs 3.45 eV on pristine | Ramírez 2022 |
| Diffusion barrier on pristine | 0.6–0.82 eV (Li 2017); 0.6 and 0.7 eV, anisotropic (Saidi 2015); 0.50 eV (Wu 2017) | — |
| Escape from S vacancy to the surface | ~3 eV (return < 0.5 eV) | Li 2017 |
| **Hop from a vacancy into an adjacent empty vacancy** | **0.75 eV** | Li 2017 |
| S-vacancy formation energy | 6.87 eV (Li 2017); 5.85 eV (Le 2014, S-atom reference) | — |
| ΔG_H*: Pt in S vacancy | 0.83 eV (PBE), 0.99 eV (HSE06) | Li 2017 |
| ΔG_H*: Pt on Mo-top / empty S vacancy / basal plane | 0.03 / −0.06 / 2.06 eV | Li 2017 |

Li 2017 concludes that filling an S vacancy with Pt **deactivates** it for HER. Yan's 0.71 eV for the single atom agrees with this.

### 5.2 Ptₙ on pristine MoS₂

- Critical nucleus size is 1: a second Pt attaches with a 0.67 eV barrier and detaches with 0.91 eV; dimer is favoured by 0.1 eV/atom (Saidi 2015).
- Growth changes from flat to 3D at n = 5. Flat clusters bond to Mo, 3D clusters bond to S (Saidi 2015; confirmed by Shi 2018).
- Binding per atom rises with size: 2.83 (n = 1) → 2.96 → 3.20 → 3.47 → 3.45 → 3.57 (n = 6) → 4.09 eV (n = 12) (Saidi 2015).
- For 6 ≤ n ≤ 20 the clusters are two-layer, (111)-oriented, fcc-stacked. Pt₉, Pt₁₃, Pt₁₆, Pt₂₀, Pt₃₈ were matched to STEM images. Closed-polyhedron shapes for Pt₁₀–₁₂ are 0.1–0.8 eV/atom less stable (Shi 2018).
- Charge flows from MoS₂ to larger clusters: about 0.2 e for Pt₁₂ (Hirshfeld; Saidi 2015).

### 5.3 Ptₙ at another defect (grain boundary) — the template

- Pt₁ at the 5|7 boundary core binds 4.57 eV, against 2.83 eV on pristine (Shi 2022).
- The extra stabilisation fades with size: Pt₁₂ is 4.23 eV/atom at the boundary against 4.09 on pristine; Pt₂₀ is the same as pristine (Shi 2022).
- At the boundary the single atom is bound **more strongly per atom than any cluster up to Pt₂₀**, the reverse of the pristine surface (Shi 2022).
- Experiment: from an H₂PtCl₆ route with a 350 °C anneal, Pt nanoclusters seed at grain-boundary dislocation cores (Wang 2018).

### 5.4 S vacancies: arrangement and mobility

| Question | Sensoy 2017 | Komsa 2013 | Le 2014 |
|---|---|---|---|
| Do vacancies attract? | No: pairs up to 0.1 eV *less* stable than two isolated | Yes, weakly: lines gain 0.05–0.2 eV per vacancy | Yes, weakly: pair 5.81 vs 5.85 eV per vacancy; rows lowest |
| Barrier, isolated vacancy | 2.24 eV | 2.3 eV | 2.32 eV |
| Barrier, vacancy next to another | "essentially identical" | drops to as low as 0.8 eV | 0.79 eV (pair rotates) |

All three agree that the interaction is weak (≤ ~0.2 eV per vacancy) and that an isolated vacancy cannot move thermally. Li 2017 adds that a Pt atom next to a vacancy does not change the vacancy's barrier (2.3 eV).

**Why they differ on attraction**

- The pair energies are within noise of each other: up to +0.1 eV (Sensoy) against about −0.08 eV per pair (Le). A gap this small can change sign with setup choices.
- Setups differ where it matters at this level: Le relaxes the cell and converges forces to 0.01 eV/Å; Sensoy uses 0.05 eV/Å and a different code. Komsa shows vacancies shrink the lattice, so cell relaxation plausibly shifts the result.
- Different objects: Sensoy studied pairs only. The clear gains in Komsa and Le come from longer rows, where the effect adds up (Le: 5.85 eV per vacancy isolated → 5.68 for a row of five → 5.46 for an infinite row).

So "pairs do not attract" and "rows are favoured" are not really in conflict.

**Why they differ on the barrier**

Probably which hop was calculated. Le's numbers next to a vacancy pair:

| Hop | Barrier |
|---|---|
| The S atom adjacent to both vacancies moves into one (pair rotates by 60°) | 0.79 eV |
| Any other neighbouring S atom moves in | 2.3–2.4 eV |

Only one specific hop is easy; Komsa finds the same drop to ~0.8 eV. Sensoy reports the pair pathway as "essentially identical" to the isolated one, which suggests an ordinary hop was computed. The paper does not say which, so this is my reading.

**Consequence for the project**

- Attraction barely matters: with a 2.2–2.3 eV isolated barrier in all three papers, vacancies stay where the plasma made them, so a random distribution is a fair model.
- If the 0.8 eV hop is real, vacancy pairs can rotate at 300 °C but still cannot travel.
- Both points are settled by step 1 of section 7: pair energies at first, second and third neighbour distance (fixed and relaxed cell), plus one NEB for the rotating hop.

### 5.5 Setups used (why numbers differ)

| Paper | Code / functional | Cell | Notes |
|---|---|---|---|
| Yan 2025 | VASP, PBE-D3, 600 eV | 2×5 rect.; 3×6 rect. | Small cell for single atom |
| Li 2017 | VASP, PBE-D2, 300 eV, Γ | 8×4 rect. (192 atoms) | HSE06 check in 6×3 cell |
| Saidi 2015 | VASP, PBE (no vdW), 350 eV, Γ | 5×5 | AIMD to generate n ≥ 5 structures |
| Shi 2018 / 2022 | VASP, PBE + EAM genetic algorithm | — / nanoribbon | Structure search |
| Sensoy 2017 | Quantum ESPRESSO, PBE | 6×6, 8×8 | Charged defects too |
| Komsa 2013 | VASP, PBE | 10×8√3 rect. | |
| Le 2014 | VASP, PBE, 500 eV, Γ | 8×8 | |

The Mo-top monomer binding alone spans 2.83–3.71 eV across papers, so the baseline must be recomputed in one setup before any comparison.

---

## 6. What follows from combining them (my inferences, not from any paper)

**6.1 The puzzle is sharper than Yan presents it.** A Pt atom in an S vacancy (~6.1 eV, Li 2017) is bound far more strongly than a Pt atom in any cluster on pristine MoS₂ (≤ ~4.1 eV/atom up to Pt₁₂, Saidi 2015), and comparably to bulk Pt (experimental cohesive energy ~5.8 eV). With free vacancies available, single atoms should win thermodynamically. The functionals differ between these numbers, so this needs confirming in one setup.

**6.2 What moves at the 300 °C anneal.** Rough rates from the published barriers, assuming a 10¹³ s⁻¹ prefactor:

| Process | Barrier | Rate at 300 °C | In 2 h |
|---|---|---|---|
| Pt on pristine surface | 0.6 eV | ~5×10⁷ s⁻¹ | mobile |
| Pt from a vacancy into an adjacent empty vacancy | 0.75 eV | ~2×10⁶ s⁻¹ | mobile |
| S vacancy next to another vacancy | 0.8 eV | ~9×10⁵ s⁻¹ | mobile (if Komsa/Le are right) |
| Isolated S vacancy | 2.3 eV | ~6×10⁻⁸ s⁻¹ | frozen |
| Pt escaping a vacancy to the surface | 3.0 eV | ~4×10⁻¹⁴ s⁻¹ | frozen |

So a Pt atom in an **isolated** vacancy is stuck, while a Pt atom in a vacancy that has an **empty neighbouring vacancy** can keep moving within that group of vacancies.

**6.3 Neighbouring vacancies are common.** Each S site has 6 in-plane S neighbours. For random vacancies, the chance a vacancy has at least one vacant neighbour is 1 − (1 − c)⁶: 47% at c = 10%, 62% at 15%, 74% at 20%.

**6.4 Working hypothesis.** Isolated vacancies hold single atoms. Vacancy pairs and patches let anchored Pt atoms meet and are where clusters nucleate. The grain-boundary result (Shi 2022) suggests a defect stabilises only the first few atoms, so growth beyond that would follow the pristine-surface behaviour.

**6.5 Alternative to keep in mind.** Komsa 2013 notes that vacancies are readily filled by other species. If many plasma-made vacancies are passivated (for example by O) before Pt arrives, fewer anchoring sites exist than the 10–15% suggests. This is outside the scope but would change the interpretation.

---

## 7. Calculations this defines

1. **Baseline in one setup:** Pt₁ on pristine sites and in a single S vacancy; bulk Pt cohesive energy; S-vacancy pair energies (settles 5.4 for our purposes). Compare with Li 2017 and Saidi 2015.
2. **Substrates:** single vacancy; adjacent pair; three in a row; triangle of three. One S layer only, as plasma mainly removes top-layer S.
3. **Ptₙ on each substrate,** n = 1–6 by hand-built candidates, then selected larger sizes (up to ~13) starting from Shi 2018 structures. Report binding per atom, addition energy, and the Saidi 2015 decomposition (MoS₂ deformation / Pt–Pt / metal–support).
4. **Decision energies:** Pt in a fresh vacancy vs added to vacancy-anchored Ptₙ.
5. **Control for gap 3:** same Ptₙ free, on pristine, on a vacancy; charge transfer by one consistent partitioning.
6. **ΔG_H*** at a few sites on the most stable structures.
7. Optional: NEB for a Pt atom joining an anchored Pt across adjacent vacancies (extends Li's 0.75 eV hop).

Cell: Yan's 2×5 is too small for clusters; Saidi's 5×5 and Li's 8×4 rectangular are the reference sizes.

---

## 8. Parked (not downloaded, outside the current scope)

Kept so the links are not lost: Co/Ru on MoS₂ with an S vacancy ([Beilstein J. Nanotechnol. 12, 56](https://beilstein-journals.org/bjnano/articles/12/56)) — the closest method template and worth downloading; [Au nucleation at S vacancies](https://par.nsf.gov/biblio/10107284); [Pt sintering on MoS₂ in H₂](https://par.nsf.gov/servlets/purl/10177813); [H on Pt clusters review](https://journal.hep.com.cn/fop/EN/1159693405750092608); Pacchioni group on SAC modelling ([stability](https://boa.unimib.it/handle/10281/455849), [perspective](https://boa.unimib.it/handle/10281/444900)); [Pt MLIP](https://arxiv.org/abs/2301.11639v2); [MoS₂ MLIP](https://arxiv.org/abs/2512.15952v1).

---

## 9. Open checks

- [ ] "Cited by" search on Li 2017 and Shi 2018 for any Ptₙ-at-S-vacancy calculation (gap in row 2 is unconfirmed).
- [ ] Yan 2025 SI: charge analysis, extra H sites, Cl in XPS.
- [ ] Li 2017 SI: Table S1 (S-vacancy formation energy near Pt).
- [ ] Shi 2018 / 2022 SI: cluster coordinates to reuse.
- [ ] Read in full the four skimmed papers if their numbers are used (Wang 2018, Özaydın 2014, Wu 2017, Ramírez 2022).

## 10. Confidence

- Numbers in section 5 were taken from the papers' text; values that appear only in figures or SI were not checked.
- Section 6 is inference from combining papers with different setups; the rates are order-of-magnitude estimates.
- No supporting information was read for any paper.
