# Revision Categorization — ASN-0006 review-1

**Date:** 2026-03-06 21:38

## Issue 1: Self-transclusion makes TC4 and TC7 contradictory
Category: INTERNAL
Reason: The contradiction is a logical inconsistency within the ASN's own frame conditions. The fix (either adding a precondition or reformulating to read-before-write semantics) is derivable entirely from the existing definitions of TC4 and TC7.

## Issue 2: Transclusion independence proof cites TC5 and TC6 beyond their scope
Category: INTERNAL
Reason: The ASN already makes the general claims in prose ("once an address enters dom.ispace, it remains forever"). The fix is to formalize what the ASN already states informally — extracting two general axioms from existing prose and re-citing them in the proof.

## Issue 3: COPY has no stated precondition
Category: INTERNAL
Reason: The required preconditions (source/target exist, source V-span resolves, insertion position valid) are standard well-formedness conditions derivable from the operation's own effect clauses and the state definitions already in the ASN.

## Issue 4: TC12 is formally identical to TC11
Category: INTERNAL
Reason: The redundancy is visible from the formulas alone (conjunction commutes). The fix — merging or giving TC12 a distinct formalization using the general isolation axiom from Issue 2 — depends only on material already present or being added within the ASN.

## Issue 5: `discoverable_links` and `endsets` are not defined
Category: GREGORY
Reason: The definition of `discoverable_links` requires knowing what the link search mechanism actually checks. The ambiguity in `endsets(L)` — whether all three endsets (from, to, type) participate in discovery or only from/to — depends on what the implementation's search function inspects.
Gregory question: When the link search function checks for intersecting endsets, does it match against all three endsets (from, to, type) or only specific ones — and does the type endset participate in span-index-based discovery the same way as from and to?

## Issue 6: No concrete example
Category: INTERNAL
Reason: Constructing a worked scenario requires only the addresses, positions, and postconditions already defined in the ASN. No external evidence about design intent or implementation behavior is needed.
