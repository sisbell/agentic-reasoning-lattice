# Review of ASN-0093

## REVISE

### Issue 1: Intro enumeration of inherited ASN-0043 invariants omits L3
**ASN-0093, opening paragraph**: "ASN-0043 introduced the link store and its structural invariants (L0/L1/L1a/L1b/L1c/L12), of which this note restates those listed"
**Problem**: The parenthetical presents itself as the enumeration of the inherited link-store structural invariants, but L3 (NEndsetStructure) is also an inherited ASN-0043 invariant that this note restates — it appears in the *Link store invariants* section and is listed in the *Properties Introduced* table with source "ASN-0043." So the enumeration is incomplete: the body restates an invariant the intro's list doesn't name. The "of which this note restates those listed" framing reads as an exhaustive accounting that doesn't match the body.
**Required**: Add L3 to the parenthetical (`L0/L1/L1a/L1b/L1c/L3/L12`), or strike the enumeration and let the Link store invariants section carry the roster.

### Issue 2: Scope/purpose prose duplicated across intro and Scope section
**ASN-0093, intro (second paragraph)** vs **Scope, Deferred bullets**: "This note extracts the allocation-substrate layer: the three allocation primitives (K.σ, K.α, K.λ) and the structural invariants on (Σ.C, Σ.L, Σ.M) they preserve. The substrate requires no commitment to Σ.E (the entity set) or Σ.R (the provenance relation)."
**Problem**: This matches the flagged pattern "multiple paragraphs in different sections defer to the same content." The second sentence pre-states the Scope section's "Entity allocation … deferred to a higher-layer ASN" and "Provenance recording … The substrate has no R component" bullets. The first sentence restates the *Provided* line of Scope ("Three primitive operations … and the structural invariants … they preserve"). The dedicated Scope section is the canonical home for both the primitive roster and the Σ.E/Σ.R non-commitments; the intro paragraph re-announces them.
**Required**: Drop the second intro paragraph's scope/deferral content (or compress to a one-line pointer), letting Scope own the Provided/Deferred accounting. The first intro paragraph already states the substrate's subject matter.

## OUT_OF_SCOPE

### Topic 1: Local labels for instantiated ASN-0040 lemmas
The note coins `ChainElementT4Validity`, `ChainEnumerationInjectivity`, `ChainPrefixExtension`, `DisjointSubAllocatorChains` as names for ASN-0040 B6(a)/S0/S1/B7 instantiated at the sub-allocator streams. Each is explicitly sourced inline, so this is scaffolding for the instantiation rather than reinvented notation; not an error in this ASN.

VERDICT: REVISE
