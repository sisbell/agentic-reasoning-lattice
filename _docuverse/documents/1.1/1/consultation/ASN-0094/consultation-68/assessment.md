# Channel Assignment — ASN-0094 review-68

**Date:** 2026-05-24 19:03

## Issue 1: Forward-reference accretion is severe
Reason: Editorial/structural problem internal to the document — removing meta-prose, justifications, and reviser drift. No design intent or implementation evidence needed; the cleanup is derivable from the framework's own anti-bloat discipline.

## Issue 2: Sh5(b) status equivocation
Reason: The framework's META commitment about its own catalog discipline is an internal design choice. The decision between "framework-enforced gate" and "hand convention" doesn't depend on Nelson's design intent (Nelson doesn't write about template catalogs) or Gregory's implementation (udanax-green has no shape templates) — pick one reading and propagate consistently.

## Issue 3: Audit-slice set-semantics commitment buried in Nullify section
Reason: The commitment itself was already established with cited Nelson/Gregory consultation in the existing prose. The reviewer's request is structural — hoist the established commitment to the framework's main introduction. No new design/evidence question.

## Issue 4: Three Peano-style axioms tucked into appendix
Reason: Editorial structural change — surface existing framework-local commitments to the main level. The axioms and non-derivability arguments are already established in the appendix; the fix is purely about visibility.

## Issue 5: LinkAddressNotPrefixOfEmit doesn't cite TA5a explicitly
Reason: Citation correction against ASN-0034's named theorem list. The fix is derivable by reading the foundation ASN to confirm TA5a (IncrementPreservesT4) is the right named theorem for T4-preservation under increment, then updating the citation.

## Issue 6: "Reach of the framework's target-domain symbols" restriction
Reason: Substantive expressiveness limitation — whether to extend vocabulary to admit `dom(Σ.M)` (option a) or document the workaround (option b) depends on design intent and implementation evidence. Nelson's view on whether documents are first-class targetable, plus Gregory's evidence on udanax-green's link targets, jointly determine which option is right.
Nelson question: In the Literary Machines design, are document-level containers (the entities at `dom(Σ.M)` with `zeros = 2`) intended to be first-class targets of typed relations, or are relations specifically meant to target content-level addresses (the entities at `dom(Σ.C)` with `zeros = 3`) within those containers?
Gregory question: In udanax-green's link store, do links admit endsets whose spans cover document-container addresses directly (the equivalent of `dom(Σ.M)` entities), or do they exclusively cover content-level entities within documents?

## Issue 7: Caller-side rejection classification protocol
Reason: Editorial promotion — restructure existing protocol content into a named Definition/Lemma. Internal organizational change with no design or evidence question.

## Issue 8: Repeated stratification clauses
Reason: Editorial consolidation — state the stratification structure once at framework level and reference. Pure deduplication, derivable from existing content.

## Issue 9: Mutual exclusion of FDD and SHCD stated in multiple places
Reason: Editorial deduplication — state once and reference. The mutual exclusion fact is already established; the fix is to consolidate its presentation.

## Issue 10: BundledDirectedPair's empty-G admissibility paragraph is essay-like
Reason: Editorial condensation — replace design rationale prose with the operational fact. No design or evidence question; the framework's commitment to admit `n = 0` is already settled by `match(0, *)`.
