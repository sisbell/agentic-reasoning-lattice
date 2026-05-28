# Review of ASN-0077

## REVISE

### Issue 1: K.ρ frame misrepresented in O0(c) totality closure for dom(C)

**ASN-0077, O0(c) totality derivation**: "...or leaves `C` unmentioned in both effect and frame (K.ρ, whose effect adds to `R` and whose frame `(A d :: M'(d) = M(d))` names only arrangements); by the framing convention adopted in (b), `C' = C` for K.ρ as well."

**Problem**: K.ρ's actual frame in ASN-0047 is `C' = C; E' = E; (A d :: M'(d) = M(d))` — it explicitly names C with the preservation clause `C' = C`. The author truncates K.ρ's frame to just the M-clause, misclassifying K.ρ as falling under the framing-convention fallback when K.ρ actually belongs in the explicit-`C' = C`-frame-clause group (alongside K.δ, K.μ⁺, K.μ⁻, K.μ~, K.λ, K.μ⁺_L). The conclusion `C' = C` for K.ρ is correct, but the cited route through framing convention is unsound because K.ρ's actual frame establishes `C' = C` directly.

This appears to be inherited from ASN-0098's LP14, which legitimately abbreviates K.ρ's frame to `(A d :: M'(d) = M(d))` for its projection-invariance purpose; the abbreviation is benign in LP14's context where only the M-clause matters, but reusing it for direct C-preservation introduces the factual misreading.

By contrast, the parallel L-closure earlier in (b) is correctly handled because K.ρ's actual frame *does* genuinely omit L — the framing convention applies legitimately there.

**Required**: Correct the classification — either (a) place K.ρ in the explicit-`C' = C`-frame-clause group, citing K.ρ's full frame `C' = C; E' = E; (A d :: M'(d) = M(d))`; or (b) keep the framing-convention treatment but cite K.ρ's frame accurately and note that the convention happens to coincide with the explicit clause in this case. A reader following the proof needs the cited foundation frame to match the actual foundation frame.

VERDICT: REVISE
