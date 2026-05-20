# Channel Assignment — ASN-0047 review-124

**Date:** 2026-05-19 18:09

## Issue 1: Properties Introduced table — inconsistent frame descriptions
Reason: Pure internal consistency — the body already states the extended-state frames; the table just needs to be updated to match. No design intent or implementation evidence needed.

## Issue 2: K.μ~ matrix entries terse for S8★ and several other invariants
Reason: Expository expansion using mechanisms already established in the ASN (link-subspace fixity via full-clearance form, trivial length-1 decomposition). Derivable from the ASN's own content.

## Issue 3: NodeRegistryBootstrap vs NodeUniqueAllocation clause (c) redundancy unclear
Reason: Structural clarification of two axioms already present. The derivation chain (no prior K.δ event for n₀ at Σ₀, so clause (c)'s inductive form requires a base case) is internal to the ASN's logic.

## Issue 4: K.μ⁻ "Per-subspace consequence of the effect clause" — empty subspace handling
Reason: Case-analysis expansion of an existing derivation, using only invariants (D-CTG★, D-MIN★, D-SEQ★) and the effect clause already in the ASN.

## Issue 5: Worked example "fork with subsequent insertion" — incomplete invariant verification on d₂
Reason: Adding explicit verification lines for invariants already specified in the ASN against V-positions chosen in the example. No external consultation needed.

## Issue 6: K.δ k=1 case dispatch hidden in discharge
Reason: Clarifying note distinguishing operational uniformity from verification-route case-split — both already present in the ASN. Internal exposition.

## Issue 7: J1' description predates extension; relationship to J1'★ could be clearer
Reason: Table annotation update; J1'★ is already defined in the ASN as the scoped form. Mechanical labelling fix.
