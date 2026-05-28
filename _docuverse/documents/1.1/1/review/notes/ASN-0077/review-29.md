# Review of ASN-0077

## REVISE

### Issue 1: Cross-ASN reference to non-foundation ASN-0093
**ASN-0077, O0 derivation (b)**: "the working frame's elementary transition vocabulary is ASN-0047's transitions (K.α, K.δ, K.μ⁺, K.μ⁻, K.μ~, K.λ, K.μ⁺_L, K.ρ) together with ASN-0093's K.σ" and "K.σ's defining clause in ASN-0093 modifies `dom(M)` by registering the new document while naming neither `L` nor `dom(L)` in effect or frame."
**Problem**: ASN-0093 is not in the foundation list. The ASN references ASN-0093's K.σ in load-bearing positions: the O0(b) closure enumeration, the O0(c) parallel closure for `dom(C)`, the working-frame definition, and discussion of V-span behavior. This violates the standard requirement that ASNs cite only foundation ASNs.
**Required**: Either (a) replace direct K.σ references with citations of LP8 (DocumentRegistrationInvariance, ASN-0098), which abstracts uniformly over K.σ and K.δ-IsDocument and *is* foundation-attested; or (b) restrict the working frame to ASN-0047 transitions only and discharge K.σ's contribution through LP8.

### Issue 2: Closure argument appeals to unstated framing convention
**ASN-0077, O0 derivation (b)**: "The framing convention that components unmentioned in effect or frame are unchanged then yields `L' = L` for K.μ⁺, K.μ⁻, K.ρ, and K.σ as well, so the only source of growth in `dom(L)` is a K.λ event."
**Problem**: The cited foundation ASNs do not establish this framing convention as a formal lemma. K.μ⁻'s frame in ASN-0047 reads `C' = C; E' = E; R' = R; (A d' : d' ≠ d : M'(d') = M(d'))` — L is unmentioned. P3 (ArrangementMutabilityOnly) gives only monotonicity `dom(L) ⊆ dom(L')` and value preservation `L'(ℓ) = L(ℓ)`; neither establishes K.λ as the *unique* source of growth, which is what the closure step requires. The same gap propagates to O0(c) via the parallel argument for `dom(C)`.
**Required**: Either explicitly state the framing convention as an axiom of the working frame, or restate the K.λ-uniqueness argument from the explicit Effect clauses of each transition (some — K.α, K.δ, K.μ~, K.μ⁺_L — already declare L' = L explicitly; for K.μ⁺, K.μ⁻, K.ρ a different grounding is needed).

### Issue 3: Imprecise characterization of K.α's emission algorithm
**ASN-0077, Singleton I-span edge case**: "K.α invokes only `inc(·, 0)` — never `inc(·, k)` with `k > 0` — so although T10a-conformance abstractly permits child-spawning, K.α's algorithm structurally precludes `A_C(d)` from spawning content children."
**Problem**: Per ASN-0047, K.α's *first emission* is constructed directly as the tumbler `[d.0.s_C.1]`, not via any `inc` call; only the *subsequent emission* invokes `inc(·, 0)`. The blanket claim "K.α invokes only `inc(·, 0)`" is therefore inaccurate. The downstream conclusion (every A_C(d) output has length `#d + 3`) is correct, but its derivation must account for both emission cases.
**Required**: Rephrase to acknowledge K.α's two-case algorithm: the first emission produces `[d.0.s_C.1]` directly with length `#d + 3`; subsequent emissions use `inc(·, 0)` which preserves length (TA5(c), ASN-0034). Together these force every A_C(d) output to have length `#d + 3`.

VERDICT: REVISE
