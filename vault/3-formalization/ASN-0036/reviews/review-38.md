# Proof Review — ASN-0036 (cycle 1)

*2026-04-12 16:42*

29 properties

### S0

## Verification of S0 (Content immutability)

**1. Precondition completeness** — The property is universally quantified over all state transitions and all addresses in dom(Σ.C). No additional preconditions are needed. Sound.

**2. Case coverage** — S0 is stated as a foundational axiom ("the central invariant of the two-stream architecture"), not derived from sub-cases. The wp formulation correctly characterizes the obligation it places on every operation: either leave C(a) unchanged or operate only on fresh addresses. Each operation ASN bears its own proof obligation to satisfy S0. Sound.

**3. Postcondition establishment** — As an axiom, S0 imposes a constraint rather than deriving one. The narrative and wp formulation are consistent with the formal statement. Sound.

**4. All conjuncts addressed** — The two conjuncts (address persistence: `a ∈ dom(Σ'.C)`, and value immutability: `Σ'.C(a) = Σ.C(a)`) are both explicitly identified and explained in the narrative paragraph beginning "S0 is a strong property." Sound.

**5. Dependency correctness** — No dependencies declared, none used. As a foundational axiom this is correct. Sound.

**6. Formal contract** — No `*Formal Contract:*` section is present.

**7. Missing guarantees** — None. S0 is axiomatic and self-contained.

```
RESULT: FOUND

**Problem**: The property section has no `*Formal Contract:*` block. S0 is
a foundational design axiom — the invariant that every operation must
preserve — and should be declared as such. The missing contract should be:

    *Formal Contract:*
    - *Invariant:* a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a) for every transition Σ → Σ'

**Required**: Append the formal contract block to the end of the S0
property section.
```

### S7b

Looking at S7b as stated:

**S7b** is declared as a "design requirement" — an axiom, not a derived result. It asserts that content addresses live at the element level. The narrative correctly invokes T4's field correspondence to explain *why* `zeros(a) = 3` implies all four fields are present. T4c confirms the bijection `zeros(t) = 3 ↔ element level`. Dependency usage is correct.

However, the property section has no `*Formal Contract:*` block.

```
RESULT: FOUND

**Problem**: Missing formal contract. S7b is a design requirement (axiom) with no
`*Formal Contract:*` section. The property narrative ends after the T4 explanation
without formalizing the contract.

**Required**: Append a formal contract. Since S7b is explicitly called a "design
requirement" (not derived from other properties), it should be:

*Formal Contract:*
- *Axiom:* (A a ∈ dom(Σ.C) :: zeros(a) = 3)
- *Preconditions:* T4 (HierarchicalParsing) — provides the definition of `zeros`
  and the level correspondence (`zeros(t) = 3` ↔ element address with all four
  fields present).
```

### S7a

**Analyzing S7a's property section against the verification checklist.**

S7a is described as "a design requirement, not a convention" — i.e., an axiom. It has no proof body (no reasoning ending in ∎) and no formal contract.

```
RESULT: FOUND

**Problem 1 — Missing formal contract (checklist §6).**
S7a has no `*Formal Contract:*` section. Since S7a is a design requirement (axiom), it needs at minimum an `*Axiom:*` field formalizing the assertion. Something like:
  - *Axiom:* For every `a ∈ dom(Σ.C)`, the document-level prefix `origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)` is the tumbler of the document whose owner allocated `a`.
  - *Preconditions:* `a ∈ dom(Σ.C)`, `zeros(a) = 3` (element-level, per S7b).

**Problem 2 — Truncated property text.**
The property section ends with: "we require:" followed by nothing. The sentence introducing a domain restriction on S7 is incomplete — the actual restriction (presumably `zeros(a) = 3` or `zeros(a) ≥ 2`) is never stated.

**Problem 3 — Dependency direction is inverted (checklist §5).**
S7 is listed as a dependency of S7a, but the actual relationship is the reverse: S7's proof *uses* S7a ("By S7a (document-scoped allocation)…"). S7a, being an axiom with no proof, does not and cannot reference S7. S7 should be removed from S7a's dependency list. T4 is appropriately listed (S7a's narrative references `fields(a).document` and `zeros(a) ≥ 2`).

**Required:**
1. Add a `*Formal Contract:*` block to S7a with at least `*Axiom:*` and `*Preconditions:*` fields.
2. Complete the truncated sentence "we require:" with the intended domain restriction.
3. Remove S7 from S7a's declared dependencies (it is a dependent, not a dependency).
```

### S7c

Looking at S7c against the verification checklist:

**1–5: Narrative reasoning is sound.** The motivation is correct: at δ = 1, the subspace identifier IS the entire element field, so TA7a's ordinal-only formulation requires an ordinal in **S** with #o ≥ 1, but stripping the subspace identifier leaves the empty sequence (not in **S**). The T10a reference is accurate — `inc(document_address, 2)` produces an element address with δ = 1, showing the constraint is non-vacuous. S7b is a genuine logical precondition (ensures the element field exists via zeros(a) = 3).

**6: Formal contract — missing entirely.** The property section ends with the parenthetical about architectural completeness. There is no `*Formal Contract:*` block. S7c is explicitly a design requirement (axiom), and it also has a precondition (S7b, for well-definedness of `fields(a).element`).

```
RESULT: FOUND

**Problem**: No formal contract section. The property section ends at "...is load-bearing for S8-depth's ordinal shift analysis below, not for S7 itself.)" with no `*Formal Contract:*` block. S7c is a design requirement (axiom) with a well-definedness precondition on S7b.

**Required**: Append a formal contract, e.g.:

*Formal Contract:*
- *Preconditions:* S7b — every `a ∈ dom(Σ.C)` satisfies `zeros(a) = 3`, so `fields(a).element` is well-defined (T4b).
- *Axiom:* `(A a ∈ dom(Σ.C) :: #fields(a).element ≥ 2)`
```

### S8-depth

## Verification of S8-depth

### Analysis

**1. Precondition completeness** — The axiom quantifies over `d`, `v₁`, `v₂` with `v₁, v₂ ∈ dom(Σ.M(d))` and `(v₁)₁ = (v₂)₁` (same subspace). Complete for a design requirement.

**2. Case coverage** — N/A. S8-depth is an axiom ("design requirement, not a convention"), not a derived property.

**3. Postcondition establishment** — The axiom is asserted by fiat, parallel to S7a. The narrative provides motivation (Gregory's evidence, two-blade knife computation) but correctly does not attempt a derivation.

**4. All conjuncts addressed** — Single conjunct `#v₁ = #v₂`. Addressed. The section also introduces definitions (consecutive V-positions, ordinal displacement extension to k=0, correspondence runs) and derives their properties from OrdinalShift and S7c. These derived claims are sound:
   - Prefix preservation follows from OrdinalShift postcondition `shift(v, n)ᵢ = vᵢ for i < m`.
   - Depth preservation follows from `#shift(v, n) = #v`.
   - I-address subspace preservation follows from S7c (`δ ≥ 2` ensures the subspace identifier is outside the action point).
   - The k=0 extension is explicitly flagged as notational, not a use of OrdinalShift with `n = 0`.

**5. Dependency correctness** — S7c is used for the I-address subspace preservation argument. OrdinalShift is used for depth and prefix preservation in ordinal displacement. Both are used correctly. T10a, TA5(c) are mentioned only as motivation in a parenthetical that explicitly disclaims dependency ("not a dependency of the decomposition proof"). S7a, S7b, TA7a are referenced contextually but not load-bearing for S8-depth itself.

**6. Formal contract** — **Missing.** The property section has no `*Formal Contract:*` block. S8-depth is a design requirement (axiom). The expected contract:

```
*Formal Contract:*
- *Axiom:* (A d, v₁, v₂ : v₁ ∈ dom(Σ.M(d)) ∧ v₂ ∈ dom(Σ.M(d)) ∧ (v₁)₁ = (v₂)₁ : #v₁ = #v₂)
```

**7. Missing guarantees** — No missing guarantees for the axiom itself. The derived correspondence-run properties rely on OrdinalShift and S7c, both provided and correctly applied.

---

```
RESULT: FOUND

**Problem**: No formal contract. S8-depth is explicitly a design requirement (axiom) but the property section lacks a `*Formal Contract:*` block.
**Required**: Append a formal contract:
  *Formal Contract:*
  - *Axiom:* (A d, v₁, v₂ : v₁ ∈ dom(Σ.M(d)) ∧ v₂ ∈ dom(Σ.M(d)) ∧ (v₁)₁ = (v₂)₁ : #v₁ = #v₂)
```

### S8-fin

RESULT: FOUND

**Problem 1 — Missing formal contract.** The property section has no `*Formal Contract:*` block. As a state invariant (holds for every reachable state), it should read:

```
*Formal Contract:*
- *Invariant:* dom(Σ.M(d)) is finite for every document d and every reachable state Σ
```

**Problem 2 — Proof is an informal appeal, not a structured argument.** The entire proof is: "follows from the operational reality… the system has performed only finitely many operations. No operation introduces infinitely many V-positions." This is a proof sketch, not a proof. The claim is an invariant over reachable states, so it requires induction over the operation trace:

- **Base case**: In the initial state, `dom(M(d))` is empty (or otherwise finite) for every document `d`. This is never stated.
- **Inductive step**: If `dom(M(d))` is finite before an operation, it remains finite after. The text asserts "No operation introduces infinitely many V-positions" but does not cite any property of INSERT, COPY, etc. that establishes this.

Neither step is made explicit.

**Problem 3 — Undeclared dependencies.** The proof relies on two guarantees that are not listed as dependencies and apparently not established by any existing property:

1. That the initial state gives each document a finite (empty) domain.
2. That each operation (INSERT, COPY, etc.) adds only finitely many V-positions to `dom(M(d))`.

These should either be proved as lemmas (per-operation finiteness preservation) or cited as axioms of the operational model.

**Required**:
1. Add a `*Formal Contract:*` section with the invariant.
2. Restructure the proof as an induction over the operation sequence, with explicit base case and inductive step.
3. Declare dependencies on whichever properties establish (a) finiteness of the initial state and (b) finite V-position introduction per operation — or create those properties if they do not yet exist.

### D-CTG

Looking at the proof carefully:

**Logic check:** The contradiction argument is sound. Given two positions v₁ < v₂ disagreeing at some component j ∈ {2, …, m−1}, the constructed w (copying v₁ through j, setting w_{j+1} = n, filling tail with 1) correctly satisfies v₁ < w < v₂ for all n > (v₁)_{j+1}. The ordering arguments are correct: w > v₁ by the j+1 component, w < v₂ by the j component. Infinitely many distinct n yield infinitely many distinct members of V_S(d) by T3, contradicting S8-fin.

**Preconditions, case coverage, postcondition establishment:** All sound. The proof by contradiction covers the only alternative to the desired conclusion. The formal postcondition matches what the proof establishes.

**Dependency correctness issue:** The proof explicitly cites **T1(i)** three times to justify ordering comparisons:

- "since v₁ < v₂ by T1(i)"
- "By T1(i), w > v₁"  
- "By T1(i), w < v₂"

T1(i) — the lexicographic ordering rule for tumblers — is not declared in the dependency list. The proof relies on the specific structure of lexicographic comparison (if two tumblers agree on a prefix and differ at the next component, the larger component determines the order), not merely on the existence of "<". This is a substantive dependency that the ordering arguments rest on.

```
RESULT: FOUND

**Problem**: T1(i) (lexicographic ordering on tumblers, ASN-0034) is referenced
three times in the proof but is not declared as a dependency. The proof's core
ordering arguments — establishing v₁ < w and w < v₂ — depend on T1(i)'s
guarantee that prefix agreement plus a strict inequality at the first
differing component determines the overall order.

**Required**: Add T1(i) to the dependency list for D-CTG.
```

### S3

RESULT: FOUND

**Problem**: S3 has no proof and no formal contract. The property section contains narrative analysis — a weakest-precondition discussion showing *what operations must do* to maintain S3, and a note that S1 prevents valid references from becoming dangling — but there is no `*Proof.*` block establishing that S3 actually holds as an invariant across all state transitions. The section also lacks a `*Formal Contract:*` block entirely.

The wp analysis identifies two cases (mapping added without content creation requires `a ∈ dom(Σ.C)`; atomic creation satisfies S3 in the post-state) and invokes S1 for persistence, but these observations are never assembled into a proof. Specifically:

1. **No base case**: There is no argument that S3 holds in an initial state (e.g., when `M(d)` is empty for all `d`, S3 holds vacuously).
2. **No inductive step**: The wp discussion identifies conditions operations must satisfy but does not prove that *every* operation in the system actually satisfies them. It states `wp(add-mapping, S3) ⟹ a ∈ dom(Σ.C)` as a requirement, but never shows this requirement is met by the system's operations.
3. **S1 usage is incomplete**: The text correctly notes S1 prevents existing references from becoming dangling, but does not address the case where an operation *removes* a V-mapping (which would preserve S3 trivially) — case coverage is implicit rather than explicit.
4. **Missing formal contract**: S3 should have a `*Formal Contract:*` with at minimum an `*Invariant:*` field stating `(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))` for every state `Σ`, and `*Preconditions:*` listing S1 (and potentially S0).

**Required**: Either (a) add a `*Proof.*` block that establishes S3 as an invariant by induction over state transitions — showing the base case, showing each operation class preserves S3, and citing S1 for the persistence argument — followed by a `*Formal Contract:*`; or (b) if S3 is intended as an axiom (a design constraint imposed on all operations rather than a derived property), designate it explicitly as such with a `*Formal Contract:*` using the `*Axiom:*` field and remove the proof-like wp reasoning that implies derivability.

### ValidInsertionPosition

Looking at the ValidInsertionPosition property against the checklist:

**1. Precondition completeness** — Adequate. The definition states "document d satisfying D-CTG" and references S8-depth, D-MIN inline. The m ≥ 2 lower bound is justified by induction (empty case requires m ≥ 2; S8-depth preserves depth thereafter).

**2. Case coverage** — Complete. Empty and non-empty are exhaustive. The m = 1 boundary is explicitly ruled out with a concrete counterexample (shift([S], 1) lands in subspace S + 1).

**3. Postcondition establishment** — Sound. The explicit form shift(min, j) = [S, 1, ..., 1 + j] follows from TumblerAdd with action point m ≥ 2. The four structural claims (distinctness, depth preservation, subspace identity, S8a consistency) are each established.

**4. All conjuncts addressed** — All four structural claims are proved. The N + 1 count is verified. The empty-case depth commitment is explained.

**5. Dependency correctness** — The proof explicitly invokes "OrdinalShift and TumblerAdd" and "the result-length identity of OrdinalShift (ASN-0034)" by name. These are distinct properties from ASN-0034 but are not listed as dependencies — only T3 from ASN-0034 is declared. The needed facts (action-point copying, result-length preservation) are partly recapitulated in S8-depth's text, but the proof attributes them directly to OrdinalShift/TumblerAdd. Minor declaration gap; the reasoning is sound given those properties.

**6. Formal contract** — **Missing entirely.** The property section ends after the examples with no `*Formal Contract:*` block.

**7. Missing guarantees** — No missing guarantees beyond the OrdinalShift/TumblerAdd dependency noted above.

```
RESULT: FOUND

**Problem**: The property has no `*Formal Contract:*` section. ValidInsertionPosition is a definition with verifiable postconditions (depth preservation, subspace identity, distinctness, S8a compliance) and implicit preconditions (d satisfies D-CTG/D-MIN/S8-depth/S8a; S ≥ 1), but none of these are collected into a formal contract. The checklist requires every property to end with a formal contract whose fields match the narrative.

**Required**: Add a formal contract after the examples section. Suggested structure:

  *Formal Contract:*
  - *Definition:* A V-position v is a valid insertion position in subspace S of document d when: (a) V_S(d) ≠ ∅ with |V_S(d)| = N and v = shift(min(V_S(d)), j) for 0 ≤ j ≤ N (where shift(·, 0) is identity); or (b) V_S(d) = ∅ and v = [S, 1, ..., 1] of depth m ≥ 2.
  - *Preconditions:* d satisfies D-CTG, D-MIN, S8-depth, S8a; S ≥ 1; in the non-empty case, m ≥ 2 (inherited from the empty-case establishment and S8-depth).
  - *Postconditions:* (i) #v = m (depth preservation); (ii) v₁ = S (subspace identity); (iii) zeros(v) = 0 ∧ v > 0 (S8a compliance); (iv) the N + 1 valid positions in the non-empty case are pairwise distinct.

Additionally, OrdinalShift and TumblerAdd (ASN-0034) should be declared as explicit dependencies alongside T3, since the proof invokes their properties by name.
```

### OrdAddHom

## Verification

The main proof (establishing postcondition (a)) is sound. The three-region decomposition via TumblerAdd is correctly applied on both sides, the index-shifting argument for `actionPoint(w_ord) = k - 1` is correct, and the component-by-component match holds, including the boundary cases `k = 2` (empty copy-from-start region) and `k = m` (empty tail region). Postcondition (b) follows directly from TumblerAdd's copy-from-start rule since `k ≥ 2`. Both instances check out.

However, postcondition (c) in the formal contract has an undeclared dependency.

```
RESULT: FOUND

**Problem**: Postcondition (c) explicitly invokes "the generalized inverse (vpos contract (b))" — the property `vpos(subspace(r), ord(r)) = r` for `#r ≥ 2` — but this property is not listed in the Dependencies section. The proof text in (c) says: "so the generalized inverse (vpos contract (b)) applies to r: vpos(subspace(r), ord(r)) = r". This is a named property from another ASN used as ground truth without declaration.

**Required**: Add the vpos inverse property (vpos contract (b): `vpos(subspace(t), ord(t)) = t` for `#t ≥ 2`) to the dependency list for OrdAddHom. The core result (a) and subspace preservation (b) are unaffected — only postcondition (c) requires this additional dependency.
```

### S2

```
RESULT: FOUND

**Problem**: The property section has no `*Formal Contract:*` section. S2 is an axiom — it asserts by design that `Σ.M(d)` is a function, justified as "inherent in the concept of a virtual byte stream." It requires a formal contract capturing this.

**Required**: Append a formal contract to the property section:

```
*Formal Contract:*
- *Axiom:* For every document d, Σ.M(d) is a function: each v ∈ dom(Σ.M(d)) maps to exactly one I-address
```

15 verified, 11 found.
