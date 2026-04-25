# Regional Review — ASN-0034/TA-strict (cycle 1)

*2026-04-23 04:18*

### T3 (CanonicalRepresentation) cited as "this ASN" but not defined
**Class**: REVISE
**Foundation**: (foundation ASN — internal)
**ASN**: TumblerAdd's Depends ("T3 (CanonicalRepresentation, this ASN) — equality sub-case of dominance concludes `r = w` from component-wise agreement and equal length"); T1's Depends ("T3 (CanonicalRepresentation, this ASN) — bridge between component-level agreement and tumbler equality; Case 1 concludes `a = b`, Cases 2 and 3 conclude `a ≠ b`"). Proof steps citing T3 include TumblerAdd's dominance sub-case `aₖ = 0` ("so `r = w` by T3") and T1 trichotomy Case 1 ("so `a = b` by T3").
**Issue**: T3 is referenced as a sibling claim in this ASN but the ASN content contains no T3 statement (no CanonicalRepresentation section). Both the dominance proof's equality branch and T1's trichotomy Case 1 / Cases 2–3 rest on T3 to bridge component-wise agreement (and equal length) with tumbler equality. Without T3 established, those equality conclusions are ungrounded and the trichotomy argument cannot discharge `a = b`.
**What needs resolving**: State and prove CanonicalRepresentation (T3) within this ASN — or, if it belongs to a different foundation ASN, correct the Depends annotations to not say "this ASN" and wire T3 in as a foundation import.

### Use-site meta-prose in TA0 and TA-strict bodies
**Class**: OBSERVE
**Foundation**: —
**ASN**: TA0 ("TA0 exports TumblerAdd's first two postconditions as a single labelled well-definedness fact."); TA-strict ("TA-strict exports TumblerAdd's ordering postcondition as a single labelled fact so downstream users (chiefly T12 span well-definedness) can cite one corollary rather than TumblerAdd's full postcondition list.").
**Issue**: Both wrapper claims carry a sentence whose content is a downstream use-site inventory and a justification for the claim's existence, not reasoning. "chiefly T12 span well-definedness" names a claim outside this ASN and will rot if T12 is renamed. The prose sits in the claim body rather than advancing the proof.

### Inconsistent "this ASN" annotation on NAT-* citations
**Class**: OBSERVE
**Foundation**: —
**ASN**: T0's Depends marks "NAT-closure (NatArithmeticClosureAndIdentity, this ASN)" but NAT-order in the same list lacks the "this ASN" tag; elsewhere (TumblerAdd, TA-Pos, ActionPoint) NAT-closure is cited without "this ASN".
**Issue**: The "this ASN" annotation is applied inconsistently across Depends lists for the same referent. Either all NAT-* sibling citations should carry it or none should; mixed usage obscures whether NAT-closure is defined in this ASN or imported.

VERDICT: REVISE
