# Review of ASN-0100

I checked the substrate decomposition, every invariant in ExtendedReachableStateInvariants (ASN-0047), all boundary cases, the wp analyses, and the cross-ASN reference discipline.

## REVISE

None.

The proof obligations are discharged at the level this ASN demands. Spot checks that usually expose gaps all hold:

- **Tiling without gaps (D-CTG★).** The closed-interval reduction handles the genuinely hard part — off-prefix slice tuples at depth `m ≥ 3` — and the deep-subspace worked example (`z = [1,2,1] > max` at the position-2 divergence) exercises it concretely rather than asserting it. The arbitrary-pair case is reduced to the extreme case via transitivity with the global min/max, not waved through.
- **Boundary cases.** Empty document (first insertion, with the correct `dom(C)`-keyed branch selection distinguishing residual-content from never-allocated), prepend (`j=0`, forced `n'_{s_C}=0` full clearance), append (`j=N`, K.μ⁻ omitted, `Right=∅`), interior, and deep-subspace are each worked and checked against the post-state invariants.
- **Exhaustiveness (INS.M-exhaustive).** Proved from the composite construction (K.α/K.ρ frame M, K.μ⁻ only removes, K.μ⁺ adds exactly two specified sets) rather than assumed — closing the "no fourth region" hole that functionality and S3★ both depend on.
- **Every invariant conjunct addressed.** S4, L0's two-conjunct split (the content clause over the *growing* `dom(C)` discharged per-fresh-address, not folded into the link clause), L14, P4★/P4a/P7/P7a, S8★ via the reused INS.C1a-app at both the post-state and the K.μ⁻ intermediate. The hard ones are not skipped.
- **Atomicity.** Per-state invariants are verified at the post-K.μ⁻ contraction intermediate (which has no I3 counterpart and gets an independent argument), and the forced-ordering analysis correctly conditions the K.μ⁻-before-K.μ⁺ ordering on K.μ⁻ actually firing.
- **wp analysis.** Two non-trivial cases (tight-endset discoverability preservation; provenance membership for a specific I-address), each properly conditioned (tightness at incorporation state) rather than computed only where the answer is trivially true.
- **References.** Every cited ASN (0034, 0036, 0047, 0058, 0082, 0093, 0098) is a foundation; no non-foundation reference, no reinvented foundation notation.

On the `review-mode.anti-bloat` lens: the COPY-aliasing contrast and "append-only / identity-by-creation" rationale recur across §Effect One, §Identity, and §Bounding the Scope, but these are statements of what the operation does or does not do — exempted from meta-prose by the stated rule — and their placements are in distinct argumentative contexts (freshness rationale vs. identity semantics vs. scope boundary), not redundant restatement of a single claim. No forward-reference accretion: the lone forward pointer (INS.proj from §Cross-document independence) is proved once below, and no document-ordering justification, axiom-rationale prose, or duplicated downstream deferral is present.

## OUT_OF_SCOPE

None to add. The ASN's own §Bounding the Scope and Open Questions correctly defer link-subspace INSERT, COPY, DELETE/REARRANGE, version derivation, replication, self-composition, and concurrency.

VERDICT: CONVERGED
