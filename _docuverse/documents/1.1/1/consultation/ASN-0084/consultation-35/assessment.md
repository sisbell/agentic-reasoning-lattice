# Channel Assignment — ASN-0084 review-35

**Date:** 2026-05-15 15:49

## Issue 1: R-PRE(v) is derivable, not a precondition
Reason: Fix is derivable from the ASN's own content. CS2 (strict cut ordering), CS3 (subspace S), CS4 (depth 2), R-PRE(iv) (affected range covered by V_S(d)), and the singleton-tumbler identification (already established in the ASN) jointly entail w_α ≥ 1 and w_β ≥ 1 by the same argument the ASN already uses to derive w_μ ≥ 1. No channels needed.

## Issue 2: Permutation Displacement carrier canonical form not stated
Reason: Fix is internal to the definition. The case analysis in PermutationDisplacement already produces exactly the canonical triples (0,0), (+,n≥1), (−,n≥1); adding a canonical-form clause and equality discipline is editorial tightening of existing material.

## Issue 3: R-PPERM/R-SPERM piecewise definitions are silent on non-S positions
Reason: Fix is derivable from the ASN's own structure. R-FRAME-P(a) and R-FRAME-S(a) already specify π = identity on non-S, and R-PPERM/R-SPERM proofs cite this; adding an explicit non-S branch (or relabeling "exterior" as "exterior or non-S") is a notation fix.

## Issue 4: Maximality of the constructed canonical run is implicit
Reason: Fix is derivable from the proof's own definitions. f(v) and r(v) are defined as maxima of bounded sets; forward/backward extension beyond them would contradict the max property by definition. The maximality conclusion is a one-line addition referencing those existing definitions.

## Issue 5: Mutual exclusivity of Δ cases not established for non-S positions
Reason: Fix is derivable from R-PPERM/R-SPERM. Non-S positions satisfy π(v) = v (already established by R-FRAME-P(a)/R-FRAME-S(a) and reflected in the non-S branch of the piecewise π), so they fall under case (a) trivially and the NAT-sub-typed cases (+) and (−) are never reached.

## Issue 6: Informal "sign(w_β − w_α) · |w_β − w_α|" notation suggests undefined operations
Reason: Fix is purely notational and internal. The formal case-analysis branches immediately following the informal expression already give the correct definition; replacing the informal formula with a forward reference to those cases preserves content without invoking undefined operations.

## Issue 7: TS5 label inconsistency
Reason: Fix is a cross-reference check against the existing ASN-0034 foundation document within the project; the correct label is whatever ASN-0034 currently uses for TS5. No design-intent or implementation-evidence question is involved — just label conformance.
