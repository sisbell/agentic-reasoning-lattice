# Cone Review — ASN-0034/TA3 (cycle 8)

*2026-04-18 16:42*

Looking through the ASN carefully for cross-cutting issues not already captured in Previous Findings.

### ZPD Relationship-to-Divergence used in Sub-case A2 without enumeration

**Foundation**: N/A — cross-cutting citation discipline established in TA3's own ZPD Depends entry, which enumerates ZPD uses by specific sub-case (B1 and B1–B2 bridge for the existence biconditional; B2–B4 for the first-position characterisation; "throughout Case B" for pre-zpd agreement).

**ASN**: TA3 Sub-case A2's `dₐ ≤ #a` argument: "We claim `dₐ ≤ #a`: if `a > w` by T1 case (i), T1 case (i) supplies `dₐ ≤ #a ∧ dₐ ≤ #w` (the explicit conjunction replacing `dₐ ≤ min(#a, #w)`), whose first conjunct `dₐ ≤ #a` is the bound claimed; if by T1 case (ii), `w` is a proper prefix of `a` and `dₐ` is the first `i > #w` with `aᵢ > 0`, so `dₐ ≤ #a`."

**Issue**: T1 case (i) supplies a witness position `j` (where `wⱼ < aⱼ` at the component divergence) with `j ≤ #a ∧ j ≤ #w`, not `dₐ`. The step "T1 case (i) supplies `dₐ ≤ #a ∧ dₐ ≤ #w`" presupposes the identification `dₐ = zpd(a, w) = divergence(a, w) = j`, which is exactly ZPD's Relationship-to-Divergence case (i). Similarly, the T1 case (ii) sub-branch claim "`dₐ` is the first `i > #w` with `aᵢ > 0`" is a paraphrase of ZPD's Relationship-to-Divergence case (ii) under the NAT-zero/NAT-order `≠ 0 ⟺ > 0` bridge, locating `dₐ` in the padding region past `w`'s last native position. TA3's ZPD Depends entry enumerates uses at B1, the B1–B2 bridge, B2–B4, and "throughout Case B", but does not account for Sub-case A2 — the Relationship-to-Divergence property is consumed at two Sub-case A2 sub-branches without a Depends-level accounting.

**What needs resolving**: TA3's ZPD Depends entry must extend its per-site accounting to cover Sub-case A2's use of ZPD's Relationship-to-Divergence (both the case-(i) identification `zpd(a, w) = divergence(a, w)` transporting T1 case (i)'s shared-position bound onto `dₐ`, and the case-(ii) characterisation locating `dₐ` as the first padding-region position with `aᵢ ≠ 0`), or reformulate Sub-case A2 so the bound `dₐ ≤ #a` is supplied by a postcondition already attributed.

## Result

Cone not converged after 8 cycles.

*Elapsed: 5103s*
