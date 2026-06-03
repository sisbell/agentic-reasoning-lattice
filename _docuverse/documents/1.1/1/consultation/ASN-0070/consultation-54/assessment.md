# Channel Assignment — ASN-0070 review-54

**Date:** 2026-06-03 01:19

## Issue 1: F-subspace Consequence invokes L14 but omits it from Depends (and the invocation is avoidable)
Reason: Internal. The fix is a citation/derivation cleanup using claims the note already cites — S3★ supplies the forward direction and L0+postcondition the converse, so the L14 detour can be dropped without consulting either channel.

## Issue 2 (anti-bloat): meta-prose announcing which Frame slots are retained
Reason: Internal. This is a pure editorial trim of structural commentary; the F-persist and F-state Frame slots already carry the content, so no design-intent or implementation evidence is needed.
