# Channel Assignment — ASN-0042 review-71

**Date:** 2026-05-29 06:45

## Issue 1: O1a/O1b "derived invariant" rationale stated three times
Reason: Pure deletion of duplicated meta-prose; the derivation already lives in *Delegation* and the Properties table. Removing the explanatory clauses from the `pfx` axiom and State Axioms intro requires no design or implementation input.

## Issue 2: MostSpecificCoveringUnique is stated, proved, and never used
Reason: This is a decision about the ASN's own proof structure — whether to wire the corollary into its advertised sites or delete it. Both options are internal; the covering-chain lemma, O1b, and the cited proofs are all already present.

## Issue 3: O18 body is rationale and implementation narrative, not an axiom statement
Reason: The required action is trimming rationale and implementation narrative down to the formula plus base/inductive roles — all of which are already stated. Pure editorial reduction, derivable from the ASN alone.

## Issue 4: Roadmap inventory in State Axioms
Reason: Straight deletion of an enumeration duplicated by the Properties table's Status column. No external input needed.

## Issue 5: Defensive "what is NOT used" citations
Reason: Removing negative-citation parentheticals; the positive derivation from Prefix is already given in each proof. Internal.

## Issue 6: Worked-example and O10 meta-prose about what each paragraph is doing
Reason: Deletion of sentences narrating the paragraphs' evidentiary status; the concrete ✓ checks remain untouched. Internal.

## Issue 7: Disproportionate existence essays in O7(c) and O8 precondition
Reason: Compression of over-argued constructions into citations of NestingByDelegation and O15/O12, all of which are already established in the ASN. Purely internal restructuring.
