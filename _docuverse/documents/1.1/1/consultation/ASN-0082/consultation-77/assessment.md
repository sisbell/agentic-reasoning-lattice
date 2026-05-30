# Channel Assignment — ASN-0082 review-77

**Date:** 2026-05-30 14:25

## Issue 1: D-SEP(a) cites the wrong clause of OrdinalExceedsDisplacement
Reason: The fix is internal — OrdinalExceedsDisplacement's clauses (i) and (iii) are both present in the ASN, and the correction is simply to re-point the citation from (i) to (iii) at v = r. No design intent or implementation evidence is needed.

## Issue 2: Defensive "independently of the order relation" prose in OrdinalExceedsDisplacement (ii)
Reason: The fix is internal — it removes hedge prose while preserving the load-bearing facts (`#v = 2 = #r` licensing OrdinalOrderEquivalence), all of which are already stated in the surrounding derivation. Purely editorial.

## Issue 3: Scoping-axiom prose explains *why the axiom is needed* rather than what it constrains
Reason: The fix is internal — trimming the rationale clause from the axiom statement and (optionally) relocating it to scope/motivation prose requires only the ASN's own text. The dependence on text-scoped foundation invariants is already documented elsewhere in the contract.
