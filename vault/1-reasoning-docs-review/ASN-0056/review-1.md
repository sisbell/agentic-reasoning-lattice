# Review of ASN-0056

## REVISE

### Issue 1: S11d proof incomplete for containment case (iv)
**ASN-0056, Unified difference bound**: "| (iv) Containment | at most 2 spans | 2 spans | S11 (ASN-0053) |"
**Problem**: SC case (iv) has two directions: β properly contained in α, and α properly contained in β. S11 (ASN-0053) has the precondition ⟦β⟧ ⊆ ⟦α⟧ — it only handles the first direction. When α ⊆ β, the difference ⟦α⟧ \ ⟦β⟧ = ∅ (0 spans), which trivially satisfies the bound, but the proof cites S11 as covering all of case (iv) without acknowledging this subcase.
**Required**: Split the containment row into its two directions, or add a sentence noting that when α ⊆ β the difference is trivially empty and S11 covers the converse.

### Issue 2: S11c symmetric overlap case — preconditions unverified
**ASN-0056, Difference for proper overlap**: "For the symmetric case (start(β) < start(α) < reach(β) < reach(α)), the difference ⟦α⟧ \ ⟦β⟧ = {t : reach(β) ≤ t < reach(α)}, constructed as (reach(β), reach(α) ⊖ reach(β)) — also exactly 1 span."
**Problem**: The main case gets a full proof: D1 preconditions verified, T12 checked, level-uniformity established. The symmetric case gets one sentence. The construction uses reaches rather than starts, so the level-compatibility argument is different: it requires chaining through level-uniformity of both spans (#reach(α) = #start(α) = #start(β) = #reach(β)) to establish D1's #a ≤ #b and the divergence bound. This chain is not stated.
**Required**: Verify D1 preconditions for (reach(β), reach(α)): reach(β) < reach(α) (given), #reach(β) = #reach(α) (from level-uniformity + level_compat on starts), divergence of type (i) with k ≤ #reach(β) (follows from equal lengths). Verify level-uniformity of the constructed span.

### Issue 3: Registry type mismatch for SC
**ASN-0056, Statement registry**: "| SC | INV, predicate | SpanClassification (ASN-0053) | cited |"
**Problem**: ASN-0053 defines SC as "LEMMA, lemma" — a classification lemma establishing five mutually exclusive, exhaustive cases. The registry lists it as "INV, predicate".
**Required**: Change to "LEMMA, lemma" to match ASN-0053.

## OUT_OF_SCOPE

### Topic 1: Span-set difference bounds
**Why out of scope**: The ASN correctly identifies this as an open question. The bound for ⟦Σ₁⟧ \ ⟦Σ₂⟧ where Σ₁ and Σ₂ are normalized span-sets is a natural extension but requires new machinery (iteration over component spans, interaction between normalization and difference). This is new territory, not an error in this ASN.

VERDICT: REVISE
