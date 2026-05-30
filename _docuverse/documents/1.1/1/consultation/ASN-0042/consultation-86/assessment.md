# Channel Assignment — ASN-0042 review-86

**Date:** 2026-05-30 00:37

## Issue 1: O7(c) claims condition (vii) is "trivially satisfied at Σ'" but never derives it
Reason: The fix is internal — either derive freshness at Σ' from B1/contiguity (ASN-0040 facts already cited throughout this ASN, e.g. that the just-baptized `pfx(π')` can have no pre-existing descendant child stream) or simply weaken the "trivially satisfied" claim to make (vii) conditional. Both paths use only the ASN's own axioms and ASN-0040 references already present.

## Issue 2: The "descent is the principal's organizational choice, not a requirement of O10" claim appears three times
Reason: Pure editorial deduplication — collapse three restatements into one in O10's contract. No external evidence needed.

## Issue 3: O8 duplicates the "owner may be π' or a sub-delegate, but never returns to π" remark
Reason: Editorial deduplication of two near-identical paragraphs within O8; keep the in-proof version. Derivable from ASN alone.

## Issue 4: AccountField's Formal Contract repeats the prose well-formedness derivation
Reason: Editorial deduplication — the case analysis is given twice; consolidate to one derivation and reduce the contract postconditions to bare claims. No external input.

## Issue 5: O10 Non-coverage analysis excludes a case the standing prefix invariant already forbids
Reason: Internal logic cleanup — `pfx(π_i) = pfx(π).0` is already excluded by the standing T4/O1a invariant on principal prefixes (a derived invariant in this ASN); drop the redundant rebuttal and cite the invariant once.

## Issue 6: Defensive terminology/disambiguation meta-prose in two structural slots
Reason: Editorial compression of the T8-distinction notation and the seed/allocate adjudication paragraph; both restate facts already established in the ASN. No external channels.
