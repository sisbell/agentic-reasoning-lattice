# Channel Assignment — ASN-0082 review-45

**Date:** 2026-05-30 07:50

## Issue 1: Core arithmetic derivations rest on ASN-0034 lemmas absent from the foundation
Reason: Internal. Resolution is either verifying the cited NAT lemmas against the ASN-0034 foundation document directly (sibling-spec reading, not a design-intent or implementation question) or rebuilding the derivations from the explicitly-listed available axioms (NAT-addcompat/closure/discrete/order/wellorder) — a pure formal derivation question. Neither Nelson's design intent nor Gregory's implementation evidence bears on whether a natural-number identity is derivable from a given axiom set.

## Issue 2: ASN-0036 citations to S7c and S9 reference nonexistent foundation claims
Reason: Internal. The review identifies the phantom citations and the in-spec replacements: drop the S7c conjunct (S7's own dependency list already omits it) and substitute S0 for the bogus S9, since S0 already supplies the content-preservation guarantee. Both fixes are citation hygiene resolvable from the ASN's own content and the foundation reference; no design or implementation input is required.

## Issue 3: Ordinal toolkit cited as foundation but not present in the extract
Reason: Internal. ord/vpos/w_ord/OrdAddHom are already fully defined within ASN-0082's "Ordinal Extraction" section, so the fix is a citation-status correction — verify their presence in ASN-0036 (direct sibling-spec reading) and relabel as "cited" or "introduced" accordingly. This is bookkeeping against the foundation document, not a question of design intent or code behavior.

## Issue 4: I3-V redundancy explained at length instead of resolved
Reason: Internal. The ASN already proves I3-V is a corollary of I3-CS; the fix (demote to a one-line corollary or remove, and delete the justification paragraph) is a pure editorial decision derivable from reasoning already present in the note.

## Issue 5: Duplicated wp "recipe" prose and parallel deferrals across the two halves
Reason: Internal. Consolidating the duplicated wp-recipe framing and the repeated future-INSERT-ASN deferrals is an editorial restructuring task fully derivable from the ASN's existing content; no external channel is needed.
