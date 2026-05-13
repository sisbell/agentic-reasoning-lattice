# Review of ASN-0053

## REVISE

(none)

## OUT_OF_SCOPE

(none — Open Questions and the Scope block already identify the genuinely-deferred topics, e.g. span-set difference bounds, allocation-driven re-normalization, cross-level operations.)

The proofs hold up under scrutiny:

- **S0 (Convexity)**: One-step transitivity on T1's total order; correct.
- **SC (Classification)**: Exhaustiveness traced via WLOG on starts then trichotomy on reaches — every ordering of the four boundary points lands in exactly one of (i)–(v).
- **S1, S3 (Intersection / Merge)**: Constructed γ verifies T12 (positivity at divergence k via NAT-sub strict positivity; action point = k ≤ #s). D1 round-trip preconditions discharged. Reverse direction in S3 case 2 correctly forces r = reach(β) from t ≥ reach(α) ∧ t < r.
- **S4, S5, S4a, S3b**: TA-assoc's four preconditions discharged before TA-LC fires (Pos(d), Pos(d'), k_d ≤ #s, k_{d'} ≤ #d = #s). S3b Case B reduces to Case A via S3a, with the swapped construction explicitly traced. Worked example numerics check at every step.
- **S8, S9 (Normalization)**: Loop invariant J carries through both branches with disjointness of emitted/current intervals preserved. S9's case analysis covers both-exist (1a/2a/2b/3a) and one-shorter (1b/3b); minimality of i forces i = n+1 in 1b, making "range j ≥ i vacuous" correct. Cases 2a/2b/3a are derived in full rather than handed-off as symmetric.
- **S11, S11a–d**: SC table is complete — five SC cases plus the SC(iv) directional split give six rows; the reverse-containment row's derivation of ⟦α⟧ ⊆ ⟦β⟧ is shown inline. Tightness of 2 in S11 uses S0 to force a contradiction at any t ∈ ⟦β⟧ (non-empty by S2).

Worked examples computed independently match the ASN's numbers: S1 ([1,5],[0,2]); S3 ([1,3],[0,8]); S4 partition + S5 width composition to [0,…,0,8]; S8 normalization to ⟨([1,3],[0,6]),([1,10],[0,3])⟩; S11 two-span difference; S11c case 1 γ=([1,3],[0,3]); S11c case 2 γ'=([1,10],[0,4]).

Foundation references (D0/D1/D2, TA-LC, TA-strict, TA0, TA-assoc, T1, T3, T12, TumblerSub) are cited with preconditions discharged at each use site.

VERDICT: CONVERGED
