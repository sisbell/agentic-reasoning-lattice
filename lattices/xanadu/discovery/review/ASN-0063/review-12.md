# Review of ASN-0063

## REVISE

### Issue 1: P4★ K.μ~ preservation — compressed derivation

**ASN-0063, Containment scoping**: "K.μ~ preserves P4★ by the link-subspace fixity established in the S3★ analysis above — π maps content-subspace positions to content-subspace positions with values preserved, so Contains_C(Σ') = Contains_C(Σ) ⊆ R = R'."

**Problem**: This sentence compresses two inference steps that should be explicit. First, "π maps content-subspace positions to content-subspace positions" is derived from the link-subspace fixity (π maps link→link) by complement under the full bijection — a step that is unstated. The fixity argument above establishes π(dom_L) = dom_L; the content→content claim follows because π is a bijection on all of dom(M(d)), so π(dom(M(d)) \ dom_L(M(d))) = dom(M'(d)) \ dom_L(M'(d)). Second, the jump from "content→content with values preserved" to "Contains_C(Σ') = Contains_C(Σ)" relies on the fact that a value-preserving bijection on positions preserves the *set* of reachable I-addresses — that is, ran(M'(d)|_{s_C}) = ran(M(d)|_{s_C}). Each step is elementary, but each is a distinct inference that the current text elides.

**Required**: Make both steps explicit. After the fixity argument, state: "Since π bijects dom(M(d)) onto dom(M'(d)) and maps dom_L bijectively onto dom_L (by fixity), it maps the complement dom_C(M(d)) bijectively onto dom_C(M'(d)) — content-subspace positions to content-subspace positions. With M'(d)(π(v)) = M(d)(v) for each such v, the set {a : (E v ∈ dom_C(M(d)) : M(d)(v) = a)} = {a : (E u ∈ dom_C(M'(d)) : M'(d)(u) = a)}, so Contains_C is unchanged for d."

### Issue 2: J4 fork consequence — missing verification that fork remains a valid composite

**ASN-0063, Extending the Transition Framework**: "A consequence for J4 (Fork, ASN-0047): since J4's K.μ⁺ step is now restricted to content-subspace V-positions, forking a document populates only the content subspace of the new document."

**Problem**: The ASN amends K.μ⁺ and introduces new coupling constraints (J1★, J1'★ replacing J1, J1'). It states a consequence for J4 but does not verify that J4 remains a valid composite under the amended framework. Specifically: J4's step (iii) K.ρ records provenance for each a ∈ ran(M'(d_new)). Under the amendment, ran(M'(d_new)) ⊆ dom(C) (since K.μ⁺ requires a ∈ dom(C)). J1★ is satisfied because K.μ⁺ creates content-subspace positions and K.ρ records provenance. J1'★ is satisfied because every new provenance entry (a, d_new) corresponds to a content-subspace extension. The derivation is straightforward but absent — the ASN states the structural consequence (link subspace starts empty) without verifying the coupling constraints hold.

**Required**: Add a brief verification that J4 satisfies J1★ and J1'★ under the amended framework: J1★ is satisfied because J4's K.μ⁺ creates content-subspace positions and J4's K.ρ records provenance for each; J1'★ is satisfied because each new (a, d_new) ∈ R' has a ∈ ran(M'(d_new)) from content-subspace extensions. Three sentences suffice.

## OUT_OF_SCOPE

### Topic 1: Link inheritance under forking
**Why out of scope**: The ASN correctly identifies that forking does not copy link-subspace mappings and defers a link inheritance mechanism to future work. This is new territory requiring its own design decisions (which source links to inherit, how to handle link-subspace population in the fork composite).

### Topic 2: Link withdrawal invariants
**Why out of scope**: The ASN identifies that K.μ⁻ applied to interior link-subspace positions violates D-CTG and K.μ~ cannot close the gap (link-subspace fixity). The withdrawal mechanism requires new design — potentially an inactive status rather than arrangement removal. This is a separate operation, not a gap in CREATELINK.

### Topic 3: Finite link store as explicit invariant
**Why out of scope**: The ASN argues dom(L) is finite in every reachable state (L₀ = ∅, each K.λ adds one entry, all others hold L in frame). This operational argument is correct but could be stated as a formal invariant analogous to S8-fin for arrangements. A future ASN consolidating link-store properties would be the natural home.

VERDICT: REVISE
