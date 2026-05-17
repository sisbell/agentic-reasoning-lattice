# Channel Assignment — ASN-0086 review-12

**Date:** 2026-05-16 20:13

## Issue 1: Sloppy `℘(A)` notation in R6a's proof
Reason: Pure notation fix. ASN-0043's coverage codomain is `℘(T)`, already cited in the note; the substitution is mechanical and requires no design-intent or implementation evidence.

## Issue 2: R0a's introductory paragraph reference is cross-cutting
Reason: Restructuring of exposition. The proof's three layers are all internal to R0a; no external channels needed to reorder the motivational paragraph.

## Issue 3: R5's consequence (d) treats provenance as substrate-derivable when it requires convention
Reason: The note's own R5(c) ("Agent provenance") already establishes the convention — emitter address goes in the from-set. Distinguishing substrate-derivable from convention-derivable predicates is internal to the ASN's existing content.

## Issue 4: Worked Sketch concrete instantiation does not verify Step 1's R5 instantiation against L-invariants
Reason: All L-invariants are enumerated in R0 Step 4 and the concrete tumbler `b₁ = 1.0.1.0.1.0.2.2` is given; verification is mechanical substitution of values into already-stated invariant predicates.

## Issue 5: The single-tuple-scope argument in Nullify's Definition restricts to `A_rel^{Σ'}` but the unrestricted coverage is wider
Reason: The justification uses the subspace-distinctness axiom (already stated at the head of the note) and L0; both are internal to the ASN. The fix is a one-sentence appeal to existing machinery.

## Issue 6: R6c's broader-scope extension argument relies on an unstated invariance of `L_R`/`nullified`/`A_K` under arrangement modifications
Reason: The dependency chain (`L_R`, `nullified`, `A_K` are functions of `Σ.L`; arrangement modifications preserve `Σ.L`) is derivable from the ASN's own definitions and the cited ASN-0036 frame conditions. No external channels needed.
