# Review of ASN-0047

## REVISE

### Issue 1: K.μ⁺_L empty-subspace case references an undefined depth `m_L(d)`
**ASN-0047, K.μ⁺_L (LinkSubspaceExtension), precondition**: "depth `m_L(d)`, the current link-subspace depth; when V_{s_L}(d) = ∅ this insertion re-pins m_L(d) at any value ≥ 2 (S8a). … If V_{s_L}(d) = ∅: v_ℓ is the minimum position `[s_L, 1, ..., 1]` of depth m_L(d) … #v_ℓ = m_L(d)"

**Problem**: In the empty case `m_L(d)` is undefined — the *V-position depth (operational)* note states `m_S(d)` "is well-defined only while V_S(d) ≠ ∅." The precondition then both *uses* `m_L(d)` to fix `v_ℓ`'s depth and *defines* `m_L(d)` as `v_ℓ`'s depth. This is circular. The intent (a free choice `m ≥ 2`) is confirmed only in the worked example — "this first link-subspace insertion fixes m_L(d) = 2 (any value ≥ 2 is admissible; we take 2 here)" — not in the precondition itself. The content subspace avoids this with the explicit `ValidFirstInsertionPosition(d, v, m)` parameter; the link side should be stated symmetrically.

**Required**: Make `m` an explicit free parameter of K.μ⁺_L in the empty case (e.g., a `ValidFirstLinkPosition(d, v_ℓ, m)`-style predicate with `m ≥ 2`), so the precondition is non-circular and checkable by an implementer.

### Issue 2: Unused partial-suffix expansion machinery in the K.μ~ decomposition
**ASN-0047, *Decomposition* (Realisation of K.μ~)**: the "*Partial-suffix expansion* at `n'_{s_C} = k₀ − 1`" bullet, with its admissibility iff-condition and the "The quantifier must range over the *image* `u` … not over the source `v < cut`, because the obligation arises wherever π maps *into* X … The Y→X case is exactly where a `v < cut`-only quantifier fails" analysis.

**Problem**: No verification in the ASN exercises the partial-suffix form. The same paragraph concludes "Verification-matrix entries for K.μ~ that name no cut point therefore read as the full-clearance form, which is always available regardless of π's structure on dom_C," and Step (A), the necessity/sufficiency proof, and every matrix cell use the full-clearance form (`n'_{s_C} = 0`). The interior-replacement worked example does use a partial-suffix K.μ⁻, but the ASN explicitly classifies that composite as *not* a K.μ~ instance. The partial-suffix realisation of K.μ~ specifically, together with its X→X / Y→X case analysis, is elaborate machinery that discharges nothing.

**Required**: Drop the partial-suffix realisation form (and its iff-derivation) from the K.μ~ decomposition, or reduce it to a one-line remark that other cut points exist; keep only the full-clearance form the proofs actually use.

### Issue 3: Duplicated default-value / `E_doc`-membership discrimination prose
**ASN-0047, *Notational convention (default value)***: "`M(d) = ∅` does not signal allocation status — a freshly registered document also has `M(d) = ∅` — so `E_doc`-membership, not the test `M(d) = ∅`, is the discriminating predicate for allocation."
**and K.δ frame, Document(e) case**: "The registered `M'(e) = ∅` is the *allocated-empty* arrangement … discriminated from the unallocated default `M(e) = ∅` by `E_doc`-membership per the *Notational convention (default value)* above."

**Problem**: The second passage restates the first and points back to it — two paragraphs in different sections saying the same thing. The K.δ frame paragraph need only state the effect (`dom(M') = dom(M) ∪ {e}`, `M'(e) = ∅`); the discrimination rationale belongs at one site.

**Required**: State the `E_doc`-vs-`M(d)=∅` discrimination once (the Notational convention) and let the K.δ frame state only the effect.

### Issue 4: Use-site inventory prose attached to discharge routes
**ASN-0047, S8★ K.μ⁻ discharge paragraph**: "This is the route taken by the K.μ⁺ and K.μ~ content-subspace cells (per-subspace projection via ASN-0036's S8)." and "This is the discharge named in the S8★ K.μ⁻ verification-matrix cells."
**ASN-0047, P4a definition box**: "This is the single statement of P4a's discharge; the Class (b) verification matrix and prose point here."

**Problem**: These sentences enumerate where a discharge is *consumed* rather than advancing the discharge's content. They are the "definition enumerates downstream consumers" pattern; the reader already follows the argument from the matrix and prose, and these back-pointers add navigation overhead without reasoning.

**Required**: Remove the consumer-inventory sentences; the matrix cells already name their discharge, so the reverse pointers are redundant.

## OUT_OF_SCOPE

### Topic 1: Link inheritance semantics under forking
The fork composite deliberately starts d_new's link subspace empty and defers any link-inheritance mechanism. This is correctly left to a future ASN (and already noted as such), not a gap in this one.

### Topic 2: Link-withdrawal / tombstoning mechanism
The orphan-link discussion references withdrawal but defers the reconciliation of tombstoning with D-CTG★/D-MIN★ to an Open Question. Withdrawal/access-control is out of scope per the Scope section.

VERDICT: REVISE
