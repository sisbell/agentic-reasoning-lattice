# Channel Assignment — ASN-0042 review-70

**Date:** 2026-05-29 06:45

## Issue 1: MostSpecificCoveringUnique is stated but never consumed
Reason: Purely editorial — the choice to cite the corollary at its re-derivation sites and delete inline repetitions, or to remove it, is resolvable from the ASN's own proof structure. No design intent or implementation evidence bears on it.

## Issue 2: O14 misattributes why FiniteRegistry is needed
Reason: Internal — the ASN's own proofs show that O10's non-coverage analysis is universally quantified (no maximum taken) while NestingByDelegation and MostSpecificCoveringUnique are the actual consumers of finiteness. The correct attribution is derivable by reading the proofs.

## Issue 3: "Why the axiom is needed" prose around the state axioms
Reason: Internal trimming — the necessity arguments reference downstream properties already present in the ASN, and the Nelson/Gregory design citations the fix retains already appear in the text. No new channel input is required to relocate or compress them.

## Issue 4: Document-ordering prose pairing O5 across two sections
Reason: Internal editorial — deciding where O5 lives and dropping the cross-pointers is a structural choice within the ASN, requiring no external evidence.

## Issue 5: Duplicated `acct(a)` definition and contract
Reason: Internal — both the AccountField well-formedness and AccountPrefix case analyses are already in the ASN; consolidating them into one shared case split is a mechanical de-duplication.

## Issue 6: Repeated deferral and repeated "forevermore" elaboration
Reason: Internal editorial — the redundant restatements and Worked-Example deferrals are all present in the ASN; collapsing them to a single home is a structural consolidation needing no external input.

## Issue 7: Meta-prose about citation and roadmap bookkeeping
Reason: Internal — the citation-practice note and derivation roster duplicate the Properties Introduced table already in the ASN; removing them is purely editorial.
