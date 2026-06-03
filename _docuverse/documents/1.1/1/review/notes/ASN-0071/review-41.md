# Review of ASN-0071

## REVISE

### Issue 1: Resolve-equivalence "matters only when" claim is incomplete — contradicted by the ASN's own cross-depth example

**ASN-0071, *Resolution***: "The relaxation matters only when `⟦σ⟧` contains positions outside `dom(M(d_s))`: ContentReference treats such a span as ill-formed, while vspec silently drops the missing positions."

**Problem**: This asserts a *single* axis of divergence between vspec resolution and well-formed-ContentReference resolution (missing positions). But the vspec preconditions (`subspace(u)=s_C`, `Pos(ℓ)`, `actionPoint(ℓ)=#u`, `#ℓ=#u`, `actionPoint≥2`) impose **no** constraint `#u = m` (the source's common content depth), whereas ASN-0058's ContentReference condition (iii) requires `#ℓ = #u = m`. The ASN's own *cross-depth query* exercises exactly this gap: for `(d_E, σ_E)` with `#u = 2 < m_C = 3`, all positions in `⟦σ_E⟧ ∩ dom(M(d_E))` are present (no missing positions), yet the vspec is **not** a well-formed ContentReference — it fails (iii), so `resolve(d_E, σ_E)` is not even defined. Thus the relaxation also "matters" on a second, independent axis (depth mismatch / shallow anchor capturing a deeper subtree) with zero missing positions, directly contradicting the "matters only when" wording.

**Required**: Amend the statement to acknowledge both divergence axes — (1) positions outside `dom(M(d_s))`, and (2) `#u < m` (the shallow-anchor / subtree-capture case the d_E example demonstrates) — or explicitly restrict the resolve-equivalence claim to vspecs satisfying `#u = m` and state that resolve is undefined (no equivalence to assert) when `#u ≠ m`.

### Issue 2: Roadmap and duality prose in structural slots (anti-bloat)

**ASN-0071, *The operation***: "The definition is brief. Everything FINDDOCSCONTAINING claims is contained in the predicate `ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ≠ ∅`. The remainder of this ASN unpacks what that predicate guarantees."

**ASN-0071, *Discovery through sharing***: "This makes `find` the structural dual of the read-direction. Reading goes from arrangement to content... Finding goes from content to arrangement... The two operations are duals over the same `M : E_doc → (T ⇀ T)` structure."

**Problem**: Neither passage advances a claim or its derivation. "The remainder of this ASN unpacks…" is a roadmap sentence; the duality paragraph is conceptual framing with no consequence drawn. Under the `review-mode.anti-bloat` classifier these are noise the reader must skip past.

**Required**: Delete the roadmap sentence; either cut the duality framing or compress it to the one operative fact (`find` and read are inverse traversals of `M`).

## OUT_OF_SCOPE

### Topic 1: Relationship between current-state `find` and historical relation `R`
**Why out of scope**: The ASN correctly flags this as an Open Question and the F-CUR discussion stays at the level of "what `find` does not promise." The invariant linking `find` to `R` across contraction is new territory, not an error here.

VERDICT: REVISE
