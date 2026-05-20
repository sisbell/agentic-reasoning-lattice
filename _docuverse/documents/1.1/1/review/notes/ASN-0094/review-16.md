# Review of ASN-0094

## REVISE

### Issue 1: AllocatedAddressAntichain Step 3 "Symmetry argument" mischaracterizes what is symmetric

**ASN-0094, Lemma — AllocatedAddressAntichain, Step 3 Symmetry argument**: "The lemma's hypothesis `x ≼ a` is symmetric in `x` and `a` only with respect to the subspace assignment"

**Problem**: The prefix relation `x ≼ a` is asymmetric in `x` and `a` by definition — `x ≼ a` does not entail `a ≼ x` (Prefix, ASN-0034). Asserting symmetry "in x and a" is mathematically incorrect even with the qualifier "only with respect to the subspace assignment", since subspace assignment is not a property of the prefix relation itself. What is actually symmetric is the *case analysis* across Sub-cases 3a and 3b: both have the same hypothesis `x ≼ a` and discharge Steps 3.1 and 3.2 identically; only Step 3.3 differs in which side carries `s_L` vs `s_C`. The paragraph's closing sentence ("Steps 3.1 and 3.2 are written once and apply to both sub-cases; Step 3.3 is written out explicitly for each") gets the intent right; the leading sentence misnames the object of symmetry.

**Required**: Reword the leading sentence to assert case-symmetry across Sub-cases 3a and 3b rather than relation-symmetry of `x ≼ a`. The remainder of the paragraph is correct.

### Issue 2: Direct ASN-0093 reference in AllocatorTreeDepth definition

**ASN-0094, Definition — AllocatorTreeDepth**: "the number of T10a child-spawn pairs (·, k') with k' ∈ {1, 2} on ASN-0093's structural chain from d to A's base address"

**Problem**: ASN-0093 is not in this ASN's foundation list (ASN-0034, ASN-0043, ASN-0086). The chain ASN-0094 requires is committed to by ASN-0086's SubstrateConformingLayer Definition (via the Chain Discipline Catalog: ChainMembershipForOrigin et al.), which is foundationally available. Naming "ASN-0093" directly in a new definition (as distinct from quoting ASN-0086's foundation text verbatim) circumvents the foundation discipline of standard 7.

**Required**: Reword to reference the chain through ASN-0086's foundation naming — e.g., "the structural chain committed to by ASN-0086's SubstrateConformingLayer Definition under ChainMembershipForOrigin" — or use the scaffolding's own clause name "*Per-document link sub-allocator chains*" (introduced later in Scope and Substrate Scaffolding). The terminology should be consistent: the same chain is variously called "ASN-0093's structural chain", "the substrate-conforming layer's link sub-allocator chain", and "the chain referenced by ASN-0086's R0a-Cor1" across the ASN.

## OUT_OF_SCOPE

All seven items listed in the Open Questions section are appropriately flagged by the ASN itself; no additional out-of-scope items to add. The framework's scoping (single-process substrates, ghost-targeting deferred, composite shapes deferred, registry mutability deferred) is honest and clear.

VERDICT: REVISE
