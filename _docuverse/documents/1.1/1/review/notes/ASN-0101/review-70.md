# Review of ASN-0101

The operation specification (D0) and its supporting claims (D1–D11) are mathematically sound: the region partition `Λ ⊎ X ⊎ Π`, the shift-inverse `σ_d`, the gap-closure contiguity argument, the three-group invariant discharge in D8 (including the careful S8★ condition-(c) routing through M12), the wp negation equivalence for the partial deterministic command, and all three worked examples check out. Edge cases (empty post-state, deletion at start/end, singleton subspace, cross-document isolation) are covered with explicit, non-hand-waved arguments. My findings are confined to the accretion patterns flagged by the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Scaffolding preamble around N2 advances no reasoning
**ASN-0101, D10, "DEL-neutrality fact"**: "The boundary derivation below relies on one fact about how a single DEL step moves the composite-boundary property P4a; we establish it here and cite it by name (N2) in the induction."
**Problem**: This sentence is document-flow narration — it announces that a fact will be stated and later cited, without contributing to the argument. The content of N2 itself ("R' = R … DEL records no new provenance pair … DEL cannot break P4a") is the load-bearing part; the announcement matches the flagged pattern of structural narration that the precise reader must skip past.
**Required**: Delete the preamble sentence and let N2 stand on its own; the single citation "P4a at Σ' holds by N2" in the boundary derivation already supplies the connection.

### Issue 2: Boundary-case paragraph forward-references the worked example and re-inventories D8
**ASN-0101, "Boundary cases", Non-singleton interior deletion**: "The worked example below (`n_S = 4`, `n = 2`, `p = 2`) instantiates this case at `Λ = {[1, 1, 1]}` … tracing every clause of D8 explicitly: S8a, S8-depth, S8-fin via the post-state's structural form; S3★ via source correspondence (`a_1 ∈ dom(C')` for `Λ`, `a_4 ∈ dom(C')` for `Q`); D-CTG★, D-MIN★, D-SEQ★ via D1's characterisation. D8's discharge routes the two summands through distinct mechanisms …"
**Problem**: The first two sentences of the case (configuration, shift formula, post-state form) are the legitimate boundary-enumeration content. The remainder is a forward-deferral to the worked example combined with a use-site inventory of D8's per-clause discharge carrying example-specific values (`a_1`, `a_4`) — content already present in D8's general justification and re-demonstrated in the worked example. This is the use-site-inventory-in-a-structural-slot accretion pattern.
**Required**: Reduce the case to its configuration and the genuinely case-specific facts (Λ/Q disjoint by last-component range; the pointwise extension when `|Λ|` or `|Q| > 1`). Drop the clause-by-clause D8 inventory and the `a_1`/`a_4` preview, which belong to the worked example, not the boundary enumeration.

## OUT_OF_SCOPE

None. The Open Questions section correctly defers versioning, reversibility, and orphan-rediscovery to future ASNs.

VERDICT: REVISE
