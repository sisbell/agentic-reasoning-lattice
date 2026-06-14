# Channel Assignment — ASN-0134 review-7

**Date:** 2026-06-13 20:28

## Issue 1: A6's "single-state" package includes cross-state stability invariants P2/R2
Reason: The fix applies the ASN's *own* single-state-vs-relational criterion consistently — P2/R2 quantify over reachable states (cross-state form), and the registry's fixity-at-construction is already established internally (W6, R1). The logical forms of P1/P2/R1/R2 are already cited from the dependency ASNs; the repair is an internal reclassification (per-state predicate `Σ_k.record = R₀` vs. cross-state corollaries P2/R2), needing no design intent or implementation evidence.

## Issue 2: H1/W1 disjointness proof omits the cross-document, cross-subspace case
Reason: Case (c) is a structural fact about the tumbler address format the ASN already exhibits in §7 — anchors `[d.0.S…]` and `[d'.0.S'…]` diverge at the document component for `d≠d'`, hence are prefix-incomparable regardless of `S, S'`. Completing the case analysis draws only on the ASN's own address structure and its cited ASN-0093 lemmas.

## Issue 3: M1(b)(ii) overstates de-duplication, contradicting I2
Reason: The fix aligns M1(b)(ii) with ASN-0128's already-cited de-dup semantics — I2 (de-dup consults `A_K`, so a nullified incumbent resurrects via a miss) and I1a (`A_K` holds ≤1 tuple per coverage class) — facts the ASN itself partly invokes (§4 carries the "lands active" hedge). It is an internal consistency repair requiring no design intent or implementation evidence.
