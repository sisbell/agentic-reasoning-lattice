# Channel Assignment — ASN-0042 review-51

**Date:** 2026-05-14 09:15

## Issue 1: Foundation terminology error — "correspondence" vs "allocator"
Reason: Fix is internal — terminology must align with ASN-0034's T10a, which is already part of the lattice and uses "allocator" consistently. No design intent or implementation evidence needed.

## Issue 2: "Vacuously" misused in NestingByDelegation base case
Reason: Fix is internal — purely a rhetorical/logical precision adjustment within the ASN's own derivation. No external channel needed.

## Issue 3: Wrong sub-account in B1 prerequisite for `delegated(π_M, π_C)`
Reason: Fix is internal — the worked example controls its own bootstrap-state seeding, and the missing justification is an explicit statement about `Σ_0.B`'s contents already determined by the example's own setup. No external channel needed.
