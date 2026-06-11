# Channel Assignment — ASN-0117 review-32

**Date:** 2026-06-11 01:33

## Issue 1: Reachability precondition is too weak for the composite-boundary discharge
Reason: The fix is internal — the review itself supplies the correct hypothesis ("composite boundary of a valid transition trace," P4a's sense in ASN-0047), and the change is to strengthen the stated precondition and re-route two citations to it. No design intent or implementation evidence bears on which reachability notion ASN-0047's theorem licenses.

## Issue 2: J1★ discharge silently narrowed to the operated document
Reason: Internal — the review identifies the missing step and its proof (DEL-FDOC gives `M'(d') = M(d')` for `d' ≠ d`, so no address is range-new for any other document). The fix is to state J1★ at its full quantification and add that one-line discharge, all from material already in the ASN.

## Issue 3: DEL-LIMM justified by restating its conclusion instead of citing its premises
Reason: Internal — the required premises are named in the review and live in already-cited foundation material (ASN-0047's K.μ⁻ and amended K.μ⁺ frame clauses listing `L' = L`, and J2 for the single-step case). This is a citation-discipline repair, not a question of what the design intends or what the code does.

## Issue 4: Anti-bloat — the "we do not re-derive" disclaimer recurs five times, plus twin deferrals
Reason: Internal — purely editorial consolidation: state the citation discipline once, delete the repeated disclaimers and the "justified, not asserted" framing while keeping the substantive disjointness step, and name the composite-frame discharge once for DEL-FENT/DEL-FPROV to cite. No external facts are needed.
