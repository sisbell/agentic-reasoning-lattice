# Review of ASN-0047

## REVISE

### Issue 1: Over-broad coupling claim contradicted by the ASN's own worked example
**ASN-0047, "Coupling and isolation"**: "Coupling constraints describe required co-occurrence — when K.μ⁺ occurs, K.ρ must also occur in the same composite transition."

**Problem**: This is false as stated, and the ASN refutes it itself. J1★ is *range-based*: it requires a co-occurring K.ρ only when an I-address is new to the content-subspace range **and** `(a, d) ∉ R`. The "two-step variant — prior-provenance replacement" worked example is exactly a valid composite of K.μ⁻ + K.μ⁺ with **no** K.ρ, justified by `(aₓ, d) ∈ R` already holding (P2-preserved). A re-transclusion of an already-recorded address, or a K.μ⁺ adding a position mapping to an address already in the content-subspace range, likewise fires no K.ρ. The blanket "when K.μ⁺ occurs, K.ρ must also occur" directly contradicts the two-step variant and the range-based J1★ it is meant to summarize.

**Required**: Restate the clarification to match J1★'s range-based trigger — K.ρ co-occurs only for content-subspace range-new addresses not already in R — or delete the over-broad sentence and defer to J1★.

### Issue 2: Foundation invariants restated twice within the ASN
**ASN-0047, "Link store and extended system state" vs. "Inherited from foundation (restated for narrative continuity)"**: The body section restates `Endset`, `Link`, the subspace identifiers, `L-fin` ("L-fin (LinkStoreFiniteness). `|dom(Σ.L)| < ∞`. Holds at Σ₀..."), and inlines L0/L1/L1a/L3/L12/L14; the closing table re-states the identical items, declaring they are "restated for narrative continuity — every statement ... supplied by the cited foundation, not by local derivation."

**Problem**: The same foundation content (L-fin, L0, L1, L1a, L3, L12, L14, Endset, Link) appears twice inside ASN-0047 — once as body prose, once as the inherited table — with the Notation section adding a third restatement of the projection functions. This is forward-reference/restatement accretion: the precise reader must reconcile two copies and verify they agree, with no reasoning added by the second copy.

**Required**: Keep one location (the "Inherited from foundation" table is the natural home) and reduce the body section to a one-line pointer plus the genuinely local content (the empty-endset reading of L3, which is the only non-inherited material the section itself flags).

### Issue 3: P4a discharge stated three times
**ASN-0047, P4a definition box, Class (b) matrix row, and Class (b) prose**: The P4a definition box carries a "*Discharge mechanism*" paragraph (induction along the witnessing trace; freshly recorded entry witnessed by Σ', persisted entry by inductive hypothesis). The Class (b) verification then restates the same mechanism in the matrix P4a row and again in the "P4a (...)" prose paragraph, re-explaining the K.ρ-before-K.μ⁺ ordering concern and the "Σ' is the witnessing state" resolution.

**Problem**: Three slots re-derive one discharge. The definition box's "Discharge mechanism" and the Class (b) prose paragraph say the same thing in different words (the matrix cell is the legitimate index entry). This is the "multiple paragraphs defer to / restate the same downstream location" pattern that compounds across cycles.

**Required**: State the discharge once (the definition box's "Discharge mechanism" or the Class (b) prose, not both) and have the other point to it.

## OUT_OF_SCOPE

None — the ASN's scope block and Open Questions already route link-withdrawal/tombstoning, concurrent allocation, node-baptism protocol, and transitive-transclusion provenance to future ASNs appropriately.

VERDICT: REVISE
