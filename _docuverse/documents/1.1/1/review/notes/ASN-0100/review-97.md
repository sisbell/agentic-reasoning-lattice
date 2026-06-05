# Review of ASN-0100

## REVISE

### Issue 1: Per-invariant spelling-out of link-subspace inheritance bloats the atomicity proof

**ASN-0100, §Atomicity and Canonical Order, "After step 2's K.μ⁻" bullet**: "S8a and S8-depth (with m_L unchanged) follow from the unchanged set; D-CTG★, D-MIN★, and D-SEQ★ on V_{s_L}(d_intermediate) each follow from their pre-state forms applied to the unchanged set — D-CTG★ because the same positions retain the same contiguity structure under the V-ordering, D-MIN★ because min(V_{s_L}(d_intermediate)) = min(V_{s_L}(d)) is preserved, and D-SEQ★ because the enumeration ... carries over unchanged."

**Problem**: K.μ⁻ retains the link subspace verbatim (`n'_{s_L} = n_{s_L}`). Once "the set is pointwise unchanged" is stated, every per-subspace invariant on it inherits trivially. Enumerating each invariant with its own clause ("D-CTG★ because…, D-MIN★ because…, D-SEQ★ because…") is a use-site inventory that adds no reasoning the unchanged-set fact does not already supply.

**Required**: Collapse to one sentence — "the link subspace is retained pointwise (`n'_{s_L} = n_{s_L}`), so every per-subspace invariant on `V_{s_L}` inherits unchanged from the pre-state" — and drop the per-invariant restatement.

### Issue 2: Redundant frame restatement in §Effect Three

**ASN-0100, §Effect Three (closing paragraph)**: "The shift's carrier is strictly the text-subspace positions at or after p. Everything else lies outside it and does not move: the left region (v < p) stays put, positions in other subspaces (including links) are untouched, other documents are untouched, and pre-existing content-store bindings are preserved..."

**Problem**: This duplicates content stated formally three further times — the Formal Contract's Frame Conditions, and claims INS.frame.subspace / INS.frame.doc / INS.frame.L. The same "everything else does not move" content appears in different words across the document.

**Required**: Delete the restatement; the formal Frame Conditions and INS.frame.* claims are the authoritative statement.

### Issue 3: Deferral cluster — multiple sections defer the same discharge downstream

**ASN-0100, §Effect Two and §D-CTG★ (empty case)**: "Well-formedness and fixed depth of these positions (S8a, S8-depth) are discharged with the rest of the post-state in §Post-state V-position well-formedness." / "this is discharged uniformly with the non-empty case in §Post-state V-position well-formedness (whose k = 0 / k ≥ 1 split covers the empty case...)". Likewise the worked-example provenance paragraphs each defer to §Provenance ("discharge exactly as in the interior example and §Provenance").

**Problem**: Several separated paragraphs point forward to the same downstream location rather than carrying their claim or being stated once. This is the deferral-accretion pattern the anti-bloat classifier targets.

**Required**: State S8a/S8-depth for the Insertion region once, at the well-formedness section, and let the earlier mentions name the region without the "discharged in §X" forward pointer; drop the redundant worked-example provenance deferrals (the §Provenance discharge is the canonical one).

## OUT_OF_SCOPE

### Topic 1: Insertion into the link subspace

**Why out of scope**: §Bounding the Scope correctly restricts to the content subspace; the `K.μ⁺_L` / `K.λ` link-insertion operation is distinct and belongs in a future ASN. The fourth open question (analogous invariants for link-subspace insertion) is the right place for it, not this revision.

VERDICT: REVISE
