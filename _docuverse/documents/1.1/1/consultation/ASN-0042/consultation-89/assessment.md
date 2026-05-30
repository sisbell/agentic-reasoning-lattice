# Channel Assignment — ASN-0042 review-89

**Date:** 2026-05-30 01:09

## Issue 1: O15's delegation-admission conditions do not guarantee O17b/O18 realizability
Reason: The reviewer prescribes tightening O15 with a `next`-reachability constraint, but the opposite fix (loosening O17b/O18) is viable if delegation was meant to target arbitrary subnumbers; picking the right direction needs design intent and implementation evidence on whether account allocation is contiguous.
Nelson question: Was account/document delegation intended to allocate the next sequential subnumber, or may an owner bestow an arbitrary subnumber skipping intervening stream positions?
Gregory question: Does the account-allocation path (findpreviousisagr / the ISA choke point) only ever produce the next contiguous sibling of a baptized stream, or can it baptize an arbitrary strictly-extending prefix in one step?

## Issue 2: O7(c) recursive-delegation right omits the contiguity precondition
Reason: This propagates the same next-reachability constraint resolved in Issue 1 to the recursive right; once Issue 1 fixes the admission gate, restating the obligation on `p''` follows from the ASN's own O17b/O18 coupling with no new external grounding.

## Issue 3: Forward-reference accretion and use-site inventory in O17b
Reason: Purely editorial trimming — reducing O17b to its disjunction plus one summary sentence and deleting the forward-reference essay is derivable from the ASN's own content with no design or implementation input.

## Issue 4: Organizational meta-prose in structural slots (State Axioms preamble)
Reason: Editorial deletion of regime-description prose whose scoping is already encoded in each axiom's quantifier; fully internal to the ASN.
