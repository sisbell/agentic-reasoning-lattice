# Channel Assignment — ASN-0091 review-75

**Date:** 2026-06-04 03:14

## Issue 1: Mis-citation in clause (iv) subspace-preservation discharge
Reason: Internal — the ASN already states R-PRE(iv) means "the affected range {v : c₀ ≤ v < c_{n−1}} must lie in V_S(d)" (in the empty-case discussion and the witness derivations), so the correct ground for affected-range positions carrying subspace S is already present in the ASN. The fix is a citation swap derivable from the ASN's own content.

## Issue 2: Vacuously-conditioned prose hedges a case CS3 already fixes
Reason: Internal — the ASN repeatedly asserts CS3 fixes S = s_C for every REARRANGE_K invocation (e.g., the clause (v) row reads "by CS3 the cut subspace is S = s_C"), so the antecedent is provably always-true from the ASN itself. Stating the consequence unconditionally needs no external channel.

## Issue 3: Constant "Status" column carries no information
Reason: Internal — purely editorial restructuring (dropping a uniform column and relocating an in-table justification into the prose where RA-frame is discharged). No design intent or implementation evidence is required.
