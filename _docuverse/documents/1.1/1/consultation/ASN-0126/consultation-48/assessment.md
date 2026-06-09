# Channel Assignment — ASN-0126 review-48

**Date:** 2026-06-09 11:43

## Issue 1: Domain-discharge argument misplaces the type slot and gives a false justification
Reason: The fix is internal. The ASN already cites ASN-0043's StandardTriple convention (type at `e₃`), and the corrected justification — arity 3 makes `{e₁, e₂}` the only content slots so the two-slot test is exhaustive — is derivable from material already present in the note.

## Issue 2: Single-source buries its commitment under retraction-responsibility prose
Reason: The fix is internal. This is a pure restructuring task: state `|F| = 1` first, compress the retraction prose, and relocate responsibility/exit material. No design-intent or implementation fact is in question; all the content already exists in the note.

## Issue 3: Two-way deferral for the gate-vs-landing separation
Reason: The fix is internal. The gate-vs-landing separation is already fully reasoned in The shape-gated emit (the third inherited conjunct); the task is to state it once there and drop the reciprocal back-pointer — an editorial consolidation of present content.

## Issue 4: Open questions defer six items to one downstream location
Reason: The fix is internal. Removing per-item editorializing and the closing exhaustiveness sentence requires only trimming the note's own prose; no external evidence or design intent is needed.
