# Review of ASN-0077

I have read this ASN carefully against the foundation ASNs (0034, 0036, 0047, 0053, 0058) and against Dijkstra's standard. The argument is methodical, the case analyses are exhaustive, and the discipline of citing foundation results step by step is maintained throughout.

The structural projection at the heart of the operation (O0, O3) is correctly grounded: S7 of ASN-0036 supplies the dom(C) case, and the extension to dom(L) in O0(b) properly threads together L1c (structural seed), K.λ's precondition (semantic binding), and closure of dom(L) under K.λ alone (frame analysis transition-by-transition). The closure step is non-trivial — the ASN explicitly inspects each transition's effect and frame rather than waving at the convention.

The lift to I-spans (origins_I) and V-spans (origins_V) is built carefully. The three forms F1, F2, F3 are explicitly proven equivalent, and the ASN correctly routes through C1a's block decomposition rather than ASN-0058's resolve function — a choice that matters because resolve's C1 integrity is restricted to dom(C) while the V-span operation must also admit link-subspace queries. O2's block uniformity proof handles content blocks via M16a and link blocks via CL-OWN, with M-sub(a) bridging the subspace antecedent on each side. The asymmetry (no "M16a for dom(L)") is genuine but does not break the argument, because CL-OWN gives the same conclusion more directly.

The permanence story is layered correctly:
- O5 is pointwise permanence, discharged via P3's dom-monotonicity and O3's purity.
- O6 gives I-span growth via P0.
- O7 gives V-span stability under a frame condition (restriction unchanged).
- O11 and O11' separately discharge monotonic growth under K.μ⁺ and K.μ⁺_L, with the worked example exhibiting why no parallel claim holds under K.μ~ — the swap of [1,1,3] and [1,1,7] sends origin {d₁} to {d₃} at the singleton σ_3, neither set a subset of the other.

The "loss of admissibility" framing for K.μ⁻ contraction (a previously well-formed V-span query becomes unposable rather than producing a wrong answer) is exactly right and resolves what could otherwise look like a non-monotonicity scandal.

The singleton I-span edge case argument is long but every step is discharged — the #b > #a case correctly chains S7a + S7d (same origin from structural agreement) → L0 + SubAllocatorAxiom (a),(e) (route to A_C(d) alone) → K.α's algorithmic structure (only inc(·, 0) for subsequent emissions) → TA5(c) (length preservation) → contradiction with #b > #a. The subtlety that T10a abstractly permits child-spawning but K.α's algorithm structurally precludes it for A_C(d) is acknowledged rather than glossed.

The wp computations are non-trivial (single-origin characterization for I-span, queryable-membership for V-span), the read-only frame is explicit (O10), and the worked example exercises O4, O5, O6, O7, O9, O10 and a K.μ~ failure mode and a K.μ⁻ admissibility-loss mode.

The Open Questions are well-targeted at genuinely future work — cross-subspace I-span lift, intermediate-chain surfacing, native-vs-transcluded distinction, unreachability behavior, historical containment, intra-document sharing per-position reporting.

No hand-waves, no checkmark proofs, no "by similar reasoning" elisions, no missing edge cases that fall within the operation's stated scope, no cross-ASN references beyond foundations.

VERDICT: CONVERGED
