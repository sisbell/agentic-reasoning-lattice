# Review of ASN-0112

The ASN is in good shape structurally — the V2 covering proof's two-case depth analysis is genuinely complete, the worked example exercises both the equidepth and depth-divergent regimes, and the wp analysis is non-trivial. Four issues remain: two proof-rigor gaps where the cited lemma does not discharge the stated claim, one exhaustiveness gap in V18's case analysis, and one anti-bloat duplication.

## REVISE

### Issue 1: V5's exact-cover proof mis-attributes the boundary argument to D-CTG★
**ASN-0112, "Exact cover within a subspace"**: "`⟦σ_d⟧` restricted to depth-`m_s` positions of subspace `s` is exactly that run — D-CTG★ rules out any occupied-depth position of `s` lying between `origin_d` and `reach_d` but outside the run."

**Problem**: D-CTG★ constrains only slice tuples lying between two members of `V_S(d)`. Since `reach_d ∉ V_S(d)`, D-CTG★ is silent on the half-open cell `(max O(d), reach_d)`, and it is likewise silent on depth-`m_s` tumblers that are not slice tuples (zero components, or first component ≠ s). The claim as recorded — "⟦σ_d⟧ contains no occupied-depth position outside O(d)" — quantifies over *all* depth-`m_s` tumblers, so two steps are missing: (i) *prefix-pinning* — any depth-`m_s` tumbler `t` with `origin_d ≤ t < reach_d` must agree with `[s,1,…,1]` on positions `1..m_s−1`, because `origin_d` and `reach_d` share that prefix, and a first divergence at `j ≤ m_s−1` with `t_j = 0` forces `t < origin_d` while `t_j ≥ 2` forces `t > reach_d`; (ii) *discreteness at the boundary cell* — the final component then satisfies `1 ≤ t_{m_s} < n_s + 1`, and no natural lies strictly between `n_s` and `n_s + 1`, so `t_{m_s} ≤ n_s` and `t` is in the D-SEQ★ run. Step (ii) is exactly the TA5 least-same-length-successor tightness of `inc(max O(d), 0)` that the ASN already establishes in the V3 paragraph but does not connect here. D-CTG★ legitimately covers only the sub-range `origin_d ≤ t ≤ max O(d)`.

**Required**: Replace the one-line D-CTG★ citation with the explicit two-step argument (prefix-pinning, then discreteness/TA5 tightness at the `(max O(d), reach_d)` cell), citing D-CTG★ only for the `t ≤ max O(d)` portion.

### Issue 2: V6's formal statement is too weak to express the dichotomy, and the wp(Exact) derivation relies on the missing strength
**ASN-0112, "Two subspaces: a bridging bounding box" and "Preconditions and well-definedness"**: V6 is recorded as "`O(d) ⊊ ⟦σ_d⟧` strictly — the span is a bounding box, not an exact cover"; the wp derivation then reasons "if `O(d)` occupies *both* subspaces, V6 gives `O(d) ⊊ ⟦σ_d⟧` strictly — … — so `¬Exact`."

**Problem**: `O(d) ⊊ ⟦σ_d⟧` holds for *every* non-empty document, including the single-subspace exact-cover case: the zero-extension `origin_d.0` satisfies `origin_d < origin_d.0` (T1 case (ii)) and `origin_d.0 < reach_d` (divergence at position `m_s`, `1 < n_s + 1`), so it lies in `⟦σ_d⟧ \ O(d)` whenever `n_s ≥ 1`. Strict inclusion of the denotation therefore does not distinguish bounding box from exact cover — `Exact` is depth-scoped and `⊊` is not — and the wp step "V6 gives ⊊ … so ¬Exact" is a non sequitur as written. What actually discharges `¬Exact` is the witness `w⋆ = [s_C,1,…,1,n_C+1]`, which is at the occupied depth `m_C`; that part of V6's proof is correct, but the recorded claim never says it.

**Required**: Restate V6 as the genuine negation of V5 — "in the multi-subspace case, `⟦σ_d⟧` contains an occupied-depth position outside `O(d)`" (witnessed by `w⋆`) — and route the necessity direction of wp(Exact) through that statement. The bare `⊊` can remain at most as a corollary, not as V6's content.

### Issue 3: V18's exhaustiveness argument skips the link-only regime
**ASN-0112, V18 paragraph**: "The remaining transitions leave content-occupancy status unchanged and so fix the origin: `K.μ⁺_L` (link-subspace extension) never touches `V_{s_C}(d)`, and `K.μ~` (reordering) preserves `O(d)` wholesale; a `K.μ⁺` into a content-present document and a `K.μ⁻` retaining at least one content position both leave `V_{s_C}(d) ≠ ∅` intact."

**Problem**: V18 claims the origin moves at *exactly* two transitions, so the fixity of every other transition must be proven — but the case analysis only addresses documents whose origin sits at the content anchor. Two in-scope link-only sub-cases are unhandled: (a) `K.μ⁺_L` into a link-only document — there the origin is `[s_L,1,…,1]`, determined by `V_{s_L}(d)`, which the extension *does* touch; "never touches `V_{s_C}(d)`" is irrelevant to this case. Fixity actually follows from D-MIN★ at `S = s_L` plus `K.μ⁺_L`'s depth-preserving append (`v_ℓ = shift(max V_{s_L}(d), 1)` at depth `m_L(d)`), which preserves the minimum. (b) `K.μ⁻` on a link-only document retaining at least one link (`n'_{s_L} ≥ 1`) — this is not "retaining at least one content position," yet it keeps the document non-empty and so falls inside V18's scope; fixity follows because the retained initial segment contains `[s_L,1,…,1]`. Both sub-cases satisfy the claim, but the stated enumeration does not cover them, so the "exactly two points" exhaustiveness is unproven as written.

**Required**: Add the two link-only sub-cases with their D-MIN★-based discharge, or restate the remaining-transitions argument uniformly: every non-toggling transition preserves `min O(d)` because each non-empty subspace's minimum is pinned at `[S,1,…,1]` by D-MIN★ in both pre- and post-states, and content-occupancy status (unchanged by hypothesis) determines which pin the origin reads.

### Issue 4: V-ReachTight stated three times in one passage (anti-bloat)
**ASN-0112, end of the V2 covering proof**: "…is recorded by **V-ReachTight** (reach tightness): `reach(σ_d) = reach_d ⟺ #origin_d ≤ #reach_d`. Both directions are already discharged by V2's two covering cases above — case 1 … closes the round-trip to `r⋆ = reach_d`, and case 2 … computes `reach_d < r⋆` — so the reach attains the constructed endpoint exactly when the origin is no deeper than the reach."

**Problem**: The biconditional is stated formally, then both directions are restated with case labels, then the same biconditional is rendered a third time in prose ("the reach attains the constructed endpoint exactly when the origin is no deeper than the reach"). The third rendering adds nothing; this is the same content in different words within a single passage.

**Required**: Keep the formal statement and the one-sentence pointer assigning each direction to its V2 case; delete the closing prose restatement.

## OUT_OF_SCOPE

### Topic 1: Per-subspace extent reporting and the multi-subspace count invariant
**Why out of scope**: The V5/V6 dichotomy naturally motivates a per-subspace span-set report, and the ASN's first open question (relating extent to occupied count in the multi-subspace case) belongs there (RETRIEVEDOCVSPANSET territory). The ASN correctly defers rather than defining claims for it.

### Topic 2: Historical-version reports and correspondence-run composition
**Why out of scope**: Both are listed in the ASN's own open questions; faithfulness of version-snapshot reports and global-from-local span composition require version and run machinery not in this operation's remit. No claims are improperly introduced for them.

VERDICT: REVISE
