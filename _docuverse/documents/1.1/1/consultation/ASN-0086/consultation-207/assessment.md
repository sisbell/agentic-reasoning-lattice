# Channel Assignment — ASN-0086 review-207

**Date:** 2026-06-01 16:00

## Issue 1: Higher-arity caveat duplicated across three sites
Reason: Pure deduplication of redundant prose already present in the ASN; consolidating the higher-arity caveat into the `L_K` definition's `|Σ.L(a)| = 3` conjunct plus one note is fully internal, requiring no design intent or implementation evidence.

## Issue 2: Observe_K is defined as a core operation but never exercised concretely
Reason: `Observe_K`'s signature, `View` selector, and subset-match semantics are fully specified in the note; constructing a worked call at Σ_1/Σ_2 over the already-computed `L_K`/`A_K` states is mechanical instantiation of existing definitions, derivable from the ASN alone.

## Issue 3: "→*-reachability is closed under →" repeated as a standalone justification
Reason: Editorial deduplication of a closure fact already stated and used internally; establishing it once in the Working-domain paragraph and citing thereafter needs no external channel.
