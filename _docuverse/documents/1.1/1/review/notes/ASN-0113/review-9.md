# Review of ASN-0113

## REVISE

### Issue 1: J4 (ForkComposite) mischaracterized in the W12 reachability construction
**ASN-0113, "What the pair reveals…" (W12 proof)**: "Equivalently, one may invoke ASN-0047's J4 (ForkComposite), which already bundles the K.δ/K.μ⁺/K.ρ steps into a single valid composite; we spell out the per-position composite here because the construction varies one subspace at a time."

**Problem**: This aside is inaccurate on two counts, and the inaccuracy concerns the one genuinely non-trivial proof in the ASN (the profile-reachability argument).
- J4 is a *fork*: its K.δ step creates a **new** document `d_new ≠ d_src` (K.δ case (ii)), so it cannot "equivalently" add a content position to the *existing* `d` whose profile W12 is driving.
- J4's K.μ⁺ step populates `M'(d_new)` from the **source** document's existing range via the order-preserving bijection `φ` — it contains **no K.α** and allocates no fresh content (`ran(M'(d_new)) = ran(M(d_op)|…)`, ASN-0047 J4). The per-position text composite W12 actually relies on *is* `K.α + K.μ⁺ + K.ρ` (fresh allocation). The two are materially different — J4 reuses I-addresses, the W12 composite allocates them — so J4 cannot serve as an equivalent witness, and in any case presupposes a pre-existing source with the target content (regressing the very reachability claim).

**Required**: Delete the J4 sentence, or restate it correctly — J4 is not an alternative route to the per-position construction. The standalone `K.α + K.μ⁺ + K.ρ` (and `K.λ + K.μ⁺_L`) composites already discharge W12; the J4 cross-reference adds only a false equivalence.

### Issue 2: W4 main-text justification attributes confinement to the wrong bound
**ASN-0113, "The extent span covers its subspace exactly" (W4 derivation)**: "By T1, `start_S = [S,1,…,1] ≤ t` forces each leading component to meet its floor; combined with `t < [S,1,…,1,1+n_S]`, the only freedom is in the last component…"

**Problem**: The lower bound `start_S ≤ t` does **not** confine the prefix to `[S,1,…,1]`. Lexicographic `≥` is not componentwise `≥`: `[S,2,1] ≥ [S,1,1]` holds, yet `[S,2,1]` has prefix `[S,2]`. Every component of `t` is already `≥ 1` by `VSlice` membership, so "forces each leading component to meet its floor" adds nothing. The actual exclusion of off-prefix tumblers comes from the **upper** bound together with T5 — exactly as the parenthetical (and the depth-3 worked instance with `[S,2,1] > reach`) demonstrates. As written, the prose attributes the load-bearing step to the wrong premise.

**Required**: Make the T5 parenthetical the primary argument: the shared prefix `[S,1,…,1]` (length `m_S − 1`) of `start_S` and `reach`, with `start_S ≤ t < reach`, confines every interior `t` to that prefix (T5), after which the last component is pinned to `1..n_S`. Drop or correct the "lower bound forces each leading component to meet its floor" claim.

## OUT_OF_SCOPE

None. The ASN correctly confines itself to the per-subspace V-extent query and defers content delivery, single-overall-extent reconciliation, link counting/discovery, version-fork permanence, and transclusion to the listed future operations (its Open Questions, not claims).

VERDICT: REVISE
