# Review of ASN-0001

## REVISE

### Issue 1: Global uniqueness proof — Case 3 does not cover nesting allocators at the same zero count

**ASN-0001, Coordination-free uniqueness, Theorem (Global uniqueness), Case 3**: "each allocator operates at exactly one hierarchical level: the root allocates nodes (zeros = 0), a node allocates users (zeros = 1), a user allocates documents (zeros = 2), a document allocates elements (zeros = 3). Since the two allocators operate at different levels, their outputs have different zero counts."

**Problem**: The proof assumes that nesting prefixes imply different zero counts. This fails for document-versus-version allocation. A user allocator producing top-level documents (document field `[D]`) and a version allocator producing versions of document 2 (document field `[2, V]`) both output addresses with `zeros = 2`. Their ownership prefixes nest — the user's prefix `1.0.3.0` is a prefix of the version allocator's prefix `1.0.3.0.2` — so T10 does not apply. And both produce addresses at the same zero count, so the "different zero counts" argument in Case 3 does not apply either. Uniqueness does hold in this case (the addresses differ in length of the document field, hence by T3), but the proof as written has no case that establishes it.

**Required**: Either add a fourth case handling nesting allocators at the same hierarchical level (arguing via T3 that their outputs differ in document-field length), or strengthen the definition of "hierarchical level" so that document allocation and version allocation are formally distinct levels with a proven structural distinguisher.

### Issue 2: T11 and T12 are in tension — span definition uses ⊕, which T11 restricts to V-space

**ASN-0001, T11**: "The shift-arithmetic properties (TA0–TA4, TA7a) apply exclusively to V-space."

**ASN-0001, T12**: "A span (s, ℓ) with ℓ > 0 denotes the set {t ∈ T : s ≤ t < s ⊕ ℓ}."

**Problem**: T12 defines spans using `⊕`. T11 says `⊕` applies exclusively to V-space. But spans are needed in I-space — links reference I-space spans, endsets are sets of I-space spans, and the ASN itself says "links reference spans, transclusion copies spans." If `⊕` is V-space-only, T12 cannot define I-space spans, and the well-definedness of I-space spans (including non-emptiness via TA-strict) is unestablished.

**Required**: Either broaden the scope of `⊕` (defining it as a generic tumbler operation applicable in both spaces, while restricting *editing shifts* to V-space), or provide a separate span definition for I-space that does not depend on `⊕` (e.g., defined by explicit endpoints `{t : s ≤ t < e}` for some end tumbler `e`). Either way, T11 and T12 must be reconciled so that I-space spans have a well-defined semantics.

### Issue 3: Partition monotonicity proof asserts sibling prefixes have the same length without justification

**ASN-0001, Theorem (Partition monotonicity)**: "Sibling prefixes are non-nesting: they have the same length (each extends p by the same structure) and diverge at the sibling-distinguishing component, so neither can be a prefix of the other."

**Problem**: This is the load-bearing claim that enables application of the prefix ordering extension lemma, but it is asserted, not proven. The claim that "each extends p by the same structure" relies on an unstated assumption about how the hierarchy is populated. At the document level within a user's partition, documents are allocated as `p.0.D` for single-component `D`, so document-level prefixes do have equal length. But this structural regularity is not derived from T0–T10 or TA0–TA8. It depends on the allocation mechanism (TA5) always producing same-length siblings at each level. If TA5 with `k = 0` is the only sibling-producing operation, and `k = 0` preserves length (TA5(c)), then siblings have equal length — but this chain of reasoning must be shown, not assumed.

**Required**: Prove that sub-partition prefixes within a given partition are always the same length, deriving the claim from TA5(c) and the allocation protocol, or weaken the theorem to state the structural assumption as a precondition.

### Issue 4: TA7a quantifies over all displacements w without restriction

**ASN-0001, TA7a**: "(A a ∈ S₁, w : a ⊕ w ∈ S₁)"

**Problem**: The quantifier on `w` is unrestricted — it ranges over all positive tumblers. This is a very strong claim: no displacement whatsoever, applied to any address in subspace `S₁`, can produce a result outside `S₁`. For single-component widths `[n]`, this is plausible (the subspace identifier at the start of the element field is not affected by incrementing later components). But for multi-component widths — which the ASN explicitly admits ("the algebra admits multi-component lengths, which arise when a span crosses a hierarchical boundary") — the claim is unverified. A multi-component width that interacts with the subspace-identifier component could violate TA7a. The ASN does not prove that `⊕` cannot affect earlier components, nor does it restrict `w` to single-component tumblers.

**Required**: Either restrict the domain of `w` in TA7a to displacements that act within the element field (and define what that means formally), or prove that `⊕` as constrained by TA0–TA4 cannot affect the subspace-identifier component regardless of the width's structure.

## OUT_OF_SCOPE

### Topic 1: Version allocation and its interplay with document allocation order

The ASN's allocation model raises an unaddressed constraint: if a user's document allocator and a document's version allocator are the same sequential stream (Case 1 of global uniqueness), then creating document 3 after document 2 prevents later creation of version 2.1 (since `3 > 2.1` by T1, violating T9). If they are separate allocators, Case 3 of the global uniqueness proof needs the fix described in REVISE Issue 1, and the relationship between the two allocators' outputs needs formal treatment. Either resolution belongs in a future ASN on allocation protocols, not in the tumbler algebra.

**Why defer**: The tumbler algebra defines the properties that addresses must satisfy. How allocators are organized — single stream versus hierarchical delegation — is an operational question that builds on the algebra but is not part of it.

### Topic 2: Exact domain and behavior of ⊕ for multi-component operands

The ASN's open questions already ask: "Must addition preserve order universally, or only when the position and width share the same hierarchical depth?" and "Can addition ever produce or consume a zero-valued component?" These are the right questions, and answering them requires a formal model of `⊕` that this ASN deliberately avoids (it states properties, not algorithms). The answers will determine whether TA1, TA-strict, TA4, and TA7a are jointly satisfiable for all tumbler pairs or only for operands at the same depth.

**Why defer**: This is new territory — defining the operational semantics of `⊕` — not an error in the axioms as stated.

### Topic 3: Formal bridge between TA5 and T9

TA5 proves `inc(t, k) > t` — each increment exceeds its input. T9 requires that every allocation exceeds all *previous* allocations, not just the immediately preceding one. The connection (allocators always apply `inc` to their latest output, so the sequence is monotonically increasing) is implicit. A future ASN on allocation protocols should formalize the allocator state machine and derive T9 from TA5 plus the allocator's operational rule.

**Why defer**: T9 is a system-level invariant about allocator behavior. TA5 is a mathematical property of the increment operation. The bridge between them is about system dynamics, which is beyond the scope of the algebra.
