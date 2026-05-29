# Channel Assignment — ASN-0053 review-37

**Date:** 2026-05-28 20:19

## Issue 1: S5 discharges TA-LC by appeal to "well-defined" rather than naming its preconditions
Reason: Purely internal proof-bookkeeping fix. The required preconditions (Pos, actionPoint bounds) come from TA-LC's already-cited contract and the proof's own TA-assoc consequences (ii)/(iii) and T12 — no design intent or implementation evidence needed.

## Issue 2: "level-uniform" / level_compat used before S6 defines them
Reason: Internal reorganization. Moving S6 ahead of WR and dropping a redundant inline rider is an editorial dependency-ordering fix derivable entirely from the ASN's own structure.

## Issue 3: Population-evolution caveat stated twice
Reason: Internal anti-bloat edit. The duplicated caveat already cites Nelson (LM 4/25); the fix is to state it once and trim, which requires no new theory or evidence.
