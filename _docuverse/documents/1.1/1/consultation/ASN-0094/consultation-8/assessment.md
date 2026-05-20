# Channel Assignment — ASN-0094 review-8

**Date:** 2026-05-19 22:18

## Issue 1: ShapeWellFormedness commentary contains misleading qualifier
Reason: Fix is editorial — the well-formedness rule `t_F = - ⟹ c_F = 0` already excludes `(c_F = 0|1, t_F = -)`, so "(typically)" is a verbal hedge contradicted by the ASN's own definition. Derivable internally.

## Issue 2: T_cat "finite distinguished set" terminology is incorrect
Reason: Fix is a terminology correction — the ASN's own clarifying sentence ("union of `~`-equivalence classes") supplies the correct framing. L5 (cited) gives why each class is infinite. Derivable internally.

## Issue 3: Sh-conf's effective weakest-precondition is not composed with ASN-0086's wp
Reason: Fix requires composing Sh-conf's added preconditions with ASN-0086's existing wp. The composition is straightforward and the source wp formulation is in the sibling ASN; no design-intent or implementation evidence needed.

## Issue 4: home_R introduced in worked example without allocation
Reason: Pure bookkeeping fix — add `home_R ∈ dom(Σ_0.M)` to the setup or insert a K.σ step. Derivable internally.

## Issue 5: "Sh5's mechanical-derivability claim degrades" overstates Sh5
Reason: Fix is to reword for consistency with Sh5's own META status, already documented in the ASN's Sh5 definition. Derivable internally.

## Issue 6: AllocatedAddressAntichain Case 3 — implicit use of `n_3 < #x`
Reason: Fix is to cite L1b (`#E ≥ 2`) and T4(iv) (`x_{#x} ≠ 0`), both already in the ASN's cited base (ASN-0043, ASN-0034). Derivable internally from the referenced properties.
