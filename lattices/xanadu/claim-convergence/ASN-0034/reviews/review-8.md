# Proof Review — ASN-0034 (cycle 1)

*2026-04-08 17:28*

59 properties

### T4

## Verification of T4 (HierarchicalParsing)

### 1. Precondition completeness
T4 is declared as an axiom constraining valid address tumblers. The three constraints (at most three zeros, positive-component, non-empty field) are clearly stated. ✓

### 2. Case coverage
The four zero-count cases (0–3) are exhaustive given the axiom `zeros(t) ≤ 3`. The T4a equivalence sketch covers both directions (non-empty fields → syntactic conditions, and vice versa under the positive-component constraint). ✓

### 3. Postcondition establishment
T4a, T4b, T4c are stated as consequences with informal reasoning. T4a's equivalence follows from the positive-component constraint ensuring zeros are exclusively separators. T4b's unique parse follows from splitting on separators. T4c's bijection is immediate from the definitions. ✓

### 4. All conjuncts addressed
All three axiom constraints and all three postconditions (T4a, T4b, T4c) are addressed. ✓

### 5. Dependency correctness

The narrative explicitly states:

> "The argument uses only **T3 (canonical representation)** and the T4 constraints themselves; no other properties are required."

Yet the dependencies section reads "(none)." T3 is invoked by name as a required ingredient — likely for T4b (UniqueParse), where canonical representation ensures the component sequence is the unique basis from which `fields(t)` parses — but is not declared.

### 6. Formal contract
The formal contract correctly combines `Axiom` + `Postconditions`, matching the narrative structure. The axiom lists all three constraints; the postconditions list T4a, T4b, T4c with accurate descriptions. ✓

### 7. Missing guarantees
Beyond the undeclared T3 dependency, no additional guarantees are assumed without basis. ✓

---

```
RESULT: FOUND

**Problem**: The proof explicitly states "The argument uses only T3 (canonical representation) and the T4 constraints themselves; no other properties are required," but T3 is not declared in the dependencies list (which reads "(none)"). T3 appears necessary for T4b (UniqueParse) — canonical representation ensures the component sequence from which `fields(t)` parses is itself unique, which is a prerequisite for the parse being unique.

**Required**: Add T3 (CanonicalRepresentation) to the dependency list.
```

### T10

## Verification of T10 (PartitionIndependence)

**Checklist walkthrough:**

1. **Precondition completeness** — All inputs stated. Non-emptiness of prefixes is implied by the non-nesting condition (an empty sequence is a prefix of everything, contradicting p₁ ⋠ p₂). Sound.

2. **Case coverage** — Splits on m ≤ n vs m > n, which is exhaustive. Case 1 uses p₁ ⋠ p₂ (since the length condition m ≤ n is met, the component condition must fail). Case 2 symmetrically uses p₂ ⋠ p₁. The m = n subcase is correctly absorbed into Case 1. Sound.

3. **Postcondition establishment** — The proof constructs divergence position k with aₖ = p₁ₖ ≠ p₂ₖ = bₖ, and k ≤ #a (from k ≤ m ≤ #a) and k ≤ #b (from k ≤ n ≤ #b), so both components are well-defined. The appeal to T3's contrapositive (∃i with aᵢ ≠ bᵢ ⟹ a ≠ b) is correct. Sound.

4. **All conjuncts addressed** — Single postcondition a ≠ b. Established. Sound.

5. **Dependency correctness** — T3 is declared and correctly used (contrapositive of forward direction: component disagreement implies inequality). **However**, the proof invokes "the definition of prefix" in four critical steps—to derive divergence in Case 1, in Case 2, and twice to transfer the divergence from prefixes to tumblers a and b—but no property or definition formalizing the prefix relation ≼ is listed among the declared dependencies. Only T3 is declared.

6. **Formal contract** — Preconditions and postconditions match the property statement exactly. Format is correct.

7. **Missing guarantees** — Covered by item 5. The formal definition of ≼ (i.e., p ≼ q iff #p ≤ #q ∧ ∀i ∈ [1,#p]: qᵢ = pᵢ) is load-bearing for the proof but absent from the dependency list.

---

```
RESULT: FOUND

**Problem**: The proof uses the formal definition of the prefix relation ≼ in four
places—deriving prefix divergence in both Case 1 ("the definition of prefix requires
p₂ᵢ = p₁ᵢ for all 1 ≤ i ≤ m") and Case 2, and transferring divergence to tumblers
("the definition of prefix gives aᵢ = p₁ᵢ for all 1 ≤ i ≤ m" and similarly for b)—
but the property or definition that formally establishes ≼ is not declared as a
dependency. Only T3 is listed.

**Required**: Add the formal definition of the prefix relation ≼ (e.g., T5 or
whichever property defines "p ≼ q iff #p ≤ #q ∧ ∀i ∈ [1,#p]: qᵢ = pᵢ") as a
declared dependency of T10.
```

### TA5-SIG

**Reviewing TA5-SIG (LastSignificantPosition)...**

**Case coverage**: Two cases — at least one nonzero component vs. all-zero — are exhaustive and mutually exclusive. ✓

**Range claim**: In case 1, the set `{i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0}` is nonempty by hypothesis, so `max` is well-defined and yields a value in `[1, #t]`. In case 2, `sig(t) = #t ≥ 1`, so `1 ≤ sig(t) ≤ #t`. ✓

**Dependency correctness**: No dependencies declared, none used. The assertion `#t ≥ 1` for every `t ∈ T` is stated as inherent to the type, which is reasonable for a foundational definition. ✓

**Formal contract**: The contract uses fields **Domain** and **Range**, which are not in the canonical field set (Preconditions, Postconditions, Invariant, Frame, Axiom, Definition). For a definition property, the correct fields are:

```
*Formal Contract:*
- *Preconditions:* `t ∈ T` (any tumbler with `#t ≥ 1`).
- *Definition:* `sig(t) = max({i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0})` when `(E i …)`; `sig(t) = #t` when `(A i …)`.
- *Postconditions:* `1 ≤ sig(t) ≤ #t`.
```

```
RESULT: FOUND

**Problem**: Formal contract uses non-standard field names "Domain" and "Range" instead of the canonical fields. "Domain: `t ∈ T` (any tumbler with `#t ≥ 1`)" should be "Preconditions"; "Range: `1 ≤ sig(t) ≤ #t`" should be "Postconditions"; "Definition" is correctly named.
**Required**: Rename "Domain" → "Preconditions" and "Range" → "Postconditions" to match the canonical field set.
```

### T8

## Verification of T8 (AllocationPermanence)

**Reasoning structure:** The proof is a case analysis over all system operations, showing each preserves `allocated(s) ⊆ allocated(s')`, followed by induction over transition sequences. The three cases (read-only, pure arithmetic, allocation) are argued correctly:

- Case 1: `allocated(s') = allocated(s)` → inclusion trivial ✓
- Case 2: `allocated(s') = allocated(s)` → inclusion trivial ✓  
- Case 3: `allocated(s') = allocated(s) ∪ {a_new}` → inclusion holds ✓
- Induction step is standard and sound ✓

**Checklist 1 (Preconditions):** Acceptable — this is a global invariant, no input preconditions needed.

**Checklist 2 (Case coverage):** Exhaustiveness is asserted and backed by the axiom in the formal contract. Acceptable for a design-level property.

**Checklist 3 (Postcondition):** The monotone inclusion is established for each case and extended by induction. ✓

**Checklist 4 (Conjuncts):** The three restatements (persists forever / no removal / monotonically non-decreasing) are all equivalent and all addressed. ✓

**Checklist 5 (Dependencies):** The proof explicitly references T1, T2, T4 (to classify as read-only), ⊕, ⊖, inc (to classify as pure arithmetic), T10a (to characterize the allocation mechanism), and TA5 (to describe the frontier-advance rule). It relies on the *content* of these — particularly T10a's claim that allocation only inserts into the allocated set, and the characterization of ⊕/⊖/inc as pure functions with no allocation side effects. Yet the dependencies section declares **(none)**.

**Checklist 6 (Formal contract):** Invariant + Axiom + Frame fields are present and match the narrative. ✓

**Checklist 7 (Missing guarantees):** No missing guarantees beyond the undeclared dependencies.

```
RESULT: FOUND

**Problem**: The proof references T1, T2, T4, T10a, TA5, ⊕, ⊖, and inc by label and relies on their characterizations (read-only, pure, insert-only) to construct the case analysis, but the dependencies section declares "(none)". Specifically, Case 3 depends on T10a's description that allocation "inserts [a_new] into the allocated set" (and does nothing else), and Cases 1–2 depend on the definitions of the named operations being side-effect-free with respect to allocation state. Without these as declared dependencies, the exhaustiveness and per-case arguments are ungrounded.

**Required**: Declare dependencies on T1, T2, T4 (read-only characterization), T10a (allocation mechanism is insert-only), TA5 (frontier advance via inc), and the definitions of ⊕, ⊖, inc (pure functions on T with no allocation side effects). These are needed to verify both the exhaustiveness claim and the per-case reasoning.
```

### T10a

## Verification of T10a (AllocatorDiscipline)

**Checklist 1–4**: The axiom statement is clear, the four consequences (T10a.1–T10a.3, T10a-N) are each addressed, and the formal contract covers all conjuncts.

**Checklist 5 (Dependency correctness)**: Two undeclared dependencies.

**Checklist 6 (Formal contract)**: The Axiom + Postconditions structure is appropriate.

**Checklist 7 (Missing guarantees)**: See below.

---

```
RESULT: FOUND

**Problem**: T10 is referenced but not declared as a dependency. Postconditions
T10a.2 and T10a-N both cite "the precondition of T10" / "the T10 precondition"
— without T10 in scope, the claims that T10a.2 *satisfies* it and that relaxing
the axiom *violates* it cannot be verified.

Additionally, postconditions T10a.1 and T10a.3 assume length properties of
`inc` that the axiom text does not establish:
  - T10a.1 requires #inc(a, 0) = #a  (length preservation for shallow increment)
  - T10a.3 requires #inc(a, k') ≥ #a + k' for k' > 0  (length extension for deep increment)
These properties must come from the definition of `inc` (or a property that
characterises it), but no such definition or property is listed as a dependency.

**Required**:
1. Add T10 as a dependency so its precondition is available for verifying T10a.2
   and T10a-N.
2. Add the `inc` definition or the property that establishes its length behaviour
   (#inc(a, 0) = #a and #inc(a, k) ≥ #a + k for k > 0) as a dependency, so
   postconditions T10a.1 and T10a.3 can be traced to ground truth.
```

### OrdinalShift

## Verification of OrdinalShift

**Checklist walkthrough:**

1. **Precondition completeness** — v ∈ T with #v = m, n ≥ 1. These suffice: δ(n, m) = [0,…,0, n] is in T (all components ∈ ℕ, length m ≥ 1), δ(n, m) > 0 (last component n ≥ 1), and actionPoint(δ(n, m)) = m = #v so the TA0 guard k ≤ #a holds. Complete.

2. **Case coverage** — The proof covers the general case (prefix preserved for i < m, action at i = m), then splits m ≥ 2 vs m = 1 for the first-component claim. Both boundary cases are handled.

3. **Postcondition establishment** — Each claim is established by direct appeal to the TumblerAdd constructive definition: prefix copy (i < k = m gives rᵢ = vᵢ), action point (rₘ = vₘ + n), no tail (k = m = n so there are no i > k positions), result-length identity (#r = #w = m = #v). The positivity claim vₘ + n ≥ 1 for n ≥ 1 is immediate. Sound.

4. **All conjuncts addressed** — Definition, TA0 satisfaction, prefix preservation, deepest-component advance, m ≥ 2 and m = 1 sub-cases, depth preservation, positivity — all addressed.

5. **Dependency correctness** — TA0 is invoked for well-definedness, TumblerAdd for the constructive rule and result-length identity. Both declared, both used. δ(n, m) is described inline (action point m, length m); no undeclared external dependency is needed.

6. **Formal contract** — The property section ends at "…vₘ + n ≥ 1 unconditionally for all vₘ ≥ 0." **No `*Formal Contract:*` block is present.**

7. **Missing guarantees** — None. All reasoning follows from the provided dependencies.

---

```
RESULT: FOUND

**Problem**: Missing formal contract. The property section has no `*Formal Contract:*`
block. Given that OrdinalShift is a definition with derived postconditions, it needs
one. The narrative establishes preconditions (v ∈ T, n ≥ 1), a definition
(shift(v, n) = v ⊕ δ(n, m)), and postconditions (membership, length preservation,
prefix preservation, positivity).

**Required**: Append a formal contract, e.g.:

  *Formal Contract:*
  - *Preconditions:* v ∈ T, n ≥ 1
  - *Definition:* shift(v, n) = v ⊕ δ(n, m) where m = #v
  - *Postconditions:* shift(v, n) ∈ T, #shift(v, n) = #v,
    shift(v, n)ᵢ = vᵢ for i < m, shift(v, n)ₘ = vₘ + n ≥ 1
```

### PositiveTumbler

## Verification

**PositiveTumbler** is a definition, not a derived theorem. The definition is clear and well-formed. The supporting claim — "every positive tumbler is greater than every zero tumbler under T1" — is argued informally but correctly:

- For positions `i < k` (where `k` is the first nonzero component of `t`), both `tᵢ = 0` and `zᵢ = 0`, so no divergence occurs before `k`.
- At position `k`, either (a) the zero tumbler still has a component there, giving `zₖ = 0 < tₖ` and `z < t` via T1 case (i), or (b) the zero tumbler has fewer than `k` components, making it a proper prefix, and `z < t` via T1 case (ii).

The case analysis is exhaustive, the dependency on T1 is correctly applied, and the observation that `w > 0` in TA0/TA4 excludes all-zero tumblers regardless of length is accurate.

However, the section has no `*Formal Contract:*` block.

```
RESULT: FOUND

**Problem**: Missing formal contract. The section defines PositiveTumbler and
zero tumbler but does not end with a `*Formal Contract:*` section. Per the
checklist, every property section must include one.

**Required**: Append a formal contract, e.g.:

*Formal Contract:*
- *Definition:* `t > 0` (positive) iff `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)`.
  Zero tumbler: `(A i : 1 ≤ i ≤ #t : tᵢ = 0)`.
```

### T10a.3

Looking at the proof of T10a.3 against its dependencies and formal contract.

**Narrative proof check:**

- Child base length = γ + k' via TA5(d) + T10a.1: correct.
- All child outputs have uniform length γ + k' by T10a.1 applied to the child allocator: correct.
- k' ≥ 1 → child length > parent length → non-collision by T3: correct.
- Single-step separation is sound.

**Multi-level claim check:**

The proof says: "Each child-spawning step adds at least one component, so a descendant d levels deep produces outputs of length at least γ + d. Outputs at different depths never collide by length alone."

Within a single lineage, the exact length at depth d is γ + k'₁ + k'₂ + … + k'_d (each step applies TA5(d) adding exactly k'_i components, then T10a.1 fixes all sibling outputs at that length). Since each k'_i ≥ 1, the sequence of exact lengths is strictly increasing with depth, so T3 applies. The reasoning is sound for a single lineage chain.

**Formal contract discrepancy:**

The parent property T10a states T10a.3 establishes:

> `#output ≥ m + k'₁ + k'₂ + … + k'_d`

But T10a.3's own formal contract states only:

> `Descendant at depth d has output length ≥ γ + d`

This is a strictly weaker bound. The proof narrative *does* establish the tighter bound (first paragraph gives length exactly γ + k', not γ + 1), but the formal contract collapses the specific k' values to their minimum (1 per level).

This matters for the non-collision claim in the same formal contract: "outputs at different nesting depths never collide (distinct lengths imply distinct tumblers by T3)." The lower bound ≥ γ + d does **not** establish distinct lengths across depths — only the exact bound (γ + Σk'_i strictly increasing along a chain) does. With just the ≥ bound, a depth-1 output of length γ + 5 and a depth-4 output of length γ + 5 are not excluded.

```
RESULT: FOUND

**Problem**: The formal contract's multi-level postcondition states "Descendant at depth d
has output length ≥ γ + d" but the parent property T10a specifies T10a.3 establishes the
tighter bound "#output ≥ m + k'₁ + k'₂ + … + k'_d". The proof narrative establishes the
tighter bound (each step gives length exactly γ + k' via TA5(d), not merely γ + 1), but the
formal contract loses the per-step k' values. Consequently, the non-collision claim in the
contract — "outputs at different nesting depths never collide (distinct lengths imply distinct
tumblers by T3)" — does not follow from the stated ≥ γ + d bound alone, since that bound
permits equal lengths at different depths.

**Required**: The formal contract's multi-level postcondition should state the tight bound
matching T10a: "Descendant at depth d along a single lineage with child-spawning parameters
k'₁, …, k'_d has output length exactly γ + k'₁ + … + k'_d ≥ γ + d." The non-collision
justification should reference the strict monotonicity of exact lengths along a lineage
(each k'_i ≥ 1 adds strictly to the cumulative sum), not merely the lower bound.
```

### TA-RC

I'll verify the proof of TA-RC step by step against the checklist.

**Witnesses:** a = [1, 3, 5], b = [1, 3, 7], w = [0, 2, 4].

**a ≠ b:** a₃ = 5 ≠ 7 = b₃, same length, so a ≠ b by T3. ✓

**w > 0:** w₂ = 2 > 0, so w has a nonzero component. ✓

**Action point:** k = min({i : wᵢ ≠ 0}) = 2 (w₁ = 0, w₂ = 2). ✓

**Well-definedness:** k = 2 ≤ 3 = #a, and k = 2 ≤ 3 = #b. Both satisfy TA0. ✓

**a ⊕ w computation (k = 2):**
- r₁ = a₁ = 1 (i < k) ✓
- r₂ = a₂ + w₂ = 3 + 2 = 5 (i = k) ✓
- r₃ = w₃ = 4 (i > k) ✓
- Result: [1, 5, 4] ✓

**b ⊕ w computation (k = 2):**
- r₁ = b₁ = 1 (i < k) ✓
- r₂ = b₂ + w₂ = 3 + 2 = 5 (i = k) ✓
- r₃ = w₃ = 4 (i > k) ✓
- Result: [1, 5, 4] ✓

**Equality:** [1, 5, 4] = [1, 5, 4], so a ⊕ w = b ⊕ w. ✓

**Checklist items 1–5:** All pass. Preconditions complete, single witness suffices for existential, postcondition established by direct computation, all conjuncts (w > 0, both action-point bounds, a ≠ b, a ⊕ w = b ⊕ w) addressed, dependencies T3/TA0/TumblerAdd all used correctly and none undeclared.

**Checklist item 6 — Formal contract:**

The formal contract labels the property as:
> *Axiom:* ∃ a, b, w ∈ T : w > 0 ∧ actionPoint(w) ≤ #a ∧ actionPoint(w) ≤ #b ∧ a ≠ b ∧ a ⊕ w = b ⊕ w

Per the checklist, "Axiom" means "fundamental assertion by definition or design, **not derived**." But TA-RC is explicitly derived — the proof constructs witnesses and verifies the claim by computation from TumblerAdd's definition and T3. It is a theorem, not an axiom.

```
RESULT: FOUND

**Problem**: Formal contract uses `*Axiom:*` for a property that is derived by constructive witness proof from TumblerAdd and T3. The checklist defines Axiom as "fundamental assertion by definition or design, not derived," but TA-RC is proved, not assumed.

**Required**: Replace `*Axiom:*` with `*Postconditions:*` (no preconditions needed — the claim is unconditional):
```
*Formal Contract:*
- *Postconditions:* ∃ a, b, w ∈ T : w > 0 ∧ actionPoint(w) ≤ #a ∧ actionPoint(w) ≤ #b ∧ a ≠ b ∧ a ⊕ w = b ⊕ w
```
```

48 verified, 9 found.
