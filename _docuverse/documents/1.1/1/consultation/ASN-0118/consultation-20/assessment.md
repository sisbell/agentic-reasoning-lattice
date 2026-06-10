# Channel Assignment — ASN-0118 review-20

**Date:** 2026-06-09 18:56

## Issue 1: CP5 conflates the spec-set source with the content's actual allocator
Reason: The fix is a wording correction grounded entirely in the ASN's own cited material — `origin` is field-projected from the address (S7) and invariant while stored (S7d), so the true allocator is determined structurally regardless of how many transclusion hops intervene; the chained-transclusion counterexample is produced by COPY's own CP2+CP1, and CP11 already uses `origin` correctly, so no design-intent or implementation evidence is required.

## Issue 2: CP11's formal object is a set, but the claim and example require a multiset
Reason: Pure notation fix (set-builder → multiset or indexed-sequence brackets) fully specified by the reviewer and derivable from the ASN's own prose ("multiset") and worked example (`{d_A, d_A, d_B}`); internal.

## Issue 3: CP0(a)'s bridge asserts run interval-disjointness without its reason
Reason: The missing justification draws only on premises the ASN already cites — shift fixes the lexicographic prefix (ASN-0034) and S8-depth gives `act(ρ,Σ)` a common depth (ASN-0036) — so the non-interleaving "wholly below the next run" step is derivable by making the existing reasoning explicit; no channel needed.

## Issue 4: Forward-reference signposts and defensive justification prose
Reason: Editorial trimming of meta-narration, forward-reference seeds, and a redundant general-principle paragraph, with the object-level content to retain already specified; entirely internal to the note's exposition.
