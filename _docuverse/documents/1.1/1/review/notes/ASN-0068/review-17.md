# Review of ASN-0068

## REVISE

### Issue 1: Result-type slot carries downstream claim material
**ASN-0068, "The Input" (Result definition)**: "Equivalently, *given a fixed admissible input* ... each element `M ∈ Result` lifts to a set of span-pairs `π*_{m_a, m_b}(M) ⊆ Span × Span` via the set-level image of the per-run projection formalized below as CV-SPAN-VIEW; the lift ... is injective ... placing `Result` in bijection with its image ... The lift is input-parameterized by `(m_a, m_b)`; it is not a universal isomorphism on `Result`."
**Problem**: This is a forward reference ("formalized below as CV-SPAN-VIEW") that fully restates CV-SPAN-VIEW (b) and (c) inside a slot whose only job is to fix `Result := P(T × T × ℕ⁺)`. The injectivity/bijection and "not a universal isomorphism" caveats are proved later; duplicating them here forces the reader past presentational meta-prose to reach the actual type. It is also imprecise in this slot: for admissible inputs with `V_S(d_a) = ∅`, `m_a` is undefined and `π*` does not exist, yet the slot asserts the bijection blanketly.
**Required**: Reduce the slot to `Result := P(T × T × ℕ⁺)` (with the one-line gloss "a set of triples ... defined below"). Let CV-SPAN-VIEW own the lift and its properties.

### Issue 2: Drafting-choice justification in CV-IN
**ASN-0068, "The Input" (CV-IN closing clause)**: "both clauses constrain the same `σ` at incompatible depths and admissibility fails — the inadmissibility is explicit rather than buried in a side-conditional resolution."
**Problem**: The trailing clause justifies *how the spec is written* rather than advancing the rule. The rule ("admissibility fails") is complete without it.
**Required**: Delete "— the inadmissibility is explicit rather than buried in a side-conditional resolution."

### Issue 3: Placement rationale appended to the action-point argument
**ASN-0068, action-point paragraph (final sentence)**: "We make the constraint explicit at the input level rather than rely on the downstream relation `corr_{a,b}` to filter cross-subspace positions via L0 + L14 (ASN-0047); structurally, the input is what the operation contracts on."
**Problem**: The preceding V-position-capture argument is legitimate reasoning, but this closing sentence defends a drafting location ("explicit at the input level rather than ... downstream"). It does not advance the claim.
**Required**: Delete the sentence.

### Issue 4: "Which layer enforces emptiness" meta-prose in CV-EMPTY
**ASN-0068, CV-EMPTY justification**: "The two situations differ in *which* layer enforces emptiness — caller's choice versus CV-IN's admissibility filter — but neither requires exception logic or special-case handling at the operation level."
**Problem**: The substance (both situations give `⟦R_a⟧ = ∅`, hence `∅`) is already stated. This sentence editorializes about layering and "exception logic," advancing no reasoning.
**Required**: Remove the sentence.

### Issue 5: Future-amendment process note in CV-ATOM
**ASN-0068, CV-ATOM derivation (final sentence)**: "Any future addition of a width threshold, merge window, or block-alignment offset would require an explicit amendment to CV-MAX or the run definition, which would automatically be flagged as a change against this claim."
**Problem**: This describes the review process for hypothetical future edits, not a property of the operation. It is meta-prose about how the spec would be maintained.
**Required**: Delete the sentence.

### Issue 6: Self-comparison structure stated three times
**ASN-0068, self-comparison material**: the paragraph "The relation behaves differently depending on whether the restrictions coincide. When `R_a = R_b` ... When `R_a ≠ R_b` ..." duplicates the content subsequently formalized in CV-SELF (`D` / `X`), which is then re-derived a third time in CV-SELF's justification. The same section also carries "We name this structure as a labeled claim, parallel to CV-LINK-SELF for the content subspace."
**Problem**: Two adjacent paragraphs say the same thing in different words before CV-SELF restates it formally; "We name this structure as a labeled claim, parallel to..." is naming-rationale meta-prose. A reader must read the same decomposition three times to extract one claim.
**Required**: Drop the informal "behaves differently" paragraph (CV-SELF subsumes it) and the "We name this structure..." sentence; keep CV-SELF and its justification.

## OUT_OF_SCOPE

None. The note stays within COMPAREVERSIONS operation semantics; it does not drift into INSERT/DELETE/COPY/REARRANGE mechanics, link semantics, or replication.

The mathematics is sound: CV-MAX existence (walk termination grounded in D-SEQ★/S8a/S8-fin) and uniqueness (lockstep-offset + maximality contradiction) are complete and case-covered; boundary cases (empty restriction, fresh fork, self-transclusion, differing depths) are verified concretely in Examples 1–4; CV-PRED, CV-SPAN-VIEW, CV-FIN, CV-SYM, CV-RO, CV-DETERM each carry explicit derivations. The findings above are accreted meta-prose and forward-reference duplication, not correctness gaps.

VERDICT: REVISE
