# Channel Assignment — ASN-0134 review-50

**Date:** 2026-06-14 17:42

## Issue 1: The K.σ realization conditional is restated repeatedly after declaring it stated "once"
Reason: The conditional and its two realization families (shared-frontier ⟹ obligation, collision-free ⟹ vacuous) are already fully stated in §4/H3; the fix is pure deduplication — collapsing the downstream re-derivations to label-citations — needing nothing the ASN does not already record.

## Issue 2: Clause 4 re-imports clause 1's content, and the minimality argument does not distinguish their counterexamples
Reason: Clause 4's genuinely independent content — a compound single read (`Observe_K`'s `L_K ∖ nullified` per W5, or `age`'s frontier descent per V0) straddling a commit *despite* atomic transitions — is a model-internal hypothetical constructible from A3, W5, and V0 already present; the fix is exposition (drop clause 1's content, rephrase the counterexample).

## Issue 3: G0's serializability/SC/linearizability exposition is duplicated and longer than the result needs
Reason: The serializability / not-SC-under-pipelining / logical-not-temporal / linearizability-under-sequential-clients content is already present and correct; the fix is trimming duplicated (table vs in-text) and textbook prose, an internal editing pass.

## Issue 4: Motivational design-intent restatements occupy structural slots after technical claims
Reason: The two flagged sentences merely restate design intent already cited and load-bearing in H1/H2 ("owned numbers") and G1 (distributed intent); deleting redundant flourishes while keeping the cited Gregory evidence needs no consultation.

## Issue 5: Numbering gap in the W-series claims
Reason: Pure renumbering or reservation note; no design intent or implementation evidence involved.
