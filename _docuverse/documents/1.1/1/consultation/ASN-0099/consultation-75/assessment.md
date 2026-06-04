# Channel Assignment — ASN-0099 review-75

**Date:** 2026-06-04 14:33

## Issue 1: Filtered-form content placed in the Match Predicate section, before the filtered form is defined
Reason: Pure structural relocation — moving one already-written sentence into the section that defines `(i, J)` and the out-of-range guard. No design intent or implementation evidence needed; both halves of the split already exist in the ASN.

## Issue 2: Forward-pointer meta-prose advertising F4
Reason: A deletion of signposting prose. F4 and its witnesses already carry the individuation; removing the announcement requires nothing external.

## Issue 3: The unfiltered-as-union-of-single-slot-filters identity is stated without derivation
Reason: The required one-line derivation (each single-slot filter's own guard `i ≤ |Σ.L(a)|` collapses the union over `1..N` to the existential over `1..|Σ.L(a)|`) follows entirely from the filtered-form definition already present in the ASN. No external channel needed.
