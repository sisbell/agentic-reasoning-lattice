# Revision Categorization — ASN-0042 review-9

**Date:** 2026-03-15 22:44

## Issue 1: Principal-introduction closure axiom missing
Category: INTERNAL
Reason: The ASN already defines delegation (O7) and bootstrap (O14) as the two principal-introduction mechanisms, and the gap is simply that it never states these are exhaustive. Adding a closure axiom is a formal completeness fix derivable from the existing model structure.

## Issue 2: O1b preservation proof covers only one case
Category: INTERNAL
Reason: The missing case (two new principals in the same transition colliding) can be resolved from the existing delegation definition — condition (ii)'s uniqueness of the most-specific covering principal and condition (iii)'s freshness requirement are already stated. The proof extension or single-introduction constraint follows from existing definitions.

## Issue 3: AccountPrefix lemma quantifier domain
Category: INTERNAL
Reason: The fix is a straightforward quantifier restriction from T to T4-valid tumblers. The ASN already notes that acct relies on FieldParsing which assumes T4, and only applies the lemma to allocated addresses. The correction is derivable from existing definitions.

## Issue 4: O10(b) is a consequence of O10(a), not an independent condition
Category: INTERNAL
Reason: The ASN's own O6 biconditional proof already establishes that pfx(π) ≼ a ≡ pfx(π) ≼ acct(a) for principals with zeros ≤ 1. Deriving (b) from (a) via this biconditional requires only the ASN's existing results.

## Issue 5: O6 forward-direction wording overstates
Category: INTERNAL
Reason: The proof logic is correct — only the word "exactly" is misleading. The ASN's own worked example (pfx = [1,0,2] vs acct = [1,0,2,3]) demonstrates the strict containment case. The wording fix is a direct editorial correction.
