# Review of ASN-0068

I worked through the CV-MAX existence and uniqueness proofs, the CV-IN action-point capture argument, CV-PRED, CV-SPAN-VIEW, and all four worked examples in detail. The mathematical content is unusually solid: the V-position-capture argument justifying `actionPoint(width(σ)) = m_σ` is rigorous, the lockstep-offset reduction in CV-MAX uniqueness is correct, the examples all verify against the definitions, and the foundation citations (S7, CL-OWN, CL-UNIQ, TS2, OrdinalShift, T5-implicit, D-SEQ★) are used faithfully. I found one genuine gap.

## REVISE

### Issue 1: CV-MAX proves run uniqueness but not offset uniqueness

**ASN-0068, CV-MAX statement and proof**: The claim states "there exists exactly one triple `(v'_a, v'_b, n) ∈ MaxRuns` **and exactly one offset `k`** with `0 ≤ k < n` such that `v_a = v'_a + k` and `v_b = v'_b + k`."

**Problem**: The Uniqueness proof establishes that the *triple* is unique (`R¹ = R²`, via the δ=0 and δ>0 case analysis). It never closes the second conjunct of the claim — that the offset `k` within the unique run is unique. In Case δ=0 the proof concludes `n¹ = n²` and `R¹ = R²` but stops there; the offsets `k¹, k²` are never shown equal. The "exactly one offset" half of the stated theorem is therefore asserted but not derived.

**Required**: Add the one-line closure: given the unique run `R = (v'_a, v'_b, n)`, if `v_a = v'_a + k = v'_a + k'`, then by OrdinalShift's last-component formula (`(v'_a + k)_{m_a} = (v'_a)_{m_a} + k`) and T3, `k = k'`. This uses exactly the reduction already deployed in the "Lockstep offset" step and discharges the remaining conjunct.

## OUT_OF_SCOPE

None. The ASN correctly defers INSERT/DELETE/COPY/REARRANGE mechanics, link semantics, and replication to its Open Questions and Scope boundary; the link-subspace corollaries (CV-LINK-DEGEN, CV-LINK-SELF) characterize `compareversions` itself rather than link operations, so they are in scope.

VERDICT: REVISE
