# Channel Assignment — ASN-0040 review-22

**Date:** 2026-05-11 09:49

## Issue 1: Invariant proofs do not explicitly handle Σ.B-frame transitions
Reason: Fix is internal — the Σ.B-frame case is trivial (children(B', p, d) = children(B, p, d) when Σ'.B = Σ.B), and B0a's partition is already defined in the ASN. Just split the inductive steps in B1 and B10 to cite the frame case before the baptismal case.

## Issue 2: Finiteness of Σ.B is not stated as a preserved invariant
Reason: Fix is internal — finiteness derives mechanically from B₀ conf. (finite seed) plus B0a (at most one new element per transition). Add an explicit B_fin invariant, prove inductively, cite at consumption sites.

## Issue 3: Genesis inclusion is claimed "by stipulation of B₀ conf." but is not actually stipulated
Reason: Fix is internal — the choice between extending B₀ conf. with a fourth clause vs. rephrasing the bridge paragraph as a separate cross-ASN axiom is a documentation-structure decision. The substantive claim (genesis inclusion is an obligation, not a theorem) is already accepted in context.

## Issue 4: Bop's listed preconditions do not match the operation description
Reason: Fix is internal — purely a presentation consistency issue between the description text and the Formal Contract. Decide whether B1/B10 are state invariants (discharged by induction) or per-call obligations and apply uniformly.

## Issue 5: B6 necessity sub-case (b) at d = 2 conflated with sub-case (a)
Reason: Fix is internal — the d = 2 propagation argument is fully derivable from TA5(b), TA5(c), TA5(d), and T4(ii), all of which are already cited in the ASN. The reviewer has even sketched the correct argument; it just needs to be inlined.
