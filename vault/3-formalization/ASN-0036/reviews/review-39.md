# Proof Review — ASN-0036 (cycle 2)

*2026-04-12 17:00*

23 properties (D-CTG, D-CTG-depth, D-MIN, D-SEQ, OrdAddHom, OrdAddS8a, OrdShiftHom, S0, S1, S2, S3, S5, S6, S7, S7a, S7b, S7c, S8, S8-depth, S8-fin, S8a, S9, ValidInsertionPosition)

### S8-depth

Looking at S8-depth against the checklist:

**Checklist 1–4 (Preconditions, Cases, Postconditions, Conjuncts):** S8-depth is declared as an axiom (design requirement), not a derived property. The axiom formula is self-contained and well-formed. No proof is needed, so case coverage and postcondition establishment don't apply.

**Checklist 5 (Dependency correctness):** The section cites S7c and OrdinalShift for the correspondence-run analysis in the narrative. These are used correctly for I-address claims. However, the subspace-preservation claim for **V-positions** does not actually follow from any cited dependency (see item 7).

**Checklist 6 (Formal contract):** The axiom formula in the formal contract matches the property statement exactly. Axiom is the correct classification. No issue here.

**Checklist 7 (Missing guarantees):** The narrative states:

> "for V-positions, the subspace identifier `v₁` is before the action point and is copied unchanged by TumblerAdd's prefix rule"

The action point of `δ(k, #v)` is `#v`. For position 1 to be strictly before the action point, we need `1 < #v`, i.e., `#v ≥ 2`. No provided dependency establishes this:

- **S8-depth** itself guarantees depth *uniformity* within a subspace, not a minimum depth. All V-positions in a subspace could have `#v = 1`.
- **S7c** establishes element-field depth ≥ 2 for **I-addresses**, not V-positions.
- **OrdinalShift** imposes no minimum depth on its input.

If `#v = 1`, then `v = [s]` where `s` is the subspace identifier, and `shift(v, k)` changes `s` itself — the ordinal shift *is* a subspace change. The correspondence-run analysis (which assumes ordinal shifts stay within a subspace for V-positions) breaks down at depth 1.

The narrative cites Gregory's evidence ("V-addresses consistently use the form `s.x` — two tumbler digits") but this is empirical, not a formal dependency. A property establishing `#v ≥ 2` for all `v ∈ dom(Σ.M(d))` is needed.

```
RESULT: FOUND

**Problem**: The narrative claims subspace preservation for V-positions under ordinal shift
("the subspace identifier v₁ is before the action point and is copied unchanged"), but this
requires #v ≥ 2, which no cited dependency establishes. S8-depth guarantees depth uniformity,
not a minimum depth. At #v = 1, OrdinalShift's action point coincides with the subspace
identifier, so shift(v, k) changes the subspace — invalidating the correspondence-run
subspace-preservation claim.

**Required**: A formal property (e.g., "S8-vdepth" or a precondition on S8-depth) establishing
that all V-positions have depth ≥ 2: (A d, v : v ∈ dom(Σ.M(d)) : #v ≥ 2). Alternatively,
add this as a precondition to the formal contract and list it as a dependency requirement.
```

### D-CTG-depth

I need to verify D-CTG-depth against the checklist.

**1. Precondition completeness** — The preconditions (V_S(d) non-empty, depth m ≥ 3 via S8-depth, D-CTG, S8-fin) are sufficient for the proof. ✓

**2. Case coverage** — The proof handles disagreement at any j ∈ {2, …, m−1}. Component 1 is excluded because both positions share subspace S. Component m is the last component (the desired reduction target). All cases covered. ✓

**3. Postcondition establishment** — The contradiction rules out any disagreement at j ∈ {2, …, m−1}, establishing the shared-prefix claim. The reduction to last-component contiguity follows directly. ✓

**4. All conjuncts addressed** — Both parts of the postcondition (shared components 2 through m−1, and reduction to last component) are established. ✓

**5. Dependency correctness** — The proof invokes **T1(i) (LexicographicOrder, ASN-0034)** three times:
- To establish that the first disagreeing component j satisfies (v₁)ⱼ < (v₂)ⱼ
- To show w > v₁ (disagreement at j+1 with w_{j+1} > (v₁)_{j+1})
- To show w < v₂ (disagreement at j with wⱼ < (v₂)ⱼ)

T1(i) is **not declared in the dependencies**. It is used but not provided. All other declared dependencies (D-CTG, S8-depth, S8-fin, T0(a), T3, T4) are referenced in the property section.

**6. Formal contract** — Matches the narrative. Preconditions and postconditions are correctly stated. ✓

**7. Missing guarantees** — T1(i) is the missing declared dependency (see item 5). No other undeclared assumptions found. The construction of w, the ordering arguments, the infinity argument via T0(a), and the distinctness argument via T3 are all sound given T1(i).

```
RESULT: FOUND

**Problem**: T1(i) (LexicographicOrder, ASN-0034) is used three times in the proof
but is not declared as a dependency. The proof relies on it to establish (1) that
v₁ < v₂ with first disagreement at j implies (v₁)ⱼ < (v₂)ⱼ, (2) w > v₁ via
disagreement at j+1, and (3) w < v₂ via disagreement at j. Without T1(i) in the
dependency list, the ordering arguments cannot be formally grounded.

**Required**: Add T1(i) (LexicographicOrder, ASN-0034) to the declared dependencies
for D-CTG-depth.
```

### ValidInsertionPosition

## Verification of ValidInsertionPosition

**Checking precondition completeness…**

The non-empty case opens with "V_S(d) ≠ ∅ with |V_S(d)| = N" and then uses N as a natural number throughout (ranging j from 0 to N, counting "N + 1 valid insertion positions," postcondition (iv) "pairwise distinct"). For |V_S(d)| = N to yield a natural number, V_S(d) must be finite. That finiteness comes from **S8-fin** (dom(M(d)) is finite). S8-fin is neither listed in the formal contract's preconditions nor provided among the dependencies.

This is not merely transitive: D-CTG and D-MIN do not imply finiteness on their own. D-MIN's own postcondition explicitly says "Combined with D-CTG **and S8-fin**, V_S(d) = {[S, 1, …, 1, k] : 1 ≤ k ≤ n} for some **finite** n ≥ 1." The ValidInsertionPosition proof relies on exactly this derived form (valid positions are [S, 1, …, 1+j] for 0 ≤ j ≤ N) without declaring S8-fin as a precondition.

**All other checks pass:**
- Case coverage: non-empty and empty cases fully handled, boundaries (j = 0, j = N, N = 1) sound.
- Postcondition establishment: all four postconditions (depth, subspace, S8a, distinctness) explicitly proved for both cases.
- All conjuncts addressed: (i)–(iv) each shown with concrete reasoning.
- Dependency correctness: D-MIN, OrdinalShift, TumblerAdd, T3, S8-depth, S8a all correctly invoked; no undeclared dependencies beyond S8-fin.
- Formal contract structure: Definition + Preconditions + Postconditions fields appropriate for a definition with verified properties.

```
RESULT: FOUND

**Problem**: S8-fin (finiteness of dom(M(d))) is missing from both the
formal contract preconditions and the dependency list. The non-empty case
defines "|V_S(d)| = N" and uses N as a natural number (0 ≤ j ≤ N,
"N + 1 valid insertion positions," postcondition (iv)). Without S8-fin,
V_S(d) could be infinite, making N undefined and the definition ill-formed.
D-MIN's own postcondition explicitly requires S8-fin to derive the general
form V_S(d) = {[S, 1, …, 1, k] : 1 ≤ k ≤ n}, which this proof relies on.

**Required**: Add S8-fin to the formal contract preconditions:
  "d satisfies D-CTG, D-MIN, S8-depth, S8a, S8-fin; S ≥ 1; …"
and include S8-fin in the dependency list.
```

### OrdAddHom

## Verification of OrdAddHom

**Main proof (postcondition (a))**: The component-wise argument is correct. Both `ord(v ⊕ w)` and `ord(v) ⊕ w_ord` expand to `[v₂, ..., v_{k-1}, vₖ + wₖ, w_{k+1}, ..., wₘ]` via TumblerAdd, and the preconditions for both TumblerAdd applications are properly established (`w_ord > 0`, `actionPoint(w_ord) = k-1 ≤ m-1 = #ord(v)`). Edge cases (`k=2`, `k=m`, `m=2`) all reduce correctly. Both instances check out.

**Postcondition (b)**: Correctly follows from TumblerAdd — since `k ≥ 2`, the copy-from-start rule gives `r₁ = v₁`. Only uses TumblerAdd (declared). Sound.

**Postcondition (c)**: The inline justification invokes **"the generalized inverse (vpos contract (b))"** — the property that `vpos(subspace(r), ord(r)) = r` for `#r ≥ 2`. This is explicitly named as an external contract but is **not listed in the Dependencies section**. Only TumblerAdd and TA0 are declared.

```
RESULT: FOUND

**Problem**: Postcondition (c) in the formal contract references "vpos contract (b)" — the generalized inverse property `vpos(subspace(r), ord(r)) = r` — which is not declared in the Dependencies section. The exact text: "so the generalized inverse (vpos contract (b)) applies to r: vpos(subspace(r), ord(r)) = r". This is an undeclared dependency: the proof names a specific external contract by label but does not list it among its dependencies.

**Required**: Add the vpos inverse property (wherever "vpos contract (b)" is formally stated) to the Dependencies section for OrdAddHom, so that postcondition (c) is traceable to its grounds.
```

19 verified, 4 found.
