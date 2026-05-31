# Review of ASN-0043

I read the ASN against the foundation contracts and re-derived the key constructions (PrefixSpanCoverage, the L1c chain, FSP/FSE, the L11a single-tree embedding, and all six worked-example steps). The mathematics is sound — the coverage equalities, the unique-`k'=1` routing, the freshness/producibility arguments, and the L8 coverage-vs-decomposition checks all hold. My findings are confined to the forward-reference / meta-prose accretion the `review-mode.anti-bloat` classifier flags.

## REVISE

### Issue 1: L1c's opening sentence restates the T10a foundation rather than advancing the axiom
**ASN-0043, L1c — LinkAllocatorConformance**: "Link allocation operates within a system conforming to T10a (AllocatorDiscipline, ASN-0034): link addresses are produced by allocators that use `inc(·, 0)` for sibling allocation and `inc(·, k')` with `k' ∈ {1, 2}` (within the TA5a bounds) for child-spawning."
**Problem**: This is a near-verbatim re-statement of T10a's own axiom ("Allocators produce sibling outputs exclusively by `inc(·, 0)`; child-spawning uses exactly one `inc(·, k')` with `k' ∈ {1, 2}`…"). The substantive content of L1c is the *Chain* existential that follows; the opening sentence re-explains a verified foundation the reader already has, adding no reasoning. It is exactly the "prose that does not advance reasoning" the anti-bloat pass targets.
**Required**: Reduce the opening to the load-bearing claim — that link addresses are T10a-conforming allocator outputs — and let the *Chain* clause carry the discipline detail, without re-listing the `inc(·,0)` / `inc(·,k')` rules already fixed by T10a.

### Issue 2: The L0a disjointness derivation is presented before the invariants it depends on
**ASN-0043, L0a — ContentSubspaceScope** (and L0b): the disjointness `dom(Σ.L) ∩ dom(Σ.C)|_{s_C} = ∅` is derived in-place using "By L1 (below), `zeros(a) = 3`…" and "T4-validity is discharged … for `a ∈ dom(Σ.L)`, by L0b (LinkAddressValidity)", while L0b is itself stated as "Derived from L1c's chain (LinkAllocatorConformance, below)".
**Problem**: This load-bearing derivation (the "L0a discharge" is later invoked by L0, L9, L11b, FSP, L14, L14a, and the worked example) rests on L1 and L1c, both stated *after* it. A reader checking the disjointness proof must jump forward past several invariants to find its premises, and L0b — a theorem — is placed in the L0 cluster far above the L1c chain that justifies it. This is forward-reference accretion: a proof appearing before its premises.
**Required**: Reorder so L1, L1b, and L1c precede the L0a disjointness derivation (or relocate the derivation after L1c), so the discharge is read with its premises already in hand rather than via "(below)" pointers.

## OUT_OF_SCOPE

### Topic 1: Link-store / content-store consistency under transclusion
The interaction between `Σ.L` and shared I-addresses appearing in multiple arrangements is correctly deferred (it is already listed under Open Questions). It is new territory for a later ASN, not a gap in this one — no action needed here.

VERDICT: REVISE
