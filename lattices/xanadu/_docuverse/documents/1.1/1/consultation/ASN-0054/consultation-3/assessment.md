# Revision Categorization — ASN-0054 review-3

**Date:** 2026-03-20 00:18

## Issue 1: A0 invariant category and K.μ⁻ gap
Category: INTERNAL
Reason: The ASN already contains both the per-elementary claim and the composite-level acknowledgment ("intermediate states within a composite may temporarily violate A0"). The fix is reclassifying A0 as a composite-boundary invariant and adjusting the formal mechanism text — all information needed is present in the ASN and ASN-0047.

## Issue 2: V(d) uniform depth relies on unstated single-subspace assumption
Category: INTERNAL
Reason: The ASN itself provides the infinite-chain argument (used in A1) that forces V(d) into a single subspace. The fix is reordering the derivation — either restricting the definition to v₁ = 1 or stating the single-subspace invariant before introducing L(d). No external evidence is needed.

## Issue 3: Worked example invokes zero displacement
Category: INTERNAL
Reason: The main text already states the correct convention ("At i = 0 no displacement arithmetic is needed — the base case is the definition of a_s"). The fix is aligning the worked example with this convention.

## Issue 4: A6 partition cites wrong property
Category: INTERNAL
Reason: The correct justification — maximal break-free intervals of a contiguous index set partition it by construction — is already implicit in the ASN's run construction. The fix replaces an incorrect citation with reasoning already present in the text.

## Issue 5: A12 equality condition omits V-span width
Category: INTERNAL
Reason: The ASN already establishes that I-span width encodes run length r_j (A7) and that V-span width is determined by r_j and depth L(d). The fix is making this implicit step explicit with a one-line note.
