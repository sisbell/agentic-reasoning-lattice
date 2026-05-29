# Channel Assignment — ASN-0040 review-45

**Date:** 2026-05-28 20:52

## Issue 1: S0 invokes T10a.7 outside its stated contract
Reason: The fix is a formal proof restructuring — either re-derive S0 from TA5(a) plus T1 transitivity/irreflexivity (a three-line induction the reviewer already sketches) or tighten S0's precondition to B6-valid pairs. Both options draw only on foundation lemmas the ASN already cites; no design-intent or implementation evidence is at issue.

## Issue 2: the sibling-stream length/sig invariant is re-derived five times
Reason: Pure deduplication — hoist the already-proven S(p,d) postcondition into its contract and have downstream proofs cite it. Entirely internal to the ASN's own derivations.

## Issue 3: B10's preservation step over-claims contiguity it does not use
Reason: The fix weakens an over-strong equality (`= c_{m+1}`) to `a ∈ S(p,d)`, removing an apparent forward dependency on B1. This is a self-contained proof correction derivable from the ASN's own definitions of next and S(p,d).

## Issue 4: B4 carries implementation and future-concurrency essay prose
Reason: The required edit deletes a mechanism catalog and speculative concurrency prose while keeping the existing one-line implementation witness untouched. Removal of out-of-scope prose needs no new evidence; the witness already present is not being re-verified.

## Issue 5: B0a carries scope-rationale and equivalence-justification meta-prose
Reason: The fix removes an authorization-deferral aside and a restatement-justification, keeping the partition law and its consequence. Trimming meta-prose is internal editorial work.

## Issue 6: Bop proof justifies its own ordering to dodge circularity
Reason: The fix drops a paragraph about proof-ordering acyclicity and cites the invariants directly; the dependency facts already live in the Properties table. Wholly internal.

## Issue 7: B9 stacks three Nelson quotes making one point
Reason: The single claim (unbounded components) is already captured by T0(a); the fix keeps one motivating quote and removes redundant glosses. Selecting which existing quote to retain is editorial and needs no fresh design-intent input.

## Issue 8: B7 body precondition is redundant
Reason: B6(i) already entails parent T4-validity, so collapsing the precondition to "both (p,d),(p',d') satisfy B6" follows directly from the ASN's own definition of B6. Internal.
