## Audit Trace

**S7b, S0, S7a, S7d, Σ.C** — These are presented without proof sections and function as axioms or definitions. Their internal consistency with each other and with the T10a/T4 foundation is coherent: S7a correctly requires A_element ∈ 𝒯 and a ∈ dom(A_element) to license T10a.4's instantiation; S7d separates documents at the event level, leaving GlobalUniqueness to handle tumbler-distinctness; S7b's `zeros(a) = 3` is correctly fed into T4b after T4-validity is established. No findings on these.

**S7 Well-definedness step** — The chain is: `a ∈ dom(Σ.C)` → S7a gives A_element ∈ 𝒯, a ∈ dom(A_element) → T10a.4 gives a T4-valid → S7b gives zeros(a) = 3 → T4b projections N(a), U(a), D(a), E(a) all defined → T4a gives each field nonempty → construct origin(a) by T0 comprehension at length p = #N(a)+1+#U(a)+1+#D(a) ≥ 5. The component map r is total into ℕ (field positions in ℕ⁺ ⊆ ℕ; separators in {0} ⊆ ℕ). T0 comprehension gives origin(a) ∈ T. T4's zero-count definition applied to r correctly identifies the zero-position set as {#N(a)+1, #N(a)+#U(a)+2}. These are distinct (difference = #U(a)+1 ≥ 2 by T4a non-emptiness). Two issues noted below.

**S7 Identification and Permanence steps** — Sound. Identification leans on S7a which is axiomatic; Permanence leans on S0 and the tumbler immutability (components of a do not change).

**S7 Uniqueness step** — The event-distinctness-to-address-distinctness bridge via GlobalUniqueness is correctly structured. One informational reference noted below.

---

### T4-validity of origin(a) absent from postconditions

**Class**: REVISE
**Foundation**: T4 (HierarchicalParsing) — T4-valid predicate requires zeros ≤ 3 AND the field-segment constraint (no adjacent zeros, nonzero first component, nonzero last component)
**ASN**: S7 Formal Contract — Postconditions state `zeros(origin(a)) = 2` and describe this as "placing origin(a) at the document level in T4's hierarchy," but do not assert that origin(a) is T4-valid
**Issue**: The Well-definedness step implicitly establishes all four T4-validity conditions for origin(a) — zeros(origin(a)) = 2 ≤ 3, no adjacent zeros (separator positions differ by #U(a)+1 ≥ 2), r(1) ∈ ℕ⁺ so first component ≠ 0, r(p) ∈ ℕ⁺ so last component ≠ 0 — but the formal contract does not synthesize these into an explicit T4-validity postcondition. A downstream consumer reading only the postconditions cannot derive T4-validity from `zeros(origin(a)) = 2` alone: zeros = 2 satisfies the count bound but says nothing about the field-segment constraint. If a downstream claim needs to apply T4b's projections to origin(a), or needs origin(a) to be a T4-conforming document address, the current postcondition does not supply the warrant.
**What needs resolving**: The postconditions must explicitly state that origin(a) is T4-valid. The Well-definedness step already has the material to discharge this (component map r places the first and last positions in ℕ⁺, and the two zero-separators are non-adjacent); those established facts should be assembled into a T4-validity conclusion.

---

### NAT-card missing from S7's Depends

**Class**: REVISE
**Foundation**: NAT-card (NatFiniteSetCardinality) — supplies the enumeration characterisation of `|·|` on finite subsets of ℕ
**ASN**: S7 Well-definedness step — "A set of two distinct indices has cardinality 2; therefore zeros(origin(a)) = 2"
**Issue**: S7 directly evaluates `|{#N(a)+1, #N(a)+#U(a)+2}| = 2` — a standalone cardinality claim — in its Well-definedness step. T4 supplies the zero-count *definition* `zeros(t) = |{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}|` and lists NAT-card in its own Depends for exactly that purpose. But S7 does not merely invoke T4's exported function: it opens the definition, reduces the index set to an explicit two-element set, and asserts the cardinality of that set equals 2. That assertion consumes NAT-card's enumeration characterisation directly. Every comparable claim in this ASN's cone that uses `|·|` reasoning lists NAT-card (T4, T4a, T4b). S7 does not.
**What needs resolving**: NAT-card must appear in S7's Depends list, with the role statement referencing the cardinality evaluation `|{#N(a)+1, #N(a)+#U(a)+2}| = 2` in Well-definedness.

---

### Undeclared S4 reference in S7 Uniqueness step

**Class**: OBSERVE
**Foundation**: N/A
**ASN**: S7 Uniqueness step — "the same theorem S4 invokes to separate I-addresses"
**Issue**: S4 appears in the proof text as an explanatory cross-reference but is not in S7's Depends list and is not presented in the ASN. The logical step is performed by GlobalUniqueness (which IS declared); the S4 mention is purely descriptive context. No inference in the proof depends on S4. However, the reference is an undeclared dependency in proof text and will become a stale annotation if S4 is later restructured or removed.
**What needs resolving**: Drop the parenthetical "the same theorem S4 invokes to separate I-addresses" from the proof text; the sentence reads correctly without it and GlobalUniqueness is the operative dependency.

---

VERDICT: REVISE