# Review of ASN-0043

## REVISE

### Issue 1: L11b's non-injectivity witness writes the carried payload as a fixed triple, contradicting the arity-≥3 generality it quantifies over

**ASN-0043, L11b — NonInjectivity, *Construction of fresh `a'`***: "`Σ'.L = Σ.L ∪ {a' ↦ (F, G, Θ)}`" and "The payload `ℓ = (F, G, Θ) = Σ.L(a)` has T12-well-formed spans … and satisfies L3 (arity ≥ 3, slot 3 the non-empty type endset …)."

**Problem**: L11b is universally quantified over `a ∈ dom(Σ.L)` with no arity restriction, and L3 (plus the ASN's own worked example, where `a₃` has arity 4) establishes that conforming links may have arity `N > 3`. For such an `a`, the equation `(F, G, Θ) = Σ.L(a)` is literally false — a 4-tuple is not a 3-tuple — so the witness as written only covers the arity-3 case. The FSP appeal in the same paragraph correctly admits any `N ≥ 3`, so the argument is sound, but the notation silently narrows the witness to the standard triple while the parenthetical even concedes "arity ≥ 3." The carried payload must be written generically.

**Required**: Write the duplicated payload as `Σ.L(a)` (an `N`-tuple, `N ≥ 3`) rather than `(F, G, Θ)`, so the witness matches the quantifier's full domain. The same applies wherever the construction text reuses `(F, G, Θ)` to denote `Σ.L(a)`.

### Issue 2: L11a closes with a defensive justification of what is *not* needed

**ASN-0043, L11a — LinkUniqueness**: "Hence both link-producing events are distinct allocation events within the single T10a system 𝒯, which is exactly GlobalUniqueness's precondition; GlobalUniqueness then yields `a₁ ≠ a₂` directly. No reconstruction of T10a's at-most-once edge-sharing is needed — the within-tree membership is all GlobalUniqueness requires."

**Problem**: The argument concludes at "GlobalUniqueness then yields `a₁ ≠ a₂` directly." The trailing sentence ("No reconstruction … is needed") advances no reasoning — it pre-empts a counterargument by stating what the proof does *not* have to do. This is exactly the defensive-justification meta-prose the anti-bloat classifier flags; a precise reader must skip past it to confirm the claim is already closed. (The adjacent remark relating L11a to partial-function single-valuedness does advance understanding and need not be cut.)

**Required**: Delete the "No reconstruction … requires" sentence.

## OUT_OF_SCOPE

None.

VERDICT: REVISE
