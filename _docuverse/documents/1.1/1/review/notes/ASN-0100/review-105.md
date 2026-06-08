# Review of ASN-0100

The core development is sound. The substrate decomposition (n K.α + optional K.μ⁻ + K.μ⁺ + n K.ρ) is correctly typed, the composite-boundary-vs-per-state invariant classification does real work (P4★/P7a are correctly held off at intermediates while P6/P7 are discharged per-state), and the boundary cases (j=0, append j=N, empty document, residual content store) are each handled. The reuse of I3 for Left ∪ Shifted-right and C1a for the per-subspace decomposition is legitimate. The findings below are the meta-prose / forward-reference accretion this note's `review-mode.anti-bloat` classifier targets.

## REVISE

### Issue 1: Document-organization meta-prose around the consolidated per-address discharge
**ASN-0100, §Post-state V-position well-formedness (S7 bullet)**: "**Per-address discharge for each freshly allocated `a_k` (single owning block — §Atomicity back-references it rather than re-deriving).**"
**Problem**: The parenthetical describes the document's own structure (that this is the "single owning block" and that §Atomicity will point back to it) rather than advancing the discharge. This is the "prose justifies document ordering" pattern. The consolidation itself is correct — only the self-describing note is noise.
**Required**: Drop the parenthetical; keep the heading "Per-address discharge for each freshly allocated `a_k`." The downstream pointer in §Atomicity is sufficient on its own.

### Issue 2: Deferral cluster pointing to the same downstream location
**ASN-0100, §sequential structure (empty case)**: "(S8a for the Insertion region — empty and non-empty cases alike — is established once in §Post-state V-position well-formedness.)" — paired with §Atomicity: "discharged once in the per-address owning block of §Post-state V-position well-formedness."
**Problem**: Multiple sections defer to the identical downstream location ("established once in §...", "discharged once in the ... owning block of §..."). This is the flagged "multiple paragraphs in different sections defer to the same downstream location" pattern. A single forward reference at the point of first need suffices; the repeated "established once in §X" phrasing is accretion.
**Required**: Reduce to one forward reference; let the other sites simply cite the claim (S8a / the per-address invariants) without narrating where it lives.

### Issue 3: Use-site inventory restating a cited foundation lemma's internal case structure
**ASN-0100, §Effect One (Allocation)**: "This conjunction is exactly the conclusion of SubsequentEmissionFreshness (ASN-0093): the subsequent emission `a_k = inc(a_prev, 0)` ... is fresh against `dom(C) ∪ dom(L)`, with the three-way split — within-document, cross-document, cross-subspace — discharged there."
**Problem**: ASN-0100 needs only the conclusion (`a_k ∉ dom(Σ_k.C) ∪ dom(Σ_k.L)`). Enumerating the three sub-cases that the foundation lemma discharges internally adds no step to this ASN's argument — it restates the cited lemma's structure. Mild but recurrent (it also reappears in §Atomicity).
**Required**: Cite the conclusion and the lemma; drop the "three-way split — within-document, cross-document, cross-subspace — discharged there" inventory.

## OUT_OF_SCOPE

### Topic 1: Implementation recovery after partial failure during the composite
**Why out of scope**: The first Open Question (recovering canonical order after partial failure) is correctly posed as future work; the abstract spec commits to atomicity at the boundary and need not specify failure recovery.

### Topic 2: Link-subspace insertion, COPY, concurrent INSERTs
**Why out of scope**: Explicitly bounded in §Bounding the Scope and the scope directive; the ASN correctly declines to specify them.

VERDICT: REVISE
