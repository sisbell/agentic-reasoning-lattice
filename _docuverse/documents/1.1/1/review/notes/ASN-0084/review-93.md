# Review of ASN-0084

I checked the algebra (singleton identification, truncated subtraction, width positivity), both well-definedness lemmas (R-PIV, R-SWP), the two permutations (R-PPERM, R-SPERM), R-COMM, R-BLK, and recomputed all six worked examples (3-cut, the three μ sub-cases, the empty-exterior boundary, and the non-S carry). The mathematics is sound — every postcondition, tiling argument, and example checks out, and the invariant-preservation audit covers all of S0–S8. My findings are confined to the prose patterns the anti-bloat classifier asks me to surface plus one scope question.

## REVISE

### Issue 1: Non-load-bearing "common refinement" framing in R-BLK Phase 1
**ASN-0084, R-BLK, "Interaction between successive cuts"**: "Splitting is therefore order-independent: the final partition is the common refinement of B by the cut set, with boundary positions exactly the union of B's run boundaries and {c₀, ..., c_{n−1}}."

**Problem**: The lemma's downstream consumer (Phase 2 classification) needs exactly one fact from this paragraph: *after Phase 1 no run straddles a cut*. That fact follows immediately from "Phase 1 splits at every cut interior to a run" — the sentence that already closes the paragraph. The order-independence claim and the "common refinement / boundary positions are the union" characterization are never used anywhere in R-BLK or the examples. This is essay content inserted into a structural slot; the reader must work past it to reach the operative conclusion.

**Required**: Delete the order-independence / common-refinement sentences. Keep only "After all cuts are processed, no run straddles any cut position cᵢ, since Phase 1 splits at every cut," which is what Phase 2 consumes.

### Issue 2: R-CS3 is design rationale, not a state/operation/invariant property
**ASN-0084, R-CS3 (SubspaceConfinementNecessity)**: "CS3 is not redundant with CS2 + R-PRE(iv): a cut sequence whose every cut lies in a subspace S'' > 1 satisfies CS1, CS2, CS4, and R-PRE(i), (ii), (iv), while violating CS3 ... CS3 is the sole clause that excludes it."

**Problem**: R-CS3 establishes nothing about the system's state, operations, or invariants — it argues that one clause of *this ASN's own definition* is not derivable from its other clauses. An alternative implementation does not need to "satisfy R-CS3"; it is internal justification for the definition's shape, which is the "explains why a clause is needed rather than what it says" drift pattern. This is weaker than the foundation's T10a-N, which establishes that a *discipline restriction* is necessary for a load-bearing structural guarantee (non-nesting → partition independence). R-CS3 only rules out a vacuous-quantification degeneracy among sibling definitional clauses.

**Required**: Remove R-CS3, or demote it to a one-line remark attached to CS3 ("CS3 is not implied by CS2+R-PRE(iv): an all-higher-subspace cut sequence passes R-PRE(iv) vacuously while collapsing the regions"). The standalone lemma, counterexample, and properties-table row are disproportionate to the point.

## OUT_OF_SCOPE

### Topic 1: k-cut generalization (k > 4) and composition of rearrangements
**Why out of scope**: The natural class of cut-point permutations for k > 4 and whether the composition of two rearrangements is itself a single rearrangement are genuinely new territory, correctly listed as open questions rather than gaps in the 3/4-cut treatment.

### Topic 2: Weakest-precondition analysis of REARRANGE_K
**Why out of scope**: The forward obligation (every S0–S8 invariant is preserved) is fully discharged here. The wp question — what R-PRE(iv) guarantees beyond D-SEQ — is a backward-direction refinement appropriately deferred to a future ASN, and the open-questions section already frames the non-trivial version of it.

### Topic 3: Recovery of the canonical (maximal) partition from B'
**Why out of scope**: R-BLK correctly produces a *valid* partition and notes (via the 4-cut example) that B' may be non-maximal; the merge-to-canonical procedure and its confluence are legitimately future work, not an error in R-BLK.

VERDICT: REVISE
