# Channel Assignment — ASN-0036 review-144

**Date:** 2026-05-29 01:34

## Issue 1: Citations to a dissolved "ordinal-shift prefix lemma"
Reason: The required fix is fully specified — swap the phantom lemma name for OrdinalShift (ASN-0034), already in the Depends lists, and note the `j = 0` identity convention. Derivable from the ASN's own dependencies; no external channel needed.

## Issue 2: S8 partition proof omits the empty-arrangement boundary
Reason: Adding the `dom(M(d)) = ∅` vacuous-partition line is a self-contained editorial fix derivable from the existing definitions and postconditions. No external channel needed.

## Issue 3: Downstream-consumer justification in D-CTG
Reason: Removing a sentence that forward-references D-CTG-depth/D-SEQ is a pure anti-bloat deletion; the relevant fact is already established locally in those proofs. No external channel needed.

## Issue 4: S3 one-directionality stated twice; S8a forward-justifies S8-depth
Reason: Trimming duplicated prose/Frame text and removing a forward-justification tail are editorial deletions internal to the ASN. No external channel needed.
