# Regional Review — ASN-0034/OrdinalDisplacement (cycle 2)

*2026-04-24 06:42*

### NAT-wellorder and NAT-discrete declared after their consumer

**Class**: OBSERVE
**Foundation**: (none — internal structural ordering)
**ASN**: The ASN introduces foundation NAT-* claims in two groups: first NAT-zero, NAT-order, NAT-addcompat, NAT-closure at the top, then later NAT-wellorder and NAT-discrete appear between ActionPoint and OrdinalDisplacement — after ActionPoint whose derivation cites both ("By NAT-wellorder, there exists m ∈ S..." and "NAT-discrete's forward direction m < n ⟹ m + 1 ≤ n at m = 0..."). The dependency graph is acyclic (each claim's Depends list is complete), so soundness is not affected, but a reader working top-to-bottom encounters the citations in ActionPoint before reaching the bodies of NAT-wellorder and NAT-discrete.
**Issue**: Presentation order places two cited NAT-* foundation claims after their first consumer, breaking the "foundation first, consumers after" grouping the rest of the ASN follows. The split across two groups is not explained, and neither of the late-arriving claims depends on anything declared between the two groups (both depend only on NAT-order, with NAT-discrete also on NAT-closure), so nothing forces the late placement.

VERDICT: OBSERVE

## Result

Regional review converged after 2 cycles.

*Elapsed: 775s*
