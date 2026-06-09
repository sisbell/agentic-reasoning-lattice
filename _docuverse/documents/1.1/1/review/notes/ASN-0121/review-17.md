# Review of ASN-0121

## REVISE

### Issue 1: FL-WP(b) attributes a set-equality to R6b that R6b does not establish

**ASN-0121, FL-WP(b) derivation**: "Now `nullified(Σ') = nullified(Σ) ∪ {t ∈ dom(Σ.L) : t ∈ coverage(G')}` (R6b), so `a ∈ addressable(Σ') ⟺ a ∉ nullified(Σ) ∧ a ∉ coverage(G')`."

**Problem**: R6b (ASN-0086, SingleDepthRetraction) is the one-directional membership claim `a ∈ A_rel^Σ ∧ (b,F',G') ∈ L_R^Σ ∧ a ∈ coverage(G') ⟹ a ∈ nullified(Σ)`. It supplies only the ⊇ direction of the displayed union (new targets become nullified). The ⊆ direction — that *no* address outside `nullified(Σ) ∪ coverage(G')` becomes nullified — is exactly what makes the wp the **weakest** precondition: it licenses concluding `a ∉ nullified(Σ')` from `a ∉ nullified(Σ) ∧ a ∉ coverage(G')`. That direction is not R6b; it requires the added premise that the retraction-bearing K.λ extends the retraction relation by exactly the one tuple, `L_R^{Σ'} = L_R^Σ ∪ {(b, ∅, G')}` (immutability L12 + the K.λ effect), so that the definition of `nullified(Σ')` decomposes as claimed. As written, the load-bearing ⊆ step is asserted under an insufficient citation — the same class of addressability gap the FL-WP(a) revision was meant to close.

**Required**: Show the ⊆ direction explicitly: cite `L_R^{Σ'} = L_R^Σ ∪ {(b,∅,G')}` and unfold the definition of `nullified(Σ')` to obtain, for existing `a ∈ dom(Σ.L)`, `a ∈ nullified(Σ') ⟺ a ∈ nullified(Σ) ∨ a ∈ coverage(G')`. R6b then discharges only the ⟸ half.

### Issue 2: FL-WP(a) leaves "ordinary, non-retraction link" undefined where the definition is load-bearing

**ASN-0121, FL-WP(a) derivation**: "An ordinary (non-retraction) K.λ leaves the retraction relation fixed, `L_R^{Σ'} = L_R^Σ`."

**Problem**: `L_R^{Σ'} = L_R^Σ` holds only because the committed type endset is *not* in the retraction coverage class — `coverage(Θ) ≠ coverage(R)`, so `ℓ ∉ L_R^{Σ'}`. The text uses "ordinary, non-retraction link" as if self-evident, but the precise condition that licenses the L_R-invariance step is never stated. Since this invariance is exactly what reduces `nullified(Σ')` to a test against `L_R^Σ`, the omitted condition is part of the proof, not flavor text.

**Required**: Define "ordinary" as `coverage(Σ'.L(ℓ).e₃) ∉ [coverage(R)]` (the committed type is not the retraction class), making `ℓ ∉ L_R^{Σ'}` and hence `L_R^{Σ'} = L_R^Σ` explicit.

## OUT_OF_SCOPE

None. The ASN correctly defers version-/time-qualified inquiry, V-spec/I-address agreement, and federation reach to its Open Questions rather than asserting claims about them.

VERDICT: REVISE
