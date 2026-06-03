# Review of ASN-0099

## REVISE

### Issue 1: K.ρ is misclassified into the convention-grounded lemma A1b; it publishes L' = L

**ASN-0099, A1 / A1b / appendix**: "Five of the eight non-allocating operations list `L' = L` in their published frames; three (K.μ⁺, K.μ⁻, K.ρ) omit `L` from the published frame." And A1b: "closed-world preservation, covering {K.μ⁺, K.μ⁻, K.ρ}."

**Problem**: Per the foundation as given, K.ρ does **not** omit `L` from its frame. ASN-0047's K.ρ (ProvenanceRecording) publishes:

> *Frame:* `C' = C; L' = L; E' = E; (A d :: M'(d) = M(d))`

`L' = L` is explicit. So K.ρ belongs in A1a (published-frame preservation), not A1b (the closed-world, convention-grounded reading). Only **two** atomic operations — K.μ⁺ and K.μ⁻ — genuinely omit `L` from their published frames and require the closed-world reading; the "three operations omit" count is wrong.

The error is internally corroborated by the ASN's own inconsistencies:
- The count "five list `L' = L`" is only reachable by counting {K.σ, K.α, K.δ, K.μ⁺_L, K.ρ} — i.e., it already presumes K.ρ is a publisher, contradicting the very next clause that puts K.ρ in the omit-three.
- F17/F18 state only "inherit A1b's commitment at the **K.μ⁺ and K.μ⁻** sub-cases" — correctly omitting K.ρ — while A1 and F9-cor wrongly include it.

This matters because A1b is the weakest, most-caveated link in the chain (an unaxiomatised convention this ASN adopts methodologically). Routing K.ρ through it overstates the methodological dependency for a fact the substrate already publishes outright.

**Required**:
- Move K.ρ from A1b to A1a; correct A1b's membership to {K.μ⁺, K.μ⁻}.
- Fix the count in A1: only **two** atomic non-allocating operations omit `L` from their published frames (K.μ⁺, K.μ⁻); the publishers are {K.σ, K.α, K.δ, K.μ⁺_L, K.ρ}. If a "third" convention-reached operation is intended, that is K.μ~ — but it is non-atomic and already handled separately via its K.μ⁻ + K.μ⁺ decomposition, so it should not be conflated with K.ρ.
- Propagate the fix to F9-cor ("inherits A1b's commitment at the K.μ⁺, K.μ⁻, **K.ρ** sub-cases" and "remaining four ... A1a" → K.ρ joins A1a, giving five A1a ops and two A1b ops).
- Correct the appendix grounding (ii), which lists K.ρ alongside K.μ⁺/K.μ⁻ as needing the closed-world reading.

## OUT_OF_SCOPE

None.

VERDICT: REVISE
