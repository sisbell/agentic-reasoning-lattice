# Channel Assignment — ASN-0103 review-30

**Date:** 2026-06-08 08:59

## Issue 1: The invariant verification is stated twice, in full
Reason: Pure editorial deduplication — collapse the table cell to a summary, keep the prose section. No design intent or implementation evidence is at stake; the content is already present in the ASN.

## Issue 2: Roadmap and editorial meta-prose that advances no reasoning
Reason: Deleting previews and editorial rankings is internal prose surgery; the frame clauses already stand on their own. No channel needed.

## Issue 3: Defensive justification of a proof strategy not taken
Reason: The freshness derivation (`d ∈ S(A,2) \ D_A ⊆ S(A,2) \ E`) already avoids contiguity, so removing the disclaimer touches nothing load-bearing. Fully internal.

## Issue 4: Out-of-scope forking mechanics described at paragraph length
Reason: Reducing the forking description to the single `ran(M'(d)) = ∅` contrast is a scope-trim using material already in the ASN; CREATENEWVERSION's mechanics are explicitly out of scope, so no Nelson/Gregory input is needed to cut them.
