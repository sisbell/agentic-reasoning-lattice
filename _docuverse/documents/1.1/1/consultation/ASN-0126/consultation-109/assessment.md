# Channel Assignment — ASN-0126 review-109

**Date:** 2026-06-10 14:36

## Issue 1: `→_sh*`-reachability is quantified over everywhere and defined nowhere
Reason: Internal. The review prescribes the exact definition (reflexive-transitive closure of `→_sh`, rooted at the registry-adjoined `Σ_init`), and all ingredients — `→_sh`, `Σ_init`, and ASN-0086's definitional pattern to mirror — are already present in the note; this is a definitional bookkeeping fix, not a design-intent or implementation question.

## Issue 2: the ghost-root witness misstates how single-tuple scope fails
Reason: Internal. The correct conclusion is already derivable from the note's own passage — the same paragraph proves `a ∉ dom(Σ.L)` via L1b, and the operation contract's only-if clause states the omission direction correctly; the fix is to make the narrative witness consistent with reasoning the note already contains.

## Issue 3: reviewer-facing announcement clauses (anti-bloat)
Reason: Internal. This is a prose deletion — strip the announcement clauses while keeping the discharges they introduce, preserving the one load-bearing fragment the review identifies; no design intent or implementation evidence bears on it.
