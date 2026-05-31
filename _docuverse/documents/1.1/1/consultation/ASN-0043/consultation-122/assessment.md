# Channel Assignment — ASN-0043 review-122

**Date:** 2026-05-30 18:58

## Issue 1: L11a's shared-home merge conflates `#E ≥ 2` with `#E = 2`
Reason: Derivable from the ASN alone. Fix option (a) — generalize the merge by observing both chains share the single `inc(d, 2)` child-spawn and thereafter lie in one subtree of 𝒯 — uses only L1c, L1b, and T10a's at-most-once constraint already in the ASN; no design-intent or implementation fact is needed to discharge GlobalUniqueness's single-system precondition without claiming sibling-of-one-allocator structure.

## Issue 2: Properties table cell carries a proof sketch, not an index entry
Reason: Purely editorial — collapse the cell to a one-line index entry and leave the reasoning in the body where it already lives. No external evidence or design intent is involved.

## Issue 3: Defensive/plausibility prose that does not advance the claim
Reason: Purely editorial deletion of two sentences that gloss already-discharged claims (L10's biconditional, L-fin's statement). The surrounding arguments stand without them; no channel input needed.
