# Channel Assignment — ASN-0133 review-47

**Date:** 2026-06-14 16:05

## Issue 1: Regime (ii)'s grow-only argument is re-derived inside obstruction (3)
Reason: Purely internal — the fix replaces a duplicated mechanism with a back-reference to regime (ii), which appears a few sentences earlier in the same proof. Both the grow-only result and the target of the back-reference are already in the ASN; no design intent or implementation evidence bears on a redundancy cut.

## Issue 2: "strong-scheduling form of regime (i)" framing is undercut by the satisfiability caveat it follows
Reason: Internal logical-consistency fix — the ASN already establishes the turn-fairness premise (joint scheduler+environment), the add-remove counterexample, and that H-SFAIR + bounded growth reaches-and-holds without environment idle. Correcting the "sub-form of regime (i)" categorization to "distinct sufficient condition" follows from material already present; neither Nelson's intent nor Gregory's evidence is needed to adjudicate an abstract fairness relationship the note itself proves.
