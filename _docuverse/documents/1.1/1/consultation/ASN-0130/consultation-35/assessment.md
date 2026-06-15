# Channel Assignment — ASN-0130 review-35

**Date:** 2026-06-14 23:14

## Issue 1: register_pred's multi-read validation cites the wrong ASN-0134 consistency clause
Reason: Citation-correctness matter internal to the note — choose between citing MIC clause 6 (as PR5's structurally identical multi-slice lint read already does) or softening the "one coherent pre-state" claim via the order-insensitivity argument the reviewer sketches. Both options are derivable from ASN-0134 (a stated dependency) and the note's own existing PR5 citation; no design intent or implementation evidence is at stake.

## Issue 2: The adversary check (worked composition, step 5) attributes the frontier-ghost rejection to the wrong condition
Reason: PR0's own text already draws the distinction — never-registered referents fail (iii) ("`sig(r)` undefined — hence no typing judgment"), de-registered referents fail (iv) — so correcting the attribution is purely internal self-consistency.

## Issue 3: Anti-bloat — discursive comparison in the worked composition's step-1 parenthetical
Reason: Pure editorial trim; the load-bearing fact being retained (link/content chain disjointness) is from ASN-0093, a stated dependency, and no new claim requiring design intent or implementation evidence is added.
