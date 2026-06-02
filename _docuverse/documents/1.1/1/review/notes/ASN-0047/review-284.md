# Review of ASN-0047

I reviewed the transition model on its own terms: the five-component state, the eight elementary/composite transitions, the coupling constraints, and the reachable-state invariant proof. The mathematics is sound — I checked the K.δ structural identities, the anchor arithmetic (`b_C(d)=inc(d,2)`, `b_L(d)=inc(b_C(d),0)`), the D-SEQ★ derivation (both `m=2` and `m≥3` cases), the K.μ~ admissibility/realisability coincidence, and the necessity/sufficiency of the K.μ~ precondition. I found no correctness holes. The findings below are the meta-prose/accretion patterns this note's `review-mode.anti-bloat` classifier directs me to surface, plus one depth item. I have deliberately avoided the previously-declined split and matrix-index findings.

## REVISE

### Issue 1: J4 introduction duplicates Definition (Fork) and defers to it
**ASN-0047, *Coupling and isolation* (J4) and *Definition (Fork)***: The J4 intro states "*Fork is version creation on d_src's version chain `A_v(d_src)`; its K.δ allocation discipline and content-source operand-tracking rule are stated once in Definition (Fork) below*," and Definition (Fork) then opens "*Fork is version creation on d_src's version chain `A_v(d_src)`, with K.δ address allocation uniform across first and subsequent versions; the content source operand tracks the same K.δ sub-case.*"

**Problem**: This is the "two paragraphs say the same thing + deferral to the same downstream location" pattern. The intro restates the version-chain allocation rule and the k=1/k=0 operand-tracking discriminator, declares it is "stated once" below, then Definition (Fork) restates it. The reader reads the rule twice and follows a forward pointer to reach the canonical form.

**Required**: Have the J4 intro state only that fork is the K.δ + K.μ⁺ + K.ρ composite and name Definition (Fork) for the allocation/operand rule; remove the duplicated rule content from the intro.

### Issue 2: The full-clearance "links-retained-pointwise" fact is re-derived in at least three places
**ASN-0047, *Decomposition of K.μ~*** (admissibility clause (v), Step (A) Case `s_L`, and *Link-subspace fixity and realisation* sub-step (2)): The same mechanical fact — *K.μ⁺ writes only content-subspace positions and K.μ⁻ removes link positions only by suffix, so the link subspace is retained pointwise* — is established from scratch three times:
- clause (v): "*K.μ⁺ writes only content-subspace positions and K.μ⁻ removes link positions only by suffix, so links are retained pointwise*";
- Step (A) Case `s_L`: "*K.μ⁺ writes only content-subspace positions, so the link-subspace positions of `M'(d)` are exactly those K.μ⁻ retains*";
- sub-step (2): "*K.μ⁺ (amended) cannot create link-subspace V-positions, so any link-subspace V-position present in dom_L(M'(d)) must have been present in dom_L(M(d))*".

**Problem**: One load-bearing structural fact is re-argued in three sections rather than proved once and cited. A precise reader must verify it is the same claim each time. This is exactly the "same thing in different words" accretion the classifier flags, and it compounds the K.μ~ section's density.

**Required**: State the fact once (e.g., as a named one-line lemma "full-clearance preserves the link subspace pointwise: `M'(d)|_{dom_L} = M(d)|_{dom_L}`") and cite it at clause (v), Step (A), and sub-step (2) rather than re-deriving.

### Issue 3: Forward-pointer accretion to "Decomposition of K.μ~"
**ASN-0047, multiple sections**: At least four sites defer to the same downstream K.μ~ material: the S3★ matrix cell ("*§Decomposition of K.μ~*"), J3 ("*K.μ~ range-invariance ... derived in the Decomposition of K.μ~ section*"), the P4★ Class-(b) argument ("*K.μ~ range-invariance ... derived in the Decomposition of K.μ~ section*"), and the K.μ⁺_L Step-3 worked example ("*proved in the K.μ~ section above*").

**Problem**: Per the forward-reference-accretion guidance, multiple paragraphs in different sections deferring to one downstream location is a flag. The reader cannot evaluate S3★-under-K.μ~, J3, or P4★-under-K.μ~ in place; each requires a jump to the same section.

**Required**: Name the two downstream results these sites need (the K.μ⁻+K.μ⁺ realisation establishing S3★(Σ'), and **K.μ~ range-invariance**) as labelled results, and cite the label rather than the section, so each deferral resolves to a stated claim instead of "see the section below."

### Issue 4: D-SEQ★ reusability meta-justification and L14a redundant prose
**ASN-0047, *D-SEQ★ (per-subspace sequential positions, derived)*** and **L14a inapplicability**: The D-SEQ★ definition carries "*The derivation is a single-state implication consuming the per-state invariants on its left and producing the per-state shape on its right; it is reusable at every reachable state without re-invoking the outer induction*" — prose about how to *use* the derivation, not the derivation. Separately, the *L14a inapplicability* subsection argues at paragraph length why L14a is dropped, while the Properties-table row "*L14a | Inapplicable in the extended state (see L14a inapplicability prose above)*" already records the same fact and points back at the prose.

**Problem**: The D-SEQ★ note is a defensive justification of the derivation's reusability (it advances no step of the derivation). The L14a treatment states the same inapplicability conclusion in two places with a back-pointer between them.

**Required**: Delete the D-SEQ★ reusability sentence (reusability is implicit in any state-local derivation). Collapse the L14a treatment to a single canonical statement — either the table row or one prose sentence, not both with a cross-pointer.

## OUT_OF_SCOPE

### Topic 1: Interior link-arrangement contraction with renumbering
The model's K.μ⁻ contracts the link subspace by suffix removal only; the implementation's interior `DELETEVSPAN` compacts-and-renumbers surviving V-positions. The ASN correctly confines K.μ⁻ to suffix removal and routes the interior case to a future ASN (it is already logged in Open Questions).
**Why out of scope**: Renumbering-aware contraction is a new operation requiring its own invariant analysis; its absence is not an error in this transition taxonomy, which is the elementary set from which such an operation would compose.

### Topic 2: Provenance for link-endset participation
Whether content participating in link endsets requires additional permanence guarantees is raised as an Open Question.
**Why out of scope**: This extends the provenance contract (R) with cross-store coupling not yet modeled; it is future territory, not a gap in the current P4★/P7/P7a treatment.

VERDICT: REVISE
