# Channel Assignment — ASN-0086 review-141

**Date:** 2026-06-01 02:34

## Issue 1: `at-most-one-key-per-home` is load-bearing for L-ContiguousPrefix/R0a but is not part of the substrate-conforming-state definition
Reason: The fix is purely definitional bookkeeping — fold the note's already-stated at-most-one commitment into the substrate-conforming-state definition and reword clause (b) to single-key landing. Both the constraint and the rationale are already present in the ASN; no design-intent or implementation evidence is needed.

## Issue 2: Defensive meta-prose around the substrate-conforming definitions (anti-bloat)
Reason: Editorial restructuring — convert justificatory prose into definitional clauses and drop the independence essay. Derivable from the ASN's own content alone.

## Issue 3: Repeated downstream deferral to the Weakest-Precondition Analysis (anti-bloat)
Reason: Editorial deduplication — remove redundant forward pointers and keep the analysis at its single WP home. Fully internal to the note's structure.
