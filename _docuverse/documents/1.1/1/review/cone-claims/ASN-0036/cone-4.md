## Audit

### Dependency trace

The claim chain through S7 runs: `a ∈ dom(Σ.C)` → via S7a, two T10a memberships → via T10a.4, T4-validity of `a` → via S7b, `zeros(a) = 3` → via T4b, projections N(a), U(a), D(a) over ℕ⁺ → via T4a (forward), each field non-empty → T0 comprehension constructs `origin(a) ∈ T`. The Well-definedness step is structurally sound up to that construction. The Identification step correctly cites S7a as the axiomatic grounding for `origin(a) = allocating document's tumbler`. The Uniqueness step correctly chains S7d (distinct documents → distinct events) → GlobalUniqueness (distinct events → distinct addresses) → S7a (origin = document tumbler) to conclude `origin(a₁) ≠ origin(a₂)`. The Permanence step correctly uses S0 as a universal-over-all-transitions invariant, which by induction over transition sequences covers all future states.

The cross-claim consistency between S7, S7a, S7b, S7d, S0, and the foundation set is otherwise intact. One derivation step is missing.

---

### `zeros(origin(a)) = 2` asserted, not derived
**Class**: REVISE
**Foundation**: T4 (HierarchicalParsing) — definition `zeros(t) = |{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}|`
**ASN**: S7 Well-definedness — "T4 then reads its separator structure: `zeros(origin(a)) = 2`, placing it at the document level in T4's hierarchy."
**Issue**: The proof explicitly constructs `origin(a)` via T0 comprehension, naming the component map `r` that places exactly two zero-valued entries — at positions `#N(a)+1` and `#N(a)+#U(a)+2` — with all other entries in ℕ⁺ (hence nonzero, by T4b's strict-positivity postcondition). Having done this work, the proof then asserts `zeros(origin(a)) = 2` without applying T4's zero-count definition to `r`. The required step is: `zeros(origin(a)) = |{i : 1 ≤ i ≤ p ∧ r(i) = 0}|` (T4's definition instantiated at the constructed `origin(a)`) = `|{#N(a)+1, #N(a)+#U(a)+2}|` (by inspection of `r`). These two positions are distinct because `#U(a)+1 ≥ 2 > 1` (T4a's non-emptiness of the U field, already established in this proof paragraph), so the set has cardinality 2. That derivation step is absent; the conclusion `zeros(origin(a)) = 2` stands unsupported.
**What needs resolving**: The Well-definedness paragraph must apply T4's zero-count definition `zeros(t) = |{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}|` to the explicitly constructed component map `r`, enumerate the two zero positions, establish they are distinct (citing T4a's non-emptiness of U(a) to confirm `#N(a)+#U(a)+2 > #N(a)+1`), and derive `zeros(origin(a)) = 2` from the resulting cardinality — rather than asserting it from T4's "separator structure."

---

### Use-site inventory sentence in GlobalUniqueness Depends entry
**Class**: OBSERVE
**Foundation**: N/A
**ASN**: S7 Depends, GlobalUniqueness entry — "The same theorem S4 invokes for the I-address case."
**Issue**: The sentence does not explain what S7 requires from GlobalUniqueness; it describes how an unrelated claim (S4) also uses it. This is a use-site inventory comment in a structural slot. A reader following S7's dependency rationale must skip past it to reach nothing — it adds no information about the dependency.
**What needs resolving**: Remove the sentence. The preceding sentence already states the instantiation and consequence.

---

VERDICT: REVISE