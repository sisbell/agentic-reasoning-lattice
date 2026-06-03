# Channel Assignment — ASN-0069 review-81

**Date:** 2026-06-03 00:49

## Issue 1: V8a introduces a third notation for the sibling/version stream that is never reconciled with V10's sibling notation
Reason: Purely a notational reconciliation between two notations the ASN already defines (`wⁱ` and `d_new^i`); the worked example already confirms the identity (`d_new² = inc(d_new, 0) = w²`). No design intent or implementation evidence is needed.

## Issue 2: The V8 paragraph previews a weaker second-version result that it then abandons
Reason: An editorial deletion of preview-then-abandon prose; the `k=2` sketch is subsumed by V8a, which is already present in the ASN. Fully internal.

## Issue 3: V7's property inventory is a defensive use-site enumeration redundant with the worked example
Reason: An editorial pruning of a redundant property list whose content is already discharged by the worked example and the one-sentence organizing principle, both present in the ASN. Fully internal.
