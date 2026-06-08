# Review of ASN-0110

## REVISE

### Issue 1: "Matches Gregory" claim conflates slot-length with empty-slot-in-position; leaves a completeness gap for arity > 3
**ASN-0110, RE-arity**: "`retrieveendsets(I, Σ) = ⟨E₁(I, Σ), …, E_{N_max(Σ)}(I, Σ)⟩`, a tuple of length `N_max(Σ)`… This matches Gregory's implementation, which always emits the three standard slots (from, to, type)."

**Problem**: The abstract result has length `N_max(Σ)`, which can exceed 3 when a higher-arity link (L3 admits `N ≥ 3`) is present in the store. Gregory emits exactly 3 slots. So the *length* does not match whenever `N_max(Σ) > 3` — the "matches" only covers the empty-slot-in-position discipline, not the tuple shape. Worse, this creates an unaddressed conformance gap against RE-exact/RE-complete: if an arity-5 link touches `I` at slot 4, then `E₄(I, Σ) ≠ ∅`, and a 3-slot implementation would violate RE-complete by omitting it. The ASN notes elsewhere that "the model admits N ≥ 3" but never reconciles this with the conformance obligation.

**Required**: Either (a) scope the operation's return to the three standard slots and state explicitly that higher-arity slots are out of scope, or (b) keep length `N_max(Σ)` and qualify the evidence note — Gregory's 3-slot emission is conformant only for stores whose links are all arity 3; reconcile RE-complete for slots `> 3` accordingly.

### Issue 2: Misattributed foundation citation in RE-overlap
**ASN-0110, RE-overlap**: "each membership test a pair of tumbler comparisons (SC, ASN-0053)."

**Problem**: SC (SpanClassification, ASN-0053) classifies the relationship between *two spans* by comparing their starts and reaches. The test invoked here is point-in-span membership, `s ≤ α < s ⊕ ℓ` — two comparisons under the tumbler total order, which is T1 (LexicographicOrder) / T2 (IntrinsicComparison, ASN-0034), not SC. RE-decide correctly cites T2 for the same predicate, so the two statements disagree on the governing foundation.

**Required**: Cite T1/T2 (ASN-0034) for the point-membership comparisons in RE-overlap, matching RE-decide.

## OUT_OF_SCOPE

### Topic 1: V-space presentation contract for partially-arranged endsets
**Why out of scope**: The ASN correctly defers (in its Open Questions) the lossy projection of a returned whole endset back into a querying document's V-coordinates when the document arranges only part of the coverage. This is a separate presentation operation, not a defect in endset retrieval.

VERDICT: REVISE
