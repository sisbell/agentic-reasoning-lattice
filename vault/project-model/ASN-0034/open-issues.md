### [REVIEW-39] [VERIFIED] T0(a)

### [REVIEW-39] [VERIFIED] T3

### [REVIEW-39] [VERIFIED] T1

### [REVIEW-39] [VERIFIED] T4

### [REVIEW-39] [VERIFIED] TA6

### [REVIEW-39] [VERIFIED] TA3

### [REVIEW-39] [FOUND] TA0
**Checklist Analysis**

1. **Precondition completeness** — All inputs and conditions are stated: `a ∈ T`, `w ∈ T`, `w > 0`, `actionPoint(w) ≤ #a`. Complete.

2. **Case coverage** — Three regions (prefix, action point, tail) cover all indices `1..n`. Boundary cases (k=1 making prefix vacuous, k=n making tail vacuous) are handled by the length arithmetic. Complete.

3. **Postcondition establishment** — Both `a ⊕ w ∈ T` and `#(a ⊕ w) = #w` are explicitly shown. Complete.

4. **All conjuncts addressed** — Membership in T requires (a) finite length, (b) length ≥ 1, (c) all components ∈ ℕ. All three are verified. The length identity is separately established. Complete.

5. **Dependency correctness** — **Mismatch.** The proof's dependency block declares:

   > **T0(a) (Carrier-set definition):** T is the set of all finite sequences over ℕ with length ≥ 1.

   But the provided T0(a) is **"Unbounded component values"** — the property that for every tumbler, component position, and bound M, there exists a tumbler exceeding M at that position. The carrier-set definition ("T is the set of all finite sequences over ℕ with length ≥ 1") appears only as an *axiom* within T0(a)'s formal contract, not as T0(a) itself. The proof never uses the unboundedness property; it only uses the carrier-set axiom. So T0(a) is declared but not used for what it actually states, and the carrier-set axiom is used but cited under the wrong label.

6. **Formal contract** — Preconditions and postconditions match the narrative exactly. Complete.

7. **Missing guarantees** — The proof uses closure of ℕ under addition (at the action point). T0(a)'s axiom states closure under *successor*; closure under addition follows by induction but is not explicitly provided by any declared dependency. This is minor (standard mathematical background) but worth noting.

---

```
RESULT: FOUND

**Problem**: The dependency block cites "T0(a) (Carrier-set definition)" but the
actual T0(a) is "Unbounded component values" — a different property entirely. The
proof never uses T0(a)'s unboundedness claim; it only uses the carrier-set axiom
(T is the set of all finite sequences over ℕ with length ≥ 1), which is a
foundational axiom listed *within* T0(a)'s formal contract, not T0(a) itself.

**Required**: Replace the T0(a) dependency citation with the correct label for the
carrier-set axiom (likely T0 or whichever property/axiom actually defines T's
carrier set). If no such standalone axiom exists in the spec, one should be
introduced and cited here. T0(a) should be removed from TA0's dependency list
since its content (unbounded component values) is not used by this proof.
```

### [REVIEW-40] [VERIFIED] TA0

### [REVIEW-40] [RESOLVED] TA0

### [REVIEW-40] [VERIFIED] TA1-strict

### [REVIEW-40] [FOUND] TumblerSub
I need to verify the TumblerSub property section, including its definition, the TA1/TA1-strict verification, the TA3/TA3-strict verification, and the TA4 cancellation proof.

**Checking precondition completeness, case coverage, postcondition establishment, formal contracts, and dependencies.**

The TumblerSub definition is well-formed. The TA1/TA1-strict verification within the property section is sound — the three-case analysis on `k` vs `j = divergence(a, b)` is exhaustive and each case correctly establishes its conclusion. The TA3-strict proof correctly eliminates Case 0 via equal-length.

However, in the **TA3 verification** (property section version), there is a gap in the transition from Case 0a to Cases 1–3. The proof states:

> For the remaining cases, `a < b` by T1 case (i) and `a` is not zero-padded-equal to `w`, so `dₐ = divergence(a, w)` is well-defined. Let `d_b = divergence(b, w)` (under zero-padding).

The proof then case-splits on the ordering of `dₐ` vs `d_b`. But it never establishes that `d_b` is well-defined — i.e., that `b` is **not** zero-padded-equal to `w`. The three-way case split (`dₐ = d_b`, `dₐ < d_b`, `dₐ > d_b`) is only valid when both values exist.

The canonical TA3 proof in the dependencies (Sub-case B1→B2 transition) fills exactly this gap with an explicit argument: if `b` were zero-padded-equal to `w`, then at position `dₐ` we'd have `a_{dₐ} > w_{dₐ} = b_{dₐ}` (since `a ≥ w` forces `a_{dₐ} > w_{dₐ}` at the divergence), while `aᵢ = wᵢ = bᵢ` for all `i < dₐ`, giving `a > b` by T1 — contradicting `a < b`. The property section's proof omits this argument entirely.

```
RESULT: FOUND

**Problem**: The TA3 proof in the property section assumes `d_b = divergence(b, w)` is well-defined without justification. At the transition "For the remaining cases... Let `d_b = divergence(b, w)` (under zero-padding)", the proof does not rule out the possibility that `b` is zero-padded-equal to `w`, which would make `d_b` undefined and invalidate the subsequent three-way case split on `dₐ` vs `d_b`. The canonical TA3 proof in the dependencies (between Sub-cases B1 and B2) includes the necessary contradiction argument; the property section's version omits it.

**Required**: Between Case 0a and the "remaining cases" paragraph, add: "We show `d_b` is well-defined. If `b` were zero-padded-equal to `w`, then since `dₐ` exists, `a_{dₐ} > w_{dₐ}` (from `a ≥ w` at the first padded divergence) and `w_{dₐ} = b_{dₐ}` (from `b`'s zero-padded equality with `w`), giving `a_{dₐ} > b_{dₐ}`. At all positions `i < dₐ`, `aᵢ = wᵢ = bᵢ`. By T1 case (i), `a > b` — contradicting `a < b`. So `b` is not zero-padded-equal to `w` and `d_b` is well-defined."
```

### [REVIEW-41] [FOUND] TumblerSub
I'll work through the verification checklist systematically for the proofs in the TumblerSub property section.

**1. Precondition completeness** — All required inputs and conditions are stated for TA1/TA1-strict (a < b, w > 0, k ≤ min(#a, #b)), TA3/TA3-strict (a < b, a ≥ w, b ≥ w, plus #a = #b for strict), and TA4 (k = #a, #w = k, zero prefix). TA4 implicitly requires w > 0 through the existence of an action point, which is acceptable.

**2. Case coverage** — TA1/TA1-strict: three cases (k < j, k = j, k > j) are exhaustive; the prefix sub-case of T1(ii) forces k < j and falls into Case 1. TA3: Case 0 (prefix), Case 0a (component divergence + zero-padded equality with w), Cases 1–3 (component divergence + divergence with w) are exhaustive and correctly partitioned. Case 2 impossibility is valid. TA3-strict: eliminating Case 0 via #a = #b is sound; the remaining cases all produce strict inequality. TA4: two sub-cases on a_k cover all possibilities.

**3. Postcondition establishment** — Each case of TA1 establishes ≤ (via equality or strict). TA1-strict establishes strict inequality in Cases 2 and 3. Every TA3 case establishes ≤. TA3-strict's remaining cases all establish strict. TA4 reconstructs a in both sub-cases.

**4. All conjuncts addressed** — Each property has a single postcondition and each is proved.

**5. Dependency correctness** — The proofs use T1 (order definition/comparison), TumblerAdd constructive definition and TA0 (via TA1's dependency), TA2 (well-definedness of subtraction), TumblerSub (the definition under verification), and the inline derivation (†) from T1 alone. No undeclared dependencies are used. The Divergence definition is correctly applied in the transition to Cases 1–3 and in TA1-strict.

**6. Formal contract** — TumblerSub definition has a correct formal contract. TA3 and TA3-strict have correct formal contracts matching their narrative claims. TA1 and TA1-strict are formally contracted in the dependencies section. However, **TA4 has no formal contract anywhere** — neither in the property section nor in the dependencies. The claim is stated in prose but lacks the required `*Formal Contract:*` block.

**7. Missing guarantees** — The TA3 proof's inline derivation (†) is fully established from T1. The TA4 proof implicitly verifies r ≥ w (needed for TumblerSub to apply) via construction. No missing external guarantees.

---

```
RESULT: FOUND

**Problem**: The TA4 verification (cancellation: `(a ⊕ w) ⊖ w = a`) has no `*Formal Contract:*` block. It is the only property in the section that is both defined and proved here (not inherited from the dependencies) yet lacks a formal contract. The claim text states preconditions in prose ("under the full precondition: k = #a, #w = k, (A i : 1 ≤ i < k : aᵢ = 0)") but does not formalize them.

**Required**: Add a formal contract after the TA4 proof, e.g.:

    *Formal Contract:*
    - *Preconditions:* a ∈ T, w ∈ T, w > 0, actionPoint(w) = #a, #w = #a, (A i : 1 ≤ i < #a : aᵢ = 0)
    - *Postconditions:* (a ⊕ w) ⊖ w = a
```

### [REVIEW-42] [VERIFIED] TumblerSub

### [REVIEW-42] [RESOLVED] TumblerSub

### [REVIEW-42] [VERIFIED] TA2

### [REVIEW-42] [VERIFIED] TA4

### [REVIEW-42] [FOUND] TumblerAdd
I need to verify the TumblerAdd definition against the checklist.

**1. Precondition completeness** — The preamble states `w > 0` and the explicit precondition states `k ≤ m`. Together these are complete for the definition. ✓

**2. Case coverage** — The piecewise definition covers `i < k`, `i = k`, `i > k` — exhaustive over all positions in the result. ✓

**3. Postcondition establishment** — The result-length identity derivation:
- `p = max(k-1, 0) + (n - k + 1)` counts prefix (`k-1` positions), action point (1 position), and tail (`n - k` positions). Correct.
- `w > 0` implies `k ≥ 1`, so `max(k-1, 0) = k-1`, giving `p = (k-1) + (n-k+1) = n = #w`. Correct. ✓

**4. All conjuncts addressed** — The three named properties (no carry propagation, tail replacement, many-to-one) are all stated and illustrated. ✓

**5. Dependency correctness** — TumblerAdd is a standalone constructive definition. It does not reference any of the listed dependencies (which serve TA4's proof). No undeclared dependencies are used. ✓

**6. Formal contract** — The property section ends with the many-to-one examples. There is **no `*Formal Contract:*` section**.

**7. Missing guarantees** — N/A for a self-contained definition.

```
RESULT: FOUND

**Problem**: The TumblerAdd property section has no formal contract. The definition
establishes preconditions (w > 0, actionPoint(w) ≤ #a), a constructive rule
(the piecewise formula), and a derived postcondition (the result-length identity
#(a ⊕ w) = #w), but none of these are collected into a formal contract block.

**Required**: Append a formal contract to the end of the TumblerAdd property section:

*Formal Contract:*
- *Preconditions:* a ∈ T, w ∈ T, w > 0, actionPoint(w) ≤ #a
- *Definition:* (a ⊕ w)ᵢ = aᵢ for i < k, (a ⊕ w)ₖ = aₖ + wₖ, (a ⊕ w)ᵢ = wᵢ for i > k, where k = actionPoint(w)
- *Postconditions:* #(a ⊕ w) = #w
```

### [REVIEW-43] [VERIFIED] TumblerAdd

### [REVIEW-43] [RESOLVED] TumblerAdd

### [REVIEW-43] [VERIFIED] TA1

### [REVIEW-43] [VERIFIED] Divergence

### [REVIEW-43] [VERIFIED] D1

### [REVIEW-43] [VERIFIED] D0

### [REVIEW-43] [VERIFIED] TA-LC

### [REVIEW-43] [VERIFIED] D2

### [REVIEW-43] [VERIFIED] T2

### [REVIEW-43] [VERIFIED] TA5

### [REVIEW-43] [VERIFIED] T10

### [REVIEW-43] [VERIFIED] T10a

### [REVIEW-43] [FOUND] T8
## Verification of T8 (Allocation permanence)

The core argument — axiom (no removal) + T10a (sole addition mechanism, which only adds) + induction — is sound. The induction step correctly applies transitivity of ⊆. Case 3 correctly derives `allocated(s) ⊆ allocated(s) ∪ {t'} = allocated(s')` from T10a.

However, the case analysis has an undeclared dependency.

**Case 2** asserts: "The operations ⊕ (tumbler addition), ⊖ (tumbler subtraction), and inc (hierarchical increment) are pure functions on T … they neither read from nor write to the allocated set." For `inc`, this is grounded in TA5 (declared dependency), which defines it as a pure construction. For ⊕ and ⊖, no definition is cited. The proof claims these operations don't modify the allocated set, but their definitions are absent from the dependency list.

The same operations appear in the formal contract's Frame clause:

> *Frame:* Read-only operations (T1, T2, T4) and pure arithmetic (⊕, ⊖, inc) preserve the allocated set exactly: `allocated(s') = allocated(s)`.

The proof also claims "These three cases are exhaustive — every operation the system defines belongs to one of them," but the exhaustiveness of the enumeration is unsupported without citing the definitions of all operations listed.

```
RESULT: FOUND

**Problem**: Case 2 references tumbler addition (⊕) and tumbler subtraction (⊖) 
as "pure functions on T" that "neither read from nor write to the allocated set," 
and the formal contract's Frame clause names them explicitly, but neither operation 
is declared as a dependency. The proof cites T1, T2, T4 in Case 1 and TA5 (inc) 
in Cases 2–3, yet ⊕ and ⊖ have no corresponding citation. The claim of exhaustive 
case analysis over "every operation the system defines" requires that all enumerated 
operations have their definitions grounded in the dependency list.

**Required**: Add the definitions of ⊕ (tumbler addition) and ⊖ (tumbler subtraction) 
to the dependency list, with a note establishing their pure-function character 
(analogous to how T1/T2/T4 are cited as "read-only operations" and TA5 is cited 
for inc). Alternatively, remove ⊕ and ⊖ from the case analysis and Frame clause, 
relying solely on the axiom ("no operation removes") which already covers them.
```
