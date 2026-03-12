# Review of ASN-0029

Based on Alloy modeling-1

## SKIP

### Intentional enforcement-necessity models (D5, D11a-c, D15, D16)

D5 (OwnershipRights), D11a/b/c (PublicationSurrender access rights), D15 (OwnerExclusiveModification), and D16 (UnconstrainedRespectsForking) all follow the same deliberate modeling pattern: operations are left unconstrained (any actor may act, access relations are unrestricted), and the assertion checks whether the property holds without enforcement. The counterexamples confirm that enforcement is independently necessary — which is exactly the model's stated purpose. Each model's header documents this intent (e.g., D5: "counterexamples demonstrate each ownership right is independently necessary").

The ASN correctly characterizes these as "design requirements on correct participants, not mechanically enforced invariants." The Alloy models validate that the requirements are non-trivial (they don't hold vacuously from the remaining structure). The companion assertions that bake in the ownership guard (NoSplitOwnership, EnforcedNoSplitModifier, D11d_OrdinaryCannotWithdraw, ForkOwnership/ForkChangesOwnership/OriginalUnchanged/OnlyForkAdded) all pass UNSAT, confirming the properties hold when enforced. No spec change needed.

### D17 BoundaryInclusion — integer overflow artifact

BoundaryInclusion asserts that a value exactly at `sp.start` is found by the query. The counterexample arises from Alloy integer overflow: with `5 Int` (range -16..15), `plus[sp.start, sp.len]` wraps past the ceiling, causing `v < plus[sp.start, sp.len]` to fail when `sp.start` is near 15. The ASN's `s < s ⊕ l` uses tumbler addition (unbounded, non-wrapping), so this is a bounded-model-checker artifact, not a spec issue. A guard like `plus[sp.start, sp.len] > sp.start` would eliminate the spurious counterexample.

### 21 properties passed

AccountAddr, account, D0, D1, D2, D3, D4, D6, D7, D7a, D7b, D8, D9, Sigma.pub, D10, D10-ext, D10a, D12, D13, D14, D14a — all UNSAT within bounded scope. No issues.

VERDICT: CONVERGED
