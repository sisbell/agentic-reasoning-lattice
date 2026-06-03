# Channel Assignment — ASN-0087 review-19

**Date:** 2026-06-03 14:32

## Issue 1: S7d is misclassified as content-quantified
Reason: The ASN already states what S7d concerns (document allocation discipline over `dom(M)`) and that `dom(Σ'.M) = dom(Σ.M)`; reclassifying S7d under document-set preservation is derivable from the ASN's own body, which justifies M0 the same way.

## Issue 2: M-Inv-State table miscategorizes M0 and S7d, contradicting the body
Reason: This is an internal reconciliation between the summary table and the body, which already correctly justifies M0 via unchanged `dom(M)`; adding an M-frame category requires no external evidence or design intent.

## Issue 3: "Vacuous" misused for invariants preserved by inheritance over nonempty domains
Reason: Purely a terminology correction (vacuous vs. preserved-by-inheritance) resolvable from the ASN's own frame reasoning; no design intent or implementation evidence is needed.

## Issue 4: `m_L(d)` referenced where it is undefined in the K.μ⁺_L precondition
Reason: The ASN itself states `m_L(d)` is well-defined only while `V_{s_L}(d) ≠ ∅` and that M-DepthConv fixes the empty-subspace depth at 2; restating the branch as `#v_ℓ = 2` is internally derivable.
