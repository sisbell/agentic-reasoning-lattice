# Review of ASN-0061

## REVISE

### Issue 1: Invariant preservation claims "each" but omits P3, P4a, P5

**ASN-0061, Invariant Preservation section**: "We verify that DELETE preserves each foundation invariant."

**Problem**: Three ASN-0047 invariants are absent from the verification list: P3 (ArrangementMutabilityOnly), P4a (HistoricalFidelity), and P5 (DestructionConfinement). All three are trivially satisfied — P3 because the composite uses only contraction and extension modes with C' = C, E' = E, R' = R; P4a because R' = R introduces no new entries requiring historical justification; P5 because C' ⊇ C, E' ⊇ E, R' ⊇ R follow immediately from D-CF's equalities. But the claim of "each" creates an expectation the list is exhaustive, and in a specification that demands precision this expectation should be met.

**Required**: Either add the three one-line verifications or replace "each foundation invariant" with an explicit enumeration of the invariants verified.

---

The remaining content of the ASN is correct. I checked every proof against the foundations and found the following hold:

- **D-CTG**: well-formulated, base case (empty arrangement in Σ₀) verified, correctly positioned as a design constraint outside ASN-0047's reachable-state theorem.
- **D-PRE**: all seven items are necessary. The depth-restricted membership predicate in (v) correctly avoids the all-depths issue with span denotation. The reduction to endpoint bounds under D-CTG is valid at depth 2.
- **Three-region partition**: disjointness by trichotomy, exhaustiveness immediate, |X| ≥ 1 from w > 0 and TA-strict.
- **D-LEFT, D-DOM, D-SHIFT**: postconditions are self-consistent. The shift σ is well-defined: ord(v) ≥ ord(r) = ord(p) ⊕ w\_ord ≥ w\_ord (using p₂ ≥ 1 from S8a), so TA2 applies. Shifted ordinals are positive (minimum is ord(p) by D-SEP, positive by S8a).
- **D-CF, D-XD, D-XS**: frame conditions follow from K.μ⁻ and K.μ⁺ elementary frames. R' = R is established by the elementary frames directly (the J1 vacuity argument is a separate coupling-validity check, not the mechanism that establishes R' = R — the prose slightly conflates these, but the conclusion is correct).
- **D-BJ**: TA3-strict preconditions verified — equal depth (#ord = 1), both ordinals ≥ w\_ord, strict ordering. Order preservation implies injectivity.
- **D-SEP**: TA4 preconditions verified — action point k = 1 = #ord(p) = #w\_ord, zero-prefix condition vacuous at k = 1. The round-trip (ord(p) ⊕ w\_ord) ⊖ w\_ord = ord(p) is established by both direct calculation and TA4 citation.
- **D-DP**: all four cases verified. Case 3 (L ≠ ∅, R ≠ ∅) is the hardest — contiguity of L (D-CTG restricted below p), contiguity of Q₃ (constant-subtraction preserves unit gaps at depth 1), adjacency at ord(p) (predecessor p₂ − 1 exists since L ≠ ∅ implies p₂ ≥ 2). The argument that depth-1 ordinals are natural numbers is correctly scoped to D-PRE(iv).
- **Composite transition**: K.μ⁻ removes X ∪ R (strict contraction since |X| ≥ 1); K.μ⁺ adds Q₃ when R ≠ ∅ (strict extension since Q₃ ∩ (L ∪ non-S) = ∅). Intermediate-state preconditions verified: no V-position collision (L has ordinals < ord(p), Q₃ has ordinals ≥ ord(p), different subspace for non-S). K.μ⁺ correctly omitted when R = ∅.
- **Coupling constraints**: J0 vacuous (dom(C') = dom(C)); J1 vacuous (ran(M'(d)) ⊆ ran(M(d)), so ran(M'(d)) \ ran(M(d)) = ∅); J1' vacuous (R' \ R = ∅). Verified for both the R = ∅ and R ≠ ∅ cases.
- **D-BLK**: six block cases are exhaustive (verified by case analysis on the relationship between {v, v\_end} and {p, r}). The key step σ(v) + j = σ(v + j) — that the shift commutes with ordinal increment — is proven via (a − c) + j = (a + j) − c for natural numbers at depth 1. B1–B3 verification for the transformed decomposition is complete.
- **Domain completeness**: Q₁ ∪ Q₂ ∪ Q₃ partition verified — Q₁ disjoint from Q₂, Q₃ by subspace; Q₂ disjoint from Q₃ by ordinal (< ord(p) vs ≥ ord(p)). The ⊆ direction (no extraneous positions) follows from the composite consisting of exactly two elementary steps with explicit frames.
- **D-ORPH, D-PSTALE**: orphaning conditions correctly identified; the proof that no V-position in L ∪ Q₃ maps to the orphaned address is valid under the all-in-X hypothesis. Provenance staleness is an existential claim with a correct witness construction.
- **Worked example**: all postconditions verified against a concrete 5-position document. Block decomposition, contiguity, width reduction all check out.

## OUT_OF_SCOPE

### Topic 1: Generalization to ordinal depth > 1
**Why out of scope**: D-PRE(iv) restricts to #p = 2. The round-trip (D-SEP), shift commutativity (σ(v) + j = σ(v + j)), and contiguity preservation (D-DP) all depend on depth-1 ordinals being natural numbers. Generalizing requires proving TumblerSub commutes with ordinal increment at deeper levels, where TA4's zero-prefix condition is no longer vacuous.

### Topic 2: D-CTG preservation by other editing operations
**Why out of scope**: D-CTG is a cross-cutting invariant introduced here. Each operation's ASN must independently prove preservation.

### Topic 3: Version reconstruction and historical backtrack
**Why out of scope**: Orphaned content is permanent (S0) and attributable (S7), but the mechanism for recovering prior arrangements is a separate system capability.

### Topic 4: Document-discovery index semantics after deletion
**Why out of scope**: D-PSTALE establishes superset reporting as a consequence. Whether exact containment queries are required is a query-layer design decision.

VERDICT: REVISE
