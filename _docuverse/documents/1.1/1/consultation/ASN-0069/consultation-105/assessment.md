# Channel Assignment — ASN-0069 review-105

**Date:** 2026-06-03 02:49

## Issue 1: V9a lists "direct allocation" as an indistinguishable acquisition path, contradicting V9b
Reason: Both properties are defined and proved within the ASN; reconciling V9a's enumeration against V9b's proven `origin(a) ≠ d_new` for fork-recorded pairs is a matter of internal scope/wording, requiring no design intent or implementation evidence.

## Issue 2: T4-validity of `d_new` is established twice by independent routes
Reason: Both derivations (B6(a) and T10a.4) and the citation convention are entirely internal to the ASN; collapsing the redundant second derivation into a citation of the first is a self-contained editorial fix.
