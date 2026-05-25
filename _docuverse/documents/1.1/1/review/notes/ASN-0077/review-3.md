# Review of ASN-0077

## REVISE

### Issue 1: Extension of origin to dom(L) is informal
**ASN-0077, "Where origin already lives"**: "The same structural projection extends uniformly to link addresses... We henceforth read origin as a total function on dom(C) ∪ dom(L), with the same structural definition."
**Problem**: The extension of `origin` from `dom(C)` (where ASN-0036's S7 grounds it) to `dom(L)` is introduced as prose without a labeled definition or formal claim. Structural well-definedness on `dom(L)` is justified via L1b, but the *semantic* correspondence — that `origin(ℓ)` equals the document that allocated `ℓ` — is not derived. CL-OWN concerns arrangement, not allocation. The semantic claim requires K.λ's precondition `origin(ℓ) = d`, which is never cited. O2's link case, O3, O5, and the V-span operation specification all depend on this extension being both structurally and semantically sound.
**Required**: Add a labeled definition extending `origin` to `dom(C) ∪ dom(L)`, with a derivation grounded in L1b (well-definedness of T4b's projections) and K.λ's allocation discipline (semantic correspondence to home document). Treat it on the same footing as ASN-0036's S7.

### Issue 2: O2 link case omits the subspace justification for CL-OWN
**ASN-0077, "Lifting origin to a V-span" (O2 derivation)**: "Link block (subspace(vⱼ) = s_L): S3★ gives aⱼ + i ∈ dom(L), and CL-OWN (ASN-0047) applied at both v = vⱼ and v = vⱼ + i (each membership of dom(M(d)) is supplied by B1 via the block decomposition) gives origin(aⱼ + i) = d = origin(aⱼ)."
**Problem**: CL-OWN's precondition is `v ∈ dom(M(d)) ∧ subspace(v) = s_L`. The author discharges `dom(M(d))` membership via B1, but does not establish `subspace(vⱼ + i) = s_L`. The block decomposition tells us `vⱼ` is in `s_L`; carrying this to `vⱼ + i` requires M-sub(a) of ASN-0058, whose precondition `#vⱼ ≥ 2` comes from S8a. Without this step, CL-OWN's hypothesis at `vⱼ + i` is not in hand.
**Required**: Cite M-sub(a) (ASN-0058) and S8a (ASN-0036) to bridge subspace from `vⱼ` to `vⱼ + i` before invoking CL-OWN at `vⱼ + i`.

### Issue 3: (F2) ≡ (F3) cites a content-only lemma to discharge a step that includes the link case
**ASN-0077, "Equivalence chain (F1) ≡ (F2) ≡ (F3)"**: "(F2) = (F3): Inside the inner set for each j, M16a applied as in O2 collapses {origin(aⱼ + i) : 0 ≤ i < nⱼ} to {origin(aⱼ)}."
**Problem**: M16a (OriginInvarianceUnderShift, ASN-0058) is defined only for `dom(C)`. It does not handle link blocks. The collapse `origin(aⱼ + i) = origin(aⱼ)` holds uniformly across content and link blocks only because O2 itself supplies a case-by-case proof (M16a for content, CL-OWN for link). Citing "M16a applied as in O2" mischaracterises the link case — M16a literally does not apply there.
**Required**: Replace the M16a citation with O2 (Block uniformity) — the just-derived claim that establishes the collapse for both subspaces.

### Issue 4: "resolve" is invoked on link-subspace V-spans, but ASN-0058's resolve targets dom(C)
**ASN-0077, "Lifting origin to a V-span"**: "Foundation ASN-0058 supplies the machinery... The resolution function returns a sequence of mapping blocks: resolve(d, σ) = ⟨ (a₁, n₁), ..., (aₖ, nₖ) ⟩, where each block (aⱼ, nⱼ) denotes the I-address run... (M2, M3 of ASN-0058)."
**Problem**: ASN-0058's `resolve` is specified for content references producing I-addresses in `dom(C)` (its C1 — ResolutionIntegrity — explicitly asserts `aⱼ + i ∈ dom(C)`). The operation specification of SHOWORIGIN_V admits link-subspace V-spans whose resolved values would lie in `dom(L)`. The formal derivations correctly route through C1a (RestrictionDecomposition, which is subspace-agnostic), but the prose names `resolve(d, σ)` — implying ASN-0058's content-restricted function applies to link inputs as well.
**Required**: Either explicitly extend `resolve` to handle link-subspace inputs (with a derivation showing the link analog of C1), or rephrase the prose to invoke C1a's block decomposition directly without naming `resolve`. The choice should be consistent throughout.

### Issue 5: Singleton I-span argument omits the #b < #a case
**ASN-0077, "Edge cases" (Singleton I-span)**: "So either #b = #a (giving b = a directly), or #b > #a (b is a proper extension of a). The latter case is excluded by structural arguments..."
**Problem**: The trichotomy on `#b` vs `#a` skips `#b < #a`. The earlier prose claims "b to agree with a at positions 1 to #a − 1" and "b_{#a} = a_{#a}" — both presupposing `#b ≥ #a`. The reader is left to verify that `#b < #a` is impossible (it is, via T1 case (ii): a proper-prefix `b` would satisfy `b < a`, contradicting `a ≤ b`), but the argument never states this.
**Required**: State explicitly that `#b < #a` is ruled out by T1 (a proper-prefix `b` of `a` gives `b < a`, contradicting `a ≤ b ∈ ⟦σ_a⟧`). Then proceed to the `#b ≥ #a` cases as written.

VERDICT: REVISE
