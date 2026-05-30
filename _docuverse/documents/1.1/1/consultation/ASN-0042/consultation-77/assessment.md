# Channel Assignment — ASN-0042 review-77

**Date:** 2026-05-29 23:02

## Issue 1: O7(c) omits the freshness gate (vii) from recursive-delegation obligations
Reason: The fix is internal — condition (vii) is already fully defined in the ASN's `delegated` predicate, and the worked example already states the namespace/principal exclusivity. Adding (vii) as a re-checking obligation and discharging it for the chain witness (each link's prefix is the unique freshly-baptized prefix at its step, hence ∉ Σ.B prior) is derivable from the ASN's own content.

## Issue 2: O2 design justification misattributes exclusivity to `tumbleraccounteq`
Reason: The correction rests on what the udanax-green predicate actually computes — whether it enumerates a registry and performs longest-match, or only a single account-level equality check — and what `validaccount` actually establishes. These are implementation-evidence claims requiring Gregory.
Gregory question: Does `tumbleraccounteq` (and the `isthisusersdocument` path) enumerate the principal registry and compute a longest-prefix match, or does it only perform a containment/equality check against the single session account tumbler — and does `validaccount` enforce anything beyond unconditionally returning TRUE?

## Issue 3: Preservation proofs of O1a, O1b, T4 are deferred far downstream
Reason: Purely a structural co-location/cross-reference fix within the ASN; no design intent or implementation evidence is at stake.

## Issue 4: Meta-prose explaining why (vii)/O18 exist rather than what they assert
Reason: Editorial reduction to the bare assertion and a single statement of the (vii)/O18 coupling; derivable from the ASN alone.

## Issue 5: Repeated `acct(a)` definition and repeated `tumbleraccounteq` description
Reason: Deduplication of an internal definition and an implementation walkthrough already present in the ASN; no external channel needed.
