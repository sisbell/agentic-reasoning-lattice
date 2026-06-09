# Channel Assignment — ASN-0126 review-45

**Date:** 2026-06-09 11:21

## Issue 1: Dangling forward reference "the front end (below)"
Reason: Pure editorial fix derivable from the ASN — the note already establishes (Single-source) that multi-source/discontiguous relations fall outside `→_sh` to the app/ungated `→`, so the "(below)" pointer can be dropped and restated as app responsibility without external input.

## Issue 2: P6's induction is fragmented across two sections
Reason: Structural reorganization only — relocating the `Σ_init.L = ∅` commitment to the Registry-permanence `Σ_init` setup and consolidating P6's induction uses material already present in the note; no design intent or implementation evidence required.

## Issue 3: wp derivation does not discharge L3 (`K ∈ T_admissible`)
Reason: The needed argument (registry stores a non-empty representative `K_j`, so `coverage(K) = coverage(K_j) ≠ ∅` and `K ∈ T_admissible`) is already proven inside P5's proof in this ASN; the fix just lifts that inline into the wp section. Internal.

## Issue 4: Coalescing guidance names only "abutting" spans
Reason: Derivable from the note's own `|F| = 1` rule — any multi-span presentation (abutting, overlapping, or nested) yields `|F| ≥ 2` and is rejected identically, so generalizing the guidance follows from the stated span-count semantics without external input.
