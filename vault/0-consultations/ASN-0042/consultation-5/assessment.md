# Revision Categorization — ASN-0042 review-5

**Date:** 2026-03-15 21:37

## Issue 1: O1b preservation by delegation is unstated
Category: INTERNAL
Reason: The review itself supplies the complete contradiction argument from conditions (i) and (ii) of the `delegated` definition, both already stated in the ASN. The fix is to write out that argument explicitly.

## Issue 2: O2 well-definedness — linear ordering of covering prefixes is a parenthetical
Category: INTERNAL
Reason: The three proof steps (WLOG, component equality via shared target, prefix conclusion) use only the prefix relation definition already present in the ASN. This is a proof expansion, not a knowledge gap.

## Issue 3: Corollary cites O5 for delegation authorization
Category: INTERNAL
Reason: The `delegated` definition's condition (ii) is already stated in the ASN and enforces the same most-specific-covering-principal constraint. The fix is a citation correction referencing existing ASN content.

## Issue 4: O6 derived property — `pfx(ω(a)) ≼ acct(a)` proof skips intermediate steps
Category: INTERNAL
Reason: The missing chain uses T4's field structure (referenced from ASN-0034), the prefix relation, and `acct(a)`'s definition — all already present or cited in the ASN. The fix is to spell out the four-step argument the review identifies.
