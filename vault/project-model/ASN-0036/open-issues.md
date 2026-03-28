### Finding 1: [stale-label] GlobalUniqueness
**Location**: deps:S4
**Detail**: Property S4 references GlobalUniqueness which does not exist in any active ASN's export

### Finding 2: [stale-label] GlobalUniqueness
**Location**: deps:S7
**Detail**: Property S7 references GlobalUniqueness which does not exist in any active ASN's export

### Finding 3: [stale-label] T0(a)
**Location**: deps:D-CTG
**Detail**: Property D-CTG references T0(a) which does not exist in any active ASN's export

### Finding 4: [stale-label] T0(a)
**Location**: deps:D-CTG-depth
**Detail**: Property D-CTG-depth references T0(a) which does not exist in any active ASN's export

### Finding 5: [stale-label] OrdinalShift
**Location**: deps:ValidInsertionPosition
**Detail**: Property ValidInsertionPosition references OrdinalShift which does not exist in any active ASN's export

### Finding 6: [stale-label] TumblerAdd
**Location**: deps:ValidInsertionPosition
**Detail**: Property ValidInsertionPosition references TumblerAdd which does not exist in any active ASN's export

### Finding 7: [prose-only] T0 (ASN-0034)
**Location**: prose
**Detail**: Prose cites T0 (ASN-0034) but no property table entry lists it in follows_from

## Category 1: Stale Labels

(none)

All foundation labels cited in ASN-0036 (T0, T0(a), T1, T3, T4, T5, T8, T9, T10, T10a, TA5, TA7a, TumblerAdd, OrdinalShift, GlobalUniqueness, etc.) exist in the current ASN-0034 foundation.

---

## Category 2: Structural Drift

(none)

All cited foundation content is consistent with current ASN-0034 statements. T8 is cited as `allocated(s) ⊆ allocated(s')` — matches. GlobalUniqueness is cited as "for every pair of addresses produced by distinct allocation events: a ≠ b" — matches. T4 field structure, T5 prefix contiguity, TA5 sub-properties (a)–(d), and TumblerAdd constructive definition are all used accurately.

---

## Category 3: Local Redefinitions

**S4 (Origin-based identity)** is listed under "Properties Introduced" but is a direct instance of GlobalUniqueness (ASN-0034).

GlobalUniqueness (ASN-0034): *Invariant:* for every pair of addresses `a, b` produced by distinct allocation events in any reachable system state: `a ≠ b`. The precondition requires only that the allocations conform to T10a — no condition on stored values.

S4 (ASN-0036): "For I-addresses `a₁`, `a₂` produced by distinct allocation events: `a₁ ≠ a₂` regardless of whether `Σ.C(a₁) = Σ.C(a₂)`." Preconditions: `a₁, a₂ ∈ dom(Σ.C)`, distinct allocation events, T10a conformance.

S4 restricts GlobalUniqueness to `dom(Σ.C) ⊆ T` and annotates value independence — but GlobalUniqueness already covers all of T and its proof makes no reference to stored values. The S4 proof body confirms this: "GlobalUniqueness yields `a₁ ≠ a₂` directly." There is no additional mathematical work. S4 should be classified as a corollary cited from GlobalUniqueness (ASN-0034), not as an introduced property.

---

## Category 4: Registry Misclassification

(none)

---

## Category 5: Missing Dependencies

(none)

All foundation citations are to ASN-0034, which is the sole declared dependency.

---

## Category 6: Exhaustiveness Gaps

(none)

---

`RESULT: 1 FINDING`

### [REVIEW-39] [FOUND] S8-fin
## Verification of S8-fin

**Checklist analysis:**

1. **Precondition completeness** — The proof implicitly assumes a base case (initial state has finite or empty domain) but never states it.

2. **Case coverage** — The proof claims "no operation introduces infinitely many V-positions" without enumerating or citing the operations. This is asserted, not shown.

3. **Postcondition establishment** — The argument is an informal induction: finitely many operations, each adding finitely many V-positions, yields a finite domain. The reasoning structure is sound but relies entirely on unstated premises.

4. **All conjuncts addressed** — Single claim (finiteness), addressed.

5. **Dependency correctness** — No dependencies are declared. Yet the proof relies on two unstated guarantees: (a) the initial state has a finite domain for each document, and (b) each operation (INSERT, COPY, etc.) adds only finitely many V-positions. These are properties of the operation definitions that should either be cited as dependencies or the property should be reclassified as an axiom/design invariant.

6. **Formal contract** — **Missing.** S8-fin is a state invariant. It should have a formal contract such as:
   ```
   *Formal Contract:*
   - *Invariant:* dom(Σ.M(d)) is finite for every document d and every reachable state Σ
   ```

7. **Missing guarantees** — The proof assumes each operation introduces finitely many V-positions. No dependency establishes this. Either individual operation ASNs need a finiteness guarantee, or this property should be declared axiomatic (justified by design rather than derived).

---

```
RESULT: FOUND

**Problem**: No formal contract is present. The proof appeals to "operational reality"
and asserts that each operation introduces finitely many V-positions, but declares no
dependencies that establish this. The base case (initial state has finite domain) is
also unstated. The argument is structurally an induction over operations but is
presented as self-evident.

**Required**: (1) Add a formal contract with an Invariant field:
  *Formal Contract:*
  - *Invariant:* dom(Σ.M(d)) is finite for every document d and every reachable state Σ
(2) Either declare dependencies on the operation definitions that establish each
operation adds finitely many V-positions, or reclassify S8-fin as an axiom with
explicit justification that finiteness is a design constraint enforced by construction
(each operation is a finite act on a finite input).
```

### [REVIEW-40] [VERIFIED] S8-fin

### [REVIEW-40] [RESOLVED] S8-fin

### [REVIEW-40] [VERIFIED] S4

### [REVIEW-40] [FOUND] S7b
**Analysis of S7b**

S7b is a design requirement (axiom): every Istream address has exactly three zeros, meaning all four tumbler fields are present. It uses T4's field correspondence to interpret `zeros(a) = 3`. S7a appears only in the forward-looking sentence "With S7a and S7b established, we can state structural attribution" — it is not used to establish S7b itself.

**Checklist:**

1. **Precondition completeness** — OK. The domain `dom(Σ.C)` is the only input.
2. **Case coverage** — N/A (axiom, not a case-based proof).
3. **Postcondition establishment** — OK. Design requirement, asserted not derived.
4. **All conjuncts addressed** — OK. Single conjunct `zeros(a) = 3`.
5. **Dependency correctness** — S7a is declared as a dependency but never used to establish S7b. It is a co-requisite for downstream properties, not a dependency of this one. T4 is correctly used (field correspondence interpretation).
6. **Formal contract** — **Missing.** The property section has no `*Formal Contract:*` block. As a design axiom, it should have one.
7. **Missing guarantees** — None.

```
RESULT: FOUND

**Problem**: (a) No formal contract. S7b is a design axiom and needs a formal contract block. 
(b) S7a is listed as a dependency but is not used to establish S7b — it appears only in a forward-looking statement about downstream consequences.

**Required**: 
(a) Add a formal contract:
   *Formal Contract:*
   - *Axiom:* (A a ∈ dom(Σ.C) :: zeros(a) = 3)

(b) Remove S7a from S7b's dependency list. S7a is a co-requisite for the downstream "structural attribution" statement, not a dependency of S7b itself. If the downstream property needs both, it should declare both as its own dependencies.
```

### [REVIEW-41] [FOUND] S7b
## Verification of S7b

**S7b** is a design requirement (axiom) stating that every Istream address has exactly 3 zeros, placing it at the element level of the tumbler hierarchy. The formal contract correctly classifies this as an Axiom, and the axiom statement `(A a ∈ dom(Σ.C) :: zeros(a) = 3)` matches the narrative exactly.

**Checklist walkthrough:**

1. **Precondition completeness** — As an axiom, no preconditions needed beyond the domain `dom(Σ.C)`. Fine.
2. **Case coverage** — N/A for an axiom.
3. **Postcondition establishment** — N/A for an axiom; it is asserted by design.
4. **All conjuncts addressed** — Single conjunct (`zeros(a) = 3`). Covered.
5. **Dependency correctness** — The narrative justification says: *"By T4's field correspondence, `zeros(a) = 3` means all four identifying fields — node, user, document, element — are present."* This uses **T4** only. The sentence *"With S7a and S7b established, we can state structural attribution"* is a forward-looking remark about what S7a+S7b together enable — it is not S7b using S7a in its own reasoning. **S7a is declared as a dependency but never used.**
6. **Formal contract** — Present, uses the correct `Axiom` field, statement matches the narrative verbatim.
7. **Missing guarantees** — None; axiom needs no derivation.

```
RESULT: FOUND

**Problem**: S7a is listed as a dependency of S7b but is not referenced in S7b's
reasoning or justification. S7b's narrative uses only T4 ("By T4's field
correspondence, zeros(a) = 3 means all four identifying fields...are present").
The only mention of S7a is the transitional sentence "With S7a and S7b
established, we can state structural attribution" — this describes what the two
companion axioms jointly enable downstream, not a use of S7a in establishing S7b.

**Required**: Remove S7a from S7b's dependency list. The sole dependency is T4,
which defines zeros(t) and the field correspondence that gives zeros(a) = 3 its
semantic meaning as "element-level."
```

### [REVIEW-42] [VERIFIED] S7b

### [REVIEW-42] [RESOLVED] S7b

### [REVIEW-42] [FOUND] S0
RESULT: FOUND

**Problem**: The property section has no `*Formal Contract:*` section. S0 states a universal invariant over all state transitions but the section ends after the weakest-precondition restatement without a formal contract summarizing the invariant.

Additionally, the section's status is ambiguous: it describes what S0 *requires* of operations but never states whether S0 is an **axiom** (imposed by design on the two-stream architecture) or a **derived invariant** (proved by case analysis over all operations). The text "This is the central invariant of the two-stream architecture" and "This constrains every operation" reads as a design constraint, but if so it should be explicitly labeled as an axiom. If it is instead meant to be proved, no proof is present — there is no enumeration of operations and no per-operation argument that each preserves `dom(C)` membership and value equality.

**Required**:

1. Add a formal contract. If S0 is an axiom:
   ```
   *Formal Contract:*
   - *Invariant:* a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a) for every transition Σ → Σ'
   - *Axiom:* imposed as a design constraint on all content-store operations
   ```

2. If S0 is instead a derived property, provide the proof: enumerate every operation that produces a successor state Σ' and show that each either (a) does not modify `C`, or (b) only extends `dom(C)` at fresh addresses with new values, leaving all existing mappings intact. This would require declaring dependencies on the definitions of those operations.

### [REVIEW-43] [VERIFIED] S0

### [REVIEW-43] [RESOLVED] S0

### [REVIEW-43] [VERIFIED] S7

### [REVIEW-43] [FOUND] S7a
RESULT: FOUND

**Problem**: The property statement is truncated. The final paragraph introduces a further design requirement — "Since Istream addresses designate content elements within documents, we require:" — but never completes the sentence. The element-level constraint (presumably `zeros(a) = 3` for all `a ∈ dom(Σ.C)`) is motivated but never actually stated.

Additionally, no `*Formal Contract:*` section is present. S7a is explicitly described as "a design requirement, not a convention," which makes it an axiom. It should have a formal contract with an `*Axiom:*` field capturing both conjuncts:
1. Document-scoped allocation: the document-level prefix of every content address identifies its creating document.
2. The unstated element-level constraint on content addresses.

**Required**:
1. Complete the truncated sentence beginning "we require:" — state the element-level constraint explicitly (e.g., `zeros(a) = 3` for all `a ∈ dom(Σ.C)`).
2. Add a formal contract, e.g.:
   ```
   *Formal Contract:*
   - *Axiom:* (a) For every a ∈ dom(Σ.C), prefix(a, document) identifies the document
     whose owner allocated a. (b) For every a ∈ dom(Σ.C), zeros(a) = 3 (element-level).
   ```
3. Declare T1 as a dependency if the "Contiguous subtrees" remark (which references T1) is meant to support S7a, or remove that reference.

### [REVIEW-44] [VERIFIED] S7a

### [REVIEW-44] [RESOLVED] S7a

### [REVIEW-44] [FOUND] S8-depth
RESULT: FOUND

**Problem**: Missing formal contract. The property is explicitly described as "a design requirement, not a convention — parallel to S7a," yet S7a has a formal contract with an `*Axiom:*` field and S8-depth has none. The checklist requires: "If the formal contract is missing or incomplete, flag as FOUND."

Additionally, the property section embeds a definition (correspondence run) that should be formalized in the contract. The formal expression for the correspondence run is given inline:

> `(A k : 0 ≤ k < n : Σ.M(d)(v + k) = a + k)`

but is never promoted to a `*Definition:*` field.

**Required**: Add a `*Formal Contract:*` section at the end of the property, parallel to S7a's structure. It should include at minimum:

```
*Formal Contract:*
- *Axiom:* (A d, v₁, v₂ : v₁ ∈ dom(Σ.M(d)) ∧ v₂ ∈ dom(Σ.M(d)) ∧ (v₁)₁ = (v₂)₁ : #v₁ = #v₂)
- *Definition:* A *correspondence run* is a triple (v, a, n) with n ≥ 1 such that (A k : 0 ≤ k < n : Σ.M(d)(v + k) = a + k), where v + k and a + k denote ordinal displacement (TA7a) applied to V-positions and I-address element ordinals respectively.
```

### [REVIEW-45] [VERIFIED] S8-depth

### [REVIEW-45] [RESOLVED] S8-depth

### [REVIEW-45] [FOUND] D-CTG
RESULT: FOUND

**Problem 1 — Missing formal contract.** The property section has no `*Formal Contract:*` block. D-CTG is a design invariant (parallel to S8-fin), so it needs one. The corollary (depth ≥ 3 restriction) is a derived theorem and could also be captured.

**Required:** Add a formal contract. Minimally:
```
*Formal Contract:*
- *Invariant:* `(A d, S, u, q : u ∈ V_S(d) ∧ q ∈ V_S(d) ∧ u < q : (A v : subspace(v) = S ∧ #v = #u ∧ u < v < q : v ∈ V_S(d)))`
- *Axiom:* Every arrangement-modifying operation preserves V-contiguity within each subspace — this is a design constraint enforced by construction, parallel to S8-fin.
```

**Problem 2 — Undeclared dependency on T1(i).** The proof cites "By T1(i)" twice — once for `w > v₁` and once for `w < v₂` — but T1(i) (lexicographic tumbler ordering) is not listed in the Dependencies section. T0(a) and T3 are both declared from ASN-0034; T1(i) should be as well.

**Required:** Add T1(i) to the declared dependencies with its statement (lexicographic ordering: the first component at which two equal-length tumblers disagree determines their order).
