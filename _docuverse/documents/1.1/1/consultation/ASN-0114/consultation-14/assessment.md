# Channel Assignment — ASN-0114 review-14

**Date:** 2026-06-09 22:28

## Issue 1: F6's confinement is coverage-level, but the prose and evidence assert representation-level non-exposure
Reason: The fix is internal — it scopes the prose down to what F1+F3 already deliver. F3 already supplies the exact pattern (representation is "below the abstraction," an implementation artifact), and the Q18 evidence is already quoted in the ASN; the required move is to recharacterize that evidence's *scope* as corroborating the implementation rather than the contract, which follows directly from the ASN's own F3 reasoning. No new design-intent or implementation fact is needed.

## Issue 2: F5 derivation is followed by a redundant premise recap
Reason: The fix is a pure deletion of a redundant recap sentence whose content (F1 and L12-via-LP13 carry F5) is already stated in the labeled derivation directly above. Entirely internal and editorial.

## Issue 3: F7's wp paragraph is bracketed by meta-commentary that does not advance it
Reason: The fix is editorial — drop the defensive "no backward reasoning is exercised" pointer and compress the trailing third-conjunct restatement so the two wp formulas stand on their own. Nothing turns on design intent or implementation evidence.
