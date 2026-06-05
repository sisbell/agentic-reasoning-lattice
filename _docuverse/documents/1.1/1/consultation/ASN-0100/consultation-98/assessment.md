# Channel Assignment — ASN-0100 review-98

**Date:** 2026-06-05 07:58

## Issue 1: Per-address content invariant discharge is duplicated across two sections
Reason: Purely editorial deduplication — consolidating two copies of the same per-address discharge into one location and replacing the other with a pointer. No design intent or implementation evidence is involved; the argument and its lemma citations are already present in the ASN.

## Issue 2: Step 1 cites the wrong lemma for the freshness precondition
Reason: The ASN itself already names the correct lemmas (SubsequentEmissionFreshness / FirstEmissionFreshness) in §Effect One; the fix swaps the misplaced ChainEnumerationInjectivity citation for those. Fully derivable from the ASN's own content.
