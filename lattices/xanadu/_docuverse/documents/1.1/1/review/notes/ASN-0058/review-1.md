# Review of ASN-0058

## REVISE

### Issue 1: M2 claims decomposition for all of dom(M(d)), but S8 only covers text subspace

**ASN-0058, "The Arrangement as a Set of Blocks"**: "M2 (DecompositionExistence). Every arrangement M(d) admits a block decomposition. This is S8 (SpanDecomposition, ASN-0036) restated in our vocabulary."

**Problem**: S8 is explicitly scoped to text-subspace V-positions: `{(v, Σ.M(d)(v)) : v ∈ dom(Σ.M(d)) ∧ v₁ ≥ 1}`. The block decomposition definition (B1) quantifies over all of `dom(M(d))` without the `v₁ ≥ 1` guard. If link-subspace V-positions exist in `dom(M(d))`, M2 asserts their decomposability without foundation support. S8a (V-position well-formedness) is similarly restricted to `v₁ ≥ 1`.

**Required**: Either restrict B1, B2, B3, and M2 to a single subspace (matching S8's scope), or provide a separate argument that the decomposition extends to all subspaces. Since "link endset semantics" is out of scope, the cleanest fix is an explicit subspace restriction: "A block decomposition of the text-subspace arrangement of document d..." propagated to all downstream results.

---

### Issue 2: Ordinal increment associativity used without statement or derivation

**ASN-0058, multiple sections**: The proofs for M5(a), M7, M9, and M10 all rely on the property `(v + c) + j = v + (c + j)`, where `+` denotes ordinal increment via TA5(c). This property is never stated, named, or derived.

**Problem**: In M5(a): "Setting `k = c + j` in the second, the union covers `{(v + k, a + k) : 0 ≤ k < n}`" — this substitution silently converts `(v + c) + j` to `v + (c + j)`. In M7: "`v₁ + k = v₁ + n₁ + j = v₂ + j`" makes the same implicit step. The property is true — it follows from TA-assoc applied to the displacement representation `v ⊕ [0,...,0,c]` — but the derivation must be shown. Specifically: let `w_k = [0,...,0,k]` (length `#v`); then `(v ⊕ w_c) ⊕ w_j = v ⊕ (w_c ⊕ w_j)` by TA-assoc, and `w_c ⊕ w_j = w_{c+j}` by TumblerAdd (shared action point at last position). State this as a lemma.

**Required**: Add a lemma (e.g., "M-aux: OrdinalIncrementAssociativity") deriving `(v + c) + j = v + (c + j)` from TA-assoc and TumblerAdd, then cite it in M5(a), M7, M9, M10.

---

### Issue 3: No concrete worked example

**ASN-0058, throughout**: The ASN provides no scenario with specific tumbler values demonstrating the split, merge, or canonical decomposition.

**Problem**: The review standards require at least one concrete example verifying key postconditions. The Gregory references serve as implementation evidence but not as formal verification. A worked example would expose any hidden mismatch between the abstract algebra and the intended semantics — e.g., what happens when V-positions are multi-component element tumblers rather than single integers.

**Required**: Add one concrete scenario. For instance: a document with three mapping blocks, specific V and I tumblers, where two blocks satisfy the merge condition and one does not. Show: (a) the merge produces the expected block, (b) the result is canonical, (c) the surviving boundary confirms M7's necessity conditions (V-adjacent but not I-adjacent).

---

### Issue 4: Open questions 2 and 5 are answerable from the ASN's own results

**ASN-0058, "Open Questions"**: "Can two blocks in a canonical decomposition have overlapping I-extents...?" and "What is the maximum multiplicity with which a single I-address can appear across all blocks in a canonical decomposition — is it bounded by any structural property of the arrangement?"

**Problem**: Question 2's first clause is answered by M13 and M14: yes, blocks can share I-extents, and such blocks are independent and unmergeable. The remaining sub-question (whether sharing must trace to an explicit operation) concerns operations, which are out of scope. Question 5 is answered by S5 (UnrestrictedSharing, ASN-0036): the multiplicity is unbounded. Listing answered questions as open suggests incomplete analysis.

**Required**: Resolve the answerable parts inline (citing M13/M14 and S5 respectively). If residual sub-questions remain (e.g., the operational origin of sharing), restate them precisely or remove them.

---

### Issue 5: M12 proof — "v − 1" well-definedness insufficiently discussed

**ASN-0058, "The Canonical Decomposition"**: "When `v` is the minimum of `dom(f)`, condition 2 is vacuously satisfied; the predecessor either does not exist as a valid address or is not in `dom(f)` by S8a, ASN-0036."

**Problem**: The parenthetical only addresses `v` being the minimum of `dom(f)`. But `v − 1` is also problematic when `v`'s last component equals 1 (producing a zero in the element field), regardless of whether `v` is the minimum. In that case `v − 1` violates S8a's strict-positivity requirement and so `v − 1 ∉ dom(f)`, satisfying condition 2. The proof is correct but the reader must infer this case.

**Required**: Generalize the parenthetical: "Condition 2 is vacuously satisfied whenever `v − 1 ∉ dom(f)` — in particular when `v` is the minimum of `dom(f)`, or when the last component of `v` equals 1 (so that `v − 1` has a zero element-field component and falls outside `dom(f)` by S8a)."

---

### Issue 6: M15(a) is imprecise as stated

**ASN-0058, "Document Independence"**: "No block appears in both a decomposition of `M(d₁)` and a decomposition of `M(d₂)`."

**Problem**: A mapping block is defined as a triple `(v, a, n)`. If two documents `d₁` and `d₂` both transclude the same I-content at the same V-position ordinals (which nothing in S0–S9 prevents), then the same triple `(v, a, n)` satisfies B3 for both `M(d₁)` and `M(d₂)`. M15(a) as written is false in that scenario. The intended claim is about representational independence — modifying one document's decomposition doesn't affect another's — which is M15(b).

**Required**: Either drop M15(a) (M15(b) carries the substance) or restate it precisely — e.g., "Block decompositions are per-document objects; membership of a triple in a decomposition of `M(d₁)` entails no relationship to any decomposition of `M(d₂)`."

---

### Issue 7: `⊕` overloaded for block merge

**ASN-0058, "Merging Adjacent Blocks"**: "`β₁ ⊕ β₂ = (v₁, a₁, n₁ + n₂)`"

**Problem**: ASN-0034 defines `⊕` as tumbler addition (`a ⊕ w`). The ASN reuses `⊕` for block merge, a different operation on a different type. In the Span Algebra Connection remark, both tumbler addition and block merge are relevant, creating genuine ambiguity.

**Required**: Use a distinct symbol for block merge (e.g., `⊞`, `merge(β₁, β₂)`, or `β₁ ∥ β₂`), or explicitly note the overloading with a convention statement at first use.

## OUT_OF_SCOPE

### Topic 1: Decomposition lattice structure
**Why out of scope**: Whether the set of equivalent decompositions forms a lattice under refinement is a structural question about the algebra's order theory, not an error in the current development. The ASN correctly identifies it as an open question.

### Topic 2: V-depth vs I-depth relationship within a block
**Why out of scope**: S8-depth constrains V-depths per subspace; S7b constrains I-depths. Whether M0 imposes additional cross-space depth constraints is a valid question but goes beyond the current ASN's claims. Open question 6 correctly flags this.

### Topic 3: Non-text-subspace block decomposition
**Why out of scope**: Link subspace V-positions (if any) would need their own decomposition argument. This belongs in a link subspace ASN, not here — but M2's scope should be narrowed (Issue 1 above) to avoid implicitly claiming it.

VERDICT: REVISE
