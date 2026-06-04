# Review of ASN-0087

This note builds a composite operation (`K.λ ; K.μ⁺_L`) on the substrate and discharges the invariant obligations carefully. The tumbler arithmetic in the worked example checks out (`a₁ ⋠ a₂` at position 8, `a₁ ⋠ ℓ` at position 7), the wp analysis reaches the non-trivial reflexive case, and the invariant verification covers the ASN-0047 per-state list plus the boundary and transition classes. The proofs I checked are sound. The findings below are accretion/precision issues, consistent with this note's `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Definition introduced by its downstream consumers
**ASN-0087, Inputs (Standard authoring)**: "We name the discipline under which several later reductions hold. An endset `e` is *standardly authored at state `Σ`* iff..."
**Problem**: The introductory sentence advances the definition by pointing at unnamed downstream uses ("several later reductions") rather than by stating what the predicate means. This is a use-site inventory in a definition slot — the reductions are named where they occur (wp reduction, side-effect vacuity), so the preamble carries no content.
**Required**: Delete the preamble; open directly with the predicate `StandardAuthoring(e, Σ) ≡ coverage(e) ⊆ dom(Σ.C) ∪ dom(Σ.L)` and its reading.

### Issue 2: Two sections defer to the same downstream argument
**ASN-0087, Invariant Preservation (S2 row)**: "v_ℓ ∉ dom(Σ.M(d)) by the two-part argument below" — and **Freshness of the Allocation**: "discharged in full by the two-part (within-subspace, cross-subspace) argument in the S2 verification of the post-state invariants below."
**Problem**: Both the Freshness section and the invariant table point forward to the same S2 two-part argument. The Freshness section's only content about `v_ℓ` is the forward pointer, so it advances nothing — the reader must jump to S2 either way.
**Required**: Either give the `v_ℓ` freshness argument once at its natural home (S2) and drop the Freshness-section sentence, or move the argument up and have S2 reference it — not two pointers to a third location.

### Issue 3: Redundant restatement of the decomposition rationale
**ASN-0087, Decomposition**: "MAKELINK includes K.μ⁺_L so the link is visible in its home document's arrangement: K.μ⁺_L places the link in the link subspace of `M(d)`... Without it, the link would be allocated but invisible to any retrieval framed against `M(d)`."
**Problem**: The preceding two paragraphs already establish that link creation needs both effects (allocate + make visible) and identify the composite. This paragraph re-says "K.μ⁺_L makes the link visible" in different words — two paragraphs in the same section asserting the same thing.
**Required**: Fold the one non-redundant clause (links live in V-space, L14a) into the prior paragraph and delete the restatement.

### Issue 4: Frame re-enumeration in the "No Permission Check" preamble
**ASN-0087, No Permission Check**: "Beyond the frame established in *What Does Not Change* (no content allocation or modification, no modification of prior links or other documents' arrangements, no entity allocation, no provenance recording), one further omission deserves explicit mention..."
**Problem**: The parenthetical re-lists the entire frame already stated in *What Does Not Change*. The substantive content (MAKELINK performs no permission check — a legitimate "what the operation does not do" statement) is buried behind the re-enumeration.
**Required**: Drop the parenthetical re-listing; state the permission-check omission directly.

### Issue 5: Housekeeping aside that does not advance MAKELINK's reasoning
**ASN-0087, Inputs**: "We write `dom(M)` throughout for the set of allocated documents (`dom(M) = E_doc` by M1, ArrangementMonotonicity, ASN-0047; ASN-0047 states some preconditions against `E_doc`)."
**Problem**: The trailing clause "ASN-0047 states some preconditions against `E_doc`" is meta-commentary about another ASN's drafting choices, not a fact MAKELINK's argument uses.
**Required**: Keep the `dom(M) = E_doc` identity; delete the clause about ASN-0047's precondition phrasing.

## OUT_OF_SCOPE

### Topic 1: Well-formedness of forward-reaching endsets
**Why out of scope**: The note correctly defers (Open Questions) the question of what constraints bind endset spans that reference not-yet-allocated addresses. L4 (ASN-0043) permits them; tightening their well-formedness is a future ASN, not a defect here.

### Topic 2: Composite-level atomicity enforcement
**Why out of scope**: The note establishes that the substrate provides no composite atomicity and assigns the guarantee to the protocol layer. Specifying that protocol layer is new territory.

VERDICT: REVISE
