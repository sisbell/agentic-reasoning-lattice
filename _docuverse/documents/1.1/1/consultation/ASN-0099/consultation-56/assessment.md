# Channel Assignment — ASN-0099 review-56

**Date:** 2026-06-03 09:36

## Issue 1: `discoverable_from = matches(ran(M(d)))` equality asserted without citing the bridge lemma
Reason: The fix is internal — it requires citing LP12 (DiscoverabilityCharacterisation, ASN-0098), a lemma already present in the lattice, at both assertion sites. No design intent or implementation evidence is needed; the bridge biconditional is already established upstream.

## Issue 2: "only treatment that leaves the operation total" is an unproven uniqueness claim
Reason: The fix is internal — the corrected discriminating property (totality without fabricating I-addresses absent from the arrangement) is derivable from `image`'s own definition and the surrounding reasoning. No design intent or implementation evidence is needed to restate the justification correctly.
