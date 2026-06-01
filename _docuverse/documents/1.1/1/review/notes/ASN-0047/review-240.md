# Review of ASN-0047

## REVISE

### Issue 1: "Link store and extended system state" is a near-empty structural slot holding only deferral prose
**ASN-0047, ## Link store and extended system state**: The entire section body is *"Semantics of empty endsets at slots 1 and 2. L3 admits e₁ = ∅ and e₂ = ∅ independently ... The semantics of empty endsets for endset-iterating consumers is left to a future ASN."*

**Problem**: The section header promises a definition of the link store and extended state, but those are already defined in *## The state model* (`Σ = (C, L, E, M, R)`, plus the `Definition (Link store)` material). This section introduces no invariant, operation, or definition — it is rationale plus a future-ASN deferral. The deferral also duplicates Open Question *"Should K.λ require e₁ ∪ e₂ ≠ ∅ ... do one-sided links ... carry distinguishable semantics."* This is exactly the "essay content in a structural slot" + "defers to a future ASN" pattern the anti-bloat note flags.

**Required**: Either delete the section (the empty-endset admission is fully carried by L3's `e₃ ≠ ∅` and the Open Question) or fold its one substantive sentence into the L3 restatement. Do not leave a structural slot whose only content is rationale and forward-deferral.

### Issue 2: Redundant link-withdrawal / fork-inheritance deferrals duplicate Open-Question content in body prose
**ASN-0047, ## Orphan links and coupling flexibility** and **J4**: *"Link withdrawal via K.μ⁻ applied to the link subspace would in principle produce the same orphan-link state but is constrained to suffix truncations under D-CTG★"* and, in J4, *"A mechanism for link inheritance under forking, if desired, would require K.μ⁺_L steps in the fork composite and is outside this ASN's scope."*

**Problem**: Both sentences state a deferral that is already an Open Question (the tombstoning question restates the suffix-truncation constraint verbatim; fork link-inheritance is implied by Open Question 1 / the fork discussion). They advance no reasoning at the point of use — they are "see future ASN" markers embedded mid-derivation, which compound across cycles per the anti-bloat note.

**Required**: Remove the inline deferral sentences; the Open Questions are the correct home for "outside this ASN's scope" remarks.

## OUT_OF_SCOPE

### Topic 1: Link-subspace correspondence-run structure beyond the trivial length-1 decomposition
**Why out of scope**: S8★(s_L) deliberately omits ASN-0036 S8's uniqueness condition (c) and uses a non-maximal length-1 run-cover. Whether the link subspace warrants a maximal-run / uniqueness treatment is genuinely new territory, and the ASN already scopes it via its Open Question on link-subspace invariants "beyond this shared sequential structure." Not an error here.

---

Note: I checked the substantive proofs — FrontierEquivalence (both directions), the D-SEQ★ m=2 and m≥3 derivations (including that inner-position-≥2 tuples fall strictly above `v_max` and so are not forced in by D-CTG★), K.μ~ admissibility/necessity-and-sufficiency, the link-subspace fixity Steps (C)–(D), Step (B)'s S3★ chain, and the Class (a)/(b) matrix coverage — and found them internally consistent and grounded in the cited foundations. The remaining issues are presentational accretion, not correctness.

VERDICT: REVISE
