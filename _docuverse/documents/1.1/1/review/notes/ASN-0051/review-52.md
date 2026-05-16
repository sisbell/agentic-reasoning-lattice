# Review of ASN-0051

## REVISE

### Issue 1: SV5 proof notation conflates state-dependent and state-independent readings of the endset
**ASN-0051, Reordering Preserves Projection, Changes Resolution**: "`π_{Σ'}(e, d) = coverage(Σ'.L.e) ∩ ran(Σ'.M(d)) = coverage(Σ.L.e) ∩ ran(Σ.M(d)) = π_Σ(e, d)`"
**Problem**: The Endset Projection definition takes `e ∈ Endset` as a state-independent argument: `π(e, d) = coverage(e) ∩ ran(M(d))`. Writing `coverage(Σ'.L.e)` reads the endset off the link store with no link address `a` to anchor the slot lookup. The notation is ambiguous between (i) `e` as slot designator (which would need `Σ'.L(a).e` for some `a`), and (ii) `e` as a value (which makes the state subscript on coverage redundant). The middle equality then needs both K.μ~'s ran-preservation *and* L12 (for the coverage identity) when only ran-preservation is required by the proper unfolding.
**Required**: Either anchor the slot lookup with an explicit link address `a` (e.g., `Σ'.L(a).s` for the link whose endset is under analysis), or drop the `Σ'.L.` prefix and cite L12 once as the reason `coverage(e)` is well-defined identically at Σ and Σ' when `e` is sourced from `Σ.L(a)`.

### Issue 2: SV9 monotonicity proof's "L-frame transition" enumeration depends on L being implicitly framed in ASN-0047, but the cited frame conditions do not say so
**ASN-0051, SV7 proof**: "For the elementaries this is direct (per-transition effect, ASN-0047)"
**Problem**: Looking at ASN-0047's frame statements as quoted in the prompt, none of K.α, K.δ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.ρ explicitly assert `L' = L` in their frame clauses. The preservation of L's entries for these transitions comes from L12 (an invariant over all state transitions), not from per-transition effect. The proof's citation conflates the two sources.
**Required**: Replace "per-transition effect" with a citation to L12 (LinkImmutability) for entry preservation and L12a (LinkStoreMonotonicity) for domain non-growth under L-frame transitions. The conclusion is correct; only the routing needs tightening.

### Issue 3: SV11 attainment witness shows only the single-block case
**ASN-0051, SV11 attainment witness**: "the construction extended to m spans... over 2m − 1 sibling addresses in a single block witnesses attainment at arbitrary m with p = 1; multi-block (p ≥ 2) attainments are constrained by the suffix/prefix topology of cross-block-spanning coverage intervals and are not exhibited here."
**Problem**: The attainment claim is m · p, but the witness only exhibits p = 1. Saying multi-block attainment is "constrained by topology and not exhibited here" leaves open whether the m · p bound is actually attainable when p ≥ 2. A reader cannot tell whether m · p is genuinely the tight bound or whether some unexamined topological constraint reduces the achievable maximum below m · p when p ≥ 2.
**Required**: Either (a) exhibit a p ≥ 2 attainment witness (e.g., two non-injective blocks with carefully chosen spans hitting non-adjacent regions in each), or (b) prove the topology constraint and state the corrected bound for p ≥ 2 cases, or (c) explicitly weaken the claim to "m · p attainable for p = 1; the multi-block tight bound is left open."

### Issue 4: SV6 informal statement omits the structural restriction k > p₃
**ASN-0051, SV6 (CrossOriginExclusion)**: "For a span (s, ℓ) in an existing endset where s is element-level (zeros(s) = 3), and a newly allocated address b with zeros(b) = 3 and origin(b) ≠ origin(s): `b ∉ ⟦(s, ℓ)⟧`"
**Problem**: The informal statement reads as a universal claim about cross-origin element-level allocations, but the formal Precondition list (immediately below) adds the load-bearing `k > p₃` restriction. The same-origin coverage growth section later describes counterexamples (child-depth entry, broader-level spans) which a reader could mistakenly believe are excluded by the informal SV6 reading. SV13(f) restates with `k > p₃` explicit; the SV6 headline should match.
**Required**: Include "and the span's action point lies strictly within the element field (k > p₃)" in the informal statement, matching SV13(f)'s phrasing.

VERDICT: REVISE
