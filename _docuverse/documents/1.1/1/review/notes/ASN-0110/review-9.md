# Review of ASN-0110

I read this as a pure-query specification: define region, define "touch," define the returned object, and characterize what survives the withholding of link identity. I checked every proof, the worked instance, the boundary cases, and foundation usage.

## REVISE

None. The proofs are complete (no "by similarly" hand-waves), every boundary is addressed, the worked instance is arithmetically correct, and the depth requirements (concrete example, non-trivial wp, derived consequences) are met.

Specifically verified:
- **RE-overlap / RE-decide**: the half-open boundary case (`α = s ⊕ ℓ` excluded) is explicit, and decidability correctly iterates over the finite `I` rather than the infinite `coverage`, discharged by T2/TA0/TA-strict and L-fin.
- **Worked instance**: `W = {(a₁,1),(a₂,1),(a₂,2)}`, `E₁={F₁,F₂}`, `E₂={F₁}`, `E₃=∅` all recompute correctly under δ(1,8)/shift arithmetic; RE-full (whole `F₁` returned with its non-touching span `(c₄,δ)`) and RE-role (value `F₁` filed under two roles) are genuinely exercised.
- **RE-wp**: the two disjuncts (unconditional persistence vs. value-gated growth) are mutually exclusive by the K.λ freshness lemma; `pre` correctly carries the sub-allocator binding with freshness as a derived guarantee, matching ASN-0093.
- **RE-mono**: correctly rests on the multi-step ★ lemmas (LP13, LP3★) rather than lifting single-step RE-immut.
- **RE-anon / RE-result**: the set-vs-bag tension is decisively resolved toward *set* ("multiplicity is structurally absent"), and the touch-by-coverage / return-by-value asymmetry is internally consistent with RE-exact read as literal set equality.
- **Boundaries**: empty region (RE-zero), empty store vs. non-empty arity-3 store (RE-conform identifies the empty-store `⟨⟩` vs `⟨∅,∅,∅⟩` divergence precisely), deleted V-content (RE-Vside silent partiality), transclusion (RE-translucent) — all covered.

Foundation usage is clean: `coverage`, `image`, T12, L3, L11b, L12, L-fin, S8-fin, the LP-family, and the K.λ/K.μ contracts are cited to provided foundation ASNs (0034/0036/0043/0047/0086/0093/0098/0099); `touches` is a justified per-endset refinement of F1's per-link `matches`, not a reinvention.

## OUT_OF_SCOPE

### Topic 1: V-space presentation of returned endsets (OQ1)
**Why out of scope**: RE-Vside returns I-space endsets verbatim; presenting them back in the querying document's V-coordinates is a separate lossy projection, correctly deferred. The operation is well-defined without it.

### Topic 2: Reconstructibility boundary for per-link from/to/type pairing (OQ3)
**Why out of scope**: RE-reveal establishes the existential non-recoverability (RE-anon) and notes the degenerate recoverable case; the exact boundary is new territory, not a defect in the present claims.

VERDICT: CONVERGED
