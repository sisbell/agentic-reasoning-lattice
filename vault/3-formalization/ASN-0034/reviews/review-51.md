# Proof Review — ASN-0034 (cycle 1)

*2026-04-15 18:28*

63 properties

### T3

## Verification of T3 (CanonicalRepresentation)

**1. Precondition completeness** — All inputs stated: a, b ∈ T. T is grounded in T0. ✓

**2. Case coverage** — Both directions of the biconditional are proved explicitly. No boundary cases are missed; T0 guarantees n ≥ 1 so empty sequences are excluded by construction. ✓

**3. Postcondition establishment** — Forward direction establishes a = b from component-wise equality via extensional sequence equality. Reverse direction establishes component-wise equality from a = b via Leibniz's law. Both are explicit and complete. ✓

**4. All conjuncts addressed** — The biconditional has two directions; both are proved. The design commitment (no quotient, no trailing-zero identification) is stated explicitly in the closing paragraph. ✓

**5. Dependency correctness** — T0 is declared and used (to establish that T consists of finite sequences over ℕ, making extensional sequence equality applicable). No undeclared dependencies. ✓

**6. Formal contract** — The content of the formal contract accurately captures the property. However, the field label is wrong. T3 is not the postcondition of any operation — there is no operation here, no inputs consumed, no outputs produced. The proof itself says "T3 is not derived from other properties; it holds by the definition of the carrier set." This is an axiom-level assertion: tumbler equality *is* sequence equality, by design. The field should be `*Axiom:*`, not `*Postconditions:*`.

**7. Missing guarantees** — None. The proof relies only on T0 (what T is) and the standard definition of sequence equality, both of which are available. ✓

```
RESULT: FOUND

**Problem**: Formal contract uses `*Postconditions:*` but T3 is not the result of an operation — it is a structural identity that holds by definition of the carrier set (as the proof explicitly states: "T3 is not derived from other properties; it holds by the definition of the carrier set"). There is no operation with pre/post conditions here.

**Required**: Change the formal contract field from `*Postconditions:*` to `*Axiom:*`:

*Formal Contract:*
- *Axiom:* Tumbler equality is sequence equality: `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`. No quotient, normalization, or external identification is imposed on T.
```

### T4

RESULT: FOUND

**Problem**: The formal contract includes a `Preconditions` field listing T3 (CanonicalRepresentation), but T4 is declared as an axiom. Axioms are foundational assertions — they have no preconditions. The narrative itself confirms T3 is needed for the corollary, not for T4: *"T3 is essential for T4b: canonical representation guarantees that the component sequence of t is fixed..."* This also contradicts the Dependencies section, which correctly states "(none)." Additionally, the formal contract includes a non-standard `Corollaries` field; the defined contract fields are Preconditions, Postconditions, Invariant, Frame, Axiom, and Definition only.

**Required**: Remove the `Preconditions` and `Corollaries` fields from T4's formal contract, leaving only the `Axiom` field. The T3 dependency belongs in T4b's own formal contract (where the uniqueness result that actually needs canonical representation is proved). The corollaries listing is informational prose appropriate to the narrative body, not to the formal contract block.

### T2

```
RESULT: FOUND

**Problem**: The proof references T1 and T3 but neither is declared as a dependency. Specifically:
- "The definition of `<` in T1 asks for the existence of a witness position `k ≥ 1`…" — T1 is the entire subject of the proof; its definition is needed to verify that the case analysis is faithful to the actual ordering.
- "if `m = n`, then T3 gives `a = b`" — T3 is invoked in Case 2 to resolve the equal-length sub-case.

Only T0 appears in the dependency list. T1 and T3 are used but not declared.

**Required**: Add T1 and T3 to the declared dependencies for T2. Both are load-bearing: T1 supplies the definition being analyzed, and T3 supplies the equality conclusion in Case 2.
```

### OrdinalDisplacement

```
RESULT: FOUND

**Problem**: The property states "Its action point is m" and the formal contract includes "action point m" in the definition, but no dependency defining the general concept of "action point" is provided. Neither T0 nor PositiveTumbler defines action point. The claim that the action point of δ(n, m) is m cannot be verified against a formal definition when that definition is absent from the dependency list.

**Required**: Add the property that defines "action point" (likely something like "the action point of a tumbler t is the largest index k such that tₖ ≠ 0") as a declared dependency. Then either (a) prove that the action point of δ(n, m) equals m under that definition (since positions 1..m−1 are zero and position m is n ≥ 1), or (b) if action point is purely stipulated as part of this definition rather than derived from a general concept, clarify that in the narrative and remove the postcondition-style assertion.
```

### PartitionMonotonicity

I need to carefully verify the PartitionMonotonicity proof against its dependencies and the checklist.

## Analysis

### Checking proof structure

The proof proceeds in four stages: (1) establish partition structure, (2) show sibling prefixes are non-nesting, (3) cross-partition ordering via PrefixOrderingExtension, (4) intra-partition ordering via structural induction on nesting depth. The non-nesting argument (uniform length from TA5(c), distinctness from TA5(a), equal-length implies no proper prefix from Prefix) is correct. The PrefixOrderingExtension application is valid — preconditions (strict order + non-nesting) are properly established.

### Checking the structural induction

- **Termination**: Each child-spawning adds ≥ 1 to length (TA5(d)), finite length bounds depth. ✓  
- **Base case**: No child spawned → single address → trivially ordered. ✓  
- **Inductive step**: Sub-sub-partitions ordered by PrefixOrderingExtension, within each by hypothesis, root precedes all by T1 case (ii). ✓ (within assumptions)

### Identifying the gap

The proof's "Total ordering" section asserts:

> "every allocated address a ≠ p belongs to exactly one sub-partition — the unique sub-partition whose prefix it extends (existence holds because the allocator discipline requires every such a to have been produced by **the child allocator** or a descendant thereof, hence to extend some tᵢ)"

This uses the **singular definite article** — "the child allocator" — assuming exactly one child allocator spawned from `p`, producing a single sibling stream `t₀, t₁, t₂, ...`. However, T10a's formal constraint is per `(t, k')` pair:

> "Each pair (t, k') — a domain element t of the parent together with a spawning parameter k' ∈ {1, 2} — produces at most one child-spawning event"

The pairs `(p, 1)` and `(p, 2)` are **distinct pairs**, each permitted one event. When `zeros(p) ≤ 2`, both `inc(p, 1)` and `inc(p, 2)` preserve T4 (by TA5a), so T10a allows two children from the same domain element at different depths. Addresses from the second child's sibling stream do not extend any prefix in the first child's stream, breaking the existence claim.

**Concrete example.** Let `p = (2)`. The parent spawns two children:

- Child A via `inc(p, 1) = (2, 1)`; siblings: `(2, 1), (2, 2), (2, 3), ...` at length 2
- Child B via `inc(p, 2) = (2, 0, 1)`; siblings: `(2, 0, 1), (2, 0, 2), ...` at length 3

Address `(2, 0, 1)` is in partition `{a : (2) ≼ a}` but extends **none** of `(2, 1), (2, 2), (2, 3), ...`. The proof's existence argument fails.

The same gap propagates into the inductive step, which also uses "the child allocator" (singular) when discussing sub-sub-partitions headed by `uⱼ`.

**Note:** The total ordering conclusion is still **true** in the multi-child case — Child B's addresses all precede Child A's by PrefixOrderingExtension (at position 2: `0 < 1`, non-nesting since lengths differ), and within each child's domain the single-child argument applies. But the proof as written does not establish this.

### Other checks

- **Non-nesting argument**: Sound. ✓  
- **Dependency usage**: All declared dependencies (Prefix, PrefixOrderingExtension, T1, T3, T5, T9, T10a, TA5) are used. No undeclared dependencies. ✓  
- **Formal contract**: Postconditions and invariant match the property statement. Preconditions reference "the parent allocator's single deep increment" — consistent with the single-child assumption but inconsistent with T10a's formal constraints. ✓/partially  
- **All conjuncts**: Total ordering, per-allocator consistency, and cross-partition ordering are all addressed. ✓  

```
RESULT: FOUND

**Problem**: The proof assumes exactly one child allocator per partition level
("the child allocator" — singular definite, in both the "Total ordering" and
"Inductive step" sections), producing a single sibling stream t₀, t₁, t₂, ....
The existence claim — "every allocated address a ≠ p belongs to exactly one
sub-partition" — requires all partition addresses to extend some tᵢ from this
single stream. However, T10a's constraint is per (t, k') pair, permitting two
child-spawning events from the same domain element p: inc(p, 1) and inc(p, 2).
When zeros(p) ≤ 2 (TA5a), both preserve T4, so T10a admits two children at
different depths. Addresses from the second child (e.g., p.0.1 when the first
child's stream is p.1, p.2, p.3, ...) do not extend any first-child sibling.

Counterexample: p = (2), Child A from inc(p,1) = (2,1) with siblings (2,1),
(2,2), (2,3), ...; Child B from inc(p,2) = (2,0,1) with siblings (2,0,1),
(2,0,2), .... Address (2,0,1) ∈ {a : (2) ≼ a} but extends no tᵢ in
{(2,1), (2,2), (2,3), ...}.

The ordering conclusion holds (Child B precedes Child A by
PrefixOrderingExtension at position 2: 0 < 1, non-nesting), but the proof
does not establish it.

**Required**: Either (1) generalize the structural induction to handle multiple
child allocators per partition level — showing their sub-partition prefix sets
are mutually non-nesting across different depths and ordered by
PrefixOrderingExtension — or (2) tighten T10a's formal contract to restrict
each domain element to at most one child-spawning event (one k' per t), rather
than one per (t, k') pair.
```

### TA3-strict

## Verification Analysis

**Precondition completeness**: All preconditions (a, b, w ∈ T, a < b, a ≥ w, b ≥ w, #a = #b) are stated and used. The equal-length condition correctly eliminates T1 case (ii). Complete.

**Case coverage**: Exhaustive. Case A (zero-padded equality) plus three cases on divergence-point ordering (d_a = d_b, d_a < d_b, d_a > d_b). Case 2 correctly shown impossible. Case 1 subcases (j = d, j > d) are exhaustive since j ≥ d is established. No missing boundaries.

**Postcondition establishment**: Every non-impossible case concludes with an explicit T1 case (i) application yielding a ⊖ w < b ⊖ w. Established.

**All conjuncts**: Single postcondition, addressed.

**Formal contract**: Matches the property statement. The added type constraints (a ∈ T, b ∈ T, w ∈ T) are implicit in the universal quantification. Correct.

**Missing guarantees**: None — all assumed facts are derivable from the definitions recalled in the Preliminaries.

**Dependency correctness**: The dependency list states **(none)**, but the proof explicitly cites two properties by name:

1. **TA2** — "By TA2, both a ⊖ w and b ⊖ w are well-defined members of T." This is logically necessary: the proof applies T1 to the subtraction results, and T1 requires its inputs to be in T. Without TA2, this precondition is unestablished.

2. **TA6** — Case A: "TA6 gives a ⊖ w < b ⊖ w." While this step *could* be replaced by direct T1 reasoning (first disagreement at j with 0 < b_j − w_j), the proof as written delegates to TA6 without declaring it.

---

```
RESULT: FOUND

**Problem**: The dependency list is "(none)" but the proof explicitly invokes
two undeclared properties:
  - TA2 (line: "By TA2, both a ⊖ w and b ⊖ w are well-defined members of T")
    — logically required to satisfy T1's precondition that its operands are in T.
  - TA6 (line: "TA6 gives a ⊖ w < b ⊖ w" in Case A)
    — cited as the justification for zero-tumbler < non-zero-tumbler ordering.

**Required**: Add TA2 and TA6 to the dependency list. Alternatively, for TA6,
replace the citation with inline T1 reasoning (the first disagreement between
the zero tumbler and b ⊖ w is at position j where 0 < b_j − w_j, giving
T1 case (i) directly), and add only TA2 as a dependency.
```

### TA1

RESULT: FOUND

**Problem**: The proof explicitly invokes four properties/definitions — **T1** (lexicographic ordering characterization of `<`), **T3** (component-wise equality implies tumbler equality), **TA0** (well-definedness of `⊕`, result ∈ T, result length = `#w`), and **TumblerAdd** (three-region definition of `⊕`) — but the dependency list declares **(none)**. Every logical step in the proof depends on at least one of these:

- T1 is used to decompose `a < b` into two cases, and again to conclude `a ⊕ w < b ⊕ w` in sub-cases j < k and j = k.
- T3 is used to conclude `a ⊕ w = b ⊕ w` from component-wise agreement in Case (ii) and sub-case j > k.
- TA0 is used to establish that `a ⊕ w` and `b ⊕ w` are well-defined members of T with length `#w`.
- TumblerAdd is used for the three-region structure (prefix-copy / advance / displacement-copy) that the entire case analysis is built on.

The proof's internal logic is sound — case coverage is exhaustive, each case establishes the postcondition, and the formal contract matches the property statement. But the dependency declarations are incomplete (checklist items 5 and 7).

**Required**: Declare T1, T3, TA0, and TumblerAdd as dependencies of TA1.

### TS2

## Verification of TS2 (ShiftInjectivity)

**Checklist analysis:**

1. **Precondition completeness** — Stated preconditions (v₁, v₂ ∈ T, n ≥ 1, #v₁ = #v₂ = m) match the quantifier guard. No constraint on m is stated; see case coverage below.

2. **Case coverage** — The proof applies TA-MTO directly without considering m = 0. When m = 0, step (i) claims "its m-th component is positive," but an empty sequence has no components. The conclusion v₁ = v₂ is trivially true (there is exactly one empty sequence), but the proof does not establish it — its main argument requires m ≥ 1 for δ(n, m) to have a positive component. A one-line dispatch ("If m = 0 then v₁ = v₂ = () and we are done; assume m ≥ 1") would close this.

3. **Postcondition establishment** — For m ≥ 1, the chain is sound: OrdinalShift expands shift to ⊕, TA-MTO's converse gives component-wise equality at all m positions, T3 gives v₁ = v₂.

4. **All conjuncts addressed** — Single implication, fully addressed (for m ≥ 1).

5. **Dependency correctness** — The proof uses **OrdinalShift** (to rewrite `shift(v, n)` as `v ⊕ δ(n, m)`) and **OrdinalDisplacement** (to characterize `δ(n, m) = [0, ..., 0, n]` and its action point). Neither is declared as a dependency. Both are load-bearing: without OrdinalShift the first rewriting step has no justification; without OrdinalDisplacement precondition (i) and the action-point value in (ii) are ungrounded.

6. **Formal contract** — Preconditions and postconditions match the property statement. Correct.

7. **Missing guarantees** — The guarantees of OrdinalShift and OrdinalDisplacement are assumed but not provided. No other missing guarantees beyond that.

```
RESULT: FOUND

**Problem**: Two undeclared dependencies. The proof invokes OrdinalShift (line: "By OrdinalShift, this assumption is v₁ ⊕ δ(n, m) = v₂ ⊕ δ(n, m)") and OrdinalDisplacement (line: "by OrdinalDisplacement, δ(n, m) = [0, ..., 0, n] with n ≥ 1") but neither appears in the dependency list. Additionally, the m = 0 edge case is not handled — the TA-MTO application requires δ(n, m) > 0 which fails for m = 0 (empty displacement has no positive component), though the conclusion holds trivially in that case.

**Required**: (1) Add OrdinalShift and OrdinalDisplacement to the declared dependencies. (2) Add a base-case dispatch for m = 0 before the TA-MTO argument (e.g., "If m = 0, both tumblers are the unique empty sequence and v₁ = v₂. Assume m ≥ 1 for the remainder.").
```

55 verified, 8 found.
