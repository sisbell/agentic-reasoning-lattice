# Review of ASN-0043

## REVISE

### Issue 1: Link definition and L3 — body vs. Properties table contradiction

**ASN-0043, Definition — Link / L3 / Properties table**: The body defines `Link = {(e₁, e₂, ..., eₙ) : N ≥ 2, each eᵢ ∈ Endset}` and L3 (NEndsetStructure) requires `|Σ.L(a)| ≥ 2`. The Properties table defines `Link` as `(from : Endset, to : Endset, type : Endset) — a triple of endsets` and L3 as `TripleEndsetStructure — every link has exactly three endsets: Σ.L(a) = (F, G, Θ)`.

**Problem**: The body and the summary table disagree on whether links are N-ary (N ≥ 2) or strictly ternary. This is not cosmetic — it propagates through multiple properties:

- L6 (SlotDistinction) is stated only for the 3-endset case: `F ≠ G ⟹ (F, G, Θ) ≠ (G, F, Θ)`.
- L8 (TypeByAddress) references `Σ.L(a₁).type` — undefined for N = 2 links that have no type slot.
- L9 (TypeGhostPermission) references `.type` in its formal statement.
- L10 (TypeHierarchyByContainment) depends on type endsets existing.
- The Summary section says "Three endsets."

If links are N-ary, the type-dependent properties (L8, L9, L10) need explicit preconditions (e.g., "for links following the standard triple convention, where `|Σ.L(a)| ≥ 3`"). If links are ternary, the body's Definition — Link and L3 must be tightened to match the table.

**Required**: Resolve the contradiction. Either (a) commit to N-ary and generalize or add preconditions to L6–L10, updating the table to match, or (b) commit to ternary and update the body's Definition — Link and L3 to say exactly three.

### Issue 2: "GlobalUniqueness (ASN-0034)" — unnamed in foundation

**ASN-0043, L11a**: `"By GlobalUniqueness (ASN-0034), no two allocation events anywhere in the system, at any time, produce the same address."`

**Problem**: The ASN-0034 formal statements contain no property named "GlobalUniqueness." The intended property is derivable: T9 (ForwardAllocation) gives strictly increasing allocation within each allocator; T10 (PartitionIndependence) gives disjoint outputs between independent allocators. Together these yield global uniqueness. But the derivation is not shown, and the cited name doesn't match any foundation label. The same phantom reference appears in the L9 witness verification and L11b proof.

**Required**: Either cite T9 + T10 directly at each use, or derive GlobalUniqueness explicitly as a one-step lemma from T9 + T10 before invoking it.

### Issue 3: PrefixSpanCoverage introduces `ℓ_x`; foundation already defines `δ(1, #x)`

**ASN-0043, Lemma — PrefixSpanCoverage**: `"define the unit-depth displacement ℓ_x with #ℓ_x = #x, zero at positions 1 through #x − 1, and value 1 at position #x"`

**Problem**: This is `δ(1, #x)` (OrdinalDisplacement, ASN-0034): `δ(n, m) = [0, ..., 0, n]` of length `m`, with `n = 1` and `m = #x`. And `x ⊕ ℓ_x = x ⊕ δ(1, #x) = shift(x, 1)` by OrdinalShift. The ASN introduces a new symbol for a concept the foundation already names. The same notation appears in the L9 witness (`ℓ_g`), L13, and the worked example (`ℓ₁`, `ℓ₂`, `ℓ_a`, `ℓ_p`).

**Required**: Replace `ℓ_x` with `δ(1, #x)` throughout PrefixSpanCoverage, L9, L13, and the worked example. Note the equivalence `x ⊕ δ(1, #x) = shift(x, 1)` to connect the lemma to the shift algebra (TS1–TS5).

### Issue 4: L8 classified as INV — it is a definition

**ASN-0043, Properties table**: `"L8 | INV | TypeByAddress"`

**Problem**: L8 introduces `same_type(a₁, a₂) ⟺ Σ.L(a₁).type = Σ.L(a₂).type`. This defines a derived relation (type matching), not a state constraint. An invariant restricts which states are reachable; a definition names a concept. The distinction matters downstream: invariants must be preserved by every operation, definitions do not impose preservation obligations.

**Required**: Reclassify L8 as DEF in the Properties table.

## OUT_OF_SCOPE

### Topic 1: Span overlap and normalization within endsets

Two spans in the same endset may have overlapping coverage (e.g., `{(s, ℓ₁), (s', ℓ₂)}` where the denoted intervals intersect). Whether overlapping spans should be prohibited, normalized, or treated as semantically meaningful is a question about canonical representation and query behavior. The ASN correctly notes the unimplemented `consolidatespanset` and lists coverage equivalence as an open question.

**Why out of scope**: Query semantics and canonical-form decisions belong in a future query or retrieval ASN, not in the structural ontology.

### Topic 2: Self-referential links

A link at address `a` whose endset contains span `(a, δ(1, #a))` is conforming under L0–L14 — no invariant prevents it. Whether such links are operationally constructible (MAKELINK would need to know `a` before creating the entry) is an operation-level question.

**Why out of scope**: The ASN's Open Questions already ask about compound link well-formedness; self-reference is a special case, and MAKELINK semantics are explicitly excluded from scope.

VERDICT: REVISE
