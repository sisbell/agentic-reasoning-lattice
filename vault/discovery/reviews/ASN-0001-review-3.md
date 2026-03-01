# Review of ASN-0001

## REVISE

### Issue 1: Partition monotonicity proof omits the ordering lemma between sibling sub-partitions

**ASN-0001, Theorem (Partition monotonicity)**: "So addresses from earlier-allocated sub-partitions precede those from later-allocated sub-partitions"

**Problem**: The proof uses an unstated lemma: if `p₁ < p₂` under T1 and neither is a prefix of the other, then for every `a` extending `p₁` and every `b` extending `p₂`, `a < b`. This is the load-bearing step — it converts "prefixes are ordered" into "all addresses under those prefixes are ordered" — and it is asserted without argument. The proof is one line: since `p₁ < p₂` by T1 case (i), there exists a divergence position `k` where `p₁ₖ < p₂ₖ`; any extension `a` of `p₁` has `aₖ = p₁ₖ < p₂ₖ = bₖ` for any extension `b` of `p₂`; agreement on `1..k-1` follows from both extending their respective prefixes. But it must be shown, not assumed. The proof also relies on sibling sub-partitions being non-nesting (neither prefix of the other), which follows from the hierarchical structure but is not stated.

**Required**: State and prove the lemma: for non-nesting prefixes `p₁ < p₂`, every extension of `p₁` precedes every extension of `p₂`. State explicitly that sibling allocations produce non-nesting prefixes (they diverge at the sibling-distinguishing component).

---

### Issue 2: Global uniqueness Case 3 relies on a zero-count-to-level correspondence not captured in T4's formal statement

**ASN-0001, Theorem (Global uniqueness), Case 3**: "addresses produced at different hierarchical levels have different numbers of zero-valued components (T4)"

**Problem**: T4 as formally stated says: "Every tumbler `t ∈ T` used as an I-space address contains at most three zero-valued components, appearing in order as field separators. The function `fields(t)` that extracts the node, user, document, and element fields is well-defined and computable from `t` alone." The property that the *number* of zeros determines the hierarchical level (0 zeros = node, 1 = user, 2 = document, 3 = element) appears in the prose preceding T4 ("A tumbler with zero zeros addresses a node. One zero: a user account...") but is not part of the formal statement. Case 3 depends on this correspondence to distinguish addresses from nesting allocators. The proof cites T4 for something T4 does not formally say.

**Required**: Either add to T4 a clause stating that the count of zero-valued components uniquely determines the hierarchical level, or state it as a separate lemma and cite that in the Global uniqueness proof.

---

### Issue 3: Global uniqueness Case 3 is imprecise about which allocator produces which level

**ASN-0001, Theorem (Global uniqueness), Case 3**: "a server-level allocation produces an address with zero zeros (a node address) or one zero (a user address), while a user-level allocation produces an address with two zeros (a document address) or three zeros (an element address)"

**Problem**: A server-level allocator allocates user prefixes (one zero), not node addresses (zero zeros). Node addresses are produced by the root-level allocator. The "or" in "zero zeros (a node address) or one zero (a user address)" suggests a single allocator can produce addresses at two different hierarchical levels, which contradicts the hierarchical design. Each allocator operates at exactly one level: the root allocates nodes (0 zeros), a node allocates users (1 zero), a user allocates documents (2 zeros), a document allocates elements (3 zeros). The argument is correct in substance — nesting allocators produce different zero counts — but the language is muddled.

**Required**: State precisely that each allocator produces addresses at exactly one hierarchical level (one specific zero count). Then Case 3 becomes: nesting implies different levels, different levels imply different zero counts, different zero counts imply distinct tumblers by T3.

---

### Issue 4: Ghost element permanence is attributed to T8 but follows from T9

**ASN-0001, T8 (Address permanence)**: "Even addresses that have no stored content are irrevocably claimed."

**Problem**: T8 says: "If tumbler `a ∈ T` is assigned to content `c` at any point in the system's history, then for all subsequent states, `a` remains assigned to `c`." This covers assigned addresses. Ghost elements are by definition *unassigned* — "conceptually assigned positions, even if nothing represents them in storage." T8's formal statement does not cover them. Ghost element permanence follows from T9 (forward allocation): the allocator has advanced past the ghost address and will never return to assign it. The prose attributes ghost permanence to the section on T8, but the formal justification is T9.

**Required**: Move the ghost element discussion to T9, or add a sentence to T8 explicitly noting that ghost permanence is a consequence of T9's monotonicity, not of T8's content immutability.

---

### Issue 5: TA7's second clause uses operational language without algebraic grounding

**ASN-0001, TA7 (Subspace confinement)**: "`(A b ∈ S₂ : b is unchanged by any shift within S₁)`"

**Problem**: "b is unchanged by any shift within S₁" is an operational statement about what happens to positions during an editing operation, not an algebraic property of `⊕` and `⊖`. The first clause — `a ⊕ w ∈ S₁` for `a ∈ S₁` — is algebraic. The second clause asserts that an operation (INSERT/DELETE in S₁) does not modify values in S₂. This is a frame condition on operations, not a property of the arithmetic. The tumbler algebra as defined has no notion of "applying a shift to some positions and not others" — that belongs to the operation semantics (the POOM modification).

**Required**: Either (a) split TA7 into an algebraic clause (closure: `a ∈ S₁ ⟹ a ⊕ w ∈ S₁`) and a frame clause stated as a system-level invariant rather than an arithmetic property, or (b) reformulate the second clause algebraically — e.g., state that no `w` in the range of text widths can produce a cross-subspace result when added to any valid position, and that the operation definition restricts shifts to same-subspace positions.


## DEFER

### Topic 1: Span cardinality and the discreteness of T

The order-theoretic section establishes that T is not dense — every tumbler has an immediate successor (its zero-extension). But the span definition `{t : s ≤ t < s ⊕ ℓ}` captures all tumblers in the range, not just allocated ones. Between two element-level tumblers like `[1,0,3,0,2,0,1,1]` and `[1,0,3,0,2,0,1,5]`, infinitely many tumblers exist (at deeper nesting levels). The relationship between a span's endpoint-defined range and the finite set of allocated positions it practically selects is not addressed.

**Why defer**: This is span semantics — how spans interact with the population of allocated addresses — not a defect in the tumbler algebra itself. The algebra correctly defines the range; what occupies the range is a question for the arrangement and content storage model.

---

### Topic 2: V-space tumbler structure

The worked example uses single-component V-space tumblers (`[1]`, `[3]`, `[5]`), and the text says V-positions "run contiguously from 1 to the document's current length." If V-space tumblers are always single-component naturals, their algebra is ordinary integer arithmetic and many of the tumbler-specific complexities (multi-component addition, cross-depth operands, subspace boundaries) vanish. The formal structure of V-space tumblers — whether they are always single-component, whether they can have hierarchical structure, and how this constrains TA0–TA4 — is not specified.

**Why defer**: The ASN establishes the algebraic contract for V-space arithmetic without committing to a representation. Pinning down V-space tumbler structure belongs in the arrangement/POOM specification, where the specific form of V-positions becomes load-bearing.

---

### Topic 3: Consistency of the axiom set — existence of a non-trivial model

The ASN demonstrates that TA-strict excludes the degenerate no-op model. But it does not demonstrate that the full axiom set (T0–T12, TA0–TA8, TA-strict) is simultaneously satisfiable by a non-degenerate model. The worked example uses single-component integer arithmetic, which satisfies the arithmetic axioms but does not exercise T4 (hierarchical parsing), TA5 (hierarchical increment), or TA7 (subspace confinement) in their full generality.

**Why defer**: Constructing a complete model that satisfies all axioms simultaneously is a substantial undertaking — essentially a reference implementation at the algebraic level. It would be a valuable future ASN but is not required to validate the individual properties stated here.
