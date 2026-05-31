# Channel Assignment — ASN-0084 review-91

**Date:** 2026-05-30 18:42

## Issue 1: Merge definition is padded with consumer-enumeration and deferral meta-prose
Reason: Pure editorial deletion — the Merge definition (V-adjacency, I-adjacency, merged triple) is complete on its own, and the Open Question already records the deferral. Derivable from the ASN alone.

## Issue 2: R-BLK's "agrees with processing each cut against the original B" is an incorrect justification
Reason: The fix is a mathematical correction internal to the ASN — splitting at cuts is order-independent and the final boundary set is the union of B's boundaries and the cut set, which the ASN's own Phase 1 construction already supplies. No external channel needed.

## Issue 3: "Canonical decomposition" reinvents S8's maximality criterion without linking them
Reason: The equivalence (lockstep extension = V-adjacent/I-adjacent neighbor) follows from S8's definition in the cited foundation ASN-0036, which is already in scope; the reviewer supplies the one-line bridge. This is a formal-spec consistency fix, not a question of design intent or implementation behavior.
