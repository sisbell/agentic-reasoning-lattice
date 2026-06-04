# Review of ASN-0100

This ASN is technically thorough and, as far as I can verify, correct: the three-region partition, the K.μ⁻ + K.μ⁺ decomposition, the per-state/composite-boundary invariant split, and the worked-example arithmetic all check out. The invariant conjuncts of ASN-0047's `ExtendedReachableStateInvariants` are each addressed. Cross-references are confined to the foundation set. The findings below are accumulated meta-prose flagged by the `anti-bloat` classifier, not correctness defects.

## REVISE

### Issue 1: Closing essay paragraph in §INSERT vs. COPY
**ASN-0100, §INSERT vs. COPY → Derived corollaries**: "The identity-by-allocation property of INSERT is foundational. All higher-level properties of the system — traceability of content to its author, royalty accounting, link survivability, version comparison via shared identity — depend on it. An implementation that silently de-duplicated content during INSERT … would corrupt every dependent guarantee."
**Problem**: This is motivational essay plus a downstream use-site inventory (royalty accounting, version comparison, traceability) that does not advance the INSERT specification. The object-level claim — each `a_k` is fresh, no de-duplication, no identification with a pre-existing I-address — is already fully stated by INS.identity and the three corollaries immediately above. The reader must skip past it to reach the scope-bounding section.
**Required**: Delete the paragraph; INS.identity and its corollaries already carry the content.

### Issue 2: Reviser-drift defensive prose in §Atomicity
**ASN-0100, §Atomicity (per-step intermediate analysis)**: e.g. after step 1's K.α — "The composite-boundary properties (J0, J1★, P4★) are not yet required to hold at this intermediate — a_k is in dom(C) but not yet placed, which J0 would forbid at a composite boundary, but the intermediate is interior to the composite"; and after step 2's K.μ⁻ — "P4★ (composite-boundary) would not hold at this intermediate if it required all post-state ran(M(d)) entries to be in R — but R has not yet been extended; the obligation is delegated to the composite boundary."
**Problem**: The per-state vs. composite-boundary distinction is established cleanly at the head of §Atomicity. These recurring sentences then imagine a stricter requirement (a boundary property evaluated at an interior state) that the established scope already excludes, and explain why it doesn't apply — the reviser-drift pattern of explaining around a case the framing already rules out. They repeat at multiple step boundaries.
**Required**: Drop the "would not hold if it required…" asides. The opening scope statement already tells the reader boundary properties are not evaluated at interior states.

### Issue 3: Repeated deferrals to §Post-state V-position well-formedness
**ASN-0100, §Effect Two, §Effect Three, §Atomicity (step 3, Insertion positions)**: "the derivation that the shift transfers p's S8a to shift(p, k) is given in full in §Post-state V-position well-formedness"; later "are established by the shift(p, k) argument in §Post-state V-position well-formedness … that derivation applies verbatim here."
**Problem**: Three separate sections defer the same `shift(p, k)` S8a/S8-depth derivation to one downstream location — the flagged "multiple paragraphs defer to the same downstream location" pattern. Each deferral is navigation overhead the precise reader must resolve.
**Required**: Consolidate so the derivation is cited once (e.g., from §Effect Two as the canonical site) and the later uses reference that single citation without re-announcing the deferral, or inline the one-line result where first needed.

## OUT_OF_SCOPE

### Topic 1: Link-subspace insertion, post-failure recovery, INSERT-composition closure
**Why out of scope**: These are correctly listed in §Open Questions and the scope section as future work (K.μ⁺_L insertion, crash recovery, self-composition). Not errors here.

VERDICT: REVISE
