# Cone Review — ASN-0034/T6 (cycle 1)

*2026-04-17 17:07*

### `fields` signature in T6 disagrees with T4b's partial-function definition
**Foundation**: T4b (UniqueParse), Definition clause and Postconditions — "`fields : T ⇀ Seq(ℕ⁺) × Seq(ℕ⁺) × Seq(ℕ⁺) × Seq(ℕ⁺)` is the partial function whose domain is exactly the T4-valid subset of `T`"
**ASN**: T6, Ingredient 1 — "The function `fields : T → Seq(ℕ⁺) × Seq(ℕ⁺) × Seq(ℕ⁺) × Seq(ℕ⁺)` decomposes a tumbler into its node, user, document, and element fields"
**Issue**: T4b fixes `fields` as partial (`⇀`) with domain restricted to the T4-valid subset; T6 rewrites the signature as total (`→`) over all of `T`. The same symbol is introduced with two different type signatures across the ASN, and T6's total form contradicts the explicit non-assignment clause in T4b ("Outside that subdomain … `fields(t)` is not assigned a value"). Under T6's stated precondition the inputs are T4-valid so evaluation is well-defined — but the cross-cutting issue is the signature, not the evaluation: downstream formalization that reads T6's type at face value will inherit a total function that T4b does not license.
**What needs resolving**: Reconcile the type signature of `fields` across T4b and T6 so a single partial-function declaration is used consistently, or document the domain restriction explicitly at T6's use site.

---

### T6 Ingredient 2 attributes field-presence biconditionals to T4c, but T4c only defines labels
**Foundation**: T4c (LevelDetermination) defines hierarchical *labels* by zero count; the field-presence biconditionals (`U(t) ≠ ε ↔ zeros(t) ≥ 1`, etc.) live in T4b's Postconditions ("absence pattern on the T4-valid subdomain, by case: … `zeros(t) = 1` → `N(t), U(t)` non-empty, `D(t) = E(t) = ε`; …") and in T4b's component-access clause ("`t.U₁` iff `zeros(t) ≥ 1`; `t.D₁` iff `zeros(t) ≥ 2`; `t.E₁` iff `zeros(t) = 3`")
**ASN**: T6, Ingredient 2 — "By T4(c), this count is computable from `t` alone and determines the hierarchical level: every tumbler has a node field (T4 requires `α ≥ 1`); a user field is present iff `zeros(t) ≥ 1`; a document field is present iff `zeros(t) ≥ 2`; an element field is present iff `zeros(t) = 3`."
**Issue**: The four biconditionals stated here are about *field presence* (whether the projection equals ε), not about *labels*. T4c explicitly disclaims this reading — its Postconditions note that "Any independent characterisation of the levels — for example, *user address* as 'the tumbler has exactly `N(t)` and `U(t)` non-empty in T4b's `fields(t)` decomposition' — is not the content of T4c". The field-presence thresholds that T6(b), T6(c), T6(d) actually consume (checking `zeros(a) ≥ 1`, `zeros(a) ≥ 2`) are the T4b absence-pattern postconditions, so T6's citation points at the wrong lemma. T6's Depends list does name both T4b and T4c, but the inline justification in the proof of Ingredient 2 mis-sources the claim.
**What needs resolving**: Route Ingredient 2's field-presence thresholds through T4b's absence-pattern postcondition (or establish an explicit lemma bridging T4c's labels to T4b's presence pattern) so the citation chain terminates on the property that actually states the biconditional being used.

---

### T6(c) labels an exact-equality check as "document-lineage" while T6(d) reserves lineage/family language for the prefix case
**Foundation**: T6(d) — "Whether the document field of `a` is a prefix of the document field of `b` (*structural subordination within a document family*)"; Nelson-derived commentary — "the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation"
**ASN**: T6(c) — "Whether `a` and `b` share the same node, user, and *document-lineage* fields", with the corresponding procedure establishing `D(a) = D(b)` (exact componentwise equality), and Postcondition (c) reading `… ∧ D(a) = D(b)`
**Issue**: The label "document-lineage" in (c) denotes exact equality of the full D projection, while "document family / structural subordination" in (d) denotes the prefix relation on D. Both gesture at ancestry/lineage, but they name logically distinct relations under T4b's `fields` — yet the same ASN uses lineage-flavoured vocabulary for both. A reader (or a formalization) that takes "lineage" to mean "shared ancestral line" in both places will conflate T6(c) with T6(d) or will read T6(c) as something weaker than `D(a) = D(b)`.
**What needs resolving**: Either rename T6(c)'s relation to match what the proof establishes (exact equality of the document field) or document explicitly what "document-lineage" denotes in (c) versus "document family" in (d), so the two cases are terminologically disjoint.
