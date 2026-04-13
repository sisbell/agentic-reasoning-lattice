# Proof Review — ASN-0036 (cycle 1)

*2026-04-13 13:45*

32 properties

### S0

Looking at property S0 against the verification checklist:

**1. Precondition completeness** — Fine. The property is universally quantified over all state transitions and all addresses; no additional preconditions needed.

**2. Case coverage** — Fine. The implication `a ∈ dom(Σ.C) ⟹ ...` correctly handles the vacuous case where `a ∉ dom(Σ.C)`.

**3. Postcondition establishment** — Fine for a foundational invariant. The property is described as "the central invariant of the two-stream architecture," positioning it as a design axiom that each operation must individually satisfy.

**4. All conjuncts addressed** — The narrative correctly identifies both conjuncts: address persistence (`a ∈ dom(Σ'.C)`) and value immutability (`Σ'.C(a) = Σ.C(a)`). The wp formulation restates both.

**5. Dependency correctness** — No dependencies declared, none used. Consistent.

**6. Formal contract** — The property section does not end with a `*Formal Contract:*` section. As a state invariant (axiom by design), it should have:

```
*Formal Contract:*
- *Axiom:* a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a) for every transition Σ → Σ'
```

**7. Missing guarantees** — No external guarantees assumed. Sound.

---

```
RESULT: FOUND

**Problem**: Missing formal contract. The property section ends with the wp elaboration but has no `*Formal Contract:*` block. Since S0 is described as "the central invariant of the two-stream architecture" and has no dependencies (it is not derived), it is an axiom — a design constraint that every operation must satisfy.

**Required**: Append a formal contract to the property section:
    *Formal Contract:*
    - *Axiom:* a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a) for every transition Σ → Σ'
```

### S7b

## Verification of S7b (Element-level I-addresses)

**Checklist:**

1. **Precondition completeness** — OK. The property quantifies over `dom(Σ.C)` and uses `zeros(a)` from T4. No unstated assumptions.

2. **Case coverage** — OK. Single universal quantification, no case split needed.

3. **Postcondition establishment** — OK. This is a design requirement (axiom), not a derived result. No proof is needed.

4. **All conjuncts addressed** — OK. Single conjunct: `zeros(a) = 3`.

5. **Dependency correctness** — OK. The narrative cites T4's field correspondence for `zeros(a) = 3 ↔` element-level. T4c establishes exactly this bijection. Dependency is used and correctly applied.

6. **Formal contract** — **MISSING.** The property section ends after the narrative paragraph with no `*Formal Contract:*` block.

7. **Missing guarantees** — OK. `zeros` and the level correspondence come from T4, which is provided.

```
RESULT: FOUND

**Problem**: No `*Formal Contract:*` section. The property is described as
"a design requirement" — an axiom imposed on valid states — but lacks the
formal contract block that makes this status explicit.

**Required**: Add a formal contract. Since S7b is a design requirement
(asserted, not derived from other properties), the appropriate form is:

    *Formal Contract:*
    - *Axiom:* (A a ∈ dom(Σ.C) :: zeros(a) = 3)
    - *Preconditions:* T4 (HierarchicalParsing) — provides the definition
      of zeros(t) and the level correspondence zeros(t) = 3 ↔ element address.
```

### S7a

## Verification of S7a

**Checklist analysis:**

1. **Precondition completeness** — S7a is stated as "a design requirement, not a convention." No proof is needed for an axiom, but the axiom must be precisely stated.

2–5. **Case coverage, postcondition establishment, conjuncts, dependency correctness** — N/A for an axiom (no proof to check). However, S7 and T4 are listed as "dependencies referenced by this proof," yet S7a has no proof. Moreover, the dependency direction is inverted: S7 depends ON S7a (S7's proof reads "S7 follows from S7a…"), not the other way around.

6. **Formal contract** — The property section for S7a has **no `*Formal Contract:*` block**. Since S7a is an axiom/design requirement, it needs an axiom-type contract stating the guarantee precisely. This is the contract that S7's proof cites when it says "By S7a (document-scoped allocation)…".

7. **Truncated text** — The property section ends with: *"Since Istream addresses designate content elements within documents, we require:"* — and then nothing follows. The requirement is never stated.

---

```
RESULT: FOUND

**Problem**: S7a has no `*Formal Contract:*` section. The property is described as
"a design requirement, not a convention" (i.e., an axiom), but the axiom is never
given a formal contract. S7's proof (in the Dependencies section) relies on S7a as
a premise ("By S7a…"), so the precise guarantee must be stated contractually.
Additionally, the property section text is truncated at "we require:" — the
sentence is incomplete and the actual requirement is never stated.

**Required**: Add a formal contract to S7a. Since it is an axiom, something like:

  *Formal Contract:*
  - *Axiom:* For every `a ∈ dom(Σ.C)`, the document-level prefix
    `origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)`
    is the tumbler of the document whose owner allocated `a`.
  - *Preconditions:* `zeros(a) ≥ 2` (T4 field correspondence ensures the
    document field exists).

Complete the truncated sentence ending "we require:" — this appears to introduce
the domain restriction (likely `zeros(a) = 3`, per S7b) but is cut off before
stating it.
```

### S7c

Looking at S7c as a design requirement (axiom), I'll work through the checklist.

**1–5**: S7c is an axiom — a design requirement imposed on `dom(Σ.C)`, not a derived property. The narrative correctly explains *why* the constraint is needed: at `δ = 1`, the subspace identifier IS the content ordinal, breaking TA7a's ordinal-only formulation. Dependencies (T4, S7b, T10a, TA7a) are used correctly as motivation, not as derivation steps. No proof is required.

**6. Formal contract**: The property section has **no `*Formal Contract:*` block**. The text ends with:

> "(S7c, stated here for architectural completeness, is load-bearing for S8-depth's ordinal shift analysis below, not for S7 itself.)"

As a design requirement, S7c needs an axiom contract. Something like:

```
*Formal Contract:*
- *Axiom:* (A a ∈ dom(Σ.C) :: #fields(a).element ≥ 2)
```

**7. Missing guarantees**: None — S7c is an axiom, not derived.

```
RESULT: FOUND

**Problem**: S7c has no formal contract section. Every property requires one per the specification conventions. S7c is a design requirement (axiom) constraining element-field depth, and its formal statement `(A a ∈ dom(Σ.C) :: #fields(a).element ≥ 2)` needs to appear in a contract block.

**Required**: Append a formal contract to the S7c property section:

    *Formal Contract:*
    - *Axiom:* (A a ∈ dom(Σ.C) :: #fields(a).element ≥ 2)
```

### S8-depth

## Analysis

**S8-depth** is explicitly declared a "design requirement, not a convention" — i.e., an axiom. The core claim is clear and the formal quantifier matches the narrative. The derived consequences (consecutive V-positions, I-address uniformity within runs, subspace preservation) follow soundly from OrdinalShift and S7c:

- **Prefix preservation**: OrdinalShift postcondition `shift(v,n)ᵢ = vᵢ for i < m` guarantees all components except the last are unchanged. The subspace identifier (component 1) is preserved since `1 < m` for any non-trivial address.
- **Depth preservation**: OrdinalShift postcondition `#shift(v,n) = #v` gives same-length result.
- **I-address subspace preservation**: S7c (`δ ≥ 2`) ensures the subspace identifier `E₁` is not the last component, so OrdinalShift leaves it untouched.
- **k = 0 extension**: Correctly handled as a notational convention separate from OrdinalShift's `n ≥ 1` precondition.

The correspondence run definition `(v, a, n)` references `Σ.M(d)` but `d` is not part of the triple — it's only implicitly bound from the surrounding S8-depth context. This is a minor notational gap.

However:

```
RESULT: FOUND

**Problem**: The property section has no `*Formal Contract:*` section. S8-depth is an axiom (design requirement), and the section also introduces the correspondence run definition. Neither has a formal contract. The correspondence run definition additionally omits document `d` from the triple — it references `Σ.M(d)(v + k)` but `d` is not a parameter of the triple `(v, a, n)`, leaving it implicitly bound.

**Required**: Add a formal contract. For example:

*Formal Contract:*
- *Axiom:* `(A d, v₁, v₂ : v₁ ∈ dom(Σ.M(d)) ∧ v₂ ∈ dom(Σ.M(d)) ∧ (v₁)₁ = (v₂)₁ : #v₁ = #v₂)`
- *Definition:* A correspondence run in document `d` is a triple `(v, a, n)` with `n ≥ 1` such that `(A k : 0 ≤ k < n : Σ.M(d)(v + k) = a + k)`, where `v + 0 = v`, `a + 0 = a`, and for `k ≥ 1`, `v + k = shift(v, k)`, `a + k = shift(a, k)`.

Either bind `d` explicitly in the correspondence run definition or make the triple a quadruple `(d, v, a, n)`.
```

### S8-fin

RESULT: FOUND

**Problem 1 — Missing formal contract.** The property section has no `*Formal Contract:*` block. S8-fin is a state invariant asserting finiteness of `dom(Σ.M(d))` across all reachable states. It needs:

```
*Formal Contract:*
- *Invariant:* dom(Σ.M(d)) is finite for every document d in every reachable state Σ
```

**Problem 2 — Proof assumes per-operation finiteness without grounding.** The argument asserts "No operation introduces infinitely many V-positions" as self-evident, but this is the core claim that needs justification. The proof is structurally an induction over the operation history:

- **Base case** (initial state): not stated. Must establish that the initial `dom(M(d))` is finite (presumably empty).
- **Inductive step**: each operation preserves finiteness — i.e., if `dom(M(d))` is finite before an operation, it is finite after. This requires citing or establishing that INSERT, COPY, etc. each add only finitely many V-positions.

Neither step is explicitly given, and no dependencies are declared to support the claim. The argument as written is an informal appeal to "operational reality" rather than a derivation from stated properties.

**Required**:
1. Add the formal contract as shown above.
2. Either (a) declare dependencies on the individual operation definitions/properties that establish each operation adds finitely many V-positions, and cite them explicitly, or (b) restructure the proof as an explicit induction with base case and inductive step, grounding the per-operation finiteness claim in the operation specifications.

### S3

## Verification

**S3 (Referential integrity):** `(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))`

**Checklist analysis:**

1. **Precondition completeness** — The narrative identifies that S1 is needed (content persistence prevents dangling references after creation), and discusses weakest-precondition reasoning for add-mapping operations. However, this is informal discussion, not a structured argument.

2. **Case coverage** — The narrative covers: (a) adding a V-mapping where target already exists, (b) atomically creating content and adding a mapping, (c) S1 preventing previously-valid references from becoming dangling. It does *not* cover operations that **modify** an existing V-mapping `M(d)(v)` to point to a different address, or operations that **rearrange** documents. These could introduce dangling references if the new target is not in `dom(C)`.

3. **Postcondition establishment** — There is no `*Proof.*` block and no QED (∎) for S3. The section contains informal reasoning about weakest preconditions and design asymmetry but never formally establishes that S3 holds as an invariant across all state transitions.

4. **All conjuncts addressed** — Single conjunct, but not formally proved.

5. **Dependency correctness** — S1 is referenced in the narrative and declared as a dependency. Correct usage.

6. **Formal contract** — **Missing entirely.** The S3 section ends with narrative text and has no `*Formal Contract:*` block.

7. **Missing guarantees** — The narrative implicitly assumes that all operations creating or modifying V-mappings ensure the target I-address is in `dom(C)` at the time of the transition. No property in the provided dependencies establishes this — it would need to come from per-operation postconditions or an explicit axiom about well-formed operations.

```
RESULT: FOUND

**Problem**: S3 has no proof and no formal contract. The property section provides
informal weakest-precondition reasoning and design commentary, but there is no
`*Proof.*` block establishing that S3 is preserved across all state transitions,
and no `*Formal Contract:*` section. Additionally, the informal reasoning omits
the case where an existing V-mapping is *modified* (M(d)(v) repointed to a
different address) — only addition of new mappings is discussed.

**Required**:
1. Add a `*Proof.*` block that either (a) proves S3 is an invariant maintained
   by all state transitions, covering addition, modification, and removal of
   V-mappings, citing S1 for the "no dangling from content removal" direction
   and per-operation preconditions for the "no dangling from mapping creation"
   direction; or (b) explicitly classifies S3 as an axiom/design requirement
   that constrains the set of valid operations.
2. Add a `*Formal Contract:*` section. If S3 is an invariant:
   - *Preconditions:* S1 (store monotonicity); all operations adding or modifying
     V-mappings ensure target I-addresses are in dom(Σ'.C).
   - *Invariant:* (A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))
3. If the per-operation precondition "target must be in dom(C)" is not established
   by an existing property, create a new property or axiom that formalizes this
   constraint on well-formed operations.
```

### ValidInsertionPosition

Looking at the ValidInsertionPosition property section against the verification checklist:

**1. Precondition completeness** — Adequate. The two cases (empty/non-empty) are stated with their conditions. The m ≥ 2 bootstrapping argument (empty case establishes it, S8-depth preserves it) is sound.

**2. Case coverage** — Exhaustive. Empty and non-empty partition all possibilities for V_S(d).

**3. Postcondition establishment** — The four structural claims (distinctness, depth preservation, subspace identity, S8a consistency) are each shown explicitly.

**4. All conjuncts addressed** — Distinctness, depth, subspace, S8a — all verified. The explicit form shift(min, j) = [S, 1, …, 1+j] is derived. The count N+1 follows from the definition plus distinctness.

**5. Dependency correctness** — D-MIN, D-CTG, S8-depth, S8a, T3 are all used as claimed. OrdinalShift, TumblerAdd, and T0(a) from ASN-0034 are used and cited but not listed in the provided dependencies — acceptable as cross-ASN references. No declared dependency goes unused.

**6. Formal contract** — **Missing.** The property section has no `*Formal Contract:*` block.

**7. Missing guarantees** — No unstated assumptions found. All reasoning chains terminate at provided dependencies or named ASN-0034 properties.

```
RESULT: FOUND

**Problem**: The ValidInsertionPosition definition has no `*Formal Contract:*` section. Every other dependency provided (D-CTG, S8-depth, D-MIN, S8a, T3) includes one, and the checklist requires it.

**Required**: Append a formal contract to the property section. Given that this is a definition with preconditions and postconditions, something like:

*Formal Contract:*
- *Definition:* A V-position v is a valid insertion position in subspace S of document d when either (1) V_S(d) ≠ ∅ with |V_S(d)| = N and v = shift(min(V_S(d)), j) for 0 ≤ j ≤ N (where shift(min, 0) = min), or (2) V_S(d) = ∅ and v = [S, 1, …, 1] of depth m ≥ 2.
- *Preconditions:* d satisfies D-CTG; S is a subspace identifier (S ≥ 1); S8-depth holds for V_S(d); D-MIN holds for V_S(d).
- *Postconditions:* All valid insertion positions satisfy #v = m (depth preservation), v₁ = S (subspace identity), zeros(v) = 0 ∧ v > 0 (S8a consistency); in the non-empty case, the N + 1 positions are pairwise distinct (by T3).
```

### S2

RESULT: FOUND

**Problem**: The property section has no `*Formal Contract:*` block. S2 is an axiom — it is declared as "inherent in the concept of a virtual byte stream" and is not derived from other properties (no dependencies). It requires an `Axiom` field in the formal contract. Additionally, the section ends with the incomplete sentence fragment "The bridge between the two state components is a well-formedness condition:" which trails off without completing the thought.

**Required**:
1. Append a formal contract to the property section, e.g.:
   ```
   *Formal Contract:*
   - *Axiom:* Σ.M(d) is a function — each v ∈ dom(Σ.M(d)) maps to exactly one I-address
   ```
2. Complete or remove the trailing fragment "The bridge between the two state components is a well-formedness condition:" — as written it introduces an idea but provides no content.

23 verified, 9 found.
