# Revision Categorization — ASN-0061 review-1

**Date:** 2026-03-21 10:19

## Issue 1: D-PRE(v) is unsatisfiable as stated
Category: INTERNAL
Reason: The fix is explicitly stated in the review — replace span denotation with a depth-restricted predicate. The rest of the ASN already works with V_S(d) directly, so the correct formulation is derivable from the existing definitions.

## Issue 2: The displacement w is used at two incompatible depths
Category: INTERNAL
Reason: The worked example already demonstrates the correct behavior at both depths; the fix is defining an explicit projection from V-depth to ordinal-depth displacement, which follows mechanically from TA7a's subspace/ordinal decomposition already referenced in the ASN.

## Issue 3: ord(v) is used throughout but never defined
Category: INTERNAL
Reason: The extraction and reconstruction functions follow directly from TA7a (ASN-0034), which the ASN already cites. The definition is implicit in every use — it just needs to be stated.

## Issue 4: Proofs restricted to depth 2 but claims unrestricted
Category: INTERNAL
Reason: The ASN itself flags the depth-general case as an open question. The recommended fix — restrict D-PRE(iv) to #p = 2 — requires no external evidence, only tightening the precondition to match the proofs already given.

## Issue 5: D-DP Case 2 contiguity argument is circular
Category: INTERNAL
Reason: The direct depth-1 proof is trivial integer arithmetic: consecutive integers shifted by a constant remain consecutive. The fix replaces a faulty general argument with a correct specific one, using only definitions already present.

## Issue 6: D-CTG's status as a system invariant is unresolved
Category: INTERNAL
Reason: The Nelson evidence for contiguity is already quoted in the ASN ("dense, contiguous sequence"). The resolution is a specification architecture choice — classifying D-CTG as a design constraint that restricts well-formed composites, or as a per-operation precondition — both derivable from existing ASN-0047 definitions without external consultation.
