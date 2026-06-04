# Review of ASN-0101

This note carries the `review-mode.anti-bloat` classifier. My findings center on forward-reference accretion and duplicated proof obligations. I checked the core proofs (D0 reduction, D1 gap closure, D8 source-correspondence, D9/D11 projection and wp, the three worked examples) and found no correctness errors — the deletion algebra, the σ_d bijection, and the wp pullbacks are sound. The issues below are structural/bloat, which in this mode are REVISE-level.

## REVISE

### Issue 1: "Boundary cases" forward-references and duplicates D8

**ASN-0101, "Boundary cases"**: "We enumerate configurations that stress different parts of the specification, verifying that D0 and **D8** hold uniformly." ... "Tracing **D8's Group (i) clauses** on the affected subspace" ... "transfer to the post-state under the **source-correspondence argument from D8's Group (i) justification**."

**Problem**: The Boundary cases section precedes "What is preserved," where D8 is first stated. The section discharges D8 clause-by-clause for each configuration (empty, start, end, singleton, interior) and explicitly *defers forward* to "D8's Group (i) justification" — a justification the reader has not yet seen. D8's own Group (i) proof then re-derives the same source-correspondence facts (S8a, S8-depth, S2, S3★, S3★-aux, CL-OWN, CL-UNIQ) generally. The reader must skip ahead to D8 to follow the boundary section, then re-read the same argument in D8. This is the forward-reference accretion pattern ("multiple paragraphs defer to the same downstream location").

**Required**: State D8 (with its general source-correspondence justification) before the boundary cases, and recast the boundary cases as *instantiations* of D8 at specific `(p, n, n_S)` rather than independent per-clause discharges. The boundary section should exercise D1/D8/D9 at the edges, not re-prove them.

### Issue 2: Empty-post-state vacuity taxonomy is meta-prose

**ASN-0101, "Boundary cases," empty post-state**: the three labeled buckets "*Vacuous-on-empty-set clauses*," "*Vacuous-on-empty-conditional clauses*," "*Non-vacuous clauses with constructive discharge*."

**Problem**: This taxonomy categorizes *how* each invariant discharges (which quantifier is empty, which antecedent is false) rather than advancing the argument. The categorization adds no content beyond "each Group (i) clause holds when `V_S(M'(d)) = ∅`," which D8 already covers via "When this set is empty (`n_S = n`), ... the predicates hold vacuously." It is the labeled-sub-paragraph meta-prose pattern.

**Required**: Replace the three labeled buckets with a single sentence noting the affected subspace's clauses discharge vacuously and the unaffected subspace inherits via D6.

### Issue 3: D7 over-justifies a partition immediate from L0 + L14

**ASN-0101, D7 Justification**: the "*Equivalently, restricted by subspace*" derivation — "if `subspace_I(a) = s_C`, then `a ∉ dom(L)` (since `a ∈ dom(L)` would force `subspace_I(a) = s_L` by L0, contradicting...), so `a ∈ dom(C)` by the partition; symmetrically..."

**Problem**: This ~150-word forward/contrapositive derivation restates the immediate consequence of L0 (subspace identifies store) and L14 (`dom(C) ∩ dom(L) = ∅`). The carrier facts (`a ∈ dom(C) ∪ dom(L)`, stores unchanged by D2/D3, origin structural) already establish D7; the subspace-partition restatement does not add a guarantee.

**Required**: Collapse to one sentence: by L0 and L14 the membership is partitioned by `subspace_I(a)`, and D2/D3 preserve both stores.

## OUT_OF_SCOPE

### Topic 1: D6 implementation-mechanism citation
**ASN-0101, D6 "Implementation evidence"**: "by two unrelated mechanisms (an exponent-guarded `tumblersub` short-circuit ... positional ordering of text below link addresses ...)." This names implementation mechanics; the abstract guarantee D6 is mechanism-agnostic. Not an error (it is cited as evidence, not as the claim), but the mechanism detail belongs to implementation notes, not the abstract D6 prose.

VERDICT: REVISE
