# Review of ASN-0043

## REVISE

### Issue 1: GlobalUniqueness listed as "introduced" — already established in foundation

**ASN-0043, Properties table and "Home and Ownership" section**: "GlobalUniqueness | LEMMA | No two allocation events produce the same address — extends S4 (OriginBasedIdentity, ASN-0036) beyond I-addresses via T9, T10, T10a, TA5, T3 (ASN-0034) | **introduced**"

**Problem**: ASN-0034 already establishes GlobalUniqueness (UniqueAddressAllocation): "For any `a, b ∈ T` produced by distinct allocation events within a system conforming to T10a: `a ≠ b`. This holds regardless of whether the events originate from the same allocator, sibling allocators at the same level, or allocators at different hierarchical levels." This is universally quantified over all allocation events — it carries no subspace restriction and already covers link addresses. The ASN re-derives it via an indirect analogy argument ("the three foundation axioms underlying S4's derivation..."), then lists it as "introduced" in the properties table. This is reinventing a foundation result.

**Required**: (1) Remove GlobalUniqueness from the properties table — it is not introduced by this ASN. (2) In the body, replace the multi-paragraph re-derivation with a direct citation: "By GlobalUniqueness (UniqueAddressAllocation, ASN-0034), no two allocation events produce the same address. Link addresses are produced by allocation events conforming to T10a (via L1a). Therefore each link receives a globally unique address." (3) L11a should cite GlobalUniqueness (ASN-0034) directly rather than via the ASN's own re-derived property.

### Issue 2: Missing element field depth constraint for link addresses (S7c analog)

**ASN-0043, "Link Ontology" throughout**: No analog of S7c (`(A a ∈ dom(Σ.C) :: #fields(a).element ≥ 2)`) is declared for link addresses.

**Problem**: Without a minimum element field depth for link addresses, a conforming state may contain a link at element field depth 1 — e.g., `d.0.s_L` with element field `[s_L]`. At depth 1, sibling allocation via `inc(·, 0)` advances the only element-field component, producing `d.0.(s_L + 1)` — an address in subspace `s_L + 1`, not `s_L`. L0 prevents this from being a link address, so the document is limited to one link at depth 1 and must descend to depth 2 for further allocation. This creates a degenerate regime where the first link address is a dead-end for sibling production.

The deeper issue parallels ValidInsertionPosition (ASN-0036): at depth 1, `shift([s_L], 1) = [s_L + 1]`, crossing subspace boundaries. The minimum depth `m ≥ 2` ensures the subspace identifier is preserved under ordinal shift (since `δ(n, m)` has action point `m > 1`, so TumblerAdd copies component 1 unchanged). The worked example implicitly assumes depth 2 (`a = 1.0.1.0.1.0.2.1`, element field `[2, 1]`), but this is not formalized.

**Required**: Add an invariant (call it L1b or similar):

`(A a ∈ dom(Σ.L) :: #fields(a).element ≥ 2)`

with the justification that depth ≥ 2 ensures sibling allocation via `inc(·, 0)` operates on the ordinal component (position `#fields(a).element`), not the subspace identifier (position 1), keeping all siblings within subspace `s_L`. This mirrors S7c and aligns with the worked example's implicit assumption.

## OUT_OF_SCOPE

### Topic 1: PrefixSpanCoverage belongs in tumbler/span algebra

PrefixSpanCoverage — `coverage({(x, δ(1, #x))}) = {t ∈ T : x ≼ t}` — is a property of spans and tumbler prefix structure, not of links. It is used here by L9 and L10 but is equally relevant to any ASN that reasons about span coverage over prefix-delimited subtrees. A future span algebra ASN should absorb it.

**Why out of scope**: The lemma is correctly proven and used within this ASN. Its organizational home is a future concern, not an error in ASN-0043.

### Topic 2: Link arrangement semantics

The ASN notes that S3 (ReferentialIntegrity) restricts `Σ.M(d)` mappings to `dom(Σ.C)`, and L0 gives `dom(Σ.L) ∩ dom(Σ.C) = ∅`, so no arrangement can map a V-position to a link address. Yet Gregory's implementation places links in V-positions within a dedicated subspace of the document's permutation matrix. The abstract model has no mechanism for link visibility, ordering within a document, or "deletion" (removal from arrangement while preserving the link entity). This requires extending the arrangement semantics — a topic for a future ASN on link operations or arrangement generalization.

**Why out of scope**: The ASN explicitly scopes out operations, V-space effects, and the three-layer deletion model. The arrangement gap is a consequence of that scope boundary, not an error in the static ontology.

VERDICT: REVISE
