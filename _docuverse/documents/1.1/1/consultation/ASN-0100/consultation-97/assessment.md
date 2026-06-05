# Channel Assignment — ASN-0100 review-97

**Date:** 2026-06-05 07:47

## Issue 1: Per-invariant spelling-out of link-subspace inheritance bloats the atomicity proof
Reason: Purely editorial collapse — the fix replaces a per-invariant enumeration with a single unchanged-set sentence, derivable entirely from the ASN's own frame statement (`n'_{s_L} = n_{s_L}`). No design intent or implementation evidence is needed.

## Issue 2: Redundant frame restatement in §Effect Three
Reason: A deletion of prose that duplicates the Formal Contract's Frame Conditions and the INS.frame.* claims already present in the ASN. The authoritative statements are internal; no channel is needed.

## Issue 3: Deferral cluster — multiple sections defer the same discharge downstream
Reason: Restructuring where a single discharge (S8a/S8-depth for the Insertion region, and the §Provenance discharge) lives versus where it is forward-referenced. All the content already exists in the ASN; consolidating it requires no external input.
