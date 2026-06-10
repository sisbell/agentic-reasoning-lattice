# Channel Assignment — ASN-0114 review-25

**Date:** 2026-06-10 00:55

## Issue 1: The L12↔LP13 composition is stated four times, and the intro's standalone attribution to L12 is imprecise
Reason: Internal fix. The ASN already states the correct relationship in its Derivation (L12 is single-step; LP13 composes across `Σ →* Σ'`); the task is to consolidate four restatements and correct the intro's attribution to match what the ASN already says. No design intent or implementation evidence is at stake — this is exposition cleanup using content already present.

## Issue 2: The synthesis re-derives the dependency structure already carried by the Claims table
Reason: Internal fix. The parenthetical merely duplicates the Status-column derivation annotations already in the Claims table; removing it requires no external input — only deletion of redundant text whose source is the table itself.
