# Channel Assignment — ASN-0102 review-3

**Date:** 2026-05-28 14:28

## Issue 1: J1'★ coupling discharge is invalid for self-transclusion (and any copy of content `d` already references)
Reason: Internal fix. The repair is a proof correction using definitions already in the note — split `{a_j+i}` into addresses new to `ran(Σ.M(d))` (recorded by COPY's effect) versus those already present (already in `Σ.R` by P4★), then discharge J1'★ for each class. No design intent or implementation evidence is at stake; X3, P4★, and the J-invariants supply everything.

## Issue 2: X7's freed-gap justification is stated backwards
Reason: Internal fix. Purely a temporal-phrasing correction (the gap is freed *by* the `·+W` relabelling, not pre-existing); the disjointness argument via TS1/TS2/TS4 is already present and correct. Derivable from the ASN alone.

## Issue 3: Symbol `Σ` overloaded — state vs. transition vocabulary
Reason: Internal fix. A notation disambiguation — pick a distinct symbol for the transition vocabulary versus system state. No external channel; the convention is fixed inside the note and its cited foundations.

## Issue 4: S8a not discharged for the interior copied positions
Reason: Internal fix. The interior positions `[s_C,1,…,1,p+c]` structurally satisfy S8a (subspace id ≥ 1, intermediate 1s, positive last component, depth `m ≥ 2`); the note already derives their shape in X16 and need only add the confirming line. Derivable from the ASN alone.
