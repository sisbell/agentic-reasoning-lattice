# Review of ASN-0086

## REVISE

I performed a thorough review of ASN-0086 covering the foundational setup, every R-claim and its proof, the three operations, the WP analysis, and the worked sketch. No genuine issues remain.

The proofs are rigorous and detailed:
- **R0**'s L-invariant preservation block exhaustively covers ASN-0036 / ASN-0043 / ASN-0093 invariants by mechanism (precondition-discharged, established by extension, preserved by Frame, preserved by SC-NEQ, preserved by chain-discipline).
- **R0a** treats both cross-home (via L1 + L1a's NUDE-prefix projection, with explicit forward and reverse direction) and same-home (via ChainMembershipForOrigin + ChainUniformLength + T3) cases.
- **R0a-Cor2** establishes `#E(a) = 2` strictly via R0a-Cor1 + ChainUniformLength + ChainUniformZeroCount + zero-position stability through TA5(c) + TA5-SigValid.
- **R5-Cor** factors out content-uniformity so subsequent Emit_K invocations need not re-verify L-invariants at arbitrary endset shapes.
- **R6a–R6c** treat the audit/active distinction with appropriate quantification-range justification (R6b labelled DEF-Consequence) and lift to `⊑̂` via LinkStoreInvarianceUnderArrangement.
- **R7a** explicitly decomposes any state-affecting `↝`-step into K.σ + K.λ replays, with strict-strengthening (catalog (b) over catalog (a)) demonstrated by the off-chain L1c-admissible witness `a* = [d.0.s_L.1.1]`.

Boundary cases are addressed: first emission (Worked Sketch Step 0), retraction of first link (Step 1), restoration (Step 2), retraction-of-retractor exhibiting R6b's non-fixpoint semantics (Step 3). Tumbler arithmetic in the sketch was spot-checked and verifies. All cross-ASN references are to foundation ASNs only.

The WP analysis covers all three retraction regimes (unit-depth, crafted-span, self-nullifying), with relational-layer discharge demonstrated for regimes (ii) and (iii). The operations' function-ness, frame conditions, and freshness postconditions are explicitly justified via ASN-0093's K.λ contract.

VERDICT: CONVERGED
