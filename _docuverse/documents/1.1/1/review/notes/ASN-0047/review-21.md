# Review of ASN-0047

## REVISE

### Issue 1: Theorem forward reference misdirects for P8 and S2–S8-fin
**ASN-0047, Coupling and isolation, Reachable-state invariants theorem**: "as the derivations of P4, P6, P7, P8 and the elementary-transition analysis of S2–S8-fin show below"
**Problem**: "Show below" is incorrect for two of the five cited items. P8 is derived in the Permanence section (above the theorem), and the S2–S8-fin preservation arguments appear in the Elementary transitions section (also above). Only P4 (Coupling and isolation), P6, and P7 (Temporal decomposition) are actually below.
**Required**: Fix the reference direction, e.g., "as derived above for P8 and S2–S8-fin, and below for P4, P6, P7."

### Issue 2: K.δ freshness not grounded in GlobalUniqueness
**ASN-0047, Elementary transitions, K.δ**: "E' = E ∪ {e} where e ∉ E ∧ ValidAddress(e) ∧ ¬IsElement(e)"
**Problem**: K.α explicitly cites GlobalUniqueness (ASN-0034) to justify a ∉ dom(C): "By GlobalUniqueness (ASN-0034), a is distinct from every previously allocated address." K.δ states e ∉ E without the corresponding citation, despite noting that entity creation uses "the same allocation mechanism" (inc/TA5). The freshness guarantee for entity addresses relies on the same GlobalUniqueness result — the asymmetry in citation leaves the justification implicit where K.α makes it explicit.
**Required**: Add a GlobalUniqueness citation to K.δ paralleling K.α's, or at minimum note that e ∉ E follows from the same GlobalUniqueness result that governs K.α.

### Issue 3: Temporal decomposition table omits K.δ's presentational-layer effect
**ASN-0047, Temporal decomposition, table**: K.δ appears only in the Existential row.
**Problem**: The prose directly below the table says "K.δ for documents also initialises M'(e) = ∅, extending M's domain — a presentational-layer effect." The table assigns each transition to exactly one row, placing K.δ solely in Existential. A reader referencing the table alone would conclude K.δ has no effect on M. The broader claim ("no elementary transition touches all three layers") is correct, but the table understates K.δ's scope — it touches two of the three layers.
**Required**: Annotate K.δ in the table (e.g., "K.δ†" with a footnote noting the M-initialization effect for documents), or add K.δ to the Presentational row with a qualifier. The text already provides the explanation; the table should not contradict it.

## OUT_OF_SCOPE

### Topic 1: Whether Contains(Σ) ⊆ R should track intermediate-state containment
The current coupling constraints (J1/J1') tie provenance to the composite's final-state containment. Content briefly placed in an arrangement and then removed within the same composite leaves no provenance trace. An alternative design — provenance for every K.μ⁺ step, regardless of subsequent K.μ⁻ — would give a strictly stronger historical record. The ASN's choice is internally consistent (P4a's witnessing states are reachable states, not intermediate states), but the design trade-off belongs in a future ASN addressing transactional semantics.
**Why out of scope**: This is a design-level question about the granularity of historical memory, not an error in the current formulation.

### Topic 2: Link vs. document arrangement structure
The ASN places links in E_doc and defers their structural distinction from documents. S8a constrains only text-subspace V-positions (v₁ ≥ 1); link-subspace positions (v₁ = 0) and link endset arrangements are unconstrained by any current invariant. A future ASN should specify arrangement invariants for the link subspace.
**Why out of scope**: The ASN explicitly defers this ("The structural distinction between documents and links... belongs to a separate analysis").

VERDICT: REVISE
