# Channel Assignment — ASN-0070 review-6

**Date:** 2026-05-25 13:53

## Issue 1: F-canonical Step 2's "Unique reconstruction" missing leftward closure
Reason: The fix is a pure proof completion using foundations already cited in the ASN (N1, N2 chained, and the consecutive-tumbler characterisation proved earlier in Step 2). The symmetric left-closure argument parallels the existing right-closure structure — no design intent or implementation evidence is required.

## Issue 2: CanonicalForm definition leaves V-position constraint on starts implicit
Reason: The fix tightens a definition so it matches an entailment already present (postcondition equality + S8a force start positivity). All ingredients — T12(b), S8a, the postcondition — are internal to ASN-0070 or its already-cited dependencies, so this is derivable from the ASN's own content.

## Issue 3: Citation imprecision — TA-strict vs T12(b)
Reason: This is a pure citation correction within ASN-0034's lemma catalogue; the reviewer specifies the target citation exactly. No design intent or implementation evidence is needed.

## Issue 4: F-canonical Step 2 cites T1 case (a) for ℕ-irreflexivity
Reason: This is a pure citation correction (T1 case (a) is tumbler-level; the chain in question is on ℕ components, so T0's NAT-order irreflexivity applies). No design intent or implementation evidence is needed.
