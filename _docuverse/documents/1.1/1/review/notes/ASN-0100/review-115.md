# Review of ASN-0100

I checked every proof obligation against its preconditions, walked all boundary cases (empty document, prepend `j=0`, append `j=N`, interior, deep subspace `m_C=3`, residual content under an empty arrangement), and verified the hard invariants (D-CTG★ tiling with off-prefix exclusion, S2 region disjointness, the composite-boundary vs. per-state invariant split). The argument holds.

## REVISE

None.

Specific things I confirmed rather than took on faith:

- **Tiling (D-CTG★).** The closed-interval reduction is complete: off-prefix slice tuples (e.g. `[1,2,1]`) are genuinely excluded by T1 case (i) at the first off-prefix divergence, and the arbitrary-pair case is reduced to the extremes via `min`/`max` being least/greatest of `Pref(m,K)`. The `m=2` degenerate and the deep `m_C=3` example both check.
- **S2 disjointness.** The last-component comparisons are sound because shared prefix `[s_C,1,…,1]` is first established from pre-state D-SEQ★ (and ValidInsertionPosition (d) for `p`), so `v<p ⟺ v_{m_C}<p_m` is a restatement of the order, not an assumption.
- **Provenance coupling.** P7a/P4★/P4a are correctly classified composite-boundary-only; the post-K.α intermediate legitimately violates P7a (a_k in C, not yet in R) and this is permitted. J1★'s range-basis correctly exempts Shifted-right addresses (already in the content-subspace range at both Σ and Σ′).
- **K.μ⁻ omission.** Firing iff `Right ≠ ∅` is consistent with ValidComposite★ (K.μ⁻ need not appear); the strict-contraction obligation `n'_{s_C}=p_m−1<n_{s_C}` is discharged exactly when K.μ⁻ fires.
- **Empty vs. residual-content branch.** The keying on `dom(C)` (not the arrangement) is handled, and the empty-case invariant verification is on V-positions, so it covers both the first-emission and residual sub-branches uniformly.
- **I3 reuse.** Citing I3-S2/S3/VP/VD/fin for Left ∪ Shifted-right is legitimate — that set *is* I3's vacated-gap arrangement, with Insertion layered on via the independently-proved cross-region disjointness.

Anti-bloat pass: the forward-reference prose is largely already consolidated. The two forward defers (`§Effect One → §Identity`, `§Cross-document → INS.proj established below`) point to *different* locations and each genuinely aids navigation, so they do not match the compounding-deferral pattern. The §Atomicity invariant enumeration is exhaustive by necessity (every ExtendedReachableStateInvariants conjunct), not noise. No drift into implementation mechanics.

## OUT_OF_SCOPE

### Topic 1: Link-subspace insertion (K.μ⁺_L / K.λ)
**Why out of scope**: Explicitly excluded by the Scope block and by §Bounding the Scope; the foundation's link extension is a structurally distinct operation.

### Topic 2: Self-composition closure, concurrency, derived document metadata
**Why out of scope**: Raised correctly in §Open Questions as future territory (composition algebra, serialisation policy, derived-vs-primitive state) — none is a missing element of the single-operation per-state contract this ASN specifies.

VERDICT: CONVERGED
