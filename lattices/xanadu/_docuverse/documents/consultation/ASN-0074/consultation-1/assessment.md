# Revision Categorization — ASN-0074 review-1

**Date:** 2026-03-22 14:48

## Issue 1: Non-foundation cross-reference to ASN-0047
Category: INTERNAL
Reason: The fix is editorial — restate E_doc locally and drop unused R. The needed definitions exist in ASN-0047 and just need to be restated or grounded in existing foundation properties.

## Issue 2: V-ordering of resolution output incorrectly attributed to B1
Category: INTERNAL
Reason: The correct derivation (resolve orders by V-start by definition; B2 disjointness makes this well-defined) uses only properties already present in ASN-0058. This is a miscitation fix.

## Issue 3: Implementation reference in abstract specification
Category: INTERNAL
Reason: The fix is to remove the implementation paragraph from the formal body. The V-ordering is already established by the definition of resolve and B2; no implementation evidence is needed to justify it.

## Issue 4: C1 derivation omits the B3 link
Category: INTERNAL
Reason: The missing chain (B3 identifies each aⱼ + i as M(d_s)(vⱼ + i), then S3 places it in dom(C)) uses only properties already cited in the ASN. The derivation steps are straightforward.

## Issue 5: C1a proof sketch miscites S2 for merge consistency
Category: INTERNAL
Reason: The correct argument (S2 for initial decomposition, case split + M-aux for merge preservation of B3) is already established in ASN-0058. This is a citation correction using existing proof structure.

## Issue 6: ContentReference definition ill-formed for empty subspace
Category: INTERNAL
Reason: Adding the precondition V_{u₁}(d_s) ≠ ∅ or redefining m is a mathematical well-formedness fix derivable from S8-depth's vacuous truth on empty sets. No external evidence needed.

## Issue 7: Implicit ordinal displacement requirement not derived
Category: INTERNAL
Reason: The argument that well-formed content references require ordinal displacements follows from D-SEQ (intermediate components forced to 1) and T0(a) (infinite range at depth ≥ 3 for non-ordinal displacements), both already in the foundation. This is a derivation to state as a lemma.

## Issue 8: No concrete example
Category: INTERNAL
Reason: A worked example can be constructed entirely from the definitions of block decomposition (ASN-0058), content reference, resolve, and C1 already present in this ASN. No external consultation needed.
