# Channel Assignment — ASN-0130 review-27

**Date:** 2026-06-13 06:07

## Issue 1: ST⁺'s aggregate-threshold extension is broader than its soundness argument
Reason: ST⁺ and its soundness argument are formal constructs internal to this note; the fix is either to narrow the phrasing to "ℕ literal or environment-bound parameter" (the two cases the present soundness proof already covers) or to add the saving clause. The saving fact — that PD0's grammar admits no ℕ-binding guard, so only literals and parameters reach a threshold — is a property of ASN-0129's rule set, a peer-spec fact the review itself states and verifies, not a question of Nelson's design intent or udanax-green's behavior (neither of which models ST⁺/PD0 at all).

## Issue 2: PR1 mis-cites the class governing pdef de-registration
Reason: Pure internal citation error — the note's own Standard registrations section defines PS1 as `pdef` and PS2 as `pd_stable`, so the correct reference for `pdef` de-registration is fixed by the ASN's own content.
