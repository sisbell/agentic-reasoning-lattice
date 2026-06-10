# Channel Assignment — ASN-0127 review-26

**Date:** 2026-06-10 12:41

## Issue 1: Circular appeal to K.μ~-FIX while establishing witness admissibility
Reason: Pure proof-structure repair. The review identifies the non-circular route already implicit in the construction — each witness's `π` is defined as a permutation of the pinned domain, so domain fixity holds by construction — and ASN-0047's admissibility clauses are already cited in the note. No design intent or implementation evidence bears on which premise discharges the clause.

## Issue 2: Illustrated transitions skip their composite-coupling obligations
Reason: The missing obligations (J0, J1★) and their discharge path (P4★ at the initial composite boundary, P2 persistence across the contraction's `R' = R` frame) are all named machinery from ASN-0047, which the note already operates over; the review spells out the one-sentence fix per bullet. Internal bookkeeping, no channel needed.

## Issue 3: "Necessary but not sufficient" — the insufficiency half has no witness
Reason: The witness is constructible entirely from the note's own machinery — multi-span endsets are already admitted (Coverage is a function of an endset's spans, ASN-0043, and the worked illustration's singleton shorthand generalizes directly), and the review supplies the exact two-span construction. No intent or implementation question remains.

## Issue 4: E-INV re-derives F-CIL-perlink instead of citing it
Reason: Pure deduplication — replace an inline derivation with citations to LP13 and the earlier-stated F-CIL-perlink, whose hypothesis and conclusion match exactly. Entirely internal.

## Issue 5: `findlinks_disc` duplicates `findlinks_V` (minor)
Reason: Notational unification within the note; the anchoring distinction is carried by how the I-argument is obtained, which the prose already states, so collapsing to one symbol (or recording the identity in the table) is a mechanical edit. Entirely internal.
