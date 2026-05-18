# Channel Assignment — ASN-0047 review-85

**Date:** 2026-05-17 18:20

## Issue 1: Forward-reference accretion — "defer to this canonical site" markers
Reason: Editorial cleanup of meta-prose cross-reference bookkeeping. Derivable from the ASN alone — no design-intent or implementation evidence needed.

## Issue 2: Defensive justification of SubspaceConventionAxiom
Reason: Removing essay-style motivation around an existing axiom statement. The axiom and its citations stand on their own; no external evidence required.

## Issue 3: Defensive justification of SubAllocatorAxiom
Reason: Removing a single sentence of why-axiomatic reasoning. Pure editorial compression, derivable from the ASN.

## Issue 4: L3 local-extension consistency paragraph
Reason: Removing a hypothetical-future paragraph about what a downstream ASN-0043 amendment would entail. No current design or implementation question — purely meta-prose about future ASNs.

## Issue 5: Redundant notation for the same projection
Reason: Pick-one editorial decision among `E(a)`, `fields(a)`, `subspace_I(a)`. Foundation notation already exists (ASN-0034 T4b); the choice can be made from the ASN's own usage patterns.

## Issue 6: Imprecise analogy in K.μ~ classification
Reason: Editorial precision — the analogy "to J0/J1★/J2/J3/J4" lumps couplings, isolation properties, and a composite definition. Fix derivable by inspecting how each J-label is defined in the ASN.

## Issue 7: Use-site inventory in V-ordering definition
Reason: Remove four-item use-site inventory from a definition preamble. Editorial cleanup; consumers cite the definition naturally without an upstream announcement.

## Issue 8: Defensive justification of P3★ in Properties Introduced
Reason: Remove bookkeeping sentences explaining where the prose ancestor appears and what role P3★ plays in proofs. The predicate itself stands; derivable from the ASN.

## Issue 9: Defensive prose around the entity-allocator-tracked predicate
Reason: Remove essay-style justification after the predicate definition; relocate the Path 1/2/3 split content to K.δ where it's consumed. Internal reorganization derivable from the ASN.

## Issue 10: Ghost-base versioning canonical-site framing
Reason: Strip "canonical site" labeling and closing cross-reference notice. Editorial cleanup; the deferral list itself can stay or move to Open Questions, derivable from the ASN.

## Issue 11: Repetition of "see the canonical X site"
Reason: Compress cross-reference accretion to terse inline pointers. Editorial pattern-replacement derivable from the ASN.

## Issue 12: Document-ordering justification in proof structure
Reason: Tighten partition prose so each invariant's class assignment is one line. The discharge content (J1★/J1'★ at composite boundary) is already stated elsewhere; this is compression derivable from the ASN.

## Issue 13: Multi-paragraph axiom prose without separation between content and rationale
Reason: Relocate "Dispatch of freshness obligations" content from SubAllocatorAxiom to K.α and K.λ use sites. Internal reorganization derivable from the ASN.

## Issue 14: Missing intermediate-state P4★ check in interior-replacement example
Reason: Add one verification line showing P4★ violated at post-K.μ⁺ pre-K.ρ intermediate, restored at K.ρ boundary. Derivable from the ASN's own P4★ definition and the elementary frames of K.μ⁺ and K.ρ.

## Issue 15: Bootstrap node single-tree decision under-examined
Reason: The single-tree commitment (NodeLineage forcing `n₀ ≼ e`, ruling out `[2]`, `[2,1]`, etc.) is presented as a "definitional convention" but corresponds to a substantive design choice about server federation. Need Nelson on whether Literary Machines commits to single-root vs. multi-server federation; need Gregory on whether the granfilade structure hardcodes a single bootstrap or supports multi-root.
Nelson question: Does Literary Machines commit the docuverse to a single-rooted tree (one bootstrap server address from which all node addresses descend), or does the design admit multiple coexisting roots for federated servers each owning a disjoint node-address subtree?
Gregory question: Does the udanax-green granfilade allocator hardcode a single bootstrap node address (e.g., `[1]`), or does it admit multiple sibling root nodes — and if the latter, by what mechanism are cross-root collisions prevented?
