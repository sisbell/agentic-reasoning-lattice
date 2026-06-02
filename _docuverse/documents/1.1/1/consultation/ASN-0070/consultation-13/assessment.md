# Channel Assignment — ASN-0070 review-13

**Date:** 2026-06-02 14:53

## Issue 1: F-contig lacks a formal contract block
Reason: Purely a presentation-consistency fix. The lemma is already fully proved inline with its dependencies (M1, T12) named in prose; reformatting it into the standard Preconditions/Postcondition/Depends/Frame block is derivable from the ASN's own content.

## Issue 2: Incorrect citation name for the home definition
Reason: A citation-accuracy fix internal to the spec corpus. The correct definition name lives in ASN-0043, a foundation note, not in design intent (Nelson) or the udanax-green implementation (Gregory); the fix is to align the label with ASN-0043's actual "Home" definition.
