# Review of ASN-0091

## REVISE

### Issue 1: Circular derivation of RA-dom and K.μ~ admissibility clause (iii) for REARRANGE_K

**ASN-0091, "K.μ~ Admissibility Clauses" + "Forward Direction" subsections**:

- The RA-dom bullet states: "RA-dom ← ASN-0047's K.μ~-FIX (DomainFixity). dom(Σ'.M(d)) = dom(Σ.M(d)) follows from π's bijectivity together with ASN-0047's D-SEQ★ at both endpoints."
- The forward-direction clause (iii) states: "By CS4, every cut cᵢ has #cᵢ = 2, and by RE-subpres ... RA-dom (dom(Σ'.M(d)) = dom(Σ.M(d)), **supplied via K.μ~-FIX**) holds the per-subspace V-position set V_S(d) fixed across the transition, so the common depth m_S is preserved ... #π(v) = m_S = #v."

**Problem**: This is a dependency cycle. ASN-0047's K.μ~-FIX derives `dom(M'(d)) = dom(M(d))` using K.μ~ **admissibility clause (iii)** (length preservation) together with D-SEQ★. ASN-0091's clause (iii) discharge in turn derives `#π(v) = #v` by routing through **RA-dom**, which it sources from K.μ~-FIX. So clause (iii) ← RA-dom ← K.μ~-FIX ← clause (iii). The same RA-dom dependency propagates into the clause (i) shape-package discharges (S8a, S8-depth, D-CTG★, D-MIN★ are each discharged "via RA-dom" in the per-invariant subsections), so the entire admissibility chain for naming K.μ~ the realiser rests on the cycle.

A clean, non-circular anchor exists but is not used:
- **RA-dom** is stated *directly* as a postcondition of REARRANGE_K — ASN-0084's PivotPostcondition and SwapPostcondition both assert "The domain is dom(M'(d)) = dom(M(d))." This requires nothing from clause (iii).
- **Clause (iii)** follows directly from the construction: by CS4 (and R-PRE forcing the affected range to depth-2 positions) every affected V-position has `#v = 2`, and R-PPERM/R-SPERM compute `π(v)` as an ordinal shift of `c₀` (depth-2), which preserves length by ASN-0034's OrdinalShift/TS3 — so `#π(v) = #v = 2` with no appeal to RA-dom or RE-subpres. Exterior/non-S positions are fixed (`π(v) = v`), trivially length-preserving.

**Required**: Source RA-dom for REARRANGE_K from ASN-0084's PivotPostcondition/SwapPostcondition domain clause (not K.μ~-FIX), and discharge clause (iii) directly from CS4 + ordinal-shift length preservation. This breaks the cycle and removes the entanglement between RA-dom and the per-subspace invariant discharges (S8-depth, D-SEQ★).

## OUT_OF_SCOPE

(none — the link-subspace-rearrangement semantics, the cardinality-increase bound, observational equivalence, and cut-sequence realizability of arbitrary bijections are already correctly parked in Open Questions.)

VERDICT: REVISE
