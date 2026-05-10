# Proof Review — ASN-0034 (cycle 1)

*2026-04-08 08:27*

58 properties

### T3

## Verification of T3 (CanonicalRepresentation)

**Logical soundness**: The biconditional proof is correct. Both directions follow from the extensional definition of sequence equality and Leibniz's law. The design commitment discussion (no trailing-zero quotient, no normalization) is accurate and well-motivated.

Two issues:

**Issue 1 — Undeclared dependency on T0.** The proof explicitly states: "By T0, T is the set of all finite sequences over ℕ." T0 is used as the ground from which the entire proof proceeds, yet the dependencies section declares "(none)".

**Issue 2 — Formal contract uses wrong field.** The proof itself says "T3 is not derived from other properties; it holds by the definition of the carrier set." This is definitional — an axiom — yet the formal contract labels it `*Postcondition:*`. There is no operation, no before/after state; the property asserts a biconditional that holds by the structure of T. The correct field is `*Axiom:*`.

```
RESULT: FOUND

**Problem**: (1) The proof explicitly cites T0 ("By T0, T is the set of all finite
sequences over ℕ") but the dependency list declares "(none)". T0 is the definitional
foundation for the entire argument. (2) The formal contract uses "*Postcondition:*"
but the proof narrative states "T3 is not derived from other properties; it holds by
the definition of the carrier set" — this is an axiom, not a postcondition.

**Required**: (1) Declare T0 as a dependency. (2) Change the formal contract from
"*Postcondition:*" to "*Axiom:*":

  *Formal Contract:*
  - *Axiom:* a = b ⟺ #a = #b ∧ (∀ i : 1 ≤ i ≤ #a : aᵢ = bᵢ). No quotient,
    normalization, or external identification is imposed on T.
```

### TumblerSub

RESULT: FOUND

**Problem**: The property section has no `*Formal Contract:*` section. TumblerSub is a definition with a stated precondition, so it needs a formal contract capturing both.

**Required**: Append a formal contract to the property section:

```
*Formal Contract:*
- *Preconditions:* a ≥ w (when a ≠ w, at the first divergence point k after zero-padding, aₖ ≥ wₖ)
- *Definition:* a ⊖ w computed by case analysis on divergence point k; rᵢ = 0 for i < k, rₖ = aₖ − wₖ, rᵢ = aᵢ for i > k; when no divergence exists, a ⊖ w = [0, …, 0]; #(a ⊖ w) = max(#a, #w)
```

### TumblerAdd

I need to verify the TumblerAdd property against the checklist.

**1. Precondition completeness**: Stated: `a ∈ T`, `w ∈ T`, `w > 0`, `k ≤ m` (action point within start position's length). These are sufficient for the definition to be well-formed.

**2. Case coverage**: The three-way case split (`i < k`, `i = k`, `i > k`) is exhaustive over all positions. The examples are correct — I verified all five by hand.

**3. Postcondition establishment**: The result-length identity `#(a ⊕ w) = #w` is derived correctly: `p = (k-1) + (n - k + 1) = n = #w`. The three stated properties (no carry, tail replacement, many-to-one) follow directly from the definition.

**4. All conjuncts addressed**: All stated properties are established.

**5. Dependency correctness**: TA4 (PartialInverse) is declared as a dependency but is **never referenced** anywhere in the TumblerAdd section. TumblerAdd is a self-contained definition. The dependency relationship is inverted — TA4's proof references TumblerAdd, not the other way around.

**6. Formal contract**: The section has **no `*Formal Contract:*` block**. TumblerAdd is a definition with preconditions and postconditions (the result-length identity). It requires a formal contract.

**7. Missing guarantees**: No issues beyond the missing formal contract.

```
RESULT: FOUND

**Problem**: (a) The TumblerAdd section has no `*Formal Contract:*` block. It is a definition with explicit preconditions (`w > 0`, `actionPoint(w) ≤ #a`) and a derived postcondition (the result-length identity `#(a ⊕ w) = #w`). (b) TA4 is declared as a dependency but is never referenced in TumblerAdd; the actual dependency runs the other direction (TA4 uses TumblerAdd).

**Required**: (a) Add a formal contract:
   ```
   *Formal Contract:*
   - *Preconditions:* a ∈ T, w ∈ T, w > 0, actionPoint(w) ≤ #a
   - *Definition:* rᵢ = aᵢ if i < k; rₖ = aₖ + wₖ; rᵢ = wᵢ if i > k
   - *Postconditions:* a ⊕ w ∈ T, #(a ⊕ w) = #w
   ```
   (b) Remove TA4 from the dependency list for TumblerAdd (it should instead list TumblerAdd as one of *its* dependencies).
```

### Divergence

Looking at the Divergence property section against the checklist:

**1. Precondition completeness** — Complete. Requires `a, b ∈ T` with `a ≠ b`. The uniqueness of `k` in case (i) follows from the agreement condition (if `k' < k` also satisfied the condition, then `aₖ' ≠ bₖ'` contradicts the agreement-before-`k` condition of `k`).

**2. Case coverage** — Sound. Cases (i) and (ii) are mutually exclusive (case (i) provides a counterexample to case (ii)'s universal quantifier) and exhaustive for `a ≠ b` (either some shared position disagrees, giving (i) via the least such, or all shared positions agree, forcing `#a ≠ #b` by T3, giving (ii)).

**3. Postcondition establishment** — The well-definedness claim ("exactly one case applies") is justified by the case structure already established in T1's trichotomy proof (Cases 2 and 3). Adequate for a definition.

**4. All conjuncts addressed** — Both cases defined, well-definedness justified, prefix-pair implications correctly derived.

**5. Dependency correctness** — T1 is used (case structure, trichotomy). TA0 and TA1-strict are referenced for motivational context (explaining significance of the definition), not as logical dependencies of the definition itself. This is acceptable.

**6. Formal contract** — Missing.

**7. Missing guarantees** — None.

```
RESULT: FOUND

**Problem**: The property section has no `*Formal Contract:*` block. As a definition, it should include a `*Definition:*` field summarizing the construction rule.

**Required**: Append a formal contract, e.g.:

*Formal Contract:*
- *Definition:* For `a, b ∈ T` with `a ≠ b`: (i) if `∃ k ≤ min(#a, #b)` with `aₖ ≠ bₖ` and `(A i : 1 ≤ i < k : aᵢ = bᵢ)`, then `divergence(a, b) = k`; (ii) if `(A i : 1 ≤ i ≤ min(#a, #b) : aᵢ = bᵢ)` and `#a ≠ #b`, then `divergence(a, b) = min(#a, #b) + 1`. Exactly one case applies.
```

### T4

RESULT: FOUND

**Problem**: The formal contract includes postconditions that T4's own section does not establish, and a dependency is referenced but not declared.

1. **Postconditions not established in T4's section.** The formal contract claims postconditions `(a) fields(t) is well-defined and unique` and `(b) zeros(t) determines the hierarchical level bijectively on {0, 1, 2, 3}`. However, the text explicitly defers these to sub-properties: "The unique-parse theorem appears as T4b (UniqueParse). The level-determination bijection appears as T4c (LevelDetermination)." T4's own section does not prove either postcondition — it only motivates why they should follow. Yet the text declares "T4 is an axiom," which should have no postconditions at all.

2. **Undeclared dependency on T3.** The narrative states: "The argument uses only T3 (canonical representation) and the T4 constraints themselves; no other properties are required." But the dependencies section lists "(none)". If T4's formal contract claims postconditions (a) and (b), and those require T3, then T3 must be declared as a dependency.

These two issues are entangled: the formal contract mixes an axiom declaration with theorem postconditions that are proved elsewhere using an undeclared dependency.

**Required**: Either:
- **(Option A)** Remove the postconditions from T4's formal contract, leaving it as a pure axiom (matching the text's declaration "T4 is an axiom"). The postconditions belong in T4b's and T4c's formal contracts, which would declare T3 and T4 as their own dependencies. The formal contract becomes:
  ```
  *Formal Contract:*
  - *Axiom:* Valid address tumblers satisfy zeros(t) ≤ 3, (A i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0 : tᵢ > 0), no adjacent zeros, t₁ ≠ 0, t_{#t} ≠ 0.
  ```
- **(Option B)** Keep the postconditions but add T3 to the dependency list and reclassify T4 as a theorem (axiom as precondition, consequences as postconditions), removing the "T4 is an axiom" declaration from the narrative.

### TA6

Looking at the proof of TA6 against the checklist.

**Conjunct 1 (invalidity):** The proof argues: "In particular `t₁ = 0`." This instantiates the universal quantifier `(A i : 1 ≤ i ≤ #t : tᵢ = 0)` at `i = 1`, which requires `1 ≤ #t`. But if `#t = 0`, the empty tumbler is vacuously a zero tumbler (the quantifier `(A i : 1 ≤ i ≤ 0 : tᵢ = 0)` holds trivially), yet `t₁` does not exist and the step "In particular `t₁ = 0`" is unjustified. The conclusion is still true — T4 requires `t₁ ≠ 0`, which cannot be satisfied when there is no first component — but the proof's reasoning path doesn't cover this case.

**Conjunct 2 (ordering):** Case 1 (`k ≤ m`) and Case 2 (`k > m`) are exhaustive. The empty zero tumbler (`m = 0`) falls correctly into Case 2 since `k ≥ 1 > 0`, and the argument goes through with vacuously true quantifiers. No gap here.

**Checklist items 3–7:** Both postconditions match the formal contract. Dependencies T1 and T4 are correctly declared and used. No undeclared dependencies or missing guarantees.

```
RESULT: FOUND

**Problem**: Conjunct 1 does not handle the boundary case `#t = 0`. The proof states "In particular `t₁ = 0`," instantiating the universal quantifier at `i = 1`, which requires `#t ≥ 1`. The empty tumbler satisfies the zero-tumbler predicate vacuously (no components to check), yet has no first component, so the step `t₁ = 0` is unjustified.

**Required**: Add a case split: "If `#t = 0`, then `t` has no first component and cannot satisfy T4's requirement `t₁ ≠ 0`, so `t` is not a valid address. If `#t ≥ 1`, then in particular `t₁ = 0`, violating T4's `t₁ > 0`."
```

### T10a

## Verification of T10a (AllocatorDiscipline)

**1. Precondition completeness** — T10a is a design axiom, so no preconditions in the derivational sense are needed. Acceptable.

**2. Case coverage** — The section outlines three consequences (T10a.1, T10a.2, T10a.3) and a necessity argument (T10a-N) but delegates their proofs to sub-properties. The trailing sentence ("We first establish a lemma…") confirms the proofs follow in subsequent sections. Acceptable as a parent axiom declaration.

**3. Postcondition establishment** — The formal contract lists three postconditions (a), (b), (c) corresponding to T10a.1, T10a.2, T10a.3. None of these are proven in this section — they are stated as consequences to be established by sub-properties. This creates a structural problem: the formal contract claims postconditions that this section does not establish.

**4. All conjuncts addressed** — All three consequences and the necessity argument are named and described. Their proofs are deferred to sub-properties.

**5. Dependency correctness** — Dependencies state "(none)". However:
- The axiom and narrative use `inc(·, k)`, which must be defined in a tumbler algebra property.
- The necessity argument explicitly references "the T10 precondition" — T10 is not listed as a dependency.
- The formal contract postconditions use predicates `same_allocator(tᵢ, tⱼ)`, `sibling(tᵢ)`, and `spawned_by(t_child, t_parent)` that are neither defined here nor provided by any dependency.

**6. Formal contract** — The contract mixes an Axiom field with a Postconditions field. If T10a is purely an axiom (as the narrative states), its contract should contain only the Axiom field. The postconditions are consequences proven by sub-properties T10a.1–T10a.3 and belong in *their* contracts, not here. Including unproven postconditions in the axiom's contract means the contract claims more than this section establishes.

**7. Missing guarantees** — The postconditions reference `same_allocator`, `sibling`, and `spawned_by` without any dependency providing their definitions. These are not standard tumbler operations — they are allocator-specific predicates that need a defining property.

---

```
RESULT: FOUND

**Problem**: The formal contract includes three Postconditions — (a) uniform sibling
length, (b) non-nesting sibling prefixes, (c) length separation — but this section
proves none of them; it delegates to sub-properties T10a.1, T10a.2, T10a.3. An
axiom's formal contract should not claim postconditions the section does not establish.

Additionally, dependencies are listed as "(none)" but the section relies on:
  1. `inc(·, k)` — used throughout but not defined here or by any dependency.
  2. T10 — the necessity argument states "violating the T10 precondition" but T10
     is not a declared dependency.
  3. Predicates `same_allocator`, `sibling`, `spawned_by` — appear in the formal
     contract postconditions but are undefined.

**Required**:
  (a) Remove the Postconditions from T10a's formal contract. The contract should
      contain only the Axiom field (the allocator discipline constraint). Move
      postconditions (a), (b), (c) to the formal contracts of T10a.1, T10a.2, T10a.3
      respectively, where their proofs reside.
  (b) Add dependencies for: the property defining `inc(·, k)` (tumbler increment),
      the property defining `same_allocator`/`sibling`/`spawned_by` predicates,
      and T10 (whose precondition the necessity argument references).
```

### OrdinalDisplacement

```
RESULT: FOUND

**Problem**: The property section has no `*Formal Contract:*` block. OrdinalDisplacement is a definition and should end with a formal contract capturing its preconditions and construction rule.

**Required**: Append a formal contract such as:

*Formal Contract:*
- *Preconditions:* n ≥ 1, m ≥ 1
- *Definition:* δ(n, m) = [0, 0, …, 0, n] of length m with action point m
```

### OrdinalShift

## Verification of OrdinalShift

**Checking dependencies:** The property uses `δ(n, m)` throughout — asserting its action point is `m`, its length is `m`, and that it is positive — but no definition of `δ` appears in the provided dependencies. The entire derivation depends on knowing that `δ(n, m) = [0, ..., 0, n]` of length `m`, yet this is neither defined in the property section nor declared as a dependency.

**Checking TA0 applicability:** For TA0 to apply, we need `δ(n, m) > 0` and `actionPoint(δ(n, m)) ≤ #v`. Both follow from the (undeclared) definition of `δ`, but without that dependency grounding them, the reasoning is unsupported.

**Checking component-wise claims against TumblerAdd:** Assuming the standard δ definition, the TumblerAdd application is correct: prefix copies (i < m), action-point addition (i = m), and no tail (since #w = m = #v and k = m). The depth-preservation claim `#shift(v, n) = m` follows from the result-length identity. The positivity claim `vₘ + n ≥ 1` is correct since `n ≥ 1` and `vₘ ∈ ℕ`.

**Checking formal contract:** The property section has no `*Formal Contract:*` block.

```
RESULT: FOUND

**Problem 1 — Missing dependency**: δ(n, m) is used but not declared as a dependency
and not defined within this property section. The text asserts "the action point of
δ(n, m) is m" and "#δₙ = m" as facts, but no provided dependency establishes them.
Every claim in the proof flows through δ's structure.

**Required**: Declare the definition of δ(n, m) (the unit displacement constructor)
as an explicit dependency, or inline its definition within this property section.

**Problem 2 — Missing formal contract**: No `*Formal Contract:*` section is present.
The property is a definition with derived guarantees. Expected:

  *Formal Contract:*
  - *Preconditions:* v ∈ T, n ≥ 1
  - *Definition:* shift(v, n) = v ⊕ δ(n, #v)
  - *Postconditions:* shift(v, n) ∈ T, #shift(v, n) = #v,
    shift(v, n)ᵢ = vᵢ for i < #v, shift(v, n)_{#v} = v_{#v} + n
```

### PositiveTumbler

## Verification of PositiveTumbler

**Checking the property section against the verification checklist:**

1. **Precondition completeness** — The definition is clear: `t ∈ T`, positivity requires at least one nonzero component, zero requires all components zero. OK.

2. **Case coverage** — The informal ordering claim ("every positive tumbler is greater than every zero tumbler") covers two sub-cases implicitly ("has a smaller component … or has run out of components") but does not explicitly handle agreement at positions before the first nonzero component, nor distinguish the sub-case where `#z < k` (zero tumbler shorter than the first nonzero position) from `#z ≥ k`. The reasoning is correct but not rigorous — there is no structured proof with ∎.

3. **Postcondition establishment** — The ordering claim is argued informally in one sentence. It does not constitute a proof. The argument says "at position `k`" without specifying that `k` must be the *first* nonzero component (needed so that all positions `i < k` agree between `t` and `z`, as T1 requires a first-divergence witness, not just any divergence).

4. **All conjuncts addressed** — The definition (two parts: positive and zero) is stated. The ordering consequence is asserted but not proved.

5. **Dependency correctness** — T1 is used for the ordering claim. T3 is used for distinctness of zero tumblers of different lengths. TA0 and TA4 are mentioned as motivation ("The condition `w > 0` in TA0 and TA4 excludes…") but are not logically depended upon — PositiveTumbler *defines* what they reference, not the other way around.

6. **Formal contract** — **Missing entirely.** The property section ends at "…excludes all all-zero displacements regardless of length." with no `*Formal Contract:*` block.

7. **Missing guarantees** — No missing external guarantees; the ordering claim follows from T1 and the definition.

---

```
RESULT: FOUND

**Problem**: The property section has no `*Formal Contract:*` block. PositiveTumbler
establishes a definition (positive tumbler, zero tumbler) and claims a derived ordering
guarantee ("Every positive tumbler is greater than every zero tumbler under T1"), but
neither the definition nor the guarantee appears in a formal contract. Per checklist
item 6: "If the formal contract is missing or incomplete, flag as FOUND."

Additionally, the ordering claim lacks a rigorous proof (no ∎). The one-sentence
argument — "if t has a nonzero component at position k, then at position k either the
zero tumbler has a smaller component (0 < tₖ) or has run out of components" — does not
specify that k is the *first* nonzero component (required for T1's agreement condition
at all positions before the divergence), and does not distinguish the two T1 cases
(component comparison vs. prefix exhaustion) with enough detail to constitute a proof.

**Required**: 
1. Add a formal contract, e.g.:

   *Formal Contract:*
   - *Definition:* t > 0 iff (E i : 1 ≤ i ≤ #t : tᵢ ≠ 0); t is a zero tumbler
     iff (A i : 1 ≤ i ≤ #t : tᵢ = 0).
   - *Postcondition:* (A t, z ∈ T : t > 0 ∧ (A j : 1 ≤ j ≤ #z : zⱼ = 0) : z < t)

2. Provide a rigorous proof of the ordering postcondition, with explicit case
   analysis on whether #z < k or #z ≥ k (where k is the first nonzero position
   of t), verifying the T1 agreement condition at positions before the divergence.
```

45 verified, 10 found.
