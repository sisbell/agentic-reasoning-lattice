# Review of ASN-0086

## REVISE

(none)

## OUT_OF_SCOPE

The ASN already enumerates appropriate forward-looking items in its Open Questions section (cross-document arrangement invariants, multi-arity link projections, retraction-of-retraction semantics, Observe ordering, atomicity model, cardinality bounds on `nullified`, L1b tightening, substrate-level retraction discipline, type creation coordination). No additional out-of-scope topics to flag.

VERDICT: CONVERGED

The ASN withstands close scrutiny. Key strengths verified:

- **R0** discharges both first-emission and subsequent-emission branches with the three-part freshness argument (same-home/cross-home/content); L-invariant preservation enumerated invariant-by-invariant.
- **R0a** carries forward and reverse directions for cross-home (Case 1), and same-home (Case 2) via ChainMembershipForOrigin. R0a-Cor1 correctly re-expresses ChainMembershipForOrigin with the J_d^Σ ∈ ℤ_{≥-1} convention absorbing the empty case. R0a-Cor2 tightens `#E ≥ 2` to `#E = 2` rigorously via zero-position stability.
- **R5/R5-Cor** decomposition is logically sound (R5-Cor doesn't depend on R5, despite the forward reference in prose).
- **R6c-Corollary** uses a strengthened three-conjunct IH that correctly threads through both `→`-steps (R3+R6a) and arrangement-modifying steps (LinkStoreInvarianceUnderArrangement).
- **R7a** discharges preconditions (1)–(4) for both K.σ-prefix and K.λ-emission step types; the per-step substrate-invariant discharge block covers catalog (a) and (b) systematically; the strict-strengthening argument for catalog (b) via the `a* = [d.0.s_L.1.1]` counterexample is convincing.
- **WP analysis** correctly partitions into regimes (i)/(ii)/(iii) and verifies the relational-layer simplification.
- **Worked Sketch** verifies first-emission, retraction, restoration, and retraction-of-retractor through concrete tumbler arithmetic; R6b's non-fixpoint semantics exhibited explicitly with both audit/active views computed at each Σ_n.

Cross-ASN citations are all to foundation ASNs (ASN-0034, ASN-0036, ASN-0040, ASN-0043, ASN-0093). No hand-waves, no missing edge cases, no unverified case-splits detected.
