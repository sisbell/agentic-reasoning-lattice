# Review of ASN-0116

I worked through the operation as a valid composite over the K-vocabulary, checked the composite-validity discharge (both clauses), verified the I3-transfer arguments to the filled arrangement, the block-disjointness interval reasoning, the provenance coupling at the boundary, the four named invariants, the wp, and the worked example. The technical core holds up under scrutiny: the append / empty / front-insertion (J=1) boundaries are covered, the K.μ⁻ → K.μ⁺ realization of the gapped-then-filled arrangement is honest about the M'₀ vs M'(d) distinction, the boundary-only evaluation of J0/J1★/J1'★ is used correctly, and the wp is genuinely non-trivial (containment, not emptiness). I found no hard mathematical error.

What remains are accreted-prose findings, which the active `review-mode.anti-bloat` classifier directs me to surface at source.

## REVISE

### Issue 1: Downstream-consumer enumeration in the P0 introduction
**ASN-0116, "What is allocated, and why it must be fresh"**: "Why must this hold for any implementation? Because everything downstream — links that survive editing, transclusion, version correspondence, historical reconstruction — anchors on identity… The freshness of P0 is precisely what lets the rest of the system trust that an I-address names one content event for all time."
**Problem**: The first and last sentences enumerate P0's downstream consumers (links / transclusion / version correspondence / historical reconstruction) and assert its importance, rather than advancing the claim — exactly the "definition's introduction enumerates downstream consumers" pattern. (The middle sentence — "Were two equal-valued insertions to share an address, a link to one would silently become a link to the other" — is an object-level statement of what the guarantee prevents and should stay.)
**Required**: Drop the downstream inventory and the "lets the rest of the system trust" importance-assertion; keep the object-level statement of what address-collision would break.

### Issue 2: Essay aphorism in a structural slot
**ASN-0116, "What we have established"**: "The whole specification is, at bottom, the discipline of never letting an ephemeral position pretend to be a permanent identity."
**Problem**: The surrounding sentences (one-line summary of the two-layer composite, pointer to the claims table) do their job; this aphorism is essay content occupying the closing structural slot and advances no reasoning.
**Required**: Remove the aphorism; retain the functional summary and the table pointer.

## OUT_OF_SCOPE

### Topic: The four Open Questions
**Why out of scope**: Transclusion-at-a-shared-position, transclusion-provenance, and fragmentation-after-editing belong to ASN-0118 (COPY) and the editing operations; concurrent insertion without a serializing authority is a replication/protocol concern (BEBE). The note correctly parks these as Open Questions rather than specifying them, consistent with the declared scope.

VERDICT: REVISE
