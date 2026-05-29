# Channel Assignment — ASN-0045 review-20

**Date:** 2026-05-28 20:14

## Issue 1: T4c treated inconsistently across the four predicates
Reason: Internal. Account's rename-equivalence derivation already shows the discharge pattern (T4c preconditions via T4b + T3, all in ASN-0034), and the same machinery applies symmetrically to node/document/element. The choice between providing all four correspondences or declaring them uninterpreted is resolved by the ASN's own framing as the hierarchy levels — no external evidence or design intent needed.

## Issue 2: Partition lists T4c as a dependency the proof does not use
Reason: Internal. The ASN's own Well-Definedness paragraphs (at-least-one explicitly avoids T4c as circular; at-most-one states T4c's injectivity "does no work") directly contradict the dependency listing. The fix is a self-consistency correction derivable from the ASN alone.

## Issue 3: Behavior on T4-invalid tumblers shown by example but never stated as a postcondition
Reason: Internal. The complement postcondition follows mechanically from the shared left conjunct `T4-valid(t)` in all four definitions — already present in the ASN. The counter-example table demonstrates exactly this; promoting it to a stated, derived postcondition requires no external channel.
