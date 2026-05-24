# Channel Assignment — ASN-0094 review-43

**Date:** 2026-05-23 22:20

## Issue 1: AllocatedAddressAntichain Sub-case 3b discharged "by symmetry"
Reason: The fix is internal — Sub-case 3a is already written out explicitly, and the worked example already exhibits the swap concretely; promoting the swap into the formal proof body requires no design intent or implementation evidence beyond the ASN's existing content.

## Issue 2: NAT-card and NAT-sub appendix invokes background facts not in the foundation
Reason: The choice between deriving ℕ-commutativity/associativity from existing NAT axioms (via a Peano successor + induction derivation routed locally in the appendix) or adding them as explicit foundation axioms is a formal-derivation decision internal to the framework; neither Nelson's design intent nor Gregory's implementation evidence bears on the axiomatization choice.

## Issue 3: Sh5 body-shape-level uniformity enforced only by hand-review
Reason: The framework already articulates both options (tighten into procedural recipe vs. explicitly demote to aspiration) and the trade-off; the choice is a META-discipline scope decision derivable from the ASN's own commitments without external evidence.

## Issue 4: Document size and prose redundancy impede review
Reason: Purely editorial — consolidating repeated Gate Ordering / per-walkthrough scaffolding / scope-clarification statements into single canonical sites with citations elsewhere requires no design or implementation input.

## Issue 5: Sh5 audit-table extension lacks a procedural commitment
Reason: The choice between committing to a minimal review checklist or downgrading the catalog to "fixed at this draft, extensions require a new ASN" is a META-discipline scope decision parallel to Issue 3, fully derivable from the framework's existing self-description.
