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

### [REVIEW-46] [VERIFIED] D-CTG

### [REVIEW-46] [RESOLVED] D-CTG

### [REVIEW-46] [VERIFIED] D-CTG-depth

### [REVIEW-46] [FOUND] D-MIN
RESULT: FOUND

**Problem**: The property section contains no proof of D-MIN. The paragraph beginning "We now derive the general form" is circular — it invokes D-MIN itself ("By D-MIN, min(V_S(d)) = [S, 1, …, 1], so those shared components have value 1") to conclude that shared components are 1 and the minimum last component is 1. That paragraph derives *consequences* of D-MIN (the [S, 1, …, 1, k] structure), not D-MIN itself.

The listed dependencies cannot establish D-MIN:
- D-CTG + S8-fin establish that V_S(d) is a finite contiguous block.
- D-CTG-depth establishes that at depth m ≥ 3, all positions share components 2 through m − 1.
- But none of these constrain *where* the block starts. V_S(d) = {[S, 5, 3, k] : 1 ≤ k ≤ n} satisfies D-CTG, D-CTG-depth, S8-depth, and S8-fin equally well. Nothing forces the shared prefix to be [S, 1, …, 1] or the minimum last component to be 1.

Additionally, no `*Formal Contract:*` section is provided (checklist item 6).

**Required**:
1. **Clarify the status of D-MIN.** If it is an axiom (a design constraint that V-position numbering starts at 1, paralleling Nelson's "addresses 1 through 100" and the tumbler convention that ordinals begin at 1 as noted at the end of the D-CTG-depth section), declare it as such with an axiom formal contract. If it is a theorem, provide a non-circular proof — this would require dependencies not currently listed (e.g., properties of how the initial document state assigns V-positions, and how each operation preserves the minimum).
2. **Add a formal contract.** If axiom: `*Formal Contract:* — *Axiom:* min(V_S(d)) = [S, 1, …, 1] for every document d and subspace S with V_S(d) non-empty.` If theorem: preconditions (V_S(d) non-empty, S8-depth, etc.) and postcondition (`min(V_S(d)) = [S, 1, …, 1]`).
3. **Separate the corollary.** The "general form" derivation (every position is [S, 1, …, 1, k] for 1 ≤ k ≤ n) is a valid consequence of D-MIN + D-CTG-depth + D-CTG + S8-fin, but it should be clearly labeled as a corollary that follows *from* D-MIN, not as the proof *of* D-MIN.

### [REVIEW-47] [VERIFIED] D-MIN

### [REVIEW-47] [RESOLVED] D-MIN

### [REVIEW-47] [FOUND] S2
```
RESULT: FOUND

**Problem**: The property section has no `*Formal Contract:*` section. S2 declares that `Σ.M(d)` is a function by design — the narrative says "This is inherent in the concept of a 'virtual byte stream'" — making it an axiom, not a derived result. The formal contract must capture this.

**Required**: Append a formal contract to the property section:

```
*Formal Contract:*
- *Axiom:* For each document d, Σ.M(d) is a function — every v ∈ dom(Σ.M(d)) maps to exactly one I-address
```
```

### [REVIEW-48] [VERIFIED] S2

### [REVIEW-48] [RESOLVED] S2

### [REVIEW-48] [VERIFIED] S8

### [REVIEW-48] [VERIFIED] S1

### [REVIEW-48] [FOUND] S3
RESULT: FOUND

**Problem**: S3 has no proof and no formal contract. The property section contains only a weakest-precondition *analysis* — it describes what operations *would need to satisfy* to preserve S3, but never formally establishes that S3 holds as an invariant. The only `*Proof.*` block and `*Formal Contract:*` block present belong to the S1 dependency, not to S3 itself.

Specifically, proving S3 as an invariant requires two obligations:

1. **Base case**: S3 holds in the initial state (trivially, if `M(d)` is empty for all `d`, or by construction).
2. **Inductive step**: Every state transition `Σ → Σ'` preserves S3. This has two sub-cases:
   - *New mappings*: Any operation adding `M(d)(v) = a` ensures `a ∈ dom(Σ'.C)`. The wp discussion sketches this but doesn't prove it — it states the requirement without showing all operations satisfy it.
   - *Existing mappings*: References valid in `Σ` remain valid in `Σ'`. This follows from S1 (`dom(Σ.C) ⊆ dom(Σ'.C)`), but the derivation is never written out.

The narrative at "a valid reference cannot become dangling through any subsequent state transition" is the right argument for the second sub-case, but it appears as prose commentary, not as a proof step.

**Required**: 
1. Add a `*Proof.*` block for S3 that establishes both the base case and the inductive step (citing S1 for preservation of existing references, and either enumerating operations or declaring the wp constraint as an axiom for new references).
2. Add a `*Formal Contract:*` for S3. Based on the property's nature as a state invariant, it should be:
   ```
   *Formal Contract:*
   - *Invariant:* (A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))
   ```

### [REVIEW-49] [FOUND] S3
RESULT: FOUND

**Problem**: The proof explicitly introduces an axiom in Case 2 — "We take this as an axiom: every arrangement-modifying operation that introduces a mapping `M(d)(v) = a` ensures `a ∈ dom(Σ'.C)` in the post-state" — but the formal contract does not reflect it. The contract lists only the invariant:

```
*Formal Contract:*
- *Invariant:* `(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))`
```

This axiom is load-bearing: without it, Case 2 has no justification and the inductive step fails. The narrative describes it as "a design constraint on all arrangement-modifying operations, parallel to S0's constraint on content-store operations," yet unlike S0 (which is a standalone property that S1 depends on), this constraint exists only as inline prose within the proof. It is neither a declared dependency nor captured in the formal contract.

Two checklist items are violated:

- **#6 (Formal contract)**: The narrative states an axiom; the formal contract omits it. The contract does not match the conditions stated in the proof.
- **#7 (Missing guarantees)**: The proof assumes a guarantee — that arrangement-modifying operations ensure target I-addresses exist in `dom(Σ'.C)` — that no provided dependency (S1) establishes. S1 gives domain monotonicity of `C`, but says nothing about what arrangement operations must do.

**Required**: Either:

(a) Add the axiom to the formal contract, e.g.:
```
*Formal Contract:*
- *Axiom:* Every arrangement-modifying operation introducing `M(d)(v) = a` ensures `a ∈ dom(Σ'.C)`.
- *Invariant:* `(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))`
```

or (b) factor the constraint out as a standalone property (the arrangement analog of S0) and declare it as a dependency of S3 — then add it to the formal contract as a precondition, following the pattern S1 uses for S0.

### [REVIEW-50] [FOUND] S3
**Checking the proof against the verification checklist:**

1. **Precondition completeness** — Base case assumes `dom(Σ₀.M(d)) = ∅` for all `d` (reasonable initial-state assumption). Inductive step uses S1 and the arrangement axiom. ✓

2. **Case coverage** — Case 1 condition: `v ∈ dom(Σ.M(d)) ∧ Σ'.M(d)(v) = Σ.M(d)(v)`. Case 2 condition: `v ∉ dom(Σ.M(d)) ∨ Σ'.M(d)(v) ≠ Σ.M(d)(v)`. These are logical complements — exhaustive. ✓

3. **Postcondition establishment** — Both cases conclude `Σ'.M(d)(v) ∈ dom(Σ'.C)` for arbitrary `d, v`. ✓

4. **All conjuncts addressed** — Single universal quantification, no conjunction. ✓

5. **Dependency correctness** — S1 is declared and used in Case 1 (preserved mapping chain: `dom(Σ.C) ⊆ dom(Σ'.C)`). No undeclared dependencies used. ✓

6. **Formal contract** — Issue found. The proof explicitly relies on S1 in Case 1: without store monotonicity, a preserved mapping's I-address target could leave `dom(C)`, breaking referential integrity for unchanged mappings. The formal contract lists the arrangement axiom and the invariant but omits S1 as a precondition entirely. Compare with S1's own formal contract, which lists its dependency on S0 as a precondition: `"Preconditions: State transition Σ → Σ' in a system satisfying S0."` S3 should follow the same pattern.

7. **Missing guarantees** — The arrangement axiom is explicitly declared. No hidden assumptions. ✓

```
RESULT: FOUND

**Problem**: The formal contract omits the dependency on S1 (store monotonicity).
Case 1 of the inductive step chains through S1: `Σ.M(d)(v) ∈ dom(Σ.C) ⊆ dom(Σ'.C)` —
the subset inclusion `dom(Σ.C) ⊆ dom(Σ'.C)` IS S1. Without it, a preserved mapping's
target could vanish from `dom(C)` across a transition, and the case fails.
S1's own formal contract sets the precedent by listing its dependency on S0 as a
precondition. S3's contract should do likewise.

**Required**: Add a Preconditions field to the formal contract:

*Formal Contract:*
- *Preconditions:* State transitions satisfy S1 (store monotonicity).
- *Axiom:* Every arrangement-modifying operation introducing a mapping `M(d)(v) = a` ensures `a ∈ dom(Σ'.C)` in the post-state.
- *Invariant:* `(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))`
```

### [REVIEW-51] [VERIFIED] S3

### [REVIEW-51] [RESOLVED] S3

### [REVIEW-51] [VERIFIED] S8a

### [REVIEW-51] [FOUND] ValidInsertionPosition
## Verification of ValidInsertionPosition

Working through the checklist:

**1. Precondition completeness** — The property assumes d satisfies D-CTG, D-MIN, S8-depth, and S8a. The document-level precondition names only D-CTG ("document d satisfying D-CTG") but freely uses D-MIN, S8-depth, and S8a throughout. This is tolerable for the narrative but would need to be explicit in a formal contract.

**2. Case coverage** — Exhaustive: V_S(d) is either empty or non-empty. The j=0 case correctly handles the OrdinalShift precondition n ≥ 1 by defining it separately as v = min(V_S(d)).

**3. Postcondition establishment** — All structural claims are established with explicit reasoning:
- Explicit form via D-MIN + OrdinalShift + TumblerAdd ✓
- Distinctness via distinct last components + T3 ✓
- Depth preservation via OrdinalShift result-length identity (j ≥ 1) and D-MIN (j = 0) ✓
- Subspace identity via action point m ≥ 2 keeping component 1 unchanged ✓
- S8a consistency via all components strictly positive ✓
- The m ≥ 2 lower bound is justified by the counterexample at m = 1 ✓

**4. All conjuncts addressed** — Each claimed property (distinctness, depth, subspace, S8a, count) is proved.

**5. Dependency correctness** — All declared dependencies are used: D-CTG (constraint on d), D-MIN (minimum position form), S8-depth (common depth), S8a (well-formedness), OrdinalShift (shift definition and result-length), TumblerAdd (component-wise behavior), T3 (distinctness), T4/hierarchical structure (subspace identifier semantics). No undeclared dependencies.

**6. Formal contract** — Missing.

**7. Missing guarantees** — No missing guarantees from dependencies. The reasoning is sound given the provided axioms and definitions.

---

```
RESULT: FOUND

**Problem**: The property has no formal contract section. ValidInsertionPosition is
a definition with verified structural postconditions, but the required
`*Formal Contract:*` block is absent. The checklist requires: "If the formal
contract is missing or incomplete, flag as FOUND."

**Required**: Add a formal contract after the S8a consistency paragraph (before the
examples). It should capture the definition, its preconditions, and the verified
structural guarantees. For example:

*Formal Contract:*
- *Preconditions:* d satisfies D-CTG, D-MIN, S8-depth, S8a; S ≥ 1 (subspace
  identifier).
- *Definition:* v is a valid insertion position in subspace S of d when:
  (1) V_S(d) ≠ ∅ with |V_S(d)| = N: v = min(V_S(d)) or v = shift(min(V_S(d)), j)
  for 1 ≤ j ≤ N; (2) V_S(d) = ∅: v = [S, 1, …, 1] of depth m ≥ 2.
- *Postconditions:* #v = m (depth preservation); v₁ = S (subspace identity);
  zeros(v) = 0 ∧ v > 0 (S8a consistency); in the non-empty case, exactly N + 1
  valid positions, pairwise distinct by T3.
```

### [REVIEW-52] [VERIFIED] ValidInsertionPosition

### [REVIEW-52] [RESOLVED] ValidInsertionPosition

### [REVIEW-52] [VERIFIED] D-SEQ

### [REVIEW-52] [VERIFIED] S6

### [REVIEW-52] [VERIFIED] S5

### [REVIEW-52] [VERIFIED] S9

### [REVIEW-52] [VERIFIED] Σ.C

### [REVIEW-52] [VERIFIED] Σ.M(d)

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

## Surface Check: ASN-0036

### 1. Stale Labels

**Finding 1** — D-CTG-depth proof, paragraph beginning "The strict inequality at component j follows from v₁ < v₂":

> "The strict inequality at component j follows from v₁ < v₂ by T1(i) **(LexicographicOrdering, ASN-0034)**"

T1 is labeled **LexicographicTotalOrder** in the foundation. "LexicographicOrdering" does not exist.

**Finding 2** — D-SEQ proof, Step 3, paragraph beginning "Let k₁ < k₂ be two values attained":

> "By T1(i) **(TumblerOrdering, ASN-0034)**, v₁ < v₂ since they agree on components 1 through m − 1"

T1 is labeled **LexicographicTotalOrder** in the foundation. "TumblerOrdering" does not exist.

### 2. Structural Drift

(none)

### 3. Local Redefinitions

(none)

### 4. Registry Misclassification

(none)

### 5. Missing Dependencies

(none)

### 6. Exhaustiveness Gaps

(none)

---

`RESULT: 2 FINDINGS`
