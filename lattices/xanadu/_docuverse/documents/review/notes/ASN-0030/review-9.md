# Review of ASN-0030

Based on Alloy modeling-1

## SKIP

### Confirmatory counterexamples (expected SAT on negated properties)

Three checks produced counterexamples. All three are confirmations of ASN claims, not spec issues — the Alloy models assert the *positive* (monotone) form and find counterexamples, which is exactly what the ASN predicts.

**A1 — ReachabilityNonMonotone.** The model asserts `ReachabilityMonotone` (the positive form) and gets SAT — a counterexample to monotonicity. This confirms the ASN's claim that reachability is non-monotone. Non-vacuity run is SAT, so the scenario is genuine. Expected result.

**A4a pre — RearrangePre.** Three checks: `PreGuaranteesDocMembership` is UNSAT (precondition works — no counterexample); `NoPre_DocMayNotBeInD` is SAT (without the precondition, d may not be in D). The SAT result validates that the precondition is necessary, not that the spec is wrong. `FindRearrange` is SAT confirming non-vacuity. Expected result.

**A7b — EndsetResolvability.** The model asserts that resolvability is preserved by Delete and gets SAT — a counterexample. This confirms the ASN's claim that `resolvable(L, d)` is non-monotone: DELETE can remove V-space mappings that made a link's endpoints reachable. Non-vacuity run is SAT. Expected result.

### Passed properties (19)

A0, A2, A3, A4 pre, A4(b), A4(c), A4(e), A4a(b), A4a(c), A5 pre, A5(a), A5(c), A5(e), A5(f), A6, A7, A7a, resolvable, A8 — all UNSAT within bounded scope. No counterexamples found.

VERDICT: CONVERGED
