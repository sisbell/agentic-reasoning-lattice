# Channel Assignment — ASN-0086 review-7

**Date:** 2026-05-16 18:04

## Issue 1: R0a's antichain proof relies on a construction that Emit_K's specification does not enforce
Reason: The fix turns on whether flat-link-domain is a designed substrate guarantee or an implementation discipline. Nelson tells us whether the link model intends prefix-incomparability among link addresses; Gregory tells us whether the udanax-green emission path is forced into sibling-frontier deposits or merely happens to land there.
Nelson question: Does Nelson's link model intend that no link address ever be a prefix of another — i.e., is the flat-link-domain property a designed semantic constraint, or an emergent consequence of the allocator's implementation?
Gregory question: Does udanax-green's link-emission path (`docreatelink` / the `LINKATOM` branch of `findisatoinsertmolecule`) ever deposit a link at an address that is a tumbler-prefix-descendant of an existing link, or is it structurally constrained to sibling-frontier positions only?

## Issue 2: Nullify's single-tuple scope inherits Issue 1's fragility
Reason: The fix branches from Issue 1's resolution — either inherit the strengthened Emit_K spec or add an explicit precondition. Whether Nullify was intended as a single-tuple primitive (vs. a subtree retraction) is design intent, so Nelson disambiguates the intended shape; Gregory's input on Issue 1 already covers the implementation side.
Nelson question: Was retraction in Nelson's design intended to nullify exactly one tuple at a time, or was subtree-broad retraction (via a deliberately broader to-span) a designed feature of the retraction primitive?

## Issue 3: R0 Step 4's "Remaining L-invariants" paragraph is grouped by one-line orthogonality assertion
Reason: Each of L2, L4–L10, L13, L14 is defined in ASN-0043 (this ASN's dependency); per-invariant reasoning is mechanical expansion using definitions already in scope. No external channel required.

## Issue 4: R0 Step 2 Case B cites T10a's at-most-once discipline for sibling-sweep pairs that T10a does not bind
Reason: T10a's axiom, T10a.7 (EnumerationInjectivity), and L12 (LinkImmutability) are all in the ASN's dependency closure (ASN-0034, ASN-0043). The reviewer has identified the correct replacement citation; the fix is a citation correction derivable from existing dependency content.

## Issue 5: "Every transition in `→` is one of (i)–(iii)" is too strong relative to the underlying transition vocabulary
Reason: Arrangement-extending transitions (INSERT and similar) are specified in ASN-0036/ASN-0058, both in this ASN's dependency closure. The fix — qualify `→` as the dom-extending substrate emissions on `(Σ.C, Σ.M, Σ.L)` and note that arrangement modifications live in a parallel transition vocabulary — is derivable from the existing scoping conventions of the underlying ASNs.
