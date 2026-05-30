# Channel Assignment — ASN-0042 review-80

**Date:** 2026-05-29 23:32

## Issue 1: O3 proof omits freshness condition when asserting the delegation predicate
Reason: Internal — the fix replaces a mis-numbered subset citation "(i)–(vi)" with the full `delegated_Σ(π_d, π')` predicate, which O15 already guarantees held at π''s introducing event; the correct form is present elsewhere in the same ASN (O8, OwnershipDomainPermanence Step 1).

## Issue 2: Covering-chain lemma states its independence from T5 three times
Reason: Internal — purely editorial deduplication; the proof's actual dependencies (Prefix, T3) are stated in the ASN, and the redundant independence-from-T5 disclaimers are removed without altering any claim.

## Issue 3: O1b axiom prose explains why-needed and forward-references O2
Reason: Internal — delete the rationale sentence; O2's dependency list already names O1b as a premise, so no external context is required.

## Issue 4: O14 prose enumerates downstream consumers
Reason: Internal — remove the use-site enumeration; each consuming induction already cites O14's relevant clause as its base case within the ASN.

## Issue 5: `allocated_by_Σ` axiom carries a "Mechanism: Out of scope" sub-paragraph
Reason: Internal — drop the redundant sub-clause; the Scope/Principal Identity sections already declare the baptism mechanism out of scope, and Signature/Semantics remain self-contained.

## Issue 6: Transfer discussion duplicated across two sections
Reason: Internal — consolidate the two redundant provenance-vs-authority paragraphs into Structural Provenance and reduce the other to a pointer; both already defer to the same existing Open Question.

## Issue 7: "forevermore" refinement reading stated three times with a forward deferral
Reason: Internal — state the refinement gloss once at OwnershipDomainPermanence and have the other two sites cite it; no design-intent clarification is needed since the reading is already established in the ASN.

## Issue 8: DelegatorAllocatesPrefix freshness paragraph is procedural meta-prose
Reason: Internal — delete the "removes the need to argue" sentence; the mechanical content (condition (vii) + O18) is already stated in the preceding two sentences.

## Issue 9: Worked Example counterfactual branch is bloat
Reason: Internal — remove the parenthetical counterfactual; the running trajectory does not take it and the mutual-exclusivity point is already made by the preceding `[1,0,2,1]`/`[1,0,2,2]` sentence.
