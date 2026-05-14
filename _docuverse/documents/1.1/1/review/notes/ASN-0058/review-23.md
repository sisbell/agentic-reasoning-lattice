# Review of ASN-0058

## REVISE

### Issue 1: C0 proof implicitly assumes k ≤ m
**ASN-0058, C0 (OrdinalDisplacementNecessity)**: "Suppose for contradiction that k < m."
**Problem**: The proof structure rules out `k < m` to conclude `k = m`, but never explicitly cites the upper bound `k ≤ m`. Without this bound, `k > m` is not excluded, leaving the conclusion `k = m` incomplete.
**Required**: Add one line citing ActionPoint's postcondition `1 ≤ actionPoint(w) ≤ #w` instantiated at `#ℓ = m`, giving `k ≤ m`. Then "we rule out k < m, leaving k = m."

### Issue 2: C1a "applies verbatim" overstates the extension
**ASN-0058, C1a (RestrictionDecomposition)**: "Both proofs require only the three conditions verified above — functionality, finite domain, and common depth m ≥ 2 across the domain; they apply to f verbatim."
**Problem**: M12's proof text invokes "S8-depth (ASN-0036) applied to that subspace" to establish `#v' = #v = m`. For arbitrary `f`, S8-depth is not in force on `f` itself — the common-depth conclusion comes from C1a's third condition. The argument structure carries over, but a textual substitution is required (S8-depth → the common-depth assumption). "Verbatim" is too strong.
**Required**: Replace "they apply to f verbatim" with explicit acknowledgment that M12's appeals to S8-depth are discharged by C1a's common-depth assumption when `f` is the restricted function; the rest of the argument structure is unchanged.

### Issue 3: Origin invariance within a block is implicit but never stated
**ASN-0058, M16 commentary**: "the canonical decomposition naturally preserves origin boundaries. In a maximally merged decomposition, every block maps to a contiguous I-range under a single document prefix."
**Problem**: The fact `origin(a + k) = origin(a)` for `0 ≤ k < n` within a block (when `a ∈ dom(C)`) is derived inside M16's proof and reused in M6(d) and the commentary above. It is never extracted as a standalone result, so downstream consumers must re-derive it from M16's internal argument.
**Required**: Add a corollary (e.g., M16a) stating: "For `a ∈ dom(C)` and any `k ≥ 0`, `origin(a + k) = origin(a)`." This is the load-bearing fact that both M6(d) and M16's contrapositive turn on.

### Issue 4: Span Algebra Connection remark asserts imprecise correspondences
**ASN-0058, Remark after M1**: "A mapping block β = (v, a, n) induces two spans in the sense of ASN-0053: a V-span over V(β) and an I-span over I(β). The block's split (M4 below) corresponds to simultaneous application of S4 (SplitPartition, ASN-0053) to both spans at corresponding positions. The merge (M7 below) corresponds to S3 (MergeEquivalence, ASN-0053) applied to both span pairs, subject to both being adjacent."
**Problem**: The asserted correspondences are loose in two ways. (i) `V(β) = {v + k : 0 ≤ k < n}` is the depth-`#v` shift orbit, while the natural ASN-0053 span `(v, δ(n, #v))` has denotation `{t ∈ T : v ≤ t < v + n}`, which includes other-depth tumblers — so `V(β) ⊊ ⟦σ⟧` in general, and "V-span over V(β)" is undefined. (ii) S3 (ASN-0053) admits overlapping spans; M7 forbids overlap (B2 violation). The "correspondence" therefore restricts S3's adjacent-only sub-case, not S3 itself.
**Required**: Either define "V-span over V(β)" precisely (e.g., as the depth-restricted projection of `(v, δ(n, #v))`) and note that the correspondence is to S3's adjacent-only sub-case; or rephrase as an analogy rather than a correspondence.

### Issue 5: Element-level allocator T10a-conformance is implicit
**ASN-0058, M16 proof step 1**: "S7d (DocumentAllocationDiscipline, ASN-0036) places the document tumblers under T10a, and S7b (ElementLevelIAddresses, ASN-0036) gives zeros(a₁) = zeros(a₂) = 3, so each I-address sits within an element-level allocator's domain."
**Problem**: S7d places document tumblers under T10a; nothing in the cited premises directly says element-level allocators (whose outputs are the I-addresses in `dom(C)`) are themselves T10a-conforming. The argument relies on T10a's recursive allocator tree, where element-level allocators are descendants spawned from document-level allocators via further `inc(·, k')` operations. Without this step, T10a.4's "every output satisfies T4" cannot be invoked on `a₁, a₂`.
**Required**: Add one line citing T10a's allocator tree (or an explicit assumption) that element-level allocators are descendants in the T10a tree, hence T10a.4 applies to their outputs.

## OUT_OF_SCOPE

None. The ASN stays within bundle algebra; it does not stray into operations, links, versions, or replication.

VERDICT: REVISE
