# Review of ASN-0098

## REVISE

### Issue 1: LP-Fin non-canonical extension to `#ℓ = #s` non-ordinal case is hand-waved
**ASN-0098, "Non-canonical spans yield infinite intersections" subsection**: "the same within-chain construction extends to that case (the divergence argument requires only `actionPoint(ℓ) < #s`, not `#ℓ < #s`)"
**Problem**: The argument for `#ℓ < #s` is carried out in full (with the chain-element divergence at position `k_ℓ`), but the extension to the `#ℓ = #s` non-ordinal-displacement case is sketched in a parenthetical. The cases differ in a structural respect: when `#ℓ = #s`, the post-comparison region (positions `k_ℓ + 1..#s`) carries the tail of `ℓ` rather than being out of range, and the within-chain element's last position must still be compared. The "extends mechanically" claim is *not* exactly the same argument.
**Required**: Explicit derivation, even if brief, showing the comparison `t_k^X(d_0)` vs. `s ⊕ ℓ` at the divergence position `k_ℓ < #s` and verifying both the upper bound (`t_k^X(d_0) < s ⊕ ℓ`) and lower bound (`t_k^X(d_0) ≥ s` for `k ≥ k_s`) hold under `#ℓ = #s` with non-ordinal `ℓ`. This is load-bearing for the tightness predicate's restriction to canonical spans.

### Issue 2: No multi-step closures of LP4–LP11
**ASN-0098, throughout**: LP2★ and LP3★ are provided as reflexive-transitive closures of the slot/coverage invariance, but no corresponding closures exist for the displacement lemmas LP4, LP6, LP7, LP8, LP9, LP10, LP11, LP14.
**Problem**: LP18 (Resurrection) requires reasoning about `Σ →* Σ'` (an arbitrary reachable sequence) and uses LP3★, but it also implicitly reasons about projection evolution across multiple steps. The proof appeals to LP3★ to fix coverage but says nothing about how projection moved across the intermediate transitions. Similarly, LP19's hypothesis names "any reachable state sequence Σ_e →* Σ_n" but the per-step displacement framework doesn't compose explicitly. Composite reasoning is left implicit.
**Required**: Either explicit statements of multi-step closures (LP4★, LP9★, LP10★, LP11★), or a single composite-displacement claim that decomposes any reachable `Σ →* Σ'` into atomic steps each governed by LP4–LP14. Without this, the "anything can happen across many transitions" reasoning is not load-bearing on cited lemmas.

### Issue 3: Claims summary table understates LP-Fin's non-canonical scope
**ASN-0098, Claims Introduced table, LP-Fin row**: "Non-canonical spans (`#ℓ < #s`) have `|F ∩ [s, s ⊕ ℓ)| = ℵ₀` and are unconditionally non-tight."
**Problem**: The body discusses three non-canonical categories: (i) `#ℓ < #s`, (ii) `#ℓ = #s` with `ℓ` non-ordinal, and (iii) `#ℓ > #s`. The table mentions only (i). The table's "unconditionally non-tight" is technically correct (categories (ii) and (iii) are non-tight by definitional canonical-form exclusion), but the table summary is misleading about *why* — it suggests only (i) is non-tight, when in fact the predicate excludes all three.
**Required**: Revise the LP-Fin table row to reflect the full non-canonical scope, distinguishing the two grounds (infinite F-intersection vs. definitional exclusion).

### Issue 4: Temporal phrasing in "What the Link Holder Can Rely On"
**ASN-0098, "What the Link Holder Can Rely On" section**: "The link cannot be *made* un-discoverable while there exists any document arranging any I-address in any of its endsets' coverage (LP12)."
**Problem**: LP12 is a single-state biconditional. The phrasing "cannot be made un-discoverable while there exists any document arranging…" suggests a temporal invariant (across some sequence of operations), but it is actually a per-state contrapositive. A reader could mistake this for a stronger claim than LP12 supports. The next bullet — "The link cannot be discovered from a document with no arrangement entry mapping to any I-address in coverage (LP12, contrapositive)" — has the same issue.
**Required**: Rephrase to make clear these are single-state characterisations of discoverability: "At any state, if some document arranges any I-address in coverage, the link is discoverable from that document. At any state, if no document's arrangement maps to any coverage I-address, the link is not discoverable."

### Issue 5: LP9 cross-reference to ASN-0047's strict-containment claim is redundant
**ASN-0098, LP9 K.μ⁺_L sub-proof**: "K.μ⁺_L's effect clause (ASN-0047) asserts `dom(Σ'.M(d)) = dom(Σ.M(d)) ∪ {v_ℓ}`; for this to constitute strict domain extension (E1) rather than mere set union with a possibly-existing element, we additionally need `v_ℓ ∉ dom(Σ.M(d))`. We discharge this freshness clause here by subspace decomposition, owning the derivation rather than citing it to ASN-0047."
**Problem**: This explicitly owns the freshness derivation rather than citing ASN-0047. The motivation given is defensive ("owning the derivation"), but the rationale isn't quite right: ASN-0047's K.μ⁺_L *does* assert `dom(M'(d)) ⊃ dom(M(d))` (strict containment), so the freshness `v_ℓ ∉ dom(M(d))` follows directly from ASN-0047. The ASN-0098 derivation is *re-proving* what ASN-0047 already discharges. If the concern is that ASN-0047's strict-containment is itself unverified, the ASN-0098 author should say so.
**Required**: Clarify why the freshness derivation is owned locally — either (a) state that ASN-0047's strict-containment claim is unverified at the level needed and this fills a gap, or (b) cite ASN-0047 and elide the re-derivation. As written, the motivation is opaque.

### Issue 6: LP19 lemma statement could be clearer about per-pair scope
**ASN-0098, LP19**: "and for each specific newly-added mapping `(v_new, a_new) ∈ dom(Σ_{n+1}.M(d)) ∖ dom(Σ_n.M(d))` in that transition whose I-address `a_new` is the address freshly allocated by the K.α (or K.λ) step on the prefix `Σ_e →* Σ_n`: v_new ∉ project(e, d, Σ_{n+1})"
**Problem**: The "for each specific newly-added mapping" universal is over a *subset* of the K.μ⁺-added pairs (only those whose a_new was freshly K.α-allocated). The lemma proof handles this correctly, but a casual reader might miss that K.μ⁺ may add multiple mappings simultaneously, with some pairs covered by LP19 and others (transclusion pairs) not. The discussion paragraph below LP19 does clarify this, but the lemma statement could be sharper.
**Required**: Either reformulate the lemma's "for each" as "for every pair (v_new, a_new) satisfying the freshness hypothesis" (making the per-pair scope explicit), or add an explicit note that K.μ⁺ may add pairs the lemma does not cover.

## OUT_OF_SCOPE

The Open Questions section already enumerates these. No additions.

VERDICT: REVISE
