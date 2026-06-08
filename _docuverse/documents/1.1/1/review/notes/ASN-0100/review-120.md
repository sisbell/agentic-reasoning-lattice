# Review of ASN-0100

I checked the substrate decomposition, the three-region effect specification, every worked example, the full invariant-preservation argument against `ExtendedReachableStateInvariants`, the `INS.proj` derivation, the wp analyses, and the atomicity/uniqueness reasoning. The technical content is unusually complete: all per-state invariants in the foundation theorem are addressed, boundary cases (prepend, append, empty document, deep subspace `m_C=3`, re-insertion into a cleared subspace) are each verified, and the `I3` reuse via `INS.I3-coincide` is correctly scoped to the `Left ∪ Shifted-right` restriction. I found no substantive rigor error. The findings below are precision/anti-bloat items, consistent with this note's `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: "Split K.μ⁺" presented as decomposition freedom understates the contiguity constraint
**ASN-0100, Atomicity and Canonical Order (uniqueness discussion)**: "K.μ⁻ retention parameters may range over {0, 1, …, p_m − 1} … *K.μ⁺ may be split across multiple firings* … provided each intermediate satisfies the per-state invariants."
**Problem**: The blanket hedge is technically correct, but the example invites the reader to treat splitting as freely available alongside the genuinely-free K.α/K.ρ reorderings. It is not: a K.μ⁺ split that adds the Shifted-right positions before the Insertion positions produces a non-contiguous intermediate `V_{s_C}` (e.g. `{[1,1],[1,2],[1,5],[1,6],[1,7]}` with a gap at `[1,3],[1,4]`), violating D-CTG★/D-SEQ★ at that intermediate. So almost every split ordering is *forbidden*, the opposite of the freedom the prose suggests.
**Required**: Either drop the "split across multiple firings" example or add one clause stating that intermediate D-CTG★ forces Insertion-before-(or-with) Shifted-right within any split, so the ordering is constrained rather than free.

### Issue 2: Link-subspace out-of-scope stated redundantly (multiple-deferral pattern)
**ASN-0100, The Operation's Inputs**: "(The link subspace s_L is governed by a structurally similar but distinct extension operation; the present analysis does not cover it.)"
**Problem**: This parenthetical duplicates Bounding the Scope ("Insertion into the link subspace; the foundation's K.μ⁺_L is a structurally different operation…"), and the same boundary is raised a third time in Open Questions. The Inputs parenthetical is the redundant one — a mid-flow scope deferral to a downstream section, the exact accretion pattern the anti-bloat classifier targets.
**Required**: Drop the Inputs parenthetical; the scope boundary is fully and correctly stated in Bounding the Scope.

## OUT_OF_SCOPE

### Topic 1: Partial-failure recovery, self-composition, concurrency, derived document properties
**Why out of scope**: These are the ASN's own Open Questions and concern future operations/protocols (recovery semantics, BEBE, version derivation). They are correctly deferred, not errors in this note.

VERDICT: REVISE
