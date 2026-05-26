# Channel Assignment — ASN-0098 review-13

**Date:** 2026-05-26 00:35

## Issue 1: LP-Fin is false for non-canonical spans
Reason: The fix is purely internal — the ASN's achievability section already commits to canonical construction (`ℓ = δ(n, #s)`, ordinal displacement with `#ℓ = #s`), and restricting LP-Fin to that form makes the structural-rigidity argument close. No design intent question or implementation evidence is needed; the canonical commitment is already present in the ASN.

## Issue 2: Tightness predicate is structurally unsatisfiable for non-canonical spans
Reason: Derivable from the ASN's own content. C-fin/L-fin plus the infinite-`F ∩ [s, s⊕ℓ)` cardinality (from Issue 1's counter-example) force non-canonical spans to be unconditionally non-tight; the fix is to restrict the predicate to canonical spans or add an explicit clause. The ASN's own commitment to canonical construction in the achievability section justifies the restriction without external input.

## Issue 3: Descendant document achievability argument requires canonical ℓ
Reason: Internal — the canonical-ℓ assumption is already implicit in the construction commitment (`ℓ = δ(n, #s)`) at the start of the achievability section; the fix is to surface it as an explicit header-level assumption and flag its load-bearing role in the descendant/ancestor cases. Proof-structural, no design or implementation question.

## Issue 4: Trace example's composite is not ValidComposite★ as written
Reason: Derivable from ASN-0047's already-referenced composite/J1★ machinery. The fix is editorial — either insert the K.ρ step into the composite or add a parenthetical noting R bookkeeping is elided since `project` does not consult `R` (a fact already established by LP14 in this ASN).
