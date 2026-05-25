# Review of ASN-0075

## REVISE

### Issue 1: D-EXH mutual exclusion not derived

**ASN-0075, Lemma D-EXH proof**: After eliminating the impossible row, the proof asserts "The remaining three rows are mutually exclusive and exhaustive."

**Problem**: Mutual exclusion of CURRENT and NEVER_INCLUDED is not immediate from their definitions. CURRENT(a,d) ≡ a ∈ ran(M(d)) constrains only the arrangement; NEVER_INCLUDED(a,d) ≡ (a,d) ∉ R constrains only provenance. From the bare definitions, both could simultaneously hold at a state where a ∈ ran(M(d)) ∧ (a,d) ∉ R — exactly the "impossible row" that P4★ rules out. The mutual exclusion claim is thus load-bearing on the row elimination, but the proof leaves the dependency implicit. The reader must perform per-row label assignment to confirm.

**Required**: After eliminating the impossible row, enumerate the label assignment for each remaining row — e.g., "Row 1 (a ∈ ran(M(d)) ∧ (a,d) ∈ R): CURRENT holds; DELETED fails (a ∈ ran(M(d))); NEVER_INCLUDED fails ((a,d) ∈ R)" — and conclude mutual exclusion from per-row uniqueness. The exhaustiveness claim should likewise be derived: every (a,d) satisfying the hypothesis lies in one of the four rows by cross-product totality; eliminating row 2 leaves three.

### Issue 2: D-ACT "and conversely" leaves the converse implicit

**ASN-0075, Actionability section**: "two I-adjacent same-origin addresses may be non-V-adjacent in any particular witness's arrangement, and conversely, so the two notions of 'run' do not coincide."

**Problem**: "And conversely" leaves the converse statement implicit, with at least two plausible readings: (a) V-adjacent positions in a witness's arrangement may map to non-I-adjacent addresses, or (b) V-adjacent positions in a witness's arrangement may map to addresses with different origins. The substantive point — that witness-run decomposition is genuinely orthogonal to block decomposition — depends on which reading is intended.

**Required**: Replace "and conversely" with the explicit converse, e.g., "and V-adjacent positions in a witness's arrangement may map to non-I-adjacent or different-origin addresses."

### Issue 3: D-EXH "impossible row" argument requires the lemma's hypothesis to discharge L14

**ASN-0075, Lemma D-EXH proof**: "The precondition for `subspace_I(a)` to be well-defined is `a ∈ dom(Σ.C)`; by L14 (`dom(C) ∩ dom(L) = ∅`), we therefore have `a ∉ dom(L)`."

**Problem**: The derivation `a ∉ dom(L)` uses the lemma's hypothesis `a ∈ dom(Σ.C)` together with L14. But the proof phrases this as if the absence followed from `subspace_I(a) = s_C` being well-defined — that step is `a ∈ dom(C)` (lemma hypothesis), and L14 then gives `a ∉ dom(L)`. The hypothesis `subspace_I(a) = s_C` is *stronger* than mere well-definedness of `subspace_I` and is independently sufficient (`subspace_I(a) = s_C ≠ s_L` plus L0 gives `a ∉ dom(L)` directly). The reasoning works but the discharge is over-routed.

**Required**: Either route through L0 + SC-NEQ (which uses the lemma's full hypothesis `subspace_I(a) = s_C`) or route through L14 from `a ∈ dom(C)` (without invoking subspace well-definedness as the intermediate). The current chain conflates the two routes.

VERDICT: REVISE
