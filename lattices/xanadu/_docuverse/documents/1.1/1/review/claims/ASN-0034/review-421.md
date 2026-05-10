# Regional Review — ASN-0034/Span (cycle 1)

*2026-04-23 02:41*

### T3 cited but not defined in the ASN
**Class**: REVISE
**Foundation**: (none — foundation ASN)
**ASN**: TumblerAdd proof: "the equality branch discharges `r = w` via T3"; TumblerAdd postconditions: "a ⊕ w ≥ w (T1, T3)"; TumblerAdd Depends: "T3 (CanonicalRepresentation) — equality sub-case of dominance concludes `r = w` from component-wise agreement and equal length"; T1 proof preamble: "The argument relies on `<` on ℕ (NAT-order) and on T3 (CanonicalRepresentation): tumblers with the same length and identical components at every position are equal"; T1 proof Cases 1–3 repeatedly invoke T3; T1 Depends: "T3 (CanonicalRepresentation) — bridge between component-level agreement and tumbler equality".
**Issue**: T3 (CanonicalRepresentation) is cited as a load-bearing claim in both TumblerAdd's dominance proof (equality sub-case) and T1's trichotomy proof (all three cases), and listed in both Depends blocks without any "this ASN" / foundation / external qualifier. But no T3 claim is stated in the ASN content; Foundation Statements is empty and Declared depends is empty, so T3 is neither in-ASN nor an imported foundation. Every invocation of "r = w by T3" / "a = b by T3" / "a ≠ b by T3" therefore hangs on an unstated principle. While sequence extensionality is a defensible interpretation, the ASN repeatedly labels it as a citable claim (T3, "CanonicalRepresentation"), which is a promise of an explicit statement somewhere, not an informal appeal to sequence semantics.
**What needs resolving**: Either state T3 explicitly as a claim in this ASN (with its own Formal Contract — what the predicate is, what it depends on, what it concludes) so that the "by T3" invocations resolve, or replace every "by T3" with a direct appeal to T0's definition of T as sequences and adjust the Depends lists accordingly.

### TumblerAdd presented before T1 despite depending on it
**Class**: OBSERVE
**Foundation**: (none)
**ASN**: TumblerAdd sits under "## Tumbler arithmetic"; T1 under "## The total order" appears later. TumblerAdd's postconditions are stated "a ⊕ w > a (T1), a ⊕ w ≥ w (T1, T3)", and its proof invokes "T1 case (i) at divergence position `k` yields `a ⊕ w > a`" and "T1's `≥` abbreviation `a ≥ b ≡ b < a ∨ b = a`".
**Issue**: The presentation order is motivational (arithmetic before order), but the logical dependency order is the reverse: TumblerAdd's two non-trivial postconditions (`> a`, `≥ w`) cannot be discharged without T1 in scope, and every "by T1 case (i)" invocation in the proof is a forward reference. T1 itself does not depend on TumblerAdd, so there is no circularity — only a presentation that forces the reader to read forward to verify each cited step.

VERDICT: REVISE
