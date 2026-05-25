# Channel Assignment — ASN-0075 review-3

**Date:** 2026-05-25 13:57

## Issue 1: D-DISCR composite-boundary notation is internally inconsistent
Reason: This is a notational consistency fix within the ASN. The correct convention (bundling K.α with K.μ⁺/K.ρ via semicolons on one arrow) is already established by the worked example's Setup, and ValidComposite★ plus J0 (both in referenced ASN-0047) determine the required grouping. No external consultation needed.

## Issue 2: "Informationally equivalent to R" in D-DISCR's necessity claim is informal
Reason: This is a sharpening of a mathematical formulation. The negative result is already proven in the ASN, and the review supplies a crisp alternative phrasing in terms of predicate disambiguation that follows from the existing proof structure. No external evidence or design intent is required.

## Issue 3: D-IDENT's derived consequences cite vague "foundation invariants"
Reason: This is a citation cleanup. The review itself enumerates the specific invariants (ASN-0047 L3, P3; ASN-0036 S2, S3★, S0/P0, S7) that need to be named for each consequence. The fix is mechanical substitution against already-existing referenced ASNs.

## Issue 4: K.α-uniformity argument cites GlobalUniqueness for a property GlobalUniqueness does not establish
Reason: This is a citation correction internal to the ASN. The K.α first-emission rule's determinism (a function of d alone) is established in the foundation, and replacing the GlobalUniqueness citation with a direct appeal to that determinism is derivable from the existing rule statement. No external consultation needed.
