# Review of ASN-0087

## REVISE

### Issue 1: D-CTG★ proof discharges a case the operation's own convention excludes
**ASN-0087, Invariant Preservation (D-CTG★ paragraph)**: "MAKELINK commits the canonical depth `m_L^{Σ'}(d) = 2` for every first link it places (M-DepthConv), and S8-depth then pins `m_L(d) = 2` for all later link V-positions... at that depth the slice is exactly `{[s_L, k]}` and last-component contiguity is the whole claim. We nonetheless discharge the interior-component step for arbitrary `m_L^{Σ'}(d) ≥ 2`, keeping the argument independent of how `m_L(d) was established."

**Problem**: The interior-component argument (the `z_j > 1` / least-`j` / T1 case (i) apparatus) only has content when `m_L ≥ 3`, since at depth 2 there are no interior positions. But M-DepthConv asserts MAKELINK places every first link at `m = 2` and that S8-depth then pins `m_L(d) = 2` thereafter — which presumes MAKELINK is the sole producer of link V-positions. Under that framing, `m_L(d) > 2` is never reachable, so the interior-component paragraph proves contiguity for a configuration the ASN's own convention guarantees cannot arise. This is the "paragraph imagines a case the precondition/carrier already excludes" pattern. There is a genuine fork here, not merely a stylistic one: either (a) MAKELINK is the sole link placer, `m_L = 2` always, and the interior argument is dead code; or (b) some other operation can set `m_L(d) > 2` before MAKELINK runs, in which case M-DepthConv's claim that "S8-depth pins `m_L(d) = 2`" is unjustified.

**Required**: Commit to (a) and reduce the D-CTG★ discharge to the one-line depth-2 argument the convention actually produces (the post-state `V_{s_L}^{Σ'}(d)` is an initial segment `{[s_L, k] : 1 ≤ k ≤ K}`, so every in-range `[s_L, k]` is present); or, if `m_L > 2` is reachable, correct M-DepthConv's pinning claim and justify the general argument as live.

### Issue 2: S2 cross-subspace exclusion cites the wrong source for `v₁ = s_C`
**ASN-0087, Invariant Preservation (S2 derivation)**: "*Cross-subspace exclusion:* `v_ℓ ∉ V_{s_C}(d)`. By construction `(v_ℓ)₁ = s_L`, while by S8a every `v ∈ V_{s_C}(d)` has `(v)₁ = s_C`."

**Problem**: S8a constrains `zeros(v) = 0`, `#v ≥ 2`, and component positivity — it does not fix the value of the first component. That `v ∈ V_{s_C}(d) ⟹ v₁ = s_C` follows from the *definition* of `V_{s_C}(d) = {v : subspace(v) = s_C}` together with `subspace(v) = v₁` (SubspaceProjection, ASN-0036), not from S8a. The conclusion is correct but the cited justification does not establish it.

**Required**: Cite the definition of `V_{s_C}(d)` and the subspace projection (`subspace(v) = v₁`) instead of S8a.

## OUT_OF_SCOPE

(none)

VERDICT: REVISE
