# Review of ASN-0086

## REVISE

### Issue 1: SharedDepthOneAllocator's "element-field depth" terminology is used in two incompatible senses

**ASN-0086, Setup / SharedDepthOneAllocator Lemma**: The Setup section defines "The element-field depth of a tumbler `t` relative to its prefix `s ≼ t` is `zeros(t) − zeros(s)`." Then the lemma describes "the subspace-specific allocators that live one element-field deeper (the content allocator at `d.0.s_C` and the link allocator at `d.0.s_L`, opened by the depth-2 child-spawns `(d.0.s_C, 1)` and `(d.0.s_L, 1)`)."

**Problem**: Under the stated definition, `A_d`'s outputs (e.g., `d.0.1`, zeros = 3) and `A_{d.0.s_C}`'s outputs (e.g., `d.0.s_C.1`, zeros = 3) have *identical* element-field depth relative to `d` — both are at +1. The "one element-field deeper" claim and "depth-2 child-spawns" terminology use a different sense of depth (allocator-tree spawn-event distance), not the zeros-count definition. The structural argument is correct, but the terminology silently switches between two notions of depth.

**Required**: Either disambiguate by introducing a separate term ("allocator-tree depth" or similar), or refactor the lemma's language to use only the defined element-field depth and a separate term where the allocator-tree sense is needed. The udanax-green reference and the R0 Step 2 chain construction both depend on the structural distinction being clear.

### Issue 2: R0 Step 4 dispatches seven L-invariants in a single bullet, breaking granularity with the rest of the proof

**ASN-0086, R0 Proof Step 4**: Step 4 verifies L-invariants under the class-(iii) emission. Most invariants (L0, L1, L1a, L1b, L1c, L2, L3, L11a, L11b, L12, L12a, L12b, L13, L14, L14a, L-fin) receive individual bullets with specific verification arguments — L11a's bullet alone runs several sentences. The bullet "L4 (EndsetGenerality), L5 (EndsetSetSemantics), L6 (SlotDistinction), L7 (DirectionalFlexibility), L8 (TypeByAddress), L9 (TypeGhostPermission), L10 (TypeHierarchyByContainment), all ASN-0043: orthogonal to the single-step extension" lumps seven invariants together with one-clause sketches.

**Problem**: The asymmetric granularity makes the verification of L4–L10 less auditable than the per-invariant verification used throughout the rest of Step 4. L9 (TypeGhostPermission) in particular is itself an existence-of-Σ' claim about state extensions; verifying that R0's class-(iii) emission preserves L9's existence guarantee at Σ' is not obvious from "permits non-content type endsets; if anything, broadens what can be referenced." The other six are arguably routine, but the bundled treatment breaks the proof's pattern.

**Required**: Either break L4–L10 into individual bullets matching the granularity of the rest of Step 4, or shorten the elaborated bullets to match this level — keep the rigor uniform. The current asymmetry suggests the bundled invariants received less rigorous verification than the others.

### Issue 3: Worked Sketch Step 3 cites T3 for prefix-incomparability, but T3 is about tumbler equality, not prefix relations

**ASN-0086, Worked Sketch Step 3 (concrete)**: To establish that `b₂ = 1.0.1.0.2.0.2.1` is prefix-incomparable with the d-rooted addresses `{a₁, b₁, a₂}`, the proof says: "b₂ shares d's and d''s first four positions (1.0.1.0) but diverges at position 5 (1 for d-rooted addresses, 2 for d'-rooted), and T3 (CanonicalRepresentation, ASN-0034) makes the resulting tumblers distinct as values and prefix-incomparable."

**Problem**: T3 establishes `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)` — tumbler equality from componentwise equality at equal length. T3 does not directly address prefix relations. T3 yields distinctness as values (a₁ ≠ b₂), but distinctness does not entail prefix-incomparability. The intended argument is from the Prefix definition (ASN-0034) directly: if `a₁ ≼ b₂`, then b₂ agrees with a₁ on positions 1..#a₁, but they differ at position 5 (≤ #a₁), contradiction; symmetrically for `b₂ ≼ a₁`.

**Required**: Replace the T3 citation with a citation to Prefix (PrefixRelation, ASN-0034) and exhibit the routine prefix-incomparability argument from divergence at a shared position. The same imprecision arguably affects the parallel argument in R0a's Case 2 sub-argument, though there the surrounding language is more explicit about the prefix-extension reasoning.

## OUT_OF_SCOPE

(No items. The ASN's Open Questions section already enumerates topics belonging in future ASNs — higher-arity link extensions, slice-wise reformulation under L14's native form, substrate-primitive tightening to discharge the sibling-frontier discipline, type-catalog coordination across layers, concurrency semantics for Emit/Observe. These are appropriately deferred and need not be duplicated here.)

VERDICT: REVISE
