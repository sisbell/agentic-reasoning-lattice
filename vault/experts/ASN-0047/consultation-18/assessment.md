# Revision Categorization — ASN-0047 review-18

**Date:** 2026-03-17 09:54

## Issue 1: Reachable-state invariants theorem lacks pre-state conditioning
Category: INTERNAL
Reason: The fix is purely logical restructuring. The ASN already contains the base-case verification (Σ₀ analysis) and the inductive-step derivations for each property — the theorem statement just needs to be reframed as an induction over reachable states or given an explicit pre-state assumption.

## Issue 2: Valid composite condition (3a) is redundant and confusingly labeled
Category: INTERNAL
Reason: The redundancy is derivable from the elementary transition frames already stated in the ASN. The fix is either removing (3a) and adding a lemma, or relabeling and annotating it as a consequence — no external evidence needed.

## Issue 3: Contains(Σ) absent from Properties Introduced table
Category: INTERNAL
Reason: Contains(Σ) is already fully defined in the ASN body. The fix is adding a row to the Properties Introduced table — a bookkeeping omission requiring no external input.
