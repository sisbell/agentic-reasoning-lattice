# Channel Assignment — ASN-0112 review-58

**Date:** 2026-06-10 23:24

## Issue 1: The exactness discriminator is a real claim but is unlabeled and absent from Claims Introduced
Reason: The biconditional `extent_d₁ = 0 ⟺ Exact` and its full two-case derivation already exist in the ASN's prose; the fix is registering it as a labeled claim row (or folding it into V5/V6), which is purely structural. No design intent or implementation evidence is required.

## Issue 2: Defensive parenthetical in V3 — meta-prose about a construction the claim disowns
Reason: The fix is an editorial trim of a defensive aside the claim itself disowns, with optional relocation of the attainability question to Open Questions. Everything needed (V3's order-theoretic scope, the parenthetical's single useful kernel) is in the ASN's own text.

## Issue 3: "occupied-depth position" is load-bearing but never defined
Reason: The definition is constructible from machinery the ASN already imports (`m_S(d)`, `V_S(d)`, S3★-aux), and the review confirms both candidate readings preserve V5's proof and V6's witness — so choosing and stating the definition, then checking consistency, is an internal formalization decision, not a design-intent or implementation question.
