# Channel Assignment — ASN-0100 review-104

**Date:** 2026-06-07 21:56

## Issue 1: Per-state invariant discharge fragmented across sections by a deferral chain
Reason: Purely an expository restructuring — consolidating per-address invariant proofs and removing relay pointers — derivable from the ASN's own content with no need for design intent or implementation evidence.

## Issue 2: INS.position duplicates INS.pre
Reason: A claims-table deduplication judgment; whether INS.position adds anything beyond INS.pre is settled by reading the two rows already present in the ASN, requiring no external channel.
