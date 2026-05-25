# Channel Assignment — ASN-0098 review-2

**Date:** 2026-05-24 19:38

## Issue 1: K.δ reference inconsistent with the state model in use
Reason: The fix is a choice between two cited ASNs already in the spec corpus (ASN-0093 vs ASN-0047). The author can resolve internal consistency by picking one model and aligning all references to it.

## Issue 2: K.ρ from ASN-0047 not addressed
Reason: K.ρ's frame (preserving M) is defined in ASN-0047, already accessible to the ASN. The fix is a one-line lemma derivable from LP4 applied to K.ρ's frame.

## Issue 3: Multi-step composition left implicit in LP18 and LP19
Reason: Purely a proof-technique fix — introducing star-corollaries via induction over per-step versions. Pattern is established in ASN-0040 and derivable from the ASN's own content.

## Issue 4: LP11 reverse inclusion not made explicit
Reason: Proof-completeness fix — the missing step uses bijectivity already stated in the proof. Internal to the ASN's existing reasoning.

## Issue 5: `discoverable_from` definition presupposes `a ∈ dom(Σ.L)` implicitly
Reason: Definition precondition fix, parallel to how `project` already conditions on `d ∈ dom(Σ.M)`. Internal.

## Issue 6: Worked trace's K.μ~ example does not illustrate projection motion
Reason: Editorial fix to the example — modify coverage or add per-V-position rebinding. Derivable from LP11's own statement.

## Issue 7: "Tight at state Σ_e" prose conflicts with formal definition
Reason: Editorial choice between dropping the parenthetical or tightening the formal definition. Review recommends the former; internal decision.

## Issue 8: Numbering gaps unexplained
Reason: Editorial fix — renumber or footnote. Internal to the ASN's presentation.

## Issue 9: "Claims Introduced" table omits `discoverable_from`
Reason: Table completeness fix. Internal.

## Issue 10: Informal text about K.α boundary insertion uses "typically" without anchoring
Reason: Forward-reference fix to align prose with LP19. Internal to the ASN's existing structure.
