# Review of ASN-0012

## REVISE

### Issue 1: Displacement algebra is underspecified — commutativity and identity required
**ASN-0012, "The displacement algebra"**: "where ⊕ is an associative binary operation on displacements"
**Problem**: The normalisation proof requires commutativity, not just associativity. When ENF4 normalisation absorbs the minimum child displacement into the parent, the new absolute address for a leaf through child c is:

    (parent ⊕ min) ⊕ (child ⊖ min)

The old absolute address is:

    parent ⊕ child

Setting x = child ⊖ min, by ENF3 we have x ⊕ min = child. Expanding with associativity: (parent ⊕ min) ⊕ x = parent ⊕ (min ⊕ x). But the old address is parent ⊕ (x ⊕ min). These are equal only if min ⊕ x = x ⊕ min — commutativity.

The same gap appears in re-homing: the new path Q.disp ⊕ ((P.disp ⊕ child.disp) ⊖ Q.disp) must equal P.disp ⊕ child.disp, which requires Q.disp ⊕ y = y ⊕ Q.disp.

Additionally, ENF4 uses "displacement 0" but no identity element for ⊕ is stated. The algebra (D, ⊕, ⊖, 0) needs: associativity (stated), commutativity (missing), identity element 0 (implicit in ENF4, never stated), and the cancellation property ENF3. Under ENF3' restriction, this is a partial commutative group.

**Required**: State commutativity as a requirement of ENF2 or a separate property. State the identity element. The algebraic specification should read: (D, ⊕) is a commutative monoid with identity 0, and ⊖ satisfies ENF3 within same-subspace operands (ENF3').

### Issue 2: ENF3 is mislabeled
**ASN-0012, "The displacement algebra"**: "which reduces to requiring that ⊖ inverts ⊕: (a ⊖ b) ⊕ b = a. This is the *cancellation* property."
**Problem**: The property (a ⊖ b) ⊕ b = a is not "left cancellation." In standard algebra, left cancellation of ⊕ means: c ⊕ a = c ⊕ b ⟹ a = b. What is stated is that ⊖ is a right inverse for ⊕ — distinct concept. The label matters because a reader looking for left cancellation in the algebraic sense will find a different property than expected.
**Required**: Either relabel as "right-inverse property" or state it as what it is: "⊖ is a right inverse of ⊕." If the ASN intends standard cancellation as a *consequence*, derive it (it follows from right-inverse + commutativity, once commutativity is added per Issue 1).

### Issue 3: ENF1 tightness claimed as correctness requirement for emptiness — unsupported
**ASN-0012, "The multi-dimensional case"**: "a loose box would break the empty-detection contract"
**Problem**: An empty enfilade has no children; its bounding box is trivially zero regardless of whether computation is tight or loose. A subtree whose leaves have all been deleted either (a) has its internal nodes cleaned up (so the subtree vanishes), or (b) retains empty children, each reporting width 0 — tight or loose bounding box of zero-width children is still zero.

The only scenario where looseness affects emptiness is if a child has non-zero width but no leaves — but that would mean width is decorrelated from content, which violates ENF0/ENF1 by definition.

Tightness IS required: it maintains ENF4-GLOBAL (root displacement = min leaf address) and it provides efficient pruning. But the emptiness argument is a non-sequitur.
**Required**: Retract the emptiness-correctness claim. Characterize ENF1 tightness as a structural invariant that maintains ENF4-GLOBAL derivability and enables efficient pruning. If there is a genuine emptiness failure mode, describe the specific state in which it occurs.

### Issue 4: Sequential partition property unstated
**ASN-0012, "Width composition"**: "the children's address ranges are non-overlapping and adjacent"
**Problem**: This property — that children of a sequential enfilade node *partition* the parent's address range into contiguous, non-overlapping intervals — is stated in passing but never labeled or formalized. It is logically independent of ENF0 (you could have additive widths over overlapping ranges) and is load-bearing for the ENF5 sequential proof (offset accumulation works only because the partition property guarantees that exactly one child covers any given position).

Without it, ENF0 alone does not establish traversal correctness. A sequential enfilade could have children with widths summing correctly but covering overlapping ranges, and the offset-accumulation traversal would miss entries in the overlap.
**Required**: State the sequential partition property explicitly: for internal node n with children c₁, ..., cₖ in order, the address range of cᵢ is [Σ_{j<i} w(cⱼ), Σ_{j≤i} w(cⱼ)), and these ranges are disjoint and their union is [0, w(n)). Give it a label. It is a correctness requirement, not a consequence of ENF0.

### Issue 5: ENF5 proofs are path-existence arguments, not traversal-correctness proofs
**ASN-0012, "Traversal completeness"**: "every ancestor of a qualifying leaf has a range that intersects Q. The traversal descends into every such ancestor."
**Problem**: The proof shows that *a path exists* from root to qualifying leaf through nodes whose ranges intersect Q. It does not show the *traversal algorithm* follows that path. Two specific gaps:

For sequential enfilades: the proof argues about a single qualifying leaf at position p, but ENF5 is about interval queries [p, q). An interval query must find *all* children whose ranges overlap [p, q), not just the one containing p. The traversal scans left-to-right and descends — but the proof doesn't argue that after descending into one qualifying child and returning, the traversal continues to find the next qualifying child. The continuation condition (rightward scan after ascent) is assumed, not shown.

For multi-dimensional enfilades: the claim "checks each child independently against the query" is stated but the algorithm that achieves this (visit ALL children at each internal node, not just the first qualifying one) is not specified or argued.
**Required**: For each enfilade species, either (a) specify the traversal algorithm precisely enough that ENF5 follows from the algorithm definition + structural invariants, or (b) state ENF5 as an axiom that any correct traversal must satisfy and defer the proof to a traversal-specification ASN. Currently the ASN occupies an uncomfortable middle ground — claiming a proof while showing only a sketch.

### Issue 6: ENF7-IND is a theorem, not an independent property
**ASN-0012, "Result ordering"**: "For any two enfilades E₁ and E₂ with identical logical content..."
**Problem**: ENF7-IND follows directly from ENF5 + ENF6 + ENF7. If E₁ and E₂ have identical leaves, then ENF5 guarantees both results contain the same qualifying leaves, ENF6 guarantees each appears exactly once, and ENF7 guarantees the same ordering. Therefore result(E₁, Q) = result(E₂, Q). Stating ENF7-IND alongside ENF5/ENF6/ENF7 as an independent property obscures this derivation and inflates the property count.
**Required**: Derive ENF7-IND as a theorem from ENF5 + ENF6 + ENF7, with the explicit proof chain. Move it out of the properties list and into a derived-results section.

### Issue 7: ENF9 says "multiset" but E is a partial function
**ASN-0012, "Content identity preservation"**: "leaves(E') = leaves(E) as a multiset"
**Problem**: The abstract structure is defined as "a finite mapping E : A ⇀ V" — a partial function from addresses to values. A partial function maps each address to at most one value. The leaf set of a partial function is a *set*, not a multiset (no two leaves share an address). If "multiset" is intentional — anticipating that distinct tree leaves might carry the same address — then the abstract structure E : A ⇀ V is wrong (it should be a multimap or a bag). If "set" was intended, "multiset" is misleading.
**Required**: Either change "multiset" to "set" (consistent with E : A ⇀ V), or explain why multiset is correct and revise the abstract structure definition accordingly.

### Issue 8: ENF4-GLOBAL derivation is a narrative, not a proof
**ASN-0012, "The normalisation invariant"**: "The child with displacement 0 at the root level is the child whose subtree contains the minimum-addressed leaf."
**Problem**: The derivation is stated as a narrative paragraph rather than an inductive proof. The inductive hypothesis — that for every internal node n, min_leaf(n) = absolute_disp(n) — is never stated. The base case (leaves) and inductive step (internal nodes using ENF4) are mixed into a single paragraph.

The correct structure is: Define min_leaf(n) = min over all leaves in n's subtree of absolute_addr(leaf). **Base case**: At the lowest internal level, children are leaves. min_leaf(n) = min_i(absolute_disp(n) + disp(cᵢ)) = absolute_disp(n) + min_i disp(cᵢ) = absolute_disp(n) + 0 = absolute_disp(n), by ENF4. **Inductive step**: At higher levels, min_leaf(n) = min_i min_leaf(cᵢ) = min_i absolute_disp(cᵢ) [by IH] = min_i(absolute_disp(n) + disp(cᵢ)) = absolute_disp(n) + 0 = absolute_disp(n), by ENF4. **At root**: absolute_disp(root) = disp(root), so disp(root) = min_leaf(root). ∎
**Required**: Replace the narrative with the explicit inductive argument.

### Issue 9: No concrete example
**ASN-0012, throughout**: The ASN introduces 18 properties and proves several derived results, but never verifies any property against a specific enfilade state.
**Problem**: A worked example would validate the properties and expose edge cases. For instance: a sequential enfilade with 3 leaves (addresses 0-2, 3-5, 6-8) where INSERT at position 4 causes a split. Walk through: new leaf set (ENF9), recomputed widths (ENF0), split post-conditions (ENF10), and range query [3,7) on the result (ENF5, ENF6, ENF7). For multi-dimensional: a POOM enfilade with 2 entries showing normalisation (ENF4), displacement accumulation (ENF2), and bounding-box computation (ENF1). Without a concrete instance, the properties float free of any grounding.
**Required**: Add at least one worked example for each enfilade species, exercising the key properties (composition law, split, and range query).

## DEFER

### Topic 1: Link enfilade classification
The vocabulary mentions three enfilade types (I-enfilade, V-enfilade, link enfilade) but the ASN only classifies two species (sequential 1D, multi-dimensional 2D). The link enfilade — which indexes from, to, and type endsets — is unclassified. Which species is it? Does it require a third composition law?
**Why defer**: The ASN's two-species taxonomy is complete for I-enfilades and V-enfilades. Link enfilade classification is additional work, not an error in what's here.

### Topic 2: DELETE operation and enfilade invariants
The ASN discusses INSERT, split, merge, and rebalancing but does not analyze how DELETE affects structural invariants. Deletion may create empty subtrees, trigger cascading merges, and temporarily violate ENF4/ENF8' before cleanup.
**Why defer**: ENF-FRAME states the meta-obligation; per-operation proofs belong in operation-specific ASNs.

### Topic 3: Relationship to EWD-008 E0/E1/E2
EWD-008 introduces enfilade properties E0, E1, E2. This ASN introduces ENF0-ENF12. The relationship (replacement, refinement, generalization) is unstated.
**Why defer**: Cross-referencing is editorial work, not a correctness issue in this ASN.

### Topic 4: Output-sensitive range query bounds
The open question about bounding visited leaves as a function of result size is important for performance guarantees but orthogonal to the correctness properties specified here.
**Why defer**: Performance bounds depend on balance properties the ASN explicitly declines to require.