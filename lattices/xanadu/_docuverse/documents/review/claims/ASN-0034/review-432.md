# Regional Review — ASN-0034/TA-assoc (cycle 2)

*2026-04-23 04:10*

I read the ASN carefully alongside the previous findings. The previous findings correctly capture the missing foundations (T1, NAT-sub, NAT-cancel, NAT-wellorder, NAT-discrete) and the TA-Pos notation note. I worked through TumblerAdd's strict-advancement and dominance cases (including the `k = 1` edge case, the three-way case split of the dominance sub-cases), ActionPoint's uniqueness argument, T3's extensional equality, and all three cases of TA-assoc's proof (checking domain subsumption, the `Pos(s)` witness construction in each sub-case, and component-wise agreement at action points).

Case coverage and index-domain bounds in TA-assoc all discharge correctly given the stated preconditions (`Pos(b)`, `Pos(c)`, `k_b ≤ #a`, `k_c ≤ #b`). The precondition set is the correct intersection of the two sides' domains, and the `min(k_b, k_c) ≤ #a` subsumption for the right side follows by trichotomy as stated. The dominance sub-case `a_k = 0` collapses to T3-equality correctly, and the `a_k > 0` sub-case's use of NAT-cancel to rule out `a_k + w_k = w_k` is exact.

I found no new issues beyond what Previous Findings already capture.

VERDICT: REVISE

## Result

Regional review not converged after 2 cycles.

*Elapsed: 863s*
