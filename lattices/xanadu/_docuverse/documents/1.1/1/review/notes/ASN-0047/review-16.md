# Review of ASN-0047

## REVISE

### Issue 1: K.μ~ decomposition — incomplete verification

**ASN-0047, Elementary transitions (K.μ~)**: "K.μ~ is a distinguished composite, not a primitive transition. When dom(M(d)) is non-empty, it decomposes into K.μ⁻ (removing all mappings) followed by K.μ⁺ (re-adding them at new positions)."

**Problem**: Two gaps in the decomposition.

**(a) Intermediate-state preconditions not verified.** The valid composite definition (condition (1)) requires each elementary step's precondition to hold at its intermediate state. After K.μ⁻ empties M(d), the K.μ⁺ step operates on an arrangement with dom = ∅. Its preconditions need explicit verification:
- Referential integrity (S3): every re-added I-address a must satisfy a ∈ dom(C) at the intermediate state. This holds because K.μ⁻'s frame preserves C, and S3 held at the pre-state (a ∈ ran(M(d)) ⊆ dom(C)). The argument is one sentence — but it is absent.
- S8a, S8-depth: the new V-positions satisfy these by K.μ~'s own precondition on π. Should be stated.
- d ∈ E_doc: unchanged by K.μ⁻ (frame).

**(b) Frame conditions stated, not derived.** K.μ~ is declared composite, yet its frame — "C' = C; E' = E; R' = R; ran(M'(d)) = ran(M(d)); (A d' : d' ≠ d : M'(d') = M(d'))" — is presented in the same format as the five primitives' frames, without derivation from the K.μ⁻ + K.μ⁺ composition. The P5 proof correctly derives K.μ~'s monotonicity property from the decomposition; the frame section and P4 proof do not. This creates a dual treatment: P4 appeals to K.μ~'s bijection definition directly ("Preserved independently of its decomposition"), while P5 derives from the decomposition.

Additionally, ran(M'(d)) = ran(M(d)) is not a frame condition — it is a defining property of the bijection. Frame conditions describe what is unchanged in components OTHER than the one being modified. Listing a constraint on how M(d) is modified alongside actual frame conditions conflates the two categories.

**Required**: Either (a) derive K.μ~'s properties from the decomposition (once), verifying intermediate preconditions, and cite the derivation in subsequent proofs; or (b) define K.μ~ by its bijection property as a sixth primitive, with the decomposition as a theorem. The current treatment claims composite status but exercises primitive privileges.

### Issue 2: Initial state Σ₀ — arrangement invariants not verified

**ASN-0047, Initial state / Valid composite (3b)**: The initial state Σ₀ is verified against P4, P6, P7, P8 (base cases explicitly stated in each derivation). The arrangement invariants S2, S3, S8a, S8-depth, S8-fin — which appear in (3b) — are not checked.

**Problem**: The induction proofs for P4, P6, P7, P8 each begin with an explicit base case at Σ₀. The arrangement invariants receive no such treatment. With (E₀)\_doc = ∅, no arrangements exist, making all five vacuously satisfied. But the induction over valid composites requires the base case to satisfy every conjunct of (3b). The asymmetry — four invariants with stated base cases, five without — leaves the base case formally incomplete.

**Required**: One sentence, e.g.: "At Σ₀, (E₀)\_doc = ∅, so S2, S3, S8a, S8-depth, and S8-fin hold vacuously — no arrangements exist."

### Issue 3: Valid composite definition — (3b) derivability

**ASN-0047, Definition (Valid composite transition)**: "(3b) State invariants: the final state Σ' satisfies P6, P7, P8, S2, S3, S8a, S8-depth, S8-fin, and Contains(Σ') ⊆ R'."

**Problem**: The ASN subsequently proves that every invariant in (3b) is maintained by any composite satisfying (1), (2), and (3a): P4 derives Contains ⊆ R from J1; P6, P7, P8 are derived by induction from the elementary preconditions and P0/P1; S2–S8-fin are preserved by each elementary transition's preconditions. This means (3b) is entirely redundant — a consequence of (1)+(2)+(3a), not an independent constraint. The definition does not note this. A reader encountering (3b) before the proofs may attempt to verify each invariant independently for each composite, not realizing the coupling constraints and elementary preconditions already guarantee them.

**Required**: Note that (3b) is derivable: "Conditions (3b) follow from (1), (2), and (3a); they are included to make the reachable-state invariants explicit."

## OUT_OF_SCOPE

### Topic 1: Provenance tracking for link endset references
**Why out of scope**: Links are modeled as entities in E_doc with arrangements, but the distinct semantics of endset-based content references (vs. arrangement-based display) may require additional provenance constraints. Acknowledged in the open questions.

### Topic 2: Subspace boundary constraints for K.μ~
**Why out of scope**: Whether reordering may move V-positions across subspace boundaries (e.g., text subspace to link subspace) is an arrangement-level constraint that belongs with the subspace semantics, not the transition taxonomy. Acknowledged in the open questions.

VERDICT: REVISE
