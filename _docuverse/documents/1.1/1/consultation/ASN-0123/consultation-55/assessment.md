# Channel Assignment — ASN-0123 review-55

**Date:** 2026-06-14 00:03

## Issue 1: V1 restates its own one-line claim three times over
Reason: Pure de-duplication of V1's own prose — drop the repeated source-size-independence and frame-equality restatements, keep the `ΔE`/`ΔM`/`ΔR` characterization, convert the G2 re-announcement to a back-cite. Every element already lives in the ASN (V1's equation, G2's derivation, V2's representation invariance); no design intent or implementation fact is at stake.

## Issue 2: the node-tier exclusion is fully explained in P-tier, then re-derived in V0
Reason: V0 should cite P-tier's already-resolved domain (owned ∪ account-tier-cross-owner) instead of re-arguing the node-tier exclusion; the full rationale is present in the contract's P-tier scope note, so the fix is an internal citation swap requiring nothing from either channel.

## Issue 3: V7 and VD both state "cross-owner forks are severed, recoverable only via shared content"
Reason: Consolidate the duplicated severance⟹not-address-discoverable⟹V9w-only kernel into VD (where it is load-bearing for the biconditional's failure) and have V7 cite it; both sections and the underlying severance theorem (V9) already exist in the ASN, so this is an internal restructuring with no Nelson or Gregory input needed.
