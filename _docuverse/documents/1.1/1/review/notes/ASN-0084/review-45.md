# Review of ASN-0084

After thorough reading, I've checked the key correctness obligations:

**Proof structure verified:**
- R-PIV/R-SWP well-definedness: tiling argument exhaustive, clauses cover [c₀, c_{n−1}) ∩ V_S(d) disjointly via ord arithmetic
- R-PPERM/R-SPERM: piecewise definitions match postconditions case-by-case; injectivity within branches; surjectivity via finite-set self-injection (S8-fin); R-RI gives ran preservation
- R-COMM: same-region hypothesis discharges j'+k < w_region for each of α/μ/β branches via associativity (Extended Associativity per the OrdinalShift consumers list)
- Canonical decomposition steps (a)–(d): helper lemma proven (NAT-sub involution + NAT-wellorder), maximality contradictions construct singletons in both forward/backward directions
- R-BLK Phase 1 cut interactions: Case A/B dispatch handles cuts processed against already-refined partitions
- R-SP: every ASN-0036 invariant clause discharged — dom-preservation handles D-CTG/D-MIN/D-SEQ/S8a/S8-fin/S8-depth; bijectivity handles S2; R-RI handles S3; C' = C handles content-store invariants; R-BLK supplies B' as constructive S8 witness; R-NS dispatches non-S cases uniformly

**Edge cases covered:**
- Empty left exterior (ord(c₀) = 1) and empty right exterior (c_{n−1} = [S, N+1]) traced in worked example 5
- All three μ-displacement sub-cases (w_β > w_α, w_β < w_α, w_β = w_α) traced in examples 2, 3, 4
- Minimum w_α = w_β = 1 in example 5
- "Outside ⋃_k V(b_k)" sub-case justified via R-PRE(iv) restricting all cuts except c_{n−1} to V_S(d)
- Width positivity derived from R-PRE(iii)+(iv), demoted from precondition

**Necessity sketches** for R-PRE(iv) and R-PRE(iii) CS3 are concrete and distinguish semantic-precondition vs. well-typedness-guard modes of indispensability.

**Foundation citations correct:** ASN-0034, ASN-0036, ASN-0053 are all in the foundation list; no improper cross-references.

**Worked examples** verify each postcondition against explicit values (R-PRE, R-EXT/R-P1/R-P2 or R-S1/R-S2/R-S3, R-PPERM/R-SPERM, R-RI, R-DISP, R-BLK Phases 1–3, merge check). Five examples cover varied configurations.

The signed-magnitude carrier for Δ is unusual but justified by foundation's lack of signed integers, and is restricted to equality comparison.

The ASN remains in specification territory — abstract operations on state, abstract mathematical objects, no implementation drift.

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: k-cut generalization (k > 4)
**Why out of scope**: Explicitly listed in Open Questions; the 3-cut and 4-cut cases establish the foundation for future generalization.

### Topic 2: Composition of multiple rearrangements
**Why out of scope**: Explicitly listed in Open Questions; each REARRANGE_K is specified atomically.

### Topic 3: Cross-subspace rearrangements
**Why out of scope**: Stated scope restricts to text subspace S=1 at depth 2; the link subspace and deeper text subspaces are explicit non-goals.

### Topic 4: Run count bounds under rearrangement
**Why out of scope**: Explicitly listed in Open Questions; the ASN acknowledges B' may need exhaustive-merge to recover maximality.

VERDICT: CONVERGED
