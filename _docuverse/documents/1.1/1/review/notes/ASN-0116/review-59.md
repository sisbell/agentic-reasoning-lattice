# Review of ASN-0116

This is a rigorous, well-constructed note. I checked the composite decomposition (K.α×n → K.μ⁻ → K.μ⁺ → K.ρ×n) step by step, the gapped/filled bridge against block-disjointness, the four boundary cases (empty subspace, append, front-insert with `n'_{s_C}=0` strict contraction, re-insert after full deletion with non-empty content region), the forward-merge impossibility (`shift(a,n) ∉ dom(C')` vs. `M(d)(q_J) ∈ dom(C')`), the IP4 witness-set non-comparability argument, the IP6 weakest-precondition (containment, not emptiness), and the provenance couplings (J0/J1★/J1'★ keyed on range-new addresses, with the shifted suffix correctly range-old via P4★). The mathematics holds; the depth standards (derived consequences, non-trivial wp, concrete worked example) are met or exceeded. The note cites only foundation ASNs.

I found no correctness defect. Under the active anti-bloat mode, one concrete prose redundancy remains.

## REVISE

### Issue 1: The reachability-licensing step is established twice across a section boundary
**ASN-0116, end of "INSERT as a valid composite" and opening of "The document remains one coherent sequence"**:

Composite section (final sentence): "...INSERT is a valid composite; since `Σ` is reachable from `Σ₀` (precondition), the post-state is reachable too, and the appeal to ExtendedReachableStateInvariants for its post-state is licensed."

Coherent-sequence section (opening): "INSERT is a valid composite, and `Σ` is reachable from `Σ₀` (precondition), so the post-state is reachable too. ExtendedReachableStateInvariants (ASN-0047) therefore delivers the *entire* post-state invariant set at once..."

**Problem**: The identical logical move — *valid composite + Σ reachable ⟹ post-state reachable ⟹ ExtendedReachableStateInvariants applies* — is made in both sentences. The composite section's whole purpose is to license that appeal; the coherent-sequence section then re-derives the license before using it. This is the "two paragraphs say the same thing in different words" pattern at a section seam.

**Required**: Drop the re-derivation in the coherent-sequence opener. Open directly with the use — "ExtendedReachableStateInvariants (ASN-0047) therefore delivers the entire post-state invariant set at once..." — relying on the licensing already concluded one section above.

## OUT_OF_SCOPE

None. The note scopes itself to text-subspace insertion (`S = s_C`) and routes transclusion-shared insertion points, concurrent-freshness, transclusion-provenance, and post-fragmentation contiguity to its four Open Questions rather than smuggling claims about them into the operation. The IP4/IP5/IP6 link- and document-level results are genuine consequences INSERT must preserve, not separate operations, so they belong here.

VERDICT: REVISE
