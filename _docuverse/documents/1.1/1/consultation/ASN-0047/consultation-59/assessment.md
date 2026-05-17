# Channel Assignment — ASN-0047 review-59

**Date:** 2026-05-16 21:25

## Issue 1: Prefix-incomparability preservation under suffix extension is asserted without proof
Reason: The fix is a pure structural derivation over the tumbler prefix relation `≼` defined in ASN-0034 (Prefix decomposes into length-difference and component-difference cases). Both cases can be discharged inline without design intent or implementation evidence.

## Issue 2: K.μ~ contract is defined in two locations with overlapping content
Reason: Editorial reorganization — moving the K.μ~ contract out of the elementary-transitions list into a dedicated subsection. No design intent or implementation evidence needed.

## Issue 3: K.μ⁻ amendment cites D-SEQ★ before its formal definition
Reason: Document-ordering fix — either move D-SEQ★'s derivation earlier or restructure so K.μ⁻'s amendment follows it. Purely internal restructuring.

## Issue 4: "Arrangement invariants from elementary preservation" lemma hand-waves the S8 derivation
Reason: The fix requires either an explicit short derivation from S8-fin + S8a + S2 + S8-depth + T5 + TA5(c) + TA7a (all foundation-named) or a named packaging lemma from ASN-0036. Either path is internal to the ASN's already-cited foundations.
