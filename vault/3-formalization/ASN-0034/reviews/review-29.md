# Cone Review — ASN-0034/PartitionMonotonicity (cycle 1)

*2026-04-13 23:23*

### TA5a and `zeros(t)`: load-bearing lemma cited across three properties but absent

**Foundation**: TA5 (HierarchicalIncrement), status table listing TA5a as "lemma"
**ASN**: T10a (AllocatorDiscipline), Consequence 4: "Since siblings use `inc(·, 0)` (unconditionally T4-preserving by TA5a) and child-spawning uses `k' ∈ {1, 2}` within TA5a bounds"; formal contract: "`k' = 1` when `zeros(t) ≤ 3`, `k' = 2` when `zeros(t) ≤ 2`"
**Issue**: TA5a is the bridge that connects the increment operation (TA5) to the structural validity constraint (T4) and is the sole basis for T10a.4 (T4 preservation under the discipline) and for the restriction of child-spawning to `k' ∈ {1, 2}`. It exists only as a one-line table entry: "inc(t, k) preserves T4 iff k = 0, or k = 1 ∧ zeros(t) ≤ 3, or k = 2 ∧ zeros(t) ≤ 2; violated for k ≥ 3." No statement, no proof, no definition of `zeros(t)`. Without knowing what `zeros(t)` counts — total zero-valued components? trailing zeros? zero-length fields in the hierarchical parse? — the boundary conditions on `k'` are unverifiable. Similarly, TA5-SigValid ("for every valid address satisfying T4, `sig(t) = #t`") is listed as a lemma but never proved; the allocation narrative relies on it to claim `inc(t, 0)` increments the last component, even though the proofs happen to avoid needing it.
**What needs resolving**: TA5a requires a full statement with `zeros(t)` formally defined, a proof establishing each case (including the failure for `k ≥ 3`), and verification that T10a's bound conditions (`zeros(t) ≤ 3` for `k' = 1`, `zeros(t) ≤ 2` for `k' = 2`) are exactly the TA5a-preserving cases. TA5-SigValid needs its proof and its T4 dependency made explicit.

---

### T10 (PartitionIndependence): justification target for T10a is absent

**Foundation**: T10a's Follows-from list names T10 as a foundation
**ASN**: T10a.2: "satisfying the precondition of T10"; T10a-N: "This violates the T10 precondition. The axiom is therefore both sufficient (T10a.1–T10a.3) and necessary for prefix-incomparability of sibling outputs."
**Issue**: T10a's entire design rationale is stated in terms of ensuring T10's precondition — that sibling outputs have non-nesting prefixes so that T10 (PartitionIndependence) can guarantee coordination-free uniqueness. The necessity argument (T10a-N) concludes by citing "the T10 precondition" as the thing that would be violated. But T10 is never stated anywhere in the ASN. Neither its guarantee (what partition independence provides) nor its precondition (what it requires of prefixes) is visible. T10a is an axiom designed to ensure a precondition for a property that has no formal existence in the document.
**What needs resolving**: T10 must be stated explicitly — at minimum its precondition (which T10a claims to ensure) and its guarantee (which motivates the discipline). Without it, T10a-N's necessity argument has no grounding: "violates the T10 precondition" references a predicate that is undefined.

---

### T5 preamble introduces a phantom dependency on T4

**Foundation**: T4 (HierarchicalParsing), referenced in T5 preamble
**ASN**: T5 (ContiguousSubtrees), preamble: "T4, combined with the total order T1, gives us the property that makes spans work"
**Issue**: T5's proof cites T1 (for ordering), T3 (for "distinct lengths imply distinct tumblers" in Case 2), and the prefix relation `≼` — nothing else. T4 appears nowhere in the proof body, the case analysis, or the formal contract. The preamble sentence creates a false dependency edge in the property DAG: a formalization attempting to verify T5 would require T4 as an input when T4 plays no logical role in the proof. The real dependency set is `{T1, T3, ≼}`.
**What needs resolving**: Either remove the T4 reference from T5's preamble (if T4 truly plays no role in contiguous subtrees), or identify the specific proof step where T4 is needed and add the citation. The current state is ambiguous — the narrative says T4 matters but the proof never invokes it.

---

### T1 trichotomy proof forward-references T3; T3 proof forward-references T0

**Foundation**: T3 (CanonicalRepresentation), T0 (carrier set definition)
**ASN**: T1 (LexicographicOrder), trichotomy proof Case 1: "Then `m = n` and `aᵢ = bᵢ` for all `1 ≤ i ≤ m`, so `a = b` by T3"; T3 proof: "By T0, T is the set of all finite sequences over ℕ"
**Issue**: T1's trichotomy proof requires T3 to conclude `a = b` from componentwise agreement — without T3, the proof cannot close Case 1. But T3 is stated *after* T1 in the document. Similarly, T3's own proof invokes T0 ("By T0, T is the set of all finite sequences over ℕ"), but T0 appears nowhere in the ASN and is not listed as a dependency. The logical dependency chain is T0 → T3 → T1, but the document presents T1 before T3 and omits T0 entirely. PrefixOrderingExtension (the very first property) then cites T1, compounding the inversion.
**What needs resolving**: The dependency order T0 → T3 → T1 → PrefixOrderingExtension must be respected in either document ordering or explicit forward-declaration. T0 (the definition of the carrier set T) must appear or be declared as a dependency — it is the ground on which T3's proof stands.

---

### Prefix relation `≼` used across six properties but lacks a standalone definition

**Foundation**: "Prefix (PrefixRelation)" cited in T10a's Follows-from list as a separate foundation
**ASN**: PrefixOrderingExtension (first property, uses `≼` in statement and proof), T5 (inline definition in proof: "`p ≼ a` means `#a ≥ #p` and `aᵢ = pᵢ` for all `1 ≤ i ≤ #p`"), T10a (lists "Prefix (PrefixRelation)" as a foundation), PartitionMonotonicity (uses `≼` throughout)
**Issue**: PrefixOrderingExtension — the first property in the document — uses `≼` in its statement ("for every `a` extending `p₁` (`p₁ ≼ a`)") and its proof. The first actual definition appears four properties later, inline in T5's proof. T10a references "Prefix (PrefixRelation)" as though it were a separately defined property with its own formal contract, but no such standalone definition exists. The usage is *consistent* across all properties — the meaning doesn't shift — but the definition is scattered across inline glosses rather than established once as a foundation for all downstream consumers.
**What needs resolving**: The prefix relation needs a single canonical definition (with formal contract specifying the biconditional `p ≼ a ⟺ #a ≥ #p ∧ (∀ i : 1 ≤ i ≤ #p : aᵢ = pᵢ)`) that precedes all properties referencing it. T10a's citation of "Prefix (PrefixRelation)" as a foundation suggests this was intended but never realized.
