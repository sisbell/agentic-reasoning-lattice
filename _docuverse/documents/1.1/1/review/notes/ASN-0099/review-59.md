# Review of ASN-0099

I checked the operation definitions, the conformance contracts (F2/F3 and variants), the survivability/monotonicity family (F9–F9★, F9-λ, F11, F19), the ordering claims (F10/F10a + sub-lemmas), and the worked example against each cited foundation.

## REVISE

None. The proofs I stress-tested hold:

- **Silent-projection uniqueness** — conditions (i) `g ⊆ img` and (ii) `img ⊆ g` are stated structurally (witnessed-by-a-V-position-of-R, reproduces-present-positions) and are genuine mutual inclusions; the alternative-treatment families (constant-∅, sentinel totalisation, constant-`ran`) correctly fail exactly one conjunct. The strengthened bound (image of `R`, not `ran`) is load-bearing and correctly distinguishes the constant-`ran` family.
- **F10a Case (ii) zero-counting** — verified: with `zeros(d₁)=zeros(d₂)=2` and `d₁ ≺ d₂`, T4 forces both of `d₁`'s zeros to positions `≤ #d₁−1` and `d₁[#d₁]≠0`; `d₂` inherits these on `1..#d₁`, exhausting its zero budget, so `d₂_{#d₁+1} ≥ 1` and the appended separator in `b_L(d₁)` gives T1 case (i) divergence at `#d₁+1`. Both cases are exhaustive for `d₁ < d₂` (versions nest, so Case (ii) is reachable, not vacuous).
- **A1/A1a** — every atomic op of `V ∖ {K.λ}` publishes `L'=L` in its operative frame, including the amended K.μ⁺/K.μ⁻ extended-state frames; K.μ~ correctly reached only via decomposition.
- **F9-λ disjoint-union** — freshness discharges disjointness; the prior-key/fresh-key split via PerLinkInvariance is sound, and ComprehensionInvariantUnderΣL is correctly declared inapplicable across domain growth.
- **F11 vs ASN-0098 V-side** — the I-side/V-side persistence divergence is correctly distinguished, and Query 5 exhibits the K.μ⁻ contraction that breaks V-side while I-side survives.
- **F13/F20/F20a** — the existential-distributes-over-disjunction lift and the three-step F20a chain are each licensed by one prior identity.
- Boundary cases (empty `I`, empty `R`, empty `dom(Σ.L)`, empty constraint set, empty target, empty non-type slots, out-of-range slot index) are all handled.

No cross-ASN references outside the foundation set; no drift into implementation mechanics (the spec stays at set-comprehension + conformance level).

## OUT_OF_SCOPE

The Open Questions (off-`dom(C)∪dom(L)` query semantics, partition tolerance, concurrency model, access-control composition, audit witnesses, timing bounds, FOLLOWLINK inverse) are correctly deferred — each is new territory, not a gap in this ASN.

VERDICT: CONVERGED
