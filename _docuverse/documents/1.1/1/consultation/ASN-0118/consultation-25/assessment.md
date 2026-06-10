# Channel Assignment — ASN-0118 review-25

**Date:** 2026-06-10 08:51

## Issue 1: CP7(c) states prior-content link survival without the LP12 chain CP7(b) is careful to supply
Reason: Internal fix. The required derivation uses only material already in the note — CP3a/CP3b for range-retention of displaced images and LP12 (ASN-0098, already cited) with `Σ'.L = Σ.L` (CP7a) for discoverability preservation. CP7(b) already models the exact chain to mirror; no design intent or implementation evidence is at stake.

## Issue 2: bare S3 (ASN-0036) cited for post-state referential integrity where S3★ (ASN-0047) governs
Reason: Internal fix. This is a citation-correctness slip — S3★ (ASN-0047) supersedes S3 in the extended state and is already used correctly in CP0(a); replacing the bare-S3 citations with S3★'s `s_C` branch is a consistency edit derivable from the note's own dependency choices.

## Issue 3: defensive and comparison meta-prose in CP0(a)
Reason: Internal fix. Pure prose deletion — the per-position grounding sentence preceding CP0 already discharges CP0(a) via S3★, so removing the defensive clause and the C1-coincidence note requires no external input.

## Issue 4: modeling-choice meta-commentary in the content-residence precondition and the resolution prose
Reason: Internal fix. Anti-bloat prose cleanup — state the precondition formula, drop the modeling-move commentary, downstream-consumer inventory, and "reuse rather than reinvent" aside; nothing here turns on design intent or implementation behavior.
