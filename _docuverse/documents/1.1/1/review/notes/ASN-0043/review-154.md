# Review of ASN-0043

I read the note in full and checked each proof, the FSP/FSE/CPP machinery, the PrefixSpanCoverage lemma (both inclusion directions), the L9 ghost construction (Cases A and B), and all six worked-example extension steps. The reasoning is sound and the worked example exercises L5/L8/L3/L6 non-vacuously (multi-span, multi-arity, discrimination, coverage-vs-decomposition). I found one citation-precision defect against the note's own per-step citation convention.

## REVISE

### Issue 1: L9 cites T0(a) for an ℕ-cardinality fact it does not supply
**ASN-0043, L9 — TypeGhostPermission, *Witness***: "Choose a subspace identifier `s_X ∈ ℕ` with `s_X ≥ 1`, `s_X ≠ s_C`, and `s_X ≠ s_L` (such `s_X` exists by T0(a)'s unbounded positive component values: infinitely many naturals differ from the two fixed constants `s_C`, `s_L`)."

**Problem**: T0(a) (UnboundedComponentValues) is an existence statement about *tumblers* with arbitrarily large components — its postcondition produces a `t' ∈ T` whose component at position `i` exceeds a bound. The fact actually needed here is purely about ℕ: that there exist at least three distinct naturals `≥ 1`, so one avoids the two constants `s_C, s_L`. That is discharged by NAT-closure (successor closure yields `1, 1+1, 1+1+1`) together with NAT-order/NAT-addcompat (`n < n+1` gives distinctness) and trichotomy — not by tumbler-component unboundedness. The note adopts an explicit per-step citation convention (visible throughout the foundation, e.g. T10a-N's meticulous splitting of ℕ steps into discreteness / order-compatibility / successor), and by that standard appealing to T0(a) for an ℕ-cardinality fact is the wrong axiom. Note the *second* T0(a) appeal in the same proof ("element-field component values are unbounded, so infinitely many element-level tumblers ... exist") is correct — it genuinely needs tumbler-component unboundedness; only the `s_X`-selection appeal is misattributed.

**Required**: Cite NAT-closure (with NAT-order/NAT-addcompat for distinctness) — or simply "ℕ contains more than two values" — for the existence of `s_X ∈ ℕ≥1 ∖ {s_C, s_L}`, reserving T0(a) for the subsequent tumbler-existence step where it is the correct source.

## OUT_OF_SCOPE

### Topic 1: Global content-subspace residence
The disjointness guarantees (L0, L14, L14a, L1d(b)) are scoped to `s_C`-resident states. The note flags this explicitly in Open Questions (whether to fix a global content-subspace constant so disjointness extends to all of `dom(Σ.C)`).
**Why out of scope**: This is a content-side invariant strengthening, properly deferred — not a defect in the link model as stated.

### Topic 2: L12b not verified in the worked example
L12b (HomeDocumentPersistence) is derived in the body (L1a at `Σ'` plus L12a) but not checked concretely against the worked example.
**Why out of scope**: L12b is a transition corollary with an explicit body derivation; the worked example's per-step note that L12/L12a hold across each transition covers the premise. Adding a concrete L12b trace would be incremental, not corrective.

VERDICT: REVISE
