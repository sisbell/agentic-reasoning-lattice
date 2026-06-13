# Channel Assignment — ASN-0108 review-46

**Date:** 2026-06-13 08:27

## Issue 1: W5's "no re-delivery" is scoped wrongly — the boxed claim is false under its own sole hypothesis (clause 1), and contradicts W9b
Reason: Pure internal logic/consistency fix. The required change — narrowing no-re-delivery's matching-scope to "continuously-matching from delivery through resume" — is dictated by the note's own cursor-advance-induction proof and by W9b's already-correct narrow form; the counterexample mechanics (content-position key, orphan/resurrect) are likewise present in-note. No design intent or implementation evidence bears on which scoping is mathematically correct.

## Issue 2: (anti-bloat): meta-prose around the key naming, and a repeated qualifier
Reason: Editorial trimming only — delete a naming-rationale sentence and collapse a thrice-stated multiplicity qualifier to one statement. Removing redundant prose requires neither design intent nor implementation evidence.
