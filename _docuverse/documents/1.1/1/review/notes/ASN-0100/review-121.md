# Review of ASN-0100

## REVISE

### Issue 1: Per-address content invariants discharged twice with identical reasoning

**ASN-0100, §Post-state V-position well-formedness (S7 bullet) and §Atomicity and Canonical Order (K.α/K.ρ paragraph)**:

The S7 bullet already states its per-address discharge covers all states: *"Each clause below holds the moment its K.α firing commits a_k to dom(C), and therefore at every K.α intermediate state and at Σ', persisting unchanged by P0"* — then discharges S7a, S7b, C1b, C1c, and L0's content clause for each `a_k`.

§Atomicity then restates the same thing: *"the per-address content invariants — S7a, S7b, C1b, C1c, and L0's content clause (subspace_I(a_k) = s_C, since a_k is an emission of A_C(d), DisjointSubAllocatorChains; ASN-0093) — hold for the fresh a_k; each is established at its K.α commit and persists by P0, so it holds at every K.α intermediate as well as at Σ'."*

**Problem**: Both paragraphs discharge the identical five invariants for each fresh `a_k`, by the identical mechanism (K.α commit + P0 persistence), and both explicitly claim coverage "at every K.α intermediate and at Σ'." The §Atomicity restatement adds nothing — it even re-cites DisjointSubAllocatorChains. This is the "two paragraphs say the same thing in different words" pattern the anti-bloat pass targets; the reader must reconcile two discharges to confirm they are the same.

**Required**: Discharge S7a/S7b/C1b/C1c/L0-content once. Since the §Post-state bullet already asserts intermediate-and-boundary coverage, §Atomicity should reference it rather than restate it, and confine itself to the obligations genuinely new at the intermediate level (P6, P7, L14, S4, C-fin, S3★-aux for the fresh addresses).

### Issue 2: L0 content conjunct deferral is fragmented across three sections

**ASN-0100, §Link store unchanged, §Atomicity (link-store bullet), §Post-state (S7 bullet)**:

- §Link store unchanged: the content conjunct *"is discharged once, for both the K.α intermediates and the boundary, in the grouped per-address paragraph of §Atomicity and Canonical Order."*
- §Atomicity (link-store bullet): L0's second conjunct *"is treated per-address with the other content invariants of the fresh a_k."*
- §Post-state (S7 bullet): actually discharges *"L0's content clause — subspace_I(a_k) = s_C."*

**Problem**: Two sections defer the L0 content conjunct downstream, but the actual discharge lives in a *third* section (§Post-state), not the one pointed to (§Atomicity discharges it a fourth time per Issue 1). This is the "multiple paragraphs defer to the same downstream location" pattern, and the deferral targets are inconsistent with where the work is done.

**Required**: Pick one home for the L0 content-conjunct discharge and point both deferrals there. Eliminate the redundant restatement.

## OUT_OF_SCOPE

### Topic 1: Link-subspace insertion (K.μ⁺_L) semantics
Correctly bounded by §Bounding the Scope; the structurally different link-allocation path is future territory, not a gap here.

### Topic 2: Crash recovery to canonical order after partial composite failure
Raised as an Open Question; belongs to an implementation-realization ASN, not this abstract spec.

VERDICT: REVISE
