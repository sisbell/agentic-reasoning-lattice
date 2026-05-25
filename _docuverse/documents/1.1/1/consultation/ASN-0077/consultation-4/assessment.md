# Channel Assignment — ASN-0077 review-4

**Date:** 2026-05-25 15:59

## Issue 1: Mixed V-spans citation error
Reason: Fix is internal — reviewer has identified the correct foundation citations (C0a PrefixConfinement and C0 from ASN-0058) that replace the incorrect S8-depth argument. No design intent or implementation evidence needed.

## Issue 2: O2 derivation — M-sub bridge missing or mis-ordered
Reason: Fix is internal — pure reordering of derivation steps using foundation properties already cited (S3★, M-sub(a), S8a, CL-OWN). The reviewer specifies the correct ordering.

## Issue 3: Singleton I-span — length-preservation chain compressed
Reason: Fix is internal — reviewer has identified the explicit foundation citations needed (SubAllocatorAxiom clauses (b)(c)(d), TA5(c)) and the structural chain to spell out. All references are to ASN-0047 properties already in the lattice.

## Issue 4: O5 hypothesis redundant
Reason: Fix is internal — restating O5 to drop the redundant conditional, using P0/L12/P3 monotonicity invariants already cited in the derivation. Pure logical simplification.
