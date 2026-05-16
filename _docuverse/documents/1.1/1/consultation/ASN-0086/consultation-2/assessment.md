# Channel Assignment — ASN-0086 review-2

**Date:** 2026-05-16 14:28

## Issue 1: T10a sub-lemma misattribution in R0
Reason: T10a's actual sub-lemmas are stated in ASN-0034; the fix is reconstructing R0's freshness argument against the foundation as written. No design intent or implementation evidence is required — the lattice already contains the properties needed.

## Issue 2: Undefined notation `s_L(d)`
Reason: L0 (ASN-0043) defines `s_L` as a constant subspace identifier; the fix is either an internal definition `s_L(d) := {a : home(a) = d ∧ subspace_I(a) = s_L}` or a rewrite using `s_L` and document prefix directly. Fully derivable.

## Issue 3: R4 proof — `s_C ≠ s_L` not established
Reason: The convention fixing distinct subspaces is set in ASN-0036's D-CTG (text=1, link=2); alternatively R4 can derive from L14 + Setup directly. Both routes are within the existing lattice.

## Issue 4: L-property misattributions in R5's Stage 2 check
Reason: The fix is a mechanical re-enumeration against ASN-0043's actual L-property list (including L0a, L11a, L14a). Pure citation correction; no external consultation needed.

## Issue 5: R0's invariant verification hand-waved
Reason: Each L1a/L1b/L1c clause's witness can be exhibited from ASN-0043's definitions and ASN-0034's T10a chain structure. The argument is mechanical assembly of existing lattice properties.

## Issue 6: Worked Sketch repeats Issue 1's misattributions
Reason: Same fix path as Issue 1 — reformulate against the actual T10a properties or weaken to an existence claim. Internal.

## Issue 7: R0's countable-infinity argument is loose
Reason: T0(a), T0(b), and the L1b depth constraint are all in the lattice; the fix is to assemble the proper argument from existing properties. No external evidence required.

## Issue 8: T7 misapplied in R4
Reason: T3 (CanonicalRepresentation) is the right tool, and is already in ASN-0034. Pure correction within the lattice.

## Issue 9: R5's L11b citation overreaches
Reason: Either construct the invariant-preserving witness explicitly using ASN-0043's L-invariants, or weaken the claim. The L4(c) + L13 + L-invariant orthogonality argument is fully internal.

## Issue 10: Active subset / Nullify on multi-arity links
Reason: R6 and Nullify are the substrate's own contribution (acknowledged in the ASN); the precondition tightening or A_K extension is an architectural decision for the substrate authors, derivable from coherence with existing definitions. Not Nelson's design intent (R6 is post-Nelson) and not relevant to udanax-green.

## Issue 11: Observe pattern semantics underspecified
Reason: Observe is part of the substrate's own primitive set; the match-relation choice is an internal design decision that should be stated explicitly with rationale, not inherited from Nelson's design (which does not specify Observe) or udanax-green's query layer.

## Issue 12: State transition relation left implicit
Reason: The transition relation is a foundational substrate decision; ASN-0043/0036 already leave it abstract, and R0's construction can be discharged either by axiomatizing invariant-preserving extension as reachability or by enumerating the relevant primitives. Internal architectural choice.
