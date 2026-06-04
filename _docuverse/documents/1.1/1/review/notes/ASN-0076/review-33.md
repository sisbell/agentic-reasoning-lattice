# Review of ASN-0076

The proofs are thorough and, on the mathematics, sound. E0's precondition discharges, E1–E10's derivations, and the E5 induction all hold up, and the E7/ASN-0098 reconciliation (the previously-flagged LP2/LP13 territory) is now handled correctly. The remaining findings are forward-reference accretion and meta-prose, consistent with this note's `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Appendix advances no reasoning and re-defers to Open Questions
**ASN-0076, "Appendix: Intended Use of the Structural Witness"**: "E7's `covers(Σ', ·)` witness is the intended substrate for a future link-search ASN... The conventions, policies, and termination guarantees such a procedure would require are not established here; they are enumerated in the Open Questions below."
**Problem**: The entire appendix is two sentences of forward-reference meta-prose. Sentence one restates a point E7's interpretation paragraph already makes ("The formalization of such operations is the proper subject of the link-search specification"); sentence two re-defers to the Open Questions, which already enumerate the same deferrals. Nothing here advances the argument — it is essay content occupying a structural slot.
**Required**: Delete the appendix. E7 and the Open Questions already carry both the intended-use note and the deferral.

### Issue 2: τ_sup definition carries defensive justification and a downstream-consumer note
**ASN-0076, §The Composite (τ_sup definition)**: "Foundation evidence supports this open-endedness: L4 (EndsetGenerality, ASN-0043) explicitly permits endset spans to reference any addresses, and L9 (TypeGhostPermission, ASN-0043) explicitly permits type-endset addresses that lie outside `dom(C) ∪ dom(L)`. ... Subsequent claims invoke `τ_sup` only as a structural witness and do not re-open this deferral."
**Problem**: The precondition `τ_sup ∈ T ∧ #τ_sup ≥ 1` already fixes the only constraint EDITLINK places on `τ_sup`; the L4/L9 citation is defensive justification for permissiveness the precondition already grants, not a step the definition needs. The trailing sentence is a downstream-consumer note ("subsequent claims invoke τ_sup only as...") — it inventories use-sites rather than advancing the definition's meaning.
**Required**: Drop the L4/L9 evidence sentence and the closing "subsequent claims invoke..." sentence. Keep the structural requirement and the single deferral pointer.

### Issue 3: Same future-ASN deferral stated in multiple sections
**ASN-0076, §The Composite and §The Supersession Relationship**: "deferred to a future ASN on type-endset conventions (Open Questions)" / "Identification depends on the external convention that designates `τ_sup` as the supersession-type address (deferred at `τ_sup`'s definition, §The Composite)."
**Problem**: The semantic-identification-is-external caveat and its deferral appear at the τ_sup definition, again in the §The Supersession Relationship opening paragraph, again parenthetically in E4, and once more in Open Questions. The repetition forces the reader to re-confirm the same deferral at four sites.
**Required**: State the caveat once (at the τ_sup definition or the §The Supersession Relationship opener) and let the later mentions be bare back-references, not restatements.

## OUT_OF_SCOPE

None. The deferred topics (type-endset conventions, supersession-chain traversal, link-search procedures, authorization of `d_new`) are correctly routed to Open Questions rather than claimed here.

VERDICT: REVISE
