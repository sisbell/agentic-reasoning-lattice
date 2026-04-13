# Proof Review — ASN-0036 (cycle 1)

*2026-04-12 19:21*

32 properties

### S8-fin

RESULT: FOUND

**Problem**: The formal contract's *Invariant* field embeds proof methodology that is not part of the invariant itself. The invariant is stated as:

> `dom(Σ.M(d)) is finite for every document d and every reachable state Σ. Base case: the initial-state axiom (Σ.M(d)) establishes dom(Σ₀.M(d)) = ∅.`

The second sentence ("Base case: the initial-state axiom (Σ.M(d)) establishes dom(Σ₀.M(d)) = ∅") is proof strategy — it describes *how* the invariant is established, not *what* the invariant asserts. The property narrative states the invariant as: "For each document `d`, `dom(Σ.M(d))` is finite." The formal contract expands beyond this by including induction base-case detail.

**Required**: Remove the base-case clause from the formal contract so the invariant field states only the invariant:

```
*Formal Contract:*
- *Invariant:* dom(Σ.M(d)) is finite for every document d and every reachable state Σ.
```

### D-CTG

**Checking the proof of D-CTG against the verification checklist.**

The construction is sound: w is well-defined for all j ∈ {2, …, m−1}, the ordering arguments are correct, T0(a) supplies unboundedly many n, and T3 distinguishes the resulting tumblers. The postcondition follows correctly from the contradiction with S8-fin.

However, there is a dependency gap:

```
RESULT: FOUND

**Problem**: The proof explicitly invokes T1(i) twice — "By T1(i), w > v₁" and
"By T1(i), w < v₂" — to establish that lexicographic comparison is decided by
the first differing component. T1(i) is not listed among the declared
dependencies (S8-fin, S8-depth, T0(a), T3). Without T1(i), the two ordering
claims are unjustified.

**Required**: Add T1(i) (LexicographicOrder, ASN-0034) to the dependency list
for D-CTG.
```

### S3

I'll verify S3's proof against the checklist.

**1. Precondition completeness** — The proof assumes S1 and an "initial-state axiom (Σ.M(d))" establishing `dom(Σ₀.M(d)) = ∅`. Both are stated. Per-operation obligations are transparently described. ✓

**2. Case coverage** — Three cases for `v ∈ dom(Σ'.M(d))`: retained, new-to-existing, atomic-create. Modified mappings (where `v ∈ dom(Σ.M(d))` but the value changes) fall under Cases 2 or 3 depending on whether the new target is in `dom(Σ.C)` or freshly created. The exhaustiveness argument confirms: `a ∈ dom(Σ.C)` or `a ∈ A` (fresh), and the fourth case (`a ∉ dom(Σ'.C)`) is explicitly excluded as a per-operation obligation. ✓

**3. Postcondition establishment** — The proof establishes `Σ'.M(d)(v) ∈ dom(Σ'.C)` for arbitrary `d`, `v` in every case. ✓

**4. All conjuncts addressed** — Single universal quantifier; both base case and inductive step proved. ✓

**5. Dependency correctness** — S1 is declared and used in Cases 1 and 2 and the exhaustiveness argument. The initial-state axiom for M(d) is used in the base case but not listed as a dependency — this may be an intra-ASN axiom, so borderline. S0, S8-fin, and D-CTG are mentioned only as analogies, not used logically. ✓

**6. Formal contract** — **Problem identified.** S3 is proved by induction over state transitions (base case + inductive step), which is the standard invariant proof pattern. The formal contract labels it as `*Axiom:*`. Compare with S1, which has an identical proof structure (invariant across transitions, derived from a precondition) and is correctly labeled:

> S1: `*Preconditions:* S0 … *Invariant:* For every state transition …`

S3's proof depends on S1 (for Case 1: retained mappings remain valid because `dom(Σ.C) ⊆ dom(Σ'.C)`). Without S1, Case 1 fails — content deletion could strand a retained reference. S3 is therefore not a standalone axiom; it is an invariant whose preservation depends on S1 as a precondition. The per-operation verification obligation (new/modified mappings must target existing or concurrently-created addresses) is also a precondition, not captured in the contract's field structure.

**7. Missing guarantees** — No missing guarantees beyond the formal contract issue above. ✓

---

```
RESULT: FOUND

**Problem**: The formal contract labels S3 as `*Axiom:*` but the proof establishes it as an invariant by induction, depending on S1 as a precondition. This is inconsistent with the proof structure and with S1's own contract, which uses `*Preconditions:* + *Invariant:*` for an analogous inductive proof. The current contract also buries S1 and the per-operation obligation in prose rather than listing them as structured fields.

**Required**: Replace the formal contract with:
- *Preconditions:* S1 (store monotonicity); initial-state axiom (Σ.M(d)) establishing dom(Σ₀.M(d)) = ∅; per-operation verification obligation — every operation that sets Σ'.M(d)(v) = a must ensure a ∈ dom(Σ'.C).
- *Invariant:* `(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))` — every V-reference resolves.
```

24 verified, 3 found.
