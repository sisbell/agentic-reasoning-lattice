# Channel Assignment — ASN-0042 review-68

**Date:** 2026-05-29 06:20

## Issue 1: `delegated_Σ` has no fixed signature
Reason: Fixing the predicate's arity is a formalization choice internal to the ASN — the branching transition semantics, the six conditions, and the structural `R_Σ` definition are all already present in the text. No design intent or implementation evidence bears on whether to write it 4-place or adopt `R_Σ` as primary.

## Issue 2: O7(a) re-proves the named covering-chain lemma
Reason: Pure deduplication — the named lemma (PrefixesOfCommonAddressAreComparable) already exists in *Ownership Domains*; the fix is to cite it and delete the inline restatement. Entirely internal.

## Issue 3: "Why the axiom is needed" prose attached to axioms
Reason: Trimming meta-prose from axiom slots; the formal contracts already carry the statement, signature, and binding constraints. No external input needed to remove justification paragraphs.

## Issue 4: Use-site inventories on derived properties
Reason: Deleting downstream-consumer bookkeeping that does not advance any property's meaning. Purely editorial and internal.

## Issue 5: SelfOwnershipAtPrefix deferral stated twice in one paragraph
Reason: Removing one of two identical disclaimers in a single paragraph. Internal.

## Issue 6: Worked-example trajectory re-derived after claiming to summarize
Reason: Choosing a single site for the B6/B1 discharge and citing the cumulative `Σ.B` elsewhere — both derivations already exist in the ASN. Internal deduplication.

## Issue 7: O8 re-explains the delegated_Σ duality
Reason: Once Issue 1 fixes the signature, this paragraph collapses to a sentence or disappears; it duplicates the duality explanation at the `delegated_Σ` definition. Internal.
