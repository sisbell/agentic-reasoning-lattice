# Channel Assignment — ASN-0094 review-12

**Date:** 2026-05-19 23:44

## Issue 1: `latest_K_for_addr` signature mismatch with body
Reason: Pure internal consistency fix — the body's `argmax` returns a tuple in `S_d ⊆ A_K^Σ`, and the walkthrough confirms tuple-return semantics with downstream `from₁(τ_3)` access. The signature must be aligned to the tuple codomain (or the body wrapped in `addr(·)`); the choice is determined by what the walkthrough already commits to.

## Issue 2: Retraction row's base templates not formally defined
Reason: The natural reformulations under `c_F = *` are already determined by the framework's own machinery — `from_K(a) ≡ {τ ∈ A_K^Σ : a ∈ slot_addrs(F_τ)}` parallels the existing point-accessor template with set-membership in place of point-equality, and the AllocatedAddressAntichain over-approximation argument fixes `pair_K(F̂, b)`'s matching semantics as exact slot-set equality. No external input needed.

## Issue 3: T_cat lifetime constancy not explicitly stated
Reason: The induction structure forces the answer — the baseline `L_K^{Σ_init} = ∅` must hold for every `K ∈ T_cat`, and the existing "mutable shape re-registration would invalidate the induction" passage already commits the framework to static registration. Stating "T_cat is lifetime-fixed at Σ_init" (or, if dynamic, requiring `L_K^{Σ_registered} = ∅` at registration) is a clarification of an already-determined design.

## Issue 4: Direct references to non-foundation ASNs
Reason: Pure architectural cleanup within the spec system's own conventions about foundation interfaces. The fix is to route ASN-0036/0093 facts through ASN-0086's `SubstrateConformingLayer` bundle or to surface them as named scaffolding clauses; both options are entirely internal restructuring choices that do not depend on design intent or implementation evidence.

## Issue 5: Sh4 Case A enumeration omits a covered sub-case
Reason: Proof-internal enumeration completeness. The omitted sub-case (K~R with self-retraction-only) is already structurally precluded by Sh-conf clause (d) — `τ_new`'s G would target the to-be-allocated fresh address, which is not in `A_rel^Σ`. The fix is to either extend the enumeration or add the structural-exclusion note; both are derivable from the ASN's existing machinery.

## Issue 6: AllocatedAddressAntichain hypothesis under-specified
Reason: The element-level character of `A^Σ = dom(Σ.C) ∪ dom(Σ.L)` follows from L1 (ASN-0043) for the link side and the content-side scaffolding clause already declared in Scope and Substrate Scaffolding. Adding the explicit hypothesis or a parenthetical citation is a local clarification using only material already present in the ASN.
