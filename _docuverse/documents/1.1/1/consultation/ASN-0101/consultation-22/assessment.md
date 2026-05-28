# Channel Assignment — ASN-0101 review-22

**Date:** 2026-05-28 08:30

## Issue 1: D11 cardinality wp derivation has an implicit step
Reason: The fix requires only stating two facts already present in the ASN (`Λ ∩ Π = ∅` from D8's S2 justification, `V_S(d) = Λ ⊎ X ⊎ Π` from D0's region definitions) and applying inclusion-exclusion. Derivable from the ASN's own content.

## Issue 2: D11 discoverability wp derivation has confusing prose
Reason: This is a rephrasing of existing material — the union and set-algebra identities are already in the text. No external channels needed.

## Issue 3: Worked examples do not explicitly verify D11's cross-document wps
Reason: The cross-document example already computes the required pre-state values, and D11's bullets 2 and 4 are stated in the body. The fix is mechanical instantiation of existing wp formulas against existing example data.

## Issue 4: D8 Group (ii) wholesale argument elides specific invariants
Reason: The fix requires identifying which components each Group (ii) invariant predicates over. These invariants are defined in prior project ASNs (ASN-0036, ASN-0043, ASN-0093), which the author can consult directly; this is project-internal apparatus, not a question of design intent or implementation behaviour.

## Issue 5: D0 "Justification of the reduction" — derivation depends on m_S ≥ 2 boundary
Reason: The fix is a single sentence handling `m_S = 2` using T1 ordering and the tumbler structures `s = [S, p]`, `r = [S, p+n]` already named in the derivation. Fully derivable from the ASN's own content.

## Issue 6: D8 Group (i) S3★ source-correspondence argument elides re-mapping case
Reason: The fix requires tightening prose to route S3★'s biconditional through the already-established `subspace(v) = subspace(u)` fact. All needed content is present in the ASN.
