# Review of ASN-0100

This is a mature, rigorous note: the math is sound, the boundary cases (empty content subspace, append, prepend with forced full clearance, deep-subspace `m_C ≥ 3`, re-insertion into a cleared subspace) are each worked concretely, the `wp` analysis is genuinely non-trivial on two postconditions, consequences are derived (cross-document identity), and there are no non-foundation cross-ASN references. I verified the three-region disjointness arithmetic, the `INS.M-exhaustive` derivation, the projection-shift correspondence step-by-step (LP6/LP10/LP9/LP14 chain), the closed-interval D-CTG★ reduction at `m ≥ 3`, and the composite-boundary atomicity discharge — all hold.

The cycle is `review-mode.anti-bloat`. Prior cycles have evidently already done most of the trimming (the patterns the classifier targets are largely absent). I found two residual instances of the targeted meta-prose, both minor.

## REVISE

### Issue 1: Vacuous forward-deferral clause in INS.I3-coincide
**ASN-0100, §Discovering the Three Effects → "Identification with the foundation's post-insertion shift (INS.I3-coincide)"**: "...so the arrangement-only lemmas I3 establishes of that arrangement hold of M'(d) restricted to those two regions, **cited at point of use in the sections that need them**."
**Problem**: The trailing clause is exactly the forward-deferral meta-prose this cycle targets. It tells the reader nothing actionable — the sections that use `I3-VP`, `I3-VD`, `I3-fin`, `I3-S2` already cite them at use (each says "the inherited I3-X (§Effect Three)"). The clause is a hub-deferral pointer with no informational content; the reader skips it.
**Required**: Delete "cited at point of use in the sections that need them." The pointwise-identity equation preceding it already licenses the per-region inheritance.

### Issue 2: Restated scope clause in the S8★ section
**ASN-0100, §Per-subspace span decomposition (S8★)**: the paragraph first states "Condition (c) — uniqueness of the maximal-run decomposition, which **S8★ requires only on the content subspace** — is exactly C1a's uniqueness assertion..." and then closes with the parenthetical "**(Condition (c) is not required on the link subspace, where S8★ asks only for the trivial length-1 decomposition.)**"
**Problem**: The parenthetical restates the earlier clause in different words within the same paragraph ("required only on content" = "not required on link"). This is the "two sentences say the same thing in different words" pattern.
**Required**: Drop the closing parenthetical; the earlier in-line clause already scopes condition (c) to the content subspace.

## OUT_OF_SCOPE

None. The "Bounding the Scope" section correctly *excludes* DELETE/COPY/REARRANGE/link-subspace/version/replication rather than defining claims for them, so no out-of-scope claims were introduced.

VERDICT: REVISE
