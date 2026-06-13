# Channel Assignment — ASN-0133 review-3

**Date:** 2026-06-13 11:00

## Issue 1: "H-W reduces to bounded domain growth" is false — what reduces is the real-fire count, not H-W
Reason: Entirely internal — the counterexample is constructed from the note's own definitions (W(σ), H-W, X-DEF, Q5a), and the repair (restate the lever as "finitely many real fires," make Q6 depend on that plus H-FAIR, drop "only unbounded-work route is unbounded new arguments") is a logical correction needing no design intent or implementation evidence.

## Issue 2: Q-FLIP's "exactly ASN-0129's falsifier inventory" omits deposit-driven re-arming
Reason: This is a consistency check against the note's own dependency cone — PD1/PD2 (ASN-0129) and BH3 "several → ⊥" semantics (ASN-0128) are already-formalized substrate results, not Xanadu design intent or udanax-green behavior, so aligning the enumeration (or softening "exactly" to "in particular") is derivable from cited content.

## Issue 3: `Post_ρ` is called "PL-expressible" over a sort PL does not have
Reason: The fix is a modeling choice between two internally-specified options governed by PL's COD type set (ASN-0129) and the operation surface (ASN-0128); both alternatives are sufficient for the note's uses, so no external evidence bears on which to pick.

## Issue 4: Q6 misattributes why post-bound fires are no-ops
Reason: A self-contained proof-citation correction — replacing the circular "Q1's argument" with Q5's bound reasoning (and adding the H-FAIR finite-σ case) draws only on results already proved in the note.
