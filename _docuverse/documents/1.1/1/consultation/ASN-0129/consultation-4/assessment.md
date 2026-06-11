# Channel Assignment — ASN-0129 review-4

**Date:** 2026-06-11 12:58

## Issue 1: V-IDX's universal-attachment condition is wrong for `targets_keyed`, and its shape rider is wrong for `age`
Reason: Internal — both corrections are already pinned by sources the note itself carries: FP's own "indexed by no single K" settles that `targets_keyed` takes no class parameter, and the review's accurate quotes of ASN-0128's BH3 join and R-C0 compatibility clauses (shape for BH1/BH2/BH3, `idem = ⊥` for BH4) fully determine the rewritten condition and rider. No design-intent or implementation question remains open.

## Issue 2: Whether `Reg` admits QD filtering and PC2a folds is left undefined
Reason: The fix is a genuine design fork — extend V-IDX's static expansion to all `Reg`-binding positions, or restrict `Reg` to PC1 quantification — and nothing in the ASN decides it: the committed cross-type forms survive either choice. Whether the type space was meant to be a queryable domain is design intent (Nelson), and whether the implementation's read surface ever computes over types rather than taking them as parameters is implementation evidence (Gregory).
Nelson question: Did the design intend the link-type vocabulary itself to be queryable as a domain — e.g., "which types of links are in use on this document," "how many types appear here" — or do types enter queries only as caller-supplied selectors, with the open-ended type vocabulary never enumerated or aggregated by the system?
Gregory question: Does any udanax-green read operation enumerate, filter, or aggregate over link types (e.g., return the set of types occurring among matched links, or count links grouped by type), or do types appear in the read path solely as caller-supplied type-set parameters to queries like findlinksfromtothree?

## Issue 3: PC2a's "set semantics, settled" clauses omit their view qualifiers, and one is false as stated
Reason: Internal — the corrected qualifiers are fully determined by ASN-0128 facts the note already cites: the note's own V section states I1a as an *active*-tuple bound, and the review's I2/R6c (resurrection re-deposits) and I3 (born-nullified) citations fix the audit/active split for both clauses. The fix is mechanical restatement, not new ground.

## Issue 4: PC6's statement equates a set of predicates with a class containing non-predicates
Reason: Internal — this is a typing repair to the theorem statement; the review observes (correctly, from the note's own text) that both proof directions already operate over COD-valued terms, so restating at the term level or adding a Boolean-restricted corollary is derivable from the note's content alone.
