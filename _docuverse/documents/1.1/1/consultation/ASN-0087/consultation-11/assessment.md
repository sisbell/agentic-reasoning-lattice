# Channel Assignment — ASN-0087 review-11

**Date:** 2026-05-26 14:14

## Issue 1: K.σ vs K.δ-IsDocument reconciliation is asserted, not derived
Reason: The fix is a notational/formal choice among three options (supersession, extension, or invariant addition) made within the ASN system itself. Both K.σ (ASN-0093) and K.δ-IsDocument (ASN-0047) are formally specified; the author needs to pick a reconciliation strategy and apply it consistently, requiring no external evidence about design intent or implementation.

## Issue 2: L1c chain uniqueness argument uses an underived "structural target"
Reason: The fix is to cite the correct lemma — K.λ's emission precondition restricting ℓ to A_L(d) outputs, combined with ChainUniformLength (ASN-0093) and ChainMembershipForOrigin (ASN-0093). All required lemmas are already in foundation ASNs that ASN-0087 builds on; this is a citation correction internal to the formal system.

## Issue 3: Σ_mid invariant analysis is selective, not comprehensive
Reason: The fix is to explicitly note that K.λ's frame gives `Σ_mid.M = Σ.M` and `Σ_mid.C = Σ.C`, discharging all M-side and C-side per-state invariants by inheritance from Σ. This is a structural inheritance argument derivable directly from K.λ's definition; no external evidence needed.

## Issue 4: "Standard authoring" is used as a hypothesis without being defined
Reason: The fix is to introduce a formal definition like `StandardAuthoring(e, Σ) ≡ (A (s, ℓ) ∈ e :: coverage({(s, ℓ)}) ⊆ dom(Σ.C) ∪ dom(Σ.L))` and cite it uniformly. The predicate is constructed entirely from existing substrate definitions (coverage, dom(C), dom(L)) already used in the ASN.

## Issue 5: Cross-document discovery cascade is not analyzed
Reason: The fix invokes only existing lemmas — LP9 (ExtensionMonotonicity), LP13 (LinkPermanence), L12 (LinkImmutability) — to argue that cascades cannot violate preserved invariants because discoverability is a derived predicate rather than state. The boundedness argument is internal to the formal system.

## Issue 6: M-Inv-Bdry's vacuity claim for J0, J1★, J1'★ could be tighter
Reason: The fix is to discharge J0 by `dom(Σ'.C) \ dom(Σ.C) = ∅` (universe-emptiness) and J1★/J1'★ by `subspace(v_ℓ) = s_L ≠ s_C` (subspace exclusion), separating the two structural reasons. Both arguments use definitions already established in ASN-0047 and the ASN's own effect specification.
