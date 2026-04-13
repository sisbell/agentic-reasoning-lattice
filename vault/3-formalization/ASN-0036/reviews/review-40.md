# Proof Review — ASN-0036 (cycle 2)

*2026-04-13 14:02*

20 properties (D-CTG, D-CTG-depth, D-MIN, D-SEQ, S0, S1, S2, S3, S5, S6, S7, S7a, S7b, S7c, S8, S8-depth, S8-fin, S8a, S9, ValidInsertionPosition)

### S7c

## Verification of S7c (Element-field depth)

S7c is an axiom (design requirement) asserting `(A a ∈ dom(Σ.C) :: #fields(a).element ≥ 2)`.

**Checklist analysis:**

1. **Precondition completeness** — The expression `#fields(a).element` is well-defined only when the element field exists, which by T4 requires `zeros(a) = 3`. S7b establishes exactly this for all `a ∈ dom(Σ.C)`. The narrative explicitly acknowledges this dependency: "With S7a and S7b established, we can state structural attribution." But the formal contract omits it.

2. **Case coverage** — N/A (axiom, not a proof).

3. **Postcondition establishment** — N/A (axiom).

4. **All conjuncts addressed** — Single conjunct, stated.

5. **Dependency correctness** — The narrative references T4, S7a, S7b, T10a, and TA7a. T10a is used to motivate why δ = 1 is problematic (it's reachable). TA7a is used to explain why δ ≥ 2 is needed (ordinal-only formulation requires a non-empty ordinal after removing the subspace identifier). These are appropriate.

6. **Formal contract** — **Gap found.** The formal contract is:
   ```
   - *Axiom:* (A a ∈ dom(Σ.C) :: #fields(a).element ≥ 2)
   ```
   Compare with S7a's formal contract, which follows the same pattern (axiom over `dom(Σ.C)` using `fields(a)`) but explicitly lists:
   ```
   - *Preconditions:* zeros(a) ≥ 2 for all a ∈ dom(Σ.C) — T4's field correspondence 
     requires this for the document field to exist. (Entailed by S7b: zeros(a) = 3.)
   ```
   S7c uses `fields(a).element`, which requires `zeros(a) = 3` for the element field to exist (T4 field correspondence). The narrative says this dependency exists ("With S7a and S7b established..."), but the formal contract doesn't state it.

7. **Missing guarantees** — No missing guarantees beyond the precondition gap above.

```
RESULT: FOUND

**Problem**: The formal contract omits the precondition that `fields(a).element` be well-defined. The quantified expression `#fields(a).element` requires the element field to exist, which T4's field correspondence guarantees only when `zeros(a) = 3`. The narrative acknowledges this: "With S7a and S7b established, we can state structural attribution." S7a's formal contract follows the correct pattern by listing `zeros(a) ≥ 2` as a precondition with a note "(Entailed by S7b)." S7c should do the same for `zeros(a) = 3`.

**Required**: Add a Preconditions field to the formal contract:
```
*Formal Contract:*
- *Axiom:* (A a ∈ dom(Σ.C) :: #fields(a).element ≥ 2)
- *Preconditions:* S7b (zeros(a) = 3 for all a ∈ dom(Σ.C)) — T4's field correspondence requires zeros(a) = 3 for the element field to exist and `#fields(a).element` to be well-defined.
```
```

### ValidInsertionPosition

Looking at the proof carefully against the checklist:

**Precondition completeness** — The narrative states "m ≥ 2" in the non-empty case and provides a detailed argument for why m = 1 fails (shift changes subspace). However, this constraint is absent from the formal contract.

**Case coverage** — Empty and non-empty are exhaustive; boundary N = 1 works. ✓

**Postcondition establishment** — Distinctness, depth preservation, subspace identity, and S8a consistency are all explicitly argued with correct reasoning, *provided* m ≥ 2 holds. ✓

**All conjuncts addressed** — All four postcondition conjuncts are proved. ✓

**Dependency correctness** — OrdinalShift and TumblerAdd (ASN-0034) are used but not listed as separate dependencies; however, their relevant properties are restated within the S8-depth dependency text (prefix preservation, result-length identity), which is sufficient. D-CTG is declared and used as a precondition on d. ✓

**Formal contract** — Mismatch with narrative. The formal contract's Definition field reads:

> (1) V_S(d) ≠ ∅ with |V_S(d)| = N and v = shift(min(V_S(d)), j) for 0 ≤ j ≤ N

No depth constraint appears in case (1). Case (2) explicitly states "of depth m ≥ 2." The Preconditions also omit m ≥ 2. Yet the narrative explicitly states "m ≥ 2" for the non-empty case and the subspace identity postcondition depends on it: at m = 1, min = [S], and shift([S], 1) = [S] ⊕ [1] produces [S + 1] — a position in subspace S + 1, not S. The justification ("the first position placed in any subspace is established by the empty case, which requires m ≥ 2, and S8-depth preserves depth thereafter") is an inductive argument about operational history, not a consequence of the four listed preconditions. A document state with V_S(d) = {[S]} satisfies D-CTG, S8-depth, D-MIN, and S8a, yet has m = 1.

```
RESULT: FOUND

**Problem**: The formal contract omits the m ≥ 2 constraint for the non-empty case.
The narrative states "m ≥ 2" and proves it is load-bearing (m = 1 breaks subspace
identity), but the formal contract's Definition for case (1) and its Preconditions
do not include this constraint. The listed preconditions (D-CTG, S ≥ 1, S8-depth,
D-MIN) are jointly satisfiable at m = 1 — e.g., V_S(d) = {[S]} satisfies all four —
yet at m = 1 the postcondition v₁ = S fails for j ≥ 1.

**Required**: Add m ≥ 2 to the formal contract — either as a precondition
("S8-depth holds for V_S(d) with common depth m ≥ 2") or as an explicit constraint
in case (1) of the Definition ("with |V_S(d)| = N and common depth m ≥ 2"). This
makes the formal contract match the narrative's stated requirement and closes the
gap that the subspace identity postcondition depends on.
```

18 verified, 2 found.
