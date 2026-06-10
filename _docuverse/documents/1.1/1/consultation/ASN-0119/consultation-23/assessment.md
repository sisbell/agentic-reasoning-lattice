# Channel Assignment — ASN-0119 review-23

**Date:** 2026-06-10 02:27

## Issue 1: LP3 cited for coverage invariance, but LP3 is a transition lemma that did not consider REARRANGE
Reason: Internal fix. The correction is a re-attribution: swap the LP3 citation for ASN-0098's *Definition — Coverage* (already imported in this note) and carry invariance through RA6 directly. The required derivation is fully present in the ASN — it mirrors the note's own re-derivation of RA7a in place of LP11. No design intent or implementation evidence is at stake.

## Issue 2: "the contiguity outcomes are therefore four" — count does not follow, and overstates exhaustiveness
Reason: Internal fix. This is a logical/expository defect in the note's own framing — the within/across reasoning yields two outcomes (preserved/broken), so "therefore four" must be dropped and the cases recast as representative illustrations. Resolvable entirely from the note's existing analysis; no external channel bears on it.
