# Channel Assignment — ASN-0051 review-22

**Date:** 2026-05-15 20:19

## Issue 1: SV0 is a definitional unfolding presented as a theorem
Reason: The fix is internal — locate(e, d) is defined as `{v ∈ dom(M(d)) : M(d)(v) ∈ coverage(e)}`, which makes the input dependency a definitional consequence. The author can choose among reframing as observation, strengthening to an architectural claim, or dropping SV0, all using material already in the ASN.

## Issue 2: SV6's proof requires explicit handling of the zeros(t) = 3 constraint
Reason: The fix is internal — it is a pure proof-gap closure. The added step "zeros(t) = 3 with three zeros already at p₁, p₂, p₃ forces no other zeros" is a direct logical consequence of the hypothesis already in the proof statement.

## Issue 3: SV11 conflates "fragment" definition with decomposition terms
Reason: The fix is internal — distinguishing "decomposition terms" (the m·p union terms) from "fragments" (maximal contiguous subsequences) is a terminological cleanup. Both concepts and their relationship are derivable from definitions already present in the ASN.

## Issue 4: SV1 and SV12 are foundation citations, not new theorems
Reason: The fix is internal — relabeling SV1 and SV12 as corollaries or framing prose around the substantive SVs is a structural editing decision. The foundation invariants (L12, S0) being cited are already established in their parent ASNs.

## Issue 5: Empty endset edge cases under-treated
Reason: The fix is internal — the asymmetric empty cases follow mechanically from the disjunction structure of BilateralVitality; `coverage(∅) = ∅` gives `π(∅, d) = ∅` directly; and the `(∅, ∅, Θ)` case is already characterized in the ASN. The additional paragraph is elaboration, not new content.

## Issue 6: K.μ⁺_L's interaction with link-referencing endsets needs depth
Reason: The fix is internal — L4 (EndsetGenerality) and L13 (ReflexiveAddressing) are already cited and establish that endsets may reference link addresses. The projection π and locate are uniformly defined across subspaces; π_text in SV11 is explicitly subspace-restricted. Either splitting SV2 or adding a clarifying note can be done from material already present, with the deeper link-subspace treatment correctly deferred to a future ASN as the ASN itself notes.

## Issue 7: K.λ's effect on existing links not explicit
Reason: The fix is internal — K.λ holds M in frame (established by its frame condition in ASN-0047) and SV9 already covers new-link discoverability. Consolidating these two facts into one explicit statement requires no new material.

## Issue 8: wp analysis is implicit but not stated
Reason: The fix is internal — the wp formulations the reviewer requests are direct logical rearrangements (negations or contrapositives) of the forward implications already proven in SV2–SV5 and SV11. The "vitality loss condition" prose in the SV3 discussion is already in essentially wp form; making this explicit requires no new content.
