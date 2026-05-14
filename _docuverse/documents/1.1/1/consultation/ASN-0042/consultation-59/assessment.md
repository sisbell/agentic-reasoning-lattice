# Channel Assignment — ASN-0042 review-59

**Date:** 2026-05-14 12:29

## Issue 1: NestingByDelegation's equality-case argument is unclear and risks circularity
Reason: The fix is a proof-restructuring exercise using condition (ii) of `delegated_Σ` and the strict ordering from condition (i) — both defined within the ASN. The reviewer supplied the replacement argument; no design intent or implementation evidence is needed.

## Issue 2: O2's Step 2 inlines what is already a named lemma
Reason: The named lemma (PrefixesOfCommonAddressAreComparable) is already established in the *Ownership Domains* section of this ASN. The fix is purely citation hygiene — replace inlined derivation with a reference. Internal to the ASN.

## Issue 3: O7(c)'s "right is recursive" appeals to O7(a)'s domain-restricted result for an unrestricted-tumbler claim
Reason: The fix is to separate two distinct arguments and ground the most-specific-covering claim on condition (vi) of the delegation relation rather than postcondition (a). All references are to ASN-internal definitions; the reviewer supplied the exact replacement text.

## Issue 4: Worked-example bootstrap snapshot includes ad-hoc seed addresses without their joint consistency proven
Reason: Tabulating the consistency check or condensing unused seeds is presentation work over already-established T4/B1/O14 obligations. The relevant constraints are defined in this ASN and ASN-0040; no external channel needed.

## Issue 5: Form B sub-delegate analysis in O10 leaves the "longer Form B" case under-justified
Reason: The fix is a one-sentence clarification about how PrefixBaptismCoupling and `hwm` interact — both internal mechanisms. The reviewer supplied the exact text to add. Internal to the ASN.

## Issue 6: Properties-Introduced table conflates "axiom" with "design requirement"
Reason: Terminology unification across the table. The choice of "axiom" vs "design requirement" is an editorial decision about the ASN's own vocabulary, not a question about design intent or implementation. Internal.
