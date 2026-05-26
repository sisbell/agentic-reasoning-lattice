# Channel Assignment — ASN-0094 review-83

**Date:** 2026-05-25 18:21

## Issue 1: Cross-ASN references to non-foundation ASNs
Reason: The fix is internal — the ASN's own scaffolding clauses already supply what the proofs need, and the reviewer offers an explicit derivation path ("the locally stated scaffolding clauses already supply what the proofs need"). The "strictly stronger" rephrasing operates entirely on the ASN's own vocabulary.

## Issue 2: Overly long introduction paragraph on semantic departure
Reason: Pure editorial compression — move rationale to Nullify Compatibility section (already exists) and reduce introduction to one sentence. No expert consultation needed.

## Issue 3: Defensive meta-prose at parametric template signature
Reason: Pure editorial removal of a meta-justification sentence; the preceding signature stands on its own. Internal fix.

## Issue 4: Two paragraphs covering coverage-class disjointness from R
Reason: Editorial consolidation of two adjacent paragraphs into one, plus removal of a forward-reference sentence. Internal fix.

## Issue 5: Sh4 Case A enumeration's "exhaustive coverage" defensiveness
Reason: Editorial removal of a restatement sentence; Lemma CaseAClosureForLK already establishes the partition that Sh0/Sh1/Sh2/Sh3 cite without redundant exhaustiveness prose. Internal fix.

## Issue 6: AllocatedAddressAntichain Case 3 length handling
Reason: Internal proof correction — the announced length dispatch never fires in Steps 3.1–3.3, and the E-field argument at i = n_3 + 1 is uniform across both length cases. Removing the misleading announcement is a direct read of the proof.

## Issue 7: Two scope-related sentences in different sections covering single-process substrate
Reason: Editorial consolidation — establish scope once and have other locations refer by name. Internal fix.

## Issue 8: Template signatures use overloaded `from_K^Σ`/`from_K(a)`
Reason: Naming convention is a design choice internal to the framework (which is this ASN's own construction, not Nelson's design intent or a udanax-green convention). Choosing a disambiguating rename is editorial.

## Issue 9: Catalog Curation Discipline NOTE entry in Properties Introduced
Reason: Editorial table reorganization — author conventions don't belong alongside load-bearing definitions and lemmas. Internal fix.

## Issue 10: Worked example for K = comment has inconsistent reference to Sh-conf gate ordering
Reason: Editorial clarification — either repeat the gate label at first use or use natural-language description. Internal fix.
