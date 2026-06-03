# Review of ASN-0099

## REVISE

### Issue 1: F9 and A1a treat K.μ~ as a single-step / atomic operation, contradicting its definition as a non-atomic composite

**ASN-0099, "Arrangement Independence" (F9) and (A1)**:
- F9: "For any *single-step* transition Σ → Σ' produced by a K.μ-family operation (K.μ⁺, K.μ⁻, **K.μ~**, K.μ⁺_L) and any I ⊆ T: findlinks(I, Σ) = findlinks(I, Σ')."
- A1a: "(published-frame preservation, covering {K.σ, K.α, K.δ, **K.μ~**, K.μ⁺_L}): conclusion immediate from the substrate's published L' = L frame clause. **No interpretive commitment.**"

**Problem**: Foundation ASN-0047 states explicitly that "**The named composite K.μ~ is not atomic**; it may appear in the sequence as shorthand for its K.μ⁻ + K.μ⁺ decomposition." A "single-step transition Σ → Σ'" (one arrow) therefore cannot be "produced by" K.μ~ — invoking K.μ~ is two transitions Σ → Σ_mid → Σ'. F9's framing places a non-atomic operation in a single-step claim, and the ASN is otherwise meticulous about atomicity (it cites SequentialTransitionAxiom and reasons step-by-step in F9★). The defect is not in the *conclusion* (findlinks invariance does hold across the composite) but in the *route*: the correct treatment composes F9 over the two atomic steps K.μ⁻ and K.μ⁺. That composition also exposes a second tension — both K.μ⁻ and K.μ⁺ fall under **A1b** (closed-world reading, "convention-grounded"), and ASN-0047's K.μ~ frame is labeled "(derived)" precisely from that decomposition. Classifying K.μ~ under A1a as carrying "no interpretive commitment" is at odds with the fact that its L'=L clause is derived from two A1b operations. The A1a/A1b distinction the ASN itself draws is muddied by placing K.μ~ on the A1a side.

**Required**: Reframe F9 (and remove K.μ~ from A1a's set) so that K.μ~ is handled as its K.μ⁻ + K.μ⁺ decomposition — both atomic steps under A1b — with the composite conclusion obtained by transitivity (as F9★ already does for multi-step sequences). Either justify why K.μ~'s "(derived)" L'=L is genuinely convention-free, or move it under A1b and have F9/F17/F18 inherit A1b's commitment at K.μ~ as they do at K.μ⁺/K.μ⁻. The single-step claims should range only over genuinely atomic operations (K.μ⁺, K.μ⁻, K.μ⁺_L).

## OUT_OF_SCOPE

None. The ASN appropriately defers the inverse direction (FOLLOWLINK), partition tolerance, caching, access control, and combined filtered-scoped forms to the "What We Have Not Specified" and "Open Questions" sections rather than mis-specifying them here.

VERDICT: REVISE
