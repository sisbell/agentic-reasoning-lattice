# Channel Assignment — ASN-0108 review-26

**Date:** 2026-06-13 01:28

## Issue 1: Defensive justification of a rejected scoping, plus a key-class aside
Reason: Pure deletion of a redundant counterfactual and its aside; the scoping it defends is already carried inline by "for every `a` matching in both states" and established by the per-step skip/duplicate unpacking below it, so the fix is fully derivable from the ASN's own content. No design intent or implementation evidence is at stake — nothing is being added or re-decided, only removed.

## Issue 2: The "state-stable but not value-total" cursor-survival argument is stated twice
Reason: Editorial deduplication — value-totality, its value-totality⟹state-stability (not conversely) relation, and the orphaning cursor-survival example are all already present in the ASN, merely stated in both the ladder and W8; consolidating to one site and trimming the ladder's use-site tags requires no new design intent or implementation fact. The logical roles being trimmed are each established at their points of use within the ASN.
