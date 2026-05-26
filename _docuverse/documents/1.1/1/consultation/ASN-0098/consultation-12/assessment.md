# Channel Assignment — ASN-0098 review-12

**Date:** 2026-05-25 23:57

## Issue 1: C0 (ASN-0058) appeal in tightness achievability does not apply to endset spans
Reason: Internal proof-structure fix. The review identifies the canonical construction's specification (ordinal-displacement spans) and proposes deriving `k_ℓ = #s` directly from OrdinalDisplacement (ASN-0034) — both citations are already in the ASN's dependency graph and need no external evidence.

## Issue 2: Induction in descendant/ancestor cases is vestigial
Reason: Pure proof-form issue — collapse vestigial induction into direct proof using M0 + Prefix + zero-count balance, all of which are already cited and used in the base case. No design or implementation evidence needed.

## Issue 3: K.δ remark hand-waves subsumption by LP8
Reason: Reference-frame clarification internal to the ASN's own setup; the working-reference-frame paragraph already declares "ASN-0047 transition-model frame layered over ASN-0093 allocation substrate," and the resolution is to make explicit which document-registration operation is canonical and how the other fits. Derivable from re-reading ASN-0047 and ASN-0093.

## Issue 4: Cross-chain achievability setup assumes specific span-endpoint chain
Reason: Pure case-enumeration exposition — split is along span-endpoint chain choice plus interfering-chain relation. Both axes are determined by the chain structure already established in ASN-0093 and cited within the ASN.

## Issue 5: Tightness predicate's universal quantifier over infinite F
Reason: Internal mathematical lemma — finitude of `F ∩ [s, s ⊕ ℓ)` follows from T1 comparison bounds on length and divergence-position component values, both of which are in ASN-0034 and already used elsewhere in the ASN's proofs.

## Issue 6: LP9 K.μ⁺_L freshness derivation duplicates ASN-0047 effect-clause work
Reason: Corpus-integration question — whether ASN-0047 already discharges `v_ℓ ∉ dom(M(d))` as a lemma, or whether ASN-0098 owns the derivation. Resolvable by inspecting ASN-0047's K.μ⁺_L proofs directly.

## Issue 7: Worked trace's e₂ construction not exhibited
Reason: Pure expository fix — exhibit a concrete span (e.g., `e₂ = {(i₁, δ(1, #i₁))}`) and verify the intersection. T12 (ASN-0034) and L4 (ASN-0043) are already cited in the ASN and suffice.

## Issue 8: "F" definition uses notation that elides T4-validity check
Reason: Internal proof-structure fix — either derive T4-validity of `a = [d, 0, s, k]` from T4's components (already in ASN-0034) or cite ASN-0093's existing chain-element-T4-validity lemma. Both sources are dependencies of the ASN.

## Issue 9: LP4 hypothesis `Σ'.M(d) = Σ.M(d)` requires both `d ∈ dom(Σ.M)` and `d ∈ dom(Σ'.M)`
Reason: Pure proof-statement clean-up — add explicit `d ∈ dom(Σ.M) ∩ dom(Σ'.M)` precondition or document the M1 dependency. No external channel needed; the choice is editorial.

## Issue 10: Range of `subspace(v)` in LP20 corollary not fully bounded
Reason: Internal clause addition — partition-completeness follows directly from S3★-aux (SubspaceExhaustiveness, ASN-0047), which is already cited in the corollary's argument.
