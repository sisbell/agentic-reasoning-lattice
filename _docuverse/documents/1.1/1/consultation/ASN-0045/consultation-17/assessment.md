# Channel Assignment — ASN-0045 review-17

**Date:** 2026-05-28 20:02

## Issue 1: At-least-one leaps from a bound to a four-element enumeration without discreteness
Reason: The fix is a pure proof-step repair — citing NAT-discrete to enumerate the bounded ℕ segment is a standard arithmetic fact and the ASN already names its other arithmetic dependencies (T0, NAT-closure). No design intent or implementation evidence is needed.

## Issue 2: Account's rename-equivalence derivation invokes T4b and T3 but omits them from Depends
Reason: T4b and T3 are already explicitly named and used in the ASN's own rename-equivalence derivation; the fix is simply adding them to the Depends list to match the text. Fully derivable from the ASN's existing content.
