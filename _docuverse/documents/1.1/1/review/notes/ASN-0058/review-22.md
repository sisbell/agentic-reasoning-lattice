# Review of ASN-0058

The mapping block algebra is well-developed: M0 (width coupling) and M1 (order preservation) are proved with careful split handling at k=0 vs k≥1 via TS4/TS5; M-aux's case split on c=0 / j=0 is correctly grounded in the OrdinalShiftBase convention; M-sub's depth-precondition sharpness is explicitly acknowledged; M7's necessity argument rigorously eliminates the overlap case via subspace identification (component 1 always defined), S8-depth lifting, and component-wise reduction to position m; M12's identification of maximally merged decompositions with maximal runs handles both partitioning of dom(f) and the (⟹)/(⟸) directions in detail, including the j ≥ 1 case via unit-shift injectivity; M16's origin-preservation argument correctly chains S7b/S7c/T10a.4 through TumblerAdd's prefix-copy clause; C0's family-of-witnesses construction at j > uₘ produces unboundedly many depth-m tumblers in ⟦σ⟧, contradicting S8-fin; C0a's J = ∅ argument correctly handles both the divergence-below-m and the #t < m cases; C1a's transfer of M11/M12 to a finite partial function f checks the three required conditions and the per-merge preservation of B1/B2/B3; C2's enumeration of depth-m tumblers in ⟦σ⟧ correctly yields ℓₘ. The two worked examples concretely verify the merge condition (V-adjacent without I-adjacent persists as a boundary) and the resolution machinery (cross-origin runs cannot fuse). Boundary cases — width-1 blocks (atomic, not splittable), empty arrangements (B = ∅ trivially maximally merged), and decompositions across subspaces (M-sub confines each block to one subspace) — are handled.

## REVISE

(none)

## OUT_OF_SCOPE

(none)

VERDICT: CONVERGED
