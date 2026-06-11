# Channel Assignment — ASN-0129 review-2

**Date:** 2026-06-11 11:57

## Issue 1: PC6's converse is circular as argued, and its unqualified statement contradicts C-reach
Reason: Internal — the fix is a definitional repair to the note's own apparatus (defining the evaluation class PC6 quantifies over, re-scoping the equality, fixing the `chain` parenthetical); the iterate-`succs` counterexample is already conceded in the note's own text, and no design intent or implementation behavior is at stake.

## Issue 2: PC2's typing excludes its own worked example, and the guard has no narrowing rule
Reason: Internal — restating PC2 over state-indexed functions mirrors the same-Σ/same-view provision PC0 already states, and the narrowing/binder rule is a grammar amendment to the note's own guard machinery.

## Issue 3: QD-fin's base case rests on an uncited premise
Reason: Internal — the reviewer already searched the cone (ASN-0086/0126/0128) and found no finiteness clause, so the sanctioned fix is the explicit named-hypothesis route; finiteness of initial stores is a modeling axiom trivially faithful to any realizable implementation and needs no evidence consultation.

## Issue 4: A QD domain expression is used in term position with no licensing rule
Reason: Internal — both sanctioned fixes (adding the address-valued domain→term rule, or striking the first spelling) are syntax repairs, and the finding itself supplies the restriction the new rule needs.

## Issue 5: The "activeness test composition otherwise lacks" justification is refuted by the note's own algebra
Reason: Internal — the refuting term is built entirely from the note's own primitives (PC1 over `A_K`, V-TUP's `addr`, V-PRIM equality), and the surviving ground for the totalization (definedness-stability for PC4/PC5) is already stated in the same paragraph.

## Issue 6: FP under-reports `targets_keyed`'s footprint, making PD2's per-type clause unsound for terms containing it
Reason: Internal — the cross-type footprint follows directly from ASN-0128's BH3 definition, which the finding quotes verbatim, and the required PD2 exception parallels the home-wide BH4 treatment the note already performs.

## Issue 7: The two enumerations of "exactly three admissions" disagree
Reason: Internal — a bookkeeping contradiction between two of the note's own passages; reconciling to one consistent enumeration requires only the note's own accounting of its read-surface additions.

## Issue 8: The `elems`/`chain` count identity fails at the default view
Reason: Internal — the failure is a direct consequence of the note's own UV clause (traversal unfiltered, returned sequence rewritten elementwise); qualifying the identity to audit/active views is a local correction.

## Issue 9: `Map_fin` is an admitted codomain with zero admitted operations
Reason: Internal — the decision material is fully in hand: the atom is committed upstream (ASN-0128 BH3), the redundancy of a lookup with `target_of` is already noted in the finding, and choosing between admitting a consumer and fencing root-position-only is a language-design call within this note's own scope.

## Issue 10: T2 is listed as an atom; it is a computability theorem, not a relation
Reason: Internal — ASN-0034's T1/T2 are in the dependency cone and the note already uses T2 correctly as a computability warrant elsewhere ("the T2-decidable prefix test"); the fix is a re-listing, not new content.

## Issue 11: PC3's view discipline is presented as a semantic boundary, but it fences no expressiveness
Reason: Internal — the finding's reconstructions (audit readings from `L_K` + V-TUP + PC2a) use only semantics this note has already fixed, so restating PC3 as an atom-name-binding convention and re-scoping Open Question 1 is derivable from the note's own content.
