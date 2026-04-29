# Cone Review — ASN-0034/GlobalUniqueness (cycle 1)

*2026-04-14 04:02*

### Child-spawning outputs fall outside GlobalUniqueness case analysis
**Foundation**: (internal consistency — GlobalUniqueness proof structure)
**ASN**: GlobalUniqueness proof, exhaustiveness claim: *"Every pair of distinct allocation events falls into exactly one case."*
**Issue**: Case 1 invokes T9 to handle same-allocator pairs, but T9 covers only the sibling stream — outputs of `inc(·, 0)`. Child-spawning operations (`inc(·, k')` with `k' > 0`) produce addresses that are neither part of the parent's sibling stream nor part of the child's sibling stream (the child's stream begins at `inc(c₀, 0)`). Three pair-types escape the case analysis: (a) parent sibling vs. parent's child-spawning output, (b) two child-spawning outputs from the same parent, (c) a child-spawning output vs. the child's own sibling outputs (the base `c₀` is never in the child's `inc(·, 0)` sequence). Case 4 implicitly reclassifies `c₀` as a "child output" — *"every child output — including c₀ itself"* — but `c₀` is produced by the parent's `inc(·, k')`, and no formal rule assigns allocation events to child domains. The length-separation argument in Case 4 is sound, but the allocation-event taxonomy that routes pairs into cases has an unacknowledged gap at the boundary between parent and child.
**What needs resolving**: Either formally define "allocation event" and "owning allocator" so that every `inc` output is assigned to exactly one allocator's domain (making the four cases genuinely exhaustive), or add a fifth case covering child-spawning outputs with an explicit distinctness argument.

---

### T0 and Prefix — foundational definitions cited but never formally stated
**Foundation**: (internal consistency — dependency chain completeness)
**ASN**: T3 proof: *"By T0, T is the set of all finite sequences over ℕ."* T10 proof: *"the definition of ≼ (Prefix) requires p₂ᵢ = p₁ᵢ for all 1 ≤ i ≤ m."* T10a justification lists Prefix among its six foundations.
**Issue**: T0 defines the carrier set on which every property in the ASN depends — T3 says it holds "by the definition of the carrier set," and T1 quantifies over T — yet T0 never appears as a formal property block. Similarly, `≼` (PrefixRelation) is invoked by name in the proofs of T10, T10a, and GlobalUniqueness, and is listed as a load-bearing foundation of T10a, but no property block states its definition. The semantics of both are recoverable from context, but as formal dependencies they are missing links: a verifier tracing the chain from GlobalUniqueness back to axioms encounters two undefined symbols.
**What needs resolving**: T0 and Prefix need formal property blocks with definitions and contracts, or the ASN's declared-depends must cite the ASN that defines them.

---

### T6, T7 — dangling references
**Foundation**: (internal consistency — referential integrity)
**ASN**: T10a Consequence 4: *"Properties T4a–T4c, T6, T7, and all downstream consumers of T4 are guaranteed their precondition by the discipline itself (T10a.4)."*
**Issue**: T6 and T7 appear nowhere else in this ASN — not defined, not stated, not in the declared-depends metadata, not referenced by any other property or proof. They are cited as beneficiaries of T10a.4's guarantee, which means their preconditions supposedly include T4, but without knowing what T6 and T7 assert, this claim is unverifiable. If they are internal properties, their statements are missing. If they are in another ASN, the dependency is undeclared.
**What needs resolving**: Either define T6 and T7 within this ASN, add the external ASN to declared-depends, or remove the dangling references from T10a.4.

---

### Seven sub-properties cited as dependencies but lacking formal statements
**Foundation**: (internal consistency — proof chain completeness)
**ASN**: T4 body: *"We verify three consequences — T4a (SyntacticEquivalence), T4b (UniqueParse), T4c (LevelDetermination)"*; TA5 section summary table lists TA5-SIG, TA5-SigValid, TA5a with status "introduced" or "proved"; T10a justification: *"TA5a (IncrementPreservesT4), which establishes that inc(t, k) preserves T4 iff..."*
**Issue**: T4a, T4b, T4c, TA5-SIG, TA5-SigValid, and TA5a are cited as results — with specific postconditions attributed to them — but none has a formal property block with statement and proof in the document body. TA5a is particularly load-bearing: T10a.4 depends on it for the induction step ("TA5a guarantees that `inc(·, 0)` unconditionally preserves T4"), and GlobalUniqueness Case 3 depends on T4c for the zero-count level determination. T4b establishes well-definedness of `fields(t)`, which T4 itself references. The summary table and parenthetical citations describe what these properties claim, but a cross-property review cannot verify that the claimed postconditions actually follow from the stated preconditions when the proofs are absent.
**What needs resolving**: Each of these seven sub-properties needs a formal property block — statement, preconditions, proof, and contract — or an explicit indication that they reside in a separately-reviewed section with a cross-reference.
