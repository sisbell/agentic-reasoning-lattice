# Channel Assignment — ASN-0100 review-93

**Date:** 2026-06-05 07:04

## Issue 1: Foundation claims renamed with non-canonical aliases
Reason: Purely a naming-consistency fix against the foundation ASNs (0047/0093); the canonical names are already given in the review, so no design-intent or implementation evidence is needed.

## Issue 2: Duplicated invariant-discharge prose between §Verifying the Invariants and §Atomicity
Reason: A structural de-duplication entirely within this ASN — consolidate the discharge in §Atomicity and cross-reference; derivable from the ASN's own content.

## Issue 3: Defensive meta-prose around the I3 inheritance
Reason: Editorial removal of disclaimer text while keeping the decomposition statement and I3 citation; no external input required.

## Issue 4: Bidirectional forward/back references for the same two claims
Reason: A reorganization to make S8a and INS.inv.depth self-contained in one place using arguments already present in the ASN; internal.
