# Review of ASN-0047

## REVISE

### Issue 1: J1'★ derivation is step-local but the stated obligation is composite-scoped
**ASN-0047, *Scoped coupling constraints* (J1'★ derivation)**: "Because K.ρ holds M in frame ... the post-state Σ' is itself the natural witnessing state, and the inductive obligation of P4a specialises to 'every new R-entry has a content-subspace witness at Σ'.'"

**Problem**: The wp calculation that justifies this runs backward through a single K.ρ atomic step, where `M' = M` makes the K.ρ post-state coincide with the witnessing state. But J1'★ is *stated* over composite boundaries (`Σ →* Σ'`), and ValidComposite★ permits M-mutating steps (K.μ⁻, K.μ⁺) to fall *between* the K.ρ event and the composite endpoint Σ'. When they do, the K.ρ-step post-state and the composite Σ' diverge, so the step-local derivation does not establish the composite-Σ' form actually written. The text presents J1'★ as derived (via wp) when the composite-scoped, Σ'-witnessed statement is in fact an imposed coupling requirement that the step-local wp only motivates. (That valid composites avoid the divergence is enforced jointly by J0 — which independently rejects allocate-then-remove — but the J1'★ derivation never invokes J0 to close this gap.)

**Required**: Either (a) extend the derivation to the composite level, explicitly invoking J0/P2 to show no valid composite strips a content witness whose provenance it records, or (b) reframe J1'★ as an imposed coupling whose wp justification is step-local intuition, not a complete derivation of the composite form.

### Issue 2: Inaccurate use claim in the Contains(Σ) definition
**ASN-0047, *Coupling and isolation* (Definition Current containment)**: "We will need it both in the valid composite definition (as a state invariant) and in the coupling derivations that follow."

**Problem**: The (unscoped) `Contains(Σ)` is neither used in the Valid composite definition nor is it a state invariant. The Valid composite definition rests on J0/J1★/J1'★, and the provenance bound those couplings serve is P4★, which is stated over `Contains_C(Σ)`, not `Contains(Σ)`. The unscoped relation is used only in J3 and the staleness discussion. The parenthetical "(as a state invariant)" is doubly wrong — it is a derived quantity, explicitly not bounded by R once any link is arranged (the ASN itself shows `Contains(Σ) ⊆ R` is unsatisfiable in the extended state).

**Required**: Correct the forward claim to reference `Contains_C` and drop "as a state invariant," or delete the sentence.

### Issue 3: Cross-section deferral stubs to a single downstream location
**ASN-0047, P4★ / P4a / P7a sections**: P7a ("Stated and proved under Class (b) in the *Extended reachable-state invariants* section."), P4★ ("Its full discharge ... is given once under Class (b)..."), P4a ("Its derivation by induction with J1'★ as the coupling is given under Class (b)...").

**Problem**: Three properties are each introduced near their conceptual home with a stub that defers proof to the same downstream Class (b) location — the "multiple paragraphs in different sections defer to the same downstream location" accretion pattern. The reader must hold three open forward pointers to one section, and the stubs carry no reasoning of their own.

**Required**: State each property once (either at its conceptual home with its proof, or only in Class (b) with a single pointer from a property index), removing the duplicated stub-plus-deferral prose.

### Issue 4: Structural-navigation prose in place of reasoning
**ASN-0047, *Extended reachable-state invariants* ("TrackedEmission carried separately") and *Class (a)* ("Derived distinctness corollaries")**: "The per-state invariant TrackedEmission ... is *not* listed in the Class (a) conjunction above and has no row in the Class (a) verification matrix; it is established by the self-contained induction given in its own definition box..." and "The following two distinctness properties are *not* per-state invariants of ExtendedReachableStateInvariants and are absent from the Class (a) conjunction and the verification matrix above."

**Problem**: These paragraphs describe where things are filed (what is in or absent from the conjunction/matrix) rather than advancing any claim — essay content in a structural slot. The reader works around them to follow the actual invariant arguments. The "Typing note (M total — overrides foundation)" enumerated survival inventory ("M0 ... Survives. M1 ... Survives.") is the same shape, though there the per-item verification is closer to load-bearing.

**Required**: Replace the organizational notes with the substantive content only — for TrackedEmission, a one-line pointer to its induction; for the distinctness corollaries, the corollary statements and their one-step discharge, dropping the "absent from the matrix" commentary.

## OUT_OF_SCOPE

### Topic 1: Concurrent allocation under a shared home document
**Why out of scope**: The ASN's last open questions raise serialization of link/content allocation under concurrent operations. SequentialTransitionAxiom fixes a totally-ordered single-event model, so concurrency is a separate transition-model extension, not a gap in this one.

### Topic 2: Interior link withdrawal / tombstoning mechanism
**Why out of scope**: D-CTG★/D-MIN★ confine K.μ⁻ to suffix truncation, so withdrawing an interior link requires a mechanism outside K.μ⁻'s presentational-removal contract. The ASN correctly catalogues this in Open Questions as future territory rather than a defect here.

VERDICT: REVISE
