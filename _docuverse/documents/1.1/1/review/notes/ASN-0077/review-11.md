# Review of ASN-0077

## REVISE

### Issue 1: O0(b) closure assumption for `dom(L)` is asserted, not derived

**ASN-0077, O0 derivation (b)**: "Composing: every ℓ ∈ dom(L) arose through a K.λ event whose precondition pins L1c's chain seed to d ∈ E_doc, the allocating document. Hence origin(ℓ) names the document that allocated ℓ."

**Problem**: The phrase "every ℓ ∈ dom(L) arose through a K.λ event" is the load-bearing bridge of the entire dom(L) extension. L1c on its own only names a chain seed `t₀ = origin(ℓ)`; K.λ's precondition `origin(ℓ) = d` only constrains link-allocation events that actually occur. To compose them and conclude that origin(ℓ) names the allocating document, one needs the closure fact that *every* ℓ in *any* reachable dom(L) came from a K.λ event — i.e., no other transition can place addresses into dom(L). This requires (i) inspecting ASN-0047's transition effects and frames to confirm K.α, K.δ, K.μ⁺, K.μ⁻, K.μ~, K.ρ, and K.μ⁺_L all preserve L (only K.λ modifies dom(L)), and (ii) invoking the initial state L₀ = ∅ together with induction over reachable transition sequences. The current derivation performs neither inspection nor induction; it asserts the closure.

The pointwise extension proof for dom(C) (S7 of ASN-0036) does not face this issue because S7 itself is established with the closure implicit in ASN-0036. O0 reproves the semantic correspondence for dom(L) "from scratch" using foundation pieces, so the closure step needs to be made explicit here.

**Required**: Insert an explicit closure step before the L1c + K.λ composition. For example: "By inspection of ASN-0047's transition effects and frames, K.λ is the unique transition that modifies dom(L) — K.α, K.δ, K.μ⁺, K.μ⁻, K.μ~, K.ρ, and K.μ⁺_L all preserve L. Combined with L₀ = ∅ in the initial state Σ₀, induction over reachable transition sequences gives that every ℓ ∈ dom(L) at any reachable state was placed by some K.λ event." Then the L1c + K.λ-precondition composition discharges (b) without a gap.

VERDICT: REVISE
