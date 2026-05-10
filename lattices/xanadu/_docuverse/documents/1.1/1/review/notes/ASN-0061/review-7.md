# Rebase Review of ASN-0061

## REVISE

(none)

The rebase of D0 and D1 is clean. ASN-0061 does not use displacement-between-two-positions (D0/D1) at all — it performs width-subtraction-from-position, which is a different operation requiring different foundation properties. The document correctly cites:

- **TA2** (SubtractionWellDefined) for `ord(v) ⊖ w_ord` in D-SHIFT — the right tool when the precondition is `a ≥ w`, not `a < b` with divergence constraints.
- **TA4** (PartialInverse) for the round-trip `(ord(p) ⊕ w_ord) ⊖ w_ord = ord(p)` in D-SEP — the right tool for `(a ⊕ w) ⊖ w = a`, vs. D1's `a ⊕ (b ⊖ a) = b`.
- **TA3-strict** (OrderPreservationSubtractionStrict) for order-preserving subtraction in D-BJ.

All preconditions for these citations are explicitly verified in context. No dangling references to D0 or D1 exist anywhere in the body. The properties table correctly omits D0/D1 (not used). The block-decomposition split points (D-BLK cases b, d, f) are justified via natural-number arithmetic at ordinal depth 1 plus M4, not via displacement theory. Prose flows naturally with no orphaned text from removed derivations.

VERDICT: CONVERGED
