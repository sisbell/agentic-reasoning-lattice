# Channel Assignment — ASN-0043 review-54

**Date:** 2026-05-13 11:21

## Issue 1: L9 case (ii) — carrier root zeros assumption is unjustified
Reason: The fix is a proof-mechanic adjustment — qualify L9's quantification, add a sub-case for zeros(r) = 3, or declare an explicit precondition. All three options are derivable from L9's existing structure, ASN-0034's T10a, and L1a (which already ties dom(Σ.L) to dom(Σ.M)). No design-intent or implementation evidence is needed.

## Issue 2: L8 — same_type equivalence properties not derived
Reason: The three properties (reflexivity, symmetry, transitivity) follow directly from set equality on coverage. Pure proof-completion task, fully internal to L8.

## Issue 3: L10 — hierarchy inclusion not derived
Reason: The inclusion lemma `p₁ ≼ p₂ ⟹ subtypes(p₂) ⊆ subtypes(p₁)` follows from transitivity of ≼ (already established in ASN-0034's PrefixRelation). Pure proof-completion task, fully internal.

## Issue 4: L11a — bundles two distinct claims under one label
Reason: This is a structural reorganization of L11a — split into uniqueness (cleanly from GlobalUniqueness via L1c) and either drop the permanence statement or restate as a corollary of L12. The fix involves only the ASN's own labeling and dependency graph.

## Issue 5: L7 — DirectionalFlexibility asserted without scan argument
Reason: The fix requires scanning the enumerated invariants L0–L14, L-fin for directional vocabulary. All invariants are defined within this ASN and are inspectable directly. No external channel needed.
