# Channel Assignment — ASN-0042 review-33

**Date:** 2026-05-14 02:44

## Issue 1: T2 misattribution in NestingByDelegation proof
Reason: Pure citation fix. The correct derivation source — the Prefix (PrefixRelation) definition applied componentwise — is already carried out in O2's proof Step 2 within this same ASN. No external evidence required.

## Issue 2: Unilateral O10★ depends on an unaxiomatized "baptismal coupling"
Reason: Choosing between adding a new state axiom (O18 DelegationBaptizes), strengthening `delegated` condition (v), or qualifying the Unilateral O10★ claim requires knowing whether the design intends delegation to materially baptize the prefix (Nelson) and whether the implementation actually does so (Gregory).
Nelson question: Does Nelson's design treat the act of delegating a sub-account at slot `k` under prefix `p` as itself baptizing `p.0.k` into the address registry, such that no delegated sub-account prefix can exist outside the high-water-mark range of its parent's child stream?
Gregory question: In udanax-green, when a sub-account is delegated (via the granfilade entry-creation path used by account allocation), is the sub-account's prefix entered into the granfilade/baptismal registry as part of the same operation, and does `findpreviousisagr` therefore see delegated sub-account prefixes when computing the next slot?

## Issue 3: T10a misnamed and misused in O9 supporting prose
Reason: Pure citation fix. The correct property (TA5(d) HierarchicalIncrement, k > 0 branch) and the correct name for T10a (AllocatorDiscipline) are both verifiable from the foundation ASNs (ASN-0034). No external evidence required.
