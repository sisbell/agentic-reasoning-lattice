# Review of ASN-0053

## REVISE

### Issue 1: S9 case analysis drops the (start=, reach=) residual
**ASN-0053, S9 proof**: "Let i be the smallest index where αᵢ ≠ βᵢ" followed by Cases 1a/1b/2a/2b/3a/3b.
**Problem**: The enumeration covers start-differs (1a, 3a), one-sequence-shorter (1b, 3b), and start-equal-reach-differs (2a, 2b). It silently omits the configuration `start(αᵢ) = start(βᵢ) ∧ reach(αᵢ) = reach(βᵢ)`. The proof's whole strategy is to derive a witness position from a start- or reach-discrepancy; if a divergence index `i` could exist with both endpoints matching, no case would fire and the contradiction would never arise. The exhaustiveness of the case split is therefore unestablished.
**Required**: State explicitly that the residual case is vacuous: two spans sharing start and reach share width (by left cancellation, `start ⊕ w₁ = reach = start ⊕ w₂ ⟹ w₁ = w₂`, TA-LC, ASN-0034), hence `αᵢ = βᵢ`, contradicting that `i` is a divergence index. One sentence closes the analysis.

### Issue 2: S8 construction references the current interval before it is initialized
**ASN-0053, S8 Construction**: "Scan left to right, maintaining a current interval [s, r). For each span σᵢ in sorted order: — If start(σᵢ) ≤ r … — If start(σᵢ) > r …"
**Problem**: For the first span in sorted order, `r` is not yet defined, so neither branch condition is evaluable. The initialization `[s, r) = [start(σ₁), reach(σ₁))` appears only inside the *Initialization* clause of the invariant, not in the construction body. The construction as written is inconsistent with the invariant about whether σ₁ passes through the loop or seeds the interval.
**Required**: Move the initialization into the construction: seed `[s, r) = [start(σ₁), reach(σ₁))` and scan σ₂…σₙ through the if/else. Then the invariant's *Initialization* clause matches the construction body.

### Issue 3: Use-site inventory of D1 (forward-reference accretion)
**ASN-0053, reach-function section**: "Every proof below that constructs a span γ = (s, r ⊖ s) and asserts ⟦γ⟧ = {t : s ≤ t < r} depends on D1: the span's reach is s ⊕ (r ⊖ s) = r."
**Problem**: This sentence enumerates downstream consumers of D1 rather than advancing the reach-function argument. It is exactly the "definition's introduction enumerates downstream consumers" pattern the anti-bloat classifier targets — each construction below already cites D1 in place, so the pre-announcement is noise the reader must skip.
**Required**: Delete the sentence. The point that `s ⊕ (r ⊖ s) = r` under the level constraint is already made by the D2/D1 discussion immediately above.

### Issue 4: D1 round-trip and the #a>#b failure each stated twice (redundancy)
**ASN-0053, reach-function section**: paragraph 3 states "the identity a ⊕ (b ⊖ a) = b additionally requires #a ≤ #b (D1)" and "For #a > #b, the foundation already settles the failure: D0's postcondition gives a ⊕ (b ⊖ a) ≠ b directly." A later paragraph restates the affirmative half ("The displacement round-trip is guaranteed by the foundation: for tumblers a, b ∈ T with a < b … a ⊕ (b ⊖ a) = b (D1)") and the final paragraph restates the failure with an example ("When #start > #width, the round-trip fails by D0's #a > #b postcondition…").
**Problem**: The same two foundation facts (D1 success for `#a ≤ #b`, D0 failure for `#a > #b`) are each asserted twice across the section in different words — the "two paragraphs say the same thing" pattern. Since level-uniform spans force `#start = #reach`, only the equal-length case is ever exercised, so the duplicated `#a > #b` material is doubly redundant.
**Required**: Consolidate into a single statement of the D0/D1 dichotomy. Retain at most one worked instance of the `#start > #width` failure if the boundary illustration is wanted; drop the duplicate prose.

## OUT_OF_SCOPE

### Topic 1: Span-set–to–span-set difference bound
**Why out of scope**: The tight bound on `|normalize(⟦Σ₁⟧ \ ⟦Σ₂⟧)|` for two span-sets is a genuine extension of S11d, not a gap in it. The ASN itself defers it under Open Questions; it belongs in a future ASN building on this algebra.

### Topic 2: Intersection/split across hierarchical levels
**Why out of scope**: The behavior of span operations at differing depths (where `level_compat` fails) is correctly excluded by S6 as a precondition and listed under Open Questions. Defining well-formed cross-level span representations is new territory, not an error here.

VERDICT: REVISE
