# Channel Assignment — ASN-0117 review-23

**Date:** 2026-06-09 10:26

## Issue 1: Claim-label revision history embedded in the spec
Reason: Purely editorial — deleting a preamble paragraph that narrates label history. No design intent or implementation evidence bears on removing PR-description content; the table and current claims are already present in the ASN.

## Issue 2: Raw LaTeX macros leaking into prose
Reason: Pure notation cleanup — replacing `\!\restriction\!` with the `|`-restriction form the ASN already uses in its foundation citations. Derivable from the ASN alone; no channel needed.
