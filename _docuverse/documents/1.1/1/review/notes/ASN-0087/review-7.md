# Review of ASN-0087

## REVISE

### Issue 1: S4 misattribution in invariant preservation
**ASN-0087, "Per-State Invariants at Σ'" section**: "S4 (origin-based identity): the new allocation event for ℓ is distinct from every prior allocation event (by ChainEnumerationInjectivity, DisjointSubAllocatorChains, and Cross-doc disjointness — see 'Freshness of the Allocation'), so S4's distinctness conclusion holds at Σ'."
**Problem**: S4 (ASN-0036) is explicitly about content addresses: "Preconditions: a₁, a₂ ∈ dom(Σ.C) produced by distinct allocation events..." The cited argument (chain enumeration injectivity, disjoint sub-allocator chains, cross-doc disjointness) is the L11a (LinkUniqueness, ASN-0043) derivation, which is about link addresses. ℓ is in dom(L), not dom(C); S4 does not apply to it. The actual content-address S4 is preserved trivially at Σ' since `dom(Σ'.C) = dom(Σ.C)` — no derivation needed beyond the frame.
**Required**: Either (a) re-attribute the link-distinctness argument to L11a and add a separate one-line note that S4 (content addresses) is preserved vacuously by the frame `Σ'.C = Σ.C`, or (b) replace the link-distinctness argument with the vacuous-by-frame argument for S4 and drop the link-specific citation chain.

## OUT_OF_SCOPE

### Topic 1: Composite-level atomicity at the protocol layer
**Why out of scope**: The Atomicity section correctly identifies that substrate-level transitions are atomic but the composite K.λ ; K.μ⁺_L is not, and notes "Composite-level atomicity, if required, belongs to the protocol layer above the substrate." Protocol-layer atomicity belongs to a transaction-management ASN.

### Topic 2: Multi-link batch operations, permission/authorization model, version-aware link semantics
**Why out of scope**: Belong to higher-level protocol ASNs; the open questions section correctly raises these without trying to resolve them in this ASN.

### Topic 3: Endset well-formedness when spans reference unallocated I-addresses
**Why out of scope**: Governed by L3 (e₃ ≠ ∅) and L4 (EndsetGenerality) in the foundation; the question of whether *additional* constraints should apply belongs to a future endset-discipline ASN.

### Topic 4: Effects on subsequent INSERT/DELETE/COPY/REARRANGE operations involving links
**Why out of scope**: Per the explicit scope restriction.

VERDICT: REVISE
