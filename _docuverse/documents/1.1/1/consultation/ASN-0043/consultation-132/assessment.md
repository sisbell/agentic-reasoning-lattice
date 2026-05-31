# Channel Assignment — ASN-0043 review-132

**Date:** 2026-05-30 20:42

## Issue 1: L11a's case analysis over-derives a single-step precondition
Reason: Pure proof-structure cleanup — replace the case split with a one-step citation of S7d (single tree 𝒯), L1c (chains stay in 𝒯), and GlobalUniqueness. Every input is already present in the ASN; no design intent or implementation evidence is at stake.

## Issue 2: L13's validity claim restates L4(c)
Reason: Editorial deduplication — drop the redundant "valid target" sentence and cite L4(c) for admissibility, retaining L13's own canonical-span content. Entirely internal cross-referencing.

## Issue 3: The "L0a discharge" is named for L0a but defined inside L0b
Reason: A labeling/cross-reference fix — relocate or rename the discharge argument so the name matches its definition site. No external evidence needed.
