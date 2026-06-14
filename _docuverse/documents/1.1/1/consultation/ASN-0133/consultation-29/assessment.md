# Channel Assignment — ASN-0133 review-29

**Date:** 2026-06-14 05:19

## Issue 1: Q0's view rebuild omits the default-view UV filter for `members`/`targets_of`/`M_K`
Reason: Internal — the fix composes two constructions already in the note: the `⋃(A_K/L_K, addrs_F)` audit↔active rebuild and the `{· : ¬filtered(·)}` UV default-view filter. The note's own six-collection UV enumeration already names `members`/`targets_of` as UV-rewritten and the heterogeneous example already builds the `filtered` body, so the correction (these three are both view-parameterized and UV-rewritten, hence take both) is derivable from content present in the ASN.

## Issue 2: PR-DISC framing in "Triggers: inline or by reference" states its conclusion twice around one technical sentence
Reason: Internal — pure redundancy/prose cleanup: collapse the duplicated "premise of Q0, not a condition on a link" conclusion to one statement, drop the unexplained scare-quoted "link"/"downstream" residue, and replace the Q1 unconditionality restatement with a single citation. No design intent or implementation evidence is at stake.

## Issue 3: "fire sequence" denotes two distinct things
Reason: Internal — terminology disambiguation the note itself already flags as "separate"; rename the fire-internal sense (a single fire's `→_sh` step run) so "fire sequence" is reserved for the H-FAIR-defined interleaving σ. No external input needed.

## Issue 4: H-RF, the operative hypothesis, is defined after the lemmas that conclude it
Reason: Internal — document reorganization: move H-RF and the H-RF/H-W separation ahead of W/H-W and Q5 so the three "(below)" pointers become backward references. The content is unchanged; only ordering is at issue.
