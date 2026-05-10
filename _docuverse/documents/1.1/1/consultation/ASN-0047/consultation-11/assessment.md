# Revision Categorization — ASN-0047 review-11

**Date:** 2026-03-17 05:36

## Issue 1: J4 formal statement is universally quantified but false as stated
Category: INTERNAL
Reason: The prose already correctly describes J4 as characterising a specific composite kind; the fix is rephrasing the formal statement to match — a notation/scoping fix derivable entirely from the ASN's own definitions and intent.

## Issue 2: K.μ~ decomposition argument applies J1 at wrong level
Category: INTERNAL
Reason: The ASN's own definition of valid composite transition specifies that coupling constraints are evaluated between initial and final states; the correct composite-level argument (ran(M'(d)) \ ran(M(d)) = ∅) is directly derivable from the reordering definition already present.

## Issue 3: K.μ~ called "elementary" despite acknowledged decomposability
Category: INTERNAL
Reason: This is a terminological consistency issue within the ASN — the completeness argument already distinguishes five primitive kinds from the state structure and acknowledges K.μ~'s decomposability; the fix is aligning the framing language with the analysis already present.
