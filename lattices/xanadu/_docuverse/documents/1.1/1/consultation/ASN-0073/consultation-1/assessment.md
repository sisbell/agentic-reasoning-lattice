# Revision Categorization — ASN-0073 review-1

**Date:** 2026-03-22 14:45

## Issue 1: Bare "+" on tumblers reinvents foundation notation
Category: INTERNAL
Reason: The fix is to rewrite using `shift` and `⊕` already defined in ASN-0034, and handle the `j = 0` case explicitly. All needed definitions are present in the foundation.

## Issue 2: Characterization claimed but not established
Category: INTERNAL
Reason: The fix is a scoping decision about what the ASN claims. Option (a) — downgrading "characterization" to "definition" and removing the preservation language — is derivable from the ASN's own content (which contains no proofs of either direction).

## Issue 3: Insertion model is implicit but load-bearing
Category: INTERNAL
Reason: The recommended fix aligns with Issue 2: if the ASN is a definition, remove the displacement claim entirely. The insertion/shift model will be defined when operations are specified; this ASN need only stop asserting something it hasn't formalized.

## Issue 4: N+1 count is wrong for the empty subspace
Category: INTERNAL
Reason: The error is mathematical — N is undefined in the empty case and the count is wrong given T3 (distinct depths yield distinct tumblers). The fix is to restrict the claim to non-empty subspaces and address the empty case separately, all derivable from existing tumbler properties.

## Issue 5: No concrete example
Category: INTERNAL
Reason: Constructing examples requires only applying the definition to concrete tumblers using V_S(d), D-CTG, D-MIN, and S8-depth from ASN-0036 — all already referenced in the ASN.
