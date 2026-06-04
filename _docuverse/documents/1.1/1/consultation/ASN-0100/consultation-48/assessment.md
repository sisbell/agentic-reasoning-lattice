# Channel Assignment — ASN-0100 review-48

**Date:** 2026-06-04 14:59

## Issue 1: Defensive not-used-lemma inventory
Reason: Pure editorial trim of defensive meta-prose; the re-derivations already in §Verifying the Invariants carry all the reasoning, so the fix is internal to the ASN.

## Issue 2: INS.M-exhaustive argument stated twice in full
Reason: Consolidating a duplicated argument into one section with a cross-reference is an internal restructuring; both copies are already present and identical in content.

## Issue 3: Implementation-latitude essay in §Atomicity
Reason: The guarantee to keep (three forced orderings determine the boundary; all other interleavings reach the same Σ') is already stated and proven in the ASN; condensing the per-pair commutativity walkthrough is internal.

## Issue 4: Notation duplication — shift vs. OrdinalShiftBase `+`
Reason: Stating the `shift(·, 0) := t` convention once and removing repeated bridging parentheticals is a purely notational cleanup derivable from the ASN's own conventions.
