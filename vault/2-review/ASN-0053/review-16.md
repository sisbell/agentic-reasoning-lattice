# Rebase Review of ASN-0053

## REVISE

(none)

**D0 citations**: All references to D0 correctly cite ASN-0034, accurately restate the precondition (`a < b`, `divergence(a,b) ≤ #a`), and correctly characterize what D0 ensures (well-defined positive displacement, TA0 satisfied for the round-trip application). The prefix-case explanation (`divergence = #a + 1 > #a`) is consistent with the foundation's Divergence definition case (ii).

**D1 citations**: All references to D1 correctly cite ASN-0034 with the full precondition triple (`a < b`, `divergence(a,b) ≤ #a`, `#a ≤ #b`). Every proof that invokes D1 (S1, S3, S4, S5, S8, S11) verifies the preconditions through level-uniformity and level-compatibility, which ensure equal-length tumblers — giving type (i) divergence with `k ≤ #a` and `#a = #b`.

**Downstream references**: No proof relied on intermediate steps within the old local derivations. All uses treat D0 and D1 as black-box results. The explanatory prose in "The reach function" section motivates the displacement formula but does not re-prove it — it describes TumblerSub's structure and then cites D0/D1 for the formal guarantees.

**Registry**: D0 marked `cited` with label `DisplacementWellDefined, ASN-0034` — matches foundation. D1 marked `cited` with label `DisplacementRoundTrip, ASN-0034` — matches foundation. D2 marked `cited` with label `D2, ASN-0034` — consistent (D2 depends on D1 via the foundation's corollary chain).

**Prose coherence**: The reach function section flows naturally: definition of reach → need for displacement recovery → citation of D0/D1 → boundary analysis (#a > #b failure, prefix case). No orphaned text or dangling references from removed derivations.

VERDICT: CONVERGED
