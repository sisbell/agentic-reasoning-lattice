# Channel Assignment — ASN-0112 review-41

**Date:** 2026-06-08 11:53

## Issue 1: Tight's wp derivation misattributed to V5/V6
Reason: Internal fix — the correction replaces a wrong cross-reference (V5/V6) with the right one (D0/D1), both already present and proved in the ASN. No design intent or implementation evidence is at stake; it is a pointer correction.

## Issue 2: V-ReachTight duplicates V2's own reach-equality clause
Reason: Internal fix — the duplication is between two claims stated in the ASN itself, and the resolution (fold the iff into V2 or strip it from V2) is a structural deduplication using only the ASN's own definitions (`reach(σ_d) = r⋆`, ASN-0053).

## Issue 3: wp digression computing `wp(…, V-ReachTight) = true` only to discard it
Reason: Internal fix — cutting the methodological digression and stating `Tight`'s wp directly uses only material already present (the D0/D1 factoring); it is a prose-trimming edit needing no external channel.
