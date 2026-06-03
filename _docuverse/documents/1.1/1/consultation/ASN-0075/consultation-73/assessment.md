# Channel Assignment — ASN-0075 review-73

**Date:** 2026-06-03 11:38

## Issue 1: wp formulas for Q1 and Q0 include a boundary conjunct that is not part of the weakest precondition
Reason: This is a self-contained internal consistency fix — the ASN already establishes (for `q`) the reasoning that strips the boundary conjunct, and applying it uniformly to `Q1`/`Q0` plus correcting the "general rule" sentence requires only the ASN's own wp treatment. No design intent or implementation evidence is involved.

## Issue 2: Roadmap scaffolding that does not advance the argument
Reason: Pure prose deletion of two structural-announcement sentences; the fix is mechanical and derivable from the ASN alone, with no semantic or implementation question at stake.
