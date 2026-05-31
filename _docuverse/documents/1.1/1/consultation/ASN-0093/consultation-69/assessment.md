# Channel Assignment — ASN-0093 review-69

**Date:** 2026-05-31 12:26

## Issue 1: Freshness proof-pointers embedded in the K.α / K.λ binding preconditions
Reason: The fix is purely a relocation of existing prose — moving the freshness sentences out of the precondition slot and into the C0/append-only discharge where they are consumed. Both lemmas (FirstEmissionFreshness, SubsequentEmissionFreshness) and the discharge site already exist in the note; no design intent or implementation evidence is needed.

## Issue 2: Properties Introduced table reproduces lemma premise lists in the Source column
Reason: The fix collapses duplicated premise lists in the index to one-token origin pointers, with the canonical premise prose remaining in the lemma bodies already present in the note. This is internal editorial deduplication requiring neither design intent nor implementation evidence.
