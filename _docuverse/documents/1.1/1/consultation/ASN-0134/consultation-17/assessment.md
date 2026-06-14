# Channel Assignment — ASN-0134 review-17

**Date:** 2026-06-14 00:56

## Issue 1: `age`/`stale` are misclassified as single-type / single-index "Observe_K-grade" reads
Reason: ASN-0128 BH4 already settles the *cross-type* nature (the chain interleaves every type homed at `d`), so that correction is internal — but the fix's branch point is whether `age`/`stale` stay single-index *home-relative* reads (fix a) or become §8 cross-type multi-reads needing clause 7 (fix b), and that turns on whether the home frontier `f_d` is a single readable quantity in the substrate or must be assembled from the per-type sub-chains. That read-surface/allocator-structure fact is implementation evidence, not design intent or internal to ASN-0134.
Gregory question: Is a home's interleaved link-allocation frontier `f_d` maintained as a single count readable in one access (e.g. a per-home width/frontier at the enfilade home node), or is it recoverable only by scanning/maxing across the per-type sub-chains homed at that document?

## Issue 2: A1's behavioral-read enumeration omits `is_in_chain`
Reason: Pure enumeration completeness — `is_in_chain` is defined in ASN-0128 BH2 as a single-type walk-membership test, already zero-step and single-index like `chain` (the reviewer confirms no classification changes), so the fix is to add it or switch to the D1–D4/BH1–BH4 category citation; fully derivable from the cited foundation.
