# Channel Assignment — ASN-0036 review-196

**Date:** 2026-05-29 23:53

## Issue 1: S8a notation bookkeeping enumerates citation behavior
Reason: Purely editorial — collapsing citation-bookkeeping prose and keeping the T0 equivalence inline. The equivalence is already stated in the ASN; no design intent or implementation evidence is required.

## Issue 2: ValidFirstInsertionPosition Depends imagines an excluded future state
Reason: Internal cleanup — removing a defensive parenthetical about a non-dependency. The predicate's preconditions and D-MIN's antecedent are already in the ASN; the fix is mechanical relocation.

## Issue 3: S8 chain lemma asserted, not shown
Reason: The missing step is a self-contained combinatorial argument (degree bounds + finiteness + acyclicity ⟹ disjoint maximal paths); all the facts it consumes (`succ` injective, acyclic, finite) are already established in the proof. No external channel needed.
