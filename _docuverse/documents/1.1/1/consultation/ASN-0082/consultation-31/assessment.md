# Channel Assignment — ASN-0082 review-31

**Date:** 2026-05-15 11:28

## Issue 1: Incomplete NAT citation for the strict inequality `1 + c > c`
Reason: This is a foundation-level proof gap. The fix is to spell out the chain using NAT axioms (NAT-addcompat, NAT-addbound, NAT-cancel, NAT-closure) already cited from ASN-0034, or introduce a derived strict order lemma once and cite it. No design intent or implementation evidence is involved — the conclusion is correct and the foundation axioms needed are already available.

## Issue 2: "Necessity from TA4" argument suppresses TA4's `k = #a` clause
Reason: This is a logical exposition issue requiring restatement of the necessity argument with TA4's full conjunctive precondition made explicit. TA4 and S8a are already cited from ASN-0034 and ASN-0036; the joint interaction at #p > 2 versus the vacuous satisfaction at #p = 2 is derivable from those statements alone.

## Issue 3: I3-V's stated necessity is unsupported — it is a corollary of I3-CS
Reason: This is a specification-structure choice between (a) dropping I3-V or (b) retaining it for readability with corrected justification. The reviewer presents both options as legitimate; the choice is editorial and derivable from the ASN's own closure logic (I3-CS already excludes the relevant positions). Neither design intent nor implementation evidence bears on the axiomatization granularity question.
