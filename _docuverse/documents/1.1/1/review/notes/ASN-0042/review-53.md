# Review of ASN-0042

I have read this ASN carefully, examined each proof, checked the worked example against the claims, and stress-tested the structural arguments for boundary cases (empty namespace forks, account vs. node-level principals, multi-step delegation chains, length-equal sub-delegates, Form A/B classification under both `zeros(pfx(π)) = 0` and `zeros(pfx(π)) = 1`).

## REVISE

(none)

The proofs in this ASN are unusually thorough. Several spots I expected to find hand-waves were instead expanded:

- O10's non-coverage analysis correctly partitions sub-delegates into Form A and Form B, eliminates Form B in the `zeros(pfx(π)) = 1` case via O1a's saturation, and uses PrefixBaptismCoupling + B1 (of ASN-0040) to bound length-(`#pfx(π)+2`) Form B prefixes below `hwm_0`. The length-only exclusion of longer Form B sub-delegates is also explicit.
- O8's multi-step persistence argument explicitly handles the trajectory routing through `Σ_d^post` rather than assuming determinism, citing O15 + condition (iii) + O12 to force the delegation event onto the witnessing path.
- The Delegation section explicitly proves preservation of O1a (via (iv)), T4 (via (v)), and O1b (via the length-contradiction chain through condition (ii) and (i)).
- O3's "no ties" argument is derived from O1b plus the Prefix definition, not asserted.
- B0 of ASN-0040 (registry monotonicity) and T8 of ASN-0034 (allocator-domain monotonicity) are repeatedly disambiguated where either could plausibly be invoked.
- AccountField is proved well-formed by exhaustive case analysis on `zeros(a) ∈ {0, 1, 2, 3}`.
- O14 includes seven distinct base-case clauses, each justified as anchoring a downstream inductive argument; the seventh clause (`pfx(π) ∈ Σ₀.B`) is load-bearing for PrefixBaptismCoupling and is properly cited.
- The Worked Example concretely verifies O0–O10 against named addresses, including a structurally-forced demonstration of the `hwm_0 = 0` field-opening branch via π_B's virgin granfilade, and a three-state trace of O8 (Σ_1, Σ_2, Σ_3).
- All cross-ASN citations are to ASN-0034 and ASN-0040 (foundation), with B0/B0★/B1/B6/B10 of ASN-0040 and T0(b)/T3/T4/T4a/T4b/T4c/T5/T8/T10a/TA5/TA5(d)/Prefix of ASN-0034 used appropriately.

## OUT_OF_SCOPE

(none beyond what the ASN's Scope section and Open Questions already enumerate — ownership transfer mechanism, cross-node federation, content-accessibility-on-orphan, delegation history reconstructibility, domain density, and overlapping-prefix enforcement are all properly deferred)

VERDICT: CONVERGED
