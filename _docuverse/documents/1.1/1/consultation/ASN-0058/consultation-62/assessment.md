# Channel Assignment — ASN-0058 review-62

**Date:** 2026-05-30 10:15

## Issue 1: M6(d) is defensive filler
Reason: Pure editorial cleanup — removing a clause whose only operative fact (each piece is a mapping block) is already established in M4. Derivable from the ASN alone.

## Issue 2: M16a re-derives the prefix-copy fact twice
Reason: Proof consolidation using facts already cited (TumblerAdd, S7b, T3, T4-validity). No design intent or implementation evidence is at stake; derivable internally.

## Issue 3: The "M0 argument" is named but re-expanded inline at use sites
Reason: Consistency fix — replace inline TS4/TS5 re-expansions with citations to the already-named M0 argument. Purely internal.

## Issue 4: M14 is subsumed by M14a
Reason: Structural decision (delete or demote M14) fully determined by the logical containment within M14a and the existing transclusion narrative. Derivable from the ASN alone.
