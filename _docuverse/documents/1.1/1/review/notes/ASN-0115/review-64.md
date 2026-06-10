# Review of ASN-0115

I worked through the Confinement lemma, the `act` definition and its override, and every one of R1–R11 (including the R6 bindable-slice gap argument, the R7 active-set agreement proof, the R8 subspace/link-vacuity dispatch, and the R11 weakest-precondition decomposition). The ASN is unusually careful: edge cases are covered (empty spec-set, empty/unallocated subspace, unit-width, frontier overrun, orphaned content, shallow/deep depth mismatch, start in an unused subspace), the claims have real derivations rather than checkmarks, the wp in R11 is genuinely non-trivial, and each major postcondition is checked against a concrete worked instance. The implementation references are used as realizability evidence with explicit "an alternative implementation would still owe…" framing, so the ASN stays at the specification level (no META).

I found one skipped step.

## REVISE

### Issue 1: The deep-case emptiness assertion cites two tools but needs a third

**ASN-0115, §"What a spec-set is" (justification of the `act` override)**: "The override changes nothing in the deep case `#s > m_S(d)`, where Confinement and S8-depth already force `dom(Σ.M(d)) ∩ ⟦σ⟧ = ∅`."

**Problem**: This is an emptiness claim of the form "follows from Confinement + S8-depth," but those two tools alone do not close it. Take any `v ∈ dom(Σ.M(d)) ∩ ⟦σ⟧` with `#s = m > m_S(d)`. Confinement gives `subspace(v) = S`, so `v ∈ V_S(d)`; S8-depth then gives `#v = m_S(d) < m`. At this point the cited tools have only established `#v = m_S(d) < m` — they have *not* yet produced a contradiction. In particular they do not rule out the boundary value `m_S(d) = m − 1`, where `v` would be a depth-`(m−1)` position agreeing with `s` on positions `1 … m−1`. What actually closes the argument is the next step, which is *not* cited: since `#v ≤ m−1`, `v` agrees with `s` on all of its `#v` positions and `#v < #s`, so `v` is a proper prefix of `s`, whence `v < s` by T1 case (ii) — contradicting `v ≥ s`, which `v ∈ ⟦σ⟧` supplies via the denotation lower bound. The remark thus asserts a derivation while naming only two of the three ingredients (the prefix-ordering step from T1, and the `v ≥ s` lower bound, are silent).

This is a non-load-bearing side remark — `act` is *defined* to force empty in the override branch regardless, so no R-claim depends on it. But the remark's whole purpose is to reassure the reader that the override discards nothing legitimately cited in the deep case; for that reassurance to hold, the emptiness must be properly grounded, and as written a careful reader hits exactly the "what rules out a depth-`(m−1)` bound position?" question with no cited answer.

**Required**: Either name the closing step — "for `v ∈ dom(Σ.M(d)) ∩ ⟦σ⟧`, Confinement and S8-depth give `#v = m_S(d) < m`, so `v` is a proper prefix of `s`, hence `v < s` (T1 case (ii)), contradicting `v ≥ s`" — or soften the assertion to "the override is vacuous here because the geometric intersection is independently empty," dropping the claim that the two named tools alone force it.

## OUT_OF_SCOPE

None. The ASN defines no claims for the listed out-of-scope operations; it delivers only link *references* (R10) and explicitly defers endset-structure reading to READLINK/FOLLOWLINK. The Open Questions (inline provenance, outright failure, dangling references under relaxed S3★, channel faithfulness, boundary-straddling spans) are correctly held for future ASNs rather than answered here.

VERDICT: REVISE
